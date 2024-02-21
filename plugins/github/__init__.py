import asyncio
import datetime
import json
import os.path
import random

import pytz
import requests
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Message

from config import Config

cfg = Config()

driver = get_driver()


def get_now(time):
    time_obj = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    # 将datetime对象的时区设置为UTC
    time_obj_utc = time_obj.replace(tzinfo=pytz.UTC)
    # 将时区从UTC转换为北京时间
    bj_timezone = pytz.timezone('Asia/Shanghai')
    time_obj_bj = time_obj_utc.astimezone(bj_timezone)
    # 格式化输出北京时间
    bj_time_str = time_obj_bj.strftime('%Y-%m-%d %H:%M:%S')
    return bj_time_str


@driver.on_bot_connect
async def _(bot: Bot):
    if not cfg.rec_group:
        return
    while True:
        for repo in cfg.github_repo:
            url = f"https://api.github.com/repos/{repo}/commits"
            if cfg.github_pat_token:
                headers = {"Authorization": f"token {cfg.github_pat_token}"}
            else:
                headers = {}
            response = requests.get(url, headers=headers)
            commits = response.json()
            # 在这里，每一次对api进行访问会返回一个包含这个仓库所有commit记录的json文件
            # 每一次commit都有一个独特的sha指纹，可以通过这个指纹来辨识对应的commit
            # 在本地将每一次commit的sha指纹进行存储来辨认哪个commit是更新发生的
            if not os.path.exists('./commits_sha.json'):
                with open('./commits_sha.json', 'w', encoding='utf-8') as f:
                    # 如果没有指纹文件，那么将本次获取的所有commits记录的指纹进行保存
                    sha_list = []
                    # 遍历返回的json来获取其中的sha指纹
                    for commit in commits:
                        sha_list.append(commit['sha'])
                    f.write(json.dumps(sha_list, indent=2, ensure_ascii=False))
                    f.close()
                    continue
            # 如果本地已经有了对应的sha指纹记录，那么将这一次获取到的结果进行记录和添加
            with open('./commits_sha.json', 'r', encoding='utf-8') as f:
                # 检测到空文件时直接将sha_list传入空列表
                if f.read() == '':
                    sha_list = []
                else:
                    # 重置游标
                    f.seek(0)
                    sha_list: list = json.loads(f.read())
            for commit in commits:
                sha = commit['sha']
                if sha in sha_list:
                    continue
                else:
                    # 检测到了不存在的sha指纹，说明这个commit记录是新的。
                    # 获取这个commit的信息
                    committer = commit['commit']['author']
                    commiter_name = committer['name']
                    commiter_email = committer['email']
                    commit_date = committer['date']
                    commit_msg = commit['commit']['message']
                    # 生成推送消息
                    push_msg = (f'检测到：\n{repo}\n有新的Commit!\n'
                                f'======\n'
                                f'{commit_msg}\n'
                                f'推送者：{commiter_name}\n'
                                # f'推送者邮箱：{commiter_email}\n'
                                f'推送时间：{get_now(commit_date)}')
                    # 遍历所有接受消息的群
                    for group in cfg.rec_group:
                        await bot.send_group_msg(group_id=group, message=push_msg)
                        await asyncio.sleep(1.2)
                    sha_list.append(sha)
                    # 保存sha指纹列表
                    with open('./commits_sha.json', 'w', encoding='utf-8') as f:
                        f.write(json.dumps(sha_list, indent=2, ensure_ascii=False))
                        f.close()
                    await asyncio.sleep(random.uniform(0.4, 1.5))
                    continue
            # 使这个任务休眠，实现频率控制
        await asyncio.sleep(cfg.github_api_freq)

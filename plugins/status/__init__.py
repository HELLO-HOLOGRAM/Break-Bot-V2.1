from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Message

import psutil
import platform
import cpuinfo

from config import Config

# 初始化读取配置文件
cfg = Config()
mem = psutil.virtual_memory()
used_mem = mem.used / 1024 / 1024 / 1024
total_mem = mem.total / 1024 / 1024 / 1024

status = on_command(' status', priority=10, block=True)


@status.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.group_id in cfg.group_whitelist:
        dist_name = '' if platform.system() == 'Windows' else f'发行版： {platform.dist()}\n'
        cpu_info = cpuinfo.get_cpu_info()
        status_text = (f"Break Bot V2.1 - ({cfg.bot_name})\n"
                       f"===基础信息===\n"
                       f"- 当前版本：{cfg.version}\n"
                       f"- 数据库连接状态：Bad!\n"
                       f"- Break Net连接状态：Bad!\n"
                       f"===主机信息===\n"
                       f"- 处理器型号：{cpu_info['brand_raw']}\n"
                       f"- 基准频率：{'%.2f'%(cpu_info['hz_actual'][0] / 1000000000)}GHz\n"
                       f"- 内核数：{psutil.cpu_count(logical=False)}c/{psutil.cpu_count()}t\n"
                       f"- 总内存：{'%.1f' % total_mem}G\n"
                       f"- 操作系统：{platform.system()}\n"
                       f"{dist_name}"
                       f"- 架构：{cpu_info['arch_string_raw']}（{cpu_info['arch']}）\n"
                       f"===运行状态===\n"
                       f"- CPU使用率：{'%.1f' % psutil.cpu_percent(interval=0.1, percpu=False)}%\n"
                       f"- 内存占用：{'%.1f' % used_mem}G/{'%.1f' % total_mem}G\n")
        await status.send(Message(status_text))


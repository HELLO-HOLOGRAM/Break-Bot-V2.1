import os.path
import yaml


class Config:
    # 项目默认值
    bot_name = 'break-bot'
    version = '2.1'

    # remote-client默认值
    client_address = 'http://127.0.0.1:8050'

    # MongoDB Server默认值
    db_ip = '127.0.0.1'
    db_port = 27017
    db_is_auth = False
    db_username = 'breakbot'
    db_passwd = ''

    # Bot通讯设置默认值
    ws_host = '0.0.0.0'
    ws_port = 12345
    onebot_token = 'break'
    command_start = '/'
    command_sep = " "
    command_prefix = 'ctn'

    # bot权限设置默认值
    super_user = [1234567890]
    group_whitelist = [9876543210]
    group_superlist = [1122334455]

    # github推送设置
    github_repo = ['HELLO-HOLOGRAM/Break-Bot-V2.1']
    rec_group = []
    github_pat_token = ''
    github_api_freq = '120'

    def __init__(self):
        # 初始化时检测是否存在配置文件
        if not os.path.exists('./bot_config.yml'):
            # 没有则先生成
            self.gen_config()
        # 读取配置文件
        self.get_config()
        # 生成环境配置文件
        self.create_env()

    def gen_config(self):
        # 生成一个配置文件
        config = (f"# Auto Generate By BreakBotV2.1\n\n"
                  f"# --项目名称--\n"
                  f"# 这个配置只会影响一部分地方显示的项目名称，改不改似乎都没什么区别\n"
                  f"bot-name: {self.bot_name}\n"
                  f"version: {self.version}\n"
                  f"\n"
                  f"# --Remote Client设置--\n"
                  f"# 配置模拟Client的连接地址\n"
                  f"# 本地运行一般无须修改，远程连接请修改成对应的url\n"
                  f"# 请不要在url的末尾添加'/'!\n"
                  f"client-address: {self.client_address}\n"
                  f"\n"
                  f"# --MongoDB设置--\n"
                  f"# 配置数据库的连接地址\n"
                  f"db-ip: {self.db_ip}\n"
                  f"db-port: {self.db_port}\n"
                  f"\n"
                  f"# 配置认证相关设置，如果不启用mongoDB的认证就不需要使用账号密码登录，但是非常不安全！\n"
                  f"# 一般建议启用数据库的用户认证功能！\n"
                  f"db-is-auth: {self.db_is_auth}\n"
                  f"db-username: {self.db_username}\n"
                  f"db-passwd: {self.db_passwd}\n"
                  f"\n"
                  f"# --Bot设置--\n"
                  f"# Bot在使用时需要通过反向websocket连接来和客户端进行通信\n"
                  f"# 具体配置详见https://onebot.adapters.nonebot.dev/docs/guide/setup\n"
                  f"# 设置反向ws通讯主机，一般设置为0.0.0.0，如果仅在本地运行可以使用127.0.0.1\n"
                  f"ws-host: {self.ws_host}\n"
                  f"ws-port: {self.ws_port}\n"
                  f"\n"
                  f"# 设置验证token\n"
                  f"onebot-token: {self.onebot_token}\n"
                  f"\n"
                  f"# 命令的前缀，分割，\n"
                  f"cmd-start: {self.command_start}\n"
                  f"cmd-sep: '{self.command_sep}'\n"
                  f"cmd-prefix: {self.command_prefix}\n"
                  f"\n"
                  f"# --权限设置--\n"
                  f"# SUPERUSER超级用户，可以使用bot的所有限制功能\n"
                  f"super-user: {self.super_user}\n"
                  f"\n"
                  f"# 群白名单\n"
                  f"#仅在群白名单列表中的群可以触发bot\n"
                  f"group-whitelist: {self.group_whitelist}\n"
                  f"\n"
                  f"# 高级群权限名单\n"
                  f"# 这个列表中的群会自动加入白名单中，请不要和群白名单重复！\n"
                  f"# 拥有这个权限的群可以使用bot的一部分限制功能\n"
                  f"group-superlist: {self.group_superlist}\n"
                  f"\n"
                  f"# --Github推送设置--\n"
                  f"# 用于设置对github仓库的更新推送检测\n"
                  f"\n"
                  f"# 监测信息发送到的群聊，如果设置为空则关闭该功能\n"
                  f"rec-group: {self.rec_group}"
                  f"\n"
                  f"# 监测的github仓库\n"
                  f"# 可以为多个仓库，但是如果设置了多个仓库请务必将github api的访问频率设置的更大，防止触发api的访问频率上限\n"
                  f"github-repo: {self.github_repo}\n"
                  f"\n"
                  f"# Github个人访问令牌（PAT）设置\n"
                  f"# 设置PAT后可以访问拥有对应权限的私有仓库的commit记录，同时可以享有更大的api访问频率限制，可以为空\n"
                  f"github-pat-token: {self.github_pat_token}\n"
                  f"\n"
                  f"# Github API访问频率，单位为秒，默认为两分钟进行一次检测\n"
                  f"# 默认情况下Github API的访问频率上限为每小时60次，在设置了个人令牌后可以达到每小时5000次\n"
                  f"# 使用时建议设置个人令牌\n"
                  f"github-api-freq: {self.github_api_freq}\n")
        with open('./bot_config.yml', 'w', encoding='utf-8') as f:
            f.write(config)
            f.close()

    def get_config(self):
        """
        调用这个方法会使Config实例重新读取config.yaml。
        :return: None
        """
        # 读取配置文件
        with open('./bot_config.yml', 'r', encoding='utf-8') as file:
            cfgs = yaml.load(file, Loader=yaml.FullLoader)
            file.close()
        # 赋值
        self.bot_name = cfgs['bot-name']
        self.version = cfgs['version']
        self.client_address = cfgs['client-address']
        self.db_ip = cfgs['db-ip']
        self.db_port = cfgs['db-port']
        self.db_is_auth = cfgs['db-is-auth']
        self.db_username = cfgs['db-username']
        self.db_passwd = cfgs['db-passwd']
        self.ws_host = cfgs['ws-host']
        self.ws_port = cfgs['ws-port']
        self.onebot_token = cfgs['onebot-token']
        self.command_start = cfgs['cmd-start'] + cfgs['cmd-prefix']
        self.command_sep = cfgs['cmd-sep']
        self.command_prefix = cfgs['cmd-prefix']
        self.super_user = cfgs['super-user']
        self.group_whitelist: list = cfgs['group-whitelist']
        self.group_whitelist.extend(cfgs['group-superlist'])
        self.group_superlist = cfgs['group-superlist']
        self.github_repo = cfgs['github-repo']
        self.github_pat_token = cfgs['github-pat-token']
        self.github_api_freq = cfgs['github-api-freq']
        self.rec_group = cfgs['rec-group']

    def create_env(self):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(f'DRIVER=~quart+~httpx+~websockets\n'
                    f'HOST={self.ws_host}\n'
                    f'PORT={self.ws_port}\n'
                    f'COMMAND_START=["{self.command_start}"]\n'
                    f'COMMAND_SEP=["{self.command_sep}"]\n'
                    f'ONEBOT_ACCESS_TOKEN={self.onebot_token}\n')
            f.close()

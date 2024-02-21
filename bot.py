import os
import sys

import nonebot
import cmd
import threading
from nonebot.adapters.onebot.v11 import Adapter as ConsoleAdapter  # 避免重复命名

from config import Config

cfg = Config()

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ConsoleAdapter)

# 在这里加载插件
nonebot.load_plugins("./plugins")

if __name__ == "__main__":
    nonebot.run()

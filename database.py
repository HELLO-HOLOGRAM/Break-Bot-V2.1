import pymongo

from config import Config

cfg = Config()


class DBConnect:
    def __init__(self):
        # 连接状态指示
        self.is_connected = False
        # 传入连接
        self.client = None
        pass

    def connect(self):
        try:
            # 建立到数据库的连接
            if cfg.db_is_auth:
                client = pymongo.MongoClient(
                    f'mongodb://{cfg.db_username}:{cfg.db_passwd}@{cfg.db_ip}:{cfg.db_port}/?authSource=admin'
                )
            else:
                client = pymongo.MongoClient(
                    f'mongodb://{cfg.db_ip}:{cfg.db_port}/?authSource=admin'
                )
            self.is_connected = True
            # 检测数据库中是否包含指定的集合
            if client.breaknet is not None:
                # 不包含时建立指定的集合
                new_cle = client['breaknet']
            self.client = client
        except Exception as e:
            # 接受可能出现的错误
            print(str(e))
            self.is_connected = False

    async def init_db(self):
        pass


conn = DBConnect()
conn.connect()
if conn.client.breaknet is None:
    print(1)
else:
    print(2)

# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:21 下午 
# @Author  : xujunpeng
import os
from config import config
from utils.logger import logger
from table import create_mydb_database

"""
项目初始化，创建数据库目录
1. 数据库项目创建
2. 数据库配置创建
    2.1 创建初始用户
    2.2 创建初始DB信息
    
"""


class Init:
    def __init__(self):
        # 执行init操作
        # 检查db目录是否创建
        logger.info("init now")
        self.check_db_dir()
        # 检查数据库的配置文件是否存在
        self.init_mydb()

    def check_db_dir(self):
        if not os.path.exists(config.DB_PATH):
            logger.info("db not exist, make db dir:{} now".format(config.DB_PATH))
            os.mkdir(config.DB_PATH)
            logger.info("make db dir:{} finish".format(config.DB_PATH))

    def init_mydb(self):
        # 初始化数据库
        # 创建用户信息

        filename = config.DATABASE_INFO_TABLE_PATH
        if not os.path.exists(filename):
            logger.info("file:{} not exist, make now".format(filename))
            create_mydb_database()


if __name__ == '__main__':
    Init()

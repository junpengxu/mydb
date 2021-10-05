# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:16 下午 
# @Author  : xujunpeng

"""
数据表相关操作
"""
import json
from db import DB
from config import config
from bplustree.serializer import StrSerializer


def create_mydb_database():
    """
    存放所有的表结构schema信息
    :return:
    :rtype:
    """
    # 1. 创建schema的表添加用户表schema
    with DB(filename=config.SCHEMA_TABLE_PATH, serializer=StrSerializer()) as f:
        # 创建user表
        user_table_schema = json.dumps([
            {"column": "username", "type": "string", "primary_key": True},
            {"column": "password", "type": "string"}
        ])
        # 创建表结构, 一条数据包含两部分，表名(str)+结构(map)，表名做B+树的key
        f.insert(config.ADMIN_TABLE_NAME, user_table_schema)

    # 2.创建user表，插入root用户
    with DB(filename=config.ADMIN_TABLE_PATH, serializer=StrSerializer()) as f:
        f.insert(key="root", value="root")

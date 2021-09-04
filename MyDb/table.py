# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:16 下午 
# @Author  : xujunpeng

"""
数据表相关操作
"""
import os
from config import config
from exception import *
import json
import bplustree


# 创建数据表
def create_table(table_name):
    """
    1. 数据表已经存在，则不能继续创建
    2. 建表
    :param table_name:
    :type table_name:
    :return:
    :rtype:
    """
    if not table_name:
        raise TableExistError()
    # 名称检查， mydb_user, mydb 这两个表不应该被创建
    if table_name in [config.DATABASE_INFO_TABLE]:
        raise TableNameError()
    with open(config.DB_PATH + table_name, "w"):
        pass


def create_mydb_database():
    """
    存放所有的表结构schema信息
    :return:
    :rtype:
    """

    def format_database_schema_data(*args):
        return config.DATABASE_SCHEMA_SEG.join(args)

    def format_table_data(*args):
        return config.TABLE_DATA_SEG.join(args)

    user_table_name = config.MYDB_USER_TABLE
    user_table_schema = json.dumps([
        {"column": "id", "type": "int", "auto_increate": True},
        {"column": "username", "type": "string"},
        {"column": "password", "type": "string"}
    ])
    with open(config.DATABASE_INFO_TABLE_PATH, "w") as f:
        # 创建表结构, 一条数据包含两部分，表名(str)+结构(map)
        # 插入用户表结构
        data = format_database_schema_data(user_table_name, user_table_schema)
        f.write(data)

    # 创建用户表，插入管理员信息
    if os.path.exists(config.DATABASE_USER_TABLE_PATH):
        raise TableExistError()
    else:
        with open(config.DATABASE_USER_TABLE_PATH, "w") as f:
            # 找到用户表结构的schema信息
            _user_table_schema = None
            # 避免读取大文件
            with open(config.DATABASE_INFO_TABLE_PATH, "r") as ff:
                for item in ff:
                    name, schema = item.split(config.DATABASE_SCHEMA_SEG)
                    if name == config.MYDB_USER_TABLE:
                        _user_table_schema = json.loads(schema)
                        break
            if not _user_table_schema:
                raise SchemaNotFountError()

            # 创建数据, 一条数据包含两部分，表名(str)+结构(map)
            master_user_info = {"username": "root", "password": "root", "id": 1}
            insert_data = []
            for item in _user_table_schema:
                # 按顺序插入
                column_name = item["column"]
                column_type = item["type"]
                if item["column"] in master_user_info:
                    tmp = master_user_info[column_name]
                else:
                    tmp = 0 if column_type == "int" else ""
                # TODO 判断自增ID
                # 取出文件的最后一行， 检查ID, 那要是批量插入可咋整？所以还是有必要使用一个专门的插入函数来做这件事情
                # 使用了特殊的分割符号，那么整数不能被拼接到字符串上该怎么办呢
                insert_data.append(str(tmp))
            f.write(format_table_data(*insert_data))

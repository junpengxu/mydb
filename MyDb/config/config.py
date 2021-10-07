# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:23 下午
# @Author  : xujunpeng
import os

DB_PATH = "/tmp/mydb/"
SCHEMA_TABLE = "schema.db"
ADMIN_TABLE = "user.db"
ADMIN_TABLE_NAME = "user"
SCHEMA_TABLE_PATH = DB_PATH + SCHEMA_TABLE
ADMIN_TABLE_PATH = DB_PATH + ADMIN_TABLE
TABLE_DATA_SEG = "&*&"  # 这是个最笨的分割方式

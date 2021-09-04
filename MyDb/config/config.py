# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:23 下午 
# @Author  : xujunpeng
import os

DB_PATH = "/tmp/mydb/"
DATABASE_SCHEMA_SEG = "|"  # 所以建表的时候不能存在特殊字符
TABLE_DATA_SEG = "|-|"  # 所以插入数据之前要判断好特殊的字符，或者是使用更好的数据分割方式
DATABASE_INFO_TABLE = "mydb"
MYDB_USER_TABLE = "mydb_user"
DATABASE_INFO_TABLE_PATH = DB_PATH + DATABASE_INFO_TABLE
DATABASE_USER_TABLE_PATH = DB_PATH + MYDB_USER_TABLE

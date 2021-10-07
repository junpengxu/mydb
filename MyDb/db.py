# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 2:54 下午 
# @Author  : xujunpeng
import json
import traceback
from utils.logger import logger
from bplustree import BPlusTree
from bplustree.serializer import StrSerializer, IntSerializer, UUIDSerializer, DatetimeUTCSerializer
from MyDb.config import config


class DB(BPlusTree):

    def __init__(self, *args, **kwargs):
        self.filename = kwargs["filename"]
        self.schema = json.loads(self.load_db_schema())
        kwargs["filename"] = config.DB_PATH + kwargs["filename"] + ".db"
        kwargs["serializer"] = self.get_serializer_type()
        super(DB, self).__init__(*args, **kwargs)

    def load_db_schema(self):
        with BPlusTree(filename=config.SCHEMA_TABLE_PATH, serializer=StrSerializer()) as f:
            return f.get(self.filename)

    def get_serializer_type(self):
        for item in self.schema:
            if item.get("primary_key"):
                if item["type"] == "string":
                    return StrSerializer()
                elif item["type"] == "int":
                    return IntSerializer()
                elif item["type"] == "uuid":
                    return UUIDSerializer()
                elif item["type"] == "datetime":
                    return DatetimeUTCSerializer()

    def get_primary_key_column(self):
        primary_key_column = None
        for item in self.schema:
            if item.get("primary_key"):
                primary_key_column = item["column"]
        return primary_key_column

    def insert(self, values, key=None, replace=False):
        # 1. 查找主键
        # 2. 拼装insert的value
        """ insert into table (column1, column2) value() """
        insert_column = []  # 具体写入顺序
        for item in self.schema:
            # 找到了主键,一定会有主键
            if item.get("primary_key"):
                key = values.get(item["column"])
            else:
                insert_column.append(values.get(item["column"]))
        super(DB, self).insert(key=key, value=config.TABLE_DATA_SEG.join(insert_column).encode())

    def select(self, column=None, x=None):
        """ select * from table where column = x; """
        result = []
        # 1. 判断查询的column在schema的索引下标
        # 2. 遍历数据，返回命中结果
        try:
            for key, record in self.items():
                # 判断select * 的情况
                # key 与 value 要拼接到一起，当作一行数据来看到
                record = record.decode().split(config.TABLE_DATA_SEG)
                record.insert(0, key)
                if not column:
                    # 判断 column 相等的情况
                    result.append(record)
                else:
                    column_index = self.find_column_index(column)
                    if x == record[column_index]:
                        result.append(record)
            return result
        except Exception as e:
            pass
        return result

    def update(self):
        """ update table set column = x where column = x; """
        pass

    def delete(self):
        """ delete from table where column = x; """
        pass

    def find_column_index(self, column):
        for index, item in enumerate(self.schema):
            if item["column"] == column:
                return index
        raise IndexError

# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 2:54 下午 
# @Author  : xujunpeng
from bplustree import BPlusTree
from bplustree.serializer import StrSerializer
from MyDb.config import config


class DB(BPlusTree):

    def __init__(self, *args, **kwargs):
        super(DB, self).__init__(*args, **kwargs)

    def load_db_schema(self, filename):
        with DB(filename=config.SCHEMA_TABLE_PATH, serializer=StrSerializer()) as f:
            return f.get(filename)

    def insert(self, key, value, replace=False):
        super(DB, self).insert(key=key, value=value.encode())

    def select(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 11:19 上午 
# @Author  : xujunpeng
import asyncio
import json
import time
import re

from db import DB


class Broker:
    def __init__(self, unregister=None):
        self.unregister = unregister

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, conn):
        self._conn = conn

    def read(self, conn, mask):
        try:  # 抛出客户端强制关闭的异常（如手动关闭客户端黑窗口）
            data = self.recv()
            if data:
                self.handle(data.decode())
            else:
                raise Exception("no data")
        except Exception as e:
            print('Client closed.', self.conn)
            self.close()
            self.unregister(self.conn)

    def recv(self):
        return self.conn.recv(8192)

    def close(self):
        self.conn.close()

    def response(self, data):
        self.conn.sendall(data.encode())

    def handle(self, data: str):
        sql = data.split(" ")
        option = sql[0]
        if option == "select":
            self.handle_select(sql)
        elif option == "update":
            self.handle_update(sql)
        elif option == "delete":
            self.handle_delete(sql)
        elif option == "insert":
            self.handle_insert(sql)

    def handle_select(self, sql):
        """ select * from table where column = x; """
        """ select * from table; """
        table = sql[3].strip(";")
        column = None if len(sql) <= 4 else sql[5]
        x = None if len(sql) <= 4 else sql[7].strip(";")
        with DB(filename=table) as db:
            res = db.select(column=column, x=x)
            print(res)
            self.response(json.dumps(res))

    def handle_update(self, sql):
        pass

    def handle_delete(self, sql):
        pass

    def handle_insert(self, sql):
        # sql = """ insert into user (username, password) value (xjp, xjp) """
        table = sql[2]
        pattern = re.compile(r"(?<=\().*?(?=\))")
        match = pattern.findall(" ".join(sql))
        columns = match[0].split(",")
        columns = [item.strip() for item in columns]
        values = match[1].split(",")
        values = [item.strip() for item in values]
        values = {column: value for column, value in zip(columns, values)}
        with DB(filename=table) as db:
            res = db.insert(values)
            print(res)
            self.response(json.dumps(res))

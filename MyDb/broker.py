# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 11:19 上午 
# @Author  : xujunpeng
import asyncio
import time


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
        pass

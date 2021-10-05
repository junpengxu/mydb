# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:08 下午 
# @Author  : xujunpeng

"""
服务端
"""

import selectors
import socket

import init_database
from broker import Broker
import asyncio
from gevent.pool import Pool
from gevent import monkey


monkey.patch_all()


class Server:
    def __init__(self, host="localhost", port=1235):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(128)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)
        self.loop = asyncio.get_event_loop()
        self.pool = Pool(1024)
        print("init db")
        init_database.Init()

    def callback(self, conn, data):
        conn.send(data)

    def accept(self, socket, mask):
        conn, addr = socket.accept()
        print('accepted', conn, 'from', addr)
        # 设置非阻塞模式
        conn.setblocking(False)
        # 再次注册一个连接，将其加入监测列表中，
        broker = self.init_broker(conn)
        # 控制最大连接数量
        self.sel.register(conn, selectors.EVENT_READ, broker.read)

    def init_broker(self, conn):
        broker = Broker(unregister=self.unregiste_conn)
        broker.conn = conn
        return broker

    def unregiste_conn(self, conn):
        self.sel.unregister(conn)

    def close_server(self):
        self.sel.close()

    def run(self):
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    # 会根据连接来决定调用accept或者read
                    callback = key.data
                    self.pool.apply_async(func=callback, args=(key.fileobj, mask), callback=None)
                    # 协程执行的会慢一些， register broker.read方法会慢一些，造成sel.select()阻塞
                    # callback(key.fileobj, mask)
        except Exception as e:
            self.close_server()
            print(e)



if __name__ == '__main__':
    try:
        Server(port=1235).run()
    except Exception as e:
        print(e)

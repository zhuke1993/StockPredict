__author__ = 'MALONG'
# coding=utf-8
import socket
import threading
import time
import DataUtil
import Logging
import logging


def tcplink(sock, addr):
    logging.info('Accept new connection from %s:%s...' % addr)
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if len(data) != 0:
            logging.info("Accept the data = %s" % (data))
            params = data.split("&")
            start = params[0].split("=")[1]
            end = params[1].split("=")[1]
            json = DataUtil.getDataPredict(start, end)
            sock.send(json)
        else:
            sock.close()
        return


def startServer():
    # 创建一个基于IPv4和TCP协议的Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    while (True):
        logging.info("Server startup success, waiting for new connection.....")
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

if __name__ == "__main__":
    startServer()

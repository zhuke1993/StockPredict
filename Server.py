__author__ = 'MALONG'
# coding=utf-8
import socket
import threading
import time
import DataUtil
import Logging
import logging
import StockPredict


def tcplink(sock, addr):
    logging.info('Accept new connection from %s:%s...' % addr)
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if len(data) != 0:
            logging.info("Accept the data = %s" % (data))
            try:
                params = data.split("&")
                start = params[0].split("=")[1]
                end = params[1].split("=")[1]
                json = StockPredict.predict(start, end)
                sock.send(json)
                logging.info("Sending data to %s, %s" % (addr, json))
            except BaseException:
                logging.error("Occured an exception")
                pass
        else:
            pass
        return


def startServer():
    # 创建一个基于IPv4和TCP协议的Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('zhuke1993.vicp.cc', 9999))
    s.listen(5)
    logging.info("Server startup success, waiting for new connection.....")
    while (True):
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


if __name__ == "__main__":
    startServer()

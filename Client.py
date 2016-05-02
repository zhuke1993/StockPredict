__author__ = 'MALONG'
# coding=utf-8
import socket

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s1.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
param = "start='2015-01-01'&end='2016-05-04'"
s1.send(param)

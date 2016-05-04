__author__ = 'MALONG'
# coding = utf-8
import Server
import StockPredict
import threading
import StockPredict
import time
import logging
import Logging


def updateDateDaily():
    while (True):
        if (time.localtime().tm_hour == 0) & (time.localtime().tm_min == 1) & (time.localtime().tm_sec == 0):
            # update the new day data
            logging.info("Updating daily data...")
            StockPredict.updateHistoryData(
                buildDayStr(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday))


def buildDayStr(year, month, day):
    if len(str(month)) == 1:
        month = "0" + str(month)
    if len(str(day)) == 1:
        day = "0" + str(day)
    return str(year) + "-" + str(month) + "-" + str(day)


def startServer():
    Server.startServer()


if __name__ == "__main__":
    StockPredict.updateModel((0.001, 3))

    t1 = threading.Thread(target=startServer())
    t2 = threading.Thread(target=updateDateDaily())
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()

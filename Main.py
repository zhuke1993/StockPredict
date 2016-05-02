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


if __name__ == "__main__":
    threading.Thread(target=updateDateDaily()).start()
    Server.startServer()


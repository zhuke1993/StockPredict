__author__ = 'MALONG'
# coding=utf-8
from sqlalchemy import Column, String, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import tushare as ts
import demjson
import Logging
import logging

BaseModel = declarative_base()


# date：日期
# open：开盘价
# high：最高价
# close：收盘价
# low：最低价
# volume：成交量
# price_change：价格变动
# p_change：涨跌幅
# ma5：5日均价
# ma10：10日均价
# ma20:20日均价
# v_ma5:5日均量
# v_ma10:10日均量
# v_ma20:20日均量
class StockData(BaseModel):
    __tablename__ = "stock_predict"
    date = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    close = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    price_change = Column(Float)
    p_change = Column(Float)
    ma5 = Column(Float)
    ma10 = Column(Float)
    ma20 = Column(Float)
    v_ma5 = Column(Float)
    v_ma10 = Column(Float)
    v_ma20 = Column(Float)


# 获得mysql会话连接
def getDBSession(url):
    engine = getDBEngine(url)
    return sessionmaker(bind=engine)


# 创建一个mysql连接引擎
def getDBEngine(url):
    return create_engine(url)


# 得到start-end期间的数据，并追加到数据库表中
def updateHistoryData(start, end):
    df = ts.get_hist_data('sh', start=start, end=end)
    engine = getDBEngine('mysql://root:929184318@127.0.0.1:3306/stock_predict?charset=utf8')
    # 存入数据库
    df.to_sql('stock_data', engine, if_exists='append')
    logging.info("Successed update the data, start = %s and end = %s" % (start, end))
    return df

# 得到start-end期间的data数据
def getData(start, end):
    engine = create_engine('mysql://root:929184318@127.0.0.1:3306/stock_predict?charset=utf8')
    sql = "select * from stock_data where date between '%s' and '%s'  order by date asc" % (start, end)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    list = session.execute(sql).fetchall()
    dataList = []
    for i in list:
        stockData = StockData(date=i[0], open=i[1], high=i[2], close=i[3], low=i[4], volume=i[5], price_change=i[6],
                              p_change=i[7], ma5=i[8], ma10=i[9], ma20=i[10], v_ma5=i[11], v_ma10=i[12], v_ma20=i[13])
        dataList.append(stockData)
    return dataList


def getDataPredict(start, end):
    engine = create_engine('mysql://root:929184318@127.0.0.1:3306/stock_predict?charset=utf8')
    sql = "select date, close from stock_data_predict where date between '%s' and '%s' order by date asc" % (start, end)
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    list = session.execute(sql).fetchall()
    return demjson.encode(list)


if __name__ == "__main__":
    print getDataPredict("2005-01-01", "2016-05-01")

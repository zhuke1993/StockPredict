__author__ = 'MALONG'
# coding=utf-8
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot
from sklearn.externals import joblib
import Logging
import logging

from DataUtil import *

model_g = ""

list = getData("2013-05-02", "2016-01-01")
x_train = []
y_train = []
for i in list:
    x_t = [i.open, i.ma5, i.ma10, i.ma20, i.v_ma5, i.v_ma10, i.v_ma20]
    x_train.append(x_t)
    y_train.append(i.close)

list1 = getData("2016-01-02", "2016-05-01")
x_test = []
y_test = []
for i in list1:
    x_t1 = [i.open, i.ma5, i.ma10, i.ma20, i.v_ma5, i.v_ma10, i.v_ma20]
    x_test.append(x_t1)
    y_test.append(i.close)


def getErrorValue(param):
    model = RandomForestRegressor(n_estimators=500, oob_score=True, n_jobs=-1, max_features=param[0],
                                  min_samples_leaf=param[1])
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    return ((y_predict - y_test) ** 2).sum()


def updateModel(param):
    model = RandomForestRegressor(n_estimators=500, oob_score=True, n_jobs=-1, max_features=param[0],
                                  min_samples_leaf=param[1])
    model.fit(x_train, y_train)
    joblib.dump(model, "model/model.pkl", compress=3)
    model_g = model
    print model_g
    logging.info("Successed update model file.")


def caculate():
    x_xies = range(653)
    model = RandomForestRegressor(n_estimators=1000, oob_score=True, n_jobs=-1,
                                  max_features=0.001, min_samples_leaf=3)
    model.fit(x_train, y_train)
    y_predict = model.predict(x_train)
    pyplot.plot(x_xies, y_train)
    pyplot.plot(x_xies, y_predict)
    pyplot.show()


if __name__ == "__main__":
    updateModel((0.001, 3))

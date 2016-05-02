__author__ = 'MALONG'
# coding=utf-8
from random import uniform, randint

import numpy as np
import logging
import Logging

import StockPredict

# 惯性权重
weight = 0.8

# 分别是粒子的个体和社会的学习因子，也称为加速常数
lr = (2, 2)

# 最大迭代次数
maxgen = 300

# 种群规模
sizepop = 50

# 粒子的位置范围限制
range_max_features = (0.001, 0.8)
range_min_samples_leaf = (1, 100)

# 粒子的速度范围限制
rangespeed = (-2, 2)

gbestpop = np.zeros((1, 2))
gbestfitness = 10000000000
pbestpop = np.zeros((sizepop, 2))
pbestfitness = range(1000000000, 1000000000 + sizepop)


def func(x):
    return StockPredict.getErrorValue(x)


def initpopvfit(sizepop):
    pop = np.zeros((sizepop, 2))
    v = np.zeros((sizepop, 2))
    fitness = np.zeros(sizepop)

    for i in range(sizepop):
        pop[i] = [uniform(0, 1) + 0.0000001, randint(0, 100) + 1]
        v[i] = [uniform(-2, 2), uniform(-2, 2)]
        fitness[i] = func(pop[i])
    return pop, v, fitness


def getinitbest(fitness, pop):
    global gbestpop, gbestfitness, pbestpop, pbestfitness

    # 群体最优的粒子位置及其适应度值
    gbestpop, gbestfitness = pop[fitness.argmin()], fitness.min()
    # 个体最优的粒子位置及其适应度值,使用copy()使得对pop的改变不影响pbestpop，pbestfitness类似
    pbestpop, pbestfitness = pop.copy(), fitness.copy()


def beginPSO():
    pop, v, fitness = initpopvfit(sizepop)
    getinitbest(fitness, pop)
    global gbestpop, gbestfitness, pbestpop, pbestfitness
    for j in range(maxgen):
        # 速度更新
        for j in range(sizepop):
            v[j] += lr[0] * np.random.rand() * (pbestpop[j] - pop[j]) + lr[1] * np.random.rand() * (gbestpop - pop[j])

        # 速度是否越界
        for j in range(sizepop):
            for k in range(2):
                if v[j][k] < rangespeed[0]:
                    v[j][k] = rangespeed[0]
                if v[j][k] > rangespeed[1]:
                    v[j][k] = rangespeed[1]

        # 粒子位置更新
        for j in range(sizepop):
            pop[j] = pop[j] + v[j]

        for j in range(sizepop):
            pop[j][1] = int(pop[j][1])

        # 位置是否越界
        for j in range(sizepop):
            if pop[j][0] < range_max_features[0]:
                pop[j][0] = range_max_features[0]
            if pop[j][0] > range_max_features[1]:
                pop[j][0] = range_max_features[1]
            if pop[j][1] < range_min_samples_leaf[0]:
                pop[j][1] = range_min_samples_leaf[0]
            if pop[j][1] > range_min_samples_leaf[1]:
                pop[j][1] = range_min_samples_leaf[1]

        # 适应度更新
        for j in range(sizepop):
            fitness[j] = func(pop[j])

        for j in range(sizepop):
            if fitness[j] < pbestfitness[j]:
                pbestfitness[j] = fitness[j]
                pbestpop[j] = pop[j].copy()

        if pbestfitness.min() < gbestfitness:
            gbestfitness = pbestfitness.min()
            gbestpop = pop[pbestfitness.argmin()].copy()
            logging.info(
                "Update the gbestfitness = ".join(gbestfitness).join(" , gbestpop").join(gbestpop[0]).join(",").join(
                    gbestpop[1]))


def getBestParam():
    beginPSO()
    return gbestpop, gbestfitness


if __name__ == "__main__":
    print getBestParam()

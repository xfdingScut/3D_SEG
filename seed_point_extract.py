# -*- coding:utf-8 -*-
# @Time    : 2018/10/18 上午10:47
# @Author  : Ding Xiao Fang
# @File    : seed_point_extract.py
# @Software: PyCharm


import numpy as np
from scipy.signal import argrelextrema
import random
import point_and_seed as ps
from matplotlib import pyplot as plt


def hist(im_data):
    [z, y, x] = im_data.shape
    # 创建直方图统计字典
    minG = int(im_data.min())
    maxG = int(im_data.max())
    d = dict()
    for d_i in range(minG, maxG+1):
        d[d_i] = list()
    for k in range(z):
        for j in range(y):
            for i in range(x):
                gray = int(im_data[k, j, i])
                if gray not in d.keys():
                    d[gray] = list()
                d[gray].append([k, j, i])
    return d


def wavelet_hist(im_data):
    [z, y, x] = im_data.shape
    # 创建直方图统计字典
    d = dict()
    for d_i in range(256):
        d[d_i] = list()
    for k in range(z):
        for j in range(y):
            for i in range(x):
                if im_data[k, j, i] != 0:
                    tmp = np.floor(im_data[k, j, i] + 0.5)
                    d[tmp].append([k, j, i])
    return d


def seed_extract(dic):
    seed_list = list()
    count_array = np.zeros(len(dic))
    # print min(dic.keys())
    plt.figure("hist")
    for i in range(len(dic)):
        # print dic[i-min(dic.keys())]
        count_array[i] = len(dic[i + min(dic.keys())])
        plt.bar(i + min(dic.keys()), count_array[i], fc='b')
    plt.show()


    # # 直方图局部最小值所处的像素值
    # less_extrema = np.array([])
    # less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[0:140], np.less, order=6)))
    # less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[140:180], np.less, order=4)) + 140)
    # less_extrema = np.append(less_extrema, np.array(argrelextrema(count_array[180:], np.less, order=6)) + 180)
    # # 直方图局部最大值所处的像素值
    # greater_extrema = np.array([])
    # greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[0:140], np.greater, order=5)))
    # # greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[70:140], np.greater, order=3)) + 70)
    # greater_extrema = np.append(greater_extrema, np.array(argrelextrema(count_array[140:], np.greater, order=3)) + 140)
    #
    # ##################################
    # # plt.figure("hist")
    # # # for i in range(len(dic)):
    # # #     plt.bar(i, len(dic[i]), fc='b')
    # # # print less_extrema
    # # for i in range(len(less_extrema)):
    # #     plt.plot(less_extrema[i], len(dic[less_extrema[i]]), 'r.')
    # # for i in range(len(greater_extrema)):
    # #     plt.plot(greater_extrema[i], len(dic[greater_extrema[i]]), 'g.')
    # # # plt.plot(greater_extrema, greater_result, 'g.')
    # # plt.show()
    # ##################################
    #
    # index = 0
    # last_seed_lower = 0
    # for j in range(greater_extrema.size):
    #     for i in range(less_extrema.size-1):
    #         if greater_extrema[j] < less_extrema[i]:
    #             break
    #         if less_extrema[i] < greater_extrema[j] < less_extrema[i+1]:
    #             index += 1
    #             seed_total = np.array(dic[greater_extrema[j]])
    #             seed_zyx = np.array(random.sample(seed_total, 3))
    #             if len(seed_list) == 0:
    #                 seed_list.append(ps.Seed(seed_zyx, less_extrema[i], less_extrema[i+1], index))
    #                 last_seed_lower = less_extrema[i]
    #             elif last_seed_lower != less_extrema[i]:
    #                 seed_list.append(ps.Seed(seed_zyx, less_extrema[i], less_extrema[i+1], index))
    #                 last_seed_lower = less_extrema[i]
    #             continue
    # return seed_list
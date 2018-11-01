# -*- coding:utf-8 -*-
# @Time    : 2018/10/29 3:59 PM
# @Author  : Ding Xiao Fang
# @File    : save_data.py
# @Software: PyCharm


import os


def write_txt(filename, data):
    filepath = os.getcwd() + "/mid_data/" + filename + ".txt"
    with open(filepath, 'w') as f:
        f.writelines(" ".join(str(i) for i in data))


def read_txt(filename):
    filepath = os.getcwd() + "/mid_data/" + filename + ".txt"
    with open(filepath, 'r') as f:
        data = f.read()
    data = list(data.split())
    # print data
    return map(float, data)

# write_txt("mid",[1,2,3])
# print read_txt("mid")

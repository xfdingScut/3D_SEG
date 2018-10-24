# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 上午10:00
# @Author  : Ding Xiao Fang
# @File    : edge_detection.py
# @Software: PyCharm


import numpy as np
import point_and_seed as ps
import itertools


def edge_detection(coeffs):
    """
    :param coeffs: 小波变化后获得的高低频信息
    coeffs = [aaa, (aad, ada, daa, add, dad, dda, ddd), (aad2, ada2, daa2, add2, dad2, dda2, ddd2)]
    """
    image_data = coeffs
    image_edge = roberts(image_data)
    # 注释掉的这部分就是分别对小波变化后获得垂直、水平高频分量采用sobel算子，对角分量采用Roberts算子进行边缘检测，最终返回各个结果的并集
    # image_edge1 = sobel(coeffs[1]['aad'])
    # image_edge2 = sobel(coeffs[1]['ada'])
    # image_edge3 = sobel(coeffs[1]['daa'])
    # image_edge4 = roberts(coeffs[1]['add'])
    # image_edge5 = roberts(coeffs[1]['dad'])
    # image_edge6 = roberts(coeffs[1]['dda'])
    # image_edge7 = roberts(coeffs[1]['ddd'])
    # image_edge = (image_edge1 + image_edge2 + image_edge3 + image_edge4 + image_edge5 +image_edge6 + image_edge7)/7.0

    # sitk.Show(sitk.GetImageFromArray(image_edge1), 'aad_sobel')
    # sitk.Show(sitk.GetImageFromArray(image_edge2), 'ada_sobel')
    # sitk.Show(sitk.GetImageFromArray(image_edge3), 'daa_sobel')
    # sitk.Show(sitk.GetImageFromArray(image_edge4), 'add_roberts')
    # sitk.Show(sitk.GetImageFromArray(image_edge5), 'dad_roberts')
    # sitk.Show(sitk.GetImageFromArray(image_edge6), 'dda_roberts')
    # sitk.Show(sitk.GetImageFromArray(image_edge7), 'ddd_roberts')
    return image_edge


def sobel(im_data):
    """
    3D-sobel：
    """
    sobel_op = ps.sobel_operator()
    [lenZ, lenY, lenX] = im_data.shape
    image_edge = np.zeros((lenZ, lenY, lenX))
    # 扩展三维数据[lenZ, lenY, lenX]->[lenZ+2, lenY+2, lenX+2]
    image_new = np.zeros((lenZ + 2, lenY + 2, lenX + 2))
    image_new[0, 1:(lenY + 1), 1:(lenX + 1)] = im_data[0, :, :]
    image_new[1:(lenZ + 1), 1:(lenY + 1), 1:(lenX + 1)] = im_data
    image_new[(lenZ + 1), 1:(lenY + 1), 1:(lenX + 1)] = im_data[(lenZ - 1), :, :]

    image_index = np.array(list(itertools.product(range(lenZ, lenY, lenX))))
    c = lambda x: cal_gradient_roberts(image_new, sobel_op, x)
    g = np.array(list(map(c, image_index)))  # 计算
    modify_index = image_index[g > 0]
    image_edge[modify_index[:, 0], modify_index[:, 1], modify_index[:, 2]] = g[g > 0]

    return image_edge


def cal_gradient_sobel(im_data, operator, image_index, z, y, x):
    """
    用sobel算子对每个体素计算梯度，用于边缘检测
    """
    dim = image_index.shape[1]  # 索引为三维
    operator_x = operator.operator_x
    operator_y = operator.operator_y
    operator_z = operator.operator_z
    super_point = im_data[z:(z + 3), y:(y + 3), x:(x + 3)]
    gx = np.sum(super_point * operator_x)
    gy = np.sum(super_point * operator_y)
    gz = np.sum(super_point * operator_z)
    g = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    return g


def cal_gradient_roberts(im_data, operator, z, y, x):
    """
    用Roberts算子对每个体素计算梯度，用于边缘检测
    """
    operator_x = operator.operator_x
    operator_y = operator.operator_y
    operator_z = operator.operator_z
    super_point = im_data[z:(z + 2), y:(y + 2), x:(x + 2)]
    gx = np.sum(super_point * operator_x)
    gy = np.sum(super_point * operator_y)
    gz = np.sum(super_point * operator_z)
    g = np.abs(gx) + np.abs(gy) + np.abs(gz)
    g = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    return g


def roberts(im_data):
    """
    3D-Roberts算子:
    """
    roberts_op = ps.roberts_operator()
    [lenZ, lenY, lenX] = im_data.shape
    image_edge = np.zeros((lenZ, lenY, lenX))
    # 扩展三维数据[lenZ, lenY, lenX]->[lenZ+1, lenY+1, lenX+1]
    image_new = np.zeros((lenZ + 1, lenY + 1, lenX + 1))
    image_new[0:lenZ, 0:lenY, 0:lenX] = im_data
    image_new[lenZ, 0:lenY, 0:lenX] = im_data[(lenZ - 1), :, :]
    for k in range(lenZ):
        for j in range(lenY):
            for i in range(lenX):
                g = cal_gradient_roberts(image_new, roberts_op, k, j, i)
                image_edge[k, j, i] = g
    return image_edge


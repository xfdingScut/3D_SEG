# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 上午10:00
# @Author  : Ding Xiao Fang
# @File    : preprocess.py
# @Software: PyCharm


import numpy as np
import SimpleITK as sitk
import pywt


def read_dcm2array(path_dcm):
    if path_dcm is None:
        path_dcm = '/Users/potato/Pictures/project_image/head'
    reader = sitk.ImageSeriesReader()
    filenames = reader.GetGDCMSeriesFileNames(path_dcm)
    reader.SetFileNames(filenames)
    img_original = reader.Execute()
    image = sitk.GetArrayFromImage(img_original)  # Z,Y,X
    image_array = np.array(image)
    return image_array


def cw(im_data):
    # CT图像数据重新调整，转换为HU值
    fRescaleSlope = 1.0
    fRescaleIntercept = -1024
    imageU = im_data * fRescaleSlope + fRescaleIntercept
    # 图像调窗
    width = 985.0  # 窗宽
    level = -679.0  # 窗位
    imageCW = imageU
    im_shape = imageU.shape
    lenZ = im_shape[0]
    lenY = im_shape[1]
    lenX = im_shape[2]
    for k in range(lenZ):
        for i in range(lenY):
            for j in range(lenX):
                if imageCW[k, i, j] < level - width / 2.0:
                    imageCW[k, i, j] = 0.0
                else:
                    if imageCW[k, i, j] > level + width / 2.0:
                        imageCW[k, i, j] = 255.0
                    else:
                        imageCW[k, i, j] = (imageU[k, i, j] + width / 2.0 - level) * 255.0 / width
    return imageCW


def wavelet2(im_data):
    db1 = pywt.Wavelet('db1')
    # 多尺度小波变化，返回值分别为[低频分量，(水平高频，垂直高频，对角线高频)]
    [cA2, (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(im_data, db1, mode='symmetric', level=2)
    return cA2


def wavelet3(im_data):
    # coeffs = [aaa, (aad, ada, daa, add, dad, dda, ddd), (aad2, ada2, daa2, add2, dad2, dda2, ddd2)]
    coeffs = pywt.wavedecn(im_data, 'db1', level=2)
    # im1 = coeffs[1]["ddd"]
    # im1[im1<50] = 0
    # im2 = coeffs[1]["aad"] + coeffs[1]["ada"] + coeffs[1]["daa"] + \
    #       coeffs[1]["add"] + coeffs[1]["dad"] + coeffs[1]["dda"] + coeffs[1]["ddd"]
    #
    # sitk.Show(sitk.GetImageFromArray(im1))
    # # sitk.Show(sitk.GetImageFromArray(im1 - (im1-im2)))
    return coeffs


def wavelet_cw(im_data):
    [z, y, x] = im_data.shape
    for k in range(z):
        min = np.amin(im_data[k, :, :])
        max = np.amax(im_data[k, :, :])
        for i in range(y):
            for j in range(x):
                im_data[k, i, j] = (im_data[k, i, j] - min) * 255.0 / (max - min)
    return im_data


def image_reduce_dim(im_data):
    [z, y, x] = im_data.shape
    img_reduce = np.zeros([z, y/4, x/4])
    for h in range(y/4):
        for w in range(x/4):
            j = h * 4
            i = w * 4
            tmp = (im_data[:, j, i] + im_data[:, j + 1, i] + im_data[:, j, i + 1] + im_data[:, j + 1, i + 1]) / 4.0
            img_reduce[:, h, w] = tmp
    return img_reduce


def write_txt(im_data):
    [lenZ, lenY, lenX] = im_data.shape
    write_data = list()
    for k in range(lenZ):
        for j in range(lenY):
            for i in range(lenX):
                if im_data[k, j, i] != 0:
                    write_data.append('%-5d%-5d%-5d  %-3d\n' % (i, j, k, 1))
    filepath = '/Users/xiaofang/Desktop/image_data_new.txt'
    with open(filepath, 'w') as f:
        f.write('[(x, y, z), class_index]: 体素三维坐标和所属类别\n')
        f.writelines(write_data)





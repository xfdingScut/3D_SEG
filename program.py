# -*- coding:utf-8 -*-
# @Time    : 2018/10/18 上午10:00
# @Author  : Ding Xiao Fang
# @File    : program.py
# @Software: PyCharm

import numpy as np
import preprocess
import seed_point_extract as extract
import segmentation as seg
import volumerendering
import edge_detection as edge
import SimpleITK as sitk
import vtk


def start(filedir):
    read = preprocess.read_dcm2array(filedir)
    image_reduce = preprocess.image_reduce_dim(read)
    # image_cw = preprocess.cw(read)
    # image_wav = preprocess.wavelet3(read)
    # image_edge = sitk.CannyEdgeDetection(sitk.Cast(sitk.GetImageFromArray(read), sitk.sitkFloat32), lowerThreshold=0.0,
    #                    upperThreshold=200.0, variance=(5.0, 5.0, 5.0))
    image_edge = sitk.SobelEdgeDetection(sitk.Cast(sitk.GetImageFromArray(read), sitk.sitkFloat32))
    # edge_wav = preprocess.wavelet3(sitk.GetArrayFromImage(image_edge))
    # sitk.Show(sitk.GetImageFromArray(image_wav[0]))
    # # image_edge = edge.edge_detection(coeffs)
    # sitk.Show(sitk.GetImageFromArray(image_reduce))
    d = extract.hist(image_reduce)

    seed_tmp = extract.seed_extract(d)
    # image_reduce = preprocess.wavelet_cw(coeffs[0])
    # d = extract.wavelet_hist(image_reduce)
    # # # d = hist(image_cw)
    # seed_tmp = extract.seed_extract(d)
    # volume = []
    # grow_mark_all = np.zeros(image_wav[0].shape)
    # for i in range(len(seed_tmp)):
    #     seed_list_tmp = seed_tmp[i]
    #     # print seed_list_tmp.seed_zyx, seed_list_tmp.lower, seed_list_tmp.upper
    #     image_grow = seg.growwithedge(image_wav[0], seed_list_tmp, grow_mark_all, image_edge[0])
    #     volume.append(volumerendering.show(image_grow, i))
    # # print len(volume)
    # volume.append(volumerendering.show(grow_mark_all, i+1))
    # return volume


if __name__ == "__main__":
    vol = start("/Users/potato/Pictures/project_image/head_test/")
    ren = vtk.vtkRenderer()
    iren = vtk.vtkRenderWindowInteractor()
    iren.GetRenderWindow().AddRenderer(ren)
    ren.AddActor(vol[0])
    iren.Initialize()


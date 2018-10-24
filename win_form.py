# -*- coding:utf-8 -*-
# @Time    : 2018/9/12 上午3:35
# @Author  : Ding Xiao Fang
# @File    : win_form.py
# @Software: PyCharm

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
import vtk
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QFileDialog
import program
import iteration

class Form(QtWidgets.QMainWindow):

    def __init__(self,volume, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.volume = volume
        # self.cb = []
        self.initUI()
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.resize(2560, 1600)
        # 生成组件
        self.centralWidget = QtWidgets.QWidget(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.btn_select = QtWidgets.QPushButton("选择DICOM目录")
        self.btn_select.clicked.connect(self.btn1_clicked)
        self.listbox = QtWidgets.QListWidget()
        self.listbox.setSelectionMode(QAbstractItemView.MultiSelection)

        self.listbox.clicked.connect(self.cb_state)
        # 创建VTK布局
        self.childLayout_vtk = QtWidgets.QGridLayout()
        self.childLayout_vtk.addWidget(self.vtkWidget)

        # 创建区域子布局
        self.childLayout_cb = QtWidgets.QVBoxLayout()
        self.childLayout_cb .addWidget(self.listbox)
        self.childLayout_cb.addStretch()

        # 创建区域子布局
        self.childLayout_button = QtWidgets.QVBoxLayout()
        self.childLayout_button.addWidget(self.btn_select)
        self.childLayout_button.addLayout(self.childLayout_cb)
        self.childLayout_button.setSpacing(1)

        # 创建父布局
        self.setCentralWidget(self.centralWidget)
        self.parentLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.parentLayout.addLayout(self.childLayout_vtk, 0, 0)
        self.parentLayout.addLayout(self.childLayout_button, 0, 1,0,3)

    def show_gui(self):
        if self.volume is not None:
            for i in range(len(self.volume)):
                self.ren.AddActor(self.volume[i])

    def btn1_clicked(self):
        filedir = QFileDialog.getExistingDirectory()
        print filedir
        if filedir is not None and len(filedir) != 0:
            self.volume = program.start(str(filedir) + "/")
            if self.volume is not None:
                for i in range(len(self.volume)):
                    self.ren.AddActor(self.volume[i])
                    self.listbox.addItem("组件"+str(i))
            self.iren.Initialize()

    def cb_state(self):
        if self.volume is not None:
            # self.ren.RemoveActor()
            for i in range((self.listbox.count())):
                print i,self.listbox.item(i).isSelected()
                if self.listbox.item(i).isSelected():
                    self.ren.AddActor(self.volume[i])
                else:
                    self.ren.RemoveActor(self.volume[i])
        #
        self.iren.Initialize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Form(None)
    window.show()
    sys.exit(app.exec_())
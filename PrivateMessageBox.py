# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 16:04:02 2018

@author: 肖建斌

@Function: 一个私人订制的无边框MessageBox
"""

import sys
import os
import math

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDesktopWidget

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import *


class PrivateMessageBox(QWidget):
    """一个无边框MessageBox"""
    def __init__(self, **kwargs):
        super(PrivateMessageBox, self).__init__(None, Qt.FramelessWindowHint)  # 设置为顶级窗口，无边框
        self.contentLabel = QLabel(self)  # 主信息界面
        self.titleLabel = QLabel(self.contentLabel)  # 标题窗
        self.imageLabel = QLabel(self.contentLabel)  # 提示图
        self.textLabel = QLabel(self.contentLabel)  # 内容窗
        self.buttonLabel = QLabel(self.contentLabel)  # 按钮窗
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.kwargs = kwargs
        self.initUI()  # 初始化界面

    def initUI(self):
        """初始化界面函数"""
        self.setObjectName('mainWindows')  # 设置变量名
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口透明
        self.setFixedSize(700, 240)  # 锁定窗口大小
        self.setWindowOpacity(0.98)  # 设置透明度0.95
        file = QFile('\\'.join((os.getcwd(), 'QSS', 'PrivateMessageBox.css')))  # QSS文件
        file.open(QFile.ReadOnly)  # 打开文件
        styleSheet = str(file.readAll(), encoding='gbk')  # 读取文件
        self.setStyleSheet(styleSheet)  # 应用样式表
        self._move_center()  # 将窗口居中
        self.contentLabel.setGeometry(10, 10, self.width()-20, self.height()-20)  # 设置内容界面大小及位置
        self.contentLabel.setAutoFillBackground(True)  # 设置背景图自动填充
        self.contentLabel.setPixmap(QPixmap('\\'.join([os.getcwd(), 'Images', 'MessageBox',
                                                       'Background.jpg'])))  # 设置主背景图
        self.contentLabel.setMouseTracking(True)  # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self.titleLabel.setGeometry(0, 0, self.contentLabel.width(), 40)  # 设置标题窗大小及位置
        self.titleLabel.setIndent(10)  # 设置标题栏文本缩进
        self.titleLabel.setMouseTracking(True)  # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置标题左对齐并居中显示
        self.imageLabel.setGeometry(30, 60,
                                    self.contentLabel.height()-120, self.contentLabel.height()-120)  # 设置标题窗大小及位置
        self.imageLabel.setAlignment(Qt.AlignCenter)  # 设置标题左对齐并居中显示
        self.textLabel.setObjectName('textLabel')  # 设置变量名称
        self.textLabel.setGeometry(self.imageLabel.width()+30, 45,
                                   self.contentLabel.width()-self.imageLabel.width()-65,
                                   self.contentLabel.height()-90)  # 设置标题窗大小及位置
        self.textLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置标题左对齐并居中显示
        # self.textLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)  # 使便签文字可被选择
        self._init_title()

    def _init_title(self):
        if 'window' in self.kwargs:  # 如果存在主界面
            icon_label = QLabel(self.titleLabel)  # 右上角主界面图标
            icon_label.setGeometry(5, 0, 40, 40)  # 设置图标位置
            icon = self.kwargs['window'].windowIcon()  # 获取主界面图标
            icon_label.setPixmap(icon.pixmap(36, 36))  # 指定图标大小并设置图标
            icon_label.setMouseTracking(True)  # 设置鼠标追随
            name_label = QLabel(self.titleLabel)  # 有上角主界面名称
            name_label.setMouseTracking(True)  # 设置鼠标追随
            name_label.setObjectName('titleText')  # 设置变量名
            name_label.setGeometry(48, 0, self.titleLabel.width()-90, 40)  # 设置位置及大小
            self.titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置标题左对齐并居中显示
            name = self.kwargs['window'].windowTitle()  # 获取主界面名称
            name_label.setText(name)  # 设置内容
        close_button = QPushButton(self.titleLabel)  # 左上角关闭按钮
        close_button.setObjectName('closeButton')  # 设置变量名
        close_button.setGeometry(self.titleLabel.width()-40, 0, 40, 40)
        close_button.setText(b'\xef\x81\xb2'.decode("utf-8"))
        close_button.setFlat(True)  # 设置按钮透明
        close_button.setToolTip('关闭')
        close_button.clicked.connect(self.close)  # 绑定关闭命令

    def _move_center(self):
        """窗口屏幕居中显示函数，打开程序自动执行"""
        qr = self.frameGeometry()  # 得到主窗口的大小
        cp = QDesktopWidget().availableGeometry().center()  # 得到显示器的分辨率并得到中间点的位置
        qr.moveCenter(cp)  # 将自己的中心点放到qr的中心点
        self.move(qr.topLeft())  # 将窗口的左上角移动到qr的左上角
        self.move(self.x(), self.y() - 100)

    def _close_animation(self):
        self.animation.setDuration(500)  # 动画时间
        self.animation.setStartValue(1)  # 开始值
        self.animation.setEndValue(0)  # 结束值
        self.animation.start()  # 开始动画
        self.animation.finished.connect(self.close)  # 动画结束后绑定命令

    def information(self, message):
        pix = '\\'.join((os.getcwd(), 'Images', 'MessageBox', 'Information.png'))
        painter = QPixmap(pix)
        self.imageLabel.setPixmap(painter.scaled(QSize(64, 64)))  # 自动调整提示图片大小为64*64
        self.textLabel.setText(''.join(['提示：', str(message)]))
        ensure_button = QPushButton(self.contentLabel)  # 设置命令键
        ensure_button.setObjectName('commandButton')  # 命名
        ensure_button.setGeometry(self.contentLabel.width()-110, self.contentLabel.height()-40, 85, 35)  # 设置键位置及大小
        ensure_button.setText('确定')  # 设置内容
        ensure_button.clicked.connect(self._close_animation)
        self.show()  # 显示界面

    def error(self, message):
        pix = '\\'.join((os.getcwd(), 'Images', 'MessageBox', 'Error.png'))
        painter = QPixmap(pix)
        self.imageLabel.setPixmap(painter.scaled(QSize(64, 64)))  # 自动调整提示图片大小为64*64
        self.textLabel.setText(''.join(['错误：', str(message)]))
        ensure_button = QPushButton(self.contentLabel)  # 设置命令键
        ensure_button.setObjectName('commandButton')  # 命名
        ensure_button.setGeometry(self.contentLabel.width() - 110, self.contentLabel.height() - 40, 85, 35)  # 设置键位置及大小
        ensure_button.setText('确定')  # 设置内容
        ensure_button.clicked.connect(self._close_animation)  # 绑定关闭命令
        self.show()  # 显示界面

    def warning(self, message):
        pix = '\\'.join((os.getcwd(), 'Images', 'MessageBox', 'Warning.png'))
        painter = QPixmap(pix)
        self.imageLabel.setPixmap(painter.scaled(QSize(64, 64)))  # 自动调整提示图片大小为64*64
        self.textLabel.setText(''.join(['警告：', str(message)]))
        ensure_button = QPushButton(self.contentLabel)  # 设置命令键
        ensure_button.setObjectName('commandButton')  # 命名
        ensure_button.setGeometry(self.contentLabel.width() - 110, self.contentLabel.height() - 40, 85, 35)  # 设置键位置及大小
        ensure_button.setText('确定')  # 设置内容
        ensure_button.clicked.connect(self._close_animation)  # 绑定关闭命令
        self.show()  # 显示界面

    def select(self, message):
        pix = '\\'.join((os.getcwd(), 'Images', 'MessageBox', 'Select.png'))
        painter = QPixmap(pix)
        self.imageLabel.setPixmap(painter.scaled(QSize(64, 64)))  # 自动调整提示图片大小为64*64
        self.textLabel.setText(''.join(['提示：', str(message)]))
        ensure_button = QPushButton(self.contentLabel)  # 设置命令键
        ensure_button.setObjectName('commandButton')  # 命名
        ensure_button.setGeometry(self.contentLabel.width() - 110, self.contentLabel.height() - 40, 85, 35)  # 设置键位置及大小
        ensure_button.setText('确定')  # 设置内容
        ensure_button.clicked.connect(self._close_animation)  # 绑定关闭命令
        self.show()  # 显示界面

    def mousePressEvent(self, event):
        self.move_DragPosition = event.globalPos() - self.pos()
        event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 标题栏拖放窗口位置
        self.move(QMouseEvent.globalPos() - self.move_DragPosition)
        QMouseEvent.accept()

    def paintEvent(self, event):
        """重写绘画事件，为窗口添加阴影"""
        m = 10
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRect(m, m, self.width() - m * 2, self.height() - m * 2)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(Qt.white))
        color = QColor(100, 100, 100, 50)
        for i in range(m):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRoundedRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2, 1, 1)
            color.setAlpha(int(150 - math.sqrt(i) * 50))
            painter.setPen(QPen(color, 1, Qt.SolidLine))
            painter.drawRoundedRect(QRect(m - i, m - i, self.width() - (m - i) * 2, self.height() - (m - i) * 2), 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QLabel()
    mainWindow.setWindowTitle('测试界面')
    mainWindow.setWindowIcon(QIcon('\\'.join((os.getcwd(), 'Images', 'MessageBox',
                                              'TestMainWindow.ico'))))
    text = '\n\t白日依山尽，\n\t黄河入海流。\n\t欲穷千里目，\n\t更上一层楼。'
    messageBox0 = PrivateMessageBox(window=mainWindow)
    messageBox0.information(text)
    messageBox1 = PrivateMessageBox(window=mainWindow)
    messageBox1.error(text)
    messageBox2 = PrivateMessageBox(window=mainWindow)
    messageBox2.warning(text)
    messageBox3 = PrivateMessageBox(window=mainWindow)
    messageBox3.select(text)
    sys.exit(app.exec_())

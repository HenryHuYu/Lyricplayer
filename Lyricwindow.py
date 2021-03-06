# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Lyricwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 719)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 719))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1024, 0))
        self.centralwidget.setToolTipDuration(-1)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.topframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(60)
        sizePolicy.setHeightForWidth(self.topframe.sizePolicy().hasHeightForWidth())
        self.topframe.setSizePolicy(sizePolicy)
        self.topframe.setMinimumSize(QtCore.QSize(0, 50))
        self.topframe.setMaximumSize(QtCore.QSize(16777215, 50))
        self.topframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topframe.setObjectName("topframe")
        self.verticalLayout_3.addWidget(self.topframe)
        self.middleframe = QtWidgets.QFrame(self.centralwidget)
        self.middleframe.setMinimumSize(QtCore.QSize(0, 540))
        self.middleframe.setObjectName("middleframe")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.middleframe)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftframe = QtWidgets.QFrame(self.middleframe)
        self.leftframe.setMinimumSize(QtCore.QSize(200, 540))
        self.leftframe.setMaximumSize(QtCore.QSize(200, 16777215))
        self.leftframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftframe.setLineWidth(0)
        self.leftframe.setObjectName("leftframe")
        self.horizontalLayout.addWidget(self.leftframe)
        self.mainframe = QtWidgets.QFrame(self.middleframe)
        self.mainframe.setMinimumSize(QtCore.QSize(824, 540))
        self.mainframe.setLineWidth(0)
        self.mainframe.setObjectName("mainframe")
        self.ori_webEngineView = QtWebEngineWidgets.QWebEngineView(self.mainframe)
        self.ori_webEngineView.setGeometry(QtCore.QRect(20, 10, 231, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ori_webEngineView.sizePolicy().hasHeightForWidth())
        self.ori_webEngineView.setSizePolicy(sizePolicy)
        self.ori_webEngineView.setMinimumSize(QtCore.QSize(0, 30))
        self.ori_webEngineView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ori_webEngineView.setSizeIncrement(QtCore.QSize(0, 0))
        self.ori_webEngineView.setStyleSheet("font: 14pt \"Songti SC\";")
        self.ori_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.ori_webEngineView.setObjectName("ori_webEngineView")
        self.lrc_textBrowser = QtWidgets.QTextBrowser(self.mainframe)
        self.lrc_textBrowser.setGeometry(QtCore.QRect(510, 20, 301, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lrc_textBrowser.sizePolicy().hasHeightForWidth())
        self.lrc_textBrowser.setSizePolicy(sizePolicy)
        self.lrc_textBrowser.setMinimumSize(QtCore.QSize(0, 0))
        self.lrc_textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lrc_textBrowser.setAutoFillBackground(True)
        self.lrc_textBrowser.setStyleSheet("")
        self.lrc_textBrowser.setObjectName("lrc_textBrowser")
        self.frame_list = QtWidgets.QFrame(self.mainframe)
        self.frame_list.setGeometry(QtCore.QRect(244, 90, 580, 450))
        self.frame_list.setMinimumSize(QtCore.QSize(580, 450))
        self.frame_list.setMaximumSize(QtCore.QSize(580, 450))
        self.frame_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_list.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_list.setObjectName("frame_list")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_list)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_list)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.list_hidebutton = QtWidgets.QPushButton(self.frame_4)
        self.list_hidebutton.setGeometry(QtCore.QRect(520, 10, 31, 31))
        self.list_hidebutton.setObjectName("list_hidebutton")
        self.verticalLayout.addWidget(self.frame_4)
        self.playlistWidget = QtWidgets.QListWidget(self.frame_list)
        self.playlistWidget.setObjectName("playlistWidget")
        self.verticalLayout.addWidget(self.playlistWidget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.openfilebutton = QtWidgets.QPushButton(self.mainframe)
        self.openfilebutton.setGeometry(QtCore.QRect(20, 450, 91, 41))
        self.openfilebutton.setObjectName("openfilebutton")
        self.horizontalLayout.addWidget(self.mainframe)
        self.verticalLayout_3.addWidget(self.middleframe)
        self.bottomframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(80)
        sizePolicy.setHeightForWidth(self.bottomframe.sizePolicy().hasHeightForWidth())
        self.bottomframe.setSizePolicy(sizePolicy)
        self.bottomframe.setMinimumSize(QtCore.QSize(0, 80))
        self.bottomframe.setMaximumSize(QtCore.QSize(16777215, 80))
        self.bottomframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottomframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottomframe.setObjectName("bottomframe")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.bottomframe)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(40)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.bottomframe)
        self.frame.setMinimumSize(QtCore.QSize(180, 78))
        self.frame.setMaximumSize(QtCore.QSize(180, 78))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.playbutton = QtWidgets.QPushButton(self.frame)
        self.playbutton.setGeometry(QtCore.QRect(70, 14, 50, 50))
        self.playbutton.setText("")
        self.playbutton.setObjectName("playbutton")
        self.pausebutton = QtWidgets.QPushButton(self.frame)
        self.pausebutton.setGeometry(QtCore.QRect(70, 14, 50, 50))
        self.pausebutton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pausebutton.setText("")
        self.pausebutton.setObjectName("pausebutton")
        self.prevbutton = QtWidgets.QPushButton(self.frame)
        self.prevbutton.setGeometry(QtCore.QRect(10, 14, 50, 50))
        self.prevbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.prevbutton.setText("")
        self.prevbutton.setFlat(False)
        self.prevbutton.setObjectName("prevbutton")
        self.nextbutton = QtWidgets.QPushButton(self.frame)
        self.nextbutton.setGeometry(QtCore.QRect(130, 14, 50, 50))
        self.nextbutton.setText("")
        self.nextbutton.setObjectName("nextbutton")
        self.horizontalLayout_2.addWidget(self.frame)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.progress_slider = QtWidgets.QSlider(self.bottomframe)
        self.progress_slider.setOrientation(QtCore.Qt.Horizontal)
        self.progress_slider.setObjectName("progress_slider")
        self.horizontalLayout_5.addWidget(self.progress_slider)
        self.songtimelabel = QtWidgets.QLabel(self.bottomframe)
        self.songtimelabel.setObjectName("songtimelabel")
        self.horizontalLayout_5.addWidget(self.songtimelabel)
        self.frame_2 = QtWidgets.QFrame(self.bottomframe)
        self.frame_2.setMinimumSize(QtCore.QSize(226, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(226, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.vmutebutton = QtWidgets.QPushButton(self.frame_2)
        self.vmutebutton.setGeometry(QtCore.QRect(30, 19, 36, 36))
        self.vmutebutton.setText("")
        self.vmutebutton.setObjectName("vmutebutton")
        self.volumebutton = QtWidgets.QPushButton(self.frame_2)
        self.volumebutton.setGeometry(QtCore.QRect(30, 20, 36, 36))
        self.volumebutton.setText("")
        self.volumebutton.setObjectName("volumebutton")
        self.volumeslider = QtWidgets.QSlider(self.frame_2)
        self.volumeslider.setGeometry(QtCore.QRect(70, 27, 157, 22))
        self.volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeslider.setObjectName("volumeslider")
        self.horizontalLayout_5.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.bottomframe)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.playbackbutton_1 = QtWidgets.QPushButton(self.frame_3)
        self.playbackbutton_1.setGeometry(QtCore.QRect(0, 10, 51, 51))
        self.playbackbutton_1.setObjectName("playbackbutton_1")
        self.playbackbutton_2 = QtWidgets.QPushButton(self.frame_3)
        self.playbackbutton_2.setGeometry(QtCore.QRect(0, 10, 51, 51))
        self.playbackbutton_2.setObjectName("playbackbutton_2")
        self.playbackbutton_3 = QtWidgets.QPushButton(self.frame_3)
        self.playbackbutton_3.setGeometry(QtCore.QRect(0, 10, 51, 51))
        self.playbackbutton_3.setObjectName("playbackbutton_3")
        self.pushButton_listshow = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_listshow.setGeometry(QtCore.QRect(70, 10, 41, 41))
        self.pushButton_listshow.setObjectName("pushButton_listshow")
        self.horizontalLayout_5.addWidget(self.frame_3)
        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 3)
        self.horizontalLayout_5.setStretch(3, 2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 9)
        self.verticalLayout_3.addWidget(self.bottomframe)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MucisPlayer"))
        self.list_hidebutton.setText(_translate("MainWindow", "X"))
        self.openfilebutton.setText(_translate("MainWindow", "添加歌曲"))
        self.songtimelabel.setText(_translate("MainWindow", "Time"))
        self.playbackbutton_1.setText(_translate("MainWindow", "顺序"))
        self.playbackbutton_2.setText(_translate("MainWindow", "单曲"))
        self.playbackbutton_3.setText(_translate("MainWindow", "随机"))
        self.pushButton_listshow.setText(_translate("MainWindow", "PushButton"))

from PyQt5 import QtWebEngineWidgets

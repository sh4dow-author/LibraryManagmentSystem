# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStyle, QDesktopWidget


class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.setObjectName("SplashScreen")
        SplashScreen.resize(680, 400)
        self.centralwidget = QtWidgets.QWidget(SplashScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dropShadowFrame = QtWidgets.QFrame(self.centralwidget)
        self.dropShadowFrame.setStyleSheet("QFrame {\n"
                                           "    background-color: rgb(56, 58, 89);\n"
                                           "    color:rgb(220,220,200);\n"
                                           "    border-radius: 15px;\n"
                                           "}")
        self.dropShadowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dropShadowFrame.setObjectName("dropShadowFrame")
        self.label_title = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_title.setGeometry(QtCore.QRect(0, 110, 641, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(40)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(254, 121, 199);")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.label_description = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_description.setGeometry(QtCore.QRect(0, 180, 651, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_description.setFont(font)
        self.label_description.setStyleSheet("color: rgb(157, 112, 255);")
        self.label_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_description.setObjectName("label_description")
        self.progressBar = QtWidgets.QProgressBar(self.dropShadowFrame)
        self.progressBar.setGeometry(QtCore.QRect(50, 240, 561, 21))
        self.progressBar.setStyleSheet("QProgressBar{\n"
                                       "    background-color: rgb(136, 101, 221);\n"
                                       "    color:rgb(200,200,200);\n"
                                       "    border-style: none;\n"
                                       "    border-radius: 10px;\n"
                                       "    text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "    border-radius: 10px;\n"
                                       "    background-color: qlineargradient(spread:pad, x1:0, y1:0.477, x2:0.984772, y2:0.511, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
                                       "}")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_loading = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_loading.setGeometry(QtCore.QRect(0, 270, 661, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_loading.setFont(font)
        self.label_loading.setStyleSheet("color: rgb(157, 112, 255);")
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter)
        self.label_loading.setObjectName("label_loading")
        self.label_credits = QtWidgets.QLabel(self.dropShadowFrame)
        self.label_credits.setGeometry(QtCore.QRect(10, 350, 641, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_credits.setFont(font)
        self.label_credits.setStyleSheet("color: rgb(157, 112, 255);")
        self.label_credits.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_credits.setObjectName("label_credits")
        self.verticalLayout.addWidget(self.dropShadowFrame)
        SplashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(SplashScreen)
        QtCore.QMetaObject.connectSlotsByName(SplashScreen)

    def retranslateUi(self, SplashScreen):
        _translate = QtCore.QCoreApplication.translate
        SplashScreen.setWindowTitle(_translate("SplashScreen", "SplashScreen"))
        self.label_title.setText(_translate("SplashScreen",
                                            "<html><head/><body><p><span style=\" font-weight:600;\">BOOK </span>Family</p></body></html>"))
        self.label_description.setText(_translate("SplashScreen",
                                                  "<html><head/><body><p><strong>READ</strong> BOOKS EVERY DAY</p><p><br/></p></body></html>"))
        self.label_loading.setText(
            _translate("SplashScreen", "<html><head/><body><p>LOADING...</p><p><br/></p></body></html>"))
        self.label_credits.setText(_translate("SplashScreen",
                                              "<html><head/><body><p><strong>Created</strong> by Pavel Yarmaliuk</p><p><br/></p></body></html>"))

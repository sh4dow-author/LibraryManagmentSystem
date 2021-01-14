from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PythonUi.LoginPage_UI import Ui_LoginPageUi
from PyQt5.Qt import QEvent
from PythonBackend.MainWindow import MainPage
import time


class LoginPage(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_LoginPageUi()
        self.ui.setupUi(self)
        self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.label_3.hide()
        # Locate window in center
        self.center_window()

        # Deleting brackets from window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton.setIcon(QtGui.QIcon('../Icons/cancel.png'))
        self.ui.pushButton_2.clicked.connect(self.checkPassword)
        self.ui.lineEdit.returnPressed.connect(self.checkPassword)
        qApp.installEventFilter(self)

    def checkPassword(self):
        with open('Password.txt', 'r') as f:
            password = f.read().strip()
        if password != self.ui.lineEdit.text():
            self.ui.label_3.show()
            self.ui.lineEdit.setStyleSheet("QLineEdit{\n"
                                           "    background-color: rgb(56, 58, 89);\n"
                                           "    border-radius:10px;\n"
                                           "    border: 1px solid rgb(255, 44, 58);\n"
                                           "    color:white;\n"
                                           "}\n"
                                           )
        else:
            self.main_window = MainPage()
            self.main_window.show()
            self.close()

    def eventFilter(self, obj, event):
        if obj.objectName() == 'pushButton':
            if event.type() == QEvent.Enter:  # if mouse on button than we will change png image
                time.sleep(0.14)
                self.ui.pushButton.setIcon(QtGui.QIcon('Icons/cancel_hover.png'))
            if event.type() == QEvent.Leave:  # if we out from image than we will change png image to default
                time.sleep(0.14)
                self.ui.pushButton.setIcon(QtGui.QIcon('Icons/cancel.png'))
        if obj.objectName() == 'lineEdit':
            if event.type() == event.MouseButtonPress:
                # If we started changing lineEdit than we will change border of widget
                self.ui.lineEdit.setStyleSheet("QLineEdit{\n"
                                               "    background-color: rgb(56, 58, 89);\n"
                                               "    border-radius:10px;\n"
                                               "    border: 1px solid rgb(23, 255, 240);\n"
                                               "    color:white;\n"
                                               "}\n"
                                               )

                self.ui.label_3.hide()  # if "incorrect password" was shown than we will hide that

        return QWidget.eventFilter(self, obj, event)

    def center_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

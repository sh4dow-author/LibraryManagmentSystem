from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.Qt import QColor
from PyQt5.QtCore import QTimer
from PythonBackend.LoginPage import LoginPage
from PythonUi.SplashScreen_UI import Ui_SplashScreen

# Global variables
counter = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Locate window in center
        self.center_window()

        # Delete border of window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Adding shadow effect for frame
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # Timer Start
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)

        # Timer in milliseconds
        self.timer.start(35)

        # Change Description
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> USER INTERFACE"))
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            self.timer.stop()
            self.login_window = LoginPage()
            self.login_window.show()
            self.close()
        # Increase counter
        counter += 1

    def center_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())




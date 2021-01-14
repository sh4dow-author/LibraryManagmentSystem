from PythonBackend.SplashScreen import SplashScreen
from PyQt5 import QtWidgets

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    splashScreen = SplashScreen()

    sys.exit(app.exec_())


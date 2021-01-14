from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.Qt import QIcon

class UI_Functuions:
    def toggleMenu(self, window, enable, maxWidth):
        if enable:
            # GET WIDTH
            width = window.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 0

            # SET MAX WIDTH
            if width == 0:
                window.ui.toggleButton.setIcon(QIcon('Icons/x-button.png'))
                widthExtended = maxExtend
            else:
                window.ui.toggleButton.setIcon(QIcon('Icons/toggle_menu_disabled.png'))
                widthExtended = standard

            # ANIMATION
            window.animation = QPropertyAnimation(window.ui.frame_left_menu, b"minimumWidth")
            window.animation.setDuration(100)
            window.animation.setStartValue(width)
            window.animation.setEndValue(widthExtended)
            window.animation.setEasingCurve(QEasingCurve.InOutQuart)
            window.animation.start()

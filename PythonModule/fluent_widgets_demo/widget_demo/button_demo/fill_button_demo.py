# coding:utf-8
import sys
import random

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


from FluentWidgets import SplitWidget, VerticalScrollWidget, OutlineToolButton, PrimaryPushButton, setTheme, Theme, \
    FluentIcon, setThemeColor
from FluentWidgets.components.widgets.button import FillPushButton, FillToolButton


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setMicaEffectEnabled(True)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.verWidget = VerticalScrollWidget(self)
        self.box.addWidget(self.verWidget)
        self.verWidget.enableTransparentBackground()
        self.verWidget.boxLayout.setSpacing(24)
        self.buttons = []

        for _ in range(100):
            button = FillPushButton(f"Button {_}", self)
            button.setFixedSize(self.width() / 1.5, 35)
            button.setFillColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.verWidget.addWidget(button, 0, Qt.AlignCenter)
            self.buttons.append(button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

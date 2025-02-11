# coding:utf-8
import sys

from FluentWidgets import HBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import FluentIcon, setTheme, Theme

from smooth_switch_widget import SmoothSwitchPushButtonBar


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = HBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.t1 = SmoothSwitchPushButtonBar(self)
        self.t1.widgetLayout.setAlignment(Qt.AlignTop)

        self.t1.addItem('1', "HOME")
        self.t1.addItem('2', "WIFI")
        self.t1.addItem('3', "SETTING")

        self.t1.addSeparator()

        self.t1.addItem('7', "EDIT")
        self.t1.addItem('8', "GITHUB")
        self.t1.addItem('9', "NONE")

        self.layout.addWidget(self.t1)
        self.t1.setCurrentWidget('1')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    setTheme(Theme.AUTO)
    window.show()
    sys.exit(app.exec())
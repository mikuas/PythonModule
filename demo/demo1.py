# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from FluentWidgets import FluentWindow, SplitFluentWindow, MSFluentWindow
from qfluentwidgets import TitleLabel, FluentIcon, PrimaryPushButton


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)
        self.setWindowTitle('FluentWindow')
        self.button = PrimaryPushButton("BUTTON", self)
        self.button.setFixedHeight(128)
        self.vBoxLayout.addWidget(self.button)

        self.homeInterface = TitleLabel("HOME", self)
        self.musicInterface = TitleLabel('MUSIC', self)
        self.settingInterface = TitleLabel("SETTING", self)

        self.homeInterface.setObjectName('home')
        self.musicInterface.setObjectName('music')
        self.settingInterface.setObjectName('setting')

        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(
            self.homeInterface,
            FluentIcon.HOME,
            'HOME'
        )
        self.addSubInterface(
            self.musicInterface,
            FluentIcon.MUSIC,
            "MUSIC"
        )
        self.addSubInterface(
            self.settingInterface,
            FluentIcon.SETTING,
            "SETTING"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
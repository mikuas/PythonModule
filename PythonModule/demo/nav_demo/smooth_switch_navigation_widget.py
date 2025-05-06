# coding:utf-8

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SmoothSwitchNavWidget, HorizontalSeparator


class Window(SmoothSwitchNavWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Switch Widget")

        self.texts = []

        self.icons = [
            FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.GAME, FluentIcon.MUSIC, FluentIcon.ADD_TO,
            FluentIcon.MENU, FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.BROOM, FluentIcon.CAR,
            FluentIcon.ASTERISK, FluentIcon.CAFE, FluentIcon.BUS, FluentIcon.CLOSE, FluentIcon.ACCEPT,
            FluentIcon.FLAG, FluentIcon.FOLDER, FluentIcon.DOWN, FluentIcon.RETURN, FluentIcon.CUT,
            FluentIcon.MUTE, FluentIcon.MAIL, FluentIcon.SCROLL, FluentIcon.SEARCH, FluentIcon.HELP,
            FluentIcon.HOME_FILL, FluentIcon.SEND, FluentIcon.PLAY, FluentIcon.WIFI, FluentIcon.SETTING
        ]

        for text in self.icons:
            self.texts.append(str(text).split('.')[-1])
        print(f"Texts {self.texts}")

        hsp = HorizontalSeparator(self)
        self._widgetLayout.insertWidget(1, hsp)

        for text, icon in zip(self.texts, self.icons):
            self.addSubInterface(text, text, TitleLabel(text + " INTERFACE", self), icon)

        for i in range(int(len(self.texts) / 5) + 1):
            self.insertSeparator(i * (5 + 1)).setSeparatorColor('deeppink')

        self.setCurrentWidget("HOME")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
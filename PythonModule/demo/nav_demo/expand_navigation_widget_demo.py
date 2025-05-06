# coding:utf-8

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SideNavWidget, NavigationItemPosition, ThemeListener


class Window(SideNavWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expand NavWidget Bar Widget")

        # ThemeListener(self)

        self.icons = [
            FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.GAME, FluentIcon.MUSIC, FluentIcon.ADD_TO,
            FluentIcon.MENU, FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.BROOM, FluentIcon.CAR,
            FluentIcon.ASTERISK, FluentIcon.CAFE, FluentIcon.BUS, FluentIcon.CLOSE, FluentIcon.ACCEPT,
            FluentIcon.FLAG, FluentIcon.FOLDER, FluentIcon.DOWN, FluentIcon.RETURN, FluentIcon.CUT,
            FluentIcon.MUTE, FluentIcon.MAIL, FluentIcon.SCROLL, FluentIcon.SEARCH, FluentIcon.HELP,
            FluentIcon.HOME_FILL, FluentIcon.SEND, FluentIcon.PLAY, FluentIcon.WIFI, FluentIcon.SETTING
        ]

        self.topTexts = []
        self.scrollText = []
        self.bottomText = []

        for text in self.icons[:5]:
            self.topTexts.append(str(text).split('.')[-1])
        print(f"Top Texts {self.topTexts}")

        for text in self.icons[5:25]:
            self.scrollText.append(str(text).split('.')[-1])
        print(f"Scroll Texts {self.scrollText}")

        for text in self.icons[25:]:
            self.bottomText.append(str(text).split('.')[-1])
        print(f"bottomText Texts {self.bottomText}")

        # add to scroll
        for text, icon in zip(self.topTexts, self.icons[:5]):
            self.addSubInterface(text, text, TitleLabel(text + " INTERFACE", self), icon, NavigationItemPosition.TOP)
        self.addSeparator()

        # add to top
        for text, icon in zip(self.scrollText, self.icons[5:25]):
            self.addSubInterface(text, text, TitleLabel(text + " INTERFACE", self), icon)

        # add to bottom
        self.addSeparator(NavigationItemPosition.BOTTOM)
        for text, icon in zip(self.bottomText, self.icons[25:]):
            self.addSubInterface(text, text, TitleLabel(text + " INTERFACE", self), icon, NavigationItemPosition.BOTTOM)

        self.setCurrentWidget("HOME")
        self.enableReturnButton(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(1000, 520)
    window.show()
    sys.exit(app.exec())
# coding:utf-8

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SmoothSwitchWidget


class Window(SmoothSwitchWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Switch Widget")

        self.addSubInterface(
            "HOME", "HOME", TitleLabel("HOME INTERFACE", self), FluentIcon.HOME
        )

        self.addSubInterface(
            "ABOUT", "ABOUT", TitleLabel("ABOUT INTERFACE", self), FluentIcon.ALBUM
        )
        self.addSubInterface(
            "GITHUB", "GITHUB", TitleLabel("GITHUB INTERFACE", self), FluentIcon.GITHUB
        )

        self.addSeparator().setSeparatorColor('deeppink')

        self.addSubInterface(
            "VIDEO", "VIDEO", TitleLabel("VIDEO INTERFACE", self), FluentIcon.VIDEO
        )
        self.addSubInterface(
            "GAME", "GAME", TitleLabel("GAME INTERFACE", self), FluentIcon.GAME
        )
        self.addSubInterface(
            "SEND", "SEND", TitleLabel("SEND INTERFACE", self), FluentIcon.SEND
        )
        self.addSubInterface(
            "SAVE", "SAVE", TitleLabel("SAVE INTERFACE", self), FluentIcon.SAVE
        )

        self.addSeparator().setSeparatorColor('aqua')

        self.addSubInterface(
            "MUSIC", "MISIC", TitleLabel("MUSIC INTERFACE", self)
        )
        self.addSubInterface(
            "SETTING", "SETTING", TitleLabel("SETTING INTERFACE", self)
        )
        self.addSubInterface(
            "WIFI", "WIFI", TitleLabel("WIFI INTERFACE", self)
        )

        self.addSeparator().setSeparatorColor('deepskyblue')

        self.addSubInterface(
            "LINK", "LINK", TitleLabel("LINK INTERFACE", self), FluentIcon.LINK
        )
        self.addSubInterface(
            "FOLDER", "FOLDER", TitleLabel("FOLDER INTERFACE", self), FluentIcon.FOLDER
        )
        self.addSubInterface(
            "EDIT", "EDIT", TitleLabel("EDIT INTERFACE", self), FluentIcon.EDIT
        )
        self.setCurrentWidget("HOME")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
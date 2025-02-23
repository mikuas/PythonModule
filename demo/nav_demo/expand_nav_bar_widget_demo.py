# coding:utf-8

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SideNavigationWidget, NavigationItemPosition


class Window(SideNavigationWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expand NavWidget Bar Widget")

        # add to scroll
        self.addSubInterface(
            "HOME", "HOME", TitleLabel("HOME INTERFACE", self), FluentIcon.HOME
        )
        self.addSubInterface(
            "ABOUT", "ABOUT", TitleLabel("ABOUT INTERFACE", self), FluentIcon.ALBUM
        )
        self.addSubInterface(
            "GITHUB", "GITHUB", TitleLabel("GITHUB INTERFACE", self), FluentIcon.GITHUB
        )
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

        # add to top
        self.addSubInterface(
            "MUSIC", "MISIC", TitleLabel("MUSIC INTERFACE", self), FluentIcon.MUSIC, NavigationItemPosition.TOP
        )
        self.addSubInterface(
            "SETTING", "SETTING", TitleLabel("SETTING INTERFACE", self), FluentIcon.SETTING, NavigationItemPosition.TOP
        )
        self.addSubInterface(
            "WIFI", "WIFI", TitleLabel("WIFI INTERFACE", self), FluentIcon.WIFI, NavigationItemPosition.TOP
        )
        self.addSeparator(NavigationItemPosition.TOP).setSeparatorColor('deepskyblue')

        # add to bottom
        self.addSeparator(NavigationItemPosition.BOTTOM).setSeparatorColor('deeppink')
        self.addSubInterface(
            "LINK", "LINK", TitleLabel("LINK INTERFACE", self), FluentIcon.LINK, NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            "FOLDER", "FOLDER", TitleLabel("FOLDER INTERFACE", self), FluentIcon.FOLDER, NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            "EDIT", "EDIT", TitleLabel("EDIT INTERFACE", self), FluentIcon.EDIT, NavigationItemPosition.BOTTOM
        )

        self.setCurrentWidget("HOME")
        self.enableReturnButton(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
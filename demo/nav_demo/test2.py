# coding:utf-8
import sys

from FluentWidgets import HorizontalScrollWidget, SideNavigationWidget, WinFluentIcon, NavigationItemPosition
from PySide6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme, TitleLabel, FluentIcon


class Window(HorizontalScrollWidget):
    def __init__(self):
        super().__init__()
        self.nav = SideNavigationWidget(self)
        self.hBoxLayout.addWidget(self.nav)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.nav.addSubInterface(
            "HOME",
            "Home",
            WinFluentIcon.HOME,
            TitleLabel("HOME INTERFACE", self),
            NavigationItemPosition.TOP
        ).addSubInterface(
            "GITHUB",
            "Github",
            FluentIcon.GITHUB,
            TitleLabel("GITHUB INTERFACE", self),
            NavigationItemPosition.TOP
        ).addSubInterface(
            "ABOUT",
            "About",
            FluentIcon.LABEL,
            TitleLabel("ABOUT INTERFACE", self),
            NavigationItemPosition.TOP
        ).addSubInterface(
            "SETTING",
            "Setting",
            WinFluentIcon.SETTING,
            TitleLabel("SETTING INTERFACE", self),
            NavigationItemPosition.BOTTOM
        )
        self.nav.insertSeparator(0, NavigationItemPosition.BOTTOM).enableReturn(True).setCurrentWidget('HOME')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    setTheme(Theme.AUTO)
    window.show()
    sys.exit(app.exec())
# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from FluentWidgets import SideNavigationWidget, NavigationItemPosition


class NavigationDemo(SideNavigationWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 520)
        self.enableReturn(True)

        self.addSubInterface(
            'HOME',
            "HOME",
            FluentIcon.HOME,
            TitleLabel("HOME", self),
            NavigationItemPosition.TOP
        )
        self.addSubInterface(
            "GITHUB",
            "GITHUB",
            FluentIcon.GITHUB,
            TitleLabel("GITHUB", self),
            NavigationItemPosition.TOP
        )
        self.addSubInterface(
            "SETTING",
            "SETTING",
            FluentIcon.SETTING,
            TitleLabel("SETTING", self),
            NavigationItemPosition.BOTTOM
        )
        self.setCurrentWidget('HOME').insertSeparator(0, NavigationItemPosition.BOTTOM)

        self.setBackgroundImg(r"C:\Users\Administrator\OneDrive\Pictures\14.jpg")
        self.setRadius(8, 8)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = NavigationDemo()
    demo.show()
    sys.exit(app.exec())
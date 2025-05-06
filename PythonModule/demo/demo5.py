# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import (
    WinFluentIcon, VBoxLayout,
    Menu, AcrylicRoundMenu, CheckedMenu, ProfileCardMenu, AcrylicProfileCardMenu,
    HorizontalPagerWidget, VerticalPagerWidget
)

from qfluentwidgets import TitleLabel, FluentIcon, PrimaryPushButton


class Widget(QWidget):
    def __init__(self, parent, menu, title):
        super().__init__(parent)
        layout = VBoxLayout(self)
        layout.addWidget(TitleLabel(title, self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.menu = menu

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        self.menu.exec(event.globalPos())


class Window(VerticalPagerWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)

        """ Menu """
        self.menu = Menu(self)
        self.menuWidget = Widget(self, self.menu, 'MENU')
        self.menu.addItems(
            [WinFluentIcon.WIN_11_LOG, WinFluentIcon.RADIUS_WIN_11_LOG, WinFluentIcon.MUSIC],
            ['WIN_11_LOG', "RADIUS_11_LOG", "MUSIC"]
        )

        """ AcrylicRoundMenu """
        self.acrylicMenu = AcrylicRoundMenu(self)
        self.acrylicMenuWidget = Widget(self, self.acrylicMenu, "ACRYLIC_ROUND_MENU")
        self.acrylicMenu.addItems(
            [WinFluentIcon.WIFI, WinFluentIcon.XIN_HAO, WinFluentIcon.HOME],
            ['WIFI', "XIN_HAO", "HOME"]
        )

        """ CheckedMenu """
        self.checkedMenu = CheckedMenu(self)
        self.checkedMenuWidget = Widget(self, self.checkedMenu, "CHECKED_MENU")
        self.checkedMenu.addItems(
            [FluentIcon.COPY, FluentIcon.CUT, FluentIcon.PASTE],
            ['COPY', "CUT", "PAST"]
        )

        """ ProfileCardMenu """
        self.profileMenu = ProfileCardMenu(
            r"C:\Users\Administrator\OneDrive\Pictures\1734703508871.jpg",
            'MiTa',
            'Ciallo～(∠・ω< )⌒☆@0721.com',
            self,
            '退出登录',
            'https://www.bilibili.com'
        )
        self.profileMenuWidget = Widget(self, self.profileMenu, "PROFILE_CARD_MENU")
        self.profileMenu.addItems(
            [FluentIcon.RETURN, FluentIcon.CODE, FluentIcon.GITHUB],
            ["RETURN", "CODE", "GITHUB"]
        )

        """ AcrylicProfileCardMenu """
        self.acrylicProfileMenu = AcrylicProfileCardMenu(
            r"C:\Users\Administrator\OneDrive\Pictures\1734703508871.jpg",
            'MiTa',
            'Ciallo～(∠・ω< )⌒☆@0721.com',
            self,
            '退出登录',
            'https://www.bilibili.com'
        )
        self.acrylicProfileMenuWidget = Widget(self, self.profileMenu, "PROFILE_CARD_MENU")
        self.acrylicProfileMenu.addItems(
            [FluentIcon.RETURN, FluentIcon.CODE, FluentIcon.GITHUB],
            ["RETURN", "CODE", "GITHUB"]
        )

        self.button = PrimaryPushButton("Click Me Show Menu", self)

        self.addWidgets([
            self.menuWidget,
            self.acrylicMenuWidget,
            self.checkedMenuWidget,
            self.profileMenuWidget,
            self.acrylicProfileMenuWidget,
            self.button
        ])

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.button.clicked.connect(
            lambda: self.menu.execWidgetCenter(self.button)
        )


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
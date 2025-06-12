# coding:utf-8

""" TopNavigationWidget """

import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, SlidingNavigationBar, FluentIcon, PopUpAniStackedWidget, TitleLabel, \
    SlidingNavigationWidget


class TopNavigationWidget(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(5, 35, 15, 0)
        self.navigation = SlidingNavigationBar(self)
        self.stackedWidget = PopUpAniStackedWidget(self)

        self.box.addWidget(self.navigation, 0)
        self.box.addWidget(self.stackedWidget, 1)

        self.initNavigation()
        self.navigation.setCurrentIndex(0)

    def initNavigation(self):
        items = {
            "主页": FluentIcon.HOME,
            "订阅": FluentIcon.BOOK_SHELF,
            "历史": FluentIcon.HISTORY,
            "下载": FluentIcon.DOWNLOAD,
            "未播放的剧集": FluentIcon.VIDEO,
            "正在播放": FluentIcon.VIDEO
        }
        for item, icon in items.items():
            w = TitleLabel(item)
            self.navigation.addItem(
                item, item, icon, lambda: self.stackedWidget.setCurrentWidget(w), False
            )
            self.stackedWidget.addWidget(w)
        self.navigation.addStretch(1)
        self.navigation.addItem(
            "Settings", "", FluentIcon.SETTING, lambda: print("Setting"), False
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TopNavigationWidget()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
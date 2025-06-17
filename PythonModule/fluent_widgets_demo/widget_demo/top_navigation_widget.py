# coding:utf-8

""" TopNavigationWidget """

import sys
from functools import partial

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, SlidingNavigationBar, FluentIcon, PopUpAniStackedWidget, TitleLabel, \
    SlidingNavigationWidget, HorizontalSeparator, Icon, WinFluentIcon


class TopNavigationWidget(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TopNavigationWidgetDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.topNavigationWidget = SlidingNavigationWidget(self)
        self.setStyleSheet("background-color: #f0f3f9")
        self.topNavigationWidget.stackedWidget.setStyleSheet("background-color: #f7f9fc")

        self.box.addWidget(self.topNavigationWidget, 1)

        self.topNavigationWidget.widgetLayout.insertSpacing(1, 5)
        self.topNavigationWidget.widgetLayout.insertWidget(2, HorizontalSeparator(self).setSeparatorColor("#e5e7ea"))
        self.initNavigation()

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
            title = TitleLabel(item, self)
            title.setAlignment(Qt.AlignCenter)
            self.topNavigationWidget.addSubInterface(
                item, item, title, icon, True if item == "下载" else False, toolTip=item
            )
        self.topNavigationWidget.navigation.addStretch(1)
        title = TitleLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        self.topNavigationWidget.addSubInterface(
            "Settings", "", title, FluentIcon.SETTING, toolTip="Settings"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TopNavigationWidget()
    # window.windowEffect.setMicaEffect(window.winId(), isAlt=True)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
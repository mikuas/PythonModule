# coding:utf-8

""" TopNavigationWidget """

import sys
from functools import partial

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, SlidingNavigationBar, FluentIcon, PopUpAniStackedWidget, TitleLabel, \
    SlidingNavigationWidget, HorizontalSeparator, Icon, WinFluentIcon, NavigationItemPosition, SlidingToolNavigationBar


class TopNavigationWidget(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TopNavigationWidgetDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.navigation = SlidingNavigationBar(self)
        self.setStyleSheet("background-color: #f0f3f9")

        self.box.addWidget(self.navigation, 1, Qt.AlignTop)
        self.initNavigation()
        self.navigation.setCurrentIndex(0)

    def initNavigation(self):
        for i in range(1, 6):
            self.navigation.addItem(
                f"Item{i}", f"Item{i}"
            )
        self.navigation.addItem(
            "None", "CHANG_CHANG_CHANG_CHANG_CHANG_CHANG_CHANG_CHANG"
        )
        self.navigation.addStretch(1)
        self.navigation.addSeparator()
        self.navigation.addItem(
            "Settings", "", FluentIcon.SETTING, toolTip="Settings"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TopNavigationWidget()
    # window.windowEffect.setMicaEffect(window.winId(), isAlt=True)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
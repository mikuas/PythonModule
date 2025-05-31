# coding:utf-8
import sys

from PySide6.QtGui import QPainter, Qt, QColor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout
from FluentWidgets import SplitWidget, FluentIcon, Icon, SlidingNavigationWidget, TitleLabel, OptionsSettingCard, qconfig


class SplitWidgetDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False, isAlt=True)
        # self.windowEffect.setAcrylicEffect(self.winId())
        # self.windowEffect.setAeroEffect(self.winId())
        self.setWindowTitle("SplitWidgetDemo")
        self.setWindowIcon(Icon(FluentIcon.GITHUB))

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 25, 0, 0)
        self.nav = SlidingNavigationWidget(self)
        self.box.addWidget(self.nav)

        self.items = {
            "HOME": FluentIcon.HOME,
            "MUSIC": FluentIcon.MUSIC,
            "VIDEOS": FluentIcon.VIDEO,
            "MAIL": FluentIcon.MAIL,
        }

        for key, value in self.items.items():
            self.nav.addSubInterface(
                key, key, OptionsSettingCard(
                    qconfig.themeMode,
                    FluentIcon.BRUSH,
                    "应用主题",
                    "调整你的应用外观",
                    ["浅色", "深色", "跟随系统设置"]
                ), toolTip=key, icon=value
            )
        self.nav._slidingNavigationBar.addStretch(1)
        self.nav.addSubInterface(
            "SETTINGS", "SETTINGS", OptionsSettingCard(
                qconfig.themeMode,
                FluentIcon.BRUSH,
                "应用主题",
                "调整你的应用外观",
                ["浅色", "深色", "跟随系统设置"]
            ), alignment=Qt.AlignmentFlag.AlignRight, icon=FluentIcon.SETTING
        )
        # self.nav._slidingNavigationBar.setBarAlignment(Qt.AlignCenter)
        self.nav.setCurrentWidget("HOME")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("deepskyblue"))
        # painter.drawRect(self.rect())
        # super().paintEvent(event)=


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SplitWidgetDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
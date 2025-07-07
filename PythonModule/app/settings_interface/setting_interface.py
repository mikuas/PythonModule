# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt

from FluentWidgets import VerticalScrollWidget, SettingCardGroup, RadioButton, ExpandGroupSettingCard, FluentIcon, \
    Theme, setTheme, BodyLabel, SubtitleLabel


class Widget(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        # self.setStyleSheet("background:transparent;")

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.title = SubtitleLabel(title, self)
        self.bottom = Bottom(self)

        self.box.addWidget(self.title, 0, Qt.AlignLeft)
        self.box.addWidget(self.bottom)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("#f9f9f9"))
        painter.setBrush((QColor("#f3f3f3")))
        painter.drawRoundedRect(self.rect().adjusted(0, 120, 0, 0), 8, 8)

class Bottom(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush((QColor("#fbfbfb")))
        painter.drawRect(self.rect())



class SettingInterface(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.enableTransparentBackground()
        self.themeSettingCardGroup = ExpandGroupSettingCard(FluentIcon.BRUSH,  "主题色", "设置主题色", parent=self)
        self.w = Widget("设置", self)

        self.addWidget(self.themeSettingCardGroup)
        self.addWidget(self.w, 0, Qt.AlignTop)

        self.initThemeRadioButton()
        self.initThemeSettingCardGroup()

    def initThemeRadioButton(self):
        self.themeWidget = QWidget(self)
        self.buttonGroup = QButtonGroup(self)

        box = QVBoxLayout(self.themeWidget)
        box.setContentsMargins(32, 10, 10, 10)
        box.setSpacing(12)

        self.lightRadio = RadioButton("亮色", self)
        self.darkRadio = RadioButton("暗色", self)
        self.autoRadio = RadioButton("自动", self)

        self.autoRadio.setChecked(True)

        box.addWidget(self.lightRadio)
        box.addWidget(self.darkRadio)
        box.addWidget(self.autoRadio)

        self.buttonGroup.addButton(self.lightRadio)
        self.buttonGroup.addButton(self.darkRadio)
        self.buttonGroup.addButton(self.autoRadio)

    def initThemeSettingCardGroup(self):
        self.themeSettingCardGroup.addGroupWidget(self.themeWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

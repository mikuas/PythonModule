# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import ExpandGroupSettingCard, SimpleExpandGroupSettingCard, ExpandSettingCard, FluentIcon, \
    TitleLabel, VerticalScrollWidget, SettingCardGroup, SettingCard, PushSettingCard


class Demo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.egsc = ExpandGroupSettingCard(FluentIcon.SETTING, 'title', 'content', self)
        self.segsc = SimpleExpandGroupSettingCard(FluentIcon.SETTING, 'title', 'content', self)
        self.esc = ExpandSettingCard(FluentIcon.SETTING, 'title', 'content', self)

        self.widget = QWidget(self)
        self.widgetLayut = QVBoxLayout(self.widget)
        for _ in range(5):
            self.widgetLayut.addWidget(TitleLabel(f"Item {_}"), alignment=Qt.AlignHCenter)
        self.egsc.addGroupWidget(self.widget)

        self.widget = QWidget(self)
        self.widgetLayut = QVBoxLayout(self.widget)
        for _ in range(5):
            self.widgetLayut.addWidget(TitleLabel(f"Item {_}"), alignment=Qt.AlignHCenter)
        self.segsc.addGroupWidget(self.widget)

        self.widget = QWidget(self)
        self.widgetLayut = QVBoxLayout(self.widget)
        for _ in range(5):
            self.widgetLayut.addWidget(TitleLabel(f"Item {_}"), alignment=Qt.AlignHCenter)
        self.esc.scrollLayout.addWidget(self.widget)

        # self.box.addWidget(self.egsc)
        # self.box.addWidget(self.segsc)
        # self.box.addWidget(self.esc)
        self.addWidget(self.egsc)
        self.addWidget(self.segsc)
        self.addWidget(self.esc)
        self.boxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

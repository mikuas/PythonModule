# coding:utf-8
import sys

from FluentWidgets.common.overload import singledispatchmethod
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtCore import Qt, QPoint, QRect, QRectF, Property, QSize

from FluentWidgets import SplitWidget, SubtitleRadioButton, SimpleCardWidget, ElevatedCardWidget, SettingCard, \
    ExpandSettingCard, SimpleExpandGroupSettingCard, ExpandGroupSettingCard, FluentIcon


class SubtitleRadioButtonDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(5, 35, 5, 0)

        self.buttonGroup = QButtonGroup(self)

        self.subRadio1 = SubtitleRadioButton("扬声器", "Realted(R) Audio", self)
        self.subRadio2 = SubtitleRadioButton("耳机", "ProjectML(R) Audio", self)
        self.subRadio3 = SubtitleRadioButton("音量", "Aird(R) Audio", self)
        self.subRadio4 = SubtitleRadioButton("空间音效", "Realted(R) Audio", self)
        self.subRadio5 = SubtitleRadioButton("显示模式", "Realted(R) Audio", self)

        self.subRadio5.setSubText('None')

        self.buttonGroup.addButton(self.subRadio1)
        self.buttonGroup.addButton(self.subRadio2)
        self.buttonGroup.addButton(self.subRadio3)
        self.buttonGroup.addButton(self.subRadio4)
        self.buttonGroup.addButton(self.subRadio5)

        self.buttonGroup.setExclusive(False)

        self.box.addWidget(self.subRadio1)
        self.box.addWidget(self.subRadio2)
        self.box.addWidget(self.subRadio3)
        self.box.addWidget(self.subRadio4)
        self.box.addWidget(self.subRadio5)

        self.settingCard = SettingCard(FluentIcon.HOME, "SettingCard", "Content", self)
        self.expandSettingCard = ExpandSettingCard(FluentIcon.HOME, "ExpandSettingCard", "Content", self)
        self.expandGroupSettingCard = ExpandGroupSettingCard(FluentIcon.HOME, "ExpandGroupSettingCard", "Content", self)

        self.subRadio1.setMinimumHeight(64)
        self.subRadio2.setMinimumHeight(64)
        self.subRadio3.setMinimumHeight(64)
        self.subRadio4.setMinimumHeight(64)
        self.subRadio5.setMinimumHeight(64)

        self.expandGroupSettingCard.view.setContentsMargins(10, 0, 0, 0)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio1)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio2)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio3)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio4)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio5)

        self.box.addWidget(self.settingCard)
        self.box.addWidget(self.expandSettingCard)
        self.box.addWidget(self.expandGroupSettingCard)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubtitleRadioButtonDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

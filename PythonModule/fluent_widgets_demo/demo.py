# coding:utf-8

import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QColor, Qt, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout


from FluentWidgets import TransparentPushButton, VBoxLayout, FluentIcon, OutlinePushButton, OutlineToolButton, Icon, setFont

from FluentWidgets.components.widgets.button import RoundToolButton, RoundPushButton



class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)

        self.opb = OutlinePushButton("OutlinePushButton", self, FluentIcon.HOME)
        self.otb = OutlineToolButton(FluentIcon.GITHUB, self)

        self.rpb = RoundPushButton("RoundPushButton", self, FluentIcon.HOME)
        self.rtb = RoundToolButton(FluentIcon.SETTING, self)

        self.box.addWidget(self.opb)
        self.box.addWidget(self.otb)
        self.box.addWidget(self.rpb)
        self.box.addWidget(self.rtb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
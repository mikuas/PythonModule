# coding:utf-8
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from qframelesswindow import StandardTitleBar


class CustomTitleBar(StandardTitleBar):
    def __init__(self, parent):
        super().__init__(parent)

    # def setMinButton(self):
    #     pass
    #
    # def setMaxButton(self):
    #     pass
    #
    # def setCloseButton(self):
    #     pass

    def setIcon(self, icon, size=QSize(20, 20)):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(size))
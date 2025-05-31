# coding:utf-8
import sys

from PySide6.QtWidgets import QWidget
from qframelesswindow import FramelessWindow

from .fluent_window import SplitTitleBar
from ..components.widgets.frameless_window import FramelessWindow as FW


class SplitWidget(FramelessWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setTitleBar(SplitTitleBar(self))

        if sys.platform == "darwin":
            self.titleBar.setFixedHeight(48)
        self.titleBar.raise_()


class TEST(FW):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitleBar(SplitTitleBar(self))
# coding:utf-8
from typing import Union
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QLayout

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import SingleDirectionScrollArea, SmoothScrollArea, ScrollArea


class SingleScrollWidgetBase(SingleDirectionScrollArea):
    """ 滚动组件基类 """
    def __init__(self, parent=None, orient: Qt.Orientation = None):
        super().__init__(parent, orient)
        self._widget = QWidget()
        self.boxLayout = None # type: Union[VBoxLayout, HBoxLayout]
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        # self.enableTransparentBackground()

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignTop):
        self.boxLayout.addWidget(widget, stretch, alignment)

    def addLayout(self, layout: QLayout, stretch=0):
        self.boxLayout.addLayout(layout, stretch)

    def insertWidget(self, index: int, widget: QWidget, stretch=0, alignment=Qt.AlignTop):
        self.boxLayout.insertWidget(index, widget, stretch, alignment)

    def insertLayout(self, index: int, layout: QLayout, stretch=0):
        self.boxLayout.insertLayout(index, layout, stretch)


class VerticalScrollWidget(SingleScrollWidgetBase):
    """ 平滑垂直滚动小部件 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent, Qt.Orientation.Vertical)
        self.boxLayout = VBoxLayout(self._widget)


class HorizontalScrollWidget(SingleScrollWidgetBase):
    """ 平滑水平滚动小部件 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self.boxLayout = HBoxLayout(self._widget)


class ScrollWidget(ScrollArea):
    """ 平滑双向滚动小部件 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__widget = QWidget()
        self.setWidget(self.__widget)
        self.setWidgetResizable(True)

    def createVBoxLayout(self):
        """ create vertical layout """
        return VBoxLayout(self.__widget)

    def createHBoxLayout(self):
        """ create horizontal layout """
        return HBoxLayout(self.__widget)


class SmoothScrollWidget(SmoothScrollArea, ScrollWidget):
    """ 靠动画实现的平滑双向滚动小部件 """
    def __init__(self, parent=None):
        super().__init__(parent)
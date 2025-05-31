# coding:utf-8
from typing import overload, Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ...common.icon import FluentIcon
from .sliding_navigation_bar import SlidingNavigationBar
from ..widgets.stacked_widget import PopUpAniStackedWidget


class SlidingNavigationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgetLayout = QVBoxLayout(self)
        self.navigation = SlidingNavigationBar(self)
        self.stackedWidget = PopUpAniStackedWidget(self)
        self.__initLayout()

    def __initLayout(self):
        self._widgetLayout.addWidget(self.navigation)
        self._widgetLayout.addWidget(self.stackedWidget)

    def _switchTo(self, widget: QWidget):
        self.stackedWidget.setCurrentWidget(widget)

    @overload
    def setCurrentWidget(self, item: str): ...
    @overload
    def setCurrentWidget(self, item: QWidget): ...

    def setCurrentWidget(self, item: Union[str, QWidget]):
        if isinstance(item, QWidget):
            item = item.property("routeKey")
        self.navigation.setCurrentWidget(item)

    def addSubInterface(self, routeKey: str, text: str, widget: QWidget, icon: FluentIcon = None, alignment=Qt.AlignTop, toolTip=None):
        widget.setProperty("routeKey", routeKey)
        self.navigation.addItem(routeKey, text, icon, lambda: self._switchTo(widget), alignment=alignment, toolTip=toolTip)
        self.stackedWidget.addWidget(widget)

    def removeSubInterface(self, widget: QWidget):
        self.navigation.removeItem(widget.property("routeKey"))
        self.stackedWidget.removeWidget(widget)

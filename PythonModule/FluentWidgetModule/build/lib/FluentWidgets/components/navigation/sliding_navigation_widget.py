# coding:utf-8
from typing import overload, Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ...common.icon import FluentIcon
from .sliding_navigation_bar import SlidingNavigationBar, SlidingToolNavigationBar, SlidingWidget
from ..widgets.stacked_widget import PopUpAniStackedWidget


class SlidingNavigationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgetLayout = QVBoxLayout(self)
        self._slidingNavigationBar = SlidingNavigationBar(self)
        self._stackedWidget = PopUpAniStackedWidget(self)

    def __initLayout(self):
        self._widgetLayout.addWidget(self._slidingNavigationBar)
        self._widgetLayout.addWidget(self._stackedWidget)

    def _switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    @overload
    def setCurrentWidget(self, item: str): ...
    @overload
    def setCurrentWidget(self, item: QWidget): ...

    def setCurrentWidget(self, item: Union[str, QWidget]):
        if isinstance(item, QWidget):
            item = item.property("routeKey")
        self._slidingNavigationBar.setCurrentWidget(item)

    def addSubInterface(self, routeKey: str, text: str, widget: QWidget, icon: FluentIcon = None, alignment=Qt.AlignTop, toolTip=None):
        widget.setProperty("routeKey", routeKey)
        self._slidingNavigationBar.addItem(routeKey, text, icon, lambda: self._switchTo(widget), alignment=alignment, toolTip=toolTip)
        self._stackedWidget.addWidget(widget)

    def removeSubInterface(self, widget: QWidget):
        self._slidingNavigationBar.removeItem(widget.property("routeKey"))
        self._stackedWidget.removeWidget(widget)
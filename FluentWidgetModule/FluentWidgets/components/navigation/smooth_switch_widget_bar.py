# coding:utf-8
from typing import Union

from PySide6.QtGui import Qt, QColor, QIcon
from PySide6.QtCore import QPropertyAnimation, QTimer, QPoint, QEvent
from qfluentwidgets import FluentIconBase

from ..layout import HBoxLayout
from ..widgets import Widget
from .smooth_switch_widget import (
    SmoothSwitchWidget, SmoothSwitchLine, SmoothSwitchSeparator, SmoothSwitchToolButton,
    SmoothSwitchPushButton
)


class SmoothSwitchToolButtonBar(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__items = {} # type: Dict[str, SmoothSwitchWidget]
        self.widgetLayout = HBoxLayout(self)
        self.currentWidget = None
        self.widgetLayout.setAlignment(Qt.AlignTop)
        parent.installEventFilter(self)

        self.line = SmoothSwitchLine(self)
        self.__posAni = QPropertyAnimation(self.line, b'pos')

    def addSeparator(self):
        self.widgetLayout.addWidget(SmoothSwitchSeparator(self))
        pass

    def insertSeparator(self, index):
        pass

    def setItemBackgroundColor(self, light, dark):
        for item in self.__items.values():
            item.setLightBackgroundColor(light)
            item.setDarkBackgroundColor(dark)

    def setItemSelectedColor(self, color: QColor | str):
        for item in self.__items.values():
            item.setTextSelectedColor(color)

    def setItemSize(self, width: int, height: int):
        for item in self.__items.values():
            item.setFixedSize(width, height)

    def setCurrentWidget(self, routeKey: str):
        if routeKey not in self.__items.keys():
            raise KeyError(f'{routeKey} is not in items')
        QTimer.singleShot(1, lambda: self._onClicked(self.__items[routeKey]))

    def _setTextColor(self, item: SmoothSwitchWidget):
        if item.isSelected:
            return
        item.updateTextColor(item.isHover)

    def append(self, routeKey: str, item: SmoothSwitchWidget):
        self.__items[routeKey] = item

    def addItem(self, routeKey: str, icon: Union[str, QIcon, FluentIconBase] = None, isSelected=False):
        if routeKey in self.getAllWidget().keys():
            raise KeyError(f'{routeKey} is already in items')
        item = SmoothSwitchToolButton(icon, self)
        self.append(routeKey, item)
        item.clicked.connect(lambda w: self._onClicked(w))
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        self.widgetLayout.addWidget(item)
        if isSelected:
            self.setCurrentWidget(routeKey)

    def __getPos(self, item: SmoothSwitchWidget):
        pos = item.pos()
        x = pos.x()
        y = pos.y()
        width = item.width()
        height = item.height()
        return QPoint(x + width / 2 - self.line.width() / 2, y + height + 5)

    def _onClicked(self, item: SmoothSwitchWidget):
        for _ in self.__items.values():
            _.setSelected(False)
        self.currentWidget = item
        item.setSelected(True)
        self.line.setFixedWidth(item.width()/2)
        self.__createPosAni(item)

    def __createPosAni(self, item: SmoothSwitchWidget):
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self.line.pos())
        self.__posAni.setEndValue(self.__getPos(item))
        self.__posAni.start()

    def eventFilter(self, watched, event):
        if watched is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            if self.currentWidget:
                self.line.move(self.__getPos(self.currentWidget))
                self.line.setFixedWidth(self.currentWidget.width() / 2)
        return super().eventFilter(watched, event)

    def getWidget(self, routeKey: str):
        return self.__items[routeKey]

    def getAllWidget(self):
        return self.__items


class SmoothSwitchPushButtonBar(SmoothSwitchToolButtonBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgetLayout.setAlignment(Qt.AlignCenter)

    def addItem(self, routeKey: str, text: str, icon: Union[str, QIcon, FluentIconBase] = None, isSelected=False):
        if routeKey in self.getAllWidget().keys():
            raise KeyError(f'{routeKey} is already in items')
        item = SmoothSwitchPushButton(text, icon, self)
        self.append(routeKey, item)
        item.clicked.connect(lambda w: self._onClicked(w))
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        self.widgetLayout.addWidget(item)
        if isSelected:
            self.setCurrentWidget(routeKey)
# coding:utf-8
from typing import Union
from PySide6.QtGui import QPainter, QColor, Qt, QIcon
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QWidget
from qfluentwidgets import isDarkTheme, FluentIcon, FluentIconBase, TransparentToolButton

from ..layout import VBoxLayout
from ..widgets import VerticalScrollWidget
from ...common import setToolTipInfo, setToolTipInfos
from .navigation_widget import (
    NavigationWidget, NavigationItemPosition, NavigationButton, RouteKeyError, NavigationSeparator
)

class NavigationBar(QWidget):
    """ navigation bar widget """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._isExpand = False
        self.__items = {}  # type: dict[str, NavigationWidget]
        self.__history = [] # type: list[str]
        self._expandWidth = 256
        self._collapsedWidth = 65

        self._navLayout = VBoxLayout(self)
        self._returnButton = TransparentToolButton(FluentIcon.RETURN, self)
        self._expandButton = TransparentToolButton(FluentIcon.MENU, self)
        self._returnButton.setFixedSize(45, 35)
        self._expandButton.setFixedSize(45, 35)
        self._scrollWidget = VerticalScrollWidget(self)
        self.__expandNavAni = QPropertyAnimation(self, b'maximumWidth')

        self.__initScrollWidget()
        self.__initLayout()
        self.setMaximumWidth(self._collapsedWidth)
        self.enableReturn(False)
        self.__connectSignalSlot()
        setToolTipInfos(
            [self._returnButton, self._expandButton],
            ['返回', '展开导航栏'],
            1500
        )

    def __initLayout(self):
        self._navLayout.addWidgets([self._returnButton, self._expandButton])

        self._topLayout = VBoxLayout()
        self._topLayout.setSpacing(5)
        self._topLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._bottomLayout = VBoxLayout()
        self._navLayout.addLayout(self._topLayout)
        self._navLayout.addWidget(self._scrollWidget)
        self._navLayout.addLayout(self._bottomLayout)

    def __initScrollWidget(self):
        self._scrollWidget.enableTransparentBackground()
        self._scrollWidget.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._scrollWidget.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def __updateHistory(self):
        if len(self.__history) > 1:
            self.__history.pop()
            return self.__history.pop()

    def __connectSignalSlot(self):
        self._returnButton.clicked.connect(lambda: self.setCurrentItem(self.__updateHistory()))
        self._expandButton.clicked.connect(self.expandNavigation)

    def expandNavigation(self):
        """ expand navigation bar """
        if self._isExpand:
            self._isExpand = False
            width = self._collapsedWidth
        else:
            self._isExpand = True
            width = self._expandWidth
        self.__createExpandNavAni(width)

    def __createExpandNavAni(self, endValue):
        self.__expandNavAni.setDuration(120)
        self.__expandNavAni.setStartValue(self.width())
        self.__expandNavAni.setEndValue(endValue)
        self.__expandNavAni.start()
        self.__expandNavAni.finished.connect(lambda: self.__expandAllButton(self._isExpand))

    def enableReturn(self, enable: bool):
        self._returnButton.setVisible(enable)

    def setExpandWidth(self, width: int):
        self._expandWidth = width

    def setCollapsedWidth(self, width: int):
        self._collapsedWidth = width

    def _onClickWidget(self, item):
        for w in self.__items.values():
            w.setSelected(False)
        item.setSelected(True)
        routeKey = item.property("routeKey")
        if self.__history and routeKey == self.__history[-1]:
            return
        self._returnButton.setEnabled(True)
        self.__history.append(routeKey)
        if len(self.__history) == 1:
            self._returnButton.setEnabled(False)
            return

    def addItem(
            self,
            routeKey: str,
            icon: Union[str, QIcon, FluentIconBase],
            text: str,
            isSelected=False,
            onClick=None,
            position=NavigationItemPosition.SCROLL
    ):
        """
        add Item to Navigation Bar

        ----------
            routeKey: str
                routeKey Are Unique

            isSelected: bool
                item Whether itis Selected

            position: NavigationItemPosition
                position to add to the navigation bar
        """
        return self.insertItem(-1, routeKey, icon, text, isSelected, onClick, position)

    def insertItem(
            self,
            index: int,
            routeKey: str,
            icon: Union[str, QIcon, FluentIconBase],
            text: str,
            isSelected=False,
            onClick=None,
            position=NavigationItemPosition.SCROLL
    ):
        """
        insert Item to Navigation Bar

        ----------
            routeKey: str
                routeKey Are Unique

            isSelected: bool
                item Whether itis Selected

            position: NavigationItemPosition
                position to add to the navigation bar
        """
        if routeKey in self.__items.keys():
            raise RouteKeyError('routeKey Are Not Unique')
        item = NavigationButton(icon, text, isSelected, self)
        item.setProperty("routeKey", routeKey)
        item.EXPAND_WIDTH = self.width() - 20
        self.__items[routeKey] = item
        item.clicked.connect(lambda: self._onClickWidget(item))
        item.clicked.connect(onClick)
        setToolTipInfo(item, routeKey, 1500)
        return self._insertWidgetToLayout(index, item, position)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick=None, position=NavigationItemPosition.TOP):
        """
        add Widget to Navigation Bar

        ----------
            routeKey: str
                routeKey Are Unique
            position: NavigationItemPosition
                position to add to the navigation bar
        """
        return self.insertWidget(-1, routeKey, widget, onClick, position)

    def insertWidget(
            self,
            index: int,
            routeKey: str,
            widget: NavigationWidget,
            onClick=None,
            position=NavigationItemPosition.SCROLL
    ):
        """
        insert Widget to Navigation Bar

        ----------
            routeKey: str
                routeKey Are Unique

            position: NavigationItemPosition
                position to add to the navigation bar
        """
        widget.clicked.connect(lambda: self._onClickWidget(widget))
        widget.clicked.connect(onClick)
        self.__items[routeKey] = widget
        widget.setProperty("routeKey", routeKey)
        setToolTipInfo(widget, routeKey, 1500)
        return self._insertWidgetToLayout(index, widget, position)

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        """ add separator to navigation bar """
        self.insertSeparator(-1, position)

    def insertSeparator(self, index: int, position=NavigationItemPosition.SCROLL):
        """ insert separator to navigation bar """
        separator = NavigationSeparator(self)
        self._insertWidgetToLayout(index, separator, position)

    def removeWidget(self, routeKey: str):
        """ remove widget from items """
        if routeKey not in self.__items.keys():
            raise RouteKeyError('routeKey not in items')
        self.__items.pop(routeKey).deleteLater()
        self.__history.remove(routeKey)

    def setCurrentItem(self, routeKey: str):
        if routeKey not in self.__items.keys():
            return
        self._onClickWidget(self.__items[routeKey])
        self.__items[routeKey].click()

    def getWidget(self, routeKey: str):
        if routeKey not in self.__items.keys():
            raise RouteKeyError('routeKey not in items')
        return self.__items[routeKey]

    def getAllWidget(self):
        return self.__items

    def _insertWidgetToLayout(self, index: int, widget: NavigationWidget, position=NavigationItemPosition.SCROLL):
        if position == NavigationItemPosition.SCROLL:
            self._scrollWidget.vBoxLayout.insertWidget(index, widget)
        elif position == NavigationItemPosition.TOP:
            self._topLayout.insertWidget(index, widget)
        else:
            self._bottomLayout.insertWidget(index, widget)
        return widget

    def __expandAllButton(self, expand: bool):
        for w in self.__items.values():
            w.EXPAND_WIDTH = self.width() - 8
            w.setExpend(expand)
        if self.width() > 100:
            self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        else:
            self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        color = QColor("#2d2d2d") if isDarkTheme() else QColor("#fafafa")
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), 8, 8)

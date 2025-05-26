# coding:utf-8
from typing import Union, Dict, List
from PySide6.QtGui import QPainter, QColor, Qt, QIcon
from PySide6.QtCore import QPropertyAnimation, QTimer, QPoint, QEvent

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import (
    VerticalScrollWidget, Widget, TransparentToolButton, SingleDirectionScrollArea, ToolTipPosition
)
from ...common.tool_info import setToolTipInfo, setToolTipInfos
from .navigation_widget import (
    ExpandNavigationWidget, ExpandNavigationButton, ExpandNavigationSeparator,
    SmoothWidget, SmoothSwitchLine, SmoothSeparator, SmoothSwitchPushButton, SmoothSwitchToolButton
)

from ...common.config import isDarkTheme
from ...common.icon import FluentIconBase, FluentIcon
from .navigation_panel import RouteKeyError, NavigationItemPosition

from qfluentwidgets import NavigationWidget


class NavigationBarBase(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _append(self, routeKey: str, item):
        if routeKey in self._items.keys():
            raise RouteKeyError("routeKey Are Not Unique")
        self._items[routeKey] = item

    def _remove(self, routeKey: str):
        if routeKey not in self._items.keys():
            raise RouteKeyError(f"{routeKey} is not in items")
        self._items.pop(routeKey).deleteLater()

    def _onClicked(self, item):
        raise NotImplementedError

    def addItem(
            self,
            routeKey: str,
            icon: Union[str, QIcon, FluentIconBase],
            text: str,
            onClick=None
    ):
        raise NotImplementedError

    def insertItem(
            self,
            index: int,
            routeKey: str,
            icon: Union[str, QIcon, FluentIconBase],
            text: str,
            onClick=None
    ):
        raise NotImplementedError

    def addSeparator(self):
        """ add separator to navigation bar """
        raise NotImplementedError

    def insertSeparator(self, index: int):
        """ insert separator to navigation bar """
        raise NotImplementedError

    def setCurrentWidget(self, routeKey: str):
        raise NotImplementedError

    def removeWidget(self, routeKey: str):
        """ remove widget from items """
        raise NotImplementedError

    def getCurrentWidget(self):
        raise NotImplementedError

    def getWidget(self, routeKey: str):
        if routeKey not in self._items.keys():
            raise RouteKeyError(f"{routeKey} is not in items")
        return self._items[routeKey]

    def getAllWidget(self):
        return self._items


class ExpandNavigationBar(NavigationBarBase):
    """ navigation bar widget """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._isExpand = False
        self._items = {}  # type: Dict[str, ExpandNavigationWidget]
        self.__history = [] # type: List[str]
        self.__currentWidget = None # type: ExpandNavigationWidget
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
        self.enableReturnButton(False)
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
        self._topLayout.setAlignment(Qt.AlignTop)
        self._bottomLayout = VBoxLayout()
        self._navLayout.addLayout(self._topLayout)
        self._navLayout.addWidget(self._scrollWidget)
        self._navLayout.addLayout(self._bottomLayout)

    def __initScrollWidget(self):
        self._scrollWidget.enableTransparentBackground()
        self._scrollWidget.boxLayout.setAlignment(Qt.AlignTop)
        self._scrollWidget.boxLayout.setContentsMargins(0, 0, 0, 0)
        self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollWidget.setMinimumHeight(120)

    def __updateHistory(self):
        if len(self.__history) > 1:
            self.__history.pop()
            return self.__history.pop()

    def __connectSignalSlot(self):
        self._returnButton.clicked.connect(lambda: self.setCurrentWidget(self.__updateHistory()))
        self._expandButton.clicked.connect(self.expandNavigation)

    def __createExpandNavAni(self, endValue):
        self.__expandNavAni.setDuration(160)
        self.__expandNavAni.setStartValue(self.width())
        self.__expandNavAni.setEndValue(endValue)
        self.__expandNavAni.start()
        self.__expandNavAni.finished.connect(lambda: self.__expandAllButton(self._isExpand))

    def __expandAllButton(self, expand: bool):
        for w in self._items.values():
            w.EXPAND_WIDTH = self.width() - 8
            w.setExpend(expand)
        if self.width() > 100:
            self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        else:
            self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _insertWidgetToLayout(self, index: int, widget: ExpandNavigationWidget, position=NavigationItemPosition.SCROLL):
        if position == NavigationItemPosition.SCROLL:
            self._scrollWidget.insertWidget(index, widget)
        elif position == NavigationItemPosition.TOP:
            self._topLayout.insertWidget(index, widget)
        else:
            self._bottomLayout.insertWidget(index, widget)

    def _onClicked(self, item: ExpandNavigationWidget):
        for w in self.getAllWidget().values():
            w.setSelected(False)
        item.setSelected(True)
        self.__currentWidget = item

        routeKey = item.property("routeKey")
        if self.__history and routeKey == self.__history[-1]:
            return
        self._returnButton.setEnabled(True)
        self.__history.append(routeKey)

        if len(self.__history) == 1:
            self._returnButton.setEnabled(False)
            return

    def expandNavigation(self):
        """ expand navigation bar """
        if self._isExpand:
            self._isExpand = False
            width = self._collapsedWidth
        else:
            self._isExpand = True
            width = self._expandWidth
        self.__createExpandNavAni(width)

    def enableReturnButton(self, enable: bool):
        self._returnButton.setVisible(enable)

    def setExpandWidth(self, width: int):
        self._expandWidth = width

    def setCollapsedWidth(self, width: int):
        self._collapsedWidth = width

    def addItem(self, routeKey, icon, text, isSelected=False, onClick=None, position=NavigationItemPosition.SCROLL):
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
        self.insertItem(-1, routeKey, icon, text, isSelected, onClick, position)

    def insertItem(self, index, routeKey, icon, text, isSelected=False, onClick=None, position=NavigationItemPosition.SCROLL):
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
        item = ExpandNavigationButton(icon, text, isSelected, self)
        self._append(routeKey, item)

        item.EXPAND_WIDTH = self.width() - 8
        item.clicked.connect(onClick)
        item.clicked.connect(lambda: self._onClicked(item))

        item.setProperty("routeKey", routeKey)
        setToolTipInfo(item, routeKey, 1500)
        self._insertWidgetToLayout(index, item, position)

    def addWidget(self, routeKey: str, widget: ExpandNavigationWidget, onClick=None, position=NavigationItemPosition.TOP):
        """
        add Widget to Navigation Bar

        ----------
            routeKey: str
                routeKey Are Unique
            position: NavigationItemPosition
                position to add to the navigation bar
        """
        self.insertWidget(-1, routeKey, widget, onClick, position)

    def insertWidget(
            self,
            index: int,
            routeKey: str,
            widget: ExpandNavigationWidget,
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
        self._append(routeKey, widget)

        widget.clicked.connect(lambda: self._onClicked(widget))
        widget.clicked.connect(onClick)

        widget.setProperty("routeKey", routeKey)
        setToolTipInfo(widget, routeKey, 1500)
        self._insertWidgetToLayout(index, widget, position)

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        return self.insertSeparator(-1, position)

    def insertSeparator(self, index, position=NavigationItemPosition.SCROLL):
        separator = ExpandNavigationSeparator(self)
        self._insertWidgetToLayout(index, separator, position)
        return separator

    def removeWidget(self, routeKey):
        self._remove(routeKey)
        self.__history.remove(routeKey)

    def setCurrentWidget(self, routeKey):
        if routeKey not in self._items.keys():
            return
        item = self.getWidget(routeKey)
        self._onClicked(item)
        item.click()

    def getCurrentWidget(self):
        return self.__currentWidget

    def getWidget(self, routeKey) -> ExpandNavigationWidget:
        return super().getWidget(routeKey)

    def getAllWidget(self) -> Dict[str, ExpandNavigationWidget]:
        return super().getAllWidget()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        color = QColor("#2d2d2d") if isDarkTheme() else QColor("#fafafa")
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), 8, 8)


class SmoothSwitchToolBar(NavigationBarBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = {} # type: Dict[str, SmoothWidget]
        self._boxLayout = HBoxLayout(self)
        self.__widget = Widget()
        self._widgetLayout = HBoxLayout(self.__widget)
        self.__currentWidget = None # type: SmoothWidget
        self.__slideLineWidth = 30
        self.__initScrollWidget()

        self.__slideLine = SmoothSwitchLine(self.__widget)
        self.__slideLine.setFixedSize(self.__slideLineWidth, 3)
        self.__posAni = QPropertyAnimation(self.__slideLine, b'pos')

        self._boxLayout.addWidget(self._scrollWidget, alignment=Qt.AlignTop)
        parent.installEventFilter(self)

    def __initScrollWidget(self):
        self._scrollWidget = SingleDirectionScrollArea(self, Qt.Orientation.Horizontal)
        self._scrollWidget.enableTransparentBackground()
        self._scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollWidget.setWidgetResizable(True)
        self._scrollWidget.setWidget(self.__widget)

    def __getSlideEndPos(self, item: SmoothWidget):
        pos = item.pos()
        x = pos.x()
        y = pos.y()
        width = item.width()
        height = item.height()
        return QPoint(x + width / 2 - self.__slideLineWidth / 2, y + height + 5)

    def __createPosAni(self, item: SmoothWidget):
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self.__slideLine.pos())
        self.__posAni.setEndValue(self.__getSlideEndPos(item))
        self.__posAni.start()

    def __adjustSlideLinePos(self):
        QTimer.singleShot(1, lambda: (self.__slideLine.move(self.__getSlideEndPos(self.__currentWidget))))

    @staticmethod
    def _setTextColor(item: SmoothWidget):
        if item.isSelected:
            return
        item.updateSelectedColor(item.isHover)

    def _onClicked(self, item: SmoothWidget):
        self.setCurrentWidget(item.property('routeKey'))

    def setBarAlignment(self, alignment: Qt.AlignmentFlag):
        self._widgetLayout.setAlignment(alignment)

    def addSeparator(self):
        return self.insertSeparator(-1)

    def insertSeparator(self, index: int):
        separator = SmoothSeparator(self)
        self._widgetLayout.insertWidget(index, separator)
        return separator

    def setSlideLineWidth(self, width: int):
        self.__slideLineWidth = width
        self.__slideLine.setFixedWidth(self.__slideLineWidth)
        self.__adjustSlideLinePos()

    def setSlideLineColor(self, color: str | QColor):
        self.__slideLine.setLineColor(color)

    def setItemBackgroundColor(self, light: QColor | str, dark: QColor | str):
        for item in self._items.values():
            item.setLightBackgroundColor(light)
            item.setDarkBackgroundColor(dark)

    def setItemSelectedColor(self, color: QColor | str):
        for item in self._items.values():
            item.setSelectedColor(color)

    def setItemSize(self, width: int, height: int):
        for item in self._items.values():
            item.setFixedSize(width, height)

    def setIconSize(self, size: int):
        for item in self._items.values():
            item.setIconSize(size)

    def setCurrentWidget(self, routeKey: str):
        if routeKey not in self._items.keys():
            return
        if self.__slideLine.isHidden(): self.__slideLine.show()
        for w in self._items.values():
            w.setSelected(False)
        item = self.getWidget(routeKey)
        self.__currentWidget = item
        item.setSelected(True)
        QTimer.singleShot(1, lambda: self.__createPosAni(item))

    def addItem(self, routeKey, icon, onClick=None, isSelected=False):
        item = SmoothSwitchToolButton(icon, self)
        item.setProperty('routeKey', routeKey)
        self._append(routeKey, item)
        setToolTipInfo(item, routeKey, 1500, ToolTipPosition.TOP)
        self._widgetLayout.addWidget(item)

        item.clicked.connect(lambda w: self._onClicked(w))
        item.clicked.connect(onClick)
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        if isSelected:
            self.setCurrentWidget(routeKey)

    def getCurrentWidget(self):
        return self.__currentWidget

    def getWidget(self, routeKey: str) -> SmoothWidget:
        return super().getWidget(routeKey)

    def getAllWidget(self) -> Dict[str, SmoothWidget]:
        return super().getAllWidget()

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Resize, QEvent.WindowStateChange] and self.getCurrentWidget():
            self.__adjustSlideLinePos()
        return super().eventFilter(obj, event)


class SmoothSwitchBar(SmoothSwitchToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def addItem(self, routeKey, text: str, icon=None, onClick=None, isSelected=False):
        item = SmoothSwitchPushButton(text, icon, self)
        item.setProperty('routeKey', routeKey)
        self._append(routeKey, item)
        setToolTipInfo(item, routeKey, 1500, ToolTipPosition.TOP)
        self._widgetLayout.addWidget(item)

        item.clicked.connect(lambda w: self._onClicked(w))
        item.clicked.connect(onClick)
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        if isSelected:
            self.setCurrentWidget(routeKey)
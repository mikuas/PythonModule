# coding:utf-8
from typing import Union, List

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, Qt
from qfluentwidgets import SegmentedWidget, SegmentedToggleToolWidget, TabBar, TabCloseButtonDisplayMode

from .navigation_bar import ExpandNavigationBar, SmoothSwitchBar
from ..layout import HBoxLayout, VBoxLayout
from ...common import FluentIconBase
from ..widgets import Widget, PopUpStackedWidget
from .navigation_panel import NavigationItemPosition
from .navigation_panel import RouteKeyError


class NavigationBase(Widget):
    """ 导航组件基类 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._widgetLayout = VBoxLayout(self)
        self._stackedWidget = PopUpStackedWidget(parent=self)
        self.navigationBar = None

    def _initLayout(self):
        self._widgetLayout.addWidgets([self.navigationBar, self._stackedWidget])

    def addSeparator(self):
        raise NotImplementedError

    def insertSeparator(self, index: int):
        raise NotImplementedError

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[str, QIcon, FluentIconBase]
    ):
        """
        add Sub Interface

        ----------
            routeKey: str
                routeKey Are Unique

            text: str
                navigation text

            widget: QWidget
                widget of current navigation

            icon: str | QIcon | FluentIconBase
                navigation icon
        """
        raise NotImplementedError

    def switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    def setCurrentWidget(self, routeKey: str):
        self.navigationBar.setCurrentWidget(routeKey)


class SegmentedNavWidget(NavigationBase):
    """ 分段导航 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigationBar = SegmentedWidget(self)
        self._initLayout()

    def setCurrentWidget(self, routeKey):
        self.navigationBar.setCurrentItem(routeKey)

    def addSubInterface(self, routeKey, text, widget, icon=None):
        self._stackedWidget.addWidget(widget)
        self.navigationBar.addItem(routeKey, text, lambda: self.switchTo(widget), icon)


class SegmentedToggleNavWidget(SegmentedNavWidget):
    def __init__(self, parent=None):
        """ 主题色选中导航 """
        super().__init__(parent)
        self.navigationBar = SegmentedToggleToolWidget(self)

    def addSubInterface(self, routeKey, widget, icon):
        self._stackedWidget.addWidget(widget)
        self.navigationBar.addItem(routeKey, icon, lambda: self.switchTo(widget))


class LabelBarNavWidget(NavigationBase):
    """ 标签页组件 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigationBar = TabBar(self)
        self.__items = [] # type: List[QWidget]
        self._initLayout()
        self.__initTitleBar()
        self.enableAddButton(False)

    def __initTitleBar(self):
        self.navigationBar.setTabShadowEnabled(True)
        self.navigationBar.setMovable(True)
        self.navigationBar.setScrollable(True)
        self.navigationBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

    def setCurrentWidget(self, routeKey):
        self.navigationBar.setCurrentTab(routeKey)

    def setTabShadowEnabled(self, enable: bool):
        self.navigationBar.setTabShadowEnabled(enable)

    def setMovable(self, movable: bool):
        self.navigationBar.setMovable(movable)

    def setScrollable(self, scrollable: bool):
        self.navigationBar.setScrollable(scrollable)

    def setCloseButtonDisplayMode(self, mode: TabCloseButtonDisplayMode):
        self.navigationBar.setCloseButtonDisplayMode(mode)

    def enableClose(self):
        self.navigationBar.tabCloseRequested.connect(lambda index: self.removeWidgetByIndex(index))

    def enableAddButton(self, enable: bool):
        if enable:
            self.navigationBar.addButton.show()
            return
        self.navigationBar.addButton.hide()

    def setCloseButtonDisplayMode(self, mode=TabCloseButtonDisplayMode.NEVER):
        self.navigationBar.setCloseButtonDisplayMode(mode)

    """ !!!!!!!!!!!!!!! """
    def addSubInterface(self, routeKey, text, widget, icon=None):
        self._stackedWidget.addWidget(widget)
        self.__items.append(widget)
        widget.setProperty('text', text)
        widget.setProperty('routeKey', routeKey)
        self.navigationBar.addTab(routeKey, text, icon, lambda: self.switchTo(widget))

    """ !!!!!!!!!!!!!!! """
    def removeWidgetByIndex(self, index: int):
        if index > len(self.__items):
            return
        item = self.__items.pop(index)
        self._stackedWidget.removeWidget(item)
        self.navigationBar.removeTab(index)
        if index > 0:
            self._stackedWidget.setCurrentIndex(index - 1)

    """ !!!!!!!!!!!!!!! """
    def removeWidgetByName(self, widget: QWidget):
        if widget not in self.__items:
            return
        self.removeWidgetByIndex(self.__items.index(widget))


class SideNavWidget(NavigationBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.__transparentBgc = False
        self._barLayout = HBoxLayout()
        self.__widgets = {} # type: dict[str, QWidget]
        self.navigationBar = ExpandNavigationBar(self)

        self._initLayout()
        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self.setRadius(8, 8)

    def _initLayout(self):
        self._widgetLayout.addLayout(self._barLayout)
        self._barLayout.addWidgets([self.navigationBar, self._stackedWidget])

    def enableReturnButton(self, enable: bool):
        self.navigationBar.enableReturnButton(enable)

    def expandNavigation(self):
        self.navigationBar.expandNavigation()

    def __addToStackedWidget(self, routeKey: str, widget: QWidget):
        if widget in self.__widgets:
            raise ValueError('widget already exists')
        self._stackedWidget.addWidget(widget)
        self.__widgets[routeKey] = widget

    def addSubInterface(self, routeKey, text, widget, icon, position=NavigationItemPosition.SCROLL):
        """
        add Sub Interface

        ----------
            routeKey: str
                routeKey Are Unique

            text: str
                navigation text

            icon: str | QIcon | FluentIconBase
                navigation icon

            widget: QWidget
                add widget to navigation bar

            position: NavigationItemPosition
                the add of navigation position
        """
        self.__addToStackedWidget(routeKey, widget)
        self.navigationBar.addItem(routeKey, icon, text, False, lambda: self.switchTo(widget), position)

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        return self.navigationBar.addSeparator(position)

    def insertSeparator(self, index, position=NavigationItemPosition.SCROLL):
        return self.navigationBar.insertSeparator(index, position)

    def removeWidget(self, routeKey: str):
        if routeKey not in self.__widgets:
            raise RouteKeyError("routeKey not in items")
        self._stackedWidget.removeWidget(self.__widgets[routeKey])
        self.navigationBar.removeWidget(routeKey)
        self.__widgets.pop(routeKey).deleteLater()

    def enableTransparentBackground(self, enable: bool):
        super().enableTransparentBackground(enable)
        if enable:
            self.navigationBar.paintEvent = self.paintEvent

    def getWidget(self, routeKey: str):
        return self.__widgets[routeKey]

    def getAllWidget(self):
        return self.__widgets


class SmoothSwitchNavWidget(NavigationBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigationBar = SmoothSwitchBar(self)
        self._initLayout()

    def setNavigationAlignment(self, alignment: Qt.AlignmentFlag):
        self.navigationBar.setBarAlignment(alignment)

    def addSeparator(self):
        return self.navigationBar.addSeparator()

    def insertSeparator(self, index):
        return self.navigationBar.insertSeparator(index)

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
    ):
        self.navigationBar.addItem(routeKey, text, icon, lambda: self.switchTo(widget))
        self._stackedWidget.addWidget(widget)

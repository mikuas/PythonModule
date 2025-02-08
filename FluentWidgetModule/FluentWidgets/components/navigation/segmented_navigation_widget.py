# coding:utf-8
from typing import Union, List

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QColor, QPainter, QPen, Qt
from qfluentwidgets import FluentIconBase, Pivot, VerticalSeparator, SegmentedWidget, SegmentedToolWidget, \
    SegmentedToggleToolWidget, TabBar, TabCloseButtonDisplayMode

from .navigation_bar import NavigationBar
from ..layout import HBoxLayout, VBoxLayout
from ..widgets import Widget, PopUpStackedWidget
from .navigation_widget import RouteKeyError, NavigationItemPosition


class NavigationBase(Widget):
    """ 导航组件基类 """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.hBoxLayout = HBoxLayout(self)
        self.stackedWidget = PopUpStackedWidget(parent=self)
        self.navigation = None

    def _initLayout(self):
        self.vLayout = VBoxLayout(self)
        self.hLayout = HBoxLayout()
        self.hBoxLayout.addLayout(self.vLayout)
        self.vLayout.addWidgets([self.navigation, self.stackedWidget])
        self.vLayout.addLayout(self.hLayout)

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
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
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(routeKey, text, lambda: self.switchTo(widget), icon)
        return self

    def switchTo(self, widget: QWidget):
        self.stackedWidget.setCurrentWidget(widget)

    def setCurrentItem(self, routeKey: str):
        self.navigation.setCurrentItem(routeKey)
        return self

    def enableNavCenter(self):
        self.vLayout.removeWidget(self.navigation)
        self.vLayout.insertWidget(0, self.navigation, alignment=Qt.AlignmentFlag.AlignHCenter)
        return self


class PivotNav(NavigationBase):
    """ 导航栏 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = Pivot(self)
        self._color = None
        self._enableSplitLine = True
        self._initLayout()

    def addNavSeparator(self):
        self.insertNavSeparator(-1)

    def insertNavSeparator(self, index: int):
        separator = VerticalSeparator(self)
        separator.setFixedHeight(self.navigation.height())
        self.navigation.hBoxLayout.insertWidget(index, separator)

    def enableSplitLine(self, isEnable: bool):
        self._enableSplitLine = isEnable
        self.update()

    def setSplitLineColor(self, color: QColor | str):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._enableSplitLine:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(self._color or QColor('#2d2d2d'), 1, Qt.SolidLine))
            painter.drawLine(0, 65, self.width(), 60)


class SegmentedNav(PivotNav):
    """ 分段导航 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = SegmentedWidget(self)
        self._initLayout()

    def paintEvent(self, event):
        pass


class SegmentedToolNav(PivotNav):
    """ 工具导航 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.navigation = SegmentedToolWidget(self)
        self._initLayout()
        self.enableNavCenter()

    def addSubInterface(self, routeKey, widget, icon=None):
        self.stackedWidget.addWidget(widget)
        self.navigation.addItem(routeKey, icon, lambda: self.switchTo(widget))
        return self

    def paintEvent(self, event):
        pass


class SegmentedToggleToolNav(SegmentedToolNav):
    def __init__(self, parent=None):
        """ 主题色选中导航 """
        super().__init__(parent)
        self.navigation = SegmentedToggleToolWidget(self)
        self._initLayout()
        self.enableNavCenter()


class LabelBarWidget(Widget):
    """ 标签页组件 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tabBar = TabBar(self)
        self._stackedWidget = PopUpStackedWidget(parent=self)
        self._hLayout = HBoxLayout(self)
        self._vLayout = VBoxLayout()
        self.__items = [] # type: List[QWidget]
        self.__initLayout()
        self.__initTitleBar()
        self.enableAddButton(False)

    def __initLayout(self):
        self._hLayout.addLayout(self._vLayout)
        self._vLayout.addWidgets([self._tabBar, self._stackedWidget])

    def __initTitleBar(self):
        self._tabBar.setTabShadowEnabled(True)
        self._tabBar.setMovable(True)
        self._tabBar.setScrollable(True)
        self._tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

    def setTabShadowEnabled(self, enable: bool):
        self._tabBar.setTabShadowEnabled(enable)

    def setMovable(self, movable: bool):
        self._tabBar.setMovable(movable)

    def setScrollable(self, scrollable: bool):
        self._tabBar.setScrollable(scrollable)

    def setCloseButtonDisplayMode(self, mode: TabCloseButtonDisplayMode):
        self._tabBar.setCloseButtonDisplayMode(mode)

    def enableClose(self):
        self._tabBar.tabCloseRequested.connect(lambda index: self.removeWidgetByIndex(index))


    def enableAddButton(self, enable: bool):
        if enable:
            self._tabBar.addButton.show()
            return
        self._tabBar.addButton.hide()

    def setCloseButtonDisplayMode(self, mode=TabCloseButtonDisplayMode.NEVER):
        self._tabBar.setCloseButtonDisplayMode(mode)

    def switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            widget: QWidget,
            icon: Union[QIcon, str, FluentIconBase] = None
    ):
        self._stackedWidget.addWidget(widget)
        self.__items.append(widget)
        widget.setProperty('text', text)
        widget.setProperty('routeKey', routeKey)
        self._tabBar.addTab(routeKey, text, icon, lambda: self.switchTo(widget))
        return widget

    def addSubInterfaces(
            self, routeKeys: List[str],
            texts: List[str],
            widgets: List[QWidget] = None,
            icons: List[Union[QIcon, str, FluentIconBase]] = None
    ):
        icons = icons if icons is not None else [None for _ in range(len(routeKeys))]
        for key, text, icon, widget in zip(routeKeys, texts, icons, widgets):
            self.addSubInterface(key, text, widget, icon)

    def removeWidgetByIndex(self, index: int):
        if index > len(self.__items):
            return
        item = self.__items.pop(index)
        self._stackedWidget.removeWidget(item)
        self._tabBar.removeTab(index)
        if index > 0:
            self._stackedWidget.setCurrentIndex(index - 1)

    def removeWidgetByName(self, widget: QWidget):
        if widget not in self.__items:
            return
        self.removeWidgetByIndex(self.__items.index(widget))


class SideNavigationWidget(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.__transparentBgc = False
        self.__widgets = {} # type: dict[str, QWidget]
        self._widgetLayout = HBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self._stackedWidget = PopUpStackedWidget(parent=self)

        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.addWidget(self.navigationBar)
        self._widgetLayout.addWidget(self._stackedWidget)
        self.setRadius(8, 8)

    def enableReturn(self, enable: bool):
        self.navigationBar.enableReturn(enable)
        return self

    def expandNavigation(self):
        self.navigationBar.expandNavigation()
        return self

    def switchTo(self, widget: QWidget):
        self._stackedWidget.setCurrentWidget(widget)

    def __addToStackedWidget(self, routeKey: str, widget: QWidget):
        if widget in self.__widgets:
            raise ValueError('widget already exists')
        self._stackedWidget.addWidget(widget)
        self.__widgets[routeKey] = widget

    def addSubInterface(
            self,
            routeKey: str,
            text: str,
            icon: Union[str, QIcon, FluentIconBase],
            widget: QWidget,
            position=NavigationItemPosition.SCROLL
    ):
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
        return self

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        self.navigationBar.addSeparator(position)
        return self

    def insertSeparator(self, index: int, position=NavigationItemPosition.SCROLL):
        self.navigationBar.insertSeparator(index, position)
        return self

    def setCurrentWidget(self, routeKey: str):
        """ set current displayed widget """
        self.navigationBar.setCurrentItem(routeKey)
        return self

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
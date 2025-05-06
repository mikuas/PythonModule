# coding:utf-8
from typing import Union, Dict, List
from PySide6.QtGui import QPainter, QColor, Qt, QIcon, QFont
from PySide6.QtCore import QPropertyAnimation, QTimer, QPoint, QEvent, Property, QRectF, QRect
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import (
    VerticalScrollWidget, Widget, TransparentToolButton, SingleDirectionScrollArea, ToolTipPosition, ScrollArea
)
from ...common.tool_info import setToolTipInfo, setToolTipInfos
from .navigation_widget import (
    ExpandNavigationWidget, ExpandNavigationButton, ExpandNavigationSeparator,
    SmoothWidget, SmoothSwitchLine, SmoothSeparator, SmoothSwitchPushButton, SmoothSwitchToolButton,
    NavigationPushButton, NavigationWidget
)

from ...common.config import isDarkTheme
from ...common.font import setFont
from ...common.style_sheet import themeColor, FluentStyleSheet
from ...common.icon import drawIcon, FluentIconBase, toQIcon, FluentIcon
from ...common.router import qrouter
from .navigation_panel import RouteKeyError, NavigationItemPosition


class IconSlideAnimation(QPropertyAnimation):
    """ Icon sliding animation """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._offset = 0
        self.maxOffset = 6
        self.setTargetObject(self)
        self.setPropertyName(b"offset")

    def getOffset(self):
        return self._offset

    def setOffset(self, value: float):
        self._offset = value
        self.parent().update()

    def slideDown(self):
        """ slide down """
        self.setEndValue(self.maxOffset)
        self.setDuration(100)
        self.start()

    def slideUp(self):
        """ slide up """
        self.setEndValue(0)
        self.setDuration(100)
        self.start()

    offset = Property(float, getOffset, setOffset)



class NavigationBarPushButton(NavigationPushButton):
    """ Navigation bar push button """

    def __init__(self, icon: Union[str, QIcon, FluentIcon], text: str, isSelectable: bool, selectedIcon=None, parent=None):
        super().__init__(icon, text, isSelectable, parent)
        self.iconAni = IconSlideAnimation(self)
        self._selectedIcon = selectedIcon
        self._isSelectedTextVisible = True

        self.setFixedSize(64, 58)
        setFont(self, 11)

    def selectedIcon(self):
        if self._selectedIcon:
            return toQIcon(self._selectedIcon)

        return QIcon()

    def setSelectedIcon(self, icon: Union[str, QIcon, FluentIcon]):
        self._selectedIcon = icon
        self.update()

    def setSelectedTextVisible(self, isVisible):
        self._isSelectedTextVisible = isVisible
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        self._drawBackground(painter)
        self._drawIcon(painter)
        self._drawText(painter)

    def _drawBackground(self, painter: QPainter):
        if self.isSelected:
            painter.setBrush(QColor(255, 255, 255, 42) if isDarkTheme() else Qt.white)
            painter.drawRoundedRect(self.rect(), 5, 5)

            # draw indicator
            painter.setBrush(themeColor())
            if not self.isPressed:
                painter.drawRoundedRect(0, 16, 4, 24, 2, 2)
            else:
                painter.drawRoundedRect(0, 19, 4, 18, 2, 2)
        elif self.isPressed or self.isEnter:
            c = 255 if isDarkTheme() else 0
            alpha = 9 if self.isEnter else 6
            painter.setBrush(QColor(c, c, c, alpha))
            painter.drawRoundedRect(self.rect(), 5, 5)

    def _drawIcon(self, painter: QPainter):
        if (self.isPressed or not self.isEnter) and not self.isSelected:
            painter.setOpacity(0.6)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        if self._isSelectedTextVisible:
            rect = QRectF(22, 13, 20, 20)
        else:
            rect = QRectF(22, 13 + self.iconAni.offset, 20, 20)

        selectedIcon = self._selectedIcon or self._icon

        if isinstance(selectedIcon, FluentIconBase) and self.isSelected:
            selectedIcon.render(painter, rect, fill=themeColor().name())
        elif self.isSelected:
            drawIcon(selectedIcon, painter, rect)
        else:
            drawIcon(self._icon, painter, rect)

    def _drawText(self, painter: QPainter):
        if self.isSelected and not self._isSelectedTextVisible:
            return

        if self.isSelected:
            painter.setPen(themeColor())
        else:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)

        painter.setFont(self.font())
        rect = QRect(0, 32, self.width(), 26)
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def setSelected(self, isSelected: bool):
        if isSelected == self.isSelected:
            return

        self.isSelected = isSelected

        if isSelected:
            self.iconAni.slideDown()
        else:
            self.iconAni.slideUp()


class NavigationBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollArea = ScrollArea(self)
        self.scrollWidget = QWidget()

        self.vBoxLayout = QVBoxLayout(self)
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)

        self.items = {}   # type: Dict[str, NavigationWidget]
        self.history = qrouter

        self.__initWidget()

    def __initWidget(self):
        self.resize(48, self.height())
        self.setAttribute(Qt.WA_StyledBackground)
        self.window().installEventFilter(self)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.horizontalScrollBar().setEnabled(False)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.scrollWidget.setObjectName('scrollWidget')
        FluentStyleSheet.NAVIGATION_INTERFACE.apply(self)
        FluentStyleSheet.NAVIGATION_INTERFACE.apply(self.scrollWidget)
        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(0, 5, 0, 5)
        self.topLayout.setContentsMargins(4, 0, 4, 0)
        self.bottomLayout.setContentsMargins(4, 0, 4, 0)
        self.scrollLayout.setContentsMargins(4, 0, 4, 0)
        self.vBoxLayout.setSpacing(4)
        self.topLayout.setSpacing(4)
        self.bottomLayout.setSpacing(4)
        self.scrollLayout.setSpacing(4)

        self.vBoxLayout.addLayout(self.topLayout, 0)
        self.vBoxLayout.addWidget(self.scrollArea)
        self.vBoxLayout.addLayout(self.bottomLayout, 0)

        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.topLayout.setAlignment(Qt.AlignTop)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.bottomLayout.setAlignment(Qt.AlignBottom)

    def widget(self, routeKey: str):
        if routeKey not in self.items:
            raise RouteKeyError(f"`{routeKey}` is illegal.")

        return self.items[routeKey]

    def addItem(self, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str, onClick=None,
                selectable=True, selectedIcon=None, position=NavigationItemPosition.TOP):
        """ add navigation item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | FluentIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            where the button is added
        """
        return self.insertItem(-1, routeKey, icon, text, onClick, selectable, selectedIcon, position)

    def addWidget(self, routeKey: str, widget: NavigationWidget, onClick=None, position=NavigationItemPosition.TOP):
        """ add custom widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the button is added
        """
        self.insertWidget(-1, routeKey, widget, onClick, position)

    def insertItem(self, index: int, routeKey: str, icon: Union[str, QIcon, FluentIconBase], text: str, onClick=None,
                   selectable=True, selectedIcon=None, position=NavigationItemPosition.TOP):
        """ insert navigation tree item

        Parameters
        ----------
        index: int
            the insert position of parent widget

        routeKey: str
            the unique name of item

        icon: str | QIcon | FluentIconBase
            the icon of navigation item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        selectable: bool
            whether the item is selectable

        selectedIcon: str | QIcon | FluentIconBase
            the icon of navigation item in selected state

        position: NavigationItemPosition
            where the button is added
        """
        if routeKey in self.items:
            return

        w = NavigationBarPushButton(icon, text, selectable, selectedIcon, self)
        self.insertWidget(index, routeKey, w, onClick, position)
        return w

    def insertWidget(self, index: int, routeKey: str, widget: NavigationWidget, onClick=None,
                     position=NavigationItemPosition.TOP):
        """ insert custom widget

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        widget: NavigationWidget
            the custom widget to be added

        onClick: callable
            the slot connected to item clicked signal

        position: NavigationItemPosition
            where the button is added
        """
        if routeKey in self.items:
            return

        self._registerWidget(routeKey, widget, onClick)
        self._insertWidgetToLayout(index, widget, position)

    def _registerWidget(self, routeKey: str, widget: NavigationWidget, onClick):
        """ register widget """
        widget.clicked.connect(self._onWidgetClicked)

        if onClick is not None:
            widget.clicked.connect(onClick)

        widget.setProperty('routeKey', routeKey)
        self.items[routeKey] = widget

    def _insertWidgetToLayout(self, index: int, widget: NavigationWidget, position: NavigationItemPosition):
        """ insert widget to layout """
        if position == NavigationItemPosition.TOP:
            widget.setParent(self)
            self.topLayout.insertWidget(
                index, widget, 0, Qt.AlignTop | Qt.AlignHCenter)
        elif position == NavigationItemPosition.SCROLL:
            widget.setParent(self.scrollWidget)
            self.scrollLayout.insertWidget(
                index, widget, 0, Qt.AlignTop | Qt.AlignHCenter)
        else:
            widget.setParent(self)
            self.bottomLayout.insertWidget(
                index, widget, 0, Qt.AlignBottom | Qt.AlignHCenter)

        widget.show()

    def removeWidget(self, routeKey: str):
        """ remove widget

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        widget = self.items.pop(routeKey)
        widget.deleteLater()
        self.history.remove(routeKey)

    def setCurrentItem(self, routeKey: str):
        """ set current selected item

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        for k, widget in self.items.items():
            widget.setSelected(k == routeKey)

    def setFont(self, font: QFont):
        """ set the font of navigation item """
        super().setFont(font)

        for widget in self.buttons():
            widget.setFont(font)

    def setSelectedTextVisible(self, isVisible: bool):
        """ set whether the text is visible when button is selected """
        for widget in self.buttons():
            widget.setSelectedTextVisible(isVisible)

    def buttons(self):
        return [i for i in self.items.values() if isinstance(i, NavigationPushButton)]

    def _onWidgetClicked(self):
        widget = self.sender()  # type: NavigationWidget
        if widget.isSelectable:
            self.setCurrentItem(widget.property('routeKey'))

###############################################################################

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
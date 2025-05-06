# coding:utf-8
from typing import Union
from enum import Enum
from PySide6.QtGui import QPainter, QColor, Qt, QIcon, QPen
from PySide6.QtCore import Signal, QRect,  QEvent
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import isDarkTheme, Theme, setTheme, FluentIcon, Icon, FluentIconBase, themeColor, TitleLabel, \
    PushButton, TransparentToolButton
from FluentWidgets import VerticalScrollWidget, VBoxLayout, HBoxLayout, setToolTipInfos, setToolTipInfo


class RouteKeyError(Exception):
    """ Route key error """
    pass


class NavigationItemPosition(Enum):
    TOP = 0
    BOTTOM = 1
    SCROLL = 2


class NavigationWidget(QWidget):
    clicked = Signal()
    EXPAND_WIDTH = 328

    def __init__(self, isSelected=False, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.isEnter = False
        self.isPressed = False
        self.isExpand = False
        self.isSelected = isSelected
        self.setFixedSize(50, 35)
        setTheme(Theme.AUTO)

    def setExpend(self, isExpand: bool):
        self.isExpand = isExpand
        self.update()

    def setSelected(self, selected: bool):
        self.isSelected = selected
        self.update()

    def click(self):
        self.clicked.emit()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.isEnter = True
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.isEnter = False
        self.isPressed = False
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.isEnter = False
        self.isPressed = False
        self.clicked.emit()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        if self.isPressed:
            painter.setOpacity(0.7)
        color = 255 if isDarkTheme() else 0
        if self.isEnter or self.isSelected:
            painter.setBrush(QColor(color, color, color, 10))
        painter.drawRoundedRect(self.rect(), 6, 6)
        if self.isSelected:
            painter.drawRoundedRect(self.rect(), 6, 6)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(themeColor())
            painter.drawRoundedRect(0, 5, 5, self.height() - 10, 3, 3)
        if self.isExpand:
            self.setFixedWidth(self.EXPAND_WIDTH)
        else:
            self.setFixedWidth(45)


class NavigationSeparator(NavigationWidget):
    def __init__(self, parent=None):
        super().__init__(False, parent)
        self.setFixedSize(parent.width() - 20, 1)
        self.parent = parent
        parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.parent and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.setFixedSize(self.parent.width() - 20, 1)
            self.update()
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        painter.setPen(QPen(QColor(color, color, color, 128)))
        painter.drawLine(0, 1, self.width(), 1)


class NavigationButton(NavigationWidget):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], text='', isSelected=False, parent=None):
        super().__init__(isSelected, parent)
        self._icon = Icon(icon)
        self._text = text
        self._iconSize = 16
        self._margin = 45

    def setIconSize(self, size: int):
        self._iconSize = size
        self.update()

    def setText(self, text: str):
        self._text = text
        self.update()

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        self._icon = Icon(icon)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.drawPixmap(15, (self.height() - self._iconSize) // 2, self._icon.pixmap(self._iconSize))

        if self.isExpand:
            painter.setFont(self.font())
            rect = QRect(self._margin, 0, self.width() - 40, self.height())
            painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter, self._text)


class NavigationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._isExpand = False
        self.__items = {}  # type: dict[str, NavigationWidget]
        self.__history = []
        self._expandWidth = 256
        self._collapsedWidth = 65


        self._navLayout = VBoxLayout(self)
        self._returnButton = TransparentToolButton(FluentIcon.RETURN, self)
        self._expandButton = TransparentToolButton(FluentIcon.MENU, self)
        self._returnButton.setFixedSize(45, 35)
        self._expandButton.setFixedSize(45, 35)
        self._scrollWidget = VerticalScrollWidget(self)

        self.__initScrollWidget()
        self.__initLayout()
        self.setMaximumWidth(self._collapsedWidth)
        self.enableReturn(False)
        self.connectSignalSlot()
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

    def connectSignalSlot(self):
        self._returnButton.clicked.connect(lambda: self.setCurrentItem(self.__updateHistory()))
        self._expandButton.clicked.connect(self.expandNav)

    def expandNav(self):
        if self._isExpand:
            self._isExpand = False
            width = self._collapsedWidth
        else:
            self._isExpand = True
            width = self._expandWidth
        self.setFixedWidth(width)
        self.__expandAllButton(self._isExpand)

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
        add Item to Navigation Bar

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
        return self.insertWidget(-1, routeKey, widget, onClick, position)

    def insertWidget(
            self,
            index: int,
            routeKey: str,
            widget: NavigationWidget,
            onClick=None,
            position=NavigationItemPosition.SCROLL
    ):
        w = widget
        w.clicked.connect(lambda: self._onClickWidget(w))
        w.clicked.connect(onClick)
        self.__items[routeKey] = w
        w.setProperty("routeKey", routeKey)
        setToolTipInfo(w, routeKey, 1500)
        return self._insertWidgetToLayout(index, w, position)

    def addSeparator(self, position=NavigationItemPosition.SCROLL):
        self.insertSeparator(-1, position)

    def insertSeparator(self, index: int, position=NavigationItemPosition.SCROLL):
        """ insert separator """
        separator = NavigationSeparator(self)
        self._insertWidgetToLayout(index, separator, position)

    def removeWidget(self, routeKey: str):
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
            w.EXPAND_WIDTH = self.width() - 20
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

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    layout = HBoxLayout(window)
    window.resize(800, 520)

    title = TitleLabel("home", window)
    button1 = PushButton('expand', window)
    button2 = PushButton('collapse', window)

    nav = NavigationBar(window)
    nav.addItem('home', FluentIcon.HOME, 'Home', False,
                lambda: title.setText('home'), NavigationItemPosition.TOP)
    nav.addSeparator(NavigationItemPosition.BOTTOM)
    nav.addItem('setting', FluentIcon.SETTING, 'Setting', False,
                lambda: title.setText('setting'), NavigationItemPosition.BOTTOM)
    nav.addItem('about', FluentIcon.INFO, 'About', False,
                lambda: title.setText('about'), NavigationItemPosition.BOTTOM)

    nav.setCurrentItem('setting')
    # nav.enableReturn(True)

    # add top
    for _ in range(2):
        nav.addItem(str(_), FluentIcon.GITHUB, str(_), onClick=lambda: title.setText(str(_)), position=NavigationItemPosition.TOP)
    nav.addSeparator(NavigationItemPosition.TOP)
    # add scroll
    for _ in range(24):
        nav.addItem(str(_) + '1', FluentIcon.GITHUB, str(_), onClick=lambda: title.setText(str(_) + "1"))

    layout.addWidget(nav)
    layout.addWidget(title)
    layout.addWidget(button1)
    layout.addWidget(button2)

    nav.expandNav()

    window.show()
    app.exec()


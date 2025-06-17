# coding:utf-8
from typing import Union, overload, List, Dict

from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout
from PySide6.QtCore import Qt, QRect, Signal, QPropertyAnimation, QPoint, QTimer, QEvent, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QPen, QIcon

from ...common.color import themeColor, isDarkTheme
from ...common.font import setFont
from ...common.icon import FluentIcon, FluentIconBase, toQIcon
from ...components.navigation.navigation_panel import RouteKeyError
from ...components.widgets.tool_tip import setToolTipInfo, ToolTipPosition
from ..widgets.scroll_widget import SingleDirectionScrollArea


class SlidingWidget(QWidget):

    clicked = Signal(QWidget)

    def __init__(self, text: str, icon: FluentIconBase = None, isSelected=False, parent=None):
        super().__init__(parent)
        setFont(self, 16)
        self.isHover = False
        self.isSelected = isSelected
        self._text = text
        self._icon = None           # type: FluentIcon
        self._itemColor = None      # type: QColor
        self._hoverColor = None     # type: QColor
        self._selectedColor = None  # type: QColor
        self._lastColor = None      # type: QColor
        self._iconSize = 16
        self._fontMetrics = QFontMetrics(self.font())
        self._adjustSize()
        self.setIcon(icon)

    def _adjustSize(self, size=0):
        self.setMinimumSize(self._fontMetrics.horizontalAdvance(self._text) + 32 + size, 35)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.isHover = True
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.isHover = False
        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.clicked.emit(self)

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.update()

    def setText(self, text: str):
        self._text = text
        self._adjustSize()
        self.update()

    def setIcon(self, icon: FluentIcon):
        self._icon = icon or QIcon()
        self._adjustSize(self._iconSize * 2)
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIconSize(self, size: int):
        if self._iconSize == size:
            return
        self._iconSize = size
        self.update()

    def setItemColor(self, color: Union[str, QColor]):
        if self._itemColor == color:
            return
        self._itemColor = color
        self.update()

    def setItemHoverColor(self, color: Union[str, QColor]):
        if self._hoverColor == color:
            return
        self._hoverColor = color
        self.update()

    def setItemSelectedColor(self, color: Union[str, QColor]):
        if self._selectedColor == color:
            return
        self._selectedColor = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing)
        rect = self.rect()
        alignment = Qt.AlignCenter
        if self.isSelected:
            color = self._selectedColor or themeColor()
        elif self.isHover:
            color = self._hoverColor or themeColor()
        else:
            color = self._itemColor or (255 if isDarkTheme() else 0)
        if not self.icon().isNull():
            rect, alignment = self._drawIcon(color, painter, rect)
        self._drawText(color, painter, rect, alignment)

    def _drawIcon(self, color: QColor, painter: QPainter, rect: QRect):
        if isinstance(self._icon, FluentIconBase) and self._lastColor != color:
            self._icon = self._icon.colored(color, color)
            self._lastColor = QColor(color)
        x = (self.width() - self._fontMetrics.horizontalAdvance(self._text) - self._iconSize) / 2
        y = (self.height() - self._iconSize) / 2
        self._icon.render(painter, QRect(x, y, self._iconSize, self._iconSize))
        rect.adjust(x + self._iconSize + 6, 0, 0, 0)
        return rect, Qt.AlignVCenter

    def _drawText(self, color, painter: QPainter, rect: QRect, alignment: Qt.AlignmentFlag):
        painter.setPen(color)
        painter.drawText(rect, alignment, self._text)


class SlidingLine(QFrame):

    def __init__(self, parent=None, color: QColor = None, height=4):
        super().__init__(parent)
        self.setFixedHeight(height)
        self._color = color

    def setLineColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color or themeColor())
        painter.drawRoundedRect(self.rect(), 2, 2)


class SmoothSeparator(QWidget):
    """ Smooth Switch Separator """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(6)
        self._color = None

    def setSeparatorColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        pen = QPen(self._color or QColor(color, color, color, 128), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(2, 10, 2, self.height() - 10)


class SlidingNavigationBar(SingleDirectionScrollArea):

    currentItemChanged = Signal(SlidingWidget)

    def __init__(self, parent: QWidget):
        super().__init__(parent, Qt.Horizontal)
        self.setFixedHeight(60)
        self._items = {} # type: Dict[str, SlidingWidget]
        self._widget = QWidget()
        self._widget.setStyleSheet("background:transparent;")
        self.__currentItem = None # type: SlidingWidget
        self._slidingLine = SlidingLine(self._widget)
        self._slidingLine.raise_()
        self.__slideLineWidth = 30
        self._slidingLine.setFixedSize(self.__slideLineWidth, 3)
        self.__posAni = QPropertyAnimation(self._slidingLine, b"pos")
        self.__posAni.setEasingCurve(QEasingCurve.OutCubic)

        self.__initScrollArea()
        self._widgetLayout = QHBoxLayout(self._widget)
        self.currentItemChanged.connect(lambda w:  w.update())
        parent.installEventFilter(self)

    def __initScrollArea(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.enableTransparentBackground()
        self.setWidgetResizable(True)
        self.setWidget(self._widget)

    def __getSlideEndPos(self, item: SlidingWidget):
        pos = item.pos()
        x = pos.x()
        y = pos.y()
        width = item.width()
        height = item.height()
        return QPoint(x + width / 2 - self.__slideLineWidth / 2, y + height + 5)

    def __createPosAni(self, item: SlidingWidget):
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self._slidingLine.pos())
        self.__posAni.setEndValue(self.__getSlideEndPos(item))
        self.__posAni.start()

    def __make(self, name: str, *args, **kwargs):
        for item in self._items.values():
            method = getattr(item, name, None)
            if callable(method):
                method(*args, **kwargs)

    def __adjustSlideLinePos(self):
        self._slidingLine.move(self.__getSlideEndPos(self.__currentItem))

    def _onClicked(self, item: SlidingWidget):
        self.setCurrentWidget(item)

    def setEasingCurve(self, easing: QEasingCurve.Type):
        self.__posAni.setEasingCurve(easing)

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
        self._slidingLine.setFixedWidth(self.__slideLineWidth)
        self.__adjustSlideLinePos()

    def setSlideLineColor(self, color: Union[str, QColor]):
        self._slidingLine.setLineColor(color)

    def setItemSelectedColor(self, color: Union[str, QColor]):
        self.__make("setItemSelectedColor", color)

    def setItemColor(self, color: Union[str, QColor]):
        self.__make("setItemColor", color)

    def setItemHoverColor(self, color: Union[str, QColor]):
        self.__make("setItemHoverColor", color)

    def setItemSize(self, width: int, height: int):
        self.__make("setFixedSize", width, height)

    @overload
    def setCurrentWidget(self, item: str): ...
    @overload
    def setCurrentWidget(self, item: SlidingWidget): ...

    def setCurrentWidget(self, item: Union[str, SlidingWidget]):
        values = self._items.values()
        if isinstance(item, str):
            if item not in self._items:
                return
            item = self._items[item]
        if item not in values or item is self.__currentItem:
            return
        for obj in values:
            obj.setSelected(False)
        self.currentItemChanged.emit(item)
        self.__currentItem = item
        item.setSelected(True)
        QTimer.singleShot(1, lambda: self.__createPosAni(item))

    def setCurrentIndex(self, index: int):
        if len(self._items.keys()) >= index < 0:
            return
        self.setCurrentWidget(list(self._items.keys())[index])

    def addStretch(self, stretch: int):
        self._widgetLayout.addStretch(stretch)

    def addSpacing(self, size: int):
        self._widgetLayout.addSpacing(size)

    def addItem(
            self,
            routeKey: str,
            text: str,
            icon: FluentIcon = None,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        self.insertItem(-1, routeKey, text, icon, onClick, isSelected, toolTip)

    def insertItem(
            self,
            index: int,
            routeKey: str,
            text: str,
            icon: FluentIcon = None,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        if routeKey in self._items:
            raise RouteKeyError('routeKey Are Not Unique')
        item = SlidingWidget(text, icon, isSelected, self._widget)
        item.setProperty("routeKey", routeKey)
        self._widgetLayout.insertWidget(index, item)
        self._items[routeKey] = item

        item.clicked.connect(self._onClicked)
        if onClick:
            item.clicked.connect(onClick)
        if isSelected:
            self.setCurrentWidget(routeKey)
        if toolTip:
            setToolTipInfo(item, toolTip, 1500, ToolTipPosition.TOP)

    def addWidget(self, widget: QWidget):
        self.insertWidget(-1, widget)

    def insertWidget(self, index: int, widget: QWidget):
        self._widgetLayout.insertWidget(index, widget)

    def removeItem(self, routeKey: str):
        if routeKey not in self._items:
            return
        widget = self._items.pop(routeKey)
        self._widgetLayout.removeWidget(widget)
        widget.clicked.disconnect()
        widget.setParent(None)
        widget.deleteLater()
        if self._items and self.__currentItem is widget:
            item = self._items[next(iter(self._items))]
            self.__currentItem = item
            self._onClicked(item)

    def currentItem(self) -> Union[SlidingWidget, None]:
        return self.__currentItem

    def item(self, routeKey: str) -> SlidingWidget:
        if routeKey not in self._items:
            raise RouteKeyError(f"`{routeKey}` is illegal")
        return self._items[routeKey]

    def allItem(self) -> List[SlidingWidget]:
        return list(self._items.values())

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Resize, QEvent.WindowStateChange] and self.__currentItem:
            self.__adjustSlideLinePos()
        return super().eventFilter(obj, event)


class SlidingToolNavigationBar(SlidingNavigationBar):

    def __init__(self, parent):
        super().__init__(parent)

    def setIconSize(self, size: int):
        for item in self.allItem():
            item.setIconSize(size)

    def addItem(
            self,
            routeKey: str,
            icon: FluentIcon,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        self.insertItem(-1, routeKey, icon, onClick, isSelected, toolTip)

    def insertItem(
            self,
            index: int,
            routeKey: str,
            icon: FluentIcon,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        if routeKey in self._items:
            raise RouteKeyError('routeKey Are Not Unique')
        item = SlidingWidget('', icon, isSelected, self._widget)
        item.setProperty("routeKey", routeKey)
        self._widgetLayout.insertWidget(index, item)
        self._items[routeKey] = item

        item.clicked.connect(self._onClicked)
        if onClick:
            item.clicked.connect(onClick)
        if isSelected:
            self.setCurrentWidget(routeKey)
        if toolTip:
            setToolTipInfo(item, toolTip, 1500, ToolTipPosition.TOP)
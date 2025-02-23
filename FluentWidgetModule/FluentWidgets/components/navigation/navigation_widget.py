# coding:utf-8
from enum import Enum
from typing import Union

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Signal, QEvent, QRect
from PySide6.QtGui import Qt, QIcon, QPainter, QColor, QPen, QFontMetrics
from qfluentwidgets import FluentIconBase, isDarkTheme, themeColor, Icon, drawIcon


class RouteKeyError(Exception):
    """ Route key error """
    pass


class NavigationItemPosition(Enum):
    """ navigation item position """
    TOP = 0
    BOTTOM = 1
    SCROLL = 2


class NavigationWidgetBase(QWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.isSelected = False

    def setSelectedColor(self, color: QColor | str):
        raise NotImplementedError

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected

    def click(self):
        self.clicked.emit()


class ExpandNavigationWidget(NavigationWidgetBase):
    """ navigation widget """
    EXPAND_WIDTH = 328

    def __init__(self, isSelected=False, parent=None):
        super().__init__(parent)
        self.isEnter = False
        self.isPressed = False
        self.isExpand = False
        self.selectedColor = None
        self.isSelected = isSelected
        self.setFixedSize(50, 35)

    def setSelectedColor(self, color):
        """ set current selected widget color """
        self.selectedColor = QColor(color)

    def setExpend(self, isExpand: bool):
        """ set expand widget """
        self.isExpand = isExpand
        self.update()

    def setSelected(self, selected):
        super().setSelected(selected)
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


class SmoothSwitchWidget(NavigationWidgetBase):
    """ Smooth Switch Widget """
    clicked = Signal(QWidget)
    hoverSignal = Signal(QWidget)
    leaveSignal = Signal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isSelected = False
        self._xRadius = 6
        self._yRadius = 6
        self._selectedColor = None
        self._itemColor = [QColor(0, 0, 0), QColor(255, 255, 255)]
        self.__lightBgcColor = QColor("#f3f3f3")
        self.__darkBgcColor = QColor("#202020")

    def setSelectedColor(self, color):
        """ set selected/hover color of current widget """
        self._selectedColor = QColor(color)

    def _setItemColor(self, light=QColor(0, 0, 0), dark=QColor(255, 255, 255)):
        self._itemColor = [QColor(light), QColor(dark)]
        self.update()

    def getItemColor(self):
        return self._itemColor[1] if isDarkTheme() else self._itemColor[0]

    def setText(self, text: str):
        self._text = text
        self.update()

    def setIcon(self, icon):
        self._icon = icon
        self.update()

    def setIconSize(self, size: int):
        self._iconSize = size
        self.update()

    def setSelected(self, isSelected):
        super().setSelected(isSelected)
        self.updateSelectedColor(isSelected)

    def setLightBackgroundColor(self, color: QColor | str):
        self.__lightBgcColor = QColor(color)
        self.update()

    def setDarkBackgroundColor(self, color: QColor | str):
        self.__darkBgcColor = QColor(color)
        self.update()

    def getBackgroundColor(self):
        return self.__darkBgcColor if isDarkTheme() else self.__lightBgcColor

    def setBorderRadius(self, x: int, y: int):
        self._xRadius = x
        self._yRadius = y
        self.update()

    def updateSelectedColor(self, update=False):
        if update:
            c = self._selectedColor or themeColor()
            self._setItemColor(c, c)
        else:
            self._setItemColor()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.isHover = True
        self.hoverSignal.emit(self)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.isHover = False
        self.leaveSignal.emit(self)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.clicked.emit(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        # drawer background color
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(self.rect(), self._xRadius, self._yRadius)


class ExpandNavigationSeparator(ExpandNavigationWidget):
    """ navigation separator """
    def __init__(self, parent=None):
        super().__init__(False, parent)
        self.setFixedSize(parent.width() - 20, 1)
        self.color = None
        self.parent = parent
        parent.installEventFilter(self)

    def setSeparatorColor(self, color: str | QColor):
        self.color = QColor(color)
        self.update()

    def eventFilter(self, obj, event):
        if obj is self.parent and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.setFixedSize(self.parent.width() - 20, 1)
            self.update()
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        painter.setPen(QPen(self.color or QColor(color, color, color, 128)))
        painter.drawLine(0, 1, self.width(), 1)


class SmoothSwitchSeparator(QWidget):
    """ Smooth Switch Separator """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(6)
        self.color = None

    def setSeparatorColor(self, color: str | QColor):
        self.color = QColor(color)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        pen = QPen(self.color or QColor(color, color, color, 128), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(2, 10, 2, self.height() - 10)


class SmoothSwitchLine(QFrame):
    """ Smooth Switch Line """
    def __init__(self, parent=None, color: QColor = None, height=4):
        super().__init__(parent)
        self.setFixedHeight(height)
        self.__color = color or themeColor()

    def setLineColor(self, color: QColor | str):
        self.__color = QColor(color)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.__color)
        painter.drawRoundedRect(self.rect(), 2, 2)


class ExpandNavigationButton(ExpandNavigationWidget):
    """ navigation button widget """
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

    def setTextMargin(self, margin: int):
        self._margin = margin
        self.update()

    def getText(self):
        return self._text

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        if self.isExpand:
            painter.setFont(self.font())
            rect = QRect(self._margin, 0, self.width() - 40, self.height())
            painter.drawText(rect, Qt.AlignVCenter, self._text)
            self.setFixedWidth(self.EXPAND_WIDTH)
        else:
            self.setFixedWidth(45)
        painter.setPen(Qt.NoPen)
        if self.isPressed:
            painter.setOpacity(0.7)
        color = 255 if isDarkTheme() else 0
        if self.isEnter or self.isSelected:
            painter.setBrush(QColor(color, color, color, 10))
        painter.drawRoundedRect(self.rect(), 6, 6)
        if self.isSelected:
            painter.drawRoundedRect(self.rect(), 6, 6)
            painter.setPen(Qt.NoPen)
            painter.setBrush(self.selectedColor or themeColor())
            painter.drawRoundedRect(0, 5, 5, self.height() - 10, 3, 3)
        painter.drawPixmap(15, (self.height() - self._iconSize) // 2, self._icon.pixmap(self._iconSize))


class SmoothSwitchToolButton(SmoothSwitchWidget):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 48)
        self._icon = icon
        self._iconSize = 16

    def updateSelectedColor(self, update=False):
        if update:
            c = self._selectedColor or themeColor()
            self._setItemColor(c, c)
            icon = self._icon.colored(c, c)
        else:
            self._setItemColor()
            icon = self._icon.colored(*self._itemColor)
        self._icon = icon
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        x = (self.width() - self._iconSize) / 2
        y = (self.height() - self._iconSize) / 2
        drawIcon(self._icon, painter, QRect(x, y, self._iconSize, self._iconSize))


class SmoothSwitchPushButton(SmoothSwitchWidget):
    def __init__(self, text: str, icon: Union[str, QIcon, FluentIconBase] = None, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 35)
        self._text = text
        self._icon = icon
        self._iconSize = 16

    def updateSelectedColor(self, update=False):
        if update:
            c = self._selectedColor or themeColor()
            self._setItemColor(c, c)
            c = [c, c]
        else:
            self._setItemColor()
            c = self._itemColor
        if self._icon:
            self._icon = self._icon.colored(*c)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        rect = self.rect()
        align = Qt.AlignCenter
        fm = QFontMetrics(self._text)
        w = self.width()
        textWidth = fm.horizontalAdvance(self._text)
        w = (w - textWidth - self._iconSize) / 2

        # draw icon
        if self._icon:
            drawIcon(
                self._icon, painter,
                QRect(w, (self.height() - self._iconSize) / 2, self._iconSize, self._iconSize)
            )
            rect.adjust(w + self._iconSize + 10, 0, 0, 0)
            align = Qt.AlignVCenter

        # draw text
        painter.setPen(self.getItemColor())
        painter.drawText(rect, align, self._text)
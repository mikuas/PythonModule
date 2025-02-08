# coding:utf-8
from enum import Enum
from typing import Union

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QEvent, QRect
from PySide6.QtGui import Qt, QIcon, QPainter, QColor, QPen
from qfluentwidgets import FluentIconBase, isDarkTheme, themeColor, Icon


class RouteKeyError(Exception):
    """ Route key error """
    pass


class NavigationItemPosition(Enum):
    """ navigation item position """
    TOP = 0
    BOTTOM = 1
    SCROLL = 2


class NavigationWidget(QWidget):
    """ navigation widget """
    clicked = Signal()
    EXPAND_WIDTH = 328

    def __init__(self, isSelected=False, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.isEnter = False
        self.isPressed = False
        self.isExpand = False
        self.isSelected = isSelected
        self.selectedColor = None
        self.setFixedSize(50, 35)

    def setSelectedColor(self, color: QColor | str):
        """ set current selected widget color """
        self.selectedColor = QColor(color)

    def setExpend(self, isExpand: bool):
        """ set expand widget """
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


class NavigationSeparator(NavigationWidget):
    """ navigation separator """
    def __init__(self, parent=None, color: QColor = None):
        super().__init__(False, parent)
        self.setFixedSize(parent.width() - 20, 1)
        self.color = color
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
        painter.setPen(QPen(self.color or QColor(color, color, color, 128)))
        painter.drawLine(0, 1, self.width(), 1)


class NavigationButton(NavigationWidget):
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
            painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter, self._text)
            self.setFixedWidth(self.EXPAND_WIDTH)
        else:
            self.setFixedWidth(45)
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
            painter.setBrush(self.selectedColor or themeColor())
            painter.drawRoundedRect(0, 5, 5, self.height() - 10, 3, 3)
        painter.drawPixmap(15, (self.height() - self._iconSize) // 2, self._icon.pixmap(self._iconSize))



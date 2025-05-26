# coding:utf-8
from typing import Union, List

from PySide6.QtCore import (
    Qt, Signal, QRect, QRectF, QPropertyAnimation, Property,
    QMargins, QEasingCurve, QPoint, QEvent, QTimer
)
from PySide6.QtGui import QColor, QPainter, QPen, QIcon, QCursor, QFont, QPixmap, QImage, QFontMetrics
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame
from collections import deque

from ...common.config import isDarkTheme
from ...common.style_sheet import themeColor
from ...common.icon import drawIcon, toQIcon, FluentIconBase, Icon, FluentIcon
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ..widgets import Widget
from ..widgets.scroll_area import ScrollArea
from ..widgets.label import AvatarWidget
from ..widgets.info_badge import InfoBadgeManager, InfoBadgePosition


class NavigationWidgetBase(Widget):
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


class SmoothWidget(NavigationWidgetBase):
    """ Smooth Switch Widget """
    clicked = Signal(QWidget)
    hoverSignal = Signal(QWidget)
    leaveSignal = Signal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isSelected = False
        self._xRadius = 8
        self._yRadius = 8
        self._selectedColor = None
        self._itemColor = [QColor(0, 0, 0), QColor(255, 255, 255)]

    def _setItemColor(self, light=QColor(0, 0, 0), dark=QColor(255, 255, 255)):
        self._itemColor = [QColor(light), QColor(dark)]
        self.update()

    def setSelectedColor(self, color):
        """ set selected/hover color of current widget """
        self._selectedColor = QColor(color)

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
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())


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


class SmoothSeparator(QWidget):
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
        self.hide()
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


class SmoothSwitchToolButton(SmoothWidget):
    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent)
        self.setMinimumSize(50, 35)
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
        drawIcon(Icon(self._icon), painter, QRect(x, y, self._iconSize, self._iconSize))


class SmoothSwitchPushButton(SmoothWidget):
    def __init__(self, text: str, icon: FluentIcon = None, parent=None):
        super().__init__(parent)
        self._text = text
        self._icon = icon
        self._iconSize = 16
        self.setMinimumSize(
            QFontMetrics(self.font()).horizontalAdvance(self._text) + 32 + self._iconSize,
            35
        )

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
                Icon(self._icon), painter,
                QRect(w, (self.height() - self._iconSize) / 2, self._iconSize, self._iconSize)
            )
            rect.adjust(w + self._iconSize + 10, 0, 0, 0)
            align = Qt.AlignVCenter

        # draw text
        painter.setPen(self.getItemColor())
        painter.drawText(rect, align, self._text)
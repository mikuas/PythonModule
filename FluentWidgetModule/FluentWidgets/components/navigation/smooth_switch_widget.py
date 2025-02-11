from typing import Union

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtGui import QPainter, Qt, QColor, QPen, QIcon
from PySide6.QtCore import Signal, QEvent
from qfluentwidgets import themeColor, Icon, isDarkTheme, FluentIconBase


class SmoothSwitchWidget(QWidget):
    clicked = Signal(QWidget)
    hoverSignal = Signal(QWidget)
    leaveSignal = Signal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(100, 35)
        self.isHover = False
        self.isSelected = False
        self._xRadius = 6
        self._yRadius = 6
        self.__textSelectedColor = None
        self.__lightBgcColor = QColor('#F9F9F9')
        self.__darkBgcColor = QColor('#272A32')
        self.setTextColor()

    def setTextSelectedColor(self, color: QColor | str):
        self.__textSelectedColor = QColor(color)

    def setTextColor(self, light=QColor(0, 0, 0), dark=QColor(255, 255, 255)):
        self.__textColor = [light, dark]
        self.update()

    def getTextColor(self):
        return self.__textColor[1] if isDarkTheme() else self.__textColor[0]

    def setText(self, text: str):
        self._text = text
        self.update()

    def setIcon(self, icon):
        self._icon = icon
        self.update()

    def setIconSize(self, size: int):
        self._iconSize = size
        self.update()

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.updateTextColor(isSelected)

    def click(self):
        self.clicked.emit(self)

    def setLightBackgroundColor(self, color: QColor | str):
        self.__lightBgcColor = QColor(color)
        self.update()

    def setDarkBackgroundColor(self, color: QColor | str):
        self.__darkBgcColor = QColor(color)
        self.update()

    def getBackgroundColor(self):
        return self.__darkBgcColor if isDarkTheme() else self.__lightBgcColor

    def setRadius(self, x: int, y: int):
        self._xRadius = x
        self._yRadius = y
        self.update()

    def updateTextColor(self, update=False):
        if update:
            c = self.__textSelectedColor or themeColor()
            self.setTextColor(c, c)
        else:
            self.setTextColor()

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


class SmoothSwitchToolButton(SmoothSwitchWidget):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent)
        self._icon = Icon(icon)
        self._iconSize = 16

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap((self.width() - self._iconSize) // 2, (self.height() - self._iconSize) // 2, self._icon.pixmap(self._iconSize))


class SmoothSwitchPushButton(SmoothSwitchWidget):
    def __init__(self, text: str, icon: Union[str, QIcon, FluentIconBase] = None, parent=None):
        super().__init__(parent)
        self._text = text
        self._icon = Icon(icon) if icon else None
        self._iconSize = 16

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(self.getTextColor())
        rect = self.rect()
        if self._icon:
            painter.drawPixmap(self._iconSize, (self.height() - self._iconSize) // 2, self._icon.pixmap(self._iconSize))
            rect.adjust(self._iconSize + 5, 0, 0, 0)
        painter.drawText(rect, Qt.AlignCenter, self._text)


class SmoothSwitchSeparator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(5)
        self.parent = parent

    def eventFilter(self, obj, event):
        if obj is self.parent and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.setFixedSize(2, self.parent.height() - 20)
            self.update()
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        painter.setPen(QPen(QColor(color, color, color, 128)))
        painter.drawLine(1, 0, 1, self.height())


class SmoothSwitchLine(QFrame):
    def __init__(self, parent=None, color: QColor | str = None, height=4):
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
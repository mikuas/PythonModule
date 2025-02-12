from typing import Dict, Union

from FluentWidgets import HBoxLayout, Widget
from PySide6.QtGui import QPainter, Qt, QColor, QPen, QIcon, QFontMetrics
from PySide6.QtCore import QPropertyAnimation, Signal, QPoint, QTimer, QEvent, QRect
from PySide6.QtWidgets import QWidget, QFrame
from qfluentwidgets import themeColor, isDarkTheme, FluentIconBase, drawIcon


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
        self._selectedColor = None
        self._itemColor = [QColor(0, 0, 0), QColor(255, 255, 255)]
        self.__lightBgcColor = QColor('#F9F9F9')
        self.__darkBgcColor = QColor('#272A32')

    def setSelectedColor(self, color: QColor | str):
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

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.updateSelectedColor(isSelected)

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


class SmoothSwitchToolButton(SmoothSwitchWidget):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent)
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


class SmoothSwitchToolButtonBar(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__items = {} # type: Dict[str, SmoothSwitchWidget]
        self._widgetLayout = HBoxLayout(self)
        self.__currentWidget = None
        self._smoothSwitchLine = SmoothSwitchLine(self)
        self.__posAni = QPropertyAnimation(self._smoothSwitchLine, b'pos')

        self._widgetLayout.setAlignment(Qt.AlignTop)
        parent.installEventFilter(self)

    def addSeparator(self):
        return self.insertSeparator(-1)

    def insertSeparator(self, index: int):
        separator = SmoothSwitchSeparator(self)
        self._widgetLayout.insertWidget(index, separator)
        return separator

    def setItemBackgroundColor(self, light: QColor | str, dark: QColor | str):
        for item in self.__items.values():
            item.setLightBackgroundColor(light)
            item.setDarkBackgroundColor(dark)

    def setItemSelectedColor(self, color: QColor | str):
        for item in self.__items.values():
            item.setSelectedColor(color)

    def setItemSize(self, width: int, height: int):
        for item in self.__items.values():
            item.setFixedSize(width, height)

    def setCurrentWidget(self, routeKey: str):
        if routeKey not in self.__items.keys():
            raise KeyError(f'{routeKey} is not in items')
        QTimer.singleShot(1, lambda: self._onClicked(self.__items[routeKey]))

    def addItem(
            self,
            routeKey: str,
            icon: Union[str, QIcon, FluentIconBase] = None,
            onClick=None,
            isSelected=False
    ):
        if routeKey in self.getAllWidget().keys():
            raise KeyError(f'{routeKey} is already in items')
        item = SmoothSwitchToolButton(icon, self)
        self._append(routeKey, item)
        self._widgetLayout.addWidget(item)

        item.clicked.connect(lambda w: self._onClicked(w))
        item.clicked.connect(onClick)
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        if isSelected:
            self.setCurrentWidget(routeKey)

    def _setTextColor(self, item: SmoothSwitchWidget):
        if item.isSelected:
            return
        item.updateSelectedColor(item.isHover)

    def _append(self, routeKey: str, item: SmoothSwitchWidget):
        self.__items[routeKey] = item

    def __getPos(self, item: SmoothSwitchWidget):
        pos = item.pos()
        x = pos.x()
        y = pos.y()
        width = item.width()
        height = item.height()
        return QPoint(x + width / 2 - self._smoothSwitchLine.width() / 2, y + height + 5)

    def _onClicked(self, item: SmoothSwitchWidget):
        for _ in self.__items.values():
            _.setSelected(False)
        self.__currentWidget = item
        item.setSelected(True)
        self._smoothSwitchLine.setFixedWidth(item.width()/2)
        self.__createPosAni(item)

    def __createPosAni(self, item: SmoothSwitchWidget):
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self._smoothSwitchLine.pos())
        self.__posAni.setEndValue(self.__getPos(item))
        self.__posAni.start()

    def eventFilter(self, watched, event):
        if watched is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            if self.__currentWidget:
                self._smoothSwitchLine.move(self.__getPos(self.__currentWidget))
                self._smoothSwitchLine.setFixedWidth(self.__currentWidget.width() / 2)
        return super().eventFilter(watched, event)

    def getWidget(self, routeKey: str):
        return self.__items[routeKey]

    def getAllWidget(self):
        return self.__items


class SmoothSwitchPushButtonBar(SmoothSwitchToolButtonBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def addItem(
            self,
            routeKey: str,
            text: str,
            icon: Union[str, QIcon, FluentIconBase] = None,
            onClick=None,
            isSelected=False
    ):
        if routeKey in self.getAllWidget().keys():
            raise KeyError(f'{routeKey} is already in items')
        item = SmoothSwitchPushButton(text, icon, self)
        self._append(routeKey, item)
        self._widgetLayout.addWidget(item)

        item.clicked.connect(lambda w: self._onClicked(w))
        item.clicked.connect(onClick)
        item.hoverSignal.connect(lambda w: self._setTextColor(w))
        item.leaveSignal.connect(lambda w: self._setTextColor(w))
        if isSelected:
            self.setCurrentWidget(routeKey)
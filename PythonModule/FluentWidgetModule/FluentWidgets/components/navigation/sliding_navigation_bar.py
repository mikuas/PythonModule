# coding:utf-8
from typing import Union

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QFontMetrics

# from ...common.color import themeColor, isDarkTheme
# from ...common.icon import FluentIcon, drawIcon, Icon
from FluentWidgets import themeColor, isDarkTheme, FluentIcon, drawIcon, Icon, setFont


class SlidingWidget(QWidget):
    def __init__(self, text: str, icon: FluentIcon = None, isSelected=False):
        super().__init__()
        self.isHover = False
        self.isSelected = isSelected
        self.__text = text
        self.__icon = icon
        self.__textColor = None
        self.__hoverColor = None
        self.__selectedColor = None
        self.__iconSize = 16
        self.__fontMetrics = QFontMetrics(self.font())
        setFont(self, 16)
        self._adjustSize()

    def _adjustSize(self, size=0):
        self.setMinimumSize(self.__fontMetrics.horizontalAdvance(self.__text) + 32 + size, 35)

    def enterEvent(self, event):
        self.isHover = True
        self.__updateIconColor()
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.__updateIconColor()
        self.update()
        super().leaveEvent(event)

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.update()

    def setText(self, text: str):
        self.__text = text
        self._adjustSize()
        self.update()

    def setIcon(self, icon: FluentIcon):
        self.__icon = icon
        self._adjustSize(self.__iconSize)
        self.update()

    def setTextColor(self, color: Union[str, QColor]):
        if self.__textColor == color:
            return
        self.__textColor = color
        self.update()

    def setHoverTextColor(self, color: Union[str, QColor]):
        if self.__hoverColor == color:
            return
        self.__hoverColor = color
        self.update()

    def setSelectedTextColor(self, color: Union[str, QColor]):
        if self.__selectedColor == color:
            return
        self.__selectedColor = color
        self.update()

    def __updateIconColor(self):
        tc = themeColor()
        if self.isSelected:
            c = self.__selectedColor or tc
            self.__icon = self.__icon.colored(c, c)
            return
        elif self.isHover:
            c = self.__hoverColor or tc
            self.__icon = self.__icon.colored(c, c)
            return
        c = 255 if isDarkTheme() else 0
        c = QColor(c, c, c)
        self.__icon = self.__icon.colored(c, c)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        rect = self.rect()
        align = Qt.AlignCenter
        if self.__icon:
            x = (self.width() - self.__fontMetrics.horizontalAdvance(self.__text) - self.__iconSize) / 2
            y = (self.height() - self.__iconSize) / 2
            drawIcon(Icon(self.__icon), painter, QRect(x, y, self.__iconSize, self.__iconSize))
            rect.adjust(x + self.__iconSize + 10, 0, 0, 0)
            align = Qt.AlignVCenter
        self._drawText(painter, rect, align)

    def _drawText(self, painter: QPainter, rect: QRect, align: Qt.AlignmentFlag):
        c = 255 if isDarkTheme() else 0
        if self.isSelected:
            painter.setPen(self.__selectedColor or themeColor())
        elif self.isHover:
            painter.setPen(self.__hoverColor or themeColor())
        else:
            painter.setPen(self.__textColor or QColor(c, c, c))
        painter.drawText(rect, align, self.__text)


class SlidingLine(QFrame):

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
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.__color)
        painter.drawRoundedRect(self.rect(), 2, 2)


if __name__ == '__main__':
    class Demo(QWidget):
        def __init__(self):
            super().__init__()
            from FluentWidgets import HBoxLayout
            self.box = HBoxLayout(self)
            self.w = SlidingWidget('hello world', icon=FluentIcon.HOME)
            self.box.addWidget(self.w, 1, Qt.AlignmentFlag.AlignTop)

    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

# class SlidingNavigationBar(SingleDirectionScrollArea):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._items = {} # type: Dict[str, None]
#         self._boxLayout = QHBoxLayout(self)
#         self.__widget = QWidget()
#         self.__currentWidget = None
#         self.__slideLineWidth = 30
#         self.__initScrollWidget()
#
#         self.__slidingLine = SlidingLine(self.__widget)
#         self.__slidingLine.setFixedSize(self.__slideLineWidth, 3)
#         self.__posAni = QPropertyAnimation(self.__slidingLine, b'pos')
#
#         parent.installEventFilter(self)
#
#     def __initScrollWidget(self):
#         self.enableTransparentBackground()
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.setWidgetResizable(True)
#         self.setWidget(self.__widget)
#
#     def __getSlideEndPos(self, item):
#         pos = item.pos()
#         x = pos.x()
#         y = pos.y()
#         width = item.width()
#         height = item.height()
#         return QPoint(x + width / 2 - self.__slideLineWidth / 2, y + height + 5)
#
#     def __createPosAni(self, item):
#         self.__posAni.setDuration(200)
#         self.__posAni.setStartValue(self.__slidingLine.pos())
#         self.__posAni.setEndValue(self.__getSlideEndPos(item))
#         self.__posAni.start()
#
#     def __adjustSlideLinePos(self):
#         QTimer.singleShot(1, lambda: (self.__slidingLine.move(self.__getSlideEndPos(self.__currentWidget))))
#
#     @staticmethod
#     def _setTextColor(item):
#         if item.isSelected:
#             return
#         item.updateSelectedColor(item.isHover)
#
#     def _onClicked(self, item: SmoothWidget):
#         self.setCurrentWidget(item.property('routeKey'))
#
#     def setBarAlignment(self, alignment: Qt.AlignmentFlag):
#         self._widgetLayout.setAlignment(alignment)
#
#     def addSeparator(self):
#         return self.insertSeparator(-1)
#
#     def insertSeparator(self, index: int):
#         separator = SmoothSeparator(self)
#         self._widgetLayout.insertWidget(index, separator)
#         return separator
#
#     def setSlideLineWidth(self, width: int):
#         self.__slideLineWidth = width
#         self.__slideLine.setFixedWidth(self.__slideLineWidth)
#         self.__adjustSlideLinePos()
#
#     def setSlideLineColor(self, color: str | QColor):
#         self.__slideLine.setLineColor(color)
#
#     def setItemBackgroundColor(self, light: QColor | str, dark: QColor | str):
#         for item in self._items.values():
#             item.setLightBackgroundColor(light)
#             item.setDarkBackgroundColor(dark)
#
#     def setItemSelectedColor(self, color: QColor | str):
#         for item in self._items.values():
#             item.setSelectedColor(color)
#
#     def setItemSize(self, width: int, height: int):
#         for item in self._items.values():
#             item.setFixedSize(width, height)
#
#     def setIconSize(self, size: int):
#         for item in self._items.values():
#             item.setIconSize(size)
#
#     def setCurrentWidget(self, routeKey: str):
#         if routeKey not in self._items.keys():
#             return
#         if self.__slideLine.isHidden(): self.__slideLine.show()
#         for w in self._items.values():
#             w.setSelected(False)
#         item = self.getWidget(routeKey)
#         self.__currentWidget = item
#         item.setSelected(True)
#         QTimer.singleShot(1, lambda: self.__createPosAni(item))
#
#     def addItem(self, routeKey, icon, onClick=None, isSelected=False):
#         item = SmoothSwitchToolButton(icon, self)
#         item.setProperty('routeKey', routeKey)
#         self._append(routeKey, item)
#         setToolTipInfo(item, routeKey, 1500, ToolTipPosition.TOP)
#         self._widgetLayout.addWidget(item)
#
#         item.clicked.connect(lambda w: self._onClicked(w))
#         item.clicked.connect(onClick)
#         item.hoverSignal.connect(lambda w: self._setTextColor(w))
#         item.leaveSignal.connect(lambda w: self._setTextColor(w))
#         if isSelected:
#             self.setCurrentWidget(routeKey)
#
#     def getCurrentWidget(self):
#         return self.__currentWidget
#
#     def getWidget(self, routeKey: str) -> SmoothWidget:
#         return super().getWidget(routeKey)
#
#     def getAllWidget(self) -> Dict[str, SmoothWidget]:
#         return super().getAllWidget()
#
#     def eventFilter(self, obj, event):
#         if event.type() in [QEvent.Resize, QEvent.WindowStateChange] and self.getCurrentWidget():
#             self.__adjustSlideLinePos()
#         return super().eventFilter(obj, event)
#
#
# class SlidingToolNavigationBar(SlidingNavigationBar):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#     def addItem(self, routeKey, text: str, icon=None, onClick=None, isSelected=False):
#         item = SmoothSwitchPushButton(text, icon, self)
#         item.setProperty('routeKey', routeKey)
#         self._append(routeKey, item)
#         self._widgetLayout.addWidget(item)
#
#         item.clicked.connect(lambda w: self._onClicked(w))
#         item.clicked.connect(onClick)
#         item.hoverSignal.connect(lambda w: self._setTextColor(w))
#         item.leaveSignal.connect(lambda w: self._setTextColor(w))
#         if isSelected:
#             self.setCurrentWidget(routeKey)
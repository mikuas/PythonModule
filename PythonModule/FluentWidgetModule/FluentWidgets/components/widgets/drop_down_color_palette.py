# coding:utf-8
import random
from typing import Union

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QButtonGroup
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QSize, Signal, QPoint, QRectF

from .separator import HorizontalSeparator
from ...common.icon import FluentIcon
from ...common.font import getFont
from .button import TransparentToolButton, TransparentPushButton
from .menu import RoundMenu, MenuAnimationType
from .label import BodyLabel


def getRandomColor(isRgb=False):
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    color = '#'
    if isRgb:
        return f"rgb({random.randint(1, 255)},{random.randint(1, 255)},{random.randint(1, 255)})"
    else:
        for i in range(6):
            color += str(random.choice(data))
        return color


class StandardItem(QPushButton):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(parent)
        self.setColor(color)

    def setColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def color(self):
        return self._color

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color())
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class DefaultColorPaletteItem(StandardItem):

    def __init__(self, color: Union[str, QColor], text: str, parent: QWidget = None):
        super().__init__(color, parent)
        self.isHover = False
        self._text = text
        self.setFixedHeight(35)

    def setText(self, text: str):
        self._text = text
        self.update()

    def text(self):
        return self._text

    def enterEvent(self, event):
        self.isHover = True
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        rect = QRectF(6.36, 6.36, 24, 24)
        painter.drawRoundedRect(rect, 6, 6)

        rect = self.rect()
        if self.isHover:
            painter.setBrush(QColor(0, 0, 0, 32))
            painter.drawRoundedRect(rect, 6, 6)

        if self.text():
            painter.setFont(getFont())
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(rect.adjusted(40, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, self.text())


class ColorPaletteItem(DefaultColorPaletteItem):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(color, "", parent)
        self.setCheckable(True)
        self.isChecked = False
        self.setFixedSize(28, 28)

    def setChecked(self, isChecked: bool):
        self.isChecked = isChecked
        self.update()

    def enterEvent(self, event):
        if self.isChecked:
            return
        self.isHover = True
        self.update()

    def leaveEvent(self, event):
        if self.isChecked:
            return
        self.isHover = False
        self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked)
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect())
        if self.isChecked:
            self._drawBorder(painter, rect)
            rect.adjust(3.1, 3.1, -3.1, -3.1)
            self._drawBackground(painter, rect)
            return
        elif self.isHover:
            self._drawBorder(painter, rect)
            self._drawBackground(painter, rect.adjusted(1.8, 1.8, -1.8, -1.8))
        else:
            self._drawBackground(painter, rect)

    def _drawBorder(self, painter: QPainter, rect: QRectF):
        painter.setPen(QColor(0, 0, 0))
        painter.drawRoundedRect(rect.adjusted(1.1, 1.1, -1.1, -1.1), 6, 6)

    def _drawBackground(self, painter: QPainter, rect: QRectF):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color())
        painter.drawRoundedRect(rect, 4, 4)


class ColorPalette(RoundMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colorButtonGroup = QButtonGroup(self)
        self.colorButtonGroup.setExclusive(True)
        self._lastButton = None # type: ColorPaletteItem
        self.__initPaletteWidget()
        self.__initDefaultColor()
        self.__initThemeColor()
        self.__initStandardColor()

        self.moreColorButton = TransparentPushButton(FluentIcon.PALETTE, "更多颜色")
        self.moreColorButton.setFixedWidth(320)
        self._widgetLayout.addWidget(self.moreColorButton)

    def __initPaletteWidget(self):
        self.view.setFixedSize(350, 390)
        self.setFixedSize(350, 390)
        self.setItemHeight(390)
        self.view.setStyleSheet("padding: 0px 0px 0px 0px; border-radius: 6px;")
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._widget = QWidget()
        self._widget.setFixedSize(350, 390)
        self.addWidget(self._widget, False)

        self._widgetLayout = QVBoxLayout(self._widget)
        self._widgetLayout.setAlignment(Qt.AlignTop)
        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.setSpacing(4)

    def __initDefaultColor(self):
        self.defaultColorItem = DefaultColorPaletteItem("black", "默认颜色", self)
        self.defaultColorItem.setFixedWidth(320)
        self._widgetLayout.addWidget(self.defaultColorItem)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initThemeColor(self):
        self.themeColorLabel = BodyLabel("主题色", self._widget)
        self._widgetLayout.addWidget(self.themeColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(4)
        colors = [QColor(255, 255, 255), "black", "gray", "orange", "pink", "deeppink", "skyblue", "blue", "deepskyblue", "aqua"]
        for i in range(10):
            vBoxLayout = QVBoxLayout()
            vBoxLayout.setSpacing(4)
            item = ColorPaletteItem(colors[i], self)
            vBoxLayout.addWidget(item)
            self.colorButtonGroup.addButton(item)
            vBoxLayout.addSpacing(10)
            for j in range(5):
                color = QColor(colors[i])
                color.setAlpha(255 / (5 - j))
                item = ColorPaletteItem(color, self)
                vBoxLayout.addWidget(item)
                self.colorButtonGroup.addButton(item)
            hBoxLayout.addLayout(vBoxLayout)
        self._widgetLayout.addLayout(hBoxLayout)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initStandardColor(self):
        self.standardColorLabel = BodyLabel("标准颜色", self)
        self._widgetLayout.addWidget(self.standardColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        box = QHBoxLayout()
        for i in range(10):
            item = ColorPaletteItem(getRandomColor(), self)
            box.addWidget(item)
            self.colorButtonGroup.addButton(item)
        self._widgetLayout.addLayout(box)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __createHorizontalSeparator(self):
        separator = HorizontalSeparator(self)
        separator.setSeparatorColor(QColor(0, 0, 0, 32))
        separator.setFixedWidth(320)
        return separator

    def updateItem(self, button: ColorPaletteItem):
        if self._lastButton and button != self._lastButton:
            self._lastButton.isHover = False
            self._lastButton.setChecked(False)
            self._lastButton.update()
        self._lastButton = button
        return button

    def setDefaultColor(self, color: Union[str, QColor]):
        self.defaultColorItem.setColor(color)

    def defaultColor(self):
        return self.defaultColorItem.color()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)
        self.adjustSize()


class DropDownColorPalette(QWidget):

    colorChange = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(62, 40)
        self.widgetLayout = QHBoxLayout(self)
        self.widgetLayout.setContentsMargins(5, 3, 5, 3)

        self.colorPalette = ColorPalette(self)
        self.item = StandardItem(self.colorPalette.defaultColor(), self)
        self.item.setFixedSize(28, 28)
        self.dropDownButton = TransparentToolButton(FluentIcon.CHEVRON_DOWN_MED, self)

        self.dropDownButton.setIconSize(QSize(12, 12))

        self.widgetLayout.addWidget(self.item)
        self.widgetLayout.addWidget(self.dropDownButton)
        self.__initSignalSlot()

    def setDefaultColor(self, color: Union[str, QColor]):
        self.item.setColor(color)
        self.colorPalette.setDefaultColor(color)

    def point(self):
        return self.mapToGlobal(QPoint(-(self.colorPalette.width() / 2) + (self.width() / 1.5) , self.height()))

    def _updateSelectedColor(self):
        color = self.colorPalette.defaultColor()
        self.colorChange.emit(color)
        self.item.setColor(color)
        button = self.colorPalette.colorButtonGroup.checkedButton()
        if button:
            button.isHover = False
            button.setChecked(False)

    def __initSignalSlot(self):
        self.colorPalette.defaultColorItem.clicked.connect(self._updateSelectedColor)
        self.colorPalette.colorButtonGroup.buttonClicked.connect(self.__onClickItem)
        self.dropDownButton.clicked.connect(lambda: self.colorPalette.exec(self.point()))
        self.colorChange.connect(self.item.setColor)

    def __onClickItem(self, item):
        item = self.colorPalette.updateItem(item)
        self.colorChange.emit(item.color() if item.isChecked else self.colorPalette.defaultColor())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.colorPalette.exec(self.point())
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)
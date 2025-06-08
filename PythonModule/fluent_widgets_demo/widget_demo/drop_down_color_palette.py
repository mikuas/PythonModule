# coding:utf-8
import sys
import random
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, \
    QFrame, QWidgetAction, QButtonGroup
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, Signal, QPoint, QRectF

from FluentWidgets import HorizontalSeparator, SplitWidget, TransparentToolButton, FluentIcon, RoundMenu, \
    MenuAnimationType, TitleLabel, MultiSelectionComboBox, BodyLabel, TransparentPushButton, getFont, ColorDialog


def getRandomColor(isRgb=False):
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    color = '#'
    if isRgb:
        return f"rgb({random.randint(1, 255)},{random.randint(1, 255)},{random.srandint(1, 255)})"
    else:
        for i in range(6):
            color += str(random.choice(data))
        return color


class DefaultColorPaletteItem(QPushButton):

    def __init__(self, color: Union[str, QColor], text: str, parent: QWidget = None):
        super().__init__(parent)
        self.isHover = False
        self._text = text
        self.setColor(color)
        self.setFixedHeight(35)

    def setColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def color(self):
        return self._color

    def setText(self, text: str):
        self._text = text
        self.update()

    def text(self):
        return self._text

    def enterEvent(self, event):
        self.isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        super().leaveEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        rect = QRectF(6.36, 6.36, 24, 24)
        painter.drawRoundedRect(rect, 6, 6)

        painter.setBrush(QColor(0, 0, 0, 32 if self.isHover else 0))
        rect = self.rect()
        painter.drawRoundedRect(rect, 6, 6)

        if self.text():
            painter.setFont(getFont())
            painter.setPen(QColor('black'))
            painter.drawText(rect.adjusted(40, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, self.text())


class ColorPaletteItem(DefaultColorPaletteItem):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(color, "", parent)
        self.isChecked = False
        self.setCheckable(True)
        self.setFixedSize(28, 28)

    def setChecked(self, isChecked: bool):
        self.isChecked = isChecked
        self.update()
        super().setChecked(isChecked)

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

    selectedChange = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._colorButtonGroup = QButtonGroup(self)
        self._colorButtonGroup.setExclusive(True)
        self._lastButton = None # type: ColorPaletteItem
        self.__initPaletteWidget()
        self.__initDefaultColor()
        self.__initThemeColor()
        self.__initStandardColor()
        self.addWidget(self._widget, False)

        self.moreColorButton = TransparentPushButton(FluentIcon.PALETTE, "更多颜色")
        self.moreColorButton.setFixedWidth(320)
        self._widgetLayout.addWidget(self.moreColorButton)

        self._colorButtonGroup.buttonClicked.connect(self.__updateButton)

    def __initPaletteWidget(self):
        self.view.setFixedSize(350, 375)
        self.setFixedSize(350, 375)
        self.setItemHeight(375)
        self.view.setStyleSheet("padding: 0px 0px 0px 0px; border-radius: 6px;")
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._widget = QWidget()
        self._widget.setFixedSize(350, 375)
        self._widgetLayout = QVBoxLayout(self._widget)
        self._widgetLayout.setAlignment(Qt.AlignTop)
        self._widgetLayout.setContentsMargins(0, 0, 0, 0)

    def __initDefaultColor(self):
        self.defaultDropDownColorItem = DefaultColorPaletteItem("black", "默认颜色", self)
        self.defaultDropDownColorItem.setFixedWidth(320)
        self._widgetLayout.addWidget(self.defaultDropDownColorItem)
        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initThemeColor(self):
        self._widgetLayout.addWidget(BodyLabel("主题色", self._widget), 0, Qt.AlignLeft | Qt.AlignVCenter)

        for i in range(6):
            box = QHBoxLayout()
            box.setSpacing(4)
            box.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            for j in range(10):
                item = ColorPaletteItem(getRandomColor(), self)
                box.addWidget(item)
                self._colorButtonGroup.addButton(item)
            self._widgetLayout.setSpacing(4)
            self._widgetLayout.addLayout(box)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initStandardColor(self):
        self._widgetLayout.addWidget(BodyLabel("标准颜色", self), 0, Qt.AlignLeft | Qt.AlignVCenter)
        box = QHBoxLayout()
        for i in range(10):
            item = ColorPaletteItem(getRandomColor(), self)
            box.addWidget(item)
            self._colorButtonGroup.addButton(item)
        self._widgetLayout.addLayout(box)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __createHorizontalSeparator(self):
        horizontalSeparator = HorizontalSeparator(self)
        horizontalSeparator.setSeparatorColor(QColor(0, 0, 0, 32))
        horizontalSeparator.setFixedWidth(320)
        return horizontalSeparator

    def __updateButton(self, button: ColorPaletteItem):
        if self._lastButton and button != self._lastButton:
            print(True)
            self._lastButton.isHover = False
            self._lastButton.setChecked(False)
            self._lastButton.update()
        self._lastButton = button
        self.selectedChange.emit(button.color())

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)
        self.adjustSize()


class DropDownColorPalette(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(62, 40)
        self.widgetLayout = QHBoxLayout(self)
        self.widgetLayout.setContentsMargins(5, 3, 2, 3)

        self.item = ColorPaletteItem("black", self)
        self.item.setCheckable(False)
        self.dropButton = TransparentToolButton(FluentIcon.CHEVRON_DOWN_MED, self)
        self.dropButton.setIconSize(QSize(12, 12))

        self.colorPalette = ColorPalette(self)
        self.colorPalette.selectedChange.connect(self.item.setColor)

        self.widgetLayout.addWidget(self.item)
        self.widgetLayout.addWidget(self.dropButton)

        self.dropButton.clicked.connect(lambda: self.colorPalette.exec(self.point()))

    def point(self):
        return self.mapToGlobal(QPoint(-(self.colorPalette.width() / 2) + (self.width() / 1.5) , self.height()))

    def mouseReleaseEvent(self, event):
        self.colorPalette.exec(self.point())
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)

        self.ddcp = DropDownColorPalette(self)

        self.box.addWidget(self.ddcp, 0, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

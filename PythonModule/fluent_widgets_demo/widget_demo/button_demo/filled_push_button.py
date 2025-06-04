# coding:utf-8
import sys
from typing import Union

from FluentWidgets.common.overload import singledispatchmethod
from FluentWidgets.common.icon import toQIcon
from FluentWidgets import setFont, VerticalScrollWidget, FluentIconBase, drawIcon, isDarkTheme, themeColor

from PySide6.QtWidgets import QApplication, QWidget, QAbstractButton, QPushButton
from PySide6.QtGui import QColor, QPainter, QFontMetrics, QIcon, QPen
from PySide6.QtCore import Qt, QSize, QRect


class RoundPushButton(QAbstractButton):
    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__isHover = False
        self.__isPressed = False
        setFont(self)
        self.setAttribute(Qt.WA_StaticContents)
        self.setFixedHeight(35)
        self.setIcon(None)
        self.setIconSize(QSize(16, 16))
        self._fontMetrics = QFontMetrics(self.font())

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, parent: QWidget = None, text: str = ''):
        self.__init__(text, parent, icon)

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.setProperty('hasIcon', icon is not None)
        self._icon = icon or QIcon()
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.__isHover = True
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.__isHover = False
        self.update()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.__isPressed = True

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.__isPressed = False

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing)
        c = 255 if isDarkTheme() else 0
        color = QColor(c, c, c, 32)
        align = Qt.AlignCenter
        pen = QPen(color)
        pen.setWidthF(1.5)
        painter.setPen(pen)
        painter.setOpacity(0.768 if self.__isHover else 1.0)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 16, 16)
        if not self.icon().isNull():
            size = self.iconSize().width()
            x = (self.width() - self._fontMetrics.horizontalAdvance(self.text()) - size) / 2
            y = (self.height() - size) / 2
            drawIcon(self._icon, painter, QRect(x, y, size, size))
            rect.adjust(x + size + 6, 0, 0, 0)
            align = Qt.AlignVCenter
        # draw text
        self._drawText(painter, color, rect, align)

    def _drawText(self, painter: QPainter, color: QColor, rect: QRect, alignment):
        color.setAlpha(255)
        painter.setPen(color)
        painter.drawText(rect, alignment, self.text())


class Demo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.button = RoundPushButton(self)
        self.button.setFixedHeight(35)
        self.button.setText("Hello World!")
        self.addWidget(self.button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

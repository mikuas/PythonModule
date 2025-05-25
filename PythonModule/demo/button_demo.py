# coding:utf-8
import random
from typing import Union

from FluentWidgets.common.icon import toQIcon
from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QIcon, QPainter, QColor, QPen, Qt, QFontMetrics
from PySide6.QtWidgets import QPushButton, QToolButton, QWidget, QAbstractButton

from FluentWidgets.common.overload import singledispatchmethod
from FluentWidgets import setFont, FluentIconBase, themeColor, isDarkTheme, qconfig, FluentIcon, setThemeColor


class OutlinePushButton(QAbstractButton):
    """ Outline PushButton

    Constructors
    ------------
    * OutlinePushButton(`parent`: QWidget = None)
    * OutlinePushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * OutlinePushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    checkedChange = Signal(bool)

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__isHover = False
        self.__isPressed = False
        self.__outlineColor = None # type: QColor
        self.setFixedHeight(35)
        self.setIconSize(QSize(16, 16))
        self.setCheckable(True)
        self.toggled.connect(lambda b: self.setChecked(b))
        setFont(self)

        qconfig.themeColorChanged.connect(self.update)

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def setOutlineColor(self, color: str | QColor):
        if isinstance(color, str):
            color = QColor(color)
        self.__outlineColor = color

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

    def setChecked(self, isChecked: bool):
        super().setChecked(isChecked)
        self.checkedChange.emit(isChecked)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        c = 255 if isDarkTheme() else 0
        bc = self.__outlineColor or themeColor() if self.isChecked() else QColor(c, c, c, 24)
        if not self.icon().isNull():
            iconSize = self.iconSize()
            metrics = QFontMetrics(self.font())
            w = metrics.horizontalAdvance(self.text())

            x = (rect.width() - iconSize.width()) // 2 - w
            y = (rect.height() - iconSize.height()) // 2
            painter.drawPixmap(x, y, self.icon().pixmap(iconSize))

            rect.adjusted(iconSize.width(), 0, 0, 0)

        pen = QPen(bc)
        pen.setWidthF(1.5)
        painter.setPen(pen)
        painter.setOpacity(0.768 if self.__isHover else 1.0)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 16, 16)

        bc.setAlpha(255)
        painter.setPen(bc)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout


    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.resize(800, 520)
            self.bvLayout = QVBoxLayout(self)
            self.hLayout = QHBoxLayout(self)
            self.bvLayout.addLayout(self.hLayout)

            self.hLayout.addWidget(OutlinePushButton('应用', self))
            self.hLayout.addWidget(OutlinePushButton('游戏', self))
            self.hLayout.addWidget(OutlinePushButton('电影和电视', self))
            self.hLayout.addWidget(OutlinePushButton('设备附带', self))

            self.button = OutlinePushButton(FluentIcon.SETTING, 'change', self)
            self.button.checkedChange.connect(lambda b: {
                setThemeColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) if b else None,
                print(self.button.isChecked())
            })
            self.hLayout.addWidget(self.button)

            self.db = OutlinePushButton('fixed outline color', self)
            self.db.setOutlineColor('deeppink')
            self.hLayout.addWidget(self.db)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
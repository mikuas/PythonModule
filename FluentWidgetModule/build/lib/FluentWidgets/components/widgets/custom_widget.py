# coding:utf-8

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPainter, Qt, QPainterPath, QImage
from PySide6.QtWidgets import QWidget
from qfluentwidgets import isDarkTheme, Theme, setTheme, qconfig


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self._xRadius = 0
        self._yRadius = 0
        self._opacity = 1.0
        self._backgroundImg = None # type: QImage | str
        self._darkBackgroundColor = QColor(32, 32, 32)
        self._lightBackgroundColor = QColor(243, 243, 243)
        self.__transparentBgc = False
        qconfig.themeChanged.connect(self.update)

    def setBackgroundImg(self, image: QImage | str = None):
        """ set background image """
        self._backgroundImg = QImage(image)
        self.update()

    def setOpacity(self, opacity: float):
        """ set background opacity, range from 0 to 1 """
        self.setWindowOpacity(opacity)

    def setRadius(self, xRadius: int, yRadius: int):
        """ set widget radius """
        self._xRadius = xRadius
        self._yRadius = yRadius
        self.update()

    def setDarkBackgroundColor(self, color: QColor | str):
        self._darkBackgroundColor = QColor(color)
        self.update()

    def setLightBackgroundColor(self, color: QColor | str):
        self._lightBackgroundColor = QColor(color)
        self.update()

    def setBackgroundColor(self, light: QColor | str, dark: QColor | str):
        self.setDarkBackgroundColor(dark)
        self.setLightBackgroundColor(light)

    def getColor(self):
        return self._darkBackgroundColor if isDarkTheme() else self._lightBackgroundColor

    def getXRadius(self):
        return self._xRadius

    def getYRadius(self):
        return self._yRadius

    def getBackgroundImg(self):
        return self._backgroundImg

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.__transparentBgc:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform)
        painter.setBrush(self.getColor())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())
        if self._backgroundImg:
            path = QPainterPath()
            rect = QRectF(self.rect())
            path.addRoundedRect(rect, self.getXRadius(), self.getYRadius())
            painter.setClipPath(path)
            painter.drawImage(rect, self.getBackgroundImg())

    def enableTransparentBackground(self, enable: bool):
        self.__transparentBgc = enable
        self.update()
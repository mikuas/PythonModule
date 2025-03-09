# coding:utf-8

from FluentWidgets import VBoxLayout
from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPainter, Qt, QPainterPath, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import isDarkTheme, Theme, setTheme, PushButton


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self._xRadius = 0
        self._yRadius = 0
        self._opacity = 1.0
        self._backgroundImg = None # type: QImage | str
        self._darkColor = QColor(32, 32, 32)
        self._lightColor = QColor(243, 243, 243)

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

    def setDarkColor(self, color: QColor | str):
        self._darkColor = QColor(color)
        self.update()

    def setLightColor(self, color: QColor | str):
        self._lightColor = QColor(color)
        self.update()

    def setBackgroundColor(self, light: QColor, dark: QColor):
        self.setDarkColor(dark)
        self.setLightColor(light)

    def getColor(self):
        return self._darkColor if isDarkTheme() else self._lightColor

    def getXRadius(self):
        return self._xRadius

    def getYRadius(self):
        return self._yRadius

    def getBackgroundImg(self):
        return self._backgroundImg

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform)
        painter.setBrush(self.getColor())
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())
        if self._backgroundImg is not None:
            path = QPainterPath()
            rect = QRectF(self.rect())
            path.addRoundedRect(rect, self.getXRadius(), self.getYRadius())
            painter.setClipPath(path)
            painter.drawImage(rect, self.getBackgroundImg())


if __name__ == '__main__':
    class Demo(Widget):
        def __init__(self):
            super().__init__()
            self.layout = VBoxLayout(self)
            self.widget1 = Widget(self)
            self.widget2 = Widget(self)

            self.widget1.setOpacity(0.8)
            self.widget2.setOpacity(0.8)

            button = PushButton("TOGGLE", self)
            button.clicked.connect(lambda: self.widget1.setBackgroundImg(r"C:\Users\Administrator\OneDrive\Pictures\ide.png"))
            self.layout.addWidget(self.widget1)
            self.layout.addWidget(self.widget2)
            self.layout.addWidget(button)


            self.widget1.setDarkColor(QColor('deepskyblue'))
            self.widget1.setRadius(16, 16)

            self.widget2.setBackgroundImg(r"C:\Users\Administrator\OneDrive\Pictures\14.jpg")

            self.layout.setContentsMargins(0, 0, 0, 0)
            self.setOpacity(0.9)

    app = QApplication([])
    demo = Demo()
    demo.resize(1000, 600)
    demo.show()
    app.exec()
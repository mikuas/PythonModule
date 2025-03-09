# coding:utf-8
import ctypes

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QColor, QPainter, Qt, QPainterPath, QImage
from PySide6.QtWidgets import QWidget

from ...common import isDarkTheme, Theme, setTheme


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

        # self._timer = QTimer(self)
        # self._timer.setSingleShot(True)
        # self._timer.timeout.connect(self.__updateTheme)
        #
        # QApplication.instance().installEventFilter(self)

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

    # def __updateTheme(self):
    #     """根据当前的调色板判断是深色还是浅色主题"""
    #     palette = QApplication.palette()
    #     bg_color = palette.color(QPalette.Window)
    #
    #     # 简单判断：如果背景颜色较暗，则是深色模式
    #     brightness = (bg_color.red() * 0.299 + bg_color.green() * 0.587 + bg_color.blue() * 0.114)
    #     if brightness < 120:
    #         setTheme(Theme.DARK, True)
    #         print("DARK")
    #     else:
    #         setTheme(Theme.LIGHT, True)
    #         print("LIGHT")
    #     self.update()
    #
    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.Type.ThemeChange:
    #         self._timer.start(100)
    #     return super().eventFilter(obj, event)

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


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("Flags", ctypes.c_int),
        ("GradientColor", ctypes.c_int),
        ("AnimationId", ctypes.c_int)
    ]

class WINDOW_COMPOSITION_ATTRIB_DATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.c_void_p),
        ("SizeOfData", ctypes.c_size_t)
    ]


class BlurEffectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.__hwnd = self.winId()  # 获取窗口句柄
        self.__accent = ACCENT_POLICY()
        self.__data = WINDOW_COMPOSITION_ATTRIB_DATA()
        self.__data.Attribute = 19  # WCA_ACCENT_POLICY

        self.__timer = QTimer(self)
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(self.__enableBlur)  # 延迟启用毛玻璃

    def __enableBlur(self):
        self.__accent.AccentState = 3  # 3 代表启用毛玻璃
        self.__accent.GradientColor = 0xCCFFFFFF  # 透明度值（0xCC代表透明度）
        self.__blur()

    def __disableBlur(self):
        self.__accent.AccentState = 0  # 0 表示禁用毛玻璃效果
        self.__accent.GradientColor = 0xCC000000
        self.__blur()

    def __blur(self):
        self.__data.Data = ctypes.cast(ctypes.pointer(self.__accent), ctypes.c_void_p)
        self.__data.SizeOfData = ctypes.sizeof(self.__accent)
        ctypes.windll.user32.SetWindowCompositionAttribute(self.__hwnd, ctypes.byref(self.__data))

    def resizeEvent(self, event):
        """开始拖动时禁用毛玻璃效果"""
        self.__disableBlur()
        self.__timer.start(120)
        super().resizeEvent(event)
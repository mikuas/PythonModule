# coding:utf-8
import weakref
from enum import Enum

from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QEvent
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QFrame,  QGraphicsOpacityEffect, QWidget
from qfluentwidgets import BodyLabel, TransparentToolButton, FluentIcon, SubtitleLabel, setTheme, Theme, qconfig

from FluentWidgets import VBoxLayout, HBoxLayout


class ToastInfoBarColor(Enum):
    """ toast infoBar color """
    SUCCESS = '#4CAF50'
    ERROR = '#FF5733'
    WARNING = '#FFEB3B'
    INFO = '#2196F3'

    def __new__(cls, color):
        obj = object.__new__(cls)
        obj.color = QColor(color)
        return obj

    @property
    def value(self):
        return self.color


class ToastInfoBarPosition(Enum):
    """ toast infoBar position """
    TOP = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5


class ToastInfoBar(QFrame):
    """ toast infoBar """
    def __init__(
            self,
            parent,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_LEFT,
            toastColor=ToastInfoBarColor.SUCCESS
    ):
        super().__init__(parent)
        setTheme(Theme.AUTO)
        self.parent().installEventFilter(self)
        self.setMinimumSize(200, 60)
        self.duration = duration
        self.toastColor = toastColor
        self.position = position

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.vBoxLayout = VBoxLayout(self)
        self.hBoxLayout = HBoxLayout()
        self.hBoxLayout.setSpacing(50)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        self.title = SubtitleLabel(title, self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.content = BodyLabel(content, self)

        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setVisible(isClosable)
        self.closeButton.clicked.connect(self.__createOpacityAni)

        self.hBoxLayout.addWidget(self.title, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addWidget(self.closeButton, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.vBoxLayout.addWidget(self.content)

        self.startPosition, self.endPosition = ToastInfoBarManager.get(self.position, self)

    def adjustSize(self):
        super().adjustSize()
        self.closeButton.adjustSize()

    def getBackgroundColor(self):
        self.backgroundColor = QColor('#2b2b2b') if qconfig.theme == Theme.DARK else QColor('#fbfbfb')
        return self.backgroundColor

    def setBackgroundColor(self, color: QColor):
        self.backgroundColor = color

    def __createPosAni(self):
        self.__geometryAni = QPropertyAnimation(self, b'pos')
        self.__geometryAni.setDuration(200)
        self.__geometryAni.setStartValue(self.startPosition)
        self.__geometryAni.setEndValue(self.endPosition)
        self.__geometryAni.start()

    def __createOpacityAni(self):
        self.__opacityAni = QPropertyAnimation(self.opacityEffect, b'opacity')
        self.__opacityAni.setDuration(300)
        self.__opacityAni.setStartValue(1)
        self.__opacityAni.setEndValue(0)
        self.__opacityAni.start()
        self.__opacityAni.finished.connect(self.hide)

    @classmethod
    def new(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            toastColor=ToastInfoBarColor.SUCCESS
    ):
        ToastInfoBar(parent, title, content, duration, isClosable, position, toastColor).show()

    @classmethod
    def success(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.SUCCESS.value)

    @classmethod
    def error(
            cls, parent: QWidget, title: str, content: str,
            duration=-1, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.ERROR.value)

    @classmethod
    def warning(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.WARNING.value)

    @classmethod
    def info(
            cls, parent: QWidget, title: str, content: str,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, ToastInfoBarColor.INFO.value)

    @classmethod
    def custom(
            cls, parent: QWidget, title: str, content: str, toastColor: QColor,
            duration=2000, isClosable=True, position=ToastInfoBarPosition.TOP_RIGHT
    ):
        cls.new(parent, title, content, duration, isClosable, position, toastColor)

    def hide(self):
        super().hide()
        self.deleteLater()

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() == QEvent.Type.Resize:
            self.move(ToastInfoBarManager.get(self.position, self)[1])
        return super().eventFilter(obj, event)

    def show(self):
        self.setVisible(True)
        self.__createPosAni()
        QTimer.singleShot(self.duration, self.__createOpacityAni)

    def showEvent(self, event):
        super().showEvent(event)
        manager = ToastInfoBarManager.get(self.position, self)
        manager.add(self)

    def paintEvent(self, event):
        super().paintEvent(event)
        topPainter = QPainter(self)
        topPainter.setRenderHint(QPainter.RenderHint.Antialiasing)
        topPainter.setPen(Qt.PenStyle.NoPen)
        topPainter.setBrush(self.toastColor)
        topPainter.drawRoundedRect(0, 0, self.width() - 0.1, self.height(), 8, 8)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(0, 5, self.width(), self.height() - 5, 6, 6)


class ToastInfoBarManager:
    """ ToastInfoBar manager """
    _instances = {}
    registry = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
        super().__init__()
        self.spacing = 16
        self.margin = 24
        self.toastInfoBarAnis = weakref.WeakKeyDictionary()

    def add(self, infoBar: ToastInfoBar):
        pass

    @classmethod
    def register(cls, operationEnum):
        def decorator(classType):
            cls.registry[operationEnum] = classType
            return classType
        return decorator

    @classmethod
    def get(cls, operation, toastInfoBar: ToastInfoBar):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation]().getPos(toastInfoBar)

    def _createAni(self):
        pass

    def getPos(self, infoView: QWidget):
        raise NotImplementedError

    def print(self):
        raise NotImplementedError


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP)
class TopToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width() / 1.3) / 2
        return QPoint(x, -infoBar.height()), QPoint(x, 24)


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_LEFT)
class TopLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        infoBar.adjustSize()
        return QPoint(-infoBar.width(), 24), QPoint(24, 24)

@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_RIGHT)
class TopRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        infoX = infoBar.width()
        return QPoint(x + infoX, 24), QPoint(x - infoX - self.margin, 24)


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM)
class BottomToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width() / 1.3) / 2
        y = parent.height()
        infoViewY = infoBar.height()
        return QPoint(x, y - infoViewY), QPoint(x, y - infoViewY - self.margin)


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_LEFT)
class BottomLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        y = parent.height()
        infoViewX = infoBar.width()
        infoViewY = infoBar.height()
        return QPoint(-infoViewX, y - infoViewY - self.margin), QPoint(24, y - infoViewY - self.margin)


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_RIGHT)
class BottomRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        y = parent.height()
        infoViewX = infoBar.width()
        infoViewY = infoBar.height()
        y = y - infoViewY - self.margin
        return QPoint(x + infoViewX, y), QPoint(x - infoViewX - self.margin, y)
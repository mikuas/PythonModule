# coding:utf-8
from enum import Enum
from typing import Union, List

from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QObject, QEvent, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QFrame,  QGraphicsOpacityEffect, QWidget

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import BodyLabel, TransparentToolButton, SubtitleLabel
from ...common import isDarkTheme, FluentIcon


class ToastInfoBarColor(Enum):
    """ toast infoBar color """
    SUCCESS = '#3EC870'
    ERROR = '#BC0E11'
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
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5


class ToastInfoBar(QFrame):
    """ toast infoBar """
    closeSignal = Signal()

    def __init__(
            self,
            parent,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_LEFT,
            toastColor: Union[str, QColor, ToastInfoBarColor] = ToastInfoBarColor.SUCCESS,
            isCustomBgcColor=False,
            bgcColor: str | QColor = None,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        super().__init__(parent)
        parent.installEventFilter(self)
        self.setFixedSize(width, height)
        self.duration = duration
        self.toastColor = toastColor
        self.position = position
        self.__isCustomColor = isCustomBgcColor
        self._bgcColor = QColor(bgcColor)

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

        self.hBoxLayout.addWidget(self.title, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self.closeButton, Qt.AlignRight)
        self.vBoxLayout.addWidget(self.content)

        self.manager = ToastInfoBarManager.get(self.position)
        self.title.setTextColor(*textColor)
        self.content.setTextColor(*textColor)

    def adjustSize(self):
        super().adjustSize()
        self.closeButton.adjustSize()

    def getBgcColor(self):
        if not self.__isCustomColor:
            self._bgcColor = QColor('#202020') if isDarkTheme() else QColor('#ECECEC')
        return self._bgcColor

    def setBgcColor(self, color: QColor | str):
        self._bgcColor = QColor(color)

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
            duration: int,
            isClosable: bool,
            position: ToastInfoBarPosition,
            toastColor: Union[str, QColor, ToastInfoBarColor],
            isCustomBgcColor=False,
            bgcColor: str | QColor = None,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        if textColor is None:
            textColor = (QColor(0, 0, 0), QColor(255, 255, 255))
        ToastInfoBar(
            parent, title, content, duration, isClosable, position,
            toastColor, isCustomBgcColor, bgcColor, width, height, textColor
        ).show()

    @classmethod
    def success(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        cls.new(
            parent, title, content, duration, isClosable, position, ToastInfoBarColor.SUCCESS.value,
            width=width, height=height, textColor=textColor
        )

    @classmethod
    def error(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=-1,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        cls.new(
            parent, title, content, duration, isClosable, position, ToastInfoBarColor.ERROR.value,
            width=width, height=height, textColor=textColor
        )

    @classmethod
    def warning(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        cls.new(
            parent, title, content, duration, isClosable, position, ToastInfoBarColor.WARNING.value,
            width=width, height=height, textColor=textColor
        )

    @classmethod
    def info(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        cls.new(
            parent, title, content, duration, isClosable, position, ToastInfoBarColor.INFO.value,
            width=width, height=height, textColor=textColor
        )

    @classmethod
    def custom(
            cls,
            parent: QWidget,
            title: str,
            content: str,
            toastColor: Union[str, QColor, ToastInfoBarColor],
            duration=2000,
            isClosable=True,
            position=ToastInfoBarPosition.TOP_RIGHT,
            isCustomBgcColor=False,
            bgcColor: str | QColor = None,
            width=200,
            height=60,
            textColor: List[QColor] = None
    ):
        cls.new(
            parent, title, content, duration, isClosable, position, QColor(toastColor),
            isCustomBgcColor, bgcColor, width, height, textColor
        )

    def showEvent(self, event):
        super().showEvent(event)
        self.manager.add(self)
        self.startPosition, self.endPosition = self.manager.getPos(self)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.closeSignal.emit()
        self.deleteLater()

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.move(self.manager.getPos(self)[1])
        return super().eventFilter(obj, event)

    def show(self):
        self.setVisible(True)
        self.__createPosAni()
        QTimer.singleShot(self.duration, self.__createOpacityAni)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.toastColor)
        painter.drawRoundedRect(0, 0, self.width() - 0.1, self.height(), 8, 8)

        painter.setBrush(self.getBgcColor())
        painter.drawRoundedRect(0, 5, self.width(), self.height() - 5, 6, 6)


class ToastInfoBarManager(QObject):
    """ ToastInfoBar manager """
    _instance = None
    registry = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToastInfoBarManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.spacing = 16
        self.margin = 24
        self.infoBars = []
        self.__initialized = True

    def add(self, infoBar: ToastInfoBar):
        infoBar.closeSignal.connect(lambda: self.remove(infoBar))
        self.infoBars.append(infoBar)

    def remove(self, infoBar: ToastInfoBar):
        self.infoBars.remove(infoBar)
        self.__adjustMove()

    def __adjustMove(self):
        for bar in self.infoBars:
            bar.move(self.getPos(bar)[1])

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType

        return decorator

    @classmethod
    def get(cls, operation):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation]()

    def getPos(self, infoBar: ToastInfoBar):
        raise NotImplementedError


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP)
class TopToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width() / 1.3) / 2
        y = -self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y), QPoint(x, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_LEFT)
class TopLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        infoBar.adjustSize()
        y = -self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(-infoBar.width(), y), QPoint(24, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_RIGHT)
class TopRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        infoX = infoBar.width()
        y = -self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y += bar.height() + self.margin
        return QPoint(x + infoX, y), QPoint(x - infoX - self.margin, y + infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM)
class BottomToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = (parent.width() - infoBar.width() / 1.3) / 2
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y), QPoint(x, y - infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_LEFT)
class BottomLeftToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(-infoBar.width(), y), QPoint(24, y - infoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_RIGHT)
class BottomRightToastInfoBarManager(ToastInfoBarManager):

    def getPos(self, infoBar):
        parent = infoBar.parent()
        infoBar.adjustSize()
        x = parent.width()
        y = parent.height() - self.margin
        for bar in self.infoBars[:self.infoBars.index(infoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x + self.margin, y), QPoint(x - infoBar.width() - self.margin, y - infoBar.height())
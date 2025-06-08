# coding:utf-8
from enum import Enum
from typing import Union

from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QObject, QEvent, Signal, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QFrame,  QGraphicsOpacityEffect, QWidget, QLabel, QVBoxLayout, QHBoxLayout

from ..widgets import TransparentToolButton
from ...common.auto_wrap import TextWrap
from ...common.icon import isDarkTheme, FluentIcon
from ...common.font import setFont


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
    closedSignal = Signal(QWidget)

    def __init__(
            self,
            title: str,
            content: str,
            duration: int,
            isClosable: bool,
            position: ToastInfoBarPosition,
            orient: Qt.Orientation,
            toastColor: Union[str, QColor, ToastInfoBarColor],
            parent: QWidget,
            backgroundColor: QColor = None
    ):
        super().__init__(parent)
        parent.installEventFilter(self)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.title = title
        self.content = content
        self.duration = duration
        self.isCloseable = isClosable
        self.orient = orient
        self.toastColor = toastColor if isinstance(toastColor, QColor) else QColor(toastColor)
        self.position = position
        self.backgroundColor = backgroundColor

        self.titleLabel = QLabel(self)
        self.contentLabel = QLabel(self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.hBoxLayout = QHBoxLayout(self)
        if orient == Qt.Horizontal:
            self.textLayout = QHBoxLayout()
            self.widgetLayout = QHBoxLayout()
        else:
            self.textLayout = QVBoxLayout()
            self.widgetLayout = QVBoxLayout()

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.__opacityAni = QPropertyAnimation(self.opacityEffect, b'opacity', self)
        self.__posAni = QPropertyAnimation(self, b'pos')
        self.__posAni.setEasingCurve(QEasingCurve.OutQuad)
        self.manager = ToastInfoBarManager.get(self.position)

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        self.closeButton.setFixedSize(36, 36)
        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.setVisible(self.isCloseable)
        self.closeButton.clicked.connect(self.close)

        setFont(self.titleLabel, 16, QFont.Weight.DemiBold)
        setFont(self.contentLabel)

    def __initLayout(self):
        self.hBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.textLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.textLayout.setAlignment(Qt.AlignTop)
        self.textLayout.setContentsMargins(1, 8, 0, 8)

        self.hBoxLayout.setSpacing(0)
        self.textLayout.setSpacing(5)

        self.textLayout.addWidget(self.titleLabel, 1, Qt.AlignTop)
        self.titleLabel.setVisible(bool(self.title))

        if self.orient == Qt.Horizontal:
            self.textLayout.addSpacing(7)

        self.textLayout.addWidget(self.contentLabel, 1, Qt.AlignTop)
        self.contentLabel.setVisible(bool(self.content))
        self.hBoxLayout.addLayout(self.textLayout)

        if self.orient == Qt.Horizontal:
            self.hBoxLayout.addLayout(self.widgetLayout)
            self.widgetLayout.setSpacing(10)
        else:
            self.textLayout.addLayout(self.widgetLayout)

        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignLeft)

        self._adjustText()

    def __createPosAni(self):
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self.startPosition)
        self.__posAni.setEndValue(self.endPosition)
        self.__posAni.start()

    def __createOpacityAni(self):
        self.__opacityAni.setDuration(300)
        self.__opacityAni.setStartValue(1)
        self.__opacityAni.setEndValue(0)
        self.__opacityAni.finished.connect(self.close)
        self.__opacityAni.start()

    def _adjustText(self):
        width = self.parent().width() / 1.5

        chars = max(min(width / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        chars = max(min(width / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])
        self.adjustSize()

    @classmethod
    def new(
            cls,
            title: str,
            content: str,
            duration: int,
            isClosable: bool,
            position: ToastInfoBarPosition,
            orient=Qt.Horizontal,
            toastColor: Union[str, QColor, ToastInfoBarColor] = ToastInfoBarColor.SUCCESS,
            parent: QWidget = None,
            backgroundColor: QColor = None,
    ):
        toastInfoBar = ToastInfoBar(
            title, content, duration, isClosable, position, orient, toastColor, parent, backgroundColor
        )
        toastInfoBar.show()
        return toastInfoBar

    @classmethod
    def info(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient: Qt.Orientation = Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.INFO.value, parent
        )

    @classmethod
    def success(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.SUCCESS.value, parent
        )

    @classmethod
    def warning(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.WARNING.value, parent
        )

    @classmethod
    def error(
            cls,
            title: str,
            content: str,
            duration: int = -1,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.ERROR.value, parent
        )

    @classmethod
    def custom(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
            toastColor: Union[str, QColor] = None,
            backgroundColor: QColor = None
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, toastColor, parent, backgroundColor
        )

    def addWidget(self, widget: QWidget, stretch=0):
        self.widgetLayout.addSpacing(6)
        align = Qt.AlignTop if self.orient == Qt.Vertical else Qt.AlignVCenter
        self.widgetLayout.addWidget(widget, stretch, Qt.AlignLeft | align)

    def showEvent(self, event):
        super().showEvent(event)
        self.manager.add(self)
        self.startPosition = self.manager._slideStartPos(self)
        self.endPosition = self.manager._pos(self)
        self.__createPosAni()

        if self.duration >= 0:
            QTimer.singleShot(self.duration, self.__createOpacityAni)

    def closeEvent(self, event):
        super().closeEvent(event)
        self.closedSignal.emit(self)
        self.deleteLater()

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self._adjustText()
            try:
                self.move(self.manager._pos(self))
            except ValueError: ...
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.toastColor)
        painter.drawRoundedRect(0, 0, self.width() - 0.1, self.height(), 8, 8)

        c = self.backgroundColor or (QColor("#202020") if isDarkTheme() else QColor("#ECECEC"))
        painter.setBrush(c)
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
        self.toastInfoBars = []
        self.__initialized = True

    def add(self, infoBar: ToastInfoBar):
        infoBar.closedSignal.connect(self.remove)
        self.toastInfoBars.append(infoBar)

    def remove(self, infoBar: ToastInfoBar):
        self.toastInfoBars.remove(infoBar)
        self.__adjustMove()

    def __adjustMove(self):
        for bar in self.toastInfoBars:
            bar.move(self._pos(bar))

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

    def _pos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        raise NotImplementedError

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        raise NotImplementedError


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP)
class TopToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        x = (toastInfoBar.parent().width() - toastInfoBar.width()) / 2
        y = -self.margin * 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(pos.x(), pos.y() - toastInfoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_LEFT)
class TopLeftToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        x = self.margin
        y = -self.margin * 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(-toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_RIGHT)
class TopRightToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        x = toastInfoBar.parent().width() - toastInfoBar.width() - self.margin
        y = -self.margin * 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(toastInfoBar.parent().width() + toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM)
class BottomToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        parent = toastInfoBar.parent()
        x = (parent.width() - toastInfoBar.width()) / 2
        y = parent.height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(pos.x(), pos.y() + toastInfoBar.height())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_LEFT)
class BottomLeftToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        x = self.margin
        y = toastInfoBar.parent().height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(-toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_RIGHT)
class BottomRightToastInfoBarManager(ToastInfoBarManager):

    def _pos(self, toastInfoBar):
        parent = toastInfoBar.parent()
        x = parent.width() - toastInfoBar.width() - self.margin
        y = parent.height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def _slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self._pos(toastInfoBar)
        return QPoint(toastInfoBar.parent().width() + self.margin, pos.y())
# coding:utf-8
from enum import Enum

from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QFrame, QWidget, QLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QEvent, QRect

from ..layout import VBoxLayout, HBoxLayout
from ..widgets import TransparentToolButton, SubtitleLabel
from ...common import FluentIcon, isDarkTheme


class PopupDrawerPosition(Enum):
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3


class PopupDrawerWidget(QFrame):
    """ pop drawer widget base """

    def __init__(
            self,
            parent,
            title="PopDrawer",
            duration=300,
            aniType=QEasingCurve.OutCubic,
            position=PopupDrawerPosition.LEFT
    ):
        super().__init__(parent)
        # Linear
        # InBack
        self.drawerManager = PopDrawerManager.get(position, self)
        self.__lightBgcColor = QColor("#ECECEC")
        self.__darkBgcColor = QColor("#323232")
        self.__xRadius = 8
        self.__yRadius = 8
        self.__isPopup = False
        self.__clickParentHide = False
        self.__geometryAni = QPropertyAnimation(self, b'geometry')
        self.__geometryAni.setEasingCurve(aniType)
        self.__geometryAni.setDuration(duration)

        self.setGeometry(*self.drawerManager.geometry)
        parent.installEventFilter(self)
        self.__initWidget(title)
        self.__initLayout()
        self.__initShadowEffect()

    def __initLayout(self):
        self.vBoxLayout = VBoxLayout(self)
        self.titleLayout = HBoxLayout()
        self.vBoxLayout.insertLayout(0, self.titleLayout)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.titleLayout.addWidget(self._title)
        self.titleLayout.addWidget(self._closeButton, alignment=Qt.AlignRight)

    def __initWidget(self, title):
        self._title = SubtitleLabel(title, self)
        self._title.setVisible(bool(title))
        self._closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self._closeButton.setCursor(Qt.PointingHandCursor)
        self._closeButton.setIconSize(QSize(12, 12))
        self._closeButton.clicked.connect(lambda: self.popDrawer(True))

    def __initShadowEffect(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(24)
        self._shadow.setOffset(0, 0)
        self._shadow.setColor(QColor(0, 0, 0, 128))
        self.setGraphicsEffect(self._shadow)

    def __adjustDrawer(self):
        self.setGeometry(*self.drawerManager.newGeometry(self.__isPopup))

    def hideCloseButton(self, hide: bool):
        if hide:
            self._closeButton.hide()

    def setDuration(self, duration: int):
        self.__geometryAni.setDuration(duration)

    def setClickParentHide(self, hide: bool):
        self.__clickParentHide = hide

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignTop):
        """ add widget to layout """
        self.vBoxLayout.addWidget(widget, stretch, alignment)

    def addLayout(self, layout: QLayout, stretch=0):
        self.vBoxLayout.addLayout(layout, stretch)

    def setTitleText(self, text: str):
        self._title.setText(text)

    def setDuration(self, duration: int):
        self.duration = duration

    def setAniType(self, aniType: QEasingCurve.Type):
        self.__geometryAni.setEasingCurve(aniType)

    def setRoundRadius(self, xRadius: int, yRadius: int):
        self.__xRadius = xRadius
        self.__yRadius = yRadius
        self.update()

    def setBackgroundColor(self, lightColor: QColor | str, darkColor: QColor | str):
        self.__lightBgcColor = QColor(lightColor)
        self.__darkBgcColor = QColor(darkColor)
        self.update()

    def getBackgroundColor(self):
        return self.__darkBgcColor if isDarkTheme() else self.__lightBgcColor

    @property
    def xRadius(self):
        return self.__xRadius

    @property
    def yRadius(self):
        return self.__yRadius

    @property
    def isPopup(self):
        return self.__isPopup

    def popDrawer(self, hide=False):
        self.__geometryAni.stop()
        self.__isPopup = not hide
        self.__geometryAni.setStartValue(self.geometry())
        self.__geometryAni.setEndValue(self.drawerManager.getEndRectValue(hide))
        self.__geometryAni.start()
        self.raise_()

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
                self.__adjustDrawer()
                self.raise_()
            if self.__clickParentHide and event.type() == QEvent.MouseButtonPress:
                self.popDrawer(True)
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        event.accept()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(self.rect(), self.xRadius, self.yRadius)


class PopDrawerManager:
    registry = {}

    def __init__(self, popDrawer: PopupDrawerWidget):
        super().__init__()
        self.popDrawer = popDrawer
        self.parent = popDrawer.parent()

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType

        return decorator

    @classmethod
    def get(cls, operation, popDrawer: PopupDrawerWidget):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation](popDrawer)

    def getEndRectValue(self, hide=False):
        raise NotImplementedError

    def newGeometry(self, isPop: bool):
        raise NotImplementedError

    @property
    def geometry(self):
        raise NotImplementedError


@PopDrawerManager.register(PopupDrawerPosition.TOP)
class TopPopDrawerManager(PopDrawerManager):

    def newGeometry(self, isPop):
        height = self.popDrawer.height()
        width = self.parent.width()
        return (0, 0, width, height) if isPop else (0, -height, width, height)

    def getEndRectValue(self, hide=False):
        height = self.popDrawer.height()
        width = self.parent.width()
        return QRect(0, -height, width, height) if hide else QRect(0, 0, width, height)

    @property
    def geometry(self):
        return (0, -200, self.parent.width(), 200)


@PopDrawerManager.register(PopupDrawerPosition.BOTTOM)
class BottomTopDrawerManager(PopDrawerManager):

    def newGeometry(self, isPop):
        width = self.parent.width()
        height = self.popDrawer.height()
        parentHeight = self.parent.height()
        return (0, parentHeight - height, width, height) if isPop else (0, parentHeight, width, height)

    def getEndRectValue(self, hide=False):
        width = self.parent.width()
        height = self.popDrawer.height()
        parentHeight = self.parent.height()
        return QRect(0, parentHeight, width, height) if hide else QRect(0, parentHeight - height, width, height)

    @property
    def geometry(self):
        width = self.parent.width()
        height = self.parent.height()
        return (0, height, width, 200)


@PopDrawerManager.register(PopupDrawerPosition.LEFT)
class LeftPopDrawerManager(PopDrawerManager):

    def newGeometry(self, isPop):
        width = self.popDrawer.width()
        height = self.parent.height()
        return (0, 0, width, height) if isPop else (-width, 0, width, height)

    def getEndRectValue(self, hide=False):
        width = self.popDrawer.width()
        height = self.parent.height()
        return QRect(-width, 0, width, height) if hide else QRect(0, 0, width, height)

    @property
    def geometry(self):
        return (-300, 0, 300, self.parent.height())


@PopDrawerManager.register(PopupDrawerPosition.RIGHT)
class RightPopDrawerManager(PopDrawerManager):

    def newGeometry(self, isPop):
        width = self.popDrawer.width()
        parentWidth = self.parent.width()
        parentHeight = self.parent.height()
        return (parentWidth - width, 0, width, parentHeight) if isPop else (parentWidth, 0, width, parentHeight)

    def getEndRectValue(self, hide=False):
        width = self.popDrawer.width()
        parentWidth = self.parent.width()
        parentHeight = self.parent.height()
        return QRect(parentWidth, 0, width, parentHeight) if hide else QRect(parentWidth - width, 0, width, parentHeight)

    @property
    def geometry(self):
        parentWidth = self.parent.width()
        parentHeight = self.parent.height()
        return (parentWidth, 0, 300, parentHeight)
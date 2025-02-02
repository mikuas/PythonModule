# coding:utf-8
from enum import Enum
from PySide6.QtWidgets import QFrame, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize, QEvent
from PySide6.QtGui import QColor, QPainter

from FluentWidgets import VBoxLayout, HBoxLayout
from qfluentwidgets import FluentIcon, TransparentToolButton, SubtitleLabel, setTheme, Theme, qconfig


class PopDrawerWidgetPosition(Enum):
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3


class PopDrawerWidgetManager:
    registry = {}

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType
        return decorator

    @classmethod
    def get(cls, operation):
        operationClass = cls.registry.get(operation)
        if operationClass:
            return operationClass()
        else:
            raise ValueError(f"No operation registered for {operation}")


    def getPos(self, parent: QWidget):
        raise NotImplementedError

    def setEventFilter(self, parent: QWidget):
        raise NotImplementedError

@PopDrawerWidgetManager.register(PopDrawerWidgetPosition.TOP)
class TopPopDrawerWidget(PopDrawerWidgetManager):

    def getPos(self, parent):
        return (QPoint(0, -parent.height()), QPoint(0, 0)), (QPoint(0, 0), QPoint(0, -parent.height()))

    def setEventFilter(self, parent: QWidget):
        parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._width = self.parent().width()
                self.setFixedSize(self._width, self._height)
                self.move(self.getShowPos()[1])
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return False


class PopDrawerWidgetBase(QFrame):
    """ pop drawer widget base """
    def __init__(
            self,
            parent,
            title='弹出抽屉',
            duration=250,
            aniType=QEasingCurve.Type.Linear,
            width: int = None,
            height: int = None,
            lightBgcColor: QColor | str = '#ECECEC',
            darkBgcColor: QColor | str = '#202020',
            xRadius=10,
            yRyRadius=10,
            clickParentHide=True
    ):
        super().__init__(parent)
        # Linear
        # InBack
        setTheme(Theme.AUTO)
        self.aniType = aniType
        self.duration = duration
        self._width = width
        self._height = height
        self.__xRadius = xRadius
        self.__yRadius = yRyRadius
        self.__lightBgcColor = QColor(lightBgcColor)
        self.__darkBgcColor = QColor(darkBgcColor)
        self._clickParentHide = clickParentHide
        self.__showPos = None
        self.__hidePos = None

        self._title = SubtitleLabel(title, self)
        self._title.setVisible(bool(title))
        self._closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self._closeButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self._closeButton.setIconSize(QSize(12, 12))
        self._closeButton.clicked.connect(self.hide)

        self.setFixedSize(self._width, self._height)
        self.parent().installEventFilter(self)
        super().hide()
        self.__initLayout()

    def __initLayout(self):
        self.__vBoxLayout = VBoxLayout(self)
        self.__hBoxLayout = HBoxLayout(self)
        self.__vBoxLayout.insertLayout(0, self.__hBoxLayout)
        self.__vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__hBoxLayout.addWidget(self._title)
        self.__hBoxLayout.addWidget(self._closeButton, alignment=Qt.AlignmentFlag.AlignRight)

    def setClickParentHide(self, isHide: bool):
        self._clickParentHide = isHide

    def addWidget(self, widget: QWidget):
        """ add widget to layout """
        self.__vBoxLayout.addWidget(widget)
        return self

    def setTitleText(self, text: str):
        self._title.setText(text)

    def __createPosAni(self, startPoint: QPoint, endPoint: QPoint):
        self.__posAni = QPropertyAnimation(self, b'pos')
        self.__posAni.setEasingCurve(self.aniType)
        self.__posAni.setDuration(self.duration)
        self.__posAni.setStartValue(startPoint)
        self.__posAni.setEndValue(endPoint)
        self.__posAni.start()

    def setRoundRadius(self, xRadius: int, yRadius: int):
        self.__xRadius = xRadius
        self.__yRadius = yRadius
        self.update()

    def setBackgroundColor(self, lightColor: QColor | str, darkColor: QColor | str):
        self.__lightBgcColor = QColor(lightColor)
        self.__darkBgcColor = QColor(darkColor)
        self.update()

    def getBackgroundColor(self):
        return self.__darkBgcColor if qconfig.theme == Theme.DARK else self.__lightBgcColor

    def getXRadius(self):
        return self.__xRadius

    def getYRadius(self):
        return self.__yRadius

    def show(self):
        if self.isVisible():
            self.hide()
            return
        self.setVisible(True)
        self.raise_()
        self.__createPosAni(*self.__showPos)

    def hide(self):
        if self.isVisible():
            self.__createPosAni(*self.__hidePos)
            QTimer.singleShot(self.duration, lambda: self.setVisible(False))

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._height = self.parent().height()
                self.setFixedSize(self._width, self._height)
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return super().eventFilter(obj, event)

    def _setPos(self, showPos: QPoint, hidePos: QPoint):
        self.__showPos = showPos
        self.__hidePos = hidePos

    def mousePressEvent(self, event):
        # 阻止事件传递给父类控件
        event.accept()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.getBackgroundColor())
        painter.drawRoundedRect(self.rect(), self.getXRadius(), self.getYRadius())
# coding:utf-8
from PySide6.QtGui import QColor, QPainter

from ..layout import VBoxLayout, HBoxLayout
from PySide6.QtWidgets import QFrame, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize, QEvent
from qfluentwidgets import FluentIcon, TransparentToolButton, SubtitleLabel, setTheme, Theme, qconfig


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
        self.__createPosAni(*self._getShowPos())

    def hide(self):
        if self.isVisible():
            self.__createPosAni(*self._getHidePos())
            QTimer.singleShot(self.duration, lambda: self.setVisible(False))

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._height = self.parent().height()
                self.setFixedSize(self._width, self._height)
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return super().eventFilter(obj, event)

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

    def _getShowPos(self):
        raise NotImplementedError

    def _getHidePos(self):
        raise NotImplementedError


class LeftPopDrawerWidget(PopDrawerWidgetBase):
    """ left pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            duration=250,
            aniType=QEasingCurve.Type.Linear,
            width=None,
            height=None,
            lightBgcColor='#ECECEC',
            darkBgcColor='#202020',
            xRadius=10,
            yRyRadius=10,
            clickParentHide=True
    ):
        super().__init__(
            parent, title, duration, aniType, width or 300, height or parent.height(),
            lightBgcColor, darkBgcColor, xRadius, yRyRadius, clickParentHide
        )

    def _getShowPos(self):
        return QPoint(-self.width(), 0), QPoint(0, 0)

    def _getHidePos(self):
        return QPoint(0, 0), QPoint(-self.width(), 0)


class RightPopDrawerWidget(PopDrawerWidgetBase):
    """ right pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            duration=250,
            aniType=QEasingCurve.Type.Linear,
            width=None,
            height=None,
            lightBgcColor='#ECECEC',
            darkBgcColor='#202020',
            xRadius=10,
            yRyRadius=10,
            clickParentHide=True
    ):
        super().__init__(
            parent, title, duration, aniType, width or 300, height or parent.height(),
            lightBgcColor, darkBgcColor, xRadius, yRyRadius, clickParentHide
        )

    def _getShowPos(self):
        parentWidth = self.parent().width()
        width = self.width()
        return QPoint(parentWidth + width, 0), QPoint(parentWidth - width, 0)

    def _getHidePos(self):
        parentWidth = self.parent().width()
        width = self.width()
        return QPoint(parentWidth - width, 0), QPoint(parentWidth + width, 0)

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._height = self.parent().height()
                self.setFixedSize(self._width, self._height)
                self.move(self._getShowPos()[1])
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return super().eventFilter(obj, event)


class TopPopDrawerWidget(PopDrawerWidgetBase):
    """ top pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            duration=250,
            aniType=QEasingCurve.Type.Linear,
            width=None,
            height=None,
            lightBgcColor='#ECECEC',
            darkBgcColor='#202020',
            xRadius=10,
            yRyRadius=10,
            clickParentHide=True
    ):
        super().__init__(
            parent, title, duration, aniType, width or parent.width(), height or 250,
            lightBgcColor, darkBgcColor, xRadius, yRyRadius, clickParentHide
        )

    def _getShowPos(self):
        return QPoint(0, -self.height()), QPoint(0, 0)

    def _getHidePos(self):
        return QPoint(0, 0), QPoint(0, -self.height())

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._width = self.parent().width()
                self.setFixedSize(self._width, self._height)
                self.move(self._getShowPos()[1])
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return False


class BottomPopDrawerWidget(PopDrawerWidgetBase):
    """ bottom pop drawer widget """

    def __init__(
            self,
            parent,
            title='弹出抽屉',
            duration=250,
            aniType=QEasingCurve.Type.Linear,
            width=None,
            height=None,
            lightBgcColor='#ECECEC',
            darkBgcColor='#202020',
            xRadius=10,
            yRyRadius=10,
            clickParentHide=True
    ):
        super().__init__(
            parent, title, duration, aniType, width or parent.width(), height or 250,
            lightBgcColor, darkBgcColor, xRadius, yRyRadius, clickParentHide
        )

    def _getShowPos(self):
        parentHeight = self.parent().height()
        height = self.height()
        return QPoint(0, parentHeight + height), QPoint(0, parentHeight - height)

    def _getHidePos(self):
        parentHeight = self.parent().height()
        height = self.height()
        return QPoint(0, parentHeight - height), QPoint(0, parentHeight + height)

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._width = self.parent().width()
                self.setFixedSize(self._width, self._height)
                self.move(self._getShowPos()[1])
            if self._clickParentHide and event.type() == QEvent.Type.MouseButtonPress:
                self.hide()
        return False
# coding:utf-8
from enum import Enum
from PySide6.QtWidgets import QStackedWidget, QWidget
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QPoint

from ...common import qconfig, isDarkTheme


class StackedPopUpPosition(Enum):
    """ stacked pop up position """
    BOTTOM_TO_TOP = 0
    TOP_TO_BOTTOM = 1
    LEFT_TO_RIGHT = 2
    RIGHT_TO_LEFT = 3
    CUSTOM_POSITION = 4


class PopUpStackedWidget(QStackedWidget):
    def __init__(
            self,
            ease=QEasingCurve.Type.Linear,
            position=StackedPopUpPosition.BOTTOM_TO_TOP,
            duration=250,
            parent=None
    ):
        super().__init__(parent)
        self.__posAni = None # type: QPropertyAnimation
        self._aniEase = ease
        self._duration = duration
        self.__startValue = None # type: QPoint
        self.__endValue = QPoint(0, 0) # type: QPoint
        self.setPopUpPosition(position)

    def setPopUpPosition(self, position: StackedPopUpPosition) -> callable:
        """ position is CUSTOM_POSITION, return setPos function """
        if position == StackedPopUpPosition.CUSTOM_POSITION:
            return self.__setPos
        if position == StackedPopUpPosition.BOTTOM_TO_TOP:
            self.__startValue = QPoint(0, 76)
        elif position == StackedPopUpPosition.TOP_TO_BOTTOM:
            self.__startValue = QPoint(0, -76)
        elif position == StackedPopUpPosition.LEFT_TO_RIGHT:
            self.__startValue = QPoint(-76, 0)
        elif position == StackedPopUpPosition.RIGHT_TO_LEFT:
            self.__startValue = QPoint(76, 0)

    def setDuration(self, duration: int):
        self._duration = duration

    def addWidget(self, w):
        self.exist(w)
        super().addWidget(w)

    def exist(self, widget: QWidget):
        for i in range(self.count()):
            if self.widget(i) == widget:
                raise ValueError("widget exist")

    def setCurrentIndex(self, index):
        w = self.widget(index)
        self.setCurrentWidget(w)

    def setCurrentWidget(self, w):
        self.__createPosAni(w)
        super().setCurrentWidget(w)

    def enableTransparentBackground(self):
        self.setStyleSheet("""QStackedWidget {background: transparent;}""")

    def __setPos(self, startValue: QPoint, endValue: QPoint):
        self.__startValue = startValue
        self.__endValue = endValue

    def __createPosAni(self, w):
        if self.currentIndex() == self.indexOf(w):
            return
        self.__currentIndex = self.indexOf(w)
        self.__posAni = QPropertyAnimation(w, b'pos')
        self.__posAni.setDuration(self._duration)
        self.__posAni.setEasingCurve(self._aniEase)
        self.__posAni.setStartValue(self.__startValue)
        self.__posAni.setEndValue(self.__endValue)
        self.__posAni.finished.connect(self.__posAni.deleteLater)
        self.__posAni.start()
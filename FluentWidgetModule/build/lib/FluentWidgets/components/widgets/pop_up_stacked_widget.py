# coding:utf-8
from enum import Enum
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QPoint


class StackedPopUpPosition(Enum):
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
        self.__ani = None # type: QPropertyAnimation
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
            self.__startValue = QPoint(0, 100)
        elif position == StackedPopUpPosition.TOP_TO_BOTTOM:
            self.__startValue = QPoint(0, -100)
        elif position == StackedPopUpPosition.LEFT_TO_RIGHT:
            self.__startValue = QPoint(-100, 0)
        elif position == StackedPopUpPosition.RIGHT_TO_LEFT:
            self.__startValue = QPoint(100, 0)

    def setDuration(self, duration: int):
        self._duration = duration

    def __setPos(self, startValue: QPoint, endValue: QPoint):
        self.__startValue = startValue
        self.__endValue = endValue

    def setCurrentIndex(self, index):
        w = self.widget(index)
        self.setCurrentWidget(w)

    def setCurrentWidget(self, w):
        self.__createAni(w)
        super().setCurrentWidget(w)

    def __createAni(self, w):
        if self.currentIndex() == self.indexOf(w):
            return
        self.__currentIndex = self.indexOf(w)
        self.__ani = QPropertyAnimation(w, b'pos')
        self.__ani.setDuration(self._duration)
        self.__ani.setEasingCurve(self._aniEase)
        self.__ani.setStartValue(self.__startValue)
        self.__ani.setEndValue(self.__endValue)
        self.__ani.finished.connect(self.__ani.deleteLater)
        self.__ani.start()
# coding:utf-8
from PySide6.QtCore import (
    QPropertyAnimation, QRect, QPoint, QSize, QParallelAnimationGroup, QSequentialAnimationGroup, QEasingCurve, QObject,
    QAbstractAnimation
)
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect


class WidgetAnimation(QObject):
    def __init__(
            self,
            target: QWidget,
            aniType,
            duration: int,
            startValue,
            endValue,
            parent,
            easing=QEasingCurve.Type.Linear,
            finished=None
    ):
        super().__init__()
        self.__animation = QPropertyAnimation(target, aniType, parent)
        self.__animation.setDuration(duration)
        self.__animation.setStartValue(startValue)
        self.__animation.setEndValue(endValue)
        if easing:
            self.__animation.setEasingCurve(easing)
        self.__animation.finished.connect(finished)


    def _getAni(self):
        return self.__animation

    @classmethod
    def createAni(
            cls,
            target: QWidget,
            aniType,
            duration: int,
            startValue,
            endValue,
            easing=QEasingCurve.Type.Linear,
            finished=None,
            parent: QWidget = None
    ):
        return WidgetAnimation(
            target, aniType, duration, startValue,
            endValue, parent or target.parent(), easing, finished
        )._getAni()

    @classmethod
    def posAni(
            cls,
            target: QWidget,
            duration: int,
            startValue: QPoint,
            endValue: QPoint,
            easing=QEasingCurve.Type.Linear,
            finished=None,
            parent: QWidget = None
    ):
        return cls.createAni(target, b'pos', duration, startValue, endValue, easing, finished, parent)

    @classmethod
    def geometryAni(
            cls,
            target: QWidget,
            duration: int,
            startValue: QRect,
            endValue: QRect,
            easing=QEasingCurve.Type.Linear,
            finished=None,
            parent: QWidget = None
    ):
        return cls.createAni(target, b'geometry', duration, startValue, endValue, easing, finished, parent)

    @classmethod
    def sizeAni(
            cls,
            target: QWidget,
            duration: int,
            startValue: QSize,
            endValue: QSize,
            easing=QEasingCurve.Type.Linear,
            finished=None,
            parent: QWidget = None
    ):
        return cls.createAni(target, b'size', duration, startValue, endValue, easing, finished, parent)

    @classmethod
    def opacityAni(
            cls,
            target: QWidget,
            duration: int,
            startValue: float,
            endValue: float,
            defaultOpacity=1,
            easing=QEasingCurve.Type.Linear,
            finished=None,
            parent: QWidget = None
    ):
        opacityEffect = QGraphicsOpacityEffect(target)
        target.setGraphicsEffect(opacityEffect)
        opacityEffect.setOpacity(defaultOpacity)
        return cls.createAni(
            opacityEffect, b'opacity', duration, startValue,
            endValue, easing, finished, parent or target.parent()
        )


class AnimationGroupBase:
    def __init__(self, parent: QWidget):
        self.__animations = []
        self.__animationGroup = None

    def addAni(self, ani: QAbstractAnimation):
        self.__animationGroup.addAnimation(ani)
        return self

    def removeAni(self, ani: QAbstractAnimation):
        self.__animationGroup.removeAnimation(ani)

    def _setGroupAni(self, obj):
        self.__animationGroup = obj

    def start(self):
        self.__animationGroup.start()

    def finish(self, function):
        self.__animationGroup.finished.connect(function)


class ParallelAnimation(AnimationGroupBase):
    def __init__(self, parent):
        super().__init__(parent)
        self._setGroupAni(QParallelAnimationGroup(parent))


class SequentialAnimation(AnimationGroupBase):
    def __init__(self, parent):
        super().__init__(parent)
        self._setGroupAni(QSequentialAnimationGroup(parent))
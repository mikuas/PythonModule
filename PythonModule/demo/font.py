# coding:utf-8
from PySide6.QtGui import QFontMetrics, QFontMetricsF, QFont

def getTextWidth(text: str, font: QFont):
    return QFontMetrics(font).horizontalAdvance(text)

def getTextWidthF(text: str, font: QFont):
    return QFontMetricsF(font).horizontalAdvance(text)
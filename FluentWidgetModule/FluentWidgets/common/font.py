# coding:utf-8
from typing import List

from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QWidget


def setFonts(widgets: List[QWidget], fontSize: int, weight: QFont.Weight = QFont.Weight.Normal):
    """ set widget font size """
    for widget in widgets:
        widget.setFont(getFont(fontSize, weight))

def getFont(fontSize: int, weight: QFont.Weight = QFont.Weight.Normal):

    """ get font size """
    font = QFont()
    font.setFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])
    font.setPixelSize(fontSize)
    font.setWeight(weight)
    return font

def setTextColor(widget: QWidget, color: QColor | str):
    widget.setStyleSheet(f"color: {color}")

def setTextColors(widgets: List[QWidget], color: List[QColor | str]):
    for widget in widgets:
        widget.setStyleSheet(f"color: {color}")
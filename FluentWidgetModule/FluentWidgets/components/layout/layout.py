# coding:utf-8
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout


class HBoxLayout(QHBoxLayout):
    """ horizontal layout """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def addWidgets(self, widgets: List[QWidget], stretch=0, alignment=Qt.AlignmentFlag(0)):
        """ add stretch default is 0, alignment default is None widgets"""
        for widget in widgets:
            self.addWidget(widget, stretch=stretch, alignment=alignment)

    def addLayouts(self, layouts: List[QLayout], stretch=0):
        """ add stretch default is 0 layouts"""
        for layout in layouts:
            self.addLayout(layout, stretch)


class VBoxLayout(QVBoxLayout, HBoxLayout):
    """ vertical layout """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
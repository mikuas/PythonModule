# coding:utf-8
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLayout


class HBoxLayout(QHBoxLayout):
    """ horizontal layout """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.widgets = []

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignTop):
        super().addWidget(widget, stretch, alignment)
        self.widgets.append(widget)

    def removeWidget(self, widget: QWidget):
        super().removeWidget(widget)
        self.widgets.remove(widget)

    def deleteWidget(self, widget: QWidget):
        self.removeWidget(widget)
        widget.hide()
        widget.deleteLater()

    def removeAllWidget(self):
        for w in self.widgets:
            super().removeWidget(w)
        self.widgets.clear()

    def addWidgets(self, widgets: List[QWidget], stretch=0, alignment=Qt.AlignTop):
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
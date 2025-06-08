# coding:utf-8
import sys
from typing import List, Union

from FluentWidgets.components.widgets.button import RoundPushButton
from FluentWidgets.components.widgets.check_box import CheckBoxState, CheckBoxIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStyledItemDelegate, QStyle, QListWidget, \
    QListWidgetItem, QStyleOptionButton
from PySide6.QtGui import QColor, QPainter, QAction
from PySide6.QtCore import Qt, QPoint, QSize, Signal

from FluentWidgets import ComboBox, EditableComboBox, VerticalScrollWidget, SplitWidget, TitleLabel, RoundListWidget, \
    PushButton, SingleDirectionScrollArea, TransparentToolButton, FluentIcon, Action, Icon, BodyLabel, CheckBox, \
    themeColor, isDarkTheme, ThemeColor
from FluentWidgets.components.widgets.combo_box import ComboBoxMenu





class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.listWidget = ComboBox(self)

        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')
        self.listWidget.addItem('hello world')

        self.box.addWidget(self.listWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import random
import sys
from typing import List


from PySide6.QtGui import QFont, Qt, QPainter, QColor, QPen
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication, QWidget, QStyle, QListWidget, QListWidgetItem, QStyledItemDelegate, QVBoxLayout, QPushButton,
    QHBoxLayout
)

from ...common.color import themeColor, isDarkTheme
from ...common.style_sheet import setThemeColor
from ...common.config import qconfig
from .line_edit import LineEdit


class RoundListWidgetItemDelegate(QStyledItemDelegate):
    def __init__(self, isFull=False, parent=None):
        super().__init__(parent)
        self.__isFull = isFull
        self.__color = None         # type: QColor
        self.__textColor = None     # type: QColor

    def createEditor(self, parent, option, index):
        editor = LineEdit(parent)
        editor.setFixedHeight(option.rect.height())
        return editor

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def setIsFull(self, isFull: bool):
        self.__isFull = isFull

    def setColor(self, color: str | QColor):
        self.__color = QColor(color)

    def setTextColor(self, textColor: str | QColor):
        self.__textColor = QColor(textColor)

    def paint(self, painter, option, index):
        painter.save()

        # 设置背景
        rect = option.rect.adjusted(2, 2, -2, -2)
        isDark = isDarkTheme()
        textColor = self.__textColor or (QColor("#000000") if isDark else QColor("#ffffff"))
        if option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver):
            color = self.__color or themeColor()
        else:
            color = QColor("#000000") if isDark else QColor("#E8E8E8")
            textColor = self.__textColor or (QColor("#ffffff") if isDark else QColor("#000000"))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        if self.__isFull:
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
        else:
            pen = QPen(color)
            pen.setWidth(2)
            painter.setPen(pen)
            textColor = self.__textColor or (QColor("#ffffff") if isDark else QColor("#000000"))
        painter.drawRoundedRect(rect, 8, 8)

        # 设置字体
        alignment = index.data(Qt.ItemDataRole.TextAlignmentRole) or Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        text = index.data()
        painter.setPen(textColor)
        painter.setFont(QFont("微软雅黑", 12))
        painter.drawText(rect.adjusted(10, 0, -10, 0), alignment, text)

        painter.restore()


class RoundListWidget(QListWidget):
    def __init__(self, parent=None, isFull=False):
        """
        RoundListWidget

        isFull:
            是否填充整个item, 如果为False则描边
        """
        super().__init__(parent)
        self.__items = []       # type: List[QListWidgetItem]
        self.__oldItem = None   # type: QListWidgetItem
        self.itemDelegate = RoundListWidgetItemDelegate(isFull, self)
        from FluentWidgets import SmoothScrollDelegate
        self.scrollDelegate = SmoothScrollDelegate(self)

        self.setItemDelegate(self.itemDelegate)
        self.setStyleSheet("QListWidget {background: transparent;}")

        qconfig.themeColorChanged.connect(lambda: self.viewport().update())

    def __doubleItem(self, item):
        self.openPersistentEditor(item)
        self.__oldItem = item

    def __closeEdit(self):
        if self.__oldItem:
            self.closePersistentEditor(self.__oldItem)

    def enableDoubleItemEdit(self, enable: bool):
        if enable:
            self.itemDoubleClicked.connect(self.__doubleItem)
            self.currentItemChanged.connect(self.__closeEdit)
        else:
            self.itemDoubleClicked.disconnect(self.__doubleItem)
            self.currentItemChanged.disconnect(self.__closeEdit)

    def setItemIsFull(self, isFull: bool):
        self.itemDelegate.setIsFull(isFull)

    def setItemColor(self, color: str | QColor):
        self.itemDelegate.setColor(color)

    def setItemTextColor(self, textColor: str | QColor):
        self.itemDelegate.setTextColor(textColor)

    def setItemHeight(self, height: int):
        for item in self.items():
            item.setSizeHint(QSize(0, height))

    def items(self):
        return self.__items

    def addItem(self, item: str | QListWidgetItem):
        if isinstance(item, str):
            item = QListWidgetItem(item)
        super().addItem(item)
        self.__items.append(item)

    def addItems(self, items: list[str] | list[QListWidgetItem]):
        for item in items:
            self.addItem(item)

    def insertItem(self, row: int, item: str | QListWidgetItem):
        if isinstance(item, str):
            item = QListWidgetItem(item)
        self.__items.append(item)
        super().insertItem(row, item)

    def insertItems(self, row, items: list[str] | list[QListWidgetItem]):
        if isinstance(items[0], str):
            items = [QListWidgetItem(item) for item in items]
        self.__items += items
        super().insertItems(row, items)

    def setItemTextAlignment(self, alignment: Qt.AlignmentFlag):
        for item in self.items():
            item.setTextAlignment(alignment)
# coding:utf-8
import random
import sys
from enum import Enum
from typing import List

from FluentWidgets import Icon, FluentIcon, themeColor, setThemeColor, qconfig, isDarkTheme, setTheme, Theme, LineEdit
from PySide6.QtGui import QFont, Qt, QPainter, QColor, QPen, QIcon, QPixmap
from PySide6.QtCore import QSize, QMimeData, QPoint, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import QApplication, QWidget, QStyle, QListWidget, QListWidgetItem, QStyledItemDelegate, \
    QVBoxLayout, QPushButton, QAbstractItemView, QScroller, QSizePolicy, QHBoxLayout


class RoundListWidgetItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = LineEdit(parent)
        editor.setFixedHeight(option.rect.height())
        editor.setClearButtonEnabled(True)
        return editor

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def paint(self, painter, option, index):
        painter.save()

        # 设置背景
        rect = option.rect.adjusted(2, 2, -2, -2)
        isDark = isDarkTheme()
        if option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver):
            color = self.__color or themeColor()
        else:
            color = QColor("#000000") if isDark else QColor("#E8E8E8")
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing)

        self._drawText()
        painter.restore()

    def _drawText(self, painter: QPainter, rect: QRect, index):
        text = index.data()
        alignment = index.data(Qt.TextAlignmentRole) or Qt.AlignLeft | Qt.AlignVCenter
        color = 255 if isDarkTheme() else 0
        painter.setPen(QColor(color, color, color))
        painter.setFont(QFont("Microsoft YaHei Ui", 14))
        painter.drawText(rect.adjusted(10, 0, -10, 0), alignment, text)


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


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.vLayout = QVBoxLayout(self)
        self.hLayout = QHBoxLayout()
        self.vLayout.addLayout(self.hLayout)

        self.listWidget1 = RoundListWidget(self)
        self.listWidget2 = RoundListWidget(self, True)
        self.hLayout.addWidget(self.listWidget1)
        self.hLayout.addWidget(self.listWidget2)

        self.items = [f'item{_}' for _ in range(1, 10001)]

        self.listWidget1.addItems(self.items)
        self.listWidget1.currentItemChanged.connect(lambda item: print(item.text()))

        self.listWidget2.addItems(self.items)
        self.listWidget2.currentItemChanged.connect(lambda item: print(item.text()))

        self.listWidget1.setItemColor('#9f53ed')
        self.listWidget2.setItemColor('#9f53ed')
        self.listWidget1.setItemTextColor('deeppink')

        self.listWidget1.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.listWidget2.setDragDropMode(QListWidget.DragDropMode.InternalMove)

        self.listWidget1.setItemHeight(50)
        self.listWidget2.setItemHeight(50)

        self.listWidget1.enableDoubleItemEdit(True)
        self.listWidget2.enableDoubleItemEdit(True)

        self.button = QPushButton("random toggle", self)
        self.button.setFixedHeight(35)
        self.button.clicked.connect(lambda: {
            setThemeColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        })
        self.vLayout.addWidget(self.button)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

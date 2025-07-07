# coding:utf-8
import json
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt

from FluentWidgets import VerticalScrollWidget, ListWidget, RoundListWidget, ImageLabel, HorizontalSeparator


class ListWidgetInterface(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.enableTransparentBackground()

        with open('../files/json/data.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())["girlFriend"]

        self.listWidget = ListWidget(self)
        self.roundListWidget = RoundListWidget(self)

        self.listWidget.setFixedHeight(500)
        self.roundListWidget.setFixedHeight(500)

        self.listWidget.addItems(data)
        self.roundListWidget.addItems(data)

        self.addWidget(self.listWidget)
        self.addSpacing(32)
        self.addWidget(self.roundListWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ListWidgetInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, BreadcrumbBar

class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)

        self.breadcrumbBar = BreadcrumbBar(self)
        for _ in range(10):
            self.breadcrumbBar.addItem(
                str(_), f"Item {_}"
            )

        self.breadcrumbBar.setCurrentItem('5')

        self.box.addWidget(self.breadcrumbBar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.windowEffect.setMicaEffect(window.winId(), isAlt=True)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
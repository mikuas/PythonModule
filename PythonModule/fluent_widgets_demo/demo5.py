# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QSize

from FluentWidgets import FlipView

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.box = QVBoxLayout(self)
        self.fv = FlipView(self)

        self.fv.addImages([
            r"C:\Users\Administrator\OneDrive\FORZA\1.png",
            r"C:\Users\Administrator\OneDrive\FORZA\2.png",
            r"C:\Users\Administrator\OneDrive\FORZA\3.png",
            r"C:\Users\Administrator\OneDrive\FORZA\4.png",
            r"C:\Users\Administrator\OneDrive\FORZA\5.png"
        ])
        # self.fv.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        self.fv.setItemSize(QSize(self.width(), self.height()))

        self.box.addWidget(self.fv)

    def resizeEvent(self, event):
        self.fv.setFixedSize(self.width(), self.height())
        # super().resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())

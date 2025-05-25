# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import VerticalScrollWidget, ColorDialog, PushButton


class ColorDialogDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.colorDialog = ColorDialog("deeppink", "Select Current Color", self, True)
        self.colorDialog.colorChanged.connect(lambda color: print(f"Color: {color}"))

        self.button = PushButton("show color dialog", self)
        self.button.clicked.connect(self.colorDialog.show)

        self.addWidget(self.button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorDialogDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
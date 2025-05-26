# coding:utf-8

import sys

from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QApplication, QWidget


from FluentWidgets import TransparentPushButton, VBoxLayout, FluentIcon


class SlidingButtonBase:
    def __init__(self):
        super().__init__()
        self.isHover = False
        self.isSelected = False

    def enterEvent(self, event):
        self.isHover = True
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.update()

class Button(TransparentPushButton, SlidingButtonBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.box = VBoxLayout(self)
        self.box.addWidget(Button(FluentIcon.HOME, 'hello'))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor('deeppink'))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, 'hello world')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
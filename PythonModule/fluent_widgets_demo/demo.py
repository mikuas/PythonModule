# coding:utf-8

import sys

from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QApplication, QWidget


from FluentWidgets import TransparentPushButton, VBoxLayout, FluentIcon


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.icon = FluentIcon.HOME
        self.color = QColor('red')
        self.icon = self.icon.colored(self.color, self.color)

    def mouseReleaseEvent(self, event):
        icon = self.icon
        color = QColor('red')
        if self.color == color:
            print(self.color.name(), color.name())
            return
        self.icon = self.icon.colored(color, color)
        print(self.icon.path(), '\n', self.icon.fluentIcon, '\n', self.icon.qicon())
        print(self.icon is icon, '\n', icon.fluentIcon is self.icon.fluentIcon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
# coding:utf-8
import sys

from FluentWidgets import Widget, NavigationWidget, VBoxLayout
from PySide6.QtWidgets import QApplication, QFrame
from qfluentwidgets import PushButton, FluentIcon


class TreeLikeButton(NavigationWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = VBoxLayout(self)
        self.layout.addWidget(PushButton(FluentIcon.GITHUB, '', self))


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.layout = VBoxLayout(self)

        self.t = TreeLikeButton(self)
        self.b = NavigationBar(self)

        self.nt = NavigationTreeWidget(FluentIcon.HOME, '', False, self.b)

        self.b.addWidget('r', self.nt, None)

        self.layout.addWidget(self.t)
        self.layout.addWidget(self.b)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import NavigationBar, VerticalScrollWidget, FluentIcon


class NavigationBarDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.navigationBar = NavigationBar(self)
        for i in range(1, 21,):
            self.navigationBar.addItem(
                f"item{str(i)}",
                FluentIcon.HOME,
                f"Interface {i}",
                lambda: print(f"Click Interface {i}")
        )

        self.addWidget(self.navigationBar, alignment=Qt.AlignLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NavigationBarDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
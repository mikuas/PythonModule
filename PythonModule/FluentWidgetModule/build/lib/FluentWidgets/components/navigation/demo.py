# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout


from sliding_navigation_bar import SlidingNavigationBar


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.slidingNavBar = SlidingNavigationBar(self)
        self.box.addWidget(self.slidingNavBar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
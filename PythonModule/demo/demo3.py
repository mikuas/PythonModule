# coding:utf-8
import sys

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication
from FluentWidgets import VerticalPagerWidget, HorizontalPagerWidget, PipsPager
from qfluentwidgets import TitleLabel, PrimaryPushButton


class Window(HorizontalPagerWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 500)
        self.hoverDisplayPrevButton().hoverDisplayNextButton()

        pager = PipsPager(Qt.Orientation.Vertical, self)
        pager.setPageNumber(10)

        self.addWidget(pager)
        for _ in range(1, 6):
            self.addWidget(TitleLabel(f"Page{_}", self))
        self.addWidget(PrimaryPushButton("BUTTON", self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
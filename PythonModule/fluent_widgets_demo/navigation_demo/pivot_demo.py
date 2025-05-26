# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import VerticalScrollWidget, HorizontalScrollWidget, Pivot, FluentIcon, VBoxLayout, NavigationItemPosition


class PivotDeo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()

        self.h = HorizontalScrollWidget(self)
        self.h.setStyleSheet('background:transparent;border:none;')
        self.h.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.h.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pivot = Pivot()
        self.pivot.setStyleSheet('background:transparent;border:none;')
        for i in range(1, 21,):
            self.pivot.addItem(
                f"item{str(i)}",
                f"Interface {i}",
                lambda: print(f"Click Interface {i}"),
                # FluentIcon.HOME,
            )

        self.h.addWidget(self.pivot, alignment=Qt.AlignTop)

        self.addWidget(self.h)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PivotDeo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
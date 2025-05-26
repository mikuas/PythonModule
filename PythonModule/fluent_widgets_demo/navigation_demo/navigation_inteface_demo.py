# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import NavigationInterface, VerticalScrollWidget, FluentIcon, VBoxLayout, NavigationItemPosition


class NavigationInterfaceDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = VBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, True, True)
        for i in range(1, 21,):
            self.navigationInterface.addItem(
                f"item{str(i)}",
                FluentIcon.HOME,
                f"Interface {i}",
                lambda: print(f"Click Interface {i}"),
                position=NavigationItemPosition.SCROLL,
                tooltip=f"Interface {i}",
            )

        self.box.addWidget(self.navigationInterface, alignment=Qt.AlignLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NavigationInterfaceDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
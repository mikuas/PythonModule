# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import ExpandLayout, VerticalScrollWidget, TitleLabel


class ExpandLayoutDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.expandLayout = ExpandLayout(self)

        self.expandLayout.addWidget(TitleLabel("Hello World"))

        # for i in range(100):
        #     self.expandLayout.addWidget(TitleLabel(f"Title {i}"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpandLayoutDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
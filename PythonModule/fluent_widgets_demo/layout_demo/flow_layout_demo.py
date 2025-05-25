# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import FlowLayout, VerticalScrollWidget, TitleLabel


class FlowLayoutDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.expandLayout = FlowLayout(needAni=True, isTight=False)
        self.addLayout(self.expandLayout)

        for i in range(100):
            self.expandLayout.addWidget(TitleLabel(f"Title {i}"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FlowLayoutDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
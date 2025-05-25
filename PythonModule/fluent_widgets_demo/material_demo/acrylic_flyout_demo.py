# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import VerticalScrollWidget, AcrylicFlyout, PushButton, FluentIcon


class AcrylicComboBoxDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.button = PushButton("show flyout", self)
        self.button.clicked.connect(lambda: AcrylicFlyout.create(
            'title',
            'content',
            FluentIcon.HOME,
            image=r"C:\Users\Administrator\OneDrive\Pictures\微信图片_20250501162545.jpg",
            target=self.button,
            parent=self
        ))

        self.addWidget(self.button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AcrylicComboBoxDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
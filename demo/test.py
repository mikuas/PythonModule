import sys

from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import InfoBar, PushButton


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = PushButton('info bar', self)
        self.btn.setFixedWidth(self.width())

        self.btn.clicked.connect(
            lambda: InfoBar.success(
                'success',
                'this is a success info bar',
                duration=5000,
                parent=self
            )
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
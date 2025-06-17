# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


from FluentWidgets import PasswordLineEdit, FluentStyleSheet, LineEdit


class PinBoxLineEdit(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)

        self.textChanged.connect(self.focusNextChild)



class PinBox(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setStyleSheet(
            """
            QLineEdit {
                width: 50px;
                height: 35px;
                caret-color: transparent;
            }
            """
        )

        self.l1 = PinBoxLineEdit(self)
        self.l2 = PinBoxLineEdit(self)
        self.l3 = PinBoxLineEdit(self)
        self.l4 = PinBoxLineEdit(self)

        self.hBoxLayout = QHBoxLayout(self)

        self.l1.setCursor(QCursor())

        self.hBoxLayout.addWidget(self.l1)
        self.hBoxLayout.addWidget(self.l2)
        self.hBoxLayout.addWidget(self.l3)
        self.hBoxLayout.addWidget(self.l4)

        self.hBoxLayout.addWidget(QPushButton("Self", self))


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QVBoxLayout(self)

        self.pinBox = PinBox(self)
        self.box.addWidget(self.pinBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

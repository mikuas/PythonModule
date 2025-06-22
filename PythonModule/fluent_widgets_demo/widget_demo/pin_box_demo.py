# coding:utf-8
import sys
from typing import List

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QColor, QCursor, QPainter, QPen, QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression, Signal

from FluentWidgets import PasswordLineEdit, FluentStyleSheet, LineEdit, themeColor


class PinBoxLineEdit(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isTop = False
        self.isEnd = False
        self.setFixedSize(45, 35)
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)

        self.__regex = QRegularExpression(r"^\S*$")
        self.__validator = QRegularExpressionValidator(self.__regex)
        self.setValidator(self.__validator)
        self.textChanged.connect(self._onTextChanged)

    def keyReleaseEvent(self, e):
        super().keyReleaseEvent(e)
        if e.key() == Qt.Key.Key_Backspace and not self.isTop:
            self.focusPreviousChild()

    def _onTextChanged(self):
        text = self.text()
        if len(text) >= 1 and not self.isEnd:
            self.focusNextChild()

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.hasFocus():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(themeColor())
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class PinBox(QWidget):

    textChanged = Signal(list)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self._totas = 4
        self._pinBoxLineEdits = []  # type: List[PinBoxLineEdit]

        self.__initPinBox()
        self.hBoxLayout.setAlignment(Qt.AlignCenter)

    def setEchoMode(self, mode: QLineEdit.EchoMode):
        for edit in self._pinBoxLineEdits:
            edit.setEchoMode(mode)

    def count(self):
        return self._totas

    def setPinBoxCount(self, num: int):
        self._totas = num
        for edit in self._pinBoxLineEdits:
            edit.deleteLater()
        self._pinBoxLineEdits.clear()
        self.__initPinBox()

    def __initPinBox(self):
        for _ in range(self._totas):
            pinBox = PinBoxLineEdit(self)
            self.hBoxLayout.addWidget(pinBox)
            self._pinBoxLineEdits.append(pinBox)
            pinBox.textChanged.connect(self.__onTextChange)
        self._pinBoxLineEdits[0].isTop = True
        self._pinBoxLineEdits[-1].isEnd = True

    def __onTextChange(self):
        result = []
        for w in self._pinBoxLineEdits:
            result.append(w.text())
        self.textChanged.emit(result)


class Demo(QWidget):
    def __init__(self):
        super().__init__()

        self.box = QVBoxLayout(self)

        self.pinBox = PinBox(self)
        self.pinBox.setPinBoxCount(10)
        self.box.addWidget(self.pinBox)

        self.pinBox.textChanged.connect(print)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import sys
import time

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy
from PySide6.QtGui import QColor, QAction, QFontMetrics
from PySide6.QtCore import Qt, QTimer

from FluentWidgets import LineEdit, TitleLabel, PushButton


class LabelLineEdit(LineEdit):
    def __init__(self, prefix: str, suffix: str, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)
        self._prefixLabel = PushButton(prefix, self)
        self._suffixLabel = PushButton(suffix, self)

        self.hBoxLayout.insertWidget(0, self._prefixLabel, 1, Qt.AlignLeft)
        self.hBoxLayout.addWidget(self._suffixLabel, 0, Qt.AlignRight)

        self._prefixLabel.adjustSize()
        self._suffixLabel.adjustSize()
        self._adjustTextMargins()

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30 + self._prefixLabel.width()
        right = len(self.rightButtons) * 30 + 28 * self.isClearButtonEnabled() + self._suffixLabel.width()
        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())

    def setPrefix(self, prefix: str):
        if prefix:
            self._prefixLabel.setText(prefix)
            self._prefixLabel.adjustSize()
            self._adjustTextMargins()

    def setSuffix(self, suffix: str):
        if suffix:
            self._suffixLabel.setText(suffix)
            self._suffixLabel.adjustSize()
            self._adjustTextMargins()

    def prefix(self):
        return self._prefixLabel.text()

    def suffix(self):
        return self._suffixLabel.text()


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)

        self.edit = LabelLineEdit("https://", ".com", self)
        self.box.addWidget(self.edit)

        self.edit.setPlaceholderText("demo")

        self.edit._suffixLabel.clicked.connect(lambda: (self.edit.setPrefix(
            self.edit.text()
        ),self.edit.setSuffix(self.edit.text())
        ))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

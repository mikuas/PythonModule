# coding:utf-8
import sys

from FluentWidgets import VerticalScrollWidget
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Signal
from qfluentwidgets import TextBrowser


class SignalWidget(QWidget):
    clicked = Signal(bool)
    hoverSignal = Signal(bool)
    leaveSignal = Signal()
    resizeSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def resizeEvent(self, event):
        self.resizeSignal.emit()
        super().resizeEvent(event)

    def enterEvent(self, event):
        self.hoverSignal.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hoverSignal.emit(False)
        self.leaveSignal.emit()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(True)
        else:
            self.clicked.emit(False)
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("red"))
        painter.drawRect(self.rect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VerticalScrollWidget()
    sw = SignalWidget(window)
    sw.clicked.connect(lambda b: tb.append('left clicked') if b else tb.append('right clicked'))
    sw.hoverSignal.connect(lambda b: tb.append('is hover') if b else tb.append('not hover'))
    sw.leaveSignal.connect(lambda: tb.append('leave'))
    sw.resizeSignal.connect(lambda: tb.append('resize'))
    window.addWidget(sw)
    tb = TextBrowser(window)
    window.addWidget(tb)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
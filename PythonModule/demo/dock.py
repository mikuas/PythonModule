from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFrame
)
from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QEvent, QTimer
import sys


class Drawer(QFrame):
    def __init__(self, parent=None, width=200):
        super().__init__(parent)
        parent.installEventFilter(self)
        self.setFixedWidth(width)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-left: 2px solid #34495e;
            }
        """)
        self.setGeometry(parent.width(), 0, 300, parent.height())
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.open = False

    def toggle(self):
        self.animation.stop()
        parent_width = self.parent().width()
        parent_height = self.parent().height()
        if self.open:
            endRect = QRect(parent_width, 0, self.width(), parent_height)  # 移出屏幕右边
        else:
            endRect = QRect(parent_width - self.width(), 0, self.width(), parent_height)  # 滑入右边
        self.open = not self.open
        self.animation.setDuration(300)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(endRect)
        self.animation.start()

    def adjust(self):
        if self.open:
            self.setGeometry(self.parent().width() - self.width(), 0, self.width(), self.parent().height())
        else:
            self.setGeometry(-self.width(), 0, self.width(), self.parent().height())
    def eventFilter(self, watched, event):
        if event.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange] and self.open:
            self.adjust()
        return super().eventFilter(watched, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("右侧 QFrame 抽屉示例")
        self.resize(800, 600)

        self.drawer = Drawer(self)

        button = QPushButton("切换抽屉", self)
        button.move(250, 20)
        button.clicked.connect(self.drawer.toggle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

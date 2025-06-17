from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property, Qt
import sys


class AnimatedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._extra_width = 0
        self.setMinimumSize(200, 100)  # 起始宽度200
        self.setStyleSheet("background-color: lightblue;")

    def get(self):
        return self._extra_width

    def set(self, value):
        self._extra_width = value
        self.resize(200 + self._extra_width, self.height())  # 实际改变控件宽度

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor("skyblue"))
        painter.setPen(Qt.NoPen)
        # 根据 enlarge_width 动态绘制更宽的背景
        painter.drawRect(0, 0, self.width() + self._extra_width, self.height())

    property_ = Property(int, get, set)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("宽度动画示例")
        self.resize(300, 200)

        self.animated = AnimatedWidget()
        self.button = QPushButton("切换宽度")

        layout = QVBoxLayout(self)
        layout.addWidget(self.animated)
        layout.addWidget(self.button)

        self.expanded = False
        self.animation = QPropertyAnimation(self.animated, b"property_")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.button.clicked.connect(self.toggle_width)

    def toggle_width(self):
        self.animation.stop()
        if self.expanded:
            self.animation.setStartValue(self.animated.get())
            self.animation.setEndValue(0)
        else:
            self.animation.setStartValue(self.animated.get())
            self.animation.setEndValue(100)
        self.animation.start()
        self.expanded = not self.expanded


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

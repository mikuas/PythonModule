import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QColor, QFont


class CustomTab(QWidget):

    clicked = Signal()

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.setFixedHeight(40)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制背景
        if self.isSelected():
            painter.fillRect(self.rect(), QColor(240, 240, 240))
        else:
            painter.fillRect(self.rect(), QColor(255, 255, 255))

        # 绘制边框
        painter.setPen(QColor(200, 200, 200))
        painter.drawLine(self.rect().topLeft(), self.rect().topRight())
        painter.drawLine(self.rect().bottomLeft(), self.rect().bottomRight())

        # 绘制文本
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(QRect(10, 0, self.width(), self.height()), Qt.AlignVCenter, self.text)

    def isSelected(self):
        return self.parent().currentIndex() == self.parent().tabs.index(self)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        super().mouseReleaseEvent(event)


class CustomTabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.current_index = 0

        self.tab_bar_layout = QHBoxLayout()
        self.tab_bar_widget = QWidget()
        self.tab_bar_widget.setLayout(self.tab_bar_layout)

        self.stacked_widget = QStackedWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_bar_widget)
        layout.addWidget(self.stacked_widget)

    def addTab(self, widget, label):
        tab = CustomTab(label, self)
        self.tabs.append(tab)
        self.tab_bar_layout.addWidget(tab)

        self.stacked_widget.addWidget(widget)

        tab.clicked.connect(self.on_tab_clicked)

    def on_tab_clicked(self):
        clicked_tab = self.sender()
        index = self.tabs.index(clicked_tab)
        self.setCurrentIndex(index)

    def setCurrentIndex(self, index):
        if 0 <= index < len(self.tabs):
            self.current_index = index
            self.stacked_widget.setCurrentIndex(index)

    def currentIndex(self):
        return self.current_index


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Tab Widget Example")

        tab_widget = CustomTabWidget()

        page1 = QWidget()
        page1_layout = QVBoxLayout()
        page1_layout.addWidget(QLabel("Content of Tab 1"))
        page1.setLayout(page1_layout)

        page2 = QWidget()
        page2_layout = QVBoxLayout()
        page2_layout.addWidget(QLabel("Content of Tab 2"))
        page2.setLayout(page2_layout)

        tab_widget.addTab(page1, "Tab 1")
        tab_widget.addTab(page2, "Tab 2")

        layout = QVBoxLayout(self)
        layout.addWidget(tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
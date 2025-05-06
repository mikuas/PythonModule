# coding:utf-8
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 设置边框颜色和宽度
        pen = QPen(Qt.red)  # 设定边框颜色为红色
        pen.setWidth(1)  # 设定边框宽度
        painter.setPen(pen)

        # 绘制边框
        rect = self.rect()  # 获取控件的矩形区域
        rect.adjust(6, 6, -2, -2)  # 调整一下防止边框超出控件范围
        painter.drawRect(rect)


if __name__ == "__main__":
    app = QApplication([])
    widget = CustomWidget()
    widget.show()
    app.exec()

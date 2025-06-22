# coding:utf-8
import sys
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtCore import Qt, QRect, QRectF

from FluentWidgets import TableWidget, TableView, TabItem, SplitWidget, setFont, ImageLabel


def drawBackgroundImage(widget: QWidget, painter: QPainter, rect: Union[QRect, QRectF], image):
    painter = QPainter(widget)
    painter.setRenderHint(QPainter.Antialiasing | QPainter.LosslessImageRendering | QPainter.SmoothPixmapTransform)
    painter.setPen(Qt.NoPen)
    path = QPainterPath()
    path.addRoundedRect(rect, 8, 8)
    painter.setClipPath(path)
    painter.drawImage(rect, image)


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.setMicaEffectEnabled(True)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(5, 35, 5, 0)

        self.tabWidget = TableWidget(self)

        self.tabWidget.setRowCount(100)
        self.tabWidget.setColumnCount(5)

        # 添加表格数据
        # songInfos = [
        #     ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
        #     ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
        #     ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
        # ]
        # for i, songInfo in enumerate(songInfos):
        #     for j in range(5):
        #         self.tabWidget.setItem(i, j, QTableWidgetItem(songInfo[j]))

        for i in range(1, 101):
            for j in range(1, 6):
                item = QTableWidgetItem(f"{i}, {j}")
                item.setTextAlignment(Qt.AlignCenter)
                self.tabWidget.setItem(i - 1, j - 1, item)

        self.tabWidget.setAlternatingRowColors(True)

        setFont(self, 24)

        # 设置水平表头并隐藏垂直表头
        self.tabWidget.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
        self.tabWidget.verticalHeader().hide()

        self.box.addWidget(self.tabWidget)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        for i in range(self.tabWidget.columnCount()):
            self.tabWidget.setColumnWidth(i, self.width() / 5 - 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec())

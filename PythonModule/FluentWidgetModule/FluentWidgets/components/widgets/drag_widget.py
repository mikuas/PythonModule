# coding:utf-8
from PySide6.QtCore import QSize, Signal, QFileInfo, Qt
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QFileDialog, QWidget, QLabel

from ..layout import VBoxLayout
from ...common import setFont
from ..widgets import HyperlinkButton


class DragFolderWidget(QWidget):
    """ get drag folder widget"""
    draggedChange = Signal(list)
    selectionChange = Signal(list)

    def __init__(self, defaultDir="./", isDashLine=False, parent=None):
        super().__init__(parent)
        self._xRadius = 16
        self._yRadius = 16
        self.__lineWidth = 1
        self._defaultDir = defaultDir
        self.__lineColor = QColor("#4AA3EE")
        self.__enableDashLine = isDashLine
        self.vBoxLayout = VBoxLayout(self)
        self.setAcceptDrops(True)
        self.setMinimumSize(QSize(256, 200))

        self.label = QLabel("拖动文件夹到此", self)
        self.orLabel = QLabel("或", self)

        self.button = HyperlinkButton('', "选择文件夹", self)
        for w in [self.button, self.label, self.orLabel]:
            setFont(w, 15)

        self.vBoxLayout.addWidgets([self.label, self.orLabel, self.button])
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button.clicked.connect(self._showDialog)

    def _showDialog(self):
        return self.selectionChange.emit([QFileDialog.getExistingDirectory(self, "选择文件夹", self._defaultDir)])

    def setLabelText(self, text):
        self.label.setText(text)

    def setBorderColor(self, color: str | QColor):
        self.__lineColor = QColor(color)
        self.update()

    def enableDashLine(self, isEnable: bool):
        self.__enableDashLine = isEnable
        self.update()

    def setXRadius(self, radius: int):
        self._xRadius = radius
        self.update()
        return self

    def setYRadius(self, radius: int):
        self._yRadius = radius
        self.update()
        return self

    def setBorderWidth(self, width: int):
        self.__lineWidth = width
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.__lineColor)
        pen.setWidth(self.__lineWidth)
        if self.__enableDashLine:
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setDashPattern([8, 4])
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect().adjust(2, 2, -2, -2), self._xRadius, self._yRadius)

    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        super().dropEvent(event)
        urls = [url.toLocalFile() for url in event.mimeData().urls()]
        dirPath = []
        if urls:
            for url in urls:
                if QFileInfo(url).isDir():
                    dirPath.append(url)
            self.draggedChange.emit(dirPath)
        event.acceptProposedAction()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.orLabel.setContentsMargins(int(self.label.width() / 2.2), 0, 0, 0)


class DragFileWidget(DragFolderWidget):
    """ get dray file widget """
    def __init__(
            self,
            defaultDir="./",
            fileFilter="所有文件 (*.*);; 文本文件 (*.txt)",
            isDashLine=False,
            parent=None
    ):
        """ 多个文件类型用;;分开 """
        super().__init__(defaultDir, isDashLine, parent)
        self.label.setContentsMargins(12, 0, 0, 0)
        self.setLabelText("拖动任意文件到此")
        self.button.setText("选择文件")
        self._fileFilter = fileFilter

    def _showDialog(self):
        return self.selectionChange.emit(
            QFileDialog.getOpenFileNames(self, "选择文件", self._defaultDir, self._fileFilter)[0]
        )

    def dropEvent(self, event):
        urls = [url.toLocalFile() for url in event.mimeData().urls()]
        filePath = []
        if urls:
            for url in urls:
                if not QFileInfo(url).isDir():
                    filePath.append(url)
            self.draggedChange.emit(filePath)
        event.acceptProposedAction()
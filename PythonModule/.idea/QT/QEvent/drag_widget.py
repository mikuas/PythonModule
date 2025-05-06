import sys

from FluentWidgets import VBoxLayout, setFonts
from PySide6.QtCore import QSize, Signal, QFileInfo, Qt
from PySide6.QtWidgets import QWidget, QApplication, QFileDialog, QFrame, QLabel
from qfluentwidgets import setTheme, Theme, HyperlinkButton


class DragFolderWidget(QFrame):
    """ get drag folder widget"""
    draggedChange = Signal(list)
    selectionChange = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = VBoxLayout(self)
        self.setAcceptDrops(True)
        self.setMinimumSize(QSize(256, 200))

        self.label = QLabel("拖动文件夹到此", self)
        self.orLabel = QLabel("或", self)

        self.button = HyperlinkButton('', "选择文件夹", self)
        self.button.setStyleSheet('color: aqua;')
        setFonts([self.button, self.label, self.orLabel], 15)

        self.vBoxLayout.addWidgets([self.label, self.orLabel, self.button])
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button.clicked.connect(self._showDialog)
        self.setBorderColor('skyblue')

    def setBorderColor(self, color: str):
        style = "QLabel {border: none; color: none;}"
        self.setStyleSheet("QFrame {" + f"border: 3px dotted {color}; border-radius: 12px;" + "}" + style)

    def _showDialog(self):
        return self.selectionChange.emit([QFileDialog.getExistingDirectory(self, "选择文件夹")])

    # """ 拖动离开事件 """
    # def dragLeaveEvent(self, event):
    #     super().dragLeaveEvent(event)

    def setLabelText(self, text):
        self.label.setText(text)

    """ 拖动进入事件 """
    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    # """ 拖动移动事件"""
    # def dragMoveEvent(self, event):
    #     super().dragMoveEvent(event)

    """ 拖动放置事件 """
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
    def __init__(self, parent=None, defaultDir="./", fileFilter="所有文件 (*.*);; 文本文件 (*.txt)"):
        """ 多个文件类型用;;分开 """
        super().__init__(parent)
        self.label.setContentsMargins(12, 0, 0, 0)
        self.setLabelText("拖动任意文件到此")
        self.button.setText("选择文件")
        self.defaultDir = defaultDir
        self.fileFilter = fileFilter

    def _showDialog(self):
        return self.selectionChange.emit(QFileDialog.getOpenFileNames(self, "选择文件", self.defaultDir, self.fileFilter)[0])

    def dropEvent(self, event):
        urls = [url.toLocalFile() for url in event.mimeData().urls()]
        filePath = []
        if urls:
            for url in urls:
                if not QFileInfo(url).isDir():
                    filePath.append(url)
            self.draggedChange.emit(filePath)
        event.acceptProposedAction()


class Demo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vLayout = VBoxLayout(self)
        self.dragFolderWidget = DragFolderWidget(self)
        self.dragFileWidget = DragFileWidget(self)
        self.dragFolderWidget.setBorderColor('deeppink')
        self.vLayout.addWidgets([self.dragFolderWidget, self.dragFileWidget])

        self.dragFolderWidget.draggedChange.connect(lambda value: print(f"拖动的文件夹: {value}"))
        self.dragFileWidget.draggedChange.connect(lambda value: print(f"拖动的文件: {value}"))
        self.dragFolderWidget.selectionChange.connect(lambda value: print(f"选择的文件夹: {value}"))
        self.dragFileWidget.selectionChange.connect(lambda value: print(f"选择的文件: {value}"))


# \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \
    """ 拖动放置事件 """
    # def dropEvent(self, event):
    #     super().dropEvent(event)
    #     urls = [url.toLocalFile() for url in event.mimeData().urls()]
    #     dirPath = []
    #     if urls:
    #         for url in urls:
    #             if QFileInfo(url).isDir():
    #                 dirPath.append(url)
    #         self.draggedChange.emit(dirPath)
    #     event.acceptProposedAction()
    #     urls = event.mimeData().urls()
    #     # get file path
    #     if urls:
    #         filePath = [url.toLocalFile() for url in urls]
    #         if QFileInfo(filePath[0]).isDir():
    #             print(f"filePath: {filePath}, This is DIR")
    #             self.button.setText(str(filePath))
    #         else:
    #             InfoBar(
    #                 InfoBarIcon.ERROR,
    #                 '拖入的文件不是文件夹',
    #                 f"FilePath: {filePath[0]}, This is Not DIR",
    #                 isClosable=False,
    #                 duration=2500,
    #                 parent=self
    #             ).show()
    #     event.acceptProposedAction()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    setTheme(Theme.AUTO)
    window.show()
    sys.exit(app.exec())
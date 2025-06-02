# coding:utf-8
import sys

from PIL.ImageDraw2 import Brush
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer

from FluentWidgets import VerticalScrollWidget, DragFileWidget, DragFolderWidget, SplitWidget, BodyLabel, Slider, \
    TitleLabel, ComboBox


class DragWidgetDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False, isAlt=True)
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)

        class Demo(VerticalScrollWidget):
            def __init__(self):
                super().__init__()
                self.enableTransparentBackground()

                # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

                self.dragFile = DragFileWidget(
                    defaultDir='.\\',
                    fileFilter="所有文件(*);; 文本文件 (*.txt)",
                    isDashLine=True,
                    parent=self
                )
                self.dragFolder = DragFolderWidget(
                    defaultDir=".\\",
                    isDashLine=True,
                    parent=self
                )

                self.addWidget(self.dragFile)
                self.addWidget(self.dragFolder)

                self.slider = Slider(Qt.Horizontal, self)
                self.slider.setRange(1, 100)
                self.addWidget(TitleLabel("设置线条宽度"), alignment=Qt.AlignHCenter)
                self.addWidget(self.slider)
                self.slider.valueChanged.connect(lambda value: {
                    self.dragFile.setBorderWidth(value),
                    self.dragFolder.setBorderWidth(value)
                })

                self.addWidget(TitleLabel("设置线条颜色"), alignment=Qt.AlignHCenter)
                self.comboBox = ComboBox(self)
                self.comboBox.addItems([
                    "black",
                    "white",
                    "darkGray",
                    "gray",
                    "lightGray",
                    "red",
                    "green",
                    "blue",
                    "cyan",
                    "magenta",
                    "yellow",
                    "darkRed",
                    "darkGreen",
                    "darkBlue",
                    "darkCyan",
                    "darkMagenta",
                    "darkYellow",
                    "deeppink",
                    "deepskyblue",
                    "pink",
                    "skyblue"
                ])
                self.addWidget(self.comboBox)
                self.comboBox.currentTextChanged.connect(
                    lambda color: {
                        self.dragFile.setBorderColor(color),
                        self.dragFolder.setBorderColor(color)
                    }
                )

                self.fileLabel = BodyLabel("文件\n", self)
                self.fileLabel.setAlignment(Qt.AlignHCenter)
                self.folderLabel = BodyLabel("文件夹\n", self)
                self.folderLabel.setAlignment(Qt.AlignHCenter)

                self.labelLayout = QHBoxLayout()
                self.labelLayout.addWidget(self.fileLabel)
                self.labelLayout.addWidget(self.folderLabel)

                self.addLayout(self.labelLayout)

                self.connectSignalSlot()

            def connectSignalSlot(self):
                self.dragFile.draggedChange.connect(
                    lambda item: {
                        self.fileLabel.setText(self.get(item))
                    }
                )
                self.dragFile.selectionChange.connect(
                    lambda item: {
                        self.fileLabel.setText(self.get(item))
                    }
                )
                self.dragFolder.draggedChange.connect(
                    lambda item: {
                        self.folderLabel.setText(self.get(item, True))
                    }
                )
                self.dragFolder.selectionChange.connect(
                    lambda item: {
                        self.folderLabel.setText(self.get(item, True))
                    }
                )

            def get(self, item, isFolder=False):
                result = "文件夹\n" if isFolder else "文件\n"
                for i in item:
                    result = result + i + '\n'
                return result

        self.box.addWidget(Demo())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DragWidgetDemo()
    window.resize(1200, 720)
    window.show()
    sys.exit(app.exec())

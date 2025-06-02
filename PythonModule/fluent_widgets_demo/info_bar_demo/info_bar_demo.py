# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import InfoBar, InfoBarPosition, PushButton, TitleLabel


class InfoBarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.infoButton = PushButton("info", self)
        self.successButton = PushButton("success", self)
        self.warningButton = PushButton("warning", self)
        self.errorButton = PushButton("error", self)

        self.initLayout()
        self.connectSignalSlot()

    def initLayout(self):
        self.vBoxLayout.addWidget(self.infoButton)
        self.vBoxLayout.addWidget(self.successButton)
        self.vBoxLayout.addWidget(self.warningButton)
        self.vBoxLayout.addWidget(self.errorButton)

    def connectSignalSlot(self):
        self.infoButton.clicked.connect(
            lambda: {
                InfoBar.info(
                    "我是Info信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    Qt.Orientation.Vertical,
                    True,
                    2_5_0_0,
                    InfoBarPosition.TOP_LEFT,
                    self
                )
            }
        )
        self.successButton.clicked.connect(
            lambda: {
                InfoBar.success(
                    "我是Success信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    Qt.Orientation.Vertical,
                    True,
                    2_5_0_0,
                    InfoBarPosition.TOP,
                    self
                )
            }
        )
        self.warningButton.clicked.connect(
            lambda: {
                InfoBar.warning(
                    "我是Warning信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    Qt.Orientation.Horizontal,
                    True,
                    2_5_0_0,
                    InfoBarPosition.TOP_RIGHT,
                    self
                )
            }
        )
        # dv = InfoBar.desktopView()
        # box = QVBoxLayout(dv)
        # box.addWidget(TitleLabel("Hello World"))
        self.errorButton.clicked.connect(
            lambda: {
                InfoBar.error(
                    "我是Error信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    Qt.Orientation.Vertical,
                    True,
                    2000,
                    InfoBarPosition.BOTTOM,
                    self
                ).addWidget(TitleLabel("Hello World"))
                # dv.show()
            }
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InfoBarDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

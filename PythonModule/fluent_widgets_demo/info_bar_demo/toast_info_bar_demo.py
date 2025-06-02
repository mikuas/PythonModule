# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import InfoBar, ToastInfoBarPosition, ToastInfoBar, PushButton, TitleLabel


class InfoBarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.infoButton = PushButton("info", self)
        self.successButton = PushButton("success", self)
        self.warningButton = PushButton("warning", self)
        self.errorButton = PushButton("error", self)
        self.cb1 = PushButton("custom 1", self)
        self.cb2 = PushButton("custom 2", self)

        self.initLayout()
        self.connectSignalSlot()

    def initLayout(self):
        self.vBoxLayout.addWidget(self.infoButton)
        self.vBoxLayout.addWidget(self.successButton)
        self.vBoxLayout.addWidget(self.warningButton)
        self.vBoxLayout.addWidget(self.errorButton)
        self.vBoxLayout.addWidget(self.cb1)
        self.vBoxLayout.addWidget(self.cb2)

    def connectSignalSlot(self):
        self.infoButton.clicked.connect(
            lambda: {
                ToastInfoBar.info(
                    "我是Info信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    2_5_0_0,
                    True,
                    ToastInfoBarPosition.TOP_LEFT,
                    Qt.Orientation.Vertical,
                    parent=self
                )
            }
        )
        self.successButton.clicked.connect(
            lambda: {
                ToastInfoBar.success(
                    "我是Success信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    2_5_0_0,
                    True,
                    ToastInfoBarPosition.TOP_RIGHT,
                    Qt.Orientation.Vertical,
                    parent=self
                )
            }
        )
        self.warningButton.clicked.connect(
            lambda: {
                ToastInfoBar.warning(
                    "我是Warning信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    2_5_0_0,
                    True,
                    ToastInfoBarPosition.BOTTOM_LEFT,
                    Qt.Orientation.Vertical,
                    parent=self
                )
            }
        )
        self.errorButton.clicked.connect(
            lambda: {
                ToastInfoBar.error(
                    "我是Error信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    -1,
                    True,
                    ToastInfoBarPosition.BOTTOM_RIGHT,
                    Qt.Vertical,
                    parent=self
                )
            }
        )
        self.cb1.clicked.connect(
            lambda: {
                ToastInfoBar.custom(
                    "我是Custom信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    position=ToastInfoBarPosition.TOP,
                    parent=self,
                    toastColor='deeppink',
                    backgroundColor=QColor("#43d2a3")
                )
            }
        )
        self.cb2.clicked.connect(
            lambda: {
                ToastInfoBar.custom(
                    "我是Custom信息栏",
                    "这是一段很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长很长的文本",
                    position=ToastInfoBarPosition.BOTTOM,
                    orient=Qt.Orientation.Vertical,
                    parent=self,
                    toastColor='deepskyblue',
                    # backgroundColor=None
                # )
                ).addWidget(TitleLabel("Hello World"))
            }
        )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InfoBarDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

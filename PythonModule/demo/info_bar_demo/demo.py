import sys

from FluentWidgets import Widget, VBoxLayout, ToastInfoBarPosition, ToastInfoBar
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from qfluentwidgets import PushButton, InfoBar

import random


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.layout = VBoxLayout(self)

        self.tb = PushButton('top info bar', self)
        self.tlb = PushButton('top left info bar', self)
        self.trb = PushButton('top right info bar', self)

        self.bb = PushButton('bottom info bar', self)
        self.blb = PushButton('bottom left info bar', self)
        self.brb = PushButton('bottom right info bar', self)

        self.layout.addWidgets([
            self.tb,
            self.tlb,
            self.trb,
            self.bb,
            self.blb,
            self.brb
        ])

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.tb.clicked.connect(
            lambda:
            ToastInfoBar.success(
                self,
                'top',
                f'success info bar {random.randint(0, 100)}',
                5000,
                False,
                ToastInfoBarPosition.TOP,
                width=350
            )
        )
        self.tlb.clicked.connect(
            lambda:
            ToastInfoBar.warning(
                self,
                'top left',
                'warning info bar',
                3000,
                position=ToastInfoBarPosition.TOP_LEFT
            )
        )
        self.trb.clicked.connect(
            lambda:
            ToastInfoBar.info(
                self,
                'top right',
                'info bar',
                500,
                position=ToastInfoBarPosition.TOP_RIGHT
            )
        )
        self.bb.clicked.connect(
            lambda:
            ToastInfoBar.error(
                self,
                'bottom',
                'error info bar',
                position=ToastInfoBarPosition.BOTTOM
            )
        )
        self.blb.clicked.connect(
            lambda:
            ToastInfoBar.custom(
                self,
                'bottom left',
                'custom info bar',
                'skyblue',
                position=ToastInfoBarPosition.BOTTOM_LEFT
            )
        )

        self.brb.clicked.connect(
            lambda:
            ToastInfoBar.custom(
                self,
                'bottom right',
                'custom info bar',
                'deeppink',
                position=ToastInfoBarPosition.BOTTOM_RIGHT,
                # isCustomBgcColor=True,
                # bgcColor='#dff6dd',
                width=500,
                textColor=[QColor('#ECECEC'), QColor('deepskyblue')]
            )
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
# coding:utf-8
import sys
import random

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer

from FluentWidgets import SplitWidget, VerticalScrollWidget, OutlineToolButton, PrimaryPushButton, setTheme, Theme, \
    FluentIcon, setThemeColor, RoundPushButton, TeachingTipView, TeachingTipTailPosition, TeachingTip, isDarkTheme
from FluentWidgets.components.widgets.button import FillPushButton, FillToolButton


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setMicaEffectEnabled(True)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.verWidget = VerticalScrollWidget(self)
        self.box.addWidget(self.verWidget)
        self.verWidget.enableTransparentBackground()
        self.verWidget.boxLayout.setSpacing(24)
        self.buttons = []

        self.button = RoundPushButton("Toggle Theme", self)
        self.button.clicked.connect(
            lambda: {
                setTheme(Theme.LIGHT) if isDarkTheme() else setTheme(Theme.DARK),
                self.setMicaEffectEnabled(True),
                QTimer.singleShot(
                    500,
                    lambda: {
                        # self.setMicaEffectEnabled(False),
                        # [widget.update() for widget in QApplication.allWidgets()]
                        self.updateWidget()
                    }
                ),
                print(True)
            }
        )

        self.verWidget.addWidget(self.button)

        for _ in range(100):
            button = FillPushButton(f"Button {_}", self)
            button.setFixedSize(self.width() / 1.5, 35)
            button.clicked.connect(
                lambda: {
                    TeachingTip.create(
                        self.button,
                        'Gyro Zeppeli',
                        """
                        “触网而起的网球会落到哪一侧，谁也无法知晓。
                        如果那种时刻到来，我希望「女神」是存在的。
                        这样的话，不管网球落到哪一边，我都会坦然接受的吧。”
                        """,
                        image=':/icons/ATRI.jpg',
                        isClosable=True,
                        duration=-1,
                        # tailPosition=TeachingTipTailPosition.NONE,
                        parent=button
                    )
                }
            )
            button.setFillColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.verWidget.addWidget(button, 0, Qt.AlignCenter)
            self.buttons.append(button)

    def updateWidget(self):
        for w in QApplication.allWidgets():
            w.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

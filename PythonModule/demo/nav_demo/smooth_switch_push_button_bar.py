# coding:utf-8

import sys

from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QApplication
from FluentWidgets import Widget, HBoxLayout, VBoxLayout, HorizontalScrollWidget
from qfluentwidgets import FluentIcon, ComboBox, PushButton, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SmoothSwitchBar


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Switch Push Button Bar Bar")
        self.widgetLayout = VBoxLayout(self)
        self.bar = SmoothSwitchBar(self)

        self.texts = []

        self.icons = [
            FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.GAME, FluentIcon.MUSIC, FluentIcon.ADD_TO,
            FluentIcon.MENU, FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.BROOM, FluentIcon.CAR,
            FluentIcon.ASTERISK, FluentIcon.CAFE, FluentIcon.BUS, FluentIcon.CLOSE, FluentIcon.ACCEPT,
            FluentIcon.FLAG, FluentIcon.FOLDER, FluentIcon.DOWN, FluentIcon.RETURN, FluentIcon.CUT,
            FluentIcon.MUTE, FluentIcon.MAIL, FluentIcon.SCROLL, FluentIcon.SEARCH, FluentIcon.HELP,
            FluentIcon.HOME_FILL, FluentIcon.SEND, FluentIcon.PLAY, FluentIcon.WIFI, FluentIcon.SETTING
        ]

        for text in self.icons:
            self.texts.append(str(text).split('.')[-1])

        for text, icon in zip(self.texts, self.icons):
            self.bar.addItem(text, text, icon)

        for i in range(int(len(self.texts) / 5) + 1):
            self.bar.insertSeparator(i * (5 + 1)).setSeparatorColor('deeppink')

        self.bar.setItemSelectedColor('deepskyblue')
        self.bar.setSmoothLineColor('deepskyblue')
        self.bar.setCurrentWidget('HOME')

        self.title = TitleLabel("Selected Current RouteKey", self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("Widget RouteKey")
        self.comboBox.addItems(list(self.bar.getAllWidget().keys()))

        self.btn = PushButton("Set Current Widget Is HOME", self)
        self.btn.clicked.connect(self.updateWidget)

        self.comboBox.currentIndexChanged.connect(
            lambda: self.btn.setText(f"Set Current Widget Is {self.comboBox.currentText()}")
        )

        self.currentTitle = TitleLabel(self)
        self.currentBtn = PushButton("Get Current Widget RouteKey", self)
        self.currentBtn.clicked.connect(self.updateCurrent)

        self.widgetLayout.addWidget(self.bar)
        self.widgetLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.widgetLayout.addWidgets([self.comboBox, self.btn, self.currentBtn])
        self.widgetLayout.addWidget(self.currentTitle, alignment=Qt.AlignmentFlag.AlignHCenter)

    def updateCurrent(self):
        w = self.bar.getCurrentWidget()
        routeKey = [key for key, value in self.bar.getAllWidget().items() if w == value]
        self.currentTitle.setText(f'Current RouteKey is "{routeKey[0]}"')

    def updateWidget(self):
        self.bar.setCurrentWidget(self.comboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
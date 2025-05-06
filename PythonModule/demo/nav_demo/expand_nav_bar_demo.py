# coding:utf-8

import sys

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication
from FluentWidgets import Widget, HBoxLayout, VBoxLayout
from qfluentwidgets import FluentIcon, ComboBox, PushButton, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import ExpandNavigationBar, NavigationItemPosition


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expand NavWidget Bar")
        self.widgetLayout = HBoxLayout(self)
        self.box = VBoxLayout()
        self.bar = ExpandNavigationBar(self)
        self.bar.enableReturnButton(True)

        self.widgetLayout.addWidget(self.bar)
        self.widgetLayout.addLayout(self.box)

        self.icons = [
            FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.GAME, FluentIcon.MUSIC, FluentIcon.ADD_TO,
            FluentIcon.MENU, FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.BROOM, FluentIcon.CAR,
            FluentIcon.ASTERISK, FluentIcon.CAFE, FluentIcon.BUS, FluentIcon.CLOSE, FluentIcon.ACCEPT,
            FluentIcon.FLAG, FluentIcon.FOLDER, FluentIcon.DOWN, FluentIcon.RETURN, FluentIcon.CUT,
            FluentIcon.MUTE, FluentIcon.MAIL, FluentIcon.SCROLL, FluentIcon.SEARCH, FluentIcon.HELP,
            FluentIcon.HOME_FILL, FluentIcon.SEND, FluentIcon.PLAY, FluentIcon.WIFI, FluentIcon.SETTING
        ]

        self.topTexts = []
        self.scrollText = []
        self.bottomText = []

        for text in self.icons[:5]:
            self.topTexts.append(str(text).split('.')[-1])
        print(f"Top Texts {self.topTexts}")

        for text in self.icons[5:25]:
            self.scrollText.append(str(text).split('.')[-1])
        print(f"Scroll Texts {self.scrollText}")

        for text in self.icons[25:]:
            self.bottomText.append(str(text).split('.')[-1])
        print(f"bottomText Texts {self.bottomText}")

        # add to scroll
        for text, icon in zip(self.topTexts, self.icons[:5]):
            self.bar.addItem(text, icon, text, position=NavigationItemPosition.TOP)
        self.bar.addSeparator()

        # add to top
        for text, icon in zip(self.scrollText, self.icons[5:25]):
            self.bar.addItem(text, icon, text)

        # add to bottom
        self.bar.addSeparator(NavigationItemPosition.BOTTOM)
        for text, icon in zip(self.bottomText, self.icons[25:]):
            self.bar.addItem(text, icon, text, position=NavigationItemPosition.BOTTOM)

        self.bar.setCurrentWidget("HOME")

        self.title = TitleLabel("Selected Current RouteKey", self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("Widget RouteKey")
        self.comboBox.addItems(list(self.bar.getAllWidget().keys()))

        self.btn = PushButton("Set Current Widget Is HOME", self)
        self.btn.clicked.connect(self.updateWidget)

        self.comboBox.currentIndexChanged.connect(
            lambda: self.btn.setText(f"Set Current Widget Is {self.comboBox.currentText()}")
        )

        self.currentBtn = PushButton("Get Current Widget RouteKey", self)
        self.currentBtn.clicked.connect(self.updateCurrent)
        self.currentTitle = TitleLabel(self)

        self.box.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.box.addWidgets([self.comboBox, self.btn, self.currentBtn])
        self.box.addWidget(self.currentTitle, alignment=Qt.AlignmentFlag.AlignHCenter)

    def updateCurrent(self):
        w = self.bar.getCurrentWidget()
        routeKey = [key for key, value in self.bar.getAllWidget().items() if w == value]
        self.currentTitle.setText(f'Current RouteKey is "{routeKey[0]}"')

    def updateWidget(self):
        self.bar.setCurrentWidget(self.comboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(1000, 520)
    window.show()
    sys.exit(app.exec())
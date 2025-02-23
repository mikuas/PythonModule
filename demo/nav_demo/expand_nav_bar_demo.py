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

        # add to scroll
        self.bar.addItem(
            "HOME", FluentIcon.HOME, "HOME", True
        )
        self.bar.addItem(
            "ABOUT", FluentIcon.ALBUM, "ABOUT", True
        )
        self.bar.addItem(
            "GITHUB", FluentIcon.GITHUB, "GITHUB", True
        )
        self.bar.addItem(
            "VIDEO", FluentIcon.VIDEO, "VIDEO", True
        )
        self.bar.addItem(
            "GAME", FluentIcon.GAME, "GAME", True
        )
        self.bar.addItem(
            "SEND", FluentIcon.SEND, "SEND", True
        )
        self.bar.addItem(
            "SAVE", FluentIcon.SAVE, "SAVE", True
        )

        # add to top
        self.bar.addItem(
            "MUSIC", FluentIcon.MUSIC, "MUSIC", position=NavigationItemPosition.TOP
        )
        self.bar.addItem(
            "SETTING", FluentIcon.SETTING, "SETTING", position=NavigationItemPosition.TOP
        )
        self.bar.addItem(
            "WIFI", FluentIcon.WIFI, "WIFI", position=NavigationItemPosition.TOP
        )
        self.bar.addSeparator(NavigationItemPosition.TOP).setSeparatorColor('deepskyblue')

        # add to bottom
        self.bar.addSeparator(NavigationItemPosition.BOTTOM).setSeparatorColor('deeppink')
        self.bar.addItem(
            "LINK", FluentIcon.LINK, "LINK", position=NavigationItemPosition.BOTTOM
        )
        self.bar.addItem(
            "FOLDER", FluentIcon.FOLDER, "FOLDER", position=NavigationItemPosition.BOTTOM
        )
        self.bar.addItem(
            "EDIT", FluentIcon.EDIT, "EDIT", position=NavigationItemPosition.BOTTOM
        )

        # self.bar.setCurrentWidget("HOME")

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
        # self.currentBtn.clicked.connect()
        self.currentTitle = TitleLabel(self)

        self.box.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.box.addWidgets([self.comboBox, self.btn, self.currentBtn])
        self.box.addWidget(self.currentTitle, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.box.setAlignment(Qt.AlignmentFlag.AlignTop)

    def updateCurrent(self):
        # self.title.setText(self.box.get)
        pass

    def updateWidget(self):
        self.bar.setCurrentWidget(self.comboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
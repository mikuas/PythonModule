# coding:utf-8

import sys

from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QApplication
from FluentWidgets import Widget, HBoxLayout, VBoxLayout
from qfluentwidgets import FluentIcon, ComboBox, PushButton, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SmoothSwitchToolButtonBar, SmoothSwitchSeparator


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Switch Tool Button Bar Bar")
        self.widgetLayout = VBoxLayout(self)
        self.bar = SmoothSwitchToolButtonBar(self)

        # add to scroll
        self.bar.addItem(
            "HOME", FluentIcon.HOME
        )
        self.bar.addItem(
            "ABOUT", FluentIcon.ALBUM
        )
        self.bar.addItem(
            "GITHUB", FluentIcon.GITHUB
        )
        self.bar.addItem(
            "VIDEO", FluentIcon.VIDEO
        )
        self.bar.addItem(
            "GAME", FluentIcon.GAME
        )
        self.bar.addItem(
            "SEND", FluentIcon.SEND
        )
        self.bar.addItem(
            "SAVE", FluentIcon.SAVE
        )

        # add to top
        self.bar.addItem(
            "MUSIC", FluentIcon.MUSIC
        )
        self.bar.addItem(
            "SETTING", FluentIcon.SETTING)
        self.bar.addItem(
            "WIFI", FluentIcon.WIFI)
        self.bar.addSeparator().setSeparatorColor('deepskyblue')

        # add to bottom
        self.bar.addItem(
            "LINK", FluentIcon.LINK)
        self.bar.addItem(
            "FOLDER", FluentIcon.FOLDER)
        self.bar.addItem(
            "EDIT", FluentIcon.EDIT)

        self.bar.setItemSelectedColor('deeppink')
        self.bar.setSmoothLineColor('deeppink')
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

        self.widgetLayout.addWidget(self.bar, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.widgetLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.widgetLayout.addWidgets([self.comboBox, self.btn])
        self.widgetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def updateWidget(self):
        self.bar.setCurrentWidget(self.comboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
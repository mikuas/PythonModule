# coding:utf-8

import sys

from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QApplication
from FluentWidgets import Widget, HBoxLayout, VBoxLayout, HorizontalScrollWidget
from qfluentwidgets import FluentIcon, ComboBox, PushButton, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import SmoothSwitchPushButtonBar, SmoothSwitchSeparator


class Window(Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smooth Switch Push Button Bar Bar")
        self.widgetLayout = VBoxLayout(self)
        self.bar = SmoothSwitchPushButtonBar(self)

        # add to scroll
        self.bar.addItem(
            "HOME", "HOME", FluentIcon.HOME, isSelected=True
        )
        self.bar.addItem(
            "ABOUT", "ABOUT", FluentIcon.ALBUM, isSelected=True
        )
        self.bar.addItem(
            "GITHUB", "GITHUB", FluentIcon.GITHUB, isSelected=True
        )
        self.bar.addItem(
            "VIDEO", "VIDEO", FluentIcon.VIDEO, isSelected=True
        )
        self.bar.addItem(
            "GAME", "GAME", FluentIcon.GAME, isSelected=True
        )
        self.bar.addItem(
            "SEND", "SEND", FluentIcon.SEND, isSelected=True
        )
        self.bar.addItem(
            "SAVE", "SAVE", FluentIcon.SAVE, isSelected=True
        )

        # add to top
        self.bar.addItem(
            "MUSIC", "MUSIC", FluentIcon.MUSIC
        )
        self.bar.addItem(
            "SETTING", "SETTING", FluentIcon.SETTING)
        self.bar.addItem(
            "WIFI", "WIFI", FluentIcon.WIFI)
        self.bar.addSeparator().setSeparatorColor('deepskyblue')

        # add to bottom
        self.bar.addItem(
            "LINK", "LINK", FluentIcon.LINK)
        self.bar.addItem(
            "FOLDER", "FOLDER", FluentIcon.FOLDER)
        self.bar.addItem(
            "EDIT", "EDIT", FluentIcon.EDIT)

        self.bar.setItemSelectedColor('deeppink')
        self.bar.setSmoothLineColor('deeppink')

        self.title = TitleLabel("Selected Current RouteKey", self)

        self.comboBox = ComboBox(self)
        self.comboBox.setPlaceholderText("Widget RouteKey")
        self.comboBox.addItems(list(self.bar.getAllWidget().keys()))

        self.btn = PushButton("Set Current Widget Is HOME", self)
        self.btn.clicked.connect(self.updateWidget)

        self.comboBox.currentIndexChanged.connect(
            lambda: self.btn.setText(f"Set Current Widget Is {self.comboBox.currentText()}")
        )

        self.widgetLayout.addWidget(self.bar)
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
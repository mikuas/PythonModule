# coding:utf-8
import sys

from PySide6.QtCore import Qt

from PythonModule.FluentWidgetModule.FluentWidgets import Widget, SmoothSwitchBar, VBoxLayout, PushButton, \
    setTheme, theme, FluentIcon, HorizontalSeparator, Theme

from PySide6.QtWidgets import QApplication


class Window(Widget):
    def __init__(self):
        super().__init__()

        self.box = VBoxLayout(self)
        self.nav = SmoothSwitchBar(self)

        self.icons = [
            FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.GAME, FluentIcon.MUSIC, FluentIcon.ADD_TO,
            FluentIcon.MENU, FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.BROOM, FluentIcon.CAR,
            FluentIcon.ASTERISK, FluentIcon.CAFE, FluentIcon.BUS, FluentIcon.CLOSE, FluentIcon.ACCEPT,
            FluentIcon.FLAG, FluentIcon.FOLDER, FluentIcon.DOWN, FluentIcon.RETURN, FluentIcon.CUT,
            FluentIcon.MUTE, FluentIcon.MAIL, FluentIcon.SCROLL, FluentIcon.SEARCH, FluentIcon.HELP,
            FluentIcon.HOME_FILL, FluentIcon.SEND, FluentIcon.PLAY, FluentIcon.WIFI, FluentIcon.SETTING
        ]

        for item in self.icons:
            self.nav.addSeparator()
            self.nav.addItem(str(item)[11:], str(item)[11:])

        self.nav.addSeparator()
        self.nav.addItem('1', '', FluentIcon.HOME)

        self.cbtn = PushButton('color', self)
        self.cbtn.clicked.connect(lambda: self.nav.setSlideLineColor('red'))

        self.wbttn = PushButton('width__128', self)
        self.wbttn.clicked.connect(lambda: self.nav.setSlideLineWidth(128))

        self.nav.setCurrentWidget('MUSIC')

        # self.nav.setItemBackgroundColor('deeppink', 'deeppink')

        self.box.addWidget(self.nav)
        # self.nav.setBarAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.box.addWidget(HorizontalSeparator(self))
        self.box.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.box.addWidget(self.cbtn, alignment=Qt.AlignmentFlag.AlignBottom)
        self.box.addWidget(self.wbttn, alignment=Qt.AlignmentFlag.AlignBottom)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
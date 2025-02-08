import sys

from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import InfoBar, PushButton, ToggleButton, FluentIcon, TitleLabel

from PythonModule.FluentWidgetModule.FluentWidgets import (
    VBoxLayout, Widget,
    NavigationButton, NavigationWidget,
    NavigationBar, SideNavigationWidget
)

class Window(Widget):
    def __init__(self):
        super().__init__()
        self.layout = VBoxLayout(self)

        self.w = NavigationWidget(True, self)
        self.bw = NavigationButton(FluentIcon.GITHUB, 'title', True, self)
        self.n = NavigationBar(self)
        self.sn = SideNavigationWidget(self)

        self.n.addWidget(
            '1',
            NavigationButton(FluentIcon.HOME, 'HOME', parent=self),
        )
        self.n.addWidget(
            '2',
            NavigationButton(FluentIcon.SETTING, 'SETTING', parent=self),
        )

        self.sn.addSubInterface(
            'n1',
            'HOME',
            FluentIcon.HOME,
            TitleLabel("HOME INTERFACE", self)
        ).addSubInterface(
            'n2',
            'SETTING',
            FluentIcon.SETTING,
            TitleLabel("SETTING INTERFACE", self)
        )
        self.sn.insertSeparator(1)
        self.sn.setCurrentWidget('n1')
        self.sn.setDarkBackgroundColor('deeppink')
        for w in self.sn.navigationBar.getAllWidget().values():
            w.setSelectedColor('red')

        self.layout.addWidget(self.w)
        self.layout.addWidget(self.bw)
        self.layout.addWidget(self.n)
        self.layout.addWidget(self.sn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
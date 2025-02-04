# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon, TitleLabel

from FluentWidgets import SideNavigationWidget, NavigationItemPosition, LabelBarWidget, SegmentedNav, SegmentedToolNav, PivotNav


class NavigationDemo(SegmentedNav):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.addSubInterface(
            'HOME',
            "HOME",
            TitleLabel("HOME", self),
            FluentIcon.HOME,
        )
        self.addSubInterface(
            "GITHUB",
            "GITHUB",
            TitleLabel("GITHUB", self),
            FluentIcon.GITHUB,
        )

        self.addSubInterface(
            "SETTING",
            "SETTING",
            TitleLabel("SETTING", self),
            FluentIcon.SETTING,
        )
        self.addSubInterface(
            "ABOUT",
            "ABOUT",
            TitleLabel("ABOUT", self),
            FluentIcon.INFO
        )
        self.addSubInterface(
            "MUSIC",
            "MUSIC",
            TitleLabel("MUSIC", self),
            FluentIcon.MUSIC
        ).setCurrentItem('HOME')

        # self.insertNavSeparator(1)
        # self.insertNavSeparator(3)
        # self.insertNavSeparator(5)
        # self.insertNavSeparator(7)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NavigationDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
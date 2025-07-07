# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt

from FluentWidgets import TopNavigationWindow, FluentIcon, setTheme, Theme, theme, isDarkTheme

from list_widget_interface.list_widget_interface import ListWidgetInterface
from settings_interface.setting_interface import SettingInterface

import resources


class MainWindow(TopNavigationWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:transparent;")

        self.setMicaEffectEnabled(True)
        self.setWindowIcon(QIcon("./files/icons/Honkai_Star_Rail.ico"))
        self.setWindowTitle("MyAppDemo")
        self.themes = {
            "亮色": Theme.LIGHT,
            "暗色": Theme.DARK,
            "自动": Theme.AUTO
        }

        self.listWidgetInterface = ListWidgetInterface(self)
        self.settingsInterface = SettingInterface(self)

        self.initNavigation()
        self.connectSignalSlot()

    def initNavigation(self):
        self.addSubInterface(
            "list_widget_interface",
            "列表",
            self.listWidgetInterface
        )

        self.navigation.addStretch(1)
        self.addSubInterface(
            "setting_interface",
            "",
            self.settingsInterface,
            FluentIcon.SETTING,
            toolTip="SettingInterface"
        )
        self.setCurrentIndex(0)

    def updateWidgetTheme(self, button):
        setTheme(self.themes[button.text()])
        if isDarkTheme():
            self.stackedWidget.setStyleSheet("background-color: #26262e")
        else:
            self.stackedWidget.setStyleSheet("background-color: #f7f9fc")

        self.setMicaEffectEnabled(True)
        for w in QApplication.allWidgets():
            print(w)
            try:
                w.update()
            except TypeError:
                w.update(w.currentIndex())

    def connectSignalSlot(self):
        self.settingsInterface.buttonGroup.buttonToggled.connect(self.updateWidgetTheme)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication
from FluentWidgets import SideNavWidget, NavigationItemPosition, VBoxLayout
from qfluentwidgets import FluentIcon, FluentTranslator

from PythonModule.FluentWidgetModule.FluentWidgets import MicaWidget
from drag_widget_interface import DragWidgetInterface
from drawer_widget_interface import DrawerWidgetInterface
from info_bar_widget_interface import InfoBarWidgetInterface
from setting_interface import SettingInterface


class MainWindow(SideNavWidget):
    def __init__(self):
        super().__init__()
        self.enableReturnButton(True)
        self.dragWidget = DragWidgetInterface(self)
        self.drawerWidget = DrawerWidgetInterface(self)
        self.infoBarWidget = InfoBarWidgetInterface(self)

        self.settingWidget = SettingInterface(self)

        self.__initSubInterface()

        self.setCurrentWidget('dragWidget')

    def __initSubInterface(self):
        self.addSubInterface(
            "dragWidget",
            "Drag Widget Interface",
            self.dragWidget,
            FluentIcon.HOME
        )
        self.addSubInterface(
            "drawerWidget",
            "Drawer Widget Interface",
            self.drawerWidget,
            FluentIcon.GITHUB
        )
        self.addSubInterface(
            "infoBarWidget",
            "Info Bar Widget Interface",
            self.infoBarWidget,
            FluentIcon.INFO
        )

        self.addSeparator(NavigationItemPosition.BOTTOM).setSeparatorColor('deeppink')
        self.addSubInterface(
            "SettingWidget",
            "Setting Interface",
            self.settingWidget,
            FluentIcon.SETTING,
            NavigationItemPosition.BOTTOM
        )

        self.navigationBar.setStyleSheet(
            """
            background: transparent;
            """
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = FluentTranslator()
    app.installTranslator(translator)
    window = MainWindow()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())
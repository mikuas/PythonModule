# coding:utf-8
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication
from FluentWidgets import SideNavigationWidget, Widget
from qfluentwidgets import FluentIcon, TitleLabel, Action

from menu import RoundMenu, AcrylicRoundMenu, ProfileCardMenu, AcrylicProfileCardMenu, CheckedMenu, AcrylicCheckedMenu


class Window(SideNavigationWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu = AcrylicProfileCardMenu(r"C:\Users\Administrator\OneDrive\Pictures\1734703508871.jpg", 'name', 'email', 'homepage', 'https://www.bilibili.com', self)
        self.menu = CheckedMenu(parent=self)
        self.menuWidget1 = SubWidget(
            self, "Menu Widget1",
            self.menu
        )
        self.menuWidget2 = SubWidget(
            self, 'Menu Widget2',
            self.menu
        )

        self.initNavigation()

        self.items = []
        self.icons = [FluentIcon.HOME, FluentIcon.GITHUB, FluentIcon.SETTING, FluentIcon.COPY, FluentIcon.CUT, FluentIcon.PASTE]
        self.texts = ['home', 'github', 'setting', 'copy', 'cut', 'past']

        for i in range(len(self.icons)):
            if i == 3:
                self.menu.addSeparator()
            self.items.append(self.menu.addItem(self.icons[i], self.texts[i], self))

        self.menu.addAction(Action(
            icon=FluentIcon.ADD,
            text='Add To',
            parent=self,
            triggered=lambda: print('Add To',),
            shortcut='ctrl+b'
        ))

        print(self.items)
        self.shorts = ['ctrl+h', 'ctrl+g', 'ctrl+s', 'ctrl+c', 'ctrl+v', 'ctrl+x']
        self.functions = [lambda: print('ctrl+h'), lambda: print('ctrl+g'), lambda: print('ctrl+s'), lambda: print('ctrl+c'), lambda: print('ctrl+v'), lambda: print('ctrl+x')]
        for item, key, func in zip(self.items, self.shorts, self.functions):
            self.menu.setShortcut(item, key)
            self.menu.setClickedSlot(item, func)

        for item in self.navigationBar.getAllWidget().values():
            item.setSelectedColor('orange')

        self.menu.addToGroup(self.menu.actions()[:3])

    def initNavigation(self):
        self.addSubInterface(
            'menu1',
            'Menu',
            FluentIcon.APPLICATION,
            self.menuWidget1
        )
        self.addSubInterface(
            'menu2',
            'Menu',
            FluentIcon.GITHUB,
            self.menuWidget2
        )
        self.setCurrentWidget('menu2')


class SubWidget(Widget):
    def __init__(self, parent=None, text=None, menu=None):
        super().__init__(parent)
        TitleLabel(text, self)
        self.menu = menu

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        # self.menu.centerExec(self)
        self.menu.exec(event.globalPos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
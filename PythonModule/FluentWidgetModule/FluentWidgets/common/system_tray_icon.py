# coding:utf-8
from typing import List

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QSystemTrayIcon
from ..components import SystemTrayMenu
from .icon import Action, FluentIconBase, Icon


class SystemTrayIcon(QSystemTrayIcon):
    """ 系统托盘图标 """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.menu = SystemTrayMenu(parent=parent)
        self.setContextMenu(self.menu)

    def setIcon(self, icon: str | QIcon | FluentIconBase):
        super().setIcon(Icon(icon))
        return self

    def addAction(self, action: QAction | Action):
        self.menu.addAction(action)
        return self

    def addActions(self, actions: List[QAction] | List[QAction]):
        self.menu.addActions(actions)
# coding:utf-8
from typing import Union, List

from PySide6.QtGui import QColor, QActionGroup, QIcon, QShortcut, QKeySequence, QAction
from PySide6.QtWidgets import QWidget
from qfluentwidgets import (
    RoundMenu as RM, Action, AvatarWidget, BodyLabel, CaptionLabel, setFont, HyperlinkButton, CheckableMenu as CM,
    MenuIndicatorType, FluentIconBase, MenuAnimationType
)
from qfluentwidgets.components.material import AcrylicMenu as AM, AcrylicCheckableMenu as ACM


class MenuBase:

    def addItem(self, icon: Union[QIcon, str, FluentIconBase], text: str, parent: QWidget = None):
        """ add item to menu"""
        action = Action(icon, text, parent=parent)
        self.addAction(action)
        return action

    def addItems(self, icon: List[Union[QIcon, str, FluentIconBase]], text: List[str], parent: QWidget = None):
        """ add items to menu """
        actions = []
        for icon, text in zip(icon, text):
            actions.append(self.addItem(icon, text, parent))
        return actions

    def setMenuMinWidth(self, width: int):
        self.setMinimumWidth(width)
        self.view.setMinimumWidth(width - 20)
        return self

    def setClickedSlot(self, action: Action, func):
        """ set click method """
        action.triggered.connect(func)
        return self

    def setShortcut(self, action: Action, key: str):
        """ set shortcut """
        action.setShortcut(QKeySequence(key))
        return self

    def centerExec(self, widget: QWidget, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        self.exec(widget.mapToGlobal(widget.rect().center()), ani, aniType)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class RoundMenu(MenuBase, RM):
    """ 菜单栏组件 """
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setMenuMinWidth(160)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicRoundMenu(MenuBase, AM):
    """ 亚力克菜单 """
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setMenuMinWidth(160)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class ProfileCardMenu(RoundMenu):
    """ 个人信息卡片组件 """
    def __init__(
            self,
            avatarPath: str,
            name: str,
            email: str,
            buttonText='主页',
            url='',
            parent=None
    ):
        super().__init__(parent)
        self._widget = QWidget()
        self._widget.setFixedSize(307, 82)
        self.addWidget(self._widget)
        self.addSeparator()
        self.__initCard(avatarPath, name, email, buttonText, url)

    def __initCard(self, avatarPath: str, name: str, email: str, buttonText: str, url: str = ''):
        self._avatar = AvatarWidget(avatarPath, self._widget)
        self._nameLabel = BodyLabel(name, self._widget)
        self._emailLabel = CaptionLabel(email, self._widget)
        self._button = HyperlinkButton(url, buttonText, self._widget)

        self._emailLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))
        self.setButtonFontSize(13)

        self.setAvatarRadius(24)
        self._avatar.move(3, 16)
        self._nameLabel.move(64, 13)
        self._emailLabel.move(64, 32)
        self._button.move(52, 48)

    def setButtonFontSize(self, size: int):
        setFont(self._button, size)
        return self

    def setAvatarMove(self, x: int, y: int):
        self._avatar.move(x, y)
        return self

    def setAvatarRadius(self, radius: int):
        self._avatar.setRadius(radius)
        return self

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicProfileCardMenu(ProfileCardMenu, AM):
    """ 亚力克个人信息卡片组件 """
    def __init__(self, avatarPath, name, email, buttonText="主页", url='', parent=None):
        super().__init__(avatarPath, name, email, buttonText, url, parent)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class CheckedMenuBase(MenuBase):

    def addItem(self, icon: Union[QIcon, str, FluentIconBase], text: str, parent: QWidget = None):
        action = Action(icon, text, checkable=True, parent=parent)
        self.addAction(action)
        return action

    def addItems(self, icon: List[Union[QIcon, str, FluentIconBase]], text: List[str], parent: QWidget = None):
        actions = []
        for i, t in zip(icon, text):
            actions.append(self.addItem(i, t, parent))
        return actions

    def addToGroup(self, actions: List[Action | QAction]):
        for item in actions:
            self._actionGroup.addAction(item)


class CheckedMenu(CheckedMenuBase, CM):
    """ 可选中菜单栏 """
    def __init__(self, title="", parent=None, indicatorType: MenuIndicatorType = MenuIndicatorType.CHECK):
        super().__init__(title, parent, indicatorType)
        self.setMenuMinWidth(160)
        self._actionGroup = QActionGroup(self)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class AcrylicCheckedMenu(CheckedMenuBase, ACM):
    def __init__(self, title="", parent=None, indicatorType: MenuIndicatorType = MenuIndicatorType.CHECK):
        super().__init__(title, parent, indicatorType)
        self._actionGroup = QActionGroup(self)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)


class Shortcut:
    """ 设置快捷键 """
    def addShortcut(self, key: str, parent: QWidget, function):
        """ set shortcut """
        shortcut = QShortcut(QKeySequence(key), parent)
        shortcut.activated.connect(function)
        return self

    def addShortcuts(self, keys: List[str], parent: QWidget, functions: List):
        for key, fc in zip(keys, functions):
            self.addShortcut(key, parent, fc)
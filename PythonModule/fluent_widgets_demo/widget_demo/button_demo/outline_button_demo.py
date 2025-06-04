# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QButtonGroup, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, OutlinePushButton, OutlineToolButton, ImageLabel, SwitchButton, FluentIcon, \
    TitleLabel, \
    ColorDialog, themeColor, PrimaryPushButton

import images_resources


class OutlineButtonDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OutlineButtonDemo")
        self.setWindowIcon(QIcon(":/images/genshin.ico"))
        self.windowEffect.setMicaEffect(self.winId(), isAlt=True)

        self.mainLayout = QHBoxLayout(self)
        self.imageLabel = ImageLabel(":/images/xier.jpg", self)
        self.imageLabel.setFixedSize(self.width() / 2.5, self.height())
        self.mainLayout.addWidget(self.imageLabel, 0, Qt.AlignLeft)

        self.widgetLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.widgetLayout, 1)
        self.widgetLayout.setContentsMargins(0, 50, 10, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.initOutlineButton()

        self.button = PrimaryPushButton("设置OutlineButton边框颜色", self)
        self.selectedAllButton = PrimaryPushButton("选择全部按钮", self)
        self.colorDialog = ColorDialog(themeColor(), '设置OutlineButton边框颜色', self)

        self.colorDialog.hide()

        self.button.clicked.connect(self.colorDialog.show)
        self.selectedAllButton.clicked.connect(self.selectedAll)
        self.colorDialog.colorChanged.connect(self.updateButtonColor)

        self.widgetLayout.addWidget(self.button, 1, Qt.AlignTop)
        self.widgetLayout.addWidget(self.selectedAllButton, 1, Qt.AlignTop)

    def selectedAll(self):
        if self.buttonGroup.exclusive():
            return
        for button in self.buttonGroup.buttons():
            button.setChecked(True)

    def updateButtonColor(self, color):
        for button in self.buttonGroup.buttons():
            button.setOutlineColor(color)

    def initOutlineButton(self):
        self.buttonGroup = QButtonGroup(self)

        for i in range(3):
            layout = QHBoxLayout()
            items = ["Home", "Music",  "Game", "GitHub", "Settings"]
            icons = [FluentIcon.HOME, FluentIcon.MUSIC, FluentIcon.GAME, FluentIcon.GITHUB, FluentIcon.SETTING]
            for item, icon in zip(items, icons):
                match i:
                    case 0:
                        button = OutlinePushButton(icon, self, item)
                    case 1:
                        button = OutlinePushButton(item, self)
                    case 2:
                        button = OutlineToolButton(icon, self)
                self.buttonGroup.addButton(button)
                layout.addWidget(button)
            self.widgetLayout.addLayout(layout, 1)

        self.buttonGroup.setExclusive(False)
        self.switch = SwitchButton(self)
        switchLayout = QHBoxLayout()
        switchLayout.addWidget(TitleLabel("启用单选"), 1, Qt.AlignHCenter | Qt.AlignTop)
        switchLayout.addWidget(self.switch, 1, Qt.AlignHCenter | Qt.AlignTop)
        self.widgetLayout.addLayout(switchLayout)
        self.switch.checkedChanged.connect(self.updateButtonGroup)

    def updateButtonGroup(self, exclusive):
        self.buttonGroup.setExclusive(exclusive)
        if exclusive:
            for button in self.buttonGroup.buttons():
                button.setChecked(False)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.titleBar.raise_()
        self.imageLabel.setFixedSize(self.width() / 2.5, self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OutlineButtonDemo()
    window.setMinimumSize(800, 520)
    window.show()
    sys.exit(app.exec())

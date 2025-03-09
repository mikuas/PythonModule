# coding:utf-8
from PySide6.QtCore import Qt, QEvent
from FluentWidgets import (
    TopPopDrawerWidget, RightPopDrawerWidget, BottomPopDrawerWidget, LeftPopDrawerWidget,
    Widget, VBoxLayout
)
from qfluentwidgets import PrimaryPushButton, ComboBox, TitleLabel


class DrawerWidgetInterface(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.box = VBoxLayout(self)

        self.topDrawer = TopPopDrawerWidget(self, "顶部弹出抽屉")
        self.rightDrawer = RightPopDrawerWidget(self, "右侧弹出抽屉")
        self.bottomDrawer = BottomPopDrawerWidget(self, "底部弹出抽屉")
        self.leftDrawer = LeftPopDrawerWidget(self, "左侧弹出抽屉")

        self.items = [self.topDrawer, self.rightDrawer, self.bottomDrawer, self.leftDrawer]

        for item in self.items:
            item.addWidget(self.createTitle("选择背景颜色"), alignment=Qt.AlignmentFlag.AlignHCenter)
            item.addWidget(self.createComboBox(['pink', 'aqua', 'deeppink', 'deepskyblue', 'blue', 'green'], item))
            item.addWidget(self.createTitle("选择大小"), alignment=Qt.AlignmentFlag.AlignHCenter)
            item.addWidget(self.createComboBox(['100', '200', '300', '400', '500'], item, 1))
            item.addWidget(self.createTitle("选择动画过度时间"), alignment=Qt.AlignmentFlag.AlignHCenter)
            item.addWidget(self.createComboBox(['100', '500', '800', '1000', '1500'], item, 2))

        self.topButton = PrimaryPushButton("弹出顶部抽屉", self)
        self.bottomButton = PrimaryPushButton("弹出底部抽屉", self)
        self.leftButton = PrimaryPushButton("弹出左侧抽屉", self)
        self.rightButton = PrimaryPushButton("弹出右侧抽屉", self)

        self.box.addWidgets([self.topButton, self.bottomButton, self.leftButton, self.rightButton])

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.topButton.clicked.connect(self.topDrawer.show)
        self.bottomButton.clicked.connect(self.bottomDrawer.show)
        self.leftButton.clicked.connect(self.leftDrawer.show)
        self.rightButton.clicked.connect(self.rightDrawer.show)

    def createComboBox(self, items, widget: TopPopDrawerWidget, index=0):
        box = ComboBox(self)
        box.addItems(items)
        if index == 0:
            box.currentTextChanged.connect(lambda text: widget.setBackgroundColor(text, text))
        elif index == 1:
            box.currentTextChanged.connect(lambda text: widget.setDrawerSize(int(text), int(text)))
        elif index == 2:
            box.currentTextChanged.connect(lambda text: widget.setDuration(int(text)))
        return box

    def createTitle(self, text):
        return TitleLabel(text)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DrawerWidgetInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
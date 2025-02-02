from FluentWidgets import (
    Widget, LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, BottomPopDrawerWidget, VBoxLayout
)
from qfluentwidgets import PushButton


class PopDrawerWidget(Widget):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(text)
        self.layout = VBoxLayout(self)
        self.topButton = PushButton('Show Top Drawer', self)
        self.leftButton = PushButton('Show Left Drawer', self)
        self.rightButton = PushButton('Show Right Drawer', self)
        self.bottomButton = PushButton('Show Bottom Drawer', self)

        self.initPopDrawer()
        self.initLayout()
        self.connectSignalSlot()
        self.enableTransparentBackground(True)

    def initPopDrawer(self):
        self.topPopDrawer = TopPopDrawerWidget(
            self,
            "弹出顶部抽屉",
            lightBackgroundColor='skyblue',
            darkBackgroundColor='skyblue'
        )
        self.leftPopDrawer = LeftPopDrawerWidget(
            self,
            "弹出左侧抽屉",
            lightBackgroundColor='pink',
            darkBackgroundColor='pink'
        )
        self.rightPopDrawer = RightPopDrawerWidget(
            self,
            "弹出右侧抽屉",
            lightBackgroundColor='deepskyblue',
            darkBackgroundColor='deepskyblue'
        )
        self.bottomPopDrawer = BottomPopDrawerWidget(
            self,
            "弹出底部抽屉",
            lightBackgroundColor='deeppink',
            darkBackgroundColor='deeppink'
        )

    def initLayout(self):
        self.layout.addWidgets([self.leftButton, self.topButton, self.rightButton, self.bottomButton])

    def connectSignalSlot(self):
        self.topButton.clicked.connect(self.topPopDrawer.show)
        self.bottomButton.clicked.connect(self.bottomPopDrawer.show)
        self.leftButton.clicked.connect(self.leftPopDrawer.show)
        self.rightButton.clicked.connect(self.rightPopDrawer.show)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = PopDrawerWidget()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
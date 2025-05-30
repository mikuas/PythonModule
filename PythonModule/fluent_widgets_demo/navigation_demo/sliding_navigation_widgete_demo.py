# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from FluentWidgets import SlidingNavigationWidget, TitleLabel, PopDrawerWidget, PopDrawerPosition, HorizontalSeparator, \
    ComboBox, PushButton, ToastInfoBar, ToastInfoBarPosition


class Widget(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.box = QVBoxLayout(self)
        self.box.addWidget(TitleLabel(title), alignment=Qt.AlignCenter)


class Demo(SlidingNavigationWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.insertWidget(1, HorizontalSeparator(self))
        self.settingPopDrawer = PopDrawerWidget(self, "Navigation Bar Settings", position=PopDrawerPosition.RIGHT)
        self.settingPopDrawer.setClickParentHide(True)
        self.settingPopDrawer.setMinimumWidth(300)

        self.colorComboBox = ComboBox(self)
        self.colorComboBox.addItems([
            'red',
            'black',
            'blue',
            'gray',
            'pink',
            'orange',
            'aqua',
            'skyblue',
            'deeppink',
            'deepskyblue'
        ])

        self.items = [
            "Hello World",
            "Hello PyQt",
            "Hello Python",
            "Hello Pycharm",
            "Hello LJW"
        ]

        self.initSubInterface()
        self.initPopDrawer()

        self._slidingNavigationBar.addItem(
            "Setting",
            "设置",
            onClick=lambda: self.settingPopDrawer.popDrawer()
        )
        item = self._slidingNavigationBar.item("Setting")
        item.clicked.disconnect(self._slidingNavigationBar._onClicked)

        self.setCurrentWidget('0')

    def initSubInterface(self):
        for _ in range(5):
            self.addSubInterface(
                str(_),
                f"Interface {_}",
                Widget(self.items[_], self)
            )

    def initPopDrawer(self):
        self.settingPopDrawer.addWidget(TitleLabel("选择颜色"), alignment=Qt.AlignHCenter)
        self.settingPopDrawer.addWidget(self.colorComboBox)

        self.itemButton = PushButton("设置导航项颜色为选定的颜色")
        self.settingPopDrawer.addWidget(self.itemButton)
        self.itemButton.clicked.connect(lambda: self.set("setItemColor", self.colorComboBox.currentText()))

        self.itemHoverButton = PushButton("设置导航项悬停色为选定的颜色")
        self.settingPopDrawer.addWidget(self.itemHoverButton)
        self.itemHoverButton.clicked.connect(lambda: self.set("setItemHoverColor", self.colorComboBox.currentText()))

        self.itemSelectedButton = PushButton("设置导航项选中颜色为选定的颜色")
        self.settingPopDrawer.addWidget(self.itemSelectedButton)
        self.itemSelectedButton.clicked.connect(lambda: self.set("setItemSelectedColor", self.colorComboBox.currentText()))

        self.lineButton = PushButton("设置滑动线颜色为选定的颜色")
        self.settingPopDrawer.addWidget(self.lineButton)
        self.lineButton.clicked.connect(lambda: self.set("setSlideLineColor", self.colorComboBox.currentText()))

    def set(self, name: str, *args):
        getattr(self._slidingNavigationBar, name, None)(*args)
        ToastInfoBar.success(
            self,
            "     设置颜色成功",
            name,
            isClosable=False,
            position=ToastInfoBarPosition.TOP,
            height=64
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.settingPopDrawer.setFixedWidth(self.width() / 2.5)
        self.settingPopDrawer.setMinimumWidth(300)
        self.settingPopDrawer.setDuration(self.width())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
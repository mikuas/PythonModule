# coding:utf-8
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QApplication
from FluentWidgets import LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, BottomPopDrawerWidget, VBoxLayout
from qfluentwidgets import InfoBar, PrimaryPushButton

# from PythonModule.FluentWidgetModule.FluentWidgets.components import LeftPopDrawerWidget, \
#     RightPopDrawerWidget, TopPopDrawerWidget, BottomPopDrawerWidget

class DanLi(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.vBoxLayout = VBoxLayout(self)
        self.leftDrawer = LeftPopDrawerWidget(self, "左侧弹出抽屉")
        self.rightDrawer = RightPopDrawerWidget(self, "右侧弹出抽屉")
        self.topDrawer = TopPopDrawerWidget(self, "顶部弹出抽屉")
        self.bottomDrawer = BottomPopDrawerWidget(self, "底部弹出抽屉")

        self.drawers = [self.leftDrawer, self.rightDrawer, self.topDrawer, self.bottomDrawer]

        for drawer in self.drawers:
            button = PrimaryPushButton(drawer._title.text(), self)
            button.clicked.connect(drawer.show)
            self.vBoxLayout.addWidget(button)


if __name__ == '__main__':
    app = QApplication([])
    window = DanLi()
    window.show()
    sys.exit(app.exec())
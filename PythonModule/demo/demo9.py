# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import VerticalPagerWidget, TopPopDrawerWidget, LeftPopDrawerWidget, \
    RightPopDrawerWidget, BottomPopDrawerWidget, VBoxLayout, VerticalSplitter, HorizontalSplitter
from qfluentwidgets import PrimaryPushButton, TitleLabel, LineEdit

from FluentWidgets import DragFileWidget, DragFolderWidget


class DrawerWidget(QWidget):
    def __init__(self, parent, widget, title):
        super().__init__(parent)
        self.vBoxLayout = VBoxLayout(self)

        self.drawer = widget(parent)

        self.button = PrimaryPushButton(title, self)
        self.button.clicked.connect(self.drawer.show)

        self.vBoxLayout.addWidget(self.button)


class VSplitter(VerticalSplitter):
    def __init__(self, parent):
        super().__init__(parent)
        self.dragFile = DragFileWidget(self, 'C:/', "文本文件 (*.txt);; 图片文件 (*.png *.jpg *.jpeg);; 视频文件 (*.mp4 *.avi *.mkv)")
        self.dragFile.setLabelText("拖动文本文件, 图片文件, 视频文件到此")
        self.dragFolder = DragFolderWidget(self, 'E:/')
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('设置边框颜色')

        self.addWidgets([self.dragFile, self.lineEdit, self.dragFolder])

        self.lineEdit.textChanged.connect(lambda color: (
            self.dragFile.setBorderColor(color),
            self.dragFolder.setBorderColor(color)
        ))

        self.dragFile.draggedChange.connect(lambda path: print(f'draggedFile: {path}'))
        self.dragFile.selectionChange.connect(lambda path: print(f'selectionFile: {path}'))

        self.dragFolder.draggedChange.connect(lambda path: print(f'draggedFolder: {path}'))
        self.dragFolder.selectionChange.connect(lambda path: print(f'selectedFolder: {path}'))



class HSplitter(HorizontalSplitter):
    def __init__(self, parent):
        super().__init__(parent)
        self.addWidget(TitleLabel("VERTICAL SPLITTER", self))
        self.addWidget(TitleLabel("VERTICAL SPLITTER", self))


class Window(VerticalPagerWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.displayPrevButton().displayNextButton()
        self.leftDrawer = DrawerWidget(self, LeftPopDrawerWidget, '"Click Me Show LeftPopDrawer')
        self.topDrawer = DrawerWidget(self, TopPopDrawerWidget, '"Click Me Show TopPopDrawer')
        self.rightDrawer = DrawerWidget(self, RightPopDrawerWidget, '"Click Me Show RightPopDrawer')
        self.bottomDrawer = DrawerWidget(self, BottomPopDrawerWidget, '"Click Me Show BottomPopDrawer')

        self.vSplitter = VSplitter(self)
        self.hSplitter = HSplitter(self)

        self.addWidgets([self.leftDrawer, self.topDrawer, self.rightDrawer, self.bottomDrawer, self.vSplitter, self.hSplitter])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

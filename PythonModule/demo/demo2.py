# coding:utf-8
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from FluentWidgets import (
    Dialog, MessageBox, UrlDialog, ColorDialog, CustomDialog,
    FlowLayoutWidget, FlipViewWidget,
    VerticalPagerWidget, HorizontalPagerWidget
)
from qfluentwidgets import PrimaryPushButton, ComboBox, TitleLabel, PushButton


class Window(VerticalPagerWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.displayPrevButton().displayNextButton().resize(800, 520)
        # self.enableScrollTogglePage(False)
        self.dialogButton = PrimaryPushButton("Show Dialog", self)
        self.messageBoxButton = PrimaryPushButton("Show Message Box", self)
        self.urlDialogButton = PrimaryPushButton("Show Url Dialog", self)
        self.colorDialogButton = PrimaryPushButton("Show Color Dialog", self)
        self.customDialogButton = PrimaryPushButton("Show Custom Dialog", self)

        self.urlDialog = UrlDialog(self)
        self.colorDialog = ColorDialog(QColor('deepskyblue'), '我是颜色选择器', self)

        self.customDialog = CustomDialog(self)
        title = TitleLabel("选择项目", self)
        self.com1 = ComboBox(self)
        self.com2 = ComboBox(self)
        self.com1.addItems(['item1', 'item2', 'item3'])
        self.com2.addItems(['item4', 'item5', 'item6'])
        self.customDialog.addWidget(title).addWidget(self.com1).addWidget(self.com2)
        self.com1.setFixedWidth(self.customDialog.width() - 50)
        self.com2.setFixedWidth(self.customDialog.width() - 50)

        self.flyout = FlowLayoutWidget()

        for _ in range(50):
            button = PushButton(str(_), self)
            button.setFixedSize(120, 60)
            self.flyout.addWidget(button)

        self.flip = FlipViewWidget(self)
        self.flip.addImages([
            r"C:\Users\Administrator\OneDrive\Pictures\17.png",
            r"C:\Users\Administrator\OneDrive\Pictures\18.png",
            r"C:\Users\Administrator\OneDrive\Pictures\19.png",
            r"C:\Users\Administrator\OneDrive\Pictures\20.png",
            r"C:\Users\Administrator\OneDrive\Pictures\21.png"
        ])
        self.flip.enableAutoPlay().setBorderRadius(8)

        self.addWidgets([
            self.dialogButton,
            self.messageBoxButton,
            self.urlDialogButton,
            self.colorDialogButton,
            self.customDialogButton,
            self.flyout,
            self.flip
        ])

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.dialogButton.clicked.connect(lambda: Dialog('我是弹出窗口', 'Hello', self).show())
        self.messageBoxButton.clicked.connect(lambda: MessageBox('我是消息框', 'Hello', self).show())
        self.urlDialogButton.clicked.connect(self.urlDialog.show)
        self.colorDialogButton.clicked.connect(self.colorDialog.show)
        self.customDialogButton.clicked.connect(self.customDialog.show)

        self.urlDialog.yesButton.clicked.connect(lambda: print(self.urlDialog.urlLineEdit.text()))
        self.colorDialog.colorChanged.connect(lambda color: print(color.name()))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.customDialog.setFixedSize(self.width() / 2, self.height() / 2)
        self.com1.setFixedWidth(self.customDialog.width() - 50)
        self.com2.setFixedWidth(self.customDialog.width() - 50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

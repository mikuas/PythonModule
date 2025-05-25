# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import VerticalScrollWidget, PushButton, Dialog, MessageDialog, UrlDialog, CustomDialog


class DialogDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.dialog = Dialog("Dialog", "Content", self)
        self.messageDialog = MessageDialog("MessageDialog", "Content", self)
        self.urlDialog = UrlDialog(self)
        self.customDialog = CustomDialog(self)

        self.dialogButton = PushButton("show dialog", self)
        self.messageDialogButton = PushButton("show message dialog dialog", self)
        self.urlDialogButton = PushButton("show url dialog", self)
        self.customDialogButton = PushButton("show custom dialog", self)

        self.dialogButton.clicked.connect(self.dialog.show)
        self.messageDialogButton.clicked.connect(self.messageDialog.show)
        self.urlDialogButton.clicked.connect(self.urlDialog.show)
        self.customDialogButton.clicked.connect(self.customDialog.show)

        self.addWidget(self.dialogButton)
        self.addWidget(self.messageDialogButton)
        self.addWidget(self.urlDialogButton)
        self.addWidget(self.customDialogButton)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DialogDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
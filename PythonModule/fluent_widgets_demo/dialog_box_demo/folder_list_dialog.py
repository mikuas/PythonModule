# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import VerticalScrollWidget, PushButton, Dialog, MessageDialog, UrlDialog, CustomDialog, FolderListDialog

# from qfluentwidgets import FolderListDialog


class FolderListDialogDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.folderListDialog = FolderListDialog(
            folderPaths=[],
            title="Title",
            content="Content",
            parent=self,
        )

        self.button = PushButton("show folder list dialog", self)
        self.button.clicked.connect(self.folderListDialog.show)

        # self.addWidget(self.button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FolderListDialogDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
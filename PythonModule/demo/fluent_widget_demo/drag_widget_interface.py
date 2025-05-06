# coding:utf-8
from FluentWidgets import SmoothSwitchNavWidget, DragFileWidget, DragFolderWidget, MessageBox, VerticalScrollWidget
from PySide6.QtCore import Qt
from qfluentwidgets import TitleLabel, PushButton, LineEdit, SwitchButton, PrimaryPushButton


class DragWidgetInterface(SmoothSwitchNavWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragFile = DragFileWidget(self)
        self.dragFolder = DragFolderWidget(self)

        self.addSubInterface('dragFolder', 'Drag Folder', self.dragFolder)
        self.addSubInterface('dragFile', 'Drag File', self.dragFile)
        self.addSubInterface('setting', 'Setting', SettingInterface(self.dragFile, self.dragFolder, self))

        self.setCurrentWidget('dragFolder')

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.dragFile.selectionChange.connect(
            lambda files: MessageBox("选择的文件", f'{[text for text in files]}', self).show()
        )
        self.dragFile.draggedChange.connect(
            lambda files: MessageBox("拖动的文件", f'{[text for text in files]}', self).show()
        )

        self.dragFolder.selectionChange.connect(
            lambda folders: MessageBox("选择的文件夹", f'{[text for text in folders]}', self).show()
        )
        self.dragFolder.draggedChange.connect(
            lambda folders: MessageBox("拖动的文件夹", f'{[text for text in folders]}', self).show()
        )


class SettingInterface(VerticalScrollWidget):
    def __init__(self, file, folder, parent=None):
        super().__init__(parent)
        self.file = file
        self.folder = folder

        self.addWidget(TitleLabel("设置边框颜色", self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.borderColor = LineEdit(self)
        self.borderColor.setText("#4AA3EE")
        self.addWidget(self.borderColor)
        self.addWidget(TitleLabel("启用虚线边框", self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.enableSwitch = SwitchButton(self)
        self.addWidget(self.enableSwitch, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(TitleLabel("设置标签文本", self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.textEdit = LineEdit(self)
        self.textEdit.setText('None')
        self.addWidget(self.textEdit)
        self.addWidget(TitleLabel("设置边框宽度", self), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.borderWidth = LineEdit(self)
        self.borderWidth .setText('1')
        self.addWidget(self.borderWidth)

        self.applyButton = PrimaryPushButton("应用", self)
        self.addWidget(self.applyButton)
        self.applyButton.clicked.connect(self.updateFc)

    def updateFc(self):
        borderColor = self.borderColor.text()
        isChecked = self.enableSwitch.isChecked()
        title = self.textEdit.text()
        width = int(self.borderWidth.text())

        self.file.setBorderColor(borderColor)
        self.file.enableDashLine(isChecked)
        self.file.setLabelText(title)
        self.file.setBorderWidth(width)

        self.folder.setBorderColor(borderColor)
        self.folder.enableDashLine(isChecked)
        self.folder.setLabelText(title)
        self.folder.setBorderWidth(width)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DragWidgetInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
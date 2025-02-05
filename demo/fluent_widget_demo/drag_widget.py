from FluentWidgets import Widget, DragFileWidget, DragFolderWidget, VBoxLayout


class DragWidget(Widget):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(text)
        self.layout = VBoxLayout(self)
        self.initDragWidget()
        self.initLayout()
        self.enableTransparentBackground(True)
        self.connectSignalSlot()

        self.dragFolderWidget.setBorderColor('red')
        self.dragFolderWidget.enableDashLine(True)
        self.dragFolderWidget.setXRadius(18)
        self.dragFolderWidget.setYRadius(18)
        self.dragFolderWidget.setBorderWidth(5)

    def initDragWidget(self):
        self.dragFileWidget = DragFileWidget(self)
        self.dragFolderWidget = DragFolderWidget(self)

    def initLayout(self):
        self.layout.addWidgets([self.dragFileWidget, self.dragFolderWidget])

    def connectSignalSlot(self):
        self.dragFileWidget.draggedChange.connect(lambda files: print(f'拖拽的文件: {files}'))
        self.dragFileWidget.selectionChange.connect(lambda files: print(f'选择的文件: {files}'))
        self.dragFolderWidget.draggedChange.connect(lambda folders: print(f'拖拽的文件夹: {folders}'))
        self.dragFolderWidget.selectionChange.connect(lambda folders: print(f'选择的文件夹: {folders}'))


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DragWidget()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
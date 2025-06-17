# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout
from PySide6.QtGui import QIcon, Qt

from FluentWidgets import RoundMenu, SplitWidget, Action, MenuBar, PlainTextEdit, SplashScreen


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 720)
        self.setWindowTitle("MenuBarDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))
        # self.windowEffect.removeBackgroundEffect(self.winId())
        # self.windowEffect.setAcrylicEffect(self.winId(), "FFFFFF")

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.box.setSpacing(0)

        self.menuBar = MenuBar(self)
        self.textEdit = PlainTextEdit(self)
        self.textEdit.setPlainText("""# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout
from PySide6.QtGui import QIcon, Qt

from FluentWidgets import RoundMenu, SplitWidget, Action, MenuBar, PlainTextEdit, setFont


class MainWindow(SplitWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 720)
        self.setWindowTitle("MenuBarDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))
        # self.windowEffect.removeBackgroundEffect(self.winId())
        # self.windowEffect.setAcrylicEffect(self.winId(), "FFFFFF")

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.box.setSpacing(0)

        self.menuBar = MenuBar(self)
        self.textEdit = PlainTextEdit(self)

        self.menuBar.setStyleSheet("background-color: #FFFFFF")
        self.box.addWidget(self.menuBar, 0, Qt.AlignTop)
        self.box.addWidget(self.textEdit, 1)
        
        setFont(self.textEdit, 24)
        
        self.fileMenu = self.menuBar.addMenu("文件")
        self.fileMenu.addActions([
           Action("新建标签页", self, triggered=lambda: print("新建标签页")).setShortcut("Ctrl+N"),
           Action("新建窗口", self, triggered=lambda: print("新建窗口")).setShortcut("Ctrl+Shift+N"),
           Action("打开", self, triggered=lambda: print("打开")).setShortcut("Ctrl+O")
        ])
        
        self.recentlyUsedMenu = RoundMenu("最近使用", self)
        action = Action("没有最近使用的文件", self, triggered=lambda: print("没有最近使用的文件"))
        action.setEnabled(False)
        self.recentlyUsedMenu.addAction(action)
        self.fileMenu.addMenu(self.recentlyUsedMenu)
        
        self.fileMenu.addActions([
           Action("保存", self, triggered=lambda: print("保存")).setShortcut("Ctrl+S"),
           Action("另存为", self, triggered=lambda: print("另存为")).setShortcut("Ctrl+Shift+S"),
           Action("全部保存", self, triggered=lambda: print("全部保存")).setShortcut("Ctrl+Alt+S")
        ])
        
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([
           Action("页面设置", self, triggered=lambda: print("页面设置")),
           Action("打印", self, triggered=lambda: print("打印")).setShortcut("Ctrl+P")
        ])
        
        self.fileMenu.addSeparator()
        self.fileMenu.addActions([
           Action("关闭选项卡", self, triggered=lambda: print("关闭选项卡")).setShortcut("Ctrl+W"),
           Action("关闭窗口", self, triggered=lambda: print("关闭窗口")).setShortcut("Ctrl+Shift+W"),
           Action("退出", self, triggered=QApplication.quit).setShortcut("Ctrl+Q")
        ])
        
        self.editMenu = self.menuBar.addMenu("编辑")
        self.editMenu.addAction(Action("撤销", self, triggered=lambda: print("撤销")).setShortcut("Ctrl+Z"))
        self.editMenu.addSeparator()
        
        self.editMenu.addActions([
           Action("剪切", self, triggered=lambda: print("剪切")).setShortcut("Ctrl+X"),
           Action("复制", self, triggered=lambda: print("复制")).setShortcut("Ctrl+C"),
           Action("粘贴", self, triggered=lambda: print("粘贴")).setShortcut("Ctrl+V"),
           Action("删除", self, triggered=lambda: print("删除")).setShortcut("Del")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addAction(Action("使用必应进行定义", self, triggered=lambda: print("使用必应进行定义")).setShortcut("Ctrl+E"))
        self.editMenu.addSeparator()
        self.editMenu.addActions([
           Action("查找", self, triggered=lambda: print("查找")).setShortcut("Ctrl+F"),
           Action("查找上一个", self, triggered=lambda: print("查找上一个")).setShortcut("F3"),
           Action("查找下一个", self, triggered=lambda: print("查找下一个")).setShortcut("Shift+F3"),
           Action("替换", self, triggered=lambda: print("替换")).setShortcut("Ctrl+H"),
           Action("转到", self, triggered=lambda: print("转到")).setShortcut("Ctrl+G")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addActions([
           Action("全选", self, triggered=lambda: print("全选")).setShortcut("Ctrl+A"),
           Action("时间/日期", self, triggered=lambda: print("时间/日期")).setShortcut("F5")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addAction(Action("字体", self, triggered=lambda: print("字体")))
        
        self.viewMenu = self.menuBar.addMenu("查看")
        self.zoomMenu = RoundMenu("缩放", self)
        self.zoomMenu.addActions([
           Action("100%", self, triggered=lambda: print("100%")),
           Action("200%", self, triggered=lambda: print("200%")),
           Action("300%", self, triggered=lambda: print("300%")),
           Action("400%", self, triggered=lambda: print("400%")),
           Action("500%", self, triggered=lambda: print("500%"))
        ])
        self.viewMenu.addMenu(self.zoomMenu)
        self.viewMenu.view.setFixedWidth(168)
        self.zoomMenu.setFixedWidth(170)
        self.zoomMenu.view.setFixedWidth(158)
        
        statusAction = Action("状态栏", self, triggered=lambda: print("状态栏"))
        autoWrapAction = Action("自动换行", self, triggered=lambda: print("自动换行"))
        self.viewMenu.addActions([statusAction, autoWrapAction])
        
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.hideTitleBarButton()
        self.show()
        self.splashScreen.run()
        
        
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.resize(800, 520)
        window.show()
        sys.exit(app.exec())
        """)

        self.box.addWidget(self.menuBar, 0, Qt.AlignTop)
        self.box.addWidget(self.textEdit, 1)

        font = self.textEdit.font()
        font.setItalic(True)
        font.setPixelSize(20)
        self.textEdit.setFont(font)

        self.fileMenu = self.menuBar.addMenu("文件")
        self.fileMenu.addActions([
            Action("新建标签页", self, triggered=lambda: print("新建标签页")).setShortcut("Ctrl+N"),
            Action("新建窗口", self, triggered=lambda: print("新建窗口")).setShortcut("Ctrl+Shift+N"),
            Action("打开", self, triggered=lambda: print("打开")).setShortcut("Ctrl+O")
        ])

        self.recentlyUsedMenu = RoundMenu("最近使用", self)
        action = Action("没有最近使用的文件", self, triggered=lambda: print("没有最近使用的文件"))
        action.setEnabled(False)
        self.recentlyUsedMenu.addAction(action)
        self.fileMenu.addMenu(self.recentlyUsedMenu)

        self.fileMenu.addActions([
            Action("保存", self, triggered=lambda: print("保存")).setShortcut("Ctrl+S"),
            Action("另存为", self, triggered=lambda: print("另存为")).setShortcut("Ctrl+Shift+S"),
            Action("全部保存", self, triggered=lambda: print("全部保存")).setShortcut("Ctrl+Alt+S")
        ])

        self.fileMenu.addSeparator()
        self.fileMenu.addActions([
            Action("页面设置", self, triggered=lambda: print("页面设置")),
            Action("打印", self, triggered=lambda: print("打印")).setShortcut("Ctrl+P")
        ])

        self.fileMenu.addSeparator()
        self.fileMenu.addActions([
            Action("关闭选项卡", self, triggered=lambda: print("关闭选项卡")).setShortcut("Ctrl+W"),
            Action("关闭窗口", self, triggered=lambda: print("关闭窗口")).setShortcut("Ctrl+Shift+W"),
            Action("退出", self, triggered=QApplication.quit).setShortcut("Ctrl+Q")
        ])

        self.editMenu = self.menuBar.addMenu("编辑")
        self.editMenu.addAction(Action("撤销", self, triggered=lambda: print("撤销")).setShortcut("Ctrl+Z"))
        self.editMenu.addSeparator()

        self.editMenu.addActions([
            Action("剪切", self, triggered=lambda: print("剪切")).setShortcut("Ctrl+X"),
            Action("复制", self, triggered=lambda: print("复制")).setShortcut("Ctrl+C"),
            Action("粘贴", self, triggered=lambda: print("粘贴")).setShortcut("Ctrl+V"),
            Action("删除", self, triggered=lambda: print("删除")).setShortcut("Del")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addAction(Action("使用必应进行定义", self, triggered=lambda: print("使用必应进行定义")).setShortcut("Ctrl+E"))
        self.editMenu.addSeparator()
        self.editMenu.addActions([
            Action("查找", self, triggered=lambda: print("查找")).setShortcut("Ctrl+F"),
            Action("查找上一个", self, triggered=lambda: print("查找上一个")).setShortcut("F3"),
            Action("查找下一个", self, triggered=lambda: print("查找下一个")).setShortcut("Shift+F3"),
            Action("替换", self, triggered=lambda: print("替换")).setShortcut("Ctrl+H"),
            Action("转到", self, triggered=lambda: print("转到")).setShortcut("Ctrl+G")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addActions([
            Action("全选", self, triggered=lambda: print("全选")).setShortcut("Ctrl+A"),
            Action("时间/日期", self, triggered=lambda: print("时间/日期")).setShortcut("F5")
        ])
        self.editMenu.addSeparator()
        self.editMenu.addAction(Action("字体", self, triggered=lambda: print("字体")))

        self.viewMenu = self.menuBar.addMenu("查看")
        self.zoomMenu = RoundMenu("缩放", self)
        self.zoomMenu.addActions([
            Action("100%", self, triggered=lambda: print("100%")),
            Action("200%", self, triggered=lambda: print("200%")),
            Action("300%", self, triggered=lambda: print("300%")),
            Action("400%", self, triggered=lambda: print("400%")),
            Action("500%", self, triggered=lambda: print("500%"))
        ])
        self.viewMenu.addMenu(self.zoomMenu)
        self.viewMenu.view.setFixedWidth(168)
        self.zoomMenu.setFixedWidth(170)
        self.zoomMenu.view.setFixedWidth(158)

        statusAction = Action("状态栏", self, triggered=lambda: print("状态栏"))
        autoWrapAction = Action("自动换行", self, triggered=lambda: print("自动换行"))
        self.viewMenu.addActions([statusAction, autoWrapAction])

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.hideTitleBarButton()
        self.show()
        self.splashScreen.run()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
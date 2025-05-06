from FluentWidgets import VerticalScrollWidget, LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, \
    BottomPopDrawerWidget
from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import QApplication
from qfluentwidgets import PrimaryPushButton, setTheme, Theme, InfoBar, FluentIcon

from PythonModule.FluentWidgetModule.FluentWidgets import PrimaryButtonCard


class Window(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('frame')
        self.setWindowTitle("QFrame 动画示例")
        self.resize(850, 600)
        self.drawerWidgets = []
        self.initWidget()

    def initWidget(self):
        widgets = [LeftPopDrawerWidget, RightPopDrawerWidget, TopPopDrawerWidget, BottomPopDrawerWidget]
        for widget in widgets:
            drawer = widget(self, '', 500, QEasingCurve.Type.InBack)
            button = PrimaryPushButton(f'Show Drawer', drawer)
            button.clicked.connect(drawer.show)

            drawer.addWidget(PrimaryButtonCard(FluentIcon.INFO, 'Title', 'Content', "确定"))

            self.vBoxLayout.addWidget(button)
            self.drawerWidgets.append(drawer)


if __name__ == '__main__':
    app = QApplication([])
    main_window = Window()
    setTheme(Theme.AUTO)
    main_window.show()
    app.exec()
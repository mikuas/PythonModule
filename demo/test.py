import sys

from PySide6.QtWidgets import QApplication

from PythonModule.FluentWidgetModule.FluentWidgets import *
from qframelesswindow import FramelessWindow, AcrylicWindow


class Window(SplitFluentWindow):
    def __init__(self):
        super().__init__()
        si = SystemTrayIcon(self)
        si.show()
        si.addAction(Action(FluentIcon.EDIT, 'edit', triggered=lambda: print(True)))
        si.setIcon(FluentIcon.HOME)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
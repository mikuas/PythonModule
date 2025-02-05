import sys
from PySide6.QtWidgets import QApplication
from FluentWidgets import MSFluentWindow
from qfluentwidgets import FluentIcon

from button_card import ButtonCardWidget
from combo_box_card import ComboBoxCardWidget
from drag_widget import DragWidget
from drawer_widget import PopDrawerWidget


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 700)
        self.setWindowTitle("FluentWidgetDemo")

        self.cardWidget = ButtonCardWidget(self, 'Card Widget')
        self.comboBoxWidget = ComboBoxCardWidget(self, 'ComboBox Widget')
        self.dragWidget = DragWidget(self, 'Drag Widget')
        self.popDrawerWidget = PopDrawerWidget(self, 'Drawer Widget')
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(
            self.cardWidget,
            FluentIcon.APPLICATION,
            'Card Widget'
        )
        self.addSubInterface(
            self.comboBoxWidget,
            FluentIcon.APPLICATION,
            'ComboBox Widget'
        )
        self.addSubInterface(
            self.dragWidget,
            FluentIcon.APPLICATION,
            'Drag Widget'
        )
        self.addSubInterface(
            self.popDrawerWidget,
            FluentIcon.APPLICATION,
            'Drawer Widget'
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
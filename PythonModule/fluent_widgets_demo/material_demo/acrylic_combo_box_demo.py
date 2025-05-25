# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from FluentWidgets import AcrylicComboBox, AcrylicEditableComboBox, VerticalScrollWidget



class AcrylicComboBoxDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.items = [f"Item {_}" for _ in range(1, 101)]

        self.acrylicComboBox = AcrylicComboBox(self)
        self.acrylicEditComboBox = AcrylicEditableComboBox(self)

        self.acrylicComboBox.addItems(self.items)
        self.acrylicEditComboBox.addItems(self.items)

        self.addWidget(self.acrylicComboBox)
        self.addWidget(self.acrylicEditComboBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AcrylicComboBoxDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
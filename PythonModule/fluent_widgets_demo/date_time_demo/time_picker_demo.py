# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import VerticalScrollWidget, TimePicker, AMTimePicker


class TimePickerDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.timePicker = TimePicker(self)
        self.atmTimePicker = AMTimePicker(self)

        self.addWidget(self.timePicker)
        self.addWidget(self.atmTimePicker)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimePickerDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
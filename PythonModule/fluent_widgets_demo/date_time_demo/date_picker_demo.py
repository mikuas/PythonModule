# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import VerticalScrollWidget, DatePicker, ZhDatePicker


class DatePickerDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.datePicker = DatePicker(self)
        self.zhDatePicker = ZhDatePicker(self)

        self.addWidget(self.datePicker)
        self.addWidget(self.zhDatePicker)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatePickerDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
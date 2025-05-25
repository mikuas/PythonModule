# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from FluentWidgets import CalendarPicker, VerticalScrollWidget, FastCalendarPicker


class CalendarPickerDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.calendarPicker = CalendarPicker(self)

        self.faseCalendarPicker = FastCalendarPicker(self)

        self.addWidget(self.calendarPicker)
        self.addWidget(self.faseCalendarPicker)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarPickerDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
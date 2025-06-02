from enum import Enum

from PySide6.QtGui import QColor


class ToastInfoBarColor(Enum):
    """ toast infoBar color """
    SUCCESS = '#3EC870'
    ERROR = '#BC0E11'
    WARNING = '#FFEB3B'
    INFO = '#2196F3'

    def __new__(cls, color):
        obj = object.__new__(cls)
        obj.color = QColor(color)
        return obj

    @property
    def value(self):
        return self.color

# print(ToastInfoBarColor.SUCCESS)
print(ToastInfoBarColor.SUCCESS.value)
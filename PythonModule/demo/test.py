from typing import overload, Union
from PySide6.QtWidgets import QWidget


class Test:
    def __init__(self):
        self.__value__ = None
        self.__type__ = None

    @overload
    def setCurrentWidget(self, widget: str): ...
    @overload
    def setCurrentWidget(self, widget: QWidget): ...

    def setCurrentWidget(self, widget: Union[str, QWidget]):
        if isinstance(widget, QWidget):
            self.__currentWidget__ = widget
        elif isinstance(widget, str):
            self.__currentWidget__.routeKey = widget
        return self

    @overload
    def push(self, value: str) -> 'Test': ...

    @overload
    def push(self, value: int) -> 'Test': ...

    def push(self, value: Union[str, int]):
        if isinstance(value, str):
            self.__value__ = value
        if isinstance(value, int):
            self.__value__ = value
        self.__type__ = type(value)
        return self

    @property
    def currentWidget(self):
        return self.__currentWidget__

    @property
    def value(self):
        return self.__value__, self.__type__


if __name__ == '__main__':
    item = Test()
    print(item.push('Hello').push(1145).value)
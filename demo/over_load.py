# coding:utf-8
from typing import Union, overload


class OverloadDemo:
    @overload
    def __init__(self, name: int): ...

    @overload
    def __init__(self, name: str): ...

    def __init__(self, name: Union[int, str]):
        super().__init__()
        if isinstance(name, int):
            print("int")
        elif isinstance(name, str):
            print("str")
        else:
            raise TypeError("Error")

    @overload
    def get(self, value: int):
        pass

    @overload
    def get(self, value: str):
        pass

    def get(self, value):
        if isinstance(value, int):
            print("Int")
            return
        elif isinstance(value, str):
            print("Str")
            return
        raise TypeError("Unsupported type")


if __name__ == '__main__':
    tp = OverloadDemo('1')

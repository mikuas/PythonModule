# coding:utf-8

from enum import Enum


class Item(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    LENGTH = 3


class Test:

    def setData(self, name: str, value):
        setattr(self, name, value)

    def getDate(self, name: str):
        try:
            return getattr(self, name)
        except AttributeError:
            return None


if __name__ == '__main__':
    test = Test()

    test.setData("name", "Interval")
    print(test.getDate("name"))
    print(test.getDate("age"))
    test.setData("name", "Null")
    print(test.getDate("name"))

    def add(*args):
        result = 0
        for _ in args:
            result += _
        print(result)

    def addF(*args):
        result = 0.0
        for _ in args:
            result += _
        print(result)

    def printf(*args):
        result = ""
        for _ in args:
            result += str(_)
        print(result)

    def length(*args):
        print(len(args))

    def make(flag: Item, *args):
        item = {
            Item.INT: add,
            Item.STRING: printf,
            Item.FLOAT: addF,
            Item.LENGTH: length
        }
        item[flag](*args)

    make(Item.STRING, 1, 1, 5, 3)
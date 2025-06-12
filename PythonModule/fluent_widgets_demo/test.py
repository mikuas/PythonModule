# coding:utf-8


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
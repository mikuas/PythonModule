# coding:utf-8

from typing import overload, Union


class Main:

    @overload
    def add(self, args: int) -> int: ...

    @overload
    def add(self, args: float) -> float: ...

    @overload
    def add(self, args: str) -> str: ...

    def add(self, args: Union[int, float, str]):
        if isinstance(str, args):
            return str(args)
        elif isinstance(int, args):
            return int(args)
        elif isinstance(float, args):
            return float(args)
        else:
            return self


main = Main()
main.add("ff")
main.add(1)
main.add(1.1)
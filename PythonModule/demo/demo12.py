# coding:utf-8
from enum import Enum

from PySide6.QtCore import QPoint
from qfluentwidgets import InfoBar


# 定义操作类型枚举
class Operation(Enum):
    TOP = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3


# 定义一个 Registry 类，用于注册操作类并执行操作
class PopView:
    registry = {}

    @classmethod
    def register(cls, operation_enum):
        """将操作类注册到 registry 字典中"""
        def decorator(class_type):
            cls.registry[operation_enum] = class_type
            return class_type
        return decorator

    @classmethod
    def get(cls, operation):
        """根据操作类型执行相应操作"""
        operation_class = cls.registry.get(operation)
        if operation_class:
            # 实例化并执行操作
            operation_instance = operation_class()
            return operation_instance.getPos()
        else:
            raise ValueError(f"No operation registered for {operation}")

    def execute(self):
        raise NotImplementedError

    def getPos(self):
        raise NotImplementedError


# 定义操作类，使用装饰器自动注册
@PopView.register(Operation.TOP)
class TopPopView(PopView):

    def getPos(self):
        return QPoint(0, 0)


@PopView.register(Operation.LEFT)
class LeftPopView(PopView):

    def getPos(self):
        return QPoint(1, 1)


@PopView.register(Operation.RIGHT)
class RightPopView(PopView):

    def getPos(self):
        return QPoint(2, 2)

@PopView.register(Operation.BOTTOM)
class BottomPopView(PopView):

    def getPos(self):
        return QPoint(3, 3)


if __name__ == '__main__':
    print(PopView.get(Operation.BOTTOM))

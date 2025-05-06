import weakref
from enum import Enum
from PySide6.QtCore import QObject
from qfluentwidgets import InfoBar

# 定义一个枚举，用作键
class Interface(Enum):
    TOP = "TOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"


# 单例类实现
class SingletonRegistry:
    _instances = {}
    managers = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
        super().__init__()
        self.spacing = 16
        self.margin = 24

    def get_pos(self):
        """ Return the position of info bar (implemented by subclasses) """
        return None

    @classmethod
    def register(cls, name):
        """ Register sub-classes """
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager
            return Manager
        return wrapper

    @classmethod
    def make(cls, position):
        """ Create and return the appropriate manager instance based on position """
        if position not in cls.managers:
            raise ValueError(f'`{position}` is an invalid animation type.')

        # Ensure we are creating an instance of the registered subclass, not the base class
        return cls.managers[position]()  # This calls the subclass' constructor


# 使用 register 注册子类，并继承 SingletonRegistry
@SingletonRegistry.register(Interface.TOP)
class Top(SingletonRegistry):

    def get_pos(self):
        return f'top: {self.margin}'


@SingletonRegistry.register(Interface.LEFT)
class Left(SingletonRegistry):

    def get_pos(self):
        return f'left: {self.margin}'


@SingletonRegistry.register(Interface.RIGHT)
class Right(SingletonRegistry):

    def get_pos(self):
        return f'right: {self.margin}'


@SingletonRegistry.register(Interface.BOTTOM)
class Bottom(SingletonRegistry):

    def get_pos(self):
        return f'bottom: {self.margin}'


# 测试代码
if __name__ == "__main__":
    # 获取单例实例
    top1 = SingletonRegistry.make(Interface.TOP)
    top2 = SingletonRegistry.make(Interface.TOP)
    bottom = SingletonRegistry.make(Interface.BOTTOM)

    print(top1.get_pos())
    top1.margin = 1
    print(top2.get_pos())
    print(bottom.get_pos())

    print(top1 is top2)
    print(top1 is bottom)
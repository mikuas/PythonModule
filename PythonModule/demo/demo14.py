import weakref
from enum import Enum
from PySide6.QtCore import QObject


class Interface(Enum):
    TOP = "TOP"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"


class SingletonRegistry(QObject):
    _instance = None  # 存储单例
    registry = {}  # 注册表

    def __new__(cls, *args, **kwargs):
        if cls is SingletonRegistry and cls._instance is None:
            # 单例模式核心逻辑
            cls._instance = super(SingletonRegistry, cls).__new__(cls, *args, **kwargs)
        elif cls is not SingletonRegistry:
            # 子类正常创建实例
            return super(SingletonRegistry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True  # 防止重复初始化
            super().__init__()
            self.spacing = 16
            self.margin = 24
            self.infoBars = weakref.WeakKeyDictionary()
            self.aniGroups = weakref.WeakKeyDictionary()

    @classmethod
    def register(cls, key):
        """注册装饰器"""
        def decorator(class_type):
            cls.registry[key] = class_type
            return class_type
        return decorator

    @classmethod
    def get(cls, key):
        """根据键获取注册的子类实例"""
        if key in cls.registry:
            instance = cls.registry[key]()  # 实例化注册的子类
            return instance.get_pos()  # 调用子类的 get_pos 方法
        raise ValueError(f"Key {key} not registered!")


# 子类继承 SingletonRegistry，只覆写 get_pos 方法
@SingletonRegistry.register(Interface.TOP)
class Top(SingletonRegistry):
    def get_pos(self):
        return f'Top position, margin: {self.margin}'


@SingletonRegistry.register(Interface.LEFT)
class Left(SingletonRegistry):
    def get_pos(self):
        return f'Left position, margin: {self.margin}'


@SingletonRegistry.register(Interface.RIGHT)
class Right(SingletonRegistry):
    def get_pos(self):
        return f'Right position, margin: {self.margin}'


@SingletonRegistry.register(Interface.BOTTOM)
class Bottom(SingletonRegistry):
    def get_pos(self):
        return f'Bottom position, margin: {self.margin}'


# 测试代码
if __name__ == "__main__":
    # 获取单例实例
    registry = SingletonRegistry()

    print("测试已注册的类:")
    print(registry.get(Interface.TOP))  # 输出: Top position, margin: 24
    print(registry.get(Interface.LEFT))  # 输出: Left position, margin: 24
    print(registry.get(Interface.RIGHT))  # 输出: Right position, margin: 24
    print(registry.get(Interface.BOTTOM))  # 输出: Bottom position, margin: 24

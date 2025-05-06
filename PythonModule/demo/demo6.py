import sys

from FluentWidgets import VBoxLayout
from PySide6.QtCore import QAbstractAnimation, QEasingCurve, QPoint, QPropertyAnimation, Signal, Qt, QTimer
from PySide6.QtWidgets import QStackedWidget, QWidget, QApplication
from qfluentwidgets import TitleLabel, PrimaryPushButton


class PopUpAniInfo:
    """ 存储单个页面的动画信息 """

    def __init__(self, widget, deltaX, deltaY, ani):
        self.widget = widget  # 对应的页面控件
        self.deltaX = deltaX  # 水平动画的偏移量
        self.deltaY = deltaY  # 垂直动画的偏移量
        self.ani = ani  # 动画对象


class PopUpAniStackedWidget(QStackedWidget):
    """ 带有弹出动画的 QStackedWidget """

    # 定义信号：动画开始和结束时触发
    aniFinished = Signal()
    aniStart = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aniInfos = []  # 用于存储每个页面的动画信息
        self._nextIndex = None  # 将要切换到的页面索引
        self._ani = None  # 当前正在运行的动画对象

    def addWidget(self, widget, deltaX=0, deltaY=76):
        """
        添加页面控件并初始化其动画信息

        Parameters
        -----------
        widget: QWidget
            要添加的页面控件

        deltaX: int
            动画的水平偏移量

        deltaY: int
            动画的垂直偏移量
        """
        super().addWidget(widget)

        # 创建动画信息对象并存储
        self.aniInfos.append(PopUpAniInfo(
            widget=widget,
            deltaX=deltaX,
            deltaY=deltaY,
            ani=QPropertyAnimation(widget, b'pos'),  # 设置动画操作的属性为控件的位置
        ))

    def removeWidget(self, widget: QWidget):
        """
        移除指定的页面控件及其动画信息

        Parameters
        ----------
        widget: QWidget
            要移除的页面控件
        """
        index = self.indexOf(widget)  # 获取控件的索引
        if index == -1:
            return  # 如果控件不在堆叠部件中则直接返回

        self.aniInfos.pop(index)  # 移除对应的动画信息
        super().removeWidget(widget)  # 调用父类的方法移除控件

    def setCurrentIndex(self, index: int, needPopOut: bool = False, showNextWidgetDirectly: bool = True,
                        duration: int = 250, easingCurve=QEasingCurve.OutQuad):
        """
        切换到指定的页面并应用动画效果

        Parameters
        ----------
        index: int
            要切换到的页面索引

        needPopOut: bool
            是否需要弹出动画（当前页面弹出）

        showNextWidgetDirectly: bool
            是否在动画开始时立即显示目标页面

        duration: int
            动画持续时间（单位：毫秒）

        easingCurve: QEasingCurve
            动画缓动曲线，用于控制动画的节奏
        """
        # 检查索引是否合法
        if index < 0 or index >= self.count():
            raise Exception(f'The index `{index}` is illegal')

        # 如果目标页面就是当前页面，则无需切换
        if index == self.currentIndex():
            return

        # 如果当前有动画正在运行，停止动画并清理状态
        if self._ani and self._ani.state() == QAbstractAnimation.Running:
            self._ani.stop()
            self.__onAniFinished()

        # 设置将要切换到的页面索引
        self._nextIndex = index

        # 获取当前页面和目标页面的动画信息
        nextAniInfo = self.aniInfos[index]
        currentAniInfo = self.aniInfos[self.currentIndex()]

        # 当前和目标控件
        currentWidget = self.currentWidget()
        nextWidget = nextAniInfo.widget

        # 根据是否需要弹出动画选择对应的动画对象
        ani = currentAniInfo.ani if needPopOut else nextAniInfo.ani
        self._ani = ani  # 存储当前动画对象

        if needPopOut:
            # 配置当前页面的弹出动画
            deltaX, deltaY = currentAniInfo.deltaX, currentAniInfo.deltaY
            pos = currentWidget.pos() + QPoint(deltaX, deltaY)  # 计算动画结束的位置
            self.__setAnimation(ani, currentWidget.pos(), pos, duration, easingCurve)
            nextWidget.setVisible(showNextWidgetDirectly)  # 根据参数决定是否立即显示目标页面
        else:
            # 配置目标页面的滑入动画
            deltaX, deltaY = nextAniInfo.deltaX, nextAniInfo.deltaY
            pos = nextWidget.pos() + QPoint(deltaX, deltaY)  # 动画开始的位置
            self.__setAnimation(ani, pos, QPoint(nextWidget.x(), 0), duration, easingCurve)
            super().setCurrentIndex(index)  # 提前切换到目标页面

        # 启动动画
        ani.finished.connect(self.__onAniFinished)  # 动画结束时触发回调
        ani.start()
        self.aniStart.emit()  # 发射动画开始信号

    def setCurrentWidget(self, widget, needPopOut: bool = False, showNextWidgetDirectly: bool = True,
                         duration: int = 250, easingCurve=QEasingCurve.OutQuad):
        """
        切换到指定的页面控件

        Parameters
        ----------
        widget: QWidget
            要切换到的页面控件

        其余参数说明见 setCurrentIndex 方法
        """
        self.setCurrentIndex(
            self.indexOf(widget), needPopOut, showNextWidgetDirectly, duration, easingCurve)

    def __setAnimation(self, ani, startValue, endValue, duration, easingCurve=QEasingCurve.Type.Linear):
        """
        配置动画属性

        Parameters
        ----------
        ani: QPropertyAnimation
            动画对象

        startValue: QVariant
            动画的起始值

        endValue: QVariant
            动画的结束值

        duration: int
            动画持续时间

        easingCurve: QEasingCurve
            动画的缓动曲线
        """
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __onAniFinished(self):
        """
        动画结束后的处理
        """
        self._ani.finished.disconnect()  # 断开信号连接
        super().setCurrentIndex(self._nextIndex)  # 切换到目标页面
        self.aniFinished.emit()  # 发射动画结束信号


if __name__ == '__main__':
    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.resize(800, 520)
            self.stackedWidget = PopUpAniStackedWidget(self)
            self.stackedWidget.setFixedSize(self.size())

            for _ in range(5):
                widget = QWidget(self)
                layout = VBoxLayout(widget)
                title = TitleLabel(f"Page {_ + 1}", widget)
                button = PrimaryPushButton(f"Switch To Page {_ + 1}", self)
                layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
                layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
                self.stackedWidget.addWidget(widget)

                button.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(2),
                                                QTimer.singleShot(1000, lambda: self.stackedWidget.setCurrentIndex(0))))


    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

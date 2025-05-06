# encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, Qt, QEasingCurve, QRect
from qfluentwidgets import PrimaryPushButton, LineEdit, ComboBox
from FluentWidgets import VerticalScrollWidget, HBoxLayout

from PythonModule.demo.animation import SequentialAnimation, ParallelAnimation
from animation import WidgetAnimation


class Window(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 500)
        self.hBoxLayout = HBoxLayout()

        self.bt1 = PrimaryPushButton('Move', self)
        self.bt2 = PrimaryPushButton('Move', self)
        self.bt3 = PrimaryPushButton('Move', self)
        self.bt4 = PrimaryPushButton('Move', self)
        self.bt5 = PrimaryPushButton('Move', self)

        self.bts = [self.bt1, self.bt2, self.bt3, self.bt4, self.bt5]
        self.hBoxLayout.addWidgets(self.bts)

        self.timeBox = ComboBox(self)
        self.timeBox.addItems(['0', '500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000'])
        self.timeBox.setCurrentIndex(-1)
        self.timeBox.setPlaceholderText('选择动画时间')

        self.startBox = ComboBox(self)
        self.startBox.addItems(['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        self.startBox.setCurrentIndex(10)
        self.startBox.setPlaceholderText('选择开始透明度')

        self.endBox = ComboBox(self)
        self.endBox.addItems(['0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1'])
        self.endBox.setCurrentIndex(-1)
        self.endBox.setPlaceholderText('选择结束透明度')

        self.buttonBox = ComboBox(self)
        self.buttonBox.addItems(['1', '2', '3', '4', '5'])
        self.buttonBox.setCurrentIndex(-1)
        self.buttonBox.setPlaceholderText('选择要透明的按钮(选了模式为顺序或并行此项不用管)')

        self.modeBox = ComboBox(self)
        self.modeBox.addItems(['单个', '顺序', '并行'])
        self.modeBox.setCurrentIndex(-1)
        self.modeBox.setPlaceholderText('选择模式')
        self.button = PrimaryPushButton("选择按钮 设置透明度", self)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidgets(
            [self.timeBox, self.startBox, self.endBox, self.buttonBox, self.modeBox, self.button],
            alignment=Qt.AlignmentFlag.AlignBottom
        )

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.button.clicked.connect(self.run)

    def run(self):
        mode = self.modeBox.currentIndex()
        if mode == 0:
            WidgetAnimation.opacityAni(
                self.bts[self.buttonBox.currentIndex()],
                int(self.timeBox.text()),
                float(self.startBox.text()),
                float(self.endBox.text()),
                finished=lambda: print('END')
            ).start()
        elif mode == 1:
            pa = SequentialAnimation(self)
            pa.finish(lambda: print('SHUN XU END'))
            for bt in self.bts:
                pa.addAni(
                    WidgetAnimation.opacityAni(
                        bt,
                        int(self.timeBox.text()),
                        float(self.startBox.text()),
                        float(self.endBox.text()),
                    )
                )
            pa.start()
        elif mode == 2:
            pa = ParallelAnimation(self)
            pa.finish(lambda: print('BIN XIN END'))
            for bt in self.bts:
                pa.addAni(
                    WidgetAnimation.opacityAni(
                        bt,
                        int(self.timeBox.text()),
                        float(self.startBox.text()),
                        float(self.endBox.text()),
                    )
                )
            pa.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
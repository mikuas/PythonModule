from PySide6.QtCore import QPropertyAnimation, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QPushButton
import sys

class VisibilityAnimation(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visible 动画效果")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("点击切换可见性", self)
        self.button.clicked.connect(self.toggle_visibility)

        self.setStyleSheet("background-color: lightblue;")  # 设置背景色以便观察变化

    def toggle_visibility(self):
        if self.isVisible():
            # 如果当前可见，执行渐隐动画
            self.animate_visibility(False)
        else:
            # 如果当前不可见，执行渐现动画
            self.animate_visibility(True)

    def animate_visibility(self, visible: bool):
        # 创建透明度动画
        animation_opacity = QPropertyAnimation(self, b"opacity")
        animation_opacity.setDuration(1000)  # 动画时长1秒
        if visible:
            animation_opacity.setStartValue(0.0)  # 透明度从0开始
            animation_opacity.setEndValue(1.0)    # 结束时透明度为1
            self.show()  # 确保控件可见
        else:
            animation_opacity.setStartValue(1.0)  # 透明度从1开始
            animation_opacity.setEndValue(0.0)    # 结束时透明度为0
            animation_opacity.finished.connect(self.hide_after_animation)  # 动画结束后隐藏控件

        # 启动透明度动画
        animation_opacity.start()

    def hide_after_animation(self):
        # 动画完成后隐藏控件
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisibilityAnimation()
    window.show()
    sys.exit(app.exec())

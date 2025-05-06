import sys

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QColor
from qfluentwidgets import PrimaryPushButton
from demo11 import ToastInfoBar, VBoxLayout, ToastInfoBarPosition


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 500)
        self.vBoxLayout = VBoxLayout(self)
        self.texts = [
            'Click Me Show TopLeft Success',
            'Click Me Show TopRight Error',
            'Click Me Show Top Warning',
            'Click Me Show Bottom Info',
            'Click Me Show BottomLeft Info',
            'Click Me Show BottomRight Info',
        ]
        self.functions = [
            lambda: ToastInfoBar.success(
                self, 'success', '我是文字我是文字我是文字我是文字我'
                                 '是文字\n我是文字我是文字我是文'
                                 '字我是文字我是文字我是\n文字我是文字我是文字我'
                                 '是文字我是文字我是文字我是文字我是文字我是文字'
                                 '我是文\n字我是文字我是文字我是文字我是文字'
                                 '我是文字我是文字我是文字我是\n文字我是文字我是'
                                 '文字我是文字我是文字我是文字我是文字我是文字我'
                                 '是文\n字我是文字我是文字我是文字我是'
                                 '文字我\n是文字我'
                                 '是文字我是文字',3000, position=ToastInfoBarPosition.TOP_LEFT
            ),
            lambda: ToastInfoBar.error(
                self, 'success', 'topRight', position=ToastInfoBarPosition.TOP_RIGHT
            ),
            lambda: ToastInfoBar.warning(
                self, 'success', 'top', position=ToastInfoBarPosition.TOP
            ),
            lambda: ToastInfoBar.info(
                self, 'success', 'bottom', isClosable=False, position=ToastInfoBarPosition.BOTTOM
            ),
            lambda: ToastInfoBar.custom(
                self, 'success', 'bottomLeft', QColor('deepskyblue'), isClosable=False, position=ToastInfoBarPosition.BOTTOM_LEFT
            ),
            lambda: ToastInfoBar.custom(
                self, 'success', 'bottomRight', QColor('deeppink'),  position=ToastInfoBarPosition.BOTTOM_RIGHT
            ),
        ]
        for text, function in zip(self.texts, self.functions):
            button = PrimaryPushButton(text, self)
            self.vBoxLayout.addWidget(button)
            button.clicked.connect(function)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
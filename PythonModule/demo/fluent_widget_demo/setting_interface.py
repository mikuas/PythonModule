# coding:utf-8
from typing import List

from FluentWidgets import VerticalScrollWidget, SmoothSwitchNavWidget
from qfluentwidgets import TitleLabel


class SettingInterface(VerticalScrollWidget):
    def __init__(self, smooth: List[SmoothSwitchNavWidget] = None, parent=None):
        super().__init__(parent)
        self.sooth = smooth
        self.addWidget(TitleLabel("设置", self))


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = SettingInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

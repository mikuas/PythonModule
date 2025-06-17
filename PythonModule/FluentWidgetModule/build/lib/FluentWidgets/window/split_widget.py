# coding:utf-8
import sys

from PySide6.QtWidgets import QWidget

from .fluent_window_titlebar import SplitTitleBar
from ..common.style_sheet import isDarkTheme
from ..components.widgets.frameless_window import FramelessWindow


class SplitWidget(FramelessWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setTitleBar(SplitTitleBar(self))
        self._isMicaEnabled = False
        self.titleBar.raise_()

        if sys.platform == "darwin":
            self.titleBar.setFixedHeight(48)

    def setMicaEffectEnabled(self, isEnabled: bool):
        """ set whether the mica effect is enabled, only available on Win11 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled
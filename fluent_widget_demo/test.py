import sys
import ctypes
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt
from ctypes import windll, byref, c_int
from ctypes.wintypes import HWND, DWORD

class MicaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mica Background with Border")
        self.resize(800, 600)

        hwnd = self.get_hwnd()
        if hwnd:
            self.enable_mica(hwnd)

    def get_hwnd(self):
        """获取窗口句柄"""
        win = self.windowHandle()
        if win:
            return int(win.winId())
        return None

    def enable_mica(self, hwnd):
        """启用 Mica 背景"""
        DWMWA_SYSTEMBACKDROP_TYPE = 38  # Mica 类型
        mica_type = DWORD(3)  # 3 = Mica

        result = windll.dwmapi.DwmSetWindowAttribute(
            HWND(hwnd),
            DWMWA_SYSTEMBACKDROP_TYPE,
            byref(mica_type),
            ctypes.sizeof(mica_type)
        )

        if result != 0:
            print(f"DwmSetWindowAttribute failed: {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MicaWindow()
    window.show()
    sys.exit(app.exec())

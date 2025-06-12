from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QFont
from PySide6.QtCore import Qt, Signal
from pyspark.examples.src.main.python.als import update


class PageButton(QWidget):
    # 发出被点击的页码信号
    clicked = Signal(int)

    def __init__(self, page_number: int, selected=False, text=None):
        super().__init__()
        self.page_number = page_number                # 该按钮代表的页码（数字或特殊符号）
        self.text = str(page_number) if text is None else text  # 显示的文字
        self.selected = selected                      # 当前是否为选中页
        self.hovered = False                          # 是否鼠标悬浮
        self.setFixedSize(32, 32)                     # 设置固定大小
        # self.setMouseTracking(True)                   # 启用悬浮跟踪

    def paintEvent(self, event):
        # 自定义绘制按钮
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置背景颜色
        if self.selected:
            painter.setBrush(QColor("#00BFFF"))     # 当前页蓝色
        elif self.hovered:
            painter.setBrush(QColor("#E0F7FF"))     # 悬浮时淡蓝
        else:
            painter.setBrush(QColor("#F0F0F0"))     # 默认灰色

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 6, 6)    # 画圆角背景

        # 设置字体和文字颜色
        painter.setPen(Qt.white if self.selected else Qt.black)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() is Qt.LeftButton:
            self.clicked.emit(self.page_number)  # 发出点击信号


class Pager(QWidget):
    def __init__(self, total_pages=20, current_page=1, max_visible=5):
        super().__init__()
        self.total_pages = total_pages
        self.current_page = current_page
        self.max_visible = max_visible

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(10, 10, 10, 10)

        obj = QLineEdit()
        methods = [name for name in dir(obj) if callable(getattr(obj, name)) and not name.startswith("__")]
        for _ in methods:
            print(_)

        signals = [
            name for name in dir(obj)
            if not name.startswith("__")
               and not callable(getattr(obj, name))
        ]
        print(signals)

        # 跳页输入框
        self.jump_input = QLineEdit()
        self.jump_input.setObjectName("edit")
        self.jump_input.setFixedWidth(40)
        self.jump_input.setPlaceholderText("页码")
        self.jump_input.returnPressed.connect(self.jump_to_page)

        self.jump_button = QPushButton("跳转")
        self.jump_button.setObjectName('jump')
        self.jump_button.clicked.connect(self.jump_to_page)

        self.build_buttons()

    def build_buttons(self):
        # 清空旧按钮
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget and widget.objectName() not in ["edit", "jump"]:
                widget.setParent(None)
                widget.deleteLater()

        # 首页/上一页
        if self.current_page > 1:
            first_btn = PageButton(1, text="«")
            first_btn.clicked.connect(lambda _: self.on_page_clicked(1))
            self.layout.addWidget(first_btn)

            prev_btn = PageButton(self.current_page - 1, text="‹")
            prev_btn.clicked.connect(lambda _: self.on_page_clicked(self.current_page - 1))
            self.layout.addWidget(prev_btn)

        # 计算页码范围（最多 max_visible 个）
        start = max(1, self.current_page - self.max_visible // 2)
        end = min(self.total_pages, start + self.max_visible - 1)
        if end - start + 1 < self.max_visible:
            start = max(1, end - self.max_visible + 1)

        # 前省略号
        if start > 2:
            self._add_page_button(1)
            self.layout.addWidget(self._ellipsis_label())
        elif start == 2:
            self._add_page_button(1)

        # 中间页码按钮
        for i in range(start, end + 1):
            self._add_page_button(i, selected=(i == self.current_page))

        # 后省略号
        if end < self.total_pages - 1:
            self.layout.addWidget(self._ellipsis_label())
            self._add_page_button(self.total_pages)
        elif end == self.total_pages - 1:
            self._add_page_button(self.total_pages)

        # 下一页/尾页
        if self.current_page < self.total_pages:
            next_btn = PageButton(self.current_page + 1, text="›")
            next_btn.clicked.connect(lambda _: self.on_page_clicked(self.current_page + 1))
            self.layout.addWidget(next_btn)

            last_btn = PageButton(self.total_pages, text="»")
            last_btn.clicked.connect(lambda _: self.on_page_clicked(self.total_pages))
            self.layout.addWidget(last_btn)

        # 添加跳转组件
        self.layout.addWidget(QLabel("跳转到"))
        self.layout.addWidget(self.jump_input)
        self.layout.addWidget(QLabel("页"))
        self.layout.addWidget(self.jump_button)

    def _add_page_button(self, page: int, selected=False):
        btn = PageButton(page, selected=selected)
        btn.clicked.connect(self.on_page_clicked)
        self.layout.addWidget(btn)

    def _ellipsis_label(self):
        # 创建一个"..."的 QLabel
        lbl = QLabel("...")
        lbl.setFixedWidth(20)
        lbl.setAlignment(Qt.AlignCenter)
        return lbl

    def on_page_clicked(self, page: int):
        # 处理页码点击
        self.current_page = page
        self.build_buttons()
        print(f"切换到第 {page} 页")

    def jump_to_page(self):
        # 处理跳页操作
        try:
            page = int(self.jump_input.text())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self.build_buttons()
        except ValueError:
            pass


if __name__ == "__main__":
    def updateButton():
        pager.total_pages = 1000

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)

    pager = Pager(total_pages=100000, current_page=1, max_visible=5)
    layout.addWidget(pager)

    button = QPushButton("set count is 1000", window)
    layout.addWidget(button)
    button.clicked.connect(updateButton)

    window.setWindowTitle("完整分页控件（自绘 + 扩展功能）")
    window.resize(900, 100)
    window.show()
    app.exec()
from PySide6.QtWidgets import (QWidget, QPushButton, QListWidget, QFrame,
                               QVBoxLayout, QApplication, QStyledItemDelegate)
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve, QEvent, QPoint
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics

class Win11ComboBox(QWidget):
    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
        self._current_index = -1
        self._max_visible_items = 5
        self._item_height = 28
        self._animation_duration = 150
        self._dropdown_visible = False

        # 主按钮
        self._button = QPushButton()
        self._button.setCursor(Qt.PointingHandCursor)
        self._button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                background-color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                border-color: #7EB9F3;
            }
        """)
        self._button.clicked.connect(self._toggle_dropdown)

        # 下拉列表
        self._list_widget = QListWidget()
        self._list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list_widget.setFrameShape(QFrame.NoFrame)
        self._list_widget.setFocusPolicy(Qt.NoFocus)
        self._list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: white;
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                padding: 2px;
                outline: none;
            }}
            QListWidget::item {{
                height: {self._item_height}px;
                padding: 0 8px;
                border-radius: 2px;
            }}
            QListWidget::item:hover {{
                background-color: #f0f0f0;
            }}
            QListWidget::item:selected {{
                background-color: #0078D7;
                color: white;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background: transparent;
            }}
            QScrollBar::handle:vertical {{
                background: #c2c2c2;
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        self._list_widget.itemClicked.connect(self._on_item_selected)
        self._list_widget.hide()

        # 安装事件过滤器
        self._list_widget.installEventFilter(self)
        self._button.installEventFilter(self)

        # 自定义委托
        self._list_widget.setItemDelegate(Win11ComboItemDelegate(self._list_widget))

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._button)
        layout.addWidget(self._list_widget)

        # 动画
        self._animation = QPropertyAnimation(self._list_widget, b"maximumHeight")
        self._animation.setDuration(self._animation_duration)
        self._animation.setEasingCurve(QEasingCurve.OutQuad)

        # 全局事件过滤器
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        # 处理全局鼠标点击事件
        if event.type() == QEvent.MouseButtonPress and self._dropdown_visible:
            # 检查点击是否在下拉框或按钮外部
            if (obj != self._list_widget and obj != self._button and
                    not self._list_widget.underMouse() and
                    not self._button.underMouse()):
                self._hide_dropdown()

        return super().eventFilter(obj, event)

    def addItem(self, text):
        self._items.append(text)
        self._list_widget.addItem(text)
        if self._current_index == -1:
            self.setCurrentIndex(0)

    def addItems(self, texts):
        for text in texts:
            self.addItem(text)

    def currentIndex(self):
        return self._current_index

    def currentText(self):
        if 0 <= self._current_index < len(self._items):
            return self._items[self._current_index]
        return ""

    def setCurrentIndex(self, index):
        if 0 <= index < len(self._items):
            self._current_index = index
            self._button.setText(self.currentText())
            self.currentIndexChanged.emit(index)
            self.currentTextChanged.emit(self.currentText())

    def count(self):
        return len(self._items)

    def _toggle_dropdown(self):
        if self._dropdown_visible:
            self._hide_dropdown()
        else:
            self._show_dropdown()

    def _show_dropdown(self):
        # 计算合适的高度
        item_count = min(self._max_visible_items, self._list_widget.count())
        content_height = item_count * self._item_height + 4

        # 设置动画
        self._animation.stop()
        self._animation.setStartValue(0)
        self._animation.setEndValue(content_height)

        self._list_widget.show()
        self._list_widget.setMaximumHeight(0)
        self._animation.start()
        self._dropdown_visible = True

        # 更新按钮样式
        self._button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                border: 1px solid #0078D7;
                border-radius: 4px;
                background-color: white;
                min-width: 120px;
            }
        """)

    def _hide_dropdown(self):
        if not self._dropdown_visible:
            return

        self._animation.stop()
        self._animation.setStartValue(self._list_widget.height())
        self._animation.setEndValue(0)
        self._animation.finished.connect(lambda: self._list_widget.hide())
        self._animation.start()
        self._dropdown_visible = False

        # 恢复按钮样式
        self._button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 5px 10px;
                border: 1px solid #d3d3d3;
                border-radius: 4px;
                background-color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                border-color: #7EB9F3;
            }
        """)

    def _on_item_selected(self, item):
        index = self._list_widget.row(item)
        self.setCurrentIndex(index)
        self._hide_dropdown()

    def resizeEvent(self, event):
        self._list_widget.setFixedWidth(self._button.width())
        super().resizeEvent(event)

class Win11ComboItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        # 绘制分隔线
        if index.row() < self.parent().count() - 1:
            painter.save()
            painter.setPen(QPen(QColor("#e5e5e5"), 1))
            bottom = option.rect.bottom()
            painter.drawLine(option.rect.left() + 8, bottom,
                             option.rect.right() - 8, bottom)
            painter.restore()

if __name__ == "__main__":
    app = QApplication([])

    combo = Win11ComboBox()
    combo.addItems(["Windows 11", "macOS", "Linux", "Android", "iOS"])
    combo.currentIndexChanged.connect(lambda i: print(f"选中索引: {i}"))
    combo.currentTextChanged.connect(lambda t: print(f"选中文本: {t}"))

    window = QWidget()
    layout = QVBoxLayout(window)
    layout.addWidget(combo)
    layout.addStretch()
    window.resize(300, 200)
    window.show()

    app.exec()
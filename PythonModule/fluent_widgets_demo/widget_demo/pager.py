# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, Signal

from FluentWidgets import SplitWidget, TransparentToolButton, FluentIcon, BodyLabel, LineEdit, themeColor, \
    setFont


class PageButton(QWidget):
    clicked = Signal(int)

    def __init__(self, page: int, selected=False, parent=None):
        super().__init__(parent)
        self.page = page
        self._text = str(page)
        self._isSelected = selected
        self.setFixedSize(32, 32)

    def setSelected(self, isSelected: bool):
        if self._isSelected == isSelected:
            return
        self._isSelected = isSelected
        self.update()

    def isSelected(self):
        return self._isSelected

    def setData(self, name: str, value):
        setattr(self, name, value)

    def getData(self, name: str):
        try:
            return getattr(self, name)
        except AttributeError:
            return None

    def mouseReleaseEvent(self, event):
        if event.button() is Qt.LeftButton:
            self.clicked.emit(self.page)
        self._isSelected = not self._isSelected
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(Qt.NoPen)
        rect = self.rect()
        if self._isSelected:
            painter.setBrush(themeColor())
        else:
            painter.setBrush(QColor(255, 255, 255))
        painter.drawRoundedRect(rect, 6, 6)

        painter.setPen(QColor(255, 255, 255) if self._isSelected else QColor(0, 0, 0))
        painter.drawText(rect, Qt.AlignCenter, self._text)


class Pager(QWidget):
    def __init__(self, pages: int, maxVisible: int, parent=None):
        super().__init__(parent)
        self._pages = pages
        self._currentPage = 0
        self._maxVisible = maxVisible

        self._widgetLayout = QHBoxLayout(self)
        self.__initWidget()
        self.__connectSignalSlot()
        self.__updateButtons()

    def __initWidget(self):
        self.topLabel = QLabel("...", self)
        self.topLabel.setFixedWidth(20)
        self.topLabel.setAlignment(Qt.AlignCenter)

        self.bottomLabel = QLabel("...", self)
        self.bottomLabel.setFixedWidth(20)
        self.bottomLabel.setAlignment(Qt.AlignCenter)

        self.topButton = TransparentToolButton(FluentIcon.LEFT_ARROW, self)
        self.bottomButton = TransparentToolButton(FluentIcon.RIGHT_ARROW, self)

        self.previousButton = TransparentToolButton(FluentIcon.CARE_LEFT_SOLID, self)
        self.nextButton = TransparentToolButton(FluentIcon.CARE_RIGHT_SOLID, self)

        self.jumpLabel = QLabel("跳转到")
        self.countLabel = QLabel(f"页 共计 {self._pages} 页")

        self.jumpEdit = LineEdit(self)
        self.jumpEdit.setFixedWidth(50)

    def __connectSignalSlot(self):
        self.topButton.clicked.connect(lambda: self._onClicked(1))
        self.bottomButton.clicked.connect(lambda: self._onClicked(self._pages))
        self.previousButton.clicked.connect(lambda: self._onClicked(self._currentPage - 1))
        self.nextButton.clicked.connect(lambda: self._onClicked(self._currentPage + 1))
        self.jumpEdit.returnPressed.connect(self.jumpToPage)

    def __updateButtons(self):
        for i in reversed(range(self._widgetLayout.count())):
            widget = self._widgetLayout.itemAt(i).widget()
            widget.setParent(None)

        self._widgetLayout.addWidget(self.topButton)
        self._widgetLayout.addWidget(self.previousButton)
        enable = self._currentPage > 1
        self.topButton.setEnabled(enable)
        self.previousButton.setEnabled(enable)

        start = max(1, self._currentPage - self._maxVisible // 2)
        end = min(self._pages, start + self._maxVisible - 1)
        if end - start + 1 < self._maxVisible:
            start = max(1, end - self._maxVisible + 1)

        if start > 2:
            self._addButtonToPage(1)
            self._widgetLayout.addWidget(self.topLabel)
        elif start == 2:
            self._addButtonToPage(1)

        for i in range(start, end + 1):
            self._addButtonToPage(i, selected=(i == self._currentPage))

        if end < self._pages - 1:
            self._widgetLayout.addWidget(self.bottomLabel)
            self._addButtonToPage(self._pages)
        elif end == self._pages - 1:
            self._addButtonToPage(self._pages)

        enable = self._currentPage < self._pages
        self._widgetLayout.addWidget(self.nextButton)
        self._widgetLayout.addWidget(self.bottomButton)
        self.nextButton.setEnabled(enable)
        self.bottomButton.setEnabled(enable)

        self._widgetLayout.addWidget(self.jumpLabel)
        self._widgetLayout.addWidget(self.jumpEdit)
        self._widgetLayout.addWidget(self.countLabel)

    def currentPage(self):
        return self._currentPage

    def count(self):
        return self._pages

    def maxVisible(self):
        return self._maxVisible

    def setPages(self, number: int):
        self._pages = number
        self.countLabel.setText(f"页 共计 {self._pages} 页")
        self.__updateButtons()

    def setCurrentPage(self, page: int):
        self._currentPage = page
        self._onClicked(page)

    def setMaxVisible(self, number: int):
        if self._maxVisible == number:
            return
        self._maxVisible = number
        self.__updateButtons()

    def _addButtonToPage(self, number: int, selected=False):
        button = PageButton(number, selected, self)
        button.clicked.connect(self._onClicked)
        self._widgetLayout.addWidget(button)

    def _onClicked(self, page: int):
        self._currentPage = page
        self.__updateButtons()
        print(f"切换到{page}页")

    def jumpToPage(self):
        try:
            page = int(self.jumpEdit.text())
            if 1 <= page <= self._pages:
                self._currentPage = page
                self.__updateButtons()
        except ValueError: ...


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)

        self.pager = Pager(5, 5, self)
        self.pager.setCurrentPage(1)
        self.pager.topLabel.hide()
        self.pager.bottomLabel.hide()

        self.box.addWidget(self.pager, 0, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.windowEffect.setMicaEffect(window.winId(), isAlt=True)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
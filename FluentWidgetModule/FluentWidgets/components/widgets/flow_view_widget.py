from PySide6.QtCore import Qt, QTimer, QRect, QModelIndex, QEvent
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QStyleOptionViewItem

from ...common.font import getFont
from ..widgets import HorizontalFlipView, FlipImageDelegate


class FlipViewWidget(HorizontalFlipView):
    """ 翻转视图组件 """
    def __init__(self, parent=None, aspectRation=Qt.AspectRatioMode.KeepAspectRatio):
        super().__init__(parent)
        self.__index = 0
        self.__num = 1
        self.setAspectRatioMode(aspectRation)
        self.setBorderRadius(24)
        parent.installEventFilter(self)

    def setDelegate(
            self,
            color: QColor,
            fontSize: int,
            fontColor: QColor,
            text: str,
            width: int = None,
            height: int = None
    ):
        self.setItemDelegate(FlipItemDelegate(color, fontSize, fontColor, text, width, height, self))

    def enableAutoPlay(self, interval: int = 1500):
        """ set image autoPlay """
        self.currentIndexChanged.connect(lambda index: self.__setIndex(index))
        self.__initTimer(interval)

    def setAutoPlayInterval(self, interval: int):
        self.timer.setInterval(interval)

    def __initTimer(self, interval: int = 1500):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: (self.__updateIndex(), self.__setIndex(self.__index + self.__num)))
        self.timer.start(interval)

    def __updateIndex(self):
        if self.__index == 0:
            self.__num = 1
        if self.__index == self.count() - 1:
            self.__num = -1
        self.setCurrentIndex(self.__index)

    def __setIndex(self, index: int):
        self.__index = index

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            self.setItemSize(self.size())
        return super().eventFilter(obj, event)


class FlipItemDelegate(FlipImageDelegate):
    def __init__(
            self,
            color: QColor,
            fontSize: int,
            fontColor: QColor,
            text: str,
            width: int = None,
            height: int = None,
            parent=None
    ):
        super().__init__(parent)
        self.color = color
        self.width = width
        self.height = height
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.text = text

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        painter.save()

        painter.setBrush(self.color)
        painter.setPen(Qt.PenStyle.NoPen)
        rect = option.rect
        rect = QRect(rect.x(), rect.y(), self.width or 200, self.height or rect.height())
        painter.drawRect(rect)

        painter.setPen(self.fontColor)
        painter.setFont(getFont(self.fontSize, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text)

        painter.restore()
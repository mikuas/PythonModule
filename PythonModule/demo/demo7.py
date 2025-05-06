# coding:utf-8
import sys
from enum import Enum

from PySide6.QtCore import QRectF, QModelIndex, Signal, QSize, Property
from PySide6.QtGui import Qt, QPainter, QColor
from PySide6.QtWidgets import QWidget, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QListWidget, QListWidgetItem, \
    QApplication
from qfluentwidgets import PipsScrollButtonDisplayMode, PopUpAniStackedWidget, Theme, setTheme, ToolButton, isDarkTheme, \
    drawIcon, SmoothScrollBar, FluentStyleSheet, FluentIcon, ToolTipFilter, ToolTipPosition, TitleLabel
from FluentWidgets import VBoxLayout, HBoxLayout
from qfluentwidgets.common.overload import singledispatchmethod


class PipsScrollButtonDisplayMode(Enum):
    """ Pips pager scroll button display mode """
    ALWAYS = 0
    ON_HOVER = 1
    NEVER = 2


class ScrollButton(ToolButton):
    """ Scroll button """

    def _postInit(self):
        self.setFixedSize(12, 12)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if isDarkTheme():
            color = QColor(255, 255, 255)
            painter.setOpacity(0.773 if self.isHover or self.isPressed else 0.541)
        else:
            color = QColor(0, 0, 0)
            painter.setOpacity(0.616 if self.isHover or self.isPressed else 0.45)

        if self.isPressed:
            rect = QRectF(3, 3, 6, 6)
        else:
            rect = QRectF(2, 2, 8, 8)

        drawIcon(self._icon, painter, rect, fill=color.name())


class PipsDelegate(QStyledItemDelegate):
    """ Pips delegate """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hoveredRow = -1
        self.pressedRow = -1

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        isHover = index.row() == self.hoveredRow
        isPressed = index.row() == self.pressedRow

        # draw pip
        if isDarkTheme():
            if isHover or isPressed:
                color = QColor(255, 255, 255, 197)
            else:
                color = QColor(255, 255, 255, 138)
        else:
            if isHover or isPressed:
                color = QColor(0, 0, 0, 157)
            else:
                color = QColor(0, 0, 0, 114)

        painter.setBrush(color)

        # if option.state & QStyle.State_Selected or (isHover and not isPressed):
        #     r = 4
        # else:
        #     r = 3
        #
        # x = option.rect.x() + 6 - r
        # y = option.rect.y() + 6 - r
        # painter.drawEllipse(QRectF(x, y, 2*r, 2*r))

        # 设置半径
        if option.state & QStyle.State_Selected or (isHover and not isPressed):
            r = 6  # 增大正方形尺寸
        else:
            r = 5  # 默认正方形尺寸

        # 计算x和y的位置
        x = option.rect.x() + 6 - r + (index.row() * (2 * r + 0))
        y = option.rect.y() + 6 - r
        size = 2 * r  # 正方形的边长
        corner_radius = r / 3  # 圆角半径，设置为边长的1/3

        # 绘制带一点圆角的正方形
        painter.drawRoundedRect(QRectF(x, y, size, size), corner_radius, corner_radius)

        painter.restore()

    def setPressedRow(self, row: int):
        self.pressedRow = row
        self.parent().viewport().update()

    def setHoveredRow(self, row: bool):
        self.hoveredRow = row
        self.parent().viewport().update()


class PipsPager(QListWidget):
    """ Pips pager

    Constructors
    ------------
    * PipsPager(`parent`: QWidget = None)
    * PipsPager(`orient`: Qt.Orientation, `parent`: QWidget = None)
    """

    currentIndexChanged = Signal(int)

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.orientation = Qt.Horizontal
        self._postInit()

    @__init__.register
    def _(self, orientation: Qt.Orientation, parent=None):
        super().__init__(parent=parent)
        self.orientation = orientation
        self._postInit()

    def _postInit(self):
        self._visibleNumber = 5
        self.isHover = False

        self.delegate = PipsDelegate(self)
        self.scrollBar = SmoothScrollBar(self.orientation, self)

        self.scrollBar.setScrollAnimation(500)
        self.scrollBar.setForceHidden(True)

        self.setMouseTracking(True)
        self.setUniformItemSizes(True)
        self.setGridSize(QSize(12, 12))
        self.setItemDelegate(self.delegate)
        self.setMovement(QListWidget.Static)
        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        FluentStyleSheet.PIPS_PAGER.apply(self)

        if self.isHorizontal():
            self.setFlow(QListWidget.LeftToRight)
            self.setViewportMargins(15, 0, 15, 0)
            self.preButton = ScrollButton(FluentIcon.CARE_LEFT_SOLID, self)
            self.nextButton = ScrollButton(FluentIcon.CARE_RIGHT_SOLID, self)
            self.setFixedHeight(12)

            self.preButton.installEventFilter(ToolTipFilter(self.preButton, 1000, ToolTipPosition.LEFT))
            self.nextButton.installEventFilter(ToolTipFilter(self.nextButton, 1000, ToolTipPosition.RIGHT))

        else:
            self.setViewportMargins(0, 15, 0, 15)
            self.preButton = ScrollButton(FluentIcon.CARE_UP_SOLID, self)
            self.nextButton = ScrollButton(FluentIcon.CARE_DOWN_SOLID, self)
            self.setFixedWidth(12)

            self.preButton.installEventFilter(ToolTipFilter(self.preButton, 1000, ToolTipPosition.TOP))
            self.nextButton.installEventFilter(ToolTipFilter(self.nextButton, 1000, ToolTipPosition.BOTTOM))

        self.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.NEVER)
        self.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.NEVER)
        self.preButton.setToolTip(self.tr('上一页'))
        self.nextButton.setToolTip(self.tr('下一页'))

        # connect signal to slot
        self.preButton.clicked.connect(self.scrollPrevious)
        self.nextButton.clicked.connect(self.scrollNext)
        self.itemPressed.connect(self._setPressedItem)
        self.itemEntered.connect(self._setHoveredItem)

    def _setPressedItem(self, item: QListWidgetItem):
        self.delegate.setPressedRow(self.row(item))
        self.setCurrentIndex(self.row(item))

    def _setHoveredItem(self, item: QListWidgetItem):
        self.delegate.setHoveredRow(self.row(item))

    def setPageNumber(self, n: int):
        """ set the number of page """
        self.clear()
        self.addItems(['15555'] * n)

        for i in range(n):
            item = self.item(i)
            item.setData(Qt.UserRole, i + 1)
            item.setSizeHint(self.gridSize())

        self.setCurrentIndex(0)
        self.adjustSize()

    def getPageNumber(self):
        """ get the number of page """
        return self.count()

    def getVisibleNumber(self):
        """ get the number of visible pips """
        return self._visibleNumber

    def setVisibleNumber(self, n: int):
        self._visibleNumber = n
        self.adjustSize()

    def scrollNext(self):
        """ scroll down an item """
        self.setCurrentIndex(self.currentIndex() + 1)

    def scrollPrevious(self):
        """ scroll up an item """
        self.setCurrentIndex(self.currentIndex() - 1)

    def scrollToItem(self, item: QListWidgetItem, hint=QListWidget.PositionAtCenter):
        """ scroll to item """
        # scroll to center position
        index = self.row(item)
        size = item.sizeHint()
        s = size.width() if self.isHorizontal() else size.height()
        self.scrollBar.scrollTo(s * (index - self.visibleNumber // 2))

        # clear selection
        self.clearSelection()
        item.setSelected(False)

        self.currentIndexChanged.emit(index)

    def adjustSize(self) -> None:
        m = self.viewportMargins()

        if self.isHorizontal():
            w = self.visibleNumber * self.gridSize().width() + m.left() + m.right()
            self.setFixedWidth(w)
        else:
            h = self.visibleNumber * self.gridSize().height() + m.top() + m.bottom()
            self.setFixedHeight(h)

    def isHorizontal(self):
        return self.orientation == Qt.Horizontal

    def setCurrentIndex(self, index: int):
        """ set current index """
        if not 0 <= index < self.count():
            return

        item = self.item(index)
        self.scrollToItem(item)
        super().setCurrentItem(item)

        self._updateScrollButtonVisibility()

    def isPreviousButtonVisible(self):
        if self.currentIndex() <= 0 or self.previousButtonDisplayMode == PipsScrollButtonDisplayMode.NEVER:
            return False

        if self.previousButtonDisplayMode == PipsScrollButtonDisplayMode.ON_HOVER:
            return self.isHover

        return True

    def isNextButtonVisible(self):
        if self.currentIndex() >= self.count() - 1 or self.nextButtonDisplayMode == PipsScrollButtonDisplayMode.NEVER:
            return False

        if self.nextButtonDisplayMode == PipsScrollButtonDisplayMode.ON_HOVER:
            return self.isHover

        return True

    def currentIndex(self):
        return super().currentIndex().row()

    def setPreviousButtonDisplayMode(self, mode: PipsScrollButtonDisplayMode):
        """ set the display mode of previous button """
        self.previousButtonDisplayMode = mode
        self.preButton.setVisible(self.isPreviousButtonVisible())

    def setNextButtonDisplayMode(self, mode: PipsScrollButtonDisplayMode):
        """ set the display mode of next button """
        self.nextButtonDisplayMode = mode
        self.nextButton.setVisible(self.isNextButtonVisible())

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.delegate.setPressedRow(-1)

    def enterEvent(self, e):
        super().enterEvent(e)
        self.isHover = True
        self._updateScrollButtonVisibility()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self.isHover = False
        self.delegate.setHoveredRow(-1)
        self._updateScrollButtonVisibility()

    def _updateScrollButtonVisibility(self):
        self.preButton.setVisible(self.isPreviousButtonVisible())
        self.nextButton.setVisible(self.isNextButtonVisible())

    def wheelEvent(self, e):
        pass

    def resizeEvent(self, e):
        w, h = self.width(), self.height()
        bw, bh = self.preButton.width(), self.preButton.height()

        if self.isHorizontal():
            self.preButton.move(0, int(h/2 - bh/2))
            self.nextButton.move(w - bw, int(h/2 - bh/2))
        else:
            self.preButton.move(int(w/2-bw/2), 0)
            self.nextButton.move(int(w/2-bw/2), h-bh)

    visibleNumber = Property(int, getVisibleNumber, setVisibleNumber)
    pageNumber = Property(int, getPageNumber, setPageNumber)


class HorizontalPipsPager(PipsPager):
    """ Horizontal pips pager """

    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)


class VerticalPipsPager(PipsPager):
    """ Vertical pips pager """

    def __init__(self, parent=None):
        super().__init__(Qt.Vertical, parent)


class PagerWidgetBase(QWidget):
    """ pager widget base class """

    def __init__(self, parent=None, orientation=Qt.Orientation.Vertical):
        super().__init__(parent)
        self.__toggle = True
        self._pager = PipsPager(orientation, self)
        self._stackedWidget = PopUpAniStackedWidget(self)
        self._pager.currentIndexChanged.connect(lambda index: self._stackedWidget.setCurrentIndex(index))
        self.__widgets = []  # type: [QWidget]
        setTheme(Theme.AUTO)

    def addWidget(self, widget: QWidget, deltaX=0, deltaY=76):
        """ add widget to stacked widget """
        self._stackedWidget.addWidget(widget, deltaX, deltaY)
        self._addToWidgets(widget)
        self._pager.setPageNumber(len(self.getAllWidget()))
        return self

    def addWidgets(self, widgets: list[QWidget]):
        """ add widgets to stacked widget """
        for widget in widgets:
            self.addWidget(widget)
        return self

    def setCurrentIndex(self, index: int):
        """ set current page index """
        self._pager.setCurrentIndex(index)

    def removeWidget(self, index: int):
        """ remove widget from stacked widget """
        if index < len(self.__widgets):
            self._stackedWidget.removeWidget(self.__widgets.pop(index))
            self._pager.setPageNumber(len(self.__widgets))
        return self

    def _addToWidgets(self, widget: QWidget):
        if widget in self.__widgets:
            return
        self.__widgets.append(widget)

    def enableScrollTogglePage(self, enable: bool):
        self.toggle = enable

    def displayNextButton(self):
        """ set next page button display """
        self._pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        return self

    def displayPrevButton(self):
        """ set previous page button display """
        self._pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        return self

    def hoverDisplayPrevButton(self):
        """ set previous page button hover display """
        self._pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)
        return self

    def hoverDisplayNextButton(self):
        """ set next page button hover display """
        self._pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)
        return self

    def setPageVisible(self, visible: bool):
        """ set page visible flag """
        self._pager.setVisible(visible)
        return self

    def setVisibleNumber(self, number: int):
        """ set page visible flag """
        self._pager.setVisibleNumber(number)
        return self

    def setStackedFixedSize(self, width: int, height: int):
        self._stackedWidget.setFixedSize(width, height)
        return self

    def setStackedMinSize(self, width: int, height: int):
        self._stackedWidget.setMinimumSize(width, height)
        return self

    def getPageNumber(self):
        return self._pager.getPageNumber()

    def getAllWidget(self):
        """ get stacked all widget """
        return self.__widgets

    def _initLayout(self):
        self.__layout = HBoxLayout(self)
        self.__layout.addWidget(self._stackedWidget)
        self.__layout.addWidget(self._pager, alignment=Qt.AlignmentFlag.AlignRight)

    def getCurrentIndex(self):
        return self._pager.currentIndex()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        if self.__toggle:
            index = self.getCurrentIndex()
            if event.angleDelta().y() > 0:
                if index == 0:
                    return
                self.setCurrentIndex(index - 1)
            else:
                if index == self.getPageNumber() - 1:
                    return
                self.setCurrentIndex(index + 1)


class VerticalPagerWidget(PagerWidgetBase):
    """ 垂直分页器 """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self._initLayout()

    def addWidget(self, widget: QWidget, deltaX=76, deltaY=0):
        """ add widget to stacked widget """
        self._stackedWidget.addWidget(widget, deltaX, deltaY)
        self._addToWidgets(widget)
        self._pager.setPageNumber(len(self.getAllWidget()))
        return self

    def _initLayout(self):
        self.__layout = VBoxLayout(self)
        self.__layout.addWidget(self._stackedWidget)
        self.__layout.addWidget(self._pager, alignment=Qt.AlignmentFlag.AlignHCenter)


class HorizontalPagerWidget(PagerWidgetBase):
    """ 水平分页器 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initLayout()


if __name__ == '__main__':
    class Window(QWidget):
        def __init__(self):
            super().__init__()
            self.resize(800, 500)
            self.page = VerticalPagerWidget(self)
            self.page.setFixedSize(self.size())

            for _ in range(5):
                self.page.addWidget(TitleLabel(f"Page {_ + 1}", self))


    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
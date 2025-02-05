# coding:utf-8
from PySide6.QtCore import QEasingCurve, QModelIndex, QRect, QTimer, Signal, QEvent
from PySide6.QtGui import Qt, QPainter, QColor, QFont
from PySide6.QtWidgets import QWidget, QStyleOptionViewItem, QLabel, QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (
    SubtitleLabel, LineEdit, ColorDialog as Color, FlowLayout, FlipImageDelegate, getFont,
    HorizontalFlipView, BodyLabel, PrimaryPushButton, TextWrap, FluentStyleSheet, MaskDialogBase,
)
from qframelesswindow import FramelessDialog

from .scroll_widget import SmoothScrollWidget


class UiMessageBox:
    """ Ui of message box """

    yesSignal = Signal()
    cancelSignal = Signal()

    def __init__(self, *args, **kwargs):
        pass

    def _setUpUi(self, title, content, parent):
        self.content = content
        self.titleLabel = QLabel(title, parent)
        self.contentLabel = BodyLabel(content, parent)

        self.buttonGroup = QFrame(parent)
        self.yesButton = PrimaryPushButton(self.tr('确定'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('取消'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(parent)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/19
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(81)

        self.contentLabel.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._adjustText()

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def _adjustText(self):
        if self.isWindow():
            if self.parent():
                w = max(self.titleLabel.width(), self.parent().width())
                chars = max(min(w / 9, 140), 30)
            else:
                chars = 100
        else:
            w = max(self.titleLabel.width(), self.window().width())
            chars = max(min(w / 9, 100), 30)

        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.textLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.textLayout.setSpacing(12)
        self.textLayout.setContentsMargins(24, 24, 24, 24)
        self.textLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, Qt.AlignTop)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def __onCancelButtonClicked(self):
        self.reject()
        self.cancelSignal.emit()

    def __onYesButtonClicked(self):
        self.accept()
        self.yesSignal.emit()

    def __setQss(self):
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')

        FluentStyleSheet.DIALOG.apply(self)
        FluentStyleSheet.DIALOG.apply(self.contentLabel)

        self.yesButton.adjustSize()
        self.cancelButton.adjustSize()

    def setContentCopyable(self, isCopyable: bool):
        """ set whether the content is copyable """
        if isCopyable:
            self.contentLabel.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse)
        else:
            self.contentLabel.setTextInteractionFlags(
                Qt.TextInteractionFlag.NoTextInteraction)


class MessageBoxBase(MaskDialogBase):
    """ Message box base """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hide()
        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('确定'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('取消'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/19
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        self.yesButton.setAttribute(Qt.WA_MacShowFocusRect, False)

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(81)

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def validate(self) -> bool:
        """ validate the data of form before closing dialog

        Returns
        -------
        isValid: bool
            whether the data of form is legal
        """
        return True

    def __onCancelButtonClicked(self):
        self.reject()

    def __onYesButtonClicked(self):
        if self.validate():
            self.accept()

    def __setQss(self):
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')
        FluentStyleSheet.DIALOG.apply(self)

    def hideYesButton(self):
        self.yesButton.hide()
        self.buttonLayout.insertStretch(0, 1)

    def hideCancelButton(self):
        self.cancelButton.hide()
        self.buttonLayout.insertStretch(0, 1)


class Dialog(FramelessDialog, UiMessageBox):
    """ Dialog box """

    yesSignal = Signal()
    cancelSignal = Signal()

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent=parent)
        self._setUpUi(title, content, self)
        self.hide()

        self.windowTitleLabel = QLabel(title, self)

        self.setResizeEnabled(False)
        self.resize(240, 192)
        self.titleBar.hide()

        self.vBoxLayout.insertWidget(0, self.windowTitleLabel, 0, Qt.AlignTop)
        self.windowTitleLabel.setObjectName('windowTitleLabel')
        FluentStyleSheet.DIALOG.apply(self)
        self.setFixedSize(self.size())

    def setTitleBarVisible(self, isVisible: bool):
        self.windowTitleLabel.setVisible(isVisible)


class MessageBox(MaskDialogBase, UiMessageBox):
    """ Message box """

    yesSignal = Signal()
    cancelSignal = Signal()

    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent=parent)
        self._setUpUi(title, content, self.widget)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.buttonGroup.setMinimumWidth(280)
        self.widget.setFixedSize(
            max(self.contentLabel.width(), self.titleLabel.width()) + 48,
            self.contentLabel.y() + self.contentLabel.height() + 105
        )

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)


class UrlDialog(MessageBoxBase):
    """ 链接对话框 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('打开 URL', self)
        self.urlLineEdit = LineEdit()

        self.urlLineEdit.setPlaceholderText('输入文件、流或者播放列表的 URL')
        self.urlLineEdit.setClearButtonEnabled(True)

        # add widget to layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)

        # set min width
        self.widget.setMinimumWidth(350)


class ColorDialog(Color):
    """ 颜色选择器对话框 """
    def __init__(self, color, title, parent=None, enableAlpha=False):
        super().__init__(color, title, parent, enableAlpha)
        self.cancelButton.setText('取消')
        self.yesButton.setText('确定')
        self.hide()


class CustomDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()
        self.widget.setMinimumSize(parent.width() / 2, parent.height() / 2)

    def addWidget(
            self,
            widget: QWidget,
            stretch: int = 0,
            alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ):
        self.viewLayout.addWidget(widget, stretch, alignment)
        return self

    def setFixedWidth(self, width: int):
        self.widget.setFixedWidth(width)
        return self

    def setFixedHeight(self, height: int):
        self.widget.setFixedHeight(height)
        return self

    def setFixedSize(self, width: int, height: int):
        self.widget.setFixedSize(width, height)
        return self

    def width(self):
        return self.widget.width()

    def height(self):
        return self.widget.height()


class FlowLayoutWidget(SmoothScrollWidget):
    """
    流式布局
    needAni: bool
        whether to add moving animation

    isTight: bool
        whether to use the tight layout when widgets are hidden
    """
    def __init__(self, duration=250, ease=QEasingCurve.Type.InCurve, parent=None, needAni=True, isTight=False):
        # InCurve
        # OutBack
        super().__init__(parent)
        self.__initLayout(duration, ease, needAni, isTight)
        self.__widgets = [] # type: [QWidget]

    def __initLayout(self, duration: int, ease: QEasingCurve.Type, needAni: bool, isTight: bool):
        self.__flowLayout = FlowLayout(needAni=needAni, isTight=isTight)
        self.__flowLayout.setAnimation(duration, ease)
        self.createVBoxLayout().addLayout(self.__flowLayout)

    def addWidget(self, widget: QWidget):
        self.__widgets.append(widget)
        self.__flowLayout.addWidget(widget)
        self.__reLoadWidget()
        return self

    def addWidgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.__widgets.append(widget)
            self.__flowLayout.addWidget(widget)
        self.__reLoadWidget()
        return self

    def __reLoadWidget(self):
        self.__flowLayout.removeAllWidgets()
        for widget in self.__widgets:
            self.__flowLayout.addWidget(widget)


class FlipViewWidget(HorizontalFlipView):
    """ 翻转视图组件 """
    def __init__(self, parent=None, aspectRation: Qt.AspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio):
        super().__init__(parent)
        self.__index = 0
        self.__num = 1
        self.setAspectRatioMode(aspectRation)
        self.setBorderRadius(24)

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
        return self

    def enableAutoPlay(self, interval: int = 1500):
        """ set image autoPlay """
        self.currentIndexChanged.connect(lambda index: self.__setIndex(index))
        self.__initTimer(interval)
        return self

    def setAutoPlayInterval(self, interval: int):
        self.timer.setInterval(interval)
        return self

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setItemSize(self.size())


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
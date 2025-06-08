# coding:utf-8
import sys

from FluentWidgets.common.overload import singledispatchmethod
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup, QLabel, \
    QCompleter
from PySide6.QtGui import QColor, QPainter, QPainterPath, QIcon
from PySide6.QtCore import Qt, QPoint, QRect, QRectF, Property, QSize, QStringListModel

from FluentWidgets import SplitWidget, SubtitleRadioButton, SimpleCardWidget, ElevatedCardWidget, SettingCard, \
    ExpandSettingCard, SimpleExpandGroupSettingCard, ExpandGroupSettingCard, FluentIcon, SplitTitleBar as SB, \
    TitleBar, FluentStyleSheet, LineEdit, Icon, TransparentToolButton, VerticalScrollWidget, SearchLineEdit

from qframelesswindow import TitleBarBase


class CustomTitleBar(TitleBarBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.hBoxLayout = QHBoxLayout(self)
        self.iconLabel = QLabel(self)
        self.titleLabel = QLabel(self)

        self.titleLabel.setObjectName('titleLabel')
        self.iconLabel.setFixedSize(18, 18)

        # add buttons to layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        self.initButton()
        self.window().windowIconChanged.connect(self.setIcon)
        self.window().windowTitleChanged.connect(self.setTitle)

        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def initButton(self):
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight | Qt.AlignTop)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight | Qt.AlignTop)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight | Qt.AlignTop)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class SearchTitleBar(CustomTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initButton(self):
        self.hBoxLayout.addStretch(1)

        self.searchEdit = SearchLineEdit(self)
        self.searchEdit.setClearButtonEnabled(True)
        self.searchEdit.setPlaceholderText("输入网址")

        self.model = QStringListModel(["Hello World", "Hello PySide6", "Hello PyQt6", "Hello Python"], self)
        self.completer = QCompleter(self.model, self)

        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # 设置匹配位置
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains) # 设置是否区分大小写
        self.completer.setMaxVisibleItems(100)
        self.searchEdit.setCompleter(self.completer)

        self.model.setStringList(
            [f"Item {_}" for _ in range(1, 101)]
        )

        self.hBoxLayout.addWidget(self.searchEdit, 0, Qt.AlignBottom)
        super().initButton()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.searchEdit.setFixedWidth(self.width() / 3)

class SubtitleRadioButtonDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setTitleBar(SearchTitleBar(self))
        self.setWindowTitle("SubtitleRadioButtonDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(5, 55, 5, 0)

        self.buttonGroup = QButtonGroup(self)

        self.subRadio1 = SubtitleRadioButton("扬声器", "Realted(R) Audio", self)
        self.subRadio2 = SubtitleRadioButton("耳机", "ProjectML(R) Audio", self)
        self.subRadio3 = SubtitleRadioButton("音量", "Aird(R) Audio", self)
        self.subRadio4 = SubtitleRadioButton("空间音效", "Realted(R) Audio", self)
        self.subRadio5 = SubtitleRadioButton("显示模式", "Realted(R) Audio", self)

        self.subRadio5.setSubText('None')

        self.buttonGroup.addButton(self.subRadio1)
        self.buttonGroup.addButton(self.subRadio2)
        self.buttonGroup.addButton(self.subRadio3)
        self.buttonGroup.addButton(self.subRadio4)
        self.buttonGroup.addButton(self.subRadio5)

        self.buttonGroup.setExclusive(False)

        self.box.addWidget(self.subRadio1)
        self.box.addWidget(self.subRadio2)
        self.box.addWidget(self.subRadio3)
        self.box.addWidget(self.subRadio4)
        self.box.addWidget(self.subRadio5)

        self.settingCard = SettingCard(FluentIcon.HOME, "SettingCard", "Content", self)
        self.expandSettingCard = ExpandSettingCard(FluentIcon.HOME, "ExpandSettingCard", "Content", self)
        self.expandGroupSettingCard = ExpandGroupSettingCard(FluentIcon.HOME, "ExpandGroupSettingCard", "Content", self)

        self.expandGroupSettingCard.view.setContentsMargins(10, 0, 0, 0)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio1)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio2)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio3)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio4)
        self.expandGroupSettingCard.addGroupWidget(self.subRadio5)

        self.box.addWidget(self.settingCard)
        self.box.addWidget(self.expandSettingCard)
        self.box.addWidget(self.expandGroupSettingCard)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubtitleRadioButtonDemo()
    window.setMinimumSize(800, 520)
    window.show()
    sys.exit(app.exec())

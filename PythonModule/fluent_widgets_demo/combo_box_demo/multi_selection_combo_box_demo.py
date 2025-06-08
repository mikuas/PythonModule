# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt

from FluentWidgets import SplitWidget, MultiSelectionComboBox, Icon, WinFluentIcon, PopupDrawerWidget, \
    TransparentPushButton, TitleLabel, RoundPushButton, ToastInfoBar, CheckBox, LineEdit, ToastInfoBarPosition, \
    HorizontalSeparator


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MultiSelectionComboBoxDemo")
        self.setWindowIcon(QIcon(":/icons/Honkai_Impact_3.ico"))
        self.windowEffect.setMicaEffect(self.winId(), isAlt=True)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(10, 40, 10, 0)

        self.multiSelectionComboBox = MultiSelectionComboBox(self, "请选择你的老婆")

        self.popDrawerWidget = PopupDrawerWidget("Settings", parent=self)
        self.popDrawerWidget.setFixedWidth(400)
        self.popDrawerWidget.setClickParentHide(True)
        self.button = TransparentPushButton("Show Setting Drawer", self)

        self.multiSelectionComboBox.selectedChange.connect(
            lambda item: print([i.text() for i in item])
        )
        self.multiSelectionComboBox.enableClearButton(True)
        self.multiSelectionComboBox.addItems([
            "绫地宁宁", "因幡爱瑠", "椎叶䌷", "亚托莉", "朝武芳乃", "丛雨", "常陆茉子", "上坂茅羽耶", "矢来美羽", "在原七海",
            "三司绫濑", "式部茉优", "二条院羽月", "和泉妃爱", "常盘华乃", "锦明日海", "镰仓诗樱", "结城明日奈", "小鸟游六花",
            "御坂美琴", "佐天泪子", "后藤一里", "山田凉", "伊地知虹夏", "喜多郁代", "我是一个很长很长很长的测试文字"
        ])
        self.multiSelectionComboBox.setMaxVisibleItems(6)

        self.button.clicked.connect(lambda: {
            self.popDrawerWidget.popDrawer(self.popDrawerWidget.isPopup),
        })

        self.box.addWidget(self.multiSelectionComboBox, 0, Qt.AlignTop)
        self.box.addWidget(self.button, 0, Qt.AlignBottom)
        self.box.addSpacing(24)

        self.initPopDrawer()

    def initPopDrawer(self):
        self.popDrawerWidget.addWidget(TitleLabel(""), alignment=Qt.AlignHCenter)
        self.selectAllButton = RoundPushButton("选中全部", self)
        self.selectAllButton.clicked.connect(self.selectedAllItem)

        self.popDrawerWidget.addWidget(self.selectAllButton)
        self.popDrawerWidget.vBoxLayout.addSpacing(10)

        self.checkBox = CheckBox("启用清除选中的Item按钮", self)
        self.checkBox.setChecked(True)
        self.checkBox.checkStateChanged.connect(lambda: self.multiSelectionComboBox.enableClearButton(self.checkBox.isChecked()))

        self.popDrawerWidget.addWidget(self.checkBox, alignment=Qt.AlignHCenter)

        self.popDrawerWidget.vBoxLayout.addSpacing(10)
        self.popDrawerWidget.addWidget(HorizontalSeparator(self.popDrawerWidget))
        self.popDrawerWidget.vBoxLayout.addSpacing(10)

        self.popDrawerWidget.addWidget(TitleLabel("添加Item"), alignment=Qt.AlignHCenter)
        self.addEdit = LineEdit(self)
        self.addEdit.setClearButtonEnabled(True)
        self.addItemButton = RoundPushButton("添加", self)
        self.addItemButton.clicked.connect(self.addItem)

        self.popDrawerWidget.addWidget(self.addEdit)
        self.popDrawerWidget.addWidget(self.addItemButton)

        self.popDrawerWidget.vBoxLayout.addSpacing(10)
        self.popDrawerWidget.addWidget(HorizontalSeparator(self.popDrawerWidget))
        self.popDrawerWidget.vBoxLayout.addSpacing(10)

        self.popDrawerWidget.addWidget(TitleLabel("删除Item"), alignment=Qt.AlignHCenter)
        self.removeEdit = LineEdit(self)
        self.removeEdit.setClearButtonEnabled(True)
        self.removeItemButton = RoundPushButton("删除", self)
        self.removeItemButton.clicked.connect(self.removeItem)

        self.popDrawerWidget.addWidget(self.removeEdit)
        self.popDrawerWidget.addWidget(self.removeItemButton)

    def addItem(self):
        text = self.addEdit.text()
        if not text or text in self.multiSelectionComboBox._texts:
            ToastInfoBar.error(
                "添加Item",
                "添加 Item 失败, 内容为空或Item已存在",
                duration=1500,
                isClosable=False,
                position=ToastInfoBarPosition.TOP,
                parent=self
            )
            return
        self.multiSelectionComboBox.addItem(text)
        ToastInfoBar.success(
            "添加Item",
            f"添加 Item 成功, 添加的内容是: {text}",
            duration=1500,
            isClosable=False,
            position=ToastInfoBarPosition.TOP,
            parent=self
        )

    def removeItem(self):
        text = self.removeEdit.text()
        if not text or text not in self.multiSelectionComboBox._texts:
            ToastInfoBar.error(
                "删除Item",
                "删除 Item 失败, Item不在List中",
                duration=1500,
                isClosable=False,
                position=ToastInfoBarPosition.TOP,
                parent=self
            )
            return
        self.multiSelectionComboBox.removeItem(text)
        ToastInfoBar.success(
            "删除Item",
            f"删除 Item 成功, 删除的内容是: {text}",
            duration=1500,
            isClosable=False,
            position=ToastInfoBarPosition.TOP,
            parent=self
        )

    def selectedAllItem(self):
        for item in self.multiSelectionComboBox.items():
            self.multiSelectionComboBox.updateCheckedState(item, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.setMinimumSize(800, 520)
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import sys

from PySide6.QtGui import QPainter, Qt, QColor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QButtonGroup
from FluentWidgets import SplitWidget, FluentIcon, Icon, SlidingNavigationWidget, OptionsSettingCard, qconfig, \
    VerticalScrollWidget, PopDrawerWidget, PopDrawerPosition, TitleLabel, CustomColorSettingCard, ColorConfigItem, \
    themeColor, FluentTranslator, SwitchButton, ComboBox, LineEdit
from FluentWidgets.components.widgets.acrylic_label import AcrylicLabel, AcrylicTextureLabel
from FluentWidgets.components.widgets.button import OutlinePushButton, OutlineToolButton, TransparentPushButton


class OutlineButtonDemo(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initTbWidget()
        self.initITbWidget()
        self.initIbWidget()
        self.addLayout(self.itbLayout)
        self.addLayout(self.tbLayout)
        self.addLayout(self.ibLayout)

        self.boxLayout.setAlignment(Qt.AlignTop)

        self.button = TransparentPushButton("设置", self)
        self.sp = PopDrawerWidget(self.parent(), "Setting")
        self.sp.setClickParentHide(True)
        self.sp.setMinimumWidth(350)

        self.addWidget(TitleLabel("启用选中互斥"), alignment=Qt.AlignHCenter)
        self.switch = SwitchButton(self)
        self.switch.setChecked(True)
        self.addWidget(self.switch, alignment=Qt.AlignHCenter)
        self.boxLayout.addStretch(1)
        self.addWidget(self.button, alignment=Qt.AlignBottom)

        self.button.clicked.connect(lambda: self.sp.popDrawer(self.sp.isPopup))

        self.buttons = [
            self.tb1, self.tb2, self.tb3, self.tb4,
            self.itb1, self.itb2, self.itb3, self.itb4,
            self.ib1, self.ib2, self.ib3, self.ib4
        ]

        self.buttonGroup = QButtonGroup(self)
        for button in self.buttons:
            self.buttonGroup.addButton(button)
        self.switch.checkedChanged.connect(self.updateGroupButton)

        self.initPopDrawer()

    def updateGroupButton(self, isUpdate):
        self.buttonGroup.setExclusive(isUpdate)
        if isUpdate:
            for button in self.buttons:
                button.setChecked(False)

    def initTbWidget(self):
        self.tb1 = OutlinePushButton("唱", self)
        self.tb2 = OutlinePushButton("跳", self)
        self.tb3 = OutlinePushButton("Rap", self)
        self.tb4 = OutlinePushButton("篮球", self)

        self.tb1.setMinimumWidth(128)
        self.tb2.setMinimumWidth(128)
        self.tb3.setMinimumWidth(128)
        self.tb4.setMinimumWidth(128)

        self.tbLayout = QHBoxLayout()
        self.tbLayout.addWidget(self.tb1)
        self.tbLayout.addWidget(self.tb2)
        self.tbLayout.addWidget(self.tb3)
        self.tbLayout.addWidget(self.tb4)

    def initITbWidget(self):
        self.itb1 = OutlinePushButton("HOME", self, FluentIcon.HOME)
        self.itb2 = OutlinePushButton("GITHUB", self, FluentIcon.GITHUB)
        self.itb3 = OutlinePushButton("MAIL", self, FluentIcon.MAIL)
        self.itb4 = OutlinePushButton("SETTING", self, FluentIcon.SETTING)

        self.itb1.setMinimumWidth(128)
        self.itb2.setMinimumWidth(128)
        self.itb3.setMinimumWidth(128)
        self.itb4.setMinimumWidth(128)

        self.itbLayout = QHBoxLayout()
        self.itbLayout.addWidget(self.itb1)
        self.itbLayout.addWidget(self.itb2)
        self.itbLayout.addWidget(self.itb3)
        self.itbLayout.addWidget(self.itb4)

    def initIbWidget(self):
        self.ib1 = OutlinePushButton(FluentIcon.HOME, self)
        self.ib2 = OutlinePushButton(FluentIcon.GITHUB, self)
        self.ib3 = OutlinePushButton(FluentIcon.MAIL, self)
        self.ib4 = OutlinePushButton(FluentIcon.SETTING, self)

        self.ib1.setMinimumWidth(128)
        self.ib2.setMinimumWidth(128)
        self.ib3.setMinimumWidth(128)
        self.ib4.setMinimumWidth(128)

        self.ibLayout = QHBoxLayout()
        self.ibLayout.addWidget(self.ib1)
        self.ibLayout.addWidget(self.ib2)
        self.ibLayout.addWidget(self.ib3)
        self.ibLayout.addWidget(self.ib4)

    def initPopDrawer(self):
        self.colorCard = CustomColorSettingCard(
            ColorConfigItem('color', 'color', themeColor()),
            FluentIcon.BRUSH,
            "设置OutlineButtonColor",
            "设置颜色",
            self.parent()
        )
        self.sp.addWidget(self.colorCard)
        self.colorCard.colorChanged.connect(self.updateColor)

        self.sp.addWidget(TitleLabel("设置Docker宽度,高度"), alignment=Qt.AlignHCenter)
        self.wEdit = LineEdit(self)
        self.hEdit = LineEdit(self)
        self.wEdit.setPlaceholderText("Width")
        self.hEdit.setPlaceholderText("Height")
        self.editLayout = QHBoxLayout()
        self.editLayout.addWidget(self.wEdit)
        self.editLayout.addWidget(self.hEdit)
        self.sp.addLayout(self.editLayout)

        self.wEdit.textChanged.connect(lambda w: self.sp.setFixedWidth(self.verify(w)))
        self.hEdit.textChanged.connect(lambda h: self.sp.setFixedHeight(self.verify(h)))

    @staticmethod
    def verify(string):
        try:
            return int(string)
        except ValueError:
            return 300

    def updateColor(self, color):
        for button in self.buttons:
            button.setOutlineColor(color)


class SplitWidgetDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False, isAlt=True)
        # self.windowEffect.setAcrylicEffect(self.winId())
        # self.windowEffect.setAeroEffect(self.winId())
        self.setWindowTitle("SplitWidgetDemo")
        self.setWindowIcon(Icon(FluentIcon.GITHUB))

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 25, 0, 0)
        self.nav = SlidingNavigationWidget(self)
        self.box.addWidget(self.nav)

        self.items = {
            "HOME": FluentIcon.HOME,
            "MUSIC": FluentIcon.MUSIC,
            "VIDEOS": FluentIcon.VIDEO,
            "MAIL": FluentIcon.MAIL,
        }

        for key, value in self.items.items():
            self.nav.addSubInterface(
                key, key, OptionsSettingCard(
                    qconfig.themeMode,
                    FluentIcon.BRUSH,
                    "应用主题",
                    "调整你的应用外观",
                    ["浅色", "深色", "跟随系统设置"]
                ), toolTip=key,
                # icon=value
            )
        self.od = OutlineButtonDemo(self)
        self.nav.addSubInterface(
            'outline_demo', "OutlinePushButton",
            self.od
        )

        self.nav._slidingNavigationBar.addStretch(1)
        self.nav._slidingNavigationBar.addItem(
            'SETTINGS',
            "",
            FluentIcon.SETTING,
            lambda: self.od.sp.popDrawer(self.od.sp.isPopup)
        )
        self.nav._slidingNavigationBar.item("SETTINGS").clicked.disconnect(self.nav._slidingNavigationBar._onClicked)
        self.nav.setCurrentWidget("HOME")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('QWidget {background: transparent; border: none;}')
    translator = FluentTranslator()
    app.installTranslator(translator)
    window = SplitWidgetDemo()
    window.setMinimumSize(800, 520)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
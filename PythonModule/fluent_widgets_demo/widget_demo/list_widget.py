# coding:utf-8
import json
import os
import subprocess
import sys
import time

from FluentWidgets.common.icon import toQIcon, ColoredFluentIcon
from FluentWidgets.components.widgets.button import FillPushButton
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QStringListModel, QSize, QModelIndex, QEasingCurve, QTimer

from FluentWidgets import ListWidget, CycleListWidget, SplitWidget, ListView, RoundListWidget, FluentIcon, getFont, \
    InfoBar, ToastInfoBar, InfoBarPosition, ToastInfoBarPosition, setTheme, Theme, theme, ComboBox, TitleLabel, \
    SlidingNavigationWidget, RoundPushButton, RoundToolButton, OutlinePushButton, OutlineToolButton, PushButton, \
    ToolButton, PrimaryPushButton, PrimaryToolButton, isDarkTheme
from pmutils import JsonUtils


class Demo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.themes = {
            "LIGHT": Theme.LIGHT,
            "DARK": Theme.DARK,
            "AUTO": Theme.AUTO
        }

        self.data = {"isReboot": False}

        with open("config.json", 'r', encoding='utf-8') as f:
            f = json.loads(f.read())
            print(sys.argv)
            try:
                self.data = json.loads(sys.argv[-1])
                print(type(self.data), self.data)
                if self.data["isMaximized"]:
                    self.showMaximized()
                    print("MAX")
                else:
                    print("RESIZE")
                    self.resize(self.data["Width"], self.data["Height"])
            except Exception:
                print("DEFAULT RESIZE")
                self.resize(1000, 640)
        setTheme(self.themes[f["Theme"]])
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(50, 35, 50, 10)

        items = [
            '白金之星', '绿色法皇', "天堂制造", "绯红之王",
            '银色战车', '疯狂钻石', "壮烈成仁", "败者食尘",
            "隐者之紫", "黄金体验", "虚无之王", "纸月之王",
            "骇人恶兽", "男子领域", "华丽挚爱", "牙 Act 4",
            "铁球破坏者", "性感手枪", 'D4C • 爱之列车', "天生完美",
            "软又湿", "佩斯利公园", "奇迹于你", "行走的心",
            "护霜旅行者", "十一月雨", "调情圣手", "片刻静候"
        ] + [f"Item {_}" for _ in range(1, 10001)]

        self.roundListWidget = RoundListWidget(self)
        self.listWidget = ListWidget(self)

        self.roundListWidget.addItems(items)
        self.listWidget.addItems(items)

        icon = toQIcon(FluentIcon.HOME)
        # icon = toQIcon(":/icons/Honkai_Star_Rail.ico")

        for item in self.roundListWidget.allItems():
            item.setIcon(icon)

        self.roundListWidget.enableDoubleItemEdit(True)
        self.listWidget.doubleClicked.connect(
            lambda index: self.listWidget.openPersistentEditor(self.listWidget.item(index.row()))
        )

        self.roundListWidget.currentItemChanged.connect(lambda _item_: print(f"点击的项目: {_item_}"))
        self.roundListWidget.currentRowChanged.connect(lambda row: print(f"点击的行数: {row}"))
        self.roundListWidget.currentTextChanged.connect(lambda text: print(f"点击的项的文本: {text}"))

        self.layout = QHBoxLayout()
        self.box.addLayout(self.layout)

        self.layout.addWidget(self.listWidget)
        self.layout.addWidget(self.roundListWidget)

        print(theme())

        self.setMicaEffectEnabled(True)

        self.themeComboBox = ComboBox(self)
        self.themeComboBox.addItems(["LIGHT", "DARK", "AUTO"])

        self.themeComboBox.setCurrentText(str(theme()).split('.')[-1])
        self.themeComboBox.currentTextChanged.connect(self.updateTheme)

        self.box.addWidget(TitleLabel("设置主题颜色", self), 0, Qt.AlignHCenter)
        self.box.addWidget(self.themeComboBox)

        self.navigation = SlidingNavigationWidget(self)
        for _ in range(1, 4):
            title = TitleLabel(f"Interface {_}", self)
            title.setAlignment(Qt.AlignCenter)
            self.navigation.addSubInterface(
                str(_),
                f"Interface {_}",
                title
            )
        title = TitleLabel("Setting Interface", self)
        title.setAlignment(Qt.AlignCenter)
        self.navigation.navigation.addStretch(1)
        self.navigation.addSubInterface(
            "Settings",
            "Setting Interface",
            title
        )

        self.roundListWidget.setItemBorderColor('deeppink')
        self.roundListWidget.setItemTextAlignment(Qt.AlignCenter)
        self.roundListWidget.setAlternatingRowColors(True)
        self.listWidget.setAlternatingRowColors(True)

        self.navigation.setCurrentIndex(0)
        # self.navigation.navigation.setEasingCurve(QEasingCurve.Type.OutCurve)

        self.box.addWidget(self.navigation)

        self.roundButton = RoundPushButton("Re Boot App", self)
        self.roundToolButton = RoundToolButton(FluentIcon.GITHUB, self)
        self.outlineButton = OutlinePushButton("主页", self)
        self.outlineToolButton = OutlineToolButton(FluentIcon.GITHUB, self)

        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(self.roundButton)
        widgetLayout.addWidget(self.roundToolButton)
        widgetLayout.addWidget(self.outlineButton)
        widgetLayout.addWidget(self.outlineToolButton)

        self.box.addLayout(widgetLayout)

        self.pushButton = PushButton("Push Button", self)
        self.toolButton = ToolButton(FluentIcon.GITHUB, self)
        self.primaryButton = PrimaryPushButton("主页", self)
        self.primaryToolButton = PrimaryToolButton(FluentIcon.GITHUB, self)

        widgetLayout = QHBoxLayout()
        widgetLayout.addWidget(self.pushButton)
        widgetLayout.addWidget(self.toolButton)
        widgetLayout.addWidget(self.primaryButton)
        widgetLayout.addWidget(self.primaryToolButton)

        self.box.addLayout(widgetLayout)

        self.roundButton.clicked.connect(self.restart)

        self.roundButton.setEnabled(not self.data["isReboot"])

        self.jsonUtil = JsonUtils()

        self.fillButton = FillPushButton("Toggle Theme", self)
        self.box.addWidget(self.fillButton)
        self.fillButton.clicked.connect(
            lambda: {
                setTheme(Theme.LIGHT) if isDarkTheme() else setTheme(Theme.DARK),
                self.setMicaEffectEnabled(True),
                # QTimer.singleShot(500, self.updateWidget),
                self.updateWidget(),
                print(True)
            }
        )

    @staticmethod
    def updateWidget():
        for w in QApplication.allWidgets():
            print(w)
            try:
                w.update()
            except TypeError:
                w.update(w.currentIndex())

    # @staticmethod
    def restart(self):
        subprocess.Popen([sys.executable] + sys.argv + [
            json.dumps(
                {
                    "isMaximized": self.isMaximized(),
                    "Width": self.width(),
                    "Height": self.height(),
                    # "X": self.x(),
                    # "Y": self.y(),
                    "isReboot": True
                }
            )
        ], close_fds=True)
        time.sleep(1)
        QApplication.quit()

    def updateTheme(self, t: str):
        data = self.jsonUtil.readJsonFile('config.json')
        data["Theme"] = t
        self.jsonUtil.writeJsonFile("config.json", data)
        InfoBar.success(
            "设置主题",
            f"设置的主题色为: {t}, 重启软件后生效",
            duration=2500,
            position=InfoBarPosition.TOP,
            parent=self
        )

        # setTheme(self.themes[data["Theme"]])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    # try:
    #     window.move(window.data["X"], window.data["Y"])
    # except Exception: ...
    sys.exit(app.exec())
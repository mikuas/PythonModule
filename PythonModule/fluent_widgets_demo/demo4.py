# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QComboBox, \
    QCompleter
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt, QStringListModel, QEventLoop, QTimer

from FluentWidgets import FluentWindow, SplitWidget, TopNavigationWindow, TitleLabel, FluentIcon, LineEdit, \
    SearchLineEdit, IconWidget, SplashScreen, SplitTitleBar
from qframelesswindow import TitleBarBase


class W(QWidget):
    def __init__(self, text, icon, parent=None):
        super().__init__(parent)
        self.box = QVBoxLayout(self)

        iw = IconWidget(icon, self)
        iw.setFixedSize(32, 32)
        self.box.addWidget(iw, 0, Qt.AlignCenter)
        self.box.addWidget(TitleLabel(text, self))

        self.box.setAlignment(Qt.AlignCenter)


class Window(TopNavigationWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        self.setWindowTitle("TopNavigationWidget")
        self.setWindowIcon(QIcon(":/icons/Honkai_Star_Rail.ico"))

        self.initBar()
        self.setCurrentWidget("主页")

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.hideTitleBarButton()
        self.show()
        self.splashScreen.run()

        # self.stringListModel = QStringListModel(self)
        # self.stringListModel.setStringList(["Hello World", "Hello PyQt", "Hello Python"])
        # self.completer = QCompleter(self.stringListModel, self)
        # self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        # self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) # 不区分大小写
        #
        # self.edit = SearchLineEdit(self)
        # self.edit.setMinimumWidth(128)
        # self.edit.setClearButtonEnabled(True)
        # self.edit.setCompleter(self.completer)

    def initBar(self):
        data = {
            "主页": FluentIcon.HOME,
            "订阅": FluentIcon.BOOK_SHELF,
            "历史": FluentIcon.HISTORY,
            "下载": FluentIcon.DOWNLOAD,
            "未播放的剧集": FluentIcon.VIDEO,
            "正在播放": FluentIcon.VIDEO
        }
        for text, icon in data.items():
            self.addSubInterface(
                text, text, W(text, icon, self), icon, toolTip=text
            )

        self.navigation.addStretch(1)
        self.addSubInterface(
            "Settings", "", W("Settings", FluentIcon.SETTING, self), FluentIcon.SETTING, False, "Settings"
        )


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.stacked = QStackedWidget(self)
        self.comboBox = QComboBox(self)
        self.box.addWidget(self.stacked)
        self.box.addWidget(self.comboBox)

        self.comboBox.addItems([str(_) for _ in range(5)])
        self.comboBox.setFixedHeight(35)
        self.comboBox.currentIndexChanged.connect(self.changePage)

        self.w = Window()
        self.t1 = TitleLabel("INTERFACE_1", self)
        self.t2 = TitleLabel("INTERFACE_2", self)
        self.t3 = TitleLabel("INTERFACE_3", self)
        self.t4 = TitleLabel("INTERFACE_4", self)

        self.stacked.addWidget(self.w)
        self.stacked.addWidget(self.t1)
        self.stacked.addWidget(self.t2)
        self.stacked.addWidget(self.t3)
        self.stacked.addWidget(self.t4)

        self.items = [self.w, self.t1, self.t2, self.t3, self.t4]

    def changePage(self, index: int):
        self.stacked.setCurrentWidget(self.items[index])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = Demo()
    window = Window()
    window.show()
    sys.exit(app.exec())

# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QVBoxLayout

from FluentWidgets import SlidingNavigationBar, SlidingToolNavigationBar, VerticalScrollWidget, \
    FluentIcon, PopupDrawerWidget, PopupDrawerPosition, PushButton, TitleLabel, ComboBox, LineEdit, SplitWidget


class Widget(VerticalScrollWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.icons = [FluentIcon.UP, FluentIcon.ADD, FluentIcon.BUS, FluentIcon.CAR, FluentIcon.CUT, FluentIcon.IOT, FluentIcon.PIN, FluentIcon.TAG, FluentIcon.VPN, FluentIcon.CAFE, FluentIcon.CHAT, FluentIcon.COPY, FluentIcon.CODE, FluentIcon.DOWN, FluentIcon.EDIT, FluentIcon.FLAG, FluentIcon.FONT, FluentIcon.GAME, FluentIcon.HELP, FluentIcon.HIDE, FluentIcon.HOME, FluentIcon.INFO, FluentIcon.LEAF, FluentIcon.LINK, FluentIcon.MAIL, FluentIcon.MENU, FluentIcon.MUTE, FluentIcon.MORE, FluentIcon.MOVE, FluentIcon.PLAY, FluentIcon.SAVE, FluentIcon.SEND, FluentIcon.SYNC, FluentIcon.UNIT, FluentIcon.VIEW, FluentIcon.WIFI, FluentIcon.ZOOM, FluentIcon.ALBUM, FluentIcon.BRUSH, FluentIcon.BROOM, FluentIcon.CLOSE, FluentIcon.CLOUD, FluentIcon.EMBED, FluentIcon.GLOBE, FluentIcon.HEART, FluentIcon.LABEL, FluentIcon.MEDIA, FluentIcon.MOVIE, FluentIcon.MUSIC, FluentIcon.ROBOT, FluentIcon.PAUSE, FluentIcon.PASTE, FluentIcon.PHOTO, FluentIcon.PHONE, FluentIcon.PRINT, FluentIcon.SHARE, FluentIcon.TILES, FluentIcon.UNPIN, FluentIcon.VIDEO, FluentIcon.TRAIN, FluentIcon.ADD_TO, FluentIcon.ACCEPT, FluentIcon.CAMERA, FluentIcon.CANCEL, FluentIcon.DELETE, FluentIcon.FOLDER, FluentIcon.FILTER, FluentIcon.MARKET, FluentIcon.SCROLL, FluentIcon.LAYOUT, FluentIcon.GITHUB, FluentIcon.UPDATE, FluentIcon.REMOVE, FluentIcon.RETURN, FluentIcon.PEOPLE, FluentIcon.QRCODE, FluentIcon.RINGER, FluentIcon.ROTATE, FluentIcon.SEARCH, FluentIcon.VOLUME, FluentIcon.FRIGID, FluentIcon.SAVE_AS, FluentIcon.ZOOM_IN, FluentIcon.CONNECT, FluentIcon.HISTORY, FluentIcon.SETTING, FluentIcon.PALETTE, FluentIcon.MESSAGE, FluentIcon.FIT_PAGE, FluentIcon.ZOOM_OUT, FluentIcon.AIRPLANE, FluentIcon.ASTERISK, FluentIcon.CALORIES, FluentIcon.CALENDAR, FluentIcon.FEEDBACK, FluentIcon.LIBRARY, FluentIcon.MINIMIZE, FluentIcon.CHECKBOX, FluentIcon.DOCUMENT, FluentIcon.LANGUAGE, FluentIcon.DOWNLOAD, FluentIcon.QUESTION, FluentIcon.SPEAKERS, FluentIcon.DATE_TIME, FluentIcon.FONT_SIZE, FluentIcon.HOME_FILL, FluentIcon.PAGE_LEFT, FluentIcon.SAVE_COPY, FluentIcon.SEND_FILL, FluentIcon.SKIP_BACK, FluentIcon.SPEED_OFF, FluentIcon.ALIGNMENT, FluentIcon.BLUETOOTH, FluentIcon.COMPLETED, FluentIcon.CONSTRACT, FluentIcon.HEADPHONE, FluentIcon.MEGAPHONE, FluentIcon.PROJECTOR, FluentIcon.EDUCATION, FluentIcon.LEFT_ARROW, FluentIcon.ERASE_TOOL, FluentIcon.PAGE_RIGHT, FluentIcon.PLAY_SOLID, FluentIcon.HIGHTLIGHT, FluentIcon.FOLDER_ADD, FluentIcon.PAUSE_BOLD, FluentIcon.PENCIL_INK, FluentIcon.PIE_SINGLE, FluentIcon.QUICK_NOTE, FluentIcon.SPEED_HIGH, FluentIcon.STOP_WATCH, FluentIcon.ZIP_FOLDER, FluentIcon.BASKETBALL, FluentIcon.BRIGHTNESS, FluentIcon.DICTIONARY, FluentIcon.MICROPHONE, FluentIcon.ARROW_DOWN, FluentIcon.FULL_SCREEN, FluentIcon.MIX_VOLUMES, FluentIcon.REMOVE_FROM, FluentIcon.RIGHT_ARROW, FluentIcon.QUIET_HOURS, FluentIcon.FINGERPRINT, FluentIcon.APPLICATION, FluentIcon.CERTIFICATE, FluentIcon.TRANSPARENT, FluentIcon.IMAGE_EXPORT, FluentIcon.SPEED_MEDIUM, FluentIcon.LIBRARY_FILL, FluentIcon.MUSIC_FOLDER, FluentIcon.POWER_BUTTON, FluentIcon.SKIP_FORWARD, FluentIcon.CARE_UP_SOLID, FluentIcon.ACCEPT_MEDIUM, FluentIcon.CANCEL_MEDIUM, FluentIcon.CHEVRON_RIGHT, FluentIcon.CLIPPING_TOOL, FluentIcon.SEARCH_MIRROR, FluentIcon.SHOPPING_CART, FluentIcon.FONT_INCREASE, FluentIcon.BACK_TO_WINDOW, FluentIcon.COMMAND_PROMPT, FluentIcon.CLOUD_DOWNLOAD, FluentIcon.DICTIONARY_ADD, FluentIcon.CARE_DOWN_SOLID, FluentIcon.CARE_LEFT_SOLID, FluentIcon.CLEAR_SELECTION, FluentIcon.DEVELOPER_TOOLS, FluentIcon.BACKGROUND_FILL, FluentIcon.CARE_RIGHT_SOLID, FluentIcon.CHEVRON_DOWN_MED, FluentIcon.CHEVRON_RIGHT_MED, FluentIcon.EMOJI_TAB_SYMBOLS, FluentIcon.EXPRESSIVE_INPUT_ENTRY]

        self.slidingNavigationBar1 = SlidingNavigationBar(self) # scroll
        self.slidingNavigationBar2 = SlidingNavigationBar(self) # right

        self.slidingToolNavigationBar1 = SlidingToolNavigationBar(self) # scroll
        self.slidingToolNavigationBar2 = SlidingToolNavigationBar(self) # right

        self.settingPopDrawer = PopupDrawerWidget(self.parent(), position=PopupDrawerPosition.RIGHT)

        self.initNavigationBar()
        self.slidingNavigationBar2.addStretch(1)
        self.slidingNavigationBar2.addItem(
            "Item End",
            "Interface",
            alignment=Qt.AlignRight
        )
        self.initToolNavigationBar()
        self.slidingToolNavigationBar2.addStretch(1)
        self.slidingToolNavigationBar2.addItem(
            "Item End",
            FluentIcon.SETTING,
            alignment=Qt.AlignRight
        )

        self.button = PushButton("show setting docker", self)
        self.button.clicked.connect(lambda: self.settingPopDrawer.popDrawer(self.settingPopDrawer.isPopup))
        self.initPopDrawer()

        self.slidingNavigationBar1.setCurrentIndex(0)
        self.slidingNavigationBar2.setCurrentIndex(0)
        self.slidingToolNavigationBar1.setCurrentIndex(0)
        self.slidingToolNavigationBar2.setCurrentIndex(0)

        self.addWidget(self.slidingNavigationBar1)
        self.addWidget(self.slidingNavigationBar2)
        self.addWidget(self.slidingToolNavigationBar1)
        self.addWidget(self.slidingToolNavigationBar2)

        self.boxLayout.addStretch(1)
        self.addWidget(self.button, alignment=Qt.AlignBottom)

        self.boxLayout.setAlignment(Qt.AlignTop)

    def initPopDrawer(self):
        self.settingPopDrawer.setFixedWidth(350)
        self.settingPopDrawer.setClickParentHide(True)
        self.settingPopDrawer.addWidget(TitleLabel("设置Item颜色"), alignment=Qt.AlignHCenter)
        colorEdit = LineEdit()
        colorEdit.setClearButtonEnabled(True)
        colorEdit.textChanged.connect(self.updateItemColor)
        self.settingPopDrawer.addWidget(colorEdit)

        self.settingPopDrawer.addWidget(TitleLabel("设置Item悬停颜色"), alignment=Qt.AlignHCenter)
        hoverColorEdit = LineEdit()
        hoverColorEdit.setClearButtonEnabled(True)
        hoverColorEdit.textChanged.connect(self.updateHoverColor)
        self.settingPopDrawer.addWidget(hoverColorEdit)

        self.settingPopDrawer.addWidget(TitleLabel("设置Item选中颜色"), alignment=Qt.AlignHCenter)
        selectedColorEdit = LineEdit()
        selectedColorEdit.setClearButtonEnabled(True)
        selectedColorEdit.textChanged.connect(self.updateSelectedColor)
        self.settingPopDrawer.addWidget(selectedColorEdit)

        self.settingPopDrawer.addWidget(TitleLabel("设置Item宽"), alignment=Qt.AlignHCenter)
        selectedColorEdit = LineEdit()
        selectedColorEdit.setClearButtonEnabled(True)
        selectedColorEdit.textChanged.connect(self.updateSize)
        self.settingPopDrawer.addWidget(selectedColorEdit)

        self.settingPopDrawer.addWidget(TitleLabel("移动到指定Index"), alignment=Qt.AlignHCenter)
        comboBox = ComboBox(self)
        comboBox.setMaxVisibleItems(10)
        comboBox.addItems([str(index) for index in range(len(self.icons))])
        comboBox.currentIndexChanged.connect(self.updateIndex)
        self.settingPopDrawer.addWidget(comboBox)

        self.settingPopDrawer.addWidget(TitleLabel("删除指定控件"), alignment=Qt.AlignHCenter)
        comboBox = ComboBox(self)
        comboBox.setMaxVisibleItems(10)
        comboBox.addItems([str(index) for index in range(len(self.icons))])
        comboBox.currentIndexChanged.connect(lambda index: {
            self.slidingNavigationBar1.removeItem(self.slidingToolNavigationBar1.allItem()[index].property("routeKey")),
        })
        self.settingPopDrawer.addWidget(comboBox)

    def updateItemColor(self, color: str):
        self.slidingNavigationBar1.setItemColor(color),
        self.slidingNavigationBar2.setItemColor(color),
        self.slidingToolNavigationBar1.setItemColor(color),
        self.slidingToolNavigationBar2.setItemColor(color)

    def updateHoverColor(self, color: str):
        self.slidingNavigationBar1.setItemHoverColor(color),
        self.slidingNavigationBar2.setItemHoverColor(color),
        self.slidingToolNavigationBar1.setItemHoverColor(color),
        self.slidingToolNavigationBar2.setItemHoverColor(color)

    def updateSelectedColor(self, color: str):
        self.slidingNavigationBar1.setItemSelectedColor(color),
        self.slidingNavigationBar2.setItemSelectedColor(color),
        self.slidingToolNavigationBar1.setItemSelectedColor(color),
        self.slidingToolNavigationBar2.setItemSelectedColor(color)

    def updateSize(self, width, height=35):
        width = int(width)
        self.slidingNavigationBar1.setItemSize(width, height),
        self.slidingNavigationBar2.setItemSize(width, height),
        self.slidingToolNavigationBar1.setItemSize(width, height),
        self.slidingToolNavigationBar2.setItemSize(width, height)

    def updateIndex(self, index: int):
        self.slidingNavigationBar1.hScrollBar.scrollTo(self.slidingNavigationBar1.item(f"Item {index}").x())
        self.slidingNavigationBar1.setCurrentIndex(index)
        self.slidingToolNavigationBar1.hScrollBar.scrollTo(self.slidingToolNavigationBar1.item(f"Item {index}").x())
        self.slidingToolNavigationBar1.setCurrentIndex(index)

    def initNavigationBar(self):
        for icon in self.icons:
            index = self.icons.index(icon)
            self.slidingNavigationBar1.addItem(
                f"Item {index}",
                f"Interface {index}",
                icon,
                toolTip=f"Item {index}",
            )
            if index > 5:
                continue
            self.slidingNavigationBar2.addItem(
                f"Item {index}",
                f"Interface {index}",
                alignment=Qt.AlignLeft,
                toolTip=f"Item {index}",
            )

    def initToolNavigationBar(self):
        for icon in self.icons:
            index = self.icons.index(icon)
            self.slidingToolNavigationBar1.addItem(
                f"Item {index}",
                icon,
                toolTip=f"Item {index}",
            )
            if index > 5:
                continue
            self.slidingToolNavigationBar2.addItem(
                f"Item {index}",
                icon,
                alignment=Qt.AlignLeft,
                toolTip=f"Item {index}",
            )


class SlidingNavigationBarDemo(SplitWidget):
    def __init__(self):
        super().__init__()
        self.windowEffect.setMicaEffect(self.winId(), isAlt=True)

        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 35, 0, 0)
        self.widget = Widget(self)
        self.widget.enableTransparentBackground()
        self.box.addWidget(self.widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SlidingNavigationBarDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLayout

from FluentWidgets import SlidingWidget, SlidingNavigationBar, SlidingToolNavigationBar, VerticalScrollWidget, \
    FluentIcon


class SlidingNavigationBarDemo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.icons = [
            FluentIcon.UP,
            FluentIcon.ADD,
            FluentIcon.BUS,
            FluentIcon.CAR,
            FluentIcon.CUT,
            FluentIcon.IOT,
            FluentIcon.PIN,
            FluentIcon.TAG,
            FluentIcon.VPN,
            FluentIcon.CAFE,
            FluentIcon.CHAT,
            FluentIcon.COPY,
            FluentIcon.CODE,
            FluentIcon.DOWN,
            FluentIcon.EDIT,
            FluentIcon.FLAG,
            FluentIcon.FONT,
            FluentIcon.GAME,
            FluentIcon.HELP,
            FluentIcon.HIDE,
            FluentIcon.HOME,
            FluentIcon.INFO,
            FluentIcon.LEAF,
            FluentIcon.LINK,
            FluentIcon.MAIL,
            FluentIcon.MENU,
            FluentIcon.MUTE,
            FluentIcon.MORE,
            FluentIcon.MOVE,
            FluentIcon.PLAY,
            FluentIcon.SAVE,
            FluentIcon.SEND,
            FluentIcon.SYNC,
            FluentIcon.UNIT,
            FluentIcon.VIEW,
            FluentIcon.WIFI,
            FluentIcon.ZOOM,
            FluentIcon.ALBUM,
            FluentIcon.BRUSH,
            FluentIcon.BROOM,
            FluentIcon.CLOSE,
            FluentIcon.CLOUD,
            FluentIcon.EMBED,
            FluentIcon.GLOBE,
            FluentIcon.HEART,
            FluentIcon.LABEL,
            FluentIcon.MEDIA,
            FluentIcon.MOVIE,
            FluentIcon.MUSIC,
            FluentIcon.ROBOT,
            FluentIcon.PAUSE,
            FluentIcon.PASTE,
            FluentIcon.PHOTO,
            FluentIcon.PHONE,
            FluentIcon.PRINT,
            FluentIcon.SHARE,
            FluentIcon.TILES,
            FluentIcon.UNPIN,
            FluentIcon.VIDEO,
            FluentIcon.TRAIN,
            FluentIcon.ADD_TO,
            FluentIcon.ACCEPT,
            FluentIcon.CAMERA,
            FluentIcon.CANCEL,
            FluentIcon.DELETE,
            FluentIcon.FOLDER,
            FluentIcon.FILTER,
            FluentIcon.MARKET,
            FluentIcon.SCROLL,
            FluentIcon.LAYOUT,
            FluentIcon.GITHUB,
            FluentIcon.UPDATE,
            FluentIcon.REMOVE,
            FluentIcon.RETURN,
            FluentIcon.PEOPLE,
            FluentIcon.QRCODE,
            FluentIcon.RINGER,
            FluentIcon.ROTATE,
            FluentIcon.SEARCH,
            FluentIcon.VOLUME,
            FluentIcon.FRIGID,
            FluentIcon.SAVE_AS,
            FluentIcon.ZOOM_IN,
            FluentIcon.CONNECT,
            FluentIcon.HISTORY,
            FluentIcon.SETTING,
            FluentIcon.PALETTE,
            FluentIcon.MESSAGE,
            FluentIcon.FIT_PAGE,
            FluentIcon.ZOOM_OUT,
            FluentIcon.AIRPLANE,
            FluentIcon.ASTERISK,
            FluentIcon.CALORIES,
            FluentIcon.CALENDAR,
            FluentIcon.FEEDBACK,
            FluentIcon.LIBRARY,
            FluentIcon.MINIMIZE,
            FluentIcon.CHECKBOX,
            FluentIcon.DOCUMENT,
            FluentIcon.LANGUAGE,
            FluentIcon.DOWNLOAD,
            FluentIcon.QUESTION,
            FluentIcon.SPEAKERS,
            FluentIcon.DATE_TIME,
            FluentIcon.FONT_SIZE,
            FluentIcon.HOME_FILL,
            FluentIcon.PAGE_LEFT,
            FluentIcon.SAVE_COPY,
            FluentIcon.SEND_FILL,
            FluentIcon.SKIP_BACK,
            FluentIcon.SPEED_OFF,
            FluentIcon.ALIGNMENT,
            FluentIcon.BLUETOOTH,
            FluentIcon.COMPLETED,
            FluentIcon.CONSTRACT,
            FluentIcon.HEADPHONE,
            FluentIcon.MEGAPHONE,
            FluentIcon.PROJECTOR,
            FluentIcon.EDUCATION,
            FluentIcon.LEFT_ARROW,
            FluentIcon.ERASE_TOOL,
            FluentIcon.PAGE_RIGHT,
            FluentIcon.PLAY_SOLID,
            FluentIcon.HIGHTLIGHT,
            FluentIcon.FOLDER_ADD,
            FluentIcon.PAUSE_BOLD,
            FluentIcon.PENCIL_INK,
            FluentIcon.PIE_SINGLE,
            FluentIcon.QUICK_NOTE,
            FluentIcon.SPEED_HIGH,
            FluentIcon.STOP_WATCH,
            FluentIcon.ZIP_FOLDER,
            FluentIcon.BASKETBALL,
            FluentIcon.BRIGHTNESS,
            FluentIcon.DICTIONARY,
            FluentIcon.MICROPHONE,
            FluentIcon.ARROW_DOWN,
            FluentIcon.FULL_SCREEN,
            FluentIcon.MIX_VOLUMES,
            FluentIcon.REMOVE_FROM,
            FluentIcon.RIGHT_ARROW,
            FluentIcon.QUIET_HOURS,
            FluentIcon.FINGERPRINT,
            FluentIcon.APPLICATION,
            FluentIcon.CERTIFICATE,
            FluentIcon.TRANSPARENT,
            FluentIcon.IMAGE_EXPORT,
            FluentIcon.SPEED_MEDIUM,
            FluentIcon.LIBRARY_FILL,
            FluentIcon.MUSIC_FOLDER,
            FluentIcon.POWER_BUTTON,
            FluentIcon.SKIP_FORWARD,
            FluentIcon.CARE_UP_SOLID,
            FluentIcon.ACCEPT_MEDIUM,
            FluentIcon.CANCEL_MEDIUM,
            FluentIcon.CHEVRON_RIGHT,
            FluentIcon.CLIPPING_TOOL,
            FluentIcon.SEARCH_MIRROR,
            FluentIcon.SHOPPING_CART,
            FluentIcon.FONT_INCREASE,
            FluentIcon.BACK_TO_WINDOW,
            FluentIcon.COMMAND_PROMPT,
            FluentIcon.CLOUD_DOWNLOAD,
            FluentIcon.DICTIONARY_ADD,
            FluentIcon.CARE_DOWN_SOLID,
            FluentIcon.CARE_LEFT_SOLID,
            FluentIcon.CLEAR_SELECTION,
            FluentIcon.DEVELOPER_TOOLS,
            FluentIcon.BACKGROUND_FILL,
            FluentIcon.CARE_RIGHT_SOLID,
            FluentIcon.CHEVRON_DOWN_MED,
            FluentIcon.CHEVRON_RIGHT_MED,
            FluentIcon.EMOJI_TAB_SYMBOLS,
            FluentIcon.EXPRESSIVE_INPUT_ENTRY
        ]

        self.slidingNavigationBar = SlidingNavigationBar(self)
        self.slidingNavigationBar_I = SlidingNavigationBar(self)
        self.slidingToolNavigationBar = SlidingToolNavigationBar(self)

        self.initNavigationBar(100)
        self.slidingNavigationBar._widgetLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.slidingNavigationBar.addStretch(1)
        self.slidingNavigationBar.addItem(
            'test', 'test', alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
        )

        self.slidingToolNavigationBar.setItemSize(64, 35)

        self.slidingNavigationBar.setCurrentIndex(0)
        self.slidingToolNavigationBar.setCurrentIndex(0)

        self.slidingNavigationBar.setSlideLineColor('deeppink')
        self.slidingNavigationBar.setItemColor("orange")
        self.slidingNavigationBar.setItemHoverColor('deepskyblue')
        self.slidingNavigationBar.setItemSelectedColor('deeppink')

        self.addWidget(self.slidingNavigationBar, 1,  alignment=Qt.AlignTop)
        self.addWidget(self.slidingNavigationBar_I, 1,  alignment=Qt.AlignTop)
        self.addWidget(self.slidingToolNavigationBar, 1, alignment=Qt.AlignTop)

    def initNavigationBar(self, end=5):
        for _ in range(end):
            self.slidingNavigationBar.addItem(
                f"Item {_}",
                f"Interface {_}",
                alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter,
                toolTip=f"Interface {_}"
            )
            try:
                self.slidingNavigationBar_I.addItem(
                    f"Item {_}",
                    f"Interface {_}",
                    self.icons[_],
                )
                self.slidingToolNavigationBar.addItem(
                    f"Item {_}",
                    self.icons[_],
                    toolTip=str(self.icons[_])
                )
            except IndexError:
                self.slidingToolNavigationBar.addItem(
                    f"Item {_}",
                    self.icons[-1],
                    toolTip=str(self.icons[-1])
                )
            # self.slidingNavigationBar.addSeparator().setSeparatorColor("deeppink")
            # self.slidingToolNavigationBar.addSeparator().setSeparatorColor("deepskyblue")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SlidingNavigationBarDemo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
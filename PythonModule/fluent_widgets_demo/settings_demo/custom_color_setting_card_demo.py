import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QLocale

from FluentWidgets import CustomColorSettingCard, ConfigItem, ColorConfigItem, FluentIcon, FluentTranslator, \
    setThemeColor, themeColor, PrimaryPushButton, SlidingNavigationWidget, TitleLabel

app = QApplication(sys.argv)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.card = CustomColorSettingCard(
            ColorConfigItem('color', 'color', themeColor()),
            FluentIcon.BRUSH, "Title", "Content", self, True

        )
        self.card.colorChanged.connect(lambda color: {
            setThemeColor(color)
        })
        self.box.addWidget(self.card)

        self.box.addWidget(PrimaryPushButton("None"))
        self.nav = SlidingNavigationWidget(self)
        self.nav.addSubInterface('item1', 'None', TitleLabel("None"))
        self.nav.addSubInterface('item2', 'None', TitleLabel("None"))
        self.nav.addSubInterface('item3', 'None', TitleLabel("None"))
        self.nav.setCurrentWidget('item1')
        self.box.addWidget(self.nav)


if __name__ == '__main__':
    translator = FluentTranslator()
    app.installTranslator(translator)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

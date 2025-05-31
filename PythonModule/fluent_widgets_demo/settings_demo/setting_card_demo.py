# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from FluentWidgets import ExpandGroupSettingCard, SimpleExpandGroupSettingCard, ExpandSettingCard, FluentIcon, \
    TitleLabel, HeaderCardWidget, SettingCardGroup, SettingCard, PushSettingCard, CardWidget, SimpleCardWidget, \
    ElevatedCardWidget, VerticalScrollWidget


class Demo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.scg = SettingCardGroup("title", self)
        self.sc = SettingCard(FluentIcon.HOME, 'title', 'content', self)
        self.psc = PushSettingCard('text', FluentIcon.HOME, 'title', 'content', self)

        self.cw = CardWidget(self)
        self.cw.setFixedHeight(65)
        self.box = QVBoxLayout(self.cw)
        self.box.addWidget(TitleLabel('Hello World'), alignment=Qt.AlignHCenter)

        self.scw = SimpleCardWidget(self)
        self.scw.setFixedHeight(65)
        self.box = QVBoxLayout(self.scw)
        self.box.addWidget(TitleLabel('Hello World'), alignment=Qt.AlignHCenter)

        self.ecw = ElevatedCardWidget(self)
        self.ecw.setFixedHeight(65)
        self.box = QVBoxLayout(self.ecw)
        self.box.addWidget(TitleLabel('Hello World'), alignment=Qt.AlignHCenter)

        self.scg.addSettingCards([self.sc, self.psc])

        self.addWidget(self.scg)
        self.addWidget(self.cw)
        self.addWidget(self.scw)
        self.addWidget(self.ecw)

        self.cw = CardWidget(self)
        self.cw.setFixedHeight(65)
        self.box = QVBoxLayout(self.cw)
        self.box.addWidget(TitleLabel("G1"), alignment=Qt.AlignHCenter)

        self.scw = SimpleCardWidget(self)
        self.scw.setFixedHeight(65)
        self.box = QVBoxLayout(self.scw)
        self.box.addWidget(TitleLabel("G2"), alignment=Qt.AlignHCenter)

        self.ecw = ElevatedCardWidget(self)
        self.ecw.setFixedHeight(65)
        self.box = QVBoxLayout(self.ecw)
        self.box.addWidget(TitleLabel("G3"), alignment=Qt.AlignHCenter)

        self.scg.addSettingCards([self.cw, self.scw, self.ecw])

        # self.addWidget(self.sc)
        # self.addWidget(self.psc)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

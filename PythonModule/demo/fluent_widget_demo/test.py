import sys

from FluentWidgets import VerticalScrollWidget, FastCalendarPicker, DatePicker, \
    TimePicker, AMTimePicker, PickerPanel, PickerColumnFormatter, ZhDatePicker, \
    ColorPickerButton, ColorDialog, ColorSettingCard, FluentTranslator, Dialog, MessageBox, PushButton
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from PythonModule.FluentWidgetModule.FluentWidgets import UrlDialog, CustomDialog, TitleLabel, FlowLayout, \
    PrimaryPushButton, FlipViewWidget

from FluentWidgets import *


class Window(VerticalScrollWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addWidget(FastCalendarPicker(self))
        self.addWidget(DatePicker(self))
        self.addWidget(TimePicker(self))
        self.addWidget(AMTimePicker(self))
        self.cbn = PushButton('color dialog', self)
        self.cbn.clicked.connect(lambda: ColorDialog(QColor('red'), 'color dialog', self).show())
        self.addWidget(self.cbn)

        self.dbn = PushButton('dialog', self)
        self.dbn.clicked.connect(lambda: Dialog('title', 'content', self).show())
        self.addWidget(self.dbn)

        self.mbn = PushButton('message box', self)
        self.mbn.clicked.connect(lambda: MessageBox('title', 'content', self).show())
        self.addWidget(self.mbn)

        self.ubn = PushButton('url dialog', self)
        self.ubn.clicked.connect(lambda: UrlDialog(self).show())
        self.addWidget(self.ubn)

        self.cbn = PushButton('custom dialog', self)
        c = CustomDialog(self)
        self.cbn.clicked.connect(c.show)
        self.addWidget(self.cbn)

        self.fw = FlipViewWidget(self)
        self.addWidget(self.fw)
        self.fw.enableAutoPlay()
        self.fw.addImages([
            r"C:\Users\Administrator\OneDrive\Pictures\0.jpg",
            r"C:\Users\Administrator\OneDrive\Pictures\1.jpg",
            r"C:\Users\Administrator\OneDrive\Pictures\2.jpg",
            r"C:\Users\Administrator\OneDrive\Pictures\3.jpg",
            r"C:\Users\Administrator\OneDrive\Pictures\4.jpg"
        ])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    translator = FluentTranslator()
    app.installTranslator(translator)
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
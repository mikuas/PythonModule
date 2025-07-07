# coding:utf-8
import sys

import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QAbstractButton, QPushButton, QRadioButton
from PySide6.QtCore import Qt, QSize, QRectF, QRect
from PySide6.QtGui import QColor, QPainter, QFontMetrics

from FluentWidgets import RadioButton as RB, SubtitleRadioButton, RoundToolButton, setFont, PushButton
from FluentWidgets.components.widgets.button import FillPushButton
from FluentWidgets import *


class FilledPushButton(QPushButton):
    def __init__(self, text: str = None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.isHover = False
        self.isPress = False
        
    def enterEvent(self, event):
        self.isHover = True
        self.update()
        
    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        
    def mousePressEvent(self, e):
        self.isPress = True
        self.update()
    
    def mouseReleaseEvent(self, e):
        self.isPress = False
        self.update()
        
    def paintEvent(self, e):
        # return super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#787979"))
        
        if not self.isEnabled():
            painter.setOpacity(0.234)
        elif self.isPress:
            painter.setOpacity(0.567)
        elif self.isHover:
            painter.setOpacity(0.768)
        
        # draw background
        painter.drawRoundedRect(self.rect(), 8, 8)
        
        # draw text 
        painter.setPen("#ffffff")
        painter.drawText(self.rect().adjusted(10, 5, -10, -5), Qt.AlignmentFlag.AlignCenter, self.text())
        ...
    
    def sizeHint(self):
        size = QFontMetrics(self.font()).size(0, self.text())
        if size.height() < 35:
            size.setHeight(35)
        else:
            ...
            size.setHeight(size.height() + 10)
        size.setWidth(size.width() + 20)
        return size


class RadioButton(QRadioButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.isPress = False
        self.setStyleSheet(
            """
                QRadioButton {
                    background-color: transparent;
                    padding: 5px; /* 扩大可点击区域 */
                    border-radius: 4px;
                }
                QRadioButton:hover {
                    background-color: #E5E5E5;
                }
            """
        )
        print(self.styleSheet())
    
    def enterEvent(self, event):
        self.isHover = True
        self.update()
    
    def leaveEvent(self, event):
        self.isHover = False
        self.update()
    
    def mousePressEvent(self, e):
        self.isPress = True
        self.update()
    
    def mouseReleaseEvent(self, e):
        self.isPress = False
        self.setChecked(not self.isChecked())
        self.update()
    
    def sizeHint(self):
        return QSize(106, 32)
    
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        rect = QRect(5, 5, 24, 24)
        margin = 1
        if self.isHover:
            margin = 0
        if self.isPress:
            margin = 1
        else:
            margin = 0
        painter.drawText(self.rect(), Qt.AlignVCenter | Qt.AlignRight, "Hello World")
        
        if self.isChecked():
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("deeppink"))
        
            painter.drawRoundedRect(rect, 32, 32)
            
            painter.setBrush(QColor("#ffffff"))
            margin += 5
            painter.drawRoundedRect(rect.adjusted(margin, margin, -margin, -margin), 32, 32)
        else:
            painter.setPen("gray")
            painter.drawRoundedRect(rect, 32, 32)
        
        # painter.setBrush(Qt.NoBrush)
            
        # return super().paintEvent(e)


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 520)
        this = self
        self.box = QVBoxLayout(this)
        
        self.button = FilledPushButton("Infomation", this)
        # self.button.setEnabled(False)
        
        print(self.button.sizeHint())
        
        self.radioButton = RadioButton(this)
        
        self.fillButton = FillPushButton("Infomation", self)
        self.fillButton.setFillColor("#ec1aa3")
        
        self.pushButton = PushButton("Infomation", self)
        
        self.box.addWidget(this.button, 0, Qt.AlignHCenter)
        self.box.addWidget(this.fillButton, 0, Qt.AlignHCenter)
        self.box.addWidget(self.pushButton, 0, Qt.AlignHCenter)
        self.box.addWidget(self.radioButton, 0, Qt.AlignHCenter)
        # self.box.addWidget(RB("Hello World", self), 0, Qt.AlignHCenter)
        self.box.addWidget(SubtitleRadioButton("Hello World", "This is Sub Title", self), 0, Qt.AlignHCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
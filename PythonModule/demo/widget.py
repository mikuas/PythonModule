# coding:utf-8
import sys
from enum import Enum

from PySide6.QtGui import QColor, QPainter

from PySide6.QtWidgets import QFrame, QWidget, QApplication, QLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QSize, QEvent, QObject, QRect

from PythonModule.FluentWidgetModule.FluentWidgets import VBoxLayout, LineEdit, PushButton, TitleLabel
from PythonModule.FluentWidgetModule.build.lib.FluentWidgets.components.widgets.drawer_widget import PopDrawerWidget, \
    PopDrawerPosition


if __name__ == '__main__':
    class Demo(QWidget):
        def __init__(self, obj: PopDrawerWidget, title: str):
            super().__init__()

            layout = VBoxLayout(self)

            self.edit = LineEdit()
            self.edit.setPlaceholderText(title)

            self.button = PushButton("apply", self)
            self.button.clicked.connect(lambda: {
                obj.setFixedWidth(self.verify(self.edit.text())) if self.edit.placeholderText() == "宽度" else
                obj.setFixedHeight(self.verify(self.edit.text()))
            })

            layout.addWidgets([self.edit, self.button])

        def verify(self, text: str):
            try:
                return int(text)
            except ValueError:
                return 200

    app = QApplication(sys.argv)
    window = QWidget()
    box = VBoxLayout(window)
    topButton = PushButton("ShowTopDock", window)
    leftButton = PushButton("ShowLeftDock", window)
    bottomButton = PushButton("ShowBottomDock", window)
    rightButton = PushButton("ShowRightDock", window)
    
    at = QEasingCurve.Type.OutCubic

    topDocker = PopDrawerWidget(window, position=PopDrawerPosition.TOP)

    leftDocker = PopDrawerWidget(window, position=PopDrawerPosition.LEFT)

    bottomDocker = PopDrawerWidget(window, position=PopDrawerPosition.BOTTOM)

    rightDocker = PopDrawerWidget(window, position=PopDrawerPosition.RIGHT)
    topDocker.setBackgroundColor('skyblue', 'skyblue')

    dockers = [
        topDocker, leftDocker, bottomDocker, rightDocker
    ]
    titles = [
        "高度", "宽度", "高度", "宽度"
    ]

    for docker, title in zip(dockers, titles):
        docker.addWidget(Demo(docker, title))
        # docker.hideCloseButton(True)
        docker.setClickParentHide(True)

    topButton.clicked.connect(topDocker.popDrawer)
    leftButton.clicked.connect(leftDocker.popDrawer)
    bottomButton.clicked.connect(bottomDocker.popDrawer)
    rightButton.clicked.connect(rightDocker.popDrawer)

    box.addWidget(topButton)
    box.addWidget(leftButton)
    box.addWidget(bottomButton)
    box.addWidget(rightButton)

    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

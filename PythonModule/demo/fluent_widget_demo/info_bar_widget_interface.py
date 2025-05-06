# coding:utf-8
from PySide6.QtCore import Qt
from FluentWidgets import SmoothSwitchNavWidget, Widget, VBoxLayout, ToastInfoBar, ToastInfoBarPosition, VerticalScrollWidget
from qfluentwidgets import SwitchButton, PrimaryPushButton, TitleLabel, LineEdit, ComboBox, FluentIcon


class InfoBarWidgetInterface(SmoothSwitchNavWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.addSubInterface(
            "Success Info Bar",
            "Success Info Bar",
            Interface(self)
        )
        self.addSubInterface(
            "Error Info Bar",
            "Error Info Bar",
            Interface(self, 'error'),
        )
        self.addSubInterface(
            "Warning Info Bar",
            "Warning Info Bar",
            Interface(self, 'warning'),
        )
        self.addSubInterface(
            "Info Info Bar",
            "Info Info Bar",
            Interface(self, 'info'),
        )
        self.addSubInterface(
            "Custom Info Bar",
            "Custom Info Bar",
            Interface(self, 'custom'),
        )

        self.setCurrentWidget("Success Info Bar")


class Interface(VerticalScrollWidget):
    def __init__(self, parent=None, type_='success'):
        super().__init__(parent)

        self.title = TitleLabel("设置标题", self)
        self.titleEdit = LineEdit(self)
        self.titleEdit.setText("标题")

        self.content = TitleLabel("设置内容", self)
        self.contentEdit = LineEdit(self)
        self.contentEdit.setText("内容")

        self.duration = TitleLabel("设置时长", self)
        self.durationEdit = LineEdit(self)
        self.durationEdit.setText("2000")

        self.closeTitle = TitleLabel("是否可关闭", self)
        self.closeSwitch = SwitchButton(self)
        self.closeSwitch.setChecked(True)

        self.position = TitleLabel("设置位置", self)
        self.positionCombobox = ComboBox(self)
        self.positions = [
            ToastInfoBarPosition.TOP, ToastInfoBarPosition.TOP_RIGHT, ToastInfoBarPosition.TOP_LEFT,
            ToastInfoBarPosition.BOTTOM, ToastInfoBarPosition.BOTTOM_RIGHT, ToastInfoBarPosition.BOTTOM_LEFT
        ]
        self.positionCombobox.addItems([str(position)[21:] for position in self.positions])

        self.width_ = TitleLabel("设置宽度, 高度, 用 ',' 隔开", self)
        self.width_Edit = LineEdit(self)
        self.width_Edit.setText('200, 60')

        self.button = PrimaryPushButton(f"弹出{type_}信息栏", self)

        if type_ == 'success':
            self.button.clicked.connect(
                lambda: ToastInfoBar.success(
                    self, self.titleEdit.text(),
                    self.contentEdit.text(),
                    int(self.durationEdit.text()),
                    self.closeSwitch.isChecked(),
                    self.positions[self.positionCombobox.currentIndex()],
                    int(self.width_Edit.text().split(',')[0]),
                    int(self.width_Edit.text().split(',')[1])
                )
            )
        elif type_ == 'error':
            self.button.clicked.connect(
                lambda: ToastInfoBar.error(
                    self, self.titleEdit.text(),
                    self.contentEdit.text(),
                    int(self.durationEdit.text()),
                    self.closeSwitch.isChecked(),
                    self.positions[self.positionCombobox.currentIndex()],
                    int(self.width_Edit.text().split(',')[0]),
                    int(self.width_Edit.text().split(',')[1])
                )
            )
        elif type_ == 'warning':
            self.button.clicked.connect(
                lambda: ToastInfoBar.warning(
                    self, self.titleEdit.text(),
                    self.contentEdit.text(),
                    int(self.durationEdit.text()),
                    self.closeSwitch.isChecked(),
                    self.positions[self.positionCombobox.currentIndex()],
                    int(self.width_Edit.text().split(',')[0]),
                    int(self.width_Edit.text().split(',')[1])
                )
            )
        elif type_ == 'info':
            self.button.clicked.connect(
                lambda: ToastInfoBar.info(
                    self, self.titleEdit.text(),
                    self.contentEdit.text(),
                    int(self.durationEdit.text()),
                    self.closeSwitch.isChecked(),
                    self.positions[self.positionCombobox.currentIndex()],
                    int(self.width_Edit.text().split(',')[0]),
                    int(self.width_Edit.text().split(',')[1])
                )
            )
        elif type_ == 'custom':
            self.isCustom = TitleLabel("启用自定义背景色", self)
            self.bgcSwitch = SwitchButton(self)
            self.bgcTitle = TitleLabel("设置背景色", self)
            self.bgcEdit = LineEdit(self)
            self.toastTitle = TitleLabel("设置信息栏颜色", self)
            self.toastColor = LineEdit(self)
            self.toastColor.setText('skyblue')
            self.addWidget(self.isCustom, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.addWidget(self.bgcSwitch, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.addWidget(self.bgcTitle, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.addWidget(self.bgcEdit)
            self.addWidget(self.toastTitle, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.addWidget(self.toastColor)
            self.button.clicked.connect(
                lambda: ToastInfoBar.custom(
                    self, self.titleEdit.text(),
                    self.contentEdit.text(),
                    self.toastColor.text(),
                    int(self.durationEdit.text()),
                    self.closeSwitch.isChecked(),
                    self.positions[self.positionCombobox.currentIndex()],
                    self.bgcSwitch.isChecked(),
                    self.bgcEdit.text(),
                    int(self.width_Edit.text().split(',')[0]),
                    int(self.width_Edit.text().split(',')[1])
                )
            )

        self.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.titleEdit)
        self.addWidget(self.content, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.contentEdit)
        self.addWidget(self.duration, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.durationEdit)
        self.addWidget(self.position, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.positionCombobox)
        self.addWidget(self.closeTitle, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.closeSwitch, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.width_, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.addWidget(self.width_Edit)
        self.addWidget(self.button)

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.enableTransparentBackground()


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = InfoBarWidgetInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
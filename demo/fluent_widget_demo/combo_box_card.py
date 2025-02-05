from PySide6.QtWidgets import QWidget
from FluentWidgets import (
    PivotNav, VBoxLayout,
    ComboBoxCard, EditComboBoxCard, AcrylicComboBoxCard, AcrylicEditComboBoxCard
)
from qfluentwidgets import FluentIcon


class ComboBoxCardWidget(PivotNav):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(text)
        # 下拉框
        self.initComboBox()
        # 可编辑下拉框
        self.initEditComboBox()

        self.initNavigation()
        self.setCurrentItem('下拉框').enableTransparentBackground(True)

    def initComboBox(self):
        self.comboBoxWidget = SubWidget(self)
        comboBox = ComboBoxCard(
            FluentIcon.EDIT,
            "下拉框",
            "下拉框卡片",
            ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"],
            True,
            '请选择',
            self
        )

        acrylicComboBox = AcrylicComboBoxCard(
            FluentIcon.EDIT,
            "亚力克下拉框",
            "亚力克下拉框卡片",
            ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"],
            True,
            '请选择',
            self
        )

        self.comboBoxWidget.layout.addWidgets([comboBox, acrylicComboBox])

    def initEditComboBox(self):
        self.editComboBoxWidget = SubWidget(self)
        comboBox = EditComboBoxCard(
            FluentIcon.EDIT,
            "下拉框",
            "下拉框卡片",
            ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        )

        acrylicEditComboBox = AcrylicEditComboBoxCard(
            FluentIcon.EDIT,
            "亚力克可编辑下拉框",
            "亚力克可编辑下拉框卡片",
            ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        )

        self.editComboBoxWidget.layout.addWidgets([comboBox, acrylicEditComboBox])

    def initNavigation(self):
        self.addSubInterface(
            '下拉框',
            '下拉框',
            self.comboBoxWidget,
            FluentIcon.APPLICATION
        ).addSubInterface(
            '可编辑下拉框',
            '可编辑下拉框',
            self.editComboBoxWidget,
            FluentIcon.APPLICATION
        )


class SubWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = VBoxLayout(self)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ComboBoxCardWidget()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
from PySide6.QtWidgets import QWidget
from FluentWidgets import (
    SideNavigationWidget, Widget, VBoxLayout, WinFluentIcon,
    ButtonCard, PrimaryButtonCard, TransparentButtonCard,
    ToolButtonCard, PrimaryToolButtonCard, TransparentToolButtonCard,
    SwitchButtonCard, CheckBoxCard, HyperLinkCard,
    DropDownCard, PrimaryDropDownCard, TransparentDropDownCard,
    DropDownToolCard, PrimaryDropDownToolCard, TransparentDropDownToolCard,
    SplitCard, PrimarySplitCard, MoreButtonCard, MorePrimaryButtonCard, MoreTransparentButtonCard
)
from qfluentwidgets import FluentIcon


class ButtonCardWidget(SideNavigationWidget):
    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        self.setObjectName(text)
        # 标准按钮
        self.initPushButton()
        # 工具按钮
        self.initToolButton()
        # 开关 | 选择 | 超链接按钮
        self.initSwitchButton()
        # 下拉按钮
        self.initDropButton()
        # 下拉工具按钮
        self.initDropToolButton()
        # 分割按钮
        self.initSplitButton()

        #
        self.initTwoButton()

        self.initNavigation()
        self.setCurrentWidget('标准按钮').enableReturn(True).enableTransparentBackground(True)

    def initPushButton(self):
        self.pushBtnWidget = SubWidget(self)
        btn1 = ButtonCard(
            FluentIcon.ACCEPT,
            "标准按钮",
            "标准按钮卡片",
            "确定",
            FluentIcon.ACCEPT,
            self.pushBtnWidget
        )

        btn2 = PrimaryButtonCard(
            FluentIcon.ACCEPT,
            "主题色标准按钮",
            "主题色标准按钮卡片",
            "确定",
            FluentIcon.ACCEPT,
            self.pushBtnWidget
        )

        btn3 = TransparentButtonCard(
            FluentIcon.ACCEPT,
            "透明标准按钮",
            "透明标准按钮卡片",
            "确定",
            FluentIcon.ACCEPT,
            self.pushBtnWidget
        )

        self.pushBtnWidget.layout.addWidgets([btn1, btn2, btn3])

    def initToolButton(self):
        self.toolBtnWidget = SubWidget(self)
        btn1 = ToolButtonCard(
            FluentIcon.ACCEPT,
            "工具按钮",
            "工具按钮卡片",
            FluentIcon.ACCEPT,
            self.toolBtnWidget
        )

        btn2 = PrimaryToolButtonCard(
            FluentIcon.ACCEPT,
            "主题色工具按钮",
            "主题色工具按钮卡片",
            FluentIcon.ACCEPT,
            self.toolBtnWidget
        )

        btn3 = TransparentToolButtonCard(
            FluentIcon.ACCEPT,
            "透明工具按钮",
            "透明工具按钮卡片",
            FluentIcon.ACCEPT,
            self.toolBtnWidget
        )

        self.toolBtnWidget.layout.addWidgets([btn1, btn2, btn3])

    def initSwitchButton(self):
        self.switchBtnWidget = SubWidget(self)
        btn1 = SwitchButtonCard(
            FluentIcon.ACCEPT,
            "开关按钮",
            "开关按钮卡片",
            True,
            self.switchBtnWidget
        )

        btn2 = CheckBoxCard(
            FluentIcon.ACCEPT,
            "复选框",
            "复选框卡片",
            True,
            'test',
            self.switchBtnWidget
        )

        btn3 = HyperLinkCard(
            "https://www.bilibili.com",
            FluentIcon.ACCEPT,
            "超链接卡片",
            'test',
            "点击跳转到bili",
            FluentIcon.VIDEO,
            self.switchBtnWidget
        )

        self.switchBtnWidget.layout.addWidgets([btn1, btn2, btn3])

    def initDropButton(self):
        self.dropBtnWidget = SubWidget(self)
        btn1 = DropDownCard(
            FluentIcon.ACCEPT,
            "下拉按钮",
            "下拉按钮卡片",
            "下拉按钮",
            FluentIcon.CHEVRON_DOWN_MED,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        btn2 = PrimaryDropDownCard(
            FluentIcon.ACCEPT,
            "下拉按钮",
            "下拉按钮卡片",
            "下拉按钮",
            FluentIcon.CHEVRON_DOWN_MED,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        btn3 = TransparentDropDownCard(
            FluentIcon.ACCEPT,
            "下拉按钮",
            "下拉按钮卡片",
            "下拉按钮",
            FluentIcon.CHEVRON_DOWN_MED,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        self.dropBtnWidget.layout.addWidgets([btn1, btn2, btn3])

    def initDropToolButton(self):
        self.dropToolBtnWidget = SubWidget(self)
        btn1 = DropDownToolCard(
            FluentIcon.ACCEPT,
            "下拉工具按钮",
            "下拉工具按钮卡片",
            FluentIcon.SEND,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        btn2 = PrimaryDropDownToolCard(
            FluentIcon.ACCEPT,
            "下拉工具按钮",
            "下拉工具按钮卡片",
            FluentIcon.SEND,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        btn3 = TransparentDropDownToolCard(
            FluentIcon.ACCEPT,
            "下拉工具按钮",
            "下拉工具按钮卡片",
            FluentIcon.SEND,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        self.dropToolBtnWidget.layout.addWidgets([btn1, btn2, btn3])

    def initSplitButton(self):
        self.splitBtnWidget = SubWidget(self)

        btn1 = SplitCard(
            FluentIcon.ACCEPT,
            "拆分按钮",
            "拆分按钮卡片",
            "确定",
            FluentIcon.ACCEPT,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        btn2 = PrimarySplitCard(
            FluentIcon.ACCEPT,
            "拆分按钮",
            "拆分按钮卡片",
            "确定",
            FluentIcon.ACCEPT,
            ['item1', 'item2', 'item3'],
            [FluentIcon.SAVE, FluentIcon.REMOVE, FluentIcon.RETURN],
            [
                lambda: print('item1'),
                lambda: print('item2'),
                lambda: print('item3')
            ],
            self
        )

        self.splitBtnWidget.layout.addWidgets([btn1, btn2])

    def initTwoButton(self):
        self.moreButtonWidget = SubWidget(self)
        btn1 = MoreButtonCard(
            FluentIcon.RETURN,
            'More Button',
            'More Button',
            '确定',
            FluentIcon.APPLICATION,
            self
        )

        btn2 = MorePrimaryButtonCard(
            FluentIcon.RETURN,
            'More Button',
            'More Button',
            '确定',
            FluentIcon.APPLICATION,
            self
        )

        btn3 = MoreTransparentButtonCard(
            FluentIcon.RETURN,
            'More Button',
            'More Button',
            '确定',
            FluentIcon.APPLICATION,
            self
        )

        self.moreButtonWidget.layout.addWidgets([btn1, btn2, btn3])

    def initNavigation(self):
        self.addSubInterface(
            '标准按钮',
            '标准按钮',
            WinFluentIcon.HOME,
            self.pushBtnWidget
        ).addSubInterface(
            '工具按钮',
            '工具按钮',
            WinFluentIcon.WIN_11_LOG,
            self.toolBtnWidget
        ).addSubInterface(
            '开关按钮',
            '开关按钮',
            WinFluentIcon.WIFI,
            self.switchBtnWidget
        ).addSubInterface(
            '下拉按钮',
            '下拉按钮',
            WinFluentIcon.DOWN,
            self.dropBtnWidget
        ).addSubInterface(
            '下拉工具按钮',
            '下拉工具按钮',
            WinFluentIcon.DROP_UP,
            self.dropToolBtnWidget
        ).addSubInterface(
            '拆分按钮',
            '拆分按钮',
            WinFluentIcon.XIN_HAO,
            self.splitBtnWidget
        ).addSubInterface(
            'More Button',
            'More Button',
            WinFluentIcon.SEARCH_MORE,
            self.moreButtonWidget
        )


class SubWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = VBoxLayout(self)
    

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ButtonCardWidget()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

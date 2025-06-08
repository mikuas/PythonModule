from PySide6.QtWidgets import (
    QApplication, QMenu, QPushButton, QWidget,
    QLineEdit, QWidgetAction
)

app = QApplication([])

main = QWidget()
main.resize(300, 200)

btn = QPushButton("弹出菜单", main)
btn.move(100, 80)

def show_menu():
    menu = QMenu()

    # 普通菜单项
    menu.addAction("选项 A")

    # 自定义 QWidget（如 QLineEdit）
    line_edit = QLineEdit()
    line_edit.setPlaceholderText("请输入内容...")

    # 包装成 QWidgetAction
    widget_action = QWidgetAction(menu)
    widget_action.setDefaultWidget(line_edit)
    menu.addAction(widget_action)

    # 更多菜单项
    menu.addAction("选项 B")

    # 弹出
    menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

btn.clicked.connect(show_menu)

main.show()
app.exec()

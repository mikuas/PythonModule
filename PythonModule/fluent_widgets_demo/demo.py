from PySide6.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
import sys

class CssShadowExample(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # 创建QFrame并应用CSS阴影
        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setMinimumSize(200, 100)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
            }
        """)

        layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setWindowTitle("CSS阴影示例")
        self.resize(300, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CssShadowExample()
    window.show()
    sys.exit(app.exec())
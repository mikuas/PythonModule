from PySide6.QtWidgets import (
    QWidget, QPlainTextEdit, QVBoxLayout, QMainWindow, QApplication, QFrame, QTextEdit
)
from PySide6.QtGui import QColor, QPainter, QTextFormat, QTextCharFormat, QSyntaxHighlighter, QFont
from PySide6.QtCore import QRect, Qt, QSize, QRegularExpression
import sys


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#C679DD"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            'def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif',
            'while', 'for', 'try', 'except', 'with', 'as', 'assert', 'yield',
            'None', 'True', 'False', 'pass', 'break', 'continue', 'in', 'is', 'not', 'and', 'or'
        ]

        self.highlighting_rules = [
            (QRegularExpression(r'\b' + kw + r'\b'), keyword_format) for kw in keywords
        ]

        nz_keywords = [
            'print', 'len', 'int', 'float', 'bool', 'str', 'dict', 'set', 'list', 'tuple'
        ]

        nz_keyword = QTextCharFormat()
        nz_keyword.setForeground(QColor("#56B6C2"))
        nz_keyword.setFontWeight(QFont.Weight.Bold)

        [self.highlighting_rules.append((QRegularExpression(r'\b' + kw + r'\b'), nz_keyword)) for kw in nz_keywords]

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), comment_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#13b26a"))
        self.highlighting_rules.append((QRegularExpression("\".*\""), string_format))
        self.highlighting_rules.append((QRegularExpression("\'.*\'"), string_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match_iter = pattern.globalMatch(text)
            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)



class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)

        font = QFont("Consolas")
        font.setPointSize(16)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        self.setFrameStyle(QFrame.NoFrame)
        self.highlight_current_line()
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)
        PythonHighlighter(self.document())

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#f0f0f0"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.darkGray)
                painter.drawText(0, top, self.line_number_area.width() - 4, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#e6f7ff"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


# 测试窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Editor with Line Numbers")
        editor = CodeEditor()
        editor.setPlainText("def hello():\n    print('Hello, world!')")

        layout = QVBoxLayout()
        layout.addWidget(editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

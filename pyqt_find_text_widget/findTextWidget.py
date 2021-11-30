import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextDocument, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QTextBrowser, QLabel, \
    QHBoxLayout, QGridLayout, QLineEdit, QMessageBox


class FindTextWidget(QWidget):

    prevClicked = pyqtSignal(str)
    nextClicked = pyqtSignal(str)
    closeSignal = pyqtSignal()

    def __init__(self, widget: QWidget):
        super().__init__()
        self.__widgetToFind = widget

        self.__widgetToFind.setStyleSheet('QTextEdit { selection-background-color: lightblue; selection-color: red; }')

        self.__selections_init()
        self.__initUi()

    def __initUi(self):
        self.__lineEdit = QLineEdit()
        self.__lineEdit.setStyleSheet('QLineEdit { border: none; }')
        self.__lineEdit.textChanged.connect(self.__textChanged)
        self.__lineEdit.returnPressed.connect(self.next)

        self.__cnt_text = '{0} results'
        self.__cnt_lbl = QLabel(self.__cnt_text.format(0))

        self.__prevBtn = QPushButton()
        self.__nextBtn = QPushButton()
        self.__nextBtn.setShortcut('Enter')

        self.__prevBtn.clicked.connect(self.prev)
        self.__nextBtn.clicked.connect(self.next)

        self.btn_toggled(False)

        self.__caseBtn = QPushButton()
        self.__caseBtn.setCheckable(True)
        self.__caseBtn.toggled.connect(self.__caseToggled)

        self.__regexBtn = QPushButton()
        self.__regexBtn.setCheckable(True)

        closeBtn = QPushButton()
        closeBtn.setShortcut('Escape')
        closeBtn.clicked.connect(self.__close)

        rel_dirname = os.path.dirname(os.path.relpath(__file__, os.getcwd()))

        css_file_path = os.path.join(rel_dirname, r'style/button.css')
        css_file = open(css_file_path)
        btn_css_code = css_file.read()
        css_file.close()

        btns = [self.__prevBtn, self.__nextBtn, self.__caseBtn, self.__regexBtn, closeBtn]

        for btn in btns:
            btn.setStyleSheet(btn_css_code)

        self.__prevBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/prev.png')))
        self.__nextBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/next.png')))
        self.__caseBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/case.png')))
        self.__regexBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/regex.png')))
        closeBtn.setIcon(QIcon(os.path.join(rel_dirname, r'ico/close.png')))

        self.__prevBtn.setToolTip('Previous Occurrence')
        self.__nextBtn.setToolTip('Next Occurrence')
        self.__caseBtn.setToolTip('Match Case')
        self.__regexBtn.setToolTip('Regex')
        closeBtn.setToolTip('Close')

        lay = QHBoxLayout()
        lay.addWidget(self.__lineEdit)
        lay.addWidget(self.__cnt_lbl)
        lay.addWidget(self.__prevBtn)
        lay.addWidget(self.__nextBtn)
        lay.addWidget(self.__caseBtn)
        lay.addWidget(self.__regexBtn)
        lay.addWidget(closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        mainWidget = QWidget()
        mainWidget.setObjectName('mainWidget')
        mainWidget.setLayout(lay)

        lay = QGridLayout()
        lay.addWidget(mainWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __textChanged(self, text, flags=None):
        f1 = text.strip() != ''
        if f1:
            if self.__caseBtn.isChecked():
                flags = QTextDocument.FindCaseSensitively
            self.__findInit(text, flags)
            f2 = len(self.__selections) > 0
            self.btn_toggled(f1 and f2)
        else:
            self.__cnt_lbl.setText(self.__cnt_text.format(0))

    def __setCount(self):
        word_cnt = len(self.__selections)
        self.__cnt_lbl.setText(self.__cnt_text.format(word_cnt))

    def btn_toggled(self, f):
        self.__prevBtn.setEnabled(f)
        self.__nextBtn.setEnabled(f)

    def __selections_init(self):
        self.__selections = []
        self.__selections_idx = -1

    def __findInit(self, text, flags=None):
        self.__selections_init()
        doc = self.__widgetToFind.document()
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.darkGreen)
        cur = QTextCursor()
        while True:
            if flags:
                cur = doc.find(text, cur, flags)
            else:
                cur = doc.find(text, cur)
            if cur.isNull() or cur.atEnd():
                break
            sel = QTextBrowser.ExtraSelection()
            sel.cursor = cur
            sel.format = fmt
            self.__selections.append(sel)
        self.__widgetToFind.setExtraSelections(self.__selections)
        self.__setCount()
        self.next()

    def prev(self):
        if self.__selections_idx-1 < 0:
            QMessageBox.information(self, 'Notice', 'Start of file.')
        else:
            self.__selections_idx -= 1

            text = self.__lineEdit.text()
            cur = self.__selections[self.__selections_idx].cursor
            start = cur.selectionStart()
            end = cur.selectionEnd()
            cur.setPosition(start, QTextCursor.MoveAnchor)
            cur.setPosition(end, QTextCursor.KeepAnchor)

            self.__widgetToFind.setTextCursor(cur)
            self.__widgetToFind.ensureCursorVisible()

            self.prevClicked.emit(text)

    def next(self):
        if len(self.__selections) > 0:
            if self.__selections_idx+1 >= len(self.__selections):
                QMessageBox.information(self, 'Notice', 'End of file.')
            else:
                self.__selections_idx += 1
                text = self.__lineEdit.text()
                cur = self.__selections[self.__selections_idx].cursor
                start = cur.selectionStart()
                end = cur.selectionEnd()
                cur.setPosition(start, QTextCursor.MoveAnchor)
                cur.setPosition(end, QTextCursor.KeepAnchor)

                self.__widgetToFind.setTextCursor(cur)
                self.__widgetToFind.ensureCursorVisible()

                self.nextClicked.emit(text)

    def __caseToggled(self, f):
        text = self.__lineEdit.text()
        if f:
            flags = QTextDocument.FindCaseSensitively
            self.__textChanged(text, flags)
        else:
            self.__textChanged(text)

    def showEvent(self, e):
        cur = self.__widgetToFind.textCursor()
        text = cur.selectedText()
        prev_text = self.__lineEdit.text()
        if prev_text == text:
            self.__textChanged(text)
        else:
            self.__lineEdit.setText(text)

        return super().showEvent(e)

    def __close(self):
        not_selections = []
        fmt = QTextCharFormat()
        fmt.setForeground(self.__widgetToFind.textColor())
        for selection in self.__selections:
            cur = selection.cursor
            sel = QTextBrowser.ExtraSelection()
            sel.cursor = cur
            sel.format = fmt
            not_selections.append(sel)
        self.__widgetToFind.setExtraSelections(not_selections)

        self.closeSignal.emit()

    def get_line_edit(self):
        return self.__lineEdit
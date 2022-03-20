from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import QWidget, QPushButton, QTextBrowser, QLabel, \
    QHBoxLayout, QGridLayout, QLineEdit, QMessageBox

from pyqt_svg_icon_pushbutton.svgIconPushButton import SvgIconPushButton


class FindTextWidget(QWidget):

    prevClicked = pyqtSignal(str)
    nextClicked = pyqtSignal(str)
    closeSignal = pyqtSignal()

    def __init__(self, widget: QWidget):
        super().__init__()
        self.__widgetToFind = widget

        self.__selectionsInit()
        self.__initUi()

    def __initUi(self):
        self.__findTextLineEdit = QLineEdit()
        self.__findTextLineEdit.setStyleSheet('QLineEdit { border: none; }')
        self.__findTextLineEdit.textChanged.connect(self.__textChanged)
        self.__findTextLineEdit.returnPressed.connect(self.next)
        self.setFocusProxy(self.__findTextLineEdit)

        self.__cnt_init_text = '{0} results'
        self.__cnt_cur_idx_text = '{0}/{1}'
        self.__cnt_lbl = QLabel(self.__cnt_init_text.format(0))

        self.__prevBtn = QPushButton()

        self.__nextBtn = QPushButton()
        self.__nextBtn.setShortcut('Enter')

        self.__prevBtn.clicked.connect(self.prev)
        self.__nextBtn.clicked.connect(self.next)

        self.__btnToggled(False)

        self.__caseBtn = QPushButton()
        self.__caseBtn.setCheckable(True)
        self.__caseBtn.toggled.connect(self.__caseToggled)

        self.__wordBtn = QPushButton()
        self.__wordBtn.setCheckable(True)
        self.__wordBtn.toggled.connect(self.__wordToggled)

        self.__regexBtn = QPushButton()
        self.__regexBtn.setCheckable(True)

        self.__closeBtn = QPushButton()
        self.__closeBtn.setVisible(False)
        self.__closeBtn.clicked.connect(self.close)
        self.__closeBtn.setShortcut('Escape')

        btns = [self.__prevBtn, self.__nextBtn, self.__caseBtn, self.__wordBtn, self.__regexBtn, self.__closeBtn]

        self.__prevBtn.setToolTip('Previous Occurrence')
        self.__nextBtn.setToolTip('Next Occurrence')
        self.__caseBtn.setToolTip('Match Case')
        self.__wordBtn.setToolTip('Match Word')
        self.__regexBtn.setToolTip('Regex')
        self.__closeBtn.setToolTip('Close')

        lay = QHBoxLayout()
        lay.addWidget(self.__findTextLineEdit)
        lay.addWidget(self.__cnt_lbl)
        lay.addWidget(self.__prevBtn)
        lay.addWidget(self.__nextBtn)
        lay.addWidget(self.__caseBtn)
        lay.addWidget(self.__wordBtn)
        lay.addWidget(self.__regexBtn)
        lay.addWidget(self.__closeBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        mainWidget = QWidget()
        mainWidget.setObjectName('mainWidget')
        mainWidget.setLayout(lay)

        lay = QGridLayout()
        lay.addWidget(mainWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def widgetTextChanged(self):
        self.__textChanged(self.__findTextLineEdit.text(), widgetTextChanged=True)

    def __textChanged(self, text, widgetTextChanged=False):
        f1 = text.strip() != ''
        flags = 0
        if self.__caseBtn.isChecked():
            flags = flags | QTextDocument.FindCaseSensitively
        else:
            flags = flags & ~QTextDocument.FindCaseSensitively
        if self.__wordBtn.isChecked():
            flags = flags | QTextDocument.FindWholeWords
        else:
            flags = flags & ~QTextDocument.FindWholeWords
        self.__findInit(text, flags=flags, widgetTextChanged=widgetTextChanged)
        f2 = len(self.__selections) > 0
        self.__btnToggled(f1 and f2)

    def __setCount(self):
        word_cnt = len(self.__selections)
        self.__cnt_lbl.setText(self.__cnt_init_text.format(word_cnt))

    def __btnToggled(self, f):
        self.__prevBtn.setEnabled(f)
        self.__nextBtn.setEnabled(f)

    def __selectionsInit(self):
        self.__selections = []
        self.__selections_idx = -1

    def __findInit(self, text, flags=0, widgetTextChanged=False):
        def addSelection():
            sel = QTextBrowser.ExtraSelection()
            sel.cursor = cur
            sel.format = fmt
            self.__selections.append(sel)

        self.__selectionsInit()
        doc = self.__widgetToFind.document()
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.green)
        fmt.setBackground(Qt.darkYellow)
        cur = QTextCursor()
        while True:
            if flags:
                cur = doc.find(text, cur, flags)
            else:
                cur = doc.find(text, cur)
            if cur.isNull() or cur.atEnd():
                if cur.atEnd():
                    if cur.selectedText() == text:
                        addSelection()
                break
            addSelection()
        self.__widgetToFind.setExtraSelections(self.__selections)
        self.__setCount()
        if widgetTextChanged:
            pass
        else:
            self.next()

    def prev(self):
        cur_pos = self.__widgetToFind.textCursor().position()
        text = self.__findTextLineEdit.text()

        def getPosList():
            pos_lst = [selection.cursor.position() for selection in self.__selections]
            pos_lst = [c for c in pos_lst if c < cur_pos]
            return pos_lst

        if self.__selections_idx-1 < 0:
            if cur_pos > self.__selections[0].cursor.position():
                pos_lst = getPosList()
                if len(pos_lst) > 0:
                    closest_value = max(pos_lst)
                    self.__selections_idx = pos_lst.index(closest_value)
                    self.__setCursor()
                    self.__cnt_lbl.setText(self.__cnt_cur_idx_text.format(self.__selections_idx+1, len(self.__selections)))
                    self.prevClicked.emit(text)
                else:
                    pass
            else:
                QMessageBox.information(self, 'Notice', 'Start of file.')
        else:
            pos_lst = getPosList()
            if len(pos_lst) > 0:
                closest_value = max(pos_lst)
                if cur_pos in pos_lst:
                    self.__selections_idx -= 1
                else:
                    self.__selections_idx = pos_lst.index(closest_value)
                self.__setCursor()
                self.__cnt_lbl.setText(self.__cnt_cur_idx_text.format(self.__selections_idx+1, len(self.__selections)))
                self.prevClicked.emit(text)
            else:
                pass

    def next(self):
        cur_pos = self.__widgetToFind.textCursor().position()
        text = self.__findTextLineEdit.text()

        def getPosList():
            pos_lst = [selection.cursor.position() for selection in self.__selections]
            pos_lst = [c for c in pos_lst if c > cur_pos]
            return pos_lst

        if len(self.__selections) > 0:
            if self.__selections_idx+1 >= len(self.__selections):
                if cur_pos < self.__selections[-1].cursor.position():
                    pos_lst = getPosList()
                    if len(pos_lst) > 0:
                        closest_value = min(pos_lst)
                        self.__selections_idx = len(self.__selections)-len(pos_lst) + pos_lst.index(closest_value)

                        self.__setCursor()
                        self.__cnt_lbl.setText(
                            self.__cnt_cur_idx_text.format(self.__selections_idx + 1, len(self.__selections)))
                        self.nextClicked.emit(text)
                    else:
                        pass
                else:
                    QMessageBox.information(self, 'Notice', 'End of file.')
            else:
                pos_lst = getPosList()
                if len(pos_lst) > 0:
                    closest_value = min(pos_lst)
                    if cur_pos in pos_lst:
                        self.__selections_idx += 1
                    else:
                        self.__selections_idx = len(self.__selections)-len(pos_lst) + pos_lst.index(closest_value)
                    self.__setCursor()
                    self.__cnt_lbl.setText(self.__cnt_cur_idx_text.format(self.__selections_idx+1, len(self.__selections)))
                    self.nextClicked.emit(text)
                else:
                    self.__selections_idx += 1
                    self.__setCursor()
                    self.nextClicked.emit(text)

    def __setCursor(self):
        cur = self.__selections[self.__selections_idx].cursor
        start = cur.selectionStart()
        end = cur.selectionEnd()
        cur.setPosition(start, QTextCursor.MoveAnchor)
        cur.setPosition(end, QTextCursor.KeepAnchor)

        self.__widgetToFind.setTextCursor(cur)
        self.__widgetToFind.ensureCursorVisible()

    def __caseToggled(self, f):
        text = self.__findTextLineEdit.text()
        self.__textChanged(text)

    def __wordToggled(self, f):
        text = self.__findTextLineEdit.text()
        self.__textChanged(text)

    def showEvent(self, e):
        cur = self.__widgetToFind.textCursor()
        text = cur.selectedText()
        prev_text = self.__findTextLineEdit.text()
        if prev_text == text:
            self.__textChanged(text)
        else:
            self.__findTextLineEdit.setText(text)

        return super().showEvent(e)

    def setCloseBtn(self, f: bool):
        self.__closeBtn.setVisible(f)

    def close(self):
        super().close()
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

    def getLineEdit(self):
        return self.__findTextLineEdit

    def setLineEdit(self, text: str):
        self.__findTextLineEdit.setText(text)


# pyqt-find-text-widget
PyQt5 find text widget

## Requirements
PyQt5 >= 5.8

## Setup
```
pip install git+https://github.com/yjg30737/pyqt-find-text-widget.git --upgrade
```

## Feature
* Previous, Next occurence
* Match case
* Makes find match only complete words
* Providing prev, next, close signals
* Enable to set close button with ```setCloseBtn(f: bool)```

I'm still working with regex feature.

## Signal
* prevClicked
* nextClicked
* closeSignal

## Usage
I just give you one sweet code example
```python
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QTextEdit
from pyqt_find_text_widget.findTextWidget import FindTextWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__te = QTextEdit()
        self.__te.setStyleSheet('QTextEdit { selection-background-color: lightblue; }') # I wrote this code because color of default selection doesn't stand out in the white textedit screen.

        self.__w = FindTextWidget(self.__te)

        lay = QGridLayout()
        lay.addWidget(self.__w)
        lay.addWidget(self.__te)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
```
And i give you sweet result video.


https://user-images.githubusercontent.com/55078043/146631688-329eade1-ba51-4e25-a6cd-8cfe8efe2eda.mp4




# pyqt-find-text-widget
PyQt widget which can be used to find text in QTextEdit/QTextBrowser

## Requirements
PyQt5 >= 5.8

## Setup
`python -m pip install pyqt-find-text-widget`

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-svg-icon-pushbutton.git">pyqt-svg-icon-pushbutton</a>

## Feature
* Find previous, next occurence based on text cursor's position
* Match case
* Makes find match only complete words
* Providing prev, next, close signals
* Enable to set close button with `setCloseBtn(f: bool)`

I'm still working with regex feature.

## Signal
* prevClicked
* nextClicked
* closeSignal

## Usage
Code Sample
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

Result

Note: Button icons in preview are obsolete. Back then these icons were PNG, now these are SVG! So don't worry about the difference.

https://user-images.githubusercontent.com/55078043/147844492-53b355ff-801a-4fca-bbef-c37fb55d1418.mp4

Match case & complete word only example

https://user-images.githubusercontent.com/55078043/147844473-76474b51-2b2d-4680-82e4-8a67ab263db3.mp4




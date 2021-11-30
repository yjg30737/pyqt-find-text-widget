# pyqt-find-text-widget
PyQt5 find text widget

## Requirements
PyQt5 >= 5.8

## Setup
```
pip install git+https://github.com/yjg30737/pyqt-find-text-widget.git --upgrade
```

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
And i give you sweet result gif

![example](example/example.gif)

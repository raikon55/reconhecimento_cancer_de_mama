# -*- coding: utf-8 -*-

import sys
from PySide6 import QtWidgets
from src.view.ImageInterface import ImageInterface

if __name__ == "__main__":

    view = QtWidgets.QApplication([])

    widget = ImageInterface('image/test.jpg')
    widget.resize(1280, 720)
    widget.show()

    sys.exit(view.exec_())
    del widget

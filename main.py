# -*- coding: utf-8 -*-

import sys
from PySide6 import QtWidgets
from src.view.ImageInterface import ImageInterface

if __name__ == "__main__":
    view = QtWidgets.QApplication([])

    widget = ImageInterface()
    widget.create_interface()

    sys.exit(view.exec_())

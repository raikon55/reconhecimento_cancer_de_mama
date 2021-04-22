# -*- coding: utf-8 -*-
from PIL.ImageQt import ImageQt
from PySide6 import QtCore
from PySide6.QtCore import QRect, QMetaObject, QCoreApplication
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QMenuBar, QButtonGroup, QFrame, QMenu, QStatusBar, \
    QMainWindow, QMdiArea, QLineEdit, QInputDialog

from ..handler.ImageHandler import ImageHandler


class ImageInterface(QMainWindow):
    # Cache
    __filename: str = None

    # Interface
    # Buttons
    __imageManipulationGroup: QButtonGroup
    __originalImageButton: QPushButton
    __resize32x32Button: QPushButton
    __resize64x64Button: QPushButton
    __equalizeButton: QPushButton

    # Actions
    __actionOpenImage: QAction
    __actionCloseImage: QAction
    __actionQuit: QAction

    # Menu
    __menuBar: QMenuBar
    __menuFile: QMenu

    # Wrapper to image handler
    __imageHandler: ImageHandler = None
    __imageContainer: ImageQt = None
    __imageModified: ImageQt = None

    __containerImagePixmap: QPixmap = None
    __imageWidget: QWidget = None
    __imageLabel: QLabel

    def __init__(self):
        # Configure interface
        super().__init__()
        self.setObjectName(u'ImagePy')
        self.resize(1280, 720)

        self.__imageWidget = QWidget(self)

        self.__imageManipulationGroup = QButtonGroup(self)
        self.__originalImageButton = QPushButton(self.__imageWidget)
        self.__resize32x32Button = QPushButton(self.__imageWidget)
        self.__resize64x64Button = QPushButton(self.__imageWidget)
        self.__equalizeButton = QPushButton(self.__imageWidget)

        self.__actionOpenImage = QAction(self)
        self.__actionCloseImage = QAction(self)
        self.__actionQuit = QAction(self)

        self.__menuBar = QMenuBar(self)
        self.__menuFile = QMenu(self.__menuBar)

        self.__statusBar = QStatusBar(self)

        self.__imageLabel = QLabel(self.__imageWidget, alignment=QtCore.Qt.AlignCenter)

        # Init interface
        self.setup_ui()

    def open_image(self) -> None:
        file_path, ok = QInputDialog.getText(self, u'text', u'Enter image path')

        self.__filename = file_path if ok else None
        self.__imageHandler = ImageHandler(self.__filename)
        self.load_image(can_update=True)

    @QtCore.Slot()
    def load_image(self, can_update: bool = False) -> None:
        if self.__imageHandler is None:
            return

        elif self.__containerImagePixmap is None or can_update:
            self.__containerImagePixmap = QPixmap(self.__imageHandler.get_file_path())
            self.__imageLabel.setPixmap(self.__containerImagePixmap)

        elif self.__containerImagePixmap is not None \
                and self.__imageModified is not None \
                and self.__imageModified != self.__imageHandler.get_image():
            self.__containerImagePixmap = QPixmap(self.__imageModified)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def recover_original_image(self) -> None:
        self.__containerImagePixmap = QPixmap(self.__imageHandler.get_file_path())
        self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def close_image(self) -> None:
        self.__imageHandler = None
        self.__containerImagePixmap = None
        self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def create_interface(self) -> None:
        super().show()

    # def zoom_out(self) -> None:
    #     print('Zoom out')

    # def zoom_in(self) -> None:
    #     print('Zoom in')

    def decrease_to_64(self) -> None:
        self.__imageModified = ImageQt(self.__imageHandler.new_resolution(64))
        self.load_image()

    def decrease_to_32(self) -> None:
        self.__imageModified = ImageQt(self.__imageHandler.new_resolution(32))
        self.load_image()

    def is_equal_image(self, filename: str) -> bool:
        return self.__filename == filename

    def setup_ui(self) -> None:
        self.__actionOpenImage.setObjectName(u'__actionOpenImage')
        self.__actionOpenImage.triggered.connect(self.open_image)

        self.__actionCloseImage.setObjectName(u'__actionCloseImage')
        self.__actionCloseImage.triggered.connect(self.close_image)

        self.__actionQuit.setObjectName(u'__actionQuit')
        self.__actionQuit.triggered.connect(self.close)

        self.__imageWidget.setObjectName(u'__imageWidget')

        self.__imageManipulationGroup.setObjectName(u'__imageManipulationGroup')

        self.__resize64x64Button.setObjectName(u'__resize64x64Button')
        self.__resize64x64Button.setGeometry(QRect(311, 470, 78, 25))
        self.__resize64x64Button.clicked.connect(self.decrease_to_64)
        self.__imageManipulationGroup.addButton(self.__resize64x64Button)

        self.__resize32x32Button.setObjectName(u'__resize32x32Button')
        self.__resize32x32Button.setGeometry(QRect(230, 470, 77, 25))
        self.__resize32x32Button.clicked.connect(self.decrease_to_32)
        self.__imageManipulationGroup.addButton(self.__resize32x32Button)

        self.__equalizeButton.setObjectName(u'__equalizeButton')
        self.__equalizeButton.setGeometry(QRect(474, 470, 77, 25))
        self.__imageManipulationGroup.addButton(self.__equalizeButton)

        self.__originalImageButton.setObjectName(u'__originalImageButton')
        self.__originalImageButton.setGeometry(QRect(393, 470, 77, 25))
        self.__originalImageButton.clicked.connect(self.recover_original_image)
        self.__imageManipulationGroup.addButton(self.__originalImageButton)

        self.__imageLabel.setObjectName(u'__imageLabel')
        self.__imageLabel.setGeometry(QRect(20, 20, 671, 431))
        self.__imageLabel.setFrameShape(QFrame.StyledPanel)
        self.__imageLabel.setFrameShadow(QFrame.Raised)

        self.setCentralWidget(self.__imageWidget)

        self.__menuBar.setObjectName(u'__menuBar')
        self.__menuBar.setGeometry(QRect(0, 0, 729, 22))

        self.__menuFile.setObjectName(u'__menuFile')
        self.setMenuBar(self.__menuBar)

        self.__statusBar.setObjectName(u'__statusBar')
        self.setStatusBar(self.__statusBar)

        self.__menuBar.addAction(self.__menuFile.menuAction())
        self.__menuFile.addAction(self.__actionOpenImage)
        self.__menuFile.addAction(self.__actionCloseImage)
        self.__menuFile.addAction(self.__actionQuit)

        self.retranslate_ui()

        QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self) -> None:
        self.setWindowTitle(QCoreApplication.translate('MainWindow', u'MainWindow', None))

        self.__menuFile.setTitle(QCoreApplication.translate('MainWindow', u'File', None))
        self.__actionOpenImage.setText(QCoreApplication.translate('MainWindow', u'Open Image...', None))
        self.__actionCloseImage.setText(QCoreApplication.translate('MainWindow', u'Close Image', None))
        self.__actionQuit.setText(QCoreApplication.translate('MainWindow', u'Quit', None))

        self.__resize64x64Button.setText(QCoreApplication.translate('MainWindow', u'64x64', None))
        self.__resize32x32Button.setText(QCoreApplication.translate('MainWindow', u'32x32', None))
        self.__originalImageButton.setText(QCoreApplication.translate('MainWindow', u'Original', None))
        self.__equalizeButton.setText(QCoreApplication.translate('MainWindow', u'Equalize', None))

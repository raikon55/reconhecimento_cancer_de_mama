# -*- coding: utf-8 -*-
from PIL.ImageQt import ImageQt
from PySide6 import QtCore
from PySide6.QtCore import QRect, QMetaObject, QCoreApplication, QPoint
from PySide6.QtGui import QPixmap, QAction, QPainter, QPen, QImage, QMouseEvent, QPaintEvent
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QMenuBar, QButtonGroup, QFrame, QMenu, QStatusBar, \
    QMainWindow, QInputDialog, QRubberBand, QDialog, QMessageBox

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
    __zoomOutButton: QPushButton
    __zoomInButton: QPushButton

    # Actions
    __actionOpenImage: QAction
    __actionCloseImage: QAction
    __actionQuit: QAction

    __point: QPoint
    __rubberBand: QRubberBand

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
        self.setMouseTracking(True)

        self.__imageWidget = QWidget(self)

        self.__imageManipulationGroup = QButtonGroup(self)
        self.__originalImageButton = QPushButton(self.__imageWidget)
        self.__resize32x32Button = QPushButton(self.__imageWidget)
        self.__resize64x64Button = QPushButton(self.__imageWidget)
        self.__equalizeButton = QPushButton(self.__imageWidget)
        self.__zoomOutButton = QPushButton(self.__imageWidget)
        self.__zoomInButton = QPushButton(self.__imageWidget)

        self.__actionOpenImage = QAction(self)
        self.__actionCloseImage = QAction(self)
        self.__actionQuit = QAction(self)

        self.__menuBar = QMenuBar(self)
        self.__menuFile = QMenu(self.__menuBar)

        self.__statusBar = QStatusBar(self)

        self.__imageLabel = ZoomLabel(self.__imageWidget, alignment=QtCore.Qt.AlignCenter)

        # Init interface
        self.setup_ui()

    def open_image(self) -> None:
        try:
            file_path, ok = QInputDialog.getText(self, u'text', u'Enter image path')

            self.__filename = file_path if ok else None
            self.__imageHandler = ImageHandler(self.__filename)
            self.load_image(can_update=True)
        except FileNotFoundError:
            msgBox = QMessageBox(self)
            msgBox.setText(u'Image path not found')
            msgBox.exec_()

    @QtCore.Slot()
    def load_image(self, can_update: bool = False) -> None:
        if self.__imageHandler is None:
            return

        elif self.__containerImagePixmap is None or can_update:
            q_image: QImage = self.__imageHandler.get_qt_image(original=False)
            self.__containerImagePixmap = QPixmap.fromImage(q_image)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)

        elif self.__containerImagePixmap is not None \
                and self.__imageModified is not None \
                and self.__imageModified != self.__imageHandler.get_image():
            q_image: QImage = self.__imageHandler.get_qt_image(original=False)
            self.__containerImagePixmap = QPixmap.fromImage(q_image)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def recover_original_image(self) -> None:
        try:
            q_image: QImage = self.__imageHandler.get_qt_image(original=True)
            self.__containerImagePixmap = QPixmap.fromImage(q_image)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)
        except AttributeError:
            return

    def close_image(self) -> None:
        self.__imageHandler = None
        self.__containerImagePixmap = None
        self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def create_interface(self) -> None:
        super().show()

    def zoom_out(self) -> None:
        try:
            zoom_image: ImageHandler = self.__imageHandler.zoom_out()
            self.__imageModified = ImageQt(zoom_image)
            self.load_image()
        except AttributeError:
            return

    def zoom_in(self) -> None:
        try:
            zoom_image: ImageHandler = self.__imageHandler.zoom_in(self.__imageLabel.get_initial_point())
            self.__imageModified = ImageQt(zoom_image)
            self.load_image()
        except AttributeError:
            return

    def decrease_to_64(self) -> None:
        try:
            self.__imageModified = ImageQt(self.__imageHandler.new_resolution(64))
            self.load_image()
        except AttributeError:
            return

    def decrease_to_32(self) -> None:
        try:
            self.__imageModified = ImageQt(self.__imageHandler.new_resolution(32))
            self.load_image()
        except AttributeError:
            return

    def equalize(self) -> None:
        print(u'equalize')

    def is_equal_image(self, filename: str) -> bool:
        return self.__filename == filename

    def setup_ui(self) -> None:
        button_place: int = 0
        distance_between_buttons: int = 20
        column_default_position_button: int = 80

        image_label_position: int = column_default_position_button - 50
        image_label_width: int = int(self.width() * 0.8)
        image_label_height: int = int(self.height() * 0.8)

        width_button: int = 80
        height_button: int = 25
        row_position_button: int = image_label_height + 30

        self.__actionOpenImage.setObjectName(u'__actionOpenImage')
        self.__actionOpenImage.triggered.connect(self.open_image)

        self.__actionCloseImage.setObjectName(u'__actionCloseImage')
        self.__actionCloseImage.triggered.connect(self.close_image)

        self.__actionQuit.setObjectName(u'__actionQuit')
        self.__actionQuit.triggered.connect(self.close)

        self.__imageWidget.setObjectName(u'__imageWidget')

        self.__imageManipulationGroup.setObjectName(u'__imageManipulationGroup')

        self.__resize32x32Button.setObjectName(u'__resize32x32Button')
        self.__resize32x32Button.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button,
                  height_button))
        self.__resize32x32Button.clicked.connect(self.decrease_to_32)
        self.__imageManipulationGroup.addButton(self.__resize32x32Button)

        button_place += (width_button + distance_between_buttons)
        self.__resize64x64Button.setObjectName(u'__resize64x64Button')
        self.__resize64x64Button.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button, height_button))
        self.__resize64x64Button.clicked.connect(self.decrease_to_64)
        self.__imageManipulationGroup.addButton(self.__resize64x64Button)

        button_place += (width_button + distance_between_buttons)
        self.__equalizeButton.setObjectName(u'__equalizeButton')
        self.__equalizeButton.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button, height_button))
        self.__equalizeButton.clicked.connect(self.equalize)
        self.__imageManipulationGroup.addButton(self.__equalizeButton)

        button_place += (width_button + distance_between_buttons)
        self.__originalImageButton.setObjectName(u'__originalImageButton')
        self.__originalImageButton.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button, height_button))
        self.__originalImageButton.clicked.connect(self.recover_original_image)
        self.__imageManipulationGroup.addButton(self.__originalImageButton)

        button_place += (width_button + distance_between_buttons)
        self.__zoomInButton.setObjectName(u'__zoomInButton')
        self.__zoomInButton.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button, height_button))
        self.__zoomInButton.clicked.connect(self.zoom_in)
        self.__imageManipulationGroup.addButton(self.__zoomInButton)

        button_place += (width_button + distance_between_buttons)
        self.__zoomOutButton.setObjectName(u'__zoomOutButton')
        self.__zoomOutButton.setGeometry(
            QRect(column_default_position_button + button_place, row_position_button, width_button, height_button))
        self.__zoomOutButton.clicked.connect(self.zoom_out)
        self.__imageManipulationGroup.addButton(self.__zoomOutButton)

        self.__imageLabel.setObjectName(u'__imageLabel')
        self.__imageLabel.setGeometry(QRect(image_label_position, 20, image_label_width, image_label_height))
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

        self.translate_ui()

        QMetaObject.connectSlotsByName(self)

    def translate_ui(self) -> None:
        self.setWindowTitle(QCoreApplication.translate('MainWindow', u'ImagePy', None))

        self.__menuFile.setTitle(QCoreApplication.translate('MainWindow', u'File', None))
        self.__actionOpenImage.setText(QCoreApplication.translate('MainWindow', u'Open Image...', None))
        self.__actionCloseImage.setText(QCoreApplication.translate('MainWindow', u'Close Image', None))
        self.__actionQuit.setText(QCoreApplication.translate('MainWindow', u'Quit', None))

        self.__resize64x64Button.setText(QCoreApplication.translate('MainWindow', u'64x64', None))
        self.__resize32x32Button.setText(QCoreApplication.translate('MainWindow', u'32x32', None))
        self.__originalImageButton.setText(QCoreApplication.translate('MainWindow', u'Original', None))
        self.__equalizeButton.setText(QCoreApplication.translate('MainWindow', u'Equalize', None))
        self.__zoomInButton.setText(QCoreApplication.translate('MainWindow', u'Zoom In', None))
        self.__zoomOutButton.setText(QCoreApplication.translate('MainWindow', u'Zoom Out', None))


class ZoomLabel(QLabel):
    __x: int = 0
    __y: int = 0
    __flag: bool = False

    def __init__(self, widget: QWidget, alignment: QtCore.Qt.AlignmentFlag):
        super().__init__(widget, alignment=alignment)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__flag = True
        self.__x = event.x()
        self.__y = event.y()
        self.update()

    def mouseReleaseEvent(self, event: QPaintEvent) -> None:
        self.__flag = False

    def mouseMoveEvent(self, event: QPaintEvent) -> None:
        if self.__flag:
            self.__x = event.x()
            self.__y = event.y()
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        rect = QRect(self.__x, self.__y, 128, 128)
        painter: QPainter = QPainter(self)
        painter.setPen(QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine))
        painter.drawRect(rect)

    def get_initial_point(self) -> tuple:
        return self.__x, self.__y

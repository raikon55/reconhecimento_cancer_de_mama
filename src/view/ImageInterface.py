# -*- coding: utf-8 -*-

from PIL.ImageQt import ImageQt
from PySide6 import QtCore
from PySide6.QtCore import QRect, QMetaObject, QCoreApplication
from PySide6.QtGui import QPixmap, QAction, QPainter, QPen, QImage, QMouseEvent, QPaintEvent, QPalette
from PySide6.QtWidgets import QLabel, QPushButton, QWidget, QMenuBar, QButtonGroup, QFrame, QMenu, QMainWindow, \
    QFileDialog, QComboBox, QMessageBox, QRadioButton, QScrollArea, QVBoxLayout

from ..classification.ImageClassification import ImageClassification
from ..handler.ImageHandler import ImageHandler


class ImageInterface(QMainWindow):
    # Cache
    __filename: str = None

    # Flow control
    __can_update: bool
    __can_classify_full_image: bool

    # Interface dimensions
    __buttonPlace: int
    __distanceBetweenButtons: int
    __columnDefaultPositionButton: int

    __imageLabelRow: int
    __imageLabelWidth: int
    __imageLabelColumn: int
    __imageLabelHeight: int

    __widthButton: int
    __heightButton: int
    __rowPositionButton: int

    # Interface
    # Buttons
    __zoomInButton: QPushButton
    __zoomOutButton: QPushButton
    __equalizeButton: QPushButton
    __grayScaleButton: QPushButton
    __resize32x32Button: QPushButton
    __resize64x64Button: QPushButton
    __originalImageButton: QPushButton
    __classifyImageButton: QPushButton
    __imageManipulationGroup: QButtonGroup

    __comboboxGrayScale: QComboBox
    __classifierRadioButton: QRadioButton

    # Actions
    __actionQuit: QAction
    __actionOpenImage: QAction
    __actionCloseImage: QAction

    __actionTrainClassifier: QAction

    # Menu
    __menuBar: QMenuBar
    __menuFile: QMenu
    __menuClassifier: QMenu
    # __subMenuSelectFilter: QMenu

    # Wrapper to image handler
    __imageModified: ImageQt = None
    __imageContainer: ImageQt = None
    __imageHandler: ImageHandler = None

    # Classifier
    __classifier: ImageClassification

    __imageLabel: QLabel
    __imageWidget: QWidget = None
    __containerImagePixmap: QPixmap = None

    def __init__(self):
        # Configure interface
        super().__init__()
        self.setObjectName(u'ImagePy')
        self.resize(1366, 786)
        self.setMouseTracking(True)

        self.__buttonPlace = 0
        self.__distanceBetweenButtons = 20
        self.__columnDefaultPositionButton = 80

        self.__widthButton = 80
        self.__heightButton = 25
        self.__rowPositionButton = 10

        self.__imageLabelWidth = int(self.width() * 0.8)
        self.__imageLabelHeight = int(self.height() * 0.8)
        self.__imageLabelRow = self.__rowPositionButton + 40
        self.__imageLabelColumn = self.__columnDefaultPositionButton - 20

        self.__can_update = False
        self.__can_classify_full_image = False

        self.__imageWidget = QWidget(self)

        self.__imageManipulationGroup = QButtonGroup(self)
        self.__zoomInButton = QPushButton(self.__imageWidget)
        self.__zoomOutButton = QPushButton(self.__imageWidget)
        self.__equalizeButton = QPushButton(self.__imageWidget)
        self.__grayScaleButton = QPushButton(self.__imageWidget)
        self.__resize64x64Button = QPushButton(self.__imageWidget)
        self.__resize32x32Button = QPushButton(self.__imageWidget)
        self.__originalImageButton = QPushButton(self.__imageWidget)
        self.__classifyImageButton = QPushButton(self.__imageWidget)
        self.__classifyImageButton.setVisible(False)

        self.__comboboxGrayScale = QComboBox(self.__imageWidget)
        self.__comboboxGrayScale.addItems([u'16', u'32', u'256'])

        self.__classifierRadioButton = QRadioButton(self)
        self.__classifierRadioButton.setText(u'Select region')
        self.__classifierRadioButton.setVisible(False)

        self.__actionQuit = QAction(self)
        self.__actionOpenImage = QAction(self)
        self.__actionCloseImage = QAction(self)

        self.__actionTrainClassifier = QAction(self)

        self.__menuBar = QMenuBar(self)
        self.__menuFile = QMenu(self.__menuBar)
        self.__menuClassifier = QMenu(self.__menuBar)

        self.__imageLabel = ZoomLabel(self.__imageWidget, alignment=QtCore.Qt.AlignCenter)

        # Init interface
        self.setup_ui()

    def open_image(self) -> None:
        file_name: tuple = QFileDialog.getOpenFileName(self, u'Open Image', u'image', u'Images (*.png *.tif *.jpg)')
        self.__filename = file_name[0]

        self.__imageHandler = ImageHandler(self.__filename)

        new_size: tuple = self.__imageHandler.get_image_size()
        self.__imageLabelWidth = int(new_size[0])
        self.__imageLabelHeight = int(new_size[1])
        self.__imageHandler.set_image_size((new_size[0], new_size[1]))
        self.__imageLabel.resize(new_size[0], new_size[1])
        self.__imageLabel.update()
        self.__can_update = True
        self.load_image()

    def load_image(self) -> None:
        if self.__imageHandler is None:
            return

        elif self.__containerImagePixmap is None or self.__can_update:
            q_image: QImage = self.__imageHandler.get_qt_image(original=False)
            self.__containerImagePixmap = QPixmap.fromImage(q_image)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)
            self.__can_update = False

        elif self.__containerImagePixmap is not None \
                and self.__imageModified is not None \
                and self.__imageModified != self.__imageHandler.get_image():
            q_image: QImage = self.__imageHandler.get_qt_image(original=False)
            self.__containerImagePixmap = QPixmap.fromImage(q_image)
            self.__imageLabel.setPixmap(self.__containerImagePixmap)

    def recover_original_image(self) -> None:
        try:
            self.__containerImagePixmap = QPixmap.fromImage(self.__imageHandler.get_qt_image(original=True))
            self.__imageLabel.setPixmap(self.__containerImagePixmap)
        except AttributeError:
            return

    def close_image(self) -> None:
        self.__imageHandler = None
        self.__imageLabel.setPixmap(None)
        del self.__imageHandler

    def create_interface(self) -> None:
        super().show()

    def zoom_out(self) -> None:
        try:
            self.__imageModified = ImageQt(self.__imageHandler.zoom_out())
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
        try:
            self.__imageModified = ImageQt(self.__imageHandler.equalize())
            self.load_image()
        except AttributeError:
            return

    def change_gray_scale(self) -> None:
        try:
            scale: int = int(self.__comboboxGrayScale.currentText())
            self.__imageModified = ImageQt(self.__imageHandler.gray_scale(scale))
            self.load_image()
        except AttributeError:
            return

    def train_classifier(self) -> None:
        dataset: str = QFileDialog.getExistingDirectory(self, u'Select Dataset folder', u'')

        self.__classifier = ImageClassification()
        self.__classifier.load_images(dataset)
        self.__classifier.train()

        self.__classifyImageButton.setVisible(True)
        self.__classifierRadioButton.setVisible(True)

        msg_box: QMessageBox = QMessageBox(self)
        msg_box.setWindowTitle(u'Classifier Result')
        msg_box.setText(self.__classifier.show_confusion_matrix())
        msg_box.exec_()

    def classify_image(self) -> None:
        self.__can_classify_full_image = not self.__classifierRadioButton.isChecked()

        if self.__can_classify_full_image:
            self.__imageHandler.get_image(original=True).save(u'image/image.png')
        else:
            self.__imageHandler.zoom_in(self.__imageLabel.get_initial_point()).save(u'image/image.png')
            self.__imageHandler.zoom_out()

        result: str = self.__classifier.classify_single_image(u'image/image.png')
        msg_box: QMessageBox = QMessageBox(self)
        msg_box.setWindowTitle(u'Classifier Result')
        msg_box.setText(result)
        msg_box.exec_()

    def is_equal_image(self, filename: str) -> bool:
        return self.__filename == filename

    def setup_ui(self) -> None:
        self.__actionOpenImage.setObjectName(u'&__actionOpenImage')
        self.__actionOpenImage.triggered.connect(self.open_image)

        self.__actionCloseImage.setObjectName(u'&__actionCloseImage')
        self.__actionCloseImage.triggered.connect(self.close_image)

        self.__actionQuit.setObjectName(u'&__actionQuit')
        self.__actionQuit.triggered.connect(self.close)

        self.__actionTrainClassifier.setObjectName(u'&__actionTrainClassifier')
        self.__actionTrainClassifier.triggered.connect(self.train_classifier)

        self.__imageWidget.setObjectName(u'&__imageWidget')

        self.__imageManipulationGroup.setObjectName(u'&__imageManipulationGroup')

        self.__originalImageButton.setObjectName(u'&__originalImageButton')
        self.__originalImageButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__originalImageButton.clicked.connect(self.recover_original_image)
        self.__imageManipulationGroup.addButton(self.__originalImageButton)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__resize32x32Button.setObjectName(u'&__resize32x32Button')
        self.__resize32x32Button.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__resize32x32Button.clicked.connect(self.decrease_to_32)
        self.__imageManipulationGroup.addButton(self.__resize32x32Button)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__resize64x64Button.setObjectName(u'&__resize64x64Button')
        self.__resize64x64Button.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__resize64x64Button.clicked.connect(self.decrease_to_64)
        self.__imageManipulationGroup.addButton(self.__resize64x64Button)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__zoomInButton.setObjectName(u'&__zoomInButton')
        self.__zoomInButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__zoomInButton.clicked.connect(self.zoom_in)
        self.__imageManipulationGroup.addButton(self.__zoomInButton)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__zoomOutButton.setObjectName(u'&__zoomOutButton')
        self.__zoomOutButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__zoomOutButton.clicked.connect(self.zoom_out)
        self.__imageManipulationGroup.addButton(self.__zoomOutButton)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__equalizeButton.setObjectName(u'&__equalizeButton')
        self.__equalizeButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__equalizeButton.clicked.connect(self.equalize)
        self.__imageManipulationGroup.addButton(self.__equalizeButton)

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons)
        self.__grayScaleButton.setObjectName(u'&__grayScaleButton')
        self.__grayScaleButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton, self.__widthButton,
                  self.__heightButton))
        self.__grayScaleButton.clicked.connect(self.change_gray_scale)
        self.__imageManipulationGroup.addButton(self.__grayScaleButton)

        self.__comboboxGrayScale.setObjectName(u'&__comboboxGrayScale')
        self.__comboboxGrayScale.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace + self.__widthButton - 2,
                  self.__rowPositionButton + 1, int(self.__widthButton * 0.6), self.__heightButton - 2))

        self.__buttonPlace += (self.__widthButton + self.__distanceBetweenButtons + 45)
        self.__classifyImageButton.setObjectName(u'&__classifyImageButton')
        self.__classifyImageButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace, self.__rowPositionButton,
                  self.__widthButton + 10,
                  self.__heightButton))
        self.__classifyImageButton.clicked.connect(self.classify_image)
        self.__imageManipulationGroup.addButton(self.__classifyImageButton)

        self.__classifierRadioButton.setObjectName(u'&__classifierRadioButton')
        self.__classifierRadioButton.setGeometry(
            QRect(self.__columnDefaultPositionButton + self.__buttonPlace + self.__widthButton + 15,
                  self.__rowPositionButton + 22, 120, self.__heightButton - 2))

        self.__imageLabel.setObjectName(u'&__imageLabel')
        self.__imageLabel.setGeometry(
            QRect(self.__imageLabelColumn, self.__imageLabelRow, self.__imageLabelWidth, self.__imageLabelHeight))
        self.__imageLabel.setFrameShape(QFrame.StyledPanel)
        self.__imageLabel.setFrameShadow(QFrame.Raised)

        self.setCentralWidget(self.__imageWidget)

        self.__menuBar.setObjectName(u'&__menuBar')
        self.__menuBar.setGeometry(QRect(0, 0, 729, 22))

        self.__menuFile.setObjectName(u'&__menuFile')
        self.setMenuBar(self.__menuBar)

        self.__menuClassifier.setObjectName(u'&__menuClassifier')
        self.setMenuBar(self.__menuBar)

        self.__menuBar.addAction(self.__menuFile.menuAction())
        self.__menuFile.addAction(self.__actionOpenImage)
        self.__menuFile.addAction(self.__actionCloseImage)
        self.__menuFile.addAction(self.__actionQuit)

        self.__menuBar.addAction(self.__menuClassifier.menuAction())
        self.__menuClassifier.addAction(self.__actionTrainClassifier)

        self.translate_ui()

        QMetaObject.connectSlotsByName(self)
        self.__buttonPlace = 0

    def translate_ui(self) -> None:
        self.setWindowTitle(QCoreApplication.translate('MainWindow', u'ImagePy', None))

        self.__menuFile.setTitle(QCoreApplication.translate('MainWindow', u'File', None))
        self.__actionOpenImage.setText(QCoreApplication.translate('MainWindow', u'Open Image...', None))
        self.__actionCloseImage.setText(QCoreApplication.translate('MainWindow', u'Close Image', None))
        self.__actionQuit.setText(QCoreApplication.translate('MainWindow', u'Quit', None))

        self.__menuClassifier.setTitle(QCoreApplication.translate('MainWindow', u'Classifier', None))
        self.__actionTrainClassifier.setText(QCoreApplication.translate('MainWindow', u'Train from dataset...', None))

        self.__resize64x64Button.setText(QCoreApplication.translate('MainWindow', u'64x64', None))
        self.__resize32x32Button.setText(QCoreApplication.translate('MainWindow', u'32x32', None))
        self.__originalImageButton.setText(QCoreApplication.translate('MainWindow', u'Original', None))
        self.__equalizeButton.setText(QCoreApplication.translate('MainWindow', u'Equalize', None))
        self.__grayScaleButton.setText(QCoreApplication.translate('MainWindow', u'Gray Scale', None))
        self.__zoomInButton.setText(QCoreApplication.translate('MainWindow', u'Zoom In', None))
        self.__zoomOutButton.setText(QCoreApplication.translate('MainWindow', u'Zoom Out', None))
        self.__classifyImageButton.setText(QCoreApplication.translate('MainWindow', u'Classify Image', None))


class ZoomLabel(QLabel):
    __x: int = 0
    __y: int = 0
    __flag: bool = False

    def __init__(self, widget: QWidget, alignment: QtCore.Qt.AlignmentFlag):
        super().__init__(widget, alignment=alignment)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__flag = True
        self.__x = (event.x() - 64)
        self.__y = (event.y() - 64)
        self.update()

    def mouseReleaseEvent(self, event: QPaintEvent) -> None:
        self.__flag = False

    def mouseMoveEvent(self, event: QPaintEvent) -> None:
        if self.__flag:
            self.__x = (event.x() - 64)
            self.__y = (event.y() - 64)
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        rect: QRect = QRect(self.__x, self.__y, 128, 128)
        painter: QPainter = QPainter(self)
        painter.setPen(QPen(QtCore.Qt.blue, 1, QtCore.Qt.SolidLine))
        painter.drawRect(rect)

    def get_initial_point(self) -> tuple:
        return self.__x, self.__y

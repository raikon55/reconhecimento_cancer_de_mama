# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imageInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtGui import QAction


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(720, 560)
        self.__actionOpen_Image = QAction(MainWindow)
        self.__actionOpen_Image.setObjectName(u"__actionOpen_Image")
        self.__actionQuit = QAction(MainWindow)
        self.__actionQuit.setObjectName(u"__actionQuit")
        self.__actionClose_Image = QAction(MainWindow)
        self.__actionClose_Image.setObjectName(u"__actionClose_Image")
        self.__imageWidget = QWidget(MainWindow)
        self.__imageWidget.setObjectName(u"__imageWidget")
        self.__resize64x64Button = QPushButton(self.__imageWidget)
        self.__imageManipulationGroup = QButtonGroup(MainWindow)
        self.__imageManipulationGroup.setObjectName(u"__imageManipulationGroup")
        self.__imageManipulationGroup.addButton(self.__resize64x64Button)
        self.__resize64x64Button.setObjectName(u"__resize64x64Button")
        self.__resize64x64Button.setGeometry(QRect(311, 470, 78, 25))
        self.__resize32x32Button = QPushButton(self.__imageWidget)
        self.__imageManipulationGroup.addButton(self.__resize32x32Button)
        self.__resize32x32Button.setObjectName(u"__resize32x32Button")
        self.__resize32x32Button.setGeometry(QRect(230, 470, 77, 25))
        self.__imageContainer = QFrame(self.__imageWidget)
        self.__imageContainer.setObjectName(u"__imageContainer")
        self.__imageContainer.setGeometry(QRect(29, 29, 671, 421))
        self.__imageContainer.setFrameShape(QFrame.StyledPanel)
        self.__imageContainer.setFrameShadow(QFrame.Raised)
        self.__equalizeButton = QPushButton(self.__imageWidget)
        self.__imageManipulationGroup.addButton(self.__equalizeButton)
        self.__equalizeButton.setObjectName(u"__equalizeButton")
        self.__equalizeButton.setGeometry(QRect(393, 470, 77, 25))
        MainWindow.setCentralWidget(self.__imageWidget)
        self.__menubar = QMenuBar(MainWindow)
        self.__menubar.setObjectName(u"__menubar")
        self.__menubar.setGeometry(QRect(0, 0, 729, 22))
        self.__menuFile = QMenu(self.__menubar)
        self.__menuFile.setObjectName(u"__menuFile")
        MainWindow.setMenuBar(self.__menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.__menubar.addAction(self.__menuFile.menuAction())
        self.__menuFile.addAction(self.__actionOpen_Image)
        self.__menuFile.addAction(self.__actionClose_Image)
        self.__menuFile.addAction(self.__actionQuit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.__actionOpen_Image.setText(QCoreApplication.translate("MainWindow", u"Open Image...", None))
        self.__actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.__actionClose_Image.setText(QCoreApplication.translate("MainWindow", u"Close Image", None))
        self.__resize64x64Button.setText(QCoreApplication.translate("MainWindow", u"64x64", None))
        self.__resize32x32Button.setText(QCoreApplication.translate("MainWindow", u"32x32", None))
        self.__equalizeButton.setText(QCoreApplication.translate("MainWindow", u"Equalize", None))
        self.__menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


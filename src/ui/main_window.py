import sys

from PyQt5.QtWidgets import *

from src.layout_creation.image_provider import ImageProvider
from src.logic.project_handler import ProjectHandler
from src.ui.central_widget import CentralWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menuBar = self.menuBar()
        fileMenu = QMenu("File", self)

        save_action = QAction("Save", self)
        #save_action.setStatusTip("Select a file to use as a database")
        save_action.triggered.connect(self.__show_save_window)
        fileMenu.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.__show_load_window)
        fileMenu.addAction(load_action)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        fileMenu.addAction(quit_action)

        menuBar.addMenu(fileMenu)

        image_provider = ImageProvider()
        self._project_handler = ProjectHandler(image_provider)
        cw = CentralWidget(image_provider, self._project_handler)
        self.setCentralWidget(cw)

    def __show_save_window(self):
        print("Show save window")

    def __show_load_window(self):
        print("Show load window")


def show_window():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(1280, 1024)
    mw.show()

    sys.exit(app.exec_())
import sys

from PyQt5.QtWidgets import *

from src.layout_creation.image_provider import ImageProvider
from src.logic.project_handler import ProjectHandler
from src.ui.central_widget import CentralWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)

        save_action = QAction("Save", self)
        #save_action.setStatusTip("Select a file to use as a database")
        save_action.triggered.connect(self.__show_save_window)
        file_menu.addAction(save_action)

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.__show_load_window)
        file_menu.addAction(load_action)

        render_action = QAction("Render", self)
        render_action.triggered.connect(self.__render)
        file_menu.addAction(render_action)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        menu_bar.addMenu(file_menu)

        image_provider = ImageProvider()
        self._project_handler = ProjectHandler(image_provider)
        cw = CentralWidget(image_provider, self._project_handler)
        self.setCentralWidget(cw)

    def __show_save_window(self):
        print("Show save window")
        self._project_handler.save_project("/home/woody/albumtest/")

    def __show_load_window(self):
        print("Show load window")

    def __render(self):
        self._project_handler.render("/home/woody/albumtest/")


def show_window():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(1280, 1024)
    mw.show()

    sys.exit(app.exec_())

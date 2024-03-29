import sys

from PyQt5.QtWidgets import *

from src.utils.image_cache import ImageCache
from src.logic.project_handler import ProjectHandler
from src.ui import UiUtils
from src.ui.central_widget import CentralWidget

# TODO: save in some configuration the latest directory used
DEFAULT_DIRECTORY = "/home/woody/albumtest/"


# TODO: add an options dialog to set default project page size, border, etc.
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menu_bar = self.menuBar()
        file_menu = QMenu("File", self)

        save_action = QAction("Save", self)
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

        image_provider = ImageCache()
        self._project_handler = ProjectHandler(image_provider)
        cw = CentralWidget(image_provider, self._project_handler)
        self.setCentralWidget(cw)

    def __show_save_window(self):
        name = QFileDialog.getSaveFileName(self, 'Save Project', DEFAULT_DIRECTORY + "project.pa", "(*.pa)")
        if not name or not name[0]:
            return
        self._project_handler.save_project(name[0])

    def __show_load_window(self):
        if self._project_handler.has_changes():
            # TODO: allow discarding changes
            msg = UiUtils.get_warning_window("Current project has changes, please save it. This message should allow to continue with discard changes option")
            msg.exec()
            return

        name = QFileDialog.getOpenFileName(self, 'Open Project', DEFAULT_DIRECTORY, "(*.pa)")
        if not name or not name[0]:
            return
        self._project_handler.load_project(name[0])

    def __render(self):
        path = QFileDialog.getExistingDirectory(self, 'Render to...', DEFAULT_DIRECTORY)
        if not path or not path[0]:
            return
        self._project_handler.render(path + "/")


def show_window():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.resize(1280, 1024)
    mw.show()

    sys.exit(app.exec_())

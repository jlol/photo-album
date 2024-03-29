import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QFileDialog

from src.album_project import album_utils
from src.album_project.album import Page
from src.logic.project_handler import ProjectHandler
from src.ui import UiUtils
from src.ui.clickable_label import ClickableLabel
from src.ui.event import Event


class ImageListUI:

    THUMBNAIL_WIDTH = 150
    THUMBNAIL_HEIGHT = 150

    def __init__(self, box_layout: QtWidgets.QVBoxLayout,
                 add_image_button: QPushButton,
                 clear_images_button: QPushButton,
                 project_handler: ProjectHandler):
        add_image_button.clicked.connect(self.add_button_clicked)
        clear_images_button.clicked.connect(self.clear_button_clicked)
        self.box_layout = box_layout
        self._image_removed = Event()
        self._images_added_event = Event()
        self._clear_images_event = Event()
        project_handler.on_page_change_event += self.on_page_changed

    def on_page_changed(self, page: Page):
        self.clear()
        filenames = album_utils.get_page_image_paths(page)
        self.__load_thumbnails_for_filenames(filenames, self.box_layout.count())

    def image_removed_event(self) -> Event:
        return self._image_removed

    def images_added_event(self) -> Event:
        return self._images_added_event

    def clear_images_event(self) -> Event:
        return self._clear_images_event

    def add_button_clicked(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setOption(QFileDialog.DontUseNativeDialog)
        dlg.setNameFilter(UiUtils.INPUT_IMAGE_FILE_FILTER)

        if not dlg.exec_():
            return

        filenames = dlg.selectedFiles()
        if filenames is None or len(filenames) == 0:
            pass
        self.add_files(filenames)

    def clear_button_clicked(self):
        self.clear()
        self._clear_images_event.notify()

    def add_files(self, filenames):
        if self.load_files(filenames):
            self._images_added_event.notify(filenames)

    def load_files(self, filenames) -> bool:
        if filenames is None or len(filenames) == 0:
            return False

        self.__load_thumbnails_for_filenames(filenames, self.box_layout.count())
        return True

    def __load_thumbnails_for_filenames(self, filenames: [str], starting_index: int):
        iconroot = os.path.dirname(__file__)
        index = starting_index

        for file in filenames:
            self.__add_image_label(file, iconroot, index)
            index += 1

    def __add_image_label(self, file, iconroot, index):
        label = ClickableLabel()
        pixmap = QPixmap(os.path.join(iconroot, file))
        label.set_index(index)
        label.clicked.connect(self.__on_image_clicked)
        label.resize(self.THUMBNAIL_WIDTH, self.THUMBNAIL_HEIGHT)
        label.setPixmap(pixmap.scaled(label.size(),
                                      QtCore.Qt.KeepAspectRatio))
        self.box_layout.addWidget(label)

    def __on_image_clicked(self, index):
        self.__remove_image_at(index)
        self._image_removed.notify(index)

    def clear(self):
        while self.box_layout.count():
            self.__remove_image_by_index(0)

    def __remove_image_at(self, index):
        self.__remove_image_by_index(index)
        self.__rearrange_image_items()

    def __remove_image_by_index(self, index):
        item = self.box_layout.takeAt(index)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()

    def __rearrange_image_items(self):
        for i in range(self.box_layout.count()):
            item = self.box_layout.itemAt(i)
            item.widget().set_index(i)

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QFrame, QSpinBox, QPushButton, QApplication, \
    QStyleFactory, QSpacerItem, QSizePolicy

from src.album_project.album import Page
from src.utils.image_cache import ImageCache
from src.logic.project_handler import ProjectHandler
from src.opengl.album_visualizer import AlbumVisualizer
from src.ui import UiUtils
from src.ui.event import Event
from src.ui.image_list_ui import ImageListUI
from src.utils.MathUtils import Vector2


class CentralWidget(QWidget):
    def __init__(self, image_provider: ImageCache, project_handler: ProjectHandler):
        super(CentralWidget, self).__init__()
        self._image_provider = image_provider
        self._project_handler = project_handler
        self._project_handler.on_page_change_event += self.on_page_changed
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        splitter = QSplitter(QtCore.Qt.Horizontal)

        left_vbox = QVBoxLayout(self)
        # Add left bar
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)

        # Page selector
        page_selector = QSpinBox(self)
        page_selector.valueChanged.connect(self.__page_selected)
        left_vbox.addWidget(page_selector)
        add_page_button = QPushButton("Add page")
        left_vbox.addWidget(add_page_button)
        # TODO: stop using magic numbers and have a dialog to select the page size, border, etc (or temporarily keep per project page size)
        add_page_button.clicked.connect(lambda: self._project_handler.add_page(Vector2(3508, 2480), 2.0))

        # Render and project
        render_button = QPushButton("Update preview")
        render_button.clicked.connect(self.__render_pressed)

        left_vbox.addWidget(render_button)

        # Photo handling
        self.__photo_handling_setup(left_vbox)

        left.setLayout(left_vbox)
        splitter.addWidget(left)

        # Add Opengl viewer
        self.album_visualizer = AlbumVisualizer(self._image_provider, self._project_handler)
        self.album_visualizer.resize(1024, 1024)
        splitter.addWidget(self.album_visualizer)

        splitter.setStretchFactor(1, 1)
        splitter.setSizes([125, 150])

        # Add spliter to widget and setup
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        self.setGeometry(0, 0, 1280, 1024)
        self.setWindowTitle('Photo Album')

    def on_page_changed(self, page: Page):
        assert page, "Page is null"
        self.album_visualizer.cleanup_photos()
        for p in page.photos:
            self.album_visualizer.add_photo(p.path, p.rect_minus_borders, p.offset)

    def __page_selected(self, index: int):
        self._project_handler.select_page(index)

    def __photo_handling_setup(self, left_vbox):
        # Photo handling
        photos_frame = QFrame(self)
        left_vbox.addWidget(photos_frame)
        add_photo_button = QPushButton("Add photos")
        left_vbox.addWidget(add_photo_button)
        clear_photos_button = QPushButton("Clear photos")
        left_vbox.addWidget(clear_photos_button)
        thumbnail_frame = QFrame(self)
        thumbnail_layout = QVBoxLayout(self)
        thumbnail_frame.setLayout(thumbnail_layout)
        left_vbox.addWidget(thumbnail_frame)
        vspacer = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_vbox.addItem(vspacer)

        # Thumbnails controller
        self.image_list = ImageListUI(thumbnail_layout, add_photo_button, clear_photos_button, self._project_handler)

        # Project Handler events
        image_removed: Event = self.image_list.image_removed_event()
        images_added: Event = self.image_list.images_added_event()
        clear_images: Event = self.image_list.clear_images_event()
        images_added.attach(lambda filenames: self._project_handler.images_added(filenames))
        image_removed.attach(lambda index: self._project_handler.image_removed(index))
        clear_images.attach(lambda: self._project_handler.images_cleared())

    def __render_pressed(self):
        if not self._project_handler.has_photos_in_current_page():
            msg = UiUtils.get_warning_window("Cannot create layout, no photos for page")
            msg.exec()
            return

        page = self._project_handler.update_layout()
        self.album_visualizer.cleanup_photos()
        for p in page.photos:
            self.album_visualizer.add_photo(p.path, p.rect_minus_borders, p.offset)

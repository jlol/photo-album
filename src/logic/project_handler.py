from src.album_project import album_utils
from src.album_project.album import Page, Album, Vector2, Photo
from src.layout_creation.image_provider import ImageProvider
from src.layout_creation.layout_creator import LayoutCreator
from src.logic.page_renderer import PageRenderer
from src.utils.custom_event import CustomEvent

MAX_ITERATIONS = 20


class ProjectHandler:
    def __init__(self, image_provider: ImageProvider):
        self._current_page_index = 0
        self._album = Album()
        self._current_page_photos: [str] = []
        self._current_page_size = Vector2(0, 0)
        self._current_page_border = 0.0
        self._current_page_bg_color = (255, 255, 255)
        self.add_page(Vector2(3508, 2480), 20.0)
        self._image_provider = image_provider
        self.on_page_change_event = CustomEvent()

    # TODO: keep track of unsaved changes
    def has_changes(self):
        return False

    def select_page(self, page_index: int):
        if self._album.number_of_pages() <= page_index or page_index < 0:
            print("Page doesn't exist")
            return

        self._current_page_index = page_index
        page = self._album.get_page(page_index)
        self._current_page_size = page.size
        self._current_page_border = page.border
        self._current_page_bg_color = page.border_color
        self._current_page_photos.clear()

        for p in page.photos:
            self._current_page_photos.append(p.path)


    def add_page(self, size: Vector2, border: float, bg_color=(255, 255, 255)):
        self._current_page_index = -1
        self._current_page_size = size
        self._current_page_border = border
        self._current_page_bg_color = bg_color
        self._current_page_photos.clear()

    def images_added(self, filenames: [str]):
        self._current_page_photos.extend(filenames)

    def image_removed(self, index: int):
        self._current_page_photos.pop(index)

    def images_cleared(self):
        self._current_page_photos.clear()

    def has_photos_in_current_page(self) -> bool:
        return len(self._current_page_photos) > 0

    def update_layout(self) -> Page:
        assert self.has_photos_in_current_page(), "Cannot update a layout without photos"

        for img in self._current_page_photos:
            self._image_provider.add_image(img)

        lc = LayoutCreator(
            [self._current_page_size.x, self._current_page_size.y],
            self._image_provider,
            self._current_page_border,
            self._current_page_bg_color
        )
        layout = lc.create_layout()
        best_score = layout.score

        for i in range(0, MAX_ITERATIONS):
            tmp_layout = lc.create_layout()

            if tmp_layout.score < best_score:
                best_score = tmp_layout.score
                layout = tmp_layout

        page = album_utils.layout_to_page(layout)

        if self._current_page_index < 0:
            self._album.add_page(page)
            self._current_page_index = 0
        else:
            self._album.replace_page(self._current_page_index, page)

        return page

    def image_offset_applied(self, index: int, offset: Vector2):
        current_page = self._album.get_page(self._current_page_index)
        photo = current_page.photos[index]
        photo.offset = offset

    def save_project(self, path: str):
        assert path, "Path shouldn't be empty or null"
        print("Saving album to " + path)
        album_utils.save_album(self._album, path)

    def load_project(self, path: str):
        assert path, "Path shouldn't be empty or null"
        print("Loading album from " + path)
        self._album = album_utils.load_album(path)
        self._current_page_index = 0
        current_page = self._album.get_page(0)
        self._current_page_photos: [str] = []

        for p in current_page.photos:
            self._current_page_photos.append(p)

        self._current_page_size = current_page.size
        # TODO: need to modify through ui border, page size, etc
        self._current_page_border = 0.0
        self._current_page_bg_color = (255, 255, 255)
        self.add_page(Vector2(3508, 2480), 20.0)
        self._image_provider.cleanup()
        self.on_page_change_event(current_page)

    def render(self, path: str):
        assert path, "Path shouldn't be empty or null"
        renderer = PageRenderer(self._image_provider)
        renderer.render_album(self._album, path)

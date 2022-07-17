import copy

from src.album_project import album_utils
from src.album_project.album import Page, Album, Vector2
from src.layout_creation.layout_image_provider import LayoutImageProvider
from src.logic.layout_change_listener import LayoutChangeListener
from src.utils.image_cache import ImageCache
from src.layout_creation.layout_creator import LayoutCreator
from src.logic.page_renderer import PageRenderer
from src.utils.custom_event import CustomEvent

MAX_ITERATIONS = 20
DEFAULT_PAGE_SIZE = Vector2(3508, 2480)
DEFAULT_BORDER = 20.0


class ProjectHandler(LayoutChangeListener):

    def __init__(self, image_provider: ImageCache):
        self.__current_page_index = 0
        self.__album = Album()
        self.__current_page_photos: [str] = []
        self.__current_page_size = Vector2(0, 0)
        self.__current_page_border = 0.0
        self.__current_page_bg_color = (255, 255, 255)
        self.on_page_change_event = CustomEvent()
        self.on_page_count_changed_event = CustomEvent()
        self.add_page()
        self.__image_cache = image_provider
        self.__has_changes = False

    def has_changes(self):
        return self.__has_changes

    def select_page(self, page_index: int):
        if self.__album.number_of_pages() <= page_index or page_index < 0:
            print("Page doesn't exist")
            return

        self.__current_page_index = page_index
        page = self.__album.get_page(page_index)
        self.__current_page_size = page.size
        self.__current_page_border = page.border
        self.__current_page_bg_color = page.border_color
        self.__current_page_photos.clear()

        for p in page.photos:
            self.__current_page_photos.append(p.path)

        self.on_page_change_event(page)

    def add_page(self, size: Vector2 = DEFAULT_PAGE_SIZE, border: float = DEFAULT_BORDER, bg_color=(255, 255, 255)):
        self.__has_changes = True
        size_copy = copy.copy(size)
        bg_color_copy = copy.deepcopy(bg_color)
        self.__current_page_size = size_copy
        self.__current_page_border = border
        self.__current_page_bg_color = bg_color_copy
        self.__current_page_photos.clear()
        self.__album.add_page(Page(size_copy, border, bg_color_copy))
        self.on_page_count_changed_event(self.__album.number_of_pages())

    def images_added(self, filenames: [str]):
        self.__current_page_photos.extend(filenames)

    def image_removed(self, index: int):
        self.__current_page_photos.pop(index)

    def images_cleared(self):
        self.__current_page_photos.clear()

    def has_photos_in_current_page(self) -> bool:
        return len(self.__current_page_photos) > 0

    def update_layout(self) -> Page:
        assert self.has_photos_in_current_page(), "Cannot update a layout without photos"

        self.__has_changes = True

        for img in self.__current_page_photos:
            self.__image_cache.add_image(img)

        image_provider = LayoutImageProvider(self.__current_page_photos, self.__image_cache)
        lc = LayoutCreator(
            [self.__current_page_size.x, self.__current_page_size.y],
            image_provider,
            self.__current_page_border,
            self.__current_page_bg_color
        )
        layout = lc.create_layout()
        best_score = layout.score

        for i in range(0, MAX_ITERATIONS):
            tmp_layout = lc.create_layout()

            if tmp_layout.score < best_score:
                best_score = tmp_layout.score
                layout = tmp_layout

        page = album_utils.layout_to_page(layout)
        self.__album.replace_page(self.__current_page_index, page)
        return page

    def save_project(self, path: str):
        assert path, "Path shouldn't be empty or null"
        self.__has_changes = False
        print("Saving album to " + path)
        album_utils.save_album(self.__album, path)

    def load_project(self, path: str):
        assert path, "Path shouldn't be empty or null"
        print("Loading album from " + path)
        self.__has_changes = False
        self.__album = album_utils.load_album(path)
        self.__current_page_index = 0
        current_page = self.__album.get_page(0)
        self.__current_page_photos: [str] = []

        for p in current_page.photos:
            self.__current_page_photos.append(p)

        self.__current_page_size = current_page.size
        self.__current_page_border = current_page.border
        self.__current_page_bg_color = current_page.border_color
        self.__image_cache.cleanup()
        self.on_page_change_event(current_page)
        self.on_page_count_changed_event(self.__album.number_of_pages())

    def render(self, path: str):
        assert path, "Path shouldn't be empty or null"
        renderer = PageRenderer(self.__image_cache)
        renderer.render_album(self.__album, path)

    def image_offset_applied(self, index: int, offset: Vector2):
        self.__has_changes = True
        current_page = self.__album.get_page(self.__current_page_index)
        photo = current_page.photos[index]
        photo.offset = offset

    def image_zoom_applied(self, index: int, zoom: float):
        print("Zoom " + str(index) + " " + str(zoom))

    def image_swap(self, image_index_a: int, image_index_b: int):
        self.__has_changes = True
        current_page = self.__album.get_page(self.__current_page_index)
        path_a = current_page.photos[image_index_a].path
        current_page.photos[image_index_a].path = current_page.photos[image_index_b].path
        current_page.photos[image_index_b].path = path_a

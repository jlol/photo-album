from src.layout_creation.rect import Rect


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return str(self.x) + " " + str(self.y)


class Photo:
    def __init__(self, rect: Rect, rect_minus_borders: Rect, path: str, offset=Vector2(0.0, 0.0)):
        self.rect = rect
        self.rect_minus_borders = rect_minus_borders
        self.path = path
        self.offset = offset


class Page:
    def __init__(self, size: Vector2, border=0.0, border_color=(255, 255, 255)):
        self.photos = []
        self.border_color = border_color
        self.border = border
        self.size = size

    def get_size_as_tuple(self) -> (int, int):
        return self.size.x, self.size.y

    def add_photo(self, photo: Photo):
        self.photos.append(photo)

    def remove_photo(self, index: int):
        self.photos.pop(index)

    def clear_photos(self):
        self.photos.clear()


class Album:
    def __init__(self):
        self._pages = []

    def add_page(self, page: Page):
        self._pages.append(page)

    def get_page(self, index: int):
        return self._pages[index]

    def replace_page(self, index: int, page: Page):
        self._pages[index] = page

    def remove_page(self, index: int):
        self._pages.pop(index)

    def number_of_pages(self):
        return len(self._pages)

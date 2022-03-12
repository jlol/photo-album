from src.layout_creation.rect import Rect


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Photo:
    def __init__(self, rect: Rect, path: str, offset=Vector2(0.0, 0.0)):
        self.rect = rect
        self.path = path
        self.offset = offset


class Page:
    def __init__(self, size: Vector2, border=0.0, border_color=(255, 255, 255)):
        self.photos = []
        self.border_color = border_color
        self.border = border
        self.size = size

    def add_photo(self, photo: Photo):
        self.photos.append(photo)


class Album:
    def __init__(self):
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)

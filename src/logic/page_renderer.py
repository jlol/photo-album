from PIL import Image

from src.album_project.album import Album, Page
from src.layout_creation.image_provider import ImageProvider


class PageRenderer:
    # TODO in the future image_provider should only handle miniatures to save space, the images should be
    # directly loaded from disk
    # TODO check PIL image modes for better color quality
    def __init__(self, image_provider: ImageProvider):
        self._image_provider = image_provider

    def render_album(self, album: Album, path: str):
        for i in range(0, album.number_of_pages()):
            self._render_page(i, album.get_page(i), path)

    def _render_page(self, index: int, page: Page, path: str):
        im = Image.new('RGB', page.get_size_as_tuple(), color = page.border_color)

        for p in page.photos:
            photo = self._image_provider.get_image(p.path)
            # TODO: do resizing if needed and offset applying
            im.paste(photo, p.rect.as_tuple())

        im.save(path + str(index) + ".png")

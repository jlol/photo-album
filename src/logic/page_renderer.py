import copy

from PIL import Image

from src.album_project.album import Album, Page, Photo
from src.utils.image_cache import ImageCache
from src.layout_creation.rect import Rect
from src.utils import ImageUtils
from src.utils.MathUtils import Vector2


class PageRenderer:
    # TODO in the future image_provider should only handle miniatures to save space, the images should be
    # directly loaded from disk
    # TODO check PIL image modes for better color quality
    def __init__(self, image_provider: ImageCache):
        self._image_provider = image_provider

    def render_album(self, album: Album, path: str):
        for i in range(0, album.number_of_pages()):
            self._render_page(i, album.get_page(i), path)

    def _render_page(self, index: int, page: Page, path: str):
        im = Image.new('RGB', page.get_size_as_tuple(), color=page.border_color)

        for p in page.photos:
            image = self._image_provider.get_image(p.path)
            adjusted_image = PageRenderer._get_size_corrected_image(image, p)
            im.paste(adjusted_image, PageRenderer._get_paste_box(p.rect_minus_borders, int(page.size.y)))

        absolute_path = path + str(index) + ".png"
        im.save(absolute_path)
        print("Saved image to " + absolute_path)

    @staticmethod
    def _get_paste_box(rect_minus_borders: Rect, page_height: int):
        left = int(rect_minus_borders.x)
        right = left + int(rect_minus_borders.w)
        down = page_height - int(rect_minus_borders.y)
        up = page_height - int(rect_minus_borders.h + rect_minus_borders.y)
        return left, up, right, down

    @staticmethod
    def _get_size_corrected_image(image: Image, photo: Photo) -> Image:
        original_image_size = Vector2.from_array(image.size)
        # TODO: Better first crop, then scale, otherwise it will take lots of memory
        scaled_size = ImageUtils.scale_size_respecting_ratio(original_image_size, photo.get_size_without_borders())
        scaled_size = Vector2.multiply_by(scaled_size, photo.zoom)
        adjusted_image = image.resize((int(scaled_size.x), int(scaled_size.y)), Image.ANTIALIAS)
        return adjusted_image.crop(PageRenderer._get_image_crop_as_pil_box(adjusted_image, photo))

    @staticmethod
    def _get_image_crop_as_pil_box(image: Image, photo: Photo) -> (int, int, int, int):
        normalized_photo_center = photo.normalized_center()
        # Invert Y-axis since PIL uses top-bottom coordinate
        normalized_photo_center.y = 1.0 - normalized_photo_center.y
        image_size = Vector2.from_array(image.size)
        center = Vector2.multiply_components(normalized_photo_center, image_size)

        rect_minus_borders = photo.rect_minus_borders
        rect_half_size = Vector2.divided_by(rect_minus_borders.get_size(), 2.0)

        left = int(center.x - rect_half_size.x)
        right = int(left + rect_minus_borders.w)
        up = int(center.y - rect_half_size.y)
        down = int(up + rect_minus_borders.h)
        return left, up, right, down

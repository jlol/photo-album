from typing import Tuple
import PIL
from PIL import Image

from src.layout_creation.layout import Layout
from src.layout_creation.node_data import NodeData
from src.layout_creation.rect import Rect
from src.utils import ImageUtils
from src.utils.MathUtils import Vector2


class LayoutRenderer:

    def __init__(self, layout: Layout, size, image_provider):
        self.size = size
        self.layout = layout
        self.__image_provider = image_provider

    def render(self) -> Image:
        nodes = self.layout.get_leaf_nodes()
        result = Image.new(mode="RGB", size=self.size,
                           color=self.layout.border_color)

        for n in nodes:
            data = n.data
            path = data.image
            tmp_image = self.__image_provider.get_image(path)

            final_rect = data.get_rect_after_borders_applied(self.layout.border)
            new_size = (int(final_rect.w), int(final_rect.h))
            scale = self._scale_size(tmp_image.size, new_size)
            tmp_image = tmp_image.resize(scale, PIL.Image.LANCZOS)

            crop_width = new_size[0]
            crop_height = new_size[1]
            crop = (0, 0, crop_width, crop_height)
            tmp_image = tmp_image.crop(crop)

            paste_position = (int(final_rect.x), int(final_rect.y))
            result.paste(tmp_image, paste_position)

        return result

    def _scale_size(self, original_size, new_size) -> Tuple[int, int]:
        new_size_floats = ImageUtils.scale_size_respecting_ratio(Vector2.from_array(original_size),
                                                                 Vector2.from_array(new_size))
        return int(new_size_floats[0]), int(new_size_floats[1])

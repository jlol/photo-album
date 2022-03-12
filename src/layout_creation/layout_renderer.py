from typing import Tuple
import PIL
from PIL import Image

from src.layout_creation.layout import Layout
from src.layout_creation.node_data import NodeData
from src.layout_creation.rect import Rect


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

            final_rect = self.__apply_border_to_rect(data)
            new_size = (int(final_rect.w), int(final_rect.h))
            scale = self.scale_size(new_size, tmp_image.size)
            tmp_image = tmp_image.resize(scale, PIL.Image.LANCZOS)

            crop_width = new_size[0]
            crop_height = new_size[1]
            crop = (0, 0, crop_width, crop_height)
            tmp_image = tmp_image.crop(crop)

            paste_position = (int(final_rect.x), int(final_rect.y))
            result.paste(tmp_image, paste_position)

        return result

    def scale_size(self, new_size, original_size) -> Tuple[int, int]:
        original_ratio = original_size[0] / original_size[1]
        new_ratio = new_size[0] / new_size[1]
        scale_x = new_size[0]
        scale_y = new_size[1]

        if new_ratio > original_ratio:
            scale_y = scale_x / original_ratio
        else:
            scale_x = scale_y * original_ratio

        return (int(scale_x), int(scale_y))

    def __apply_border_to_rect(self, data) -> Rect:
        rect = Rect(data.rect.x, data.rect.y, data.rect.w, data.rect.h)
        border = self.layout.border

        if border == 0:
            return rect

        if data.has_neighbour(NodeData.LEFT_NEIGHBOUR):

            if data.has_neighbour(NodeData.RIGHT_NEIGHBOUR):
                rect.w -= border
            else:
                rect.w -= border
        else:
            rect.x += border

            if data.has_neighbour(NodeData.RIGHT_NEIGHBOUR):
                rect.w -= 2.0 * border
            else:
                rect.w -= 2.0 * border

        if data.has_neighbour(NodeData.TOP_NEIGHBOUR):

            if data.has_neighbour(NodeData.BOTTOM_NEIGHBOUR):
                rect.h -= border
            else:
                rect.h -= border
        else:
            rect.y += border

            if data.has_neighbour(NodeData.BOTTOM_NEIGHBOUR):
                rect.h -= 2.0 * border
            else:
                rect.h -= 2.0 * border

        return rect

from PIL import Image
from OpenGL.GL import *

from src.layout_creation.rect import Rect
from src.utils.MathUtils import Vector2


class ImageSceneObject:
    def __init__(self, image: Image, rect: Rect, offset: Vector2):
        width, height = image.size
        self.__size = image.size
        self.__zoom = 1.0
        self.__rect: Rect = rect
        self.__ratio: float = float(self.__rect.w) / float(self.__rect.h)

        # Set default values for UV
        self.__uv_center = Vector2(0.5, 0.5) + offset
        self.__maximum_uv_size = Vector2(1.0, 1.0)
        self.__uv_bottom_left = Vector2(0, 0)
        self.__uv_top_right = Vector2(1.0, 1.0)

        # Dirty hack for portrait textures, they seem to work with
        # POT width, otherwise texture looks bad
        if width < height or width % 2 != 0:
            new_height = height * (2048.0 / width)
            image = image.resize((2048, int(new_height)))
            width, height = image.size
            self.__size = image.size

        self.img_data = image.tobytes("raw", "RGB", 0, -1)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.img_data)
        self.__texture = texture

        self.set_rect(rect)

    def set_rect(self, rect: Rect):
        self.__zoom = 1.0
        self.__rect = rect
        self._adjust_uv_size_to_ratio(rect)
        self.__uv_bottom_left, self.__uv_top_right = self._calculate_uv_corners(self.__uv_center, self.__maximum_uv_size)

    def _adjust_uv_size_to_ratio(self, rect):
        width_ratio = self.__size[0] / float(rect.w)
        height_ratio = self.__size[1] / float(rect.h)
        uv_size = Vector2(1.0, 1.0)
        default_uv_center = Vector2(0.5, 0.5)

        if width_ratio > height_ratio:
            uv_size.x = height_ratio / width_ratio
            default_uv_center.x = uv_size.x / 2.0
        else:
            uv_size.y = width_ratio / height_ratio
            default_uv_center.y = uv_size.y / 2.0

        self.__maximum_uv_size = uv_size
        self.__uv_center = default_uv_center

    def _calculate_uv_corners(self, center: Vector2, uv_size: Vector2) -> (Vector2, Vector2):
        half_uv_size = Vector2.divided_by(uv_size, 2.0)
        return center - half_uv_size, center + half_uv_size

    def _get_uv_size_after_zoom(self, zoom) -> Vector2:
        return Vector2.divided_by(self.__maximum_uv_size, zoom)

    def _get_half_uv_size_after_zoom(self) -> Vector2:
        return Vector2.divided_by(self._get_uv_size_after_zoom(self.__zoom), 2.0)

    def get_rect(self) -> Rect:
        return Rect.clone(self.__rect)

    '''Returns an offset based on the minimum value for uv center'''
    def get_uv_offset(self) -> Vector2:
        return self.__uv_center - self._get_half_uv_size_after_zoom()

    def reset_uv_offset(self):
        self.__uv_center = Vector2.divided_by(self.__maximum_uv_size, 2.0)

    def add_uv_offset(self, delta: Vector2):
        new_center = self.__uv_center + delta
        uv_size_after_zoom = self._get_uv_size_after_zoom(self.__zoom)
        bottom_left, top_right = self._calculate_uv_corners(new_center, uv_size_after_zoom)

        if delta.x > 0.0 and top_right.x > 1.0:
            new_center.x -= top_right.x - 1.0
        elif delta.x < 0.0 and bottom_left.x < 0.0:
            new_center.x += -bottom_left.x

        if delta.y > 0.0 and top_right.y > 1.0:
            new_center.y -= top_right.y - 1.0
        elif delta.y < 0.0 and bottom_left.y < 0.0:
            new_center.y += -bottom_left.y

        self.__uv_center = new_center
        self.__uv_bottom_left, self.__uv_top_right = self._calculate_uv_corners(new_center, uv_size_after_zoom)

    def change_zoom(self, delta: float):
        self.__zoom = min(max(self.__zoom + delta, 1.0), 7.0)
        new_uv_size = self._get_uv_size_after_zoom(self.__zoom)
        new_center = self.__uv_center
        bottom_left, top_right = self._calculate_uv_corners(self.__uv_center, new_uv_size)

        if top_right.x > 1.0:
            new_center.x -= top_right.x - 1.0
        elif bottom_left.x < 0.0:
            new_center.x += -bottom_left.x

        if top_right.y > 1.0:
            new_center.y -= top_right.y - 1.0
        elif bottom_left.y < 0.0:
            new_center.y += -bottom_left.y

        self.__uv_center = new_center
        self.__uv_bottom_left, self.__uv_top_right = self._calculate_uv_corners(new_center, new_uv_size)

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.__texture)

        corners = self.__rect.get_corners()

        glBegin(GL_QUADS)
        glTexCoord2f(self.__uv_bottom_left.x, self.__uv_top_right.y)
        glVertex3f(corners[0].x, corners[0].y, 0.0)
        glTexCoord2f(self.__uv_bottom_left.x, self.__uv_bottom_left.y)
        glVertex3f(corners[1].x, corners[1].y, 0.0)
        glTexCoord2f(self.__uv_top_right.x, self.__uv_bottom_left.y)
        glVertex3f(corners[2].x, corners[2].y, 0.0)
        glTexCoord2f(self.__uv_top_right.x, self.__uv_top_right.y)
        glVertex3f(corners[3].x, corners[3].y, 0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def dispose(self):
        glDeleteTextures(1, self.__texture)

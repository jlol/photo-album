from PIL import Image
from OpenGL.GL import *

from src.layout_creation.rect import Rect
from src.utils.MathUtils import Vector2


class ImageSceneObject:
    def __init__(self, image: Image, rect: Rect, offset: Vector2):
        self.__max_uv_size: Vector2 = None
        self.uv_min: Vector2 = None
        self.uv_max: Vector2 = None
        self.__rect: Rect = None
        self.__lock_height_uv = False
        self.uv_offset: Vector2 = Vector2(0.0, 0.0)

        width, height = image.size
        self.__size = image.size
        self.__zoom = 1.0

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

        self._initialize_uv(offset)
        self.set_rect(rect)

    def set_rect(self, rect: Rect):
        self.__rect = rect
        width_ratio = self.__size[0] / rect.w
        height_ratio = self.__size[1] / rect.h
        if width_ratio > height_ratio:
            self.__lock_height_uv = True
            self.uv_max.x = height_ratio / width_ratio
        else:
            self.__lock_height_uv = False
            self.uv_max.y = width_ratio / height_ratio
        self.__max_uv_size = self.uv_max - self.uv_min

    def get_rect(self) -> Rect:
        return self.__rect

    def get_size(self) -> (float, float):
        return self.__size

    def set_size(self, size: (float, float)):
        self.__size = size

    def reset_offset(self):
        self.uv_offset = Vector2(0.0, 0.0)

    def add_uv_offset(self, delta: Vector2):
        if self.__lock_height_uv:
            self.uv_offset.x -= delta.x
        else:
            self.uv_offset.y += delta.y

        resulting_uv_min = self.uv_min + self.uv_offset
        resulting_uv_max = self.uv_max + self.uv_offset

        if resulting_uv_max.x > 1.0:
            diff = resulting_uv_max.x - 1.0
            self.uv_offset.x -= diff
        elif resulting_uv_min.x < 0.0:
            diff = resulting_uv_min.x
            self.uv_offset.x -= diff

        if resulting_uv_max.y > 1.0:
            diff = resulting_uv_max.y - 1.0
            self.uv_offset.y -= diff
        elif resulting_uv_min.y < 0.0:
            diff = resulting_uv_min.y
            self.uv_offset.y -= diff

    # TODO: review the correctness of this method
    # TODO: unlock vertical/horizontal movement of uv when zoomed in
    def change_zoom(self, delta: float):
        self.__zoom = min(max(self.__zoom + delta, 1.0), 7.0)

        self.uv_min = Vector2(0.0, 0.0)
        self.uv_offset = Vector2(0.0, 0.0)
        max_x = self.__max_uv_size.x / self.__zoom
        max_y = self.__max_uv_size.y / self.__zoom

        if max_x > 1.0:
            diff = max_x - 1.0
            relative_correction = diff / self.__max_uv_size.x
            self.__zoom -= delta * relative_correction
            max_x = 1.0
            max_y -= diff

        if max_y > 1.0:
            diff = 1.0 - max_y
            relative_correction = diff / self.__max_uv_size.y
            self.__zoom -= delta * relative_correction
            max_y = 1.0
            max_x -= diff

        self.uv_max = Vector2(max_x, max_y)

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.__texture)

        corners = self.__rect.get_corners()

        uv_min = Vector2(self.uv_min.x, self.uv_min.y)
        uv_max = Vector2(self.uv_max.x, self.uv_max.y)
        uv_min += self.uv_offset
        uv_max += self.uv_offset

        glBegin(GL_QUADS)
        glTexCoord2f(uv_min.x, uv_max.y)
        glVertex3f(corners[0].x, corners[0].y, 0.0)
        glTexCoord2f(uv_min.x, uv_min.y)
        glVertex3f(corners[1].x, corners[1].y, 0.0)
        glTexCoord2f(uv_max.x, uv_min.y)
        glVertex3f(corners[2].x, corners[2].y, 0.0)
        glTexCoord2f(uv_max.x, uv_max.y)
        glVertex3f(corners[3].x, corners[3].y, 0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def dispose(self):
        glDeleteTextures(1, self.__texture)

    def _initialize_uv(self, offset):
        # Initialize UV
        self.uv_min = Vector2(0, 0)
        self.uv_max = Vector2(1, 1)
        self.uv_offset = offset

from PIL import Image
from OpenGL.GL import *

from src.album_project.album import Vector2
from src.layout_creation.rect import Rect


class ImageSceneObject:
    def __init__(self, rect: Rect, image):
        self.rect = rect

        width, height = image.size

        # Dirty hack for portrait textures, they seem to work with
        # POT width, otherwise texture looks bad
        if width < height or width % 2 != 0:
            new_height = height * (2048.0 / width)
            image = image.resize((2048, int(new_height)))
            width, height = image.size

        self.img_data = image.tobytes("raw", "RGB", 0, -1)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.img_data)
        self.texture = texture

        glEnable(GL_TEXTURE_2D)

        self.texture = texture

        # Initialize UV
        self.uv_min = Vector2(0, 0)
        self.uv_max = Vector2(1, 1)
        self._uv_offset = Vector2(0, 0)

        width_ratio = width / rect.w
        height_ratio = height / rect.h

        if width_ratio > height_ratio:
            self._lock_height_uv = True
            self.uv_max.x = height_ratio / width_ratio
        else:
            self._lock_height_uv = False
            self.uv_max.y = width_ratio / height_ratio

    def add_uv_offset(self, delta: Vector2):
        if self._lock_height_uv:
            self._uv_offset.x -= delta.x
        else:
            self._uv_offset.y += delta.y

        resulting_uv_min = self.uv_min + self._uv_offset
        resulting_uv_max = self.uv_max + self._uv_offset

        if resulting_uv_max.x > 1.0:
            diff = resulting_uv_max.x - 1.0
            self._uv_offset.x -= diff
        elif resulting_uv_min.x < 0.0:
            diff = resulting_uv_min.x
            self._uv_offset.x -= diff

        if resulting_uv_max.y > 1.0:
            diff = resulting_uv_max.y - 1.0
            self._uv_offset.y -= diff
        elif resulting_uv_min.y < 0.0:
            diff = resulting_uv_min.y
            self._uv_offset.y -= diff


    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        corners = self.rect.get_corners()

        uv_min = Vector2(self.uv_min.x, self.uv_min.y)
        uv_max = Vector2(self.uv_max.x, self.uv_max.y)
        uv_min += self._uv_offset
        uv_max += self._uv_offset

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
        glDeleteTextures(1, self.texture)

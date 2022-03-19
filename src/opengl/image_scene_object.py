from PIL import Image
from OpenGL.GL import *

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

    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        corners = self.rect.get_corners()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex3f(corners[0].x, corners[0].y, 0.0)
        glTexCoord2f(0, 0)
        glVertex3f(corners[1].x, corners[1].y, 0.0)
        glTexCoord2f(1, 0)
        glVertex3f(corners[2].x, corners[2].y, 0.0)
        glTexCoord2f(1, 1)
        glVertex3f(corners[3].x, corners[3].y, 0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def dispose(self):
        glDeleteTextures(1, self.texture)

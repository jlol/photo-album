import OpenGL.GL as gl
from OpenGL.GLU import *

from src.album_project.album import Vector2

ZNEAR = 0

ZFAR = 1000

CAMERA_MOVEMENT_SPEED = 0.9
ZOOM_SPEED = 0.001


class Camera:
    def __init__(self, bg_color, ortho_size=1024):
        self.camera_offset = [0, 0, 0]
        self.ortho_size = ortho_size
        self.zoom = 1
        self.bg_color = bg_color
        self._widget_size = None

    def initializeGL(self, widget_size):
        gl.glClearColor(self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3])
        gl.glMatrixMode(gl.GL_PROJECTION)
        self._widget_size = widget_size
        self.__set_ortho()

    def resizeGL(self, widget_size):
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_PROJECTION)
        self._widget_size = widget_size
        self.__set_ortho()

    def __set_ortho(self):
        ratio = self.__get_ratio()
        horizontal_ortho_size = self.__get_horizontal_ortho_size()
        gl.glOrtho(-horizontal_ortho_size, horizontal_ortho_size, -self.ortho_size, self.ortho_size, ZNEAR, ZFAR)

    def paintGL(self):
        gl.glTranslate(-self.camera_offset[0], -self.camera_offset[1], 0)
        gl.glScale(self.zoom, self.zoom, 1.0)

    def apply_zoom_delta(self, delta):
        self.zoom += delta * ZOOM_SPEED
        if self.zoom <= 0:
            self.zoom = 0.001

    def apply_movement_delta(self, delta):
        self.camera_offset[0] -= delta.x() * CAMERA_MOVEMENT_SPEED
        self.camera_offset[1] += delta.y() * CAMERA_MOVEMENT_SPEED

    def screen_to_world(self, screen: Vector2) -> Vector2:
        top_left = self.__get_world_top_left()
        screen_to_world_ratio = (2.0 * self.ortho_size) / (self.zoom * self._widget_size.height())
        return Vector2(top_left.x + screen.x * screen_to_world_ratio, top_left.y - screen.y * screen_to_world_ratio)

    def __get_ratio(self):
        if self._widget_size is None:
            print("[Warning] Accessing widget size before setting it")
            return 1.0
        return self._widget_size.width() / self._widget_size.height()

    def __get_world_top_left(self) -> Vector2:
        return Vector2((self.camera_offset[0] - self.__get_horizontal_ortho_size()) / self.zoom,
                       (self.camera_offset[1] + self.ortho_size) / self.zoom)

    def __get_horizontal_ortho_size(self) -> float:
        return self.ortho_size * self.__get_ratio()

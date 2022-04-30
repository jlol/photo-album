from enum import Enum

from OpenGL import GL as gl
from PyQt5.QtCore import QPoint, QSize, Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget

from src.album_project.album import Vector2
from src.layout_creation.image_provider import ImageProvider
from src.layout_creation.rect import Rect
from src.opengl.camera import Camera
from src.opengl.camera_raycast import CameraRaycast
from src.opengl.image_scene_object import ImageSceneObject


class MouseMode(Enum):
    NONE = 0
    OBJECT = 1
    CAMERA_MOVE = 2


class AlbumVisualizer(QOpenGLWidget):

    def __init__(self, image_provider: ImageProvider):
        super().__init__()
        self.is_mouse_down = False
        self.last_mouse_pos = QPoint()
        bg_color = (0.5, 0.8, 0.7, 1.0)
        self.camera = Camera(bg_color)
        self._camera_raycast = CameraRaycast(self.camera)
        self.photos = []
        self.rects = []
        self._image_provider = image_provider
        self._mouse_mode = MouseMode.NONE
        self._selected_object_index = -1

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(50)

    def initializeGL(self):
        self.camera.initializeGL(self.size())

    def resizeGL(self, w, h):
        self.camera.resizeGL(QSize(w, h))

    def add_photo(self, rect: Rect, path):
        self.makeCurrent()
        image = self._image_provider.get_image(path)
        photo = ImageSceneObject(rect, image)
        self.rects.append(rect)
        self.photos.append(photo)

    def cleanup_photos(self):
        self.makeCurrent()
        for p in self.photos:
            p.dispose()

        self.rects = []
        self.photos = []

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()
        self.camera.paintGL()

        gl.glPushMatrix()    # push the current matrix to the current stack

        for photo in self.photos:
            photo.draw()

        gl.glPopMatrix()    # restore the previous modelview matrix
        gl.glPopMatrix()

        gl.glFlush()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.window.close()

    def wheelEvent(self, event):
        self.camera.apply_zoom_delta(event.angleDelta().y())

    def mousePressEvent(self, event):
        self.is_mouse_down = True

        screen_point = Vector2(event.pos().x(), event.pos().y())
        raycast_result = self._camera_raycast.raycast(screen_point, self.rects)
        self.last_mouse_pos = event.pos()

        if raycast_result.is_ok:
            self._mouse_mode = MouseMode.OBJECT
            self._selected_object_index = raycast_result.value
            return

        self._mouse_mode = MouseMode.CAMERA_MOVE

    def mouseReleaseEvent(self, event):
        self.is_mouse_down = False
        self._mouse_mode = MouseMode.NONE

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.last_mouse_pos = event.pos()

        if self._mouse_mode == MouseMode.OBJECT:
            self.__apply_delta_to_photo(self._selected_object_index, Vector2(delta.x(), delta.y()))
            return
        elif self._mouse_mode == MouseMode.CAMERA_MOVE:
            self.camera.apply_movement_delta(delta)

    def __apply_delta_to_photo(self, index: int, delta: Vector2):
        if index >= len(self.photos) or index < 0:
            return

        photo = self.photos[index]
        delta.x *= 0.001
        delta.y *= 0.001
        photo.add_uv_offset(delta)

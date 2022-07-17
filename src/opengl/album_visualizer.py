import copy

from enum import Enum
from OpenGL import GL as gl
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QSize, Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from src.logic.layout_change_listener import LayoutChangeListener
from src.utils.image_cache import ImageCache
from src.layout_creation.rect import Rect
from src.opengl.camera import Camera
from src.opengl.camera_raycast import CameraRaycast, RaycastResult
from src.opengl.image_scene_object import ImageSceneObject
from src.utils.MathUtils import Vector2


class MouseMode(Enum):
    NONE = 0
    OBJECT = 1
    CAMERA_MOVE = 2
    SWAP_MODE = 3


class AlbumVisualizer(QOpenGLWidget):
    # TODO: use an interface for project handler
    def __init__(self, image_provider: ImageCache, layout_change_listener: LayoutChangeListener):
        super().__init__()
        self.is_mouse_down = False
        self.last_mouse_pos = QPoint()
        bg_color = (0.5, 0.8, 0.7, 1.0)
        self.camera = Camera(bg_color)
        self._camera_raycast = CameraRaycast(self.camera)
        self.photos: [ImageSceneObject] = []
        self.rects: [Rect] = []
        self._image_provider = image_provider
        self._mouse_mode = MouseMode.NONE
        self._selected_object_index = -1
        self._swap_index_a = -1
        self._layout_change_listener = layout_change_listener

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(50)

    def initializeGL(self):
        self.camera.initializeGL(self.size())

    def resizeGL(self, w, h):
        self.camera.resizeGL(QSize(w, h))

    def add_photo(self, path: str, rect: Rect, offset: Vector2):
        self.makeCurrent()
        image = self._image_provider.get_image(path)
        photo = ImageSceneObject(image, rect, copy.copy(offset))
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
        raycast_result = self._raycast_rects(event.pos())
        scroll_delta = event.angleDelta().y()

        if raycast_result.is_ok:
            self._apply_zoom(raycast_result.value, scroll_delta)
            return

        self.camera.apply_zoom_delta(scroll_delta)

    def mousePressEvent(self, event):
        self.is_mouse_down = True
        raycast_result = self._raycast_rects(event.pos())
        self.last_mouse_pos = event.pos()

        if not raycast_result.is_ok:
            self._mouse_mode = MouseMode.CAMERA_MOVE
            return

        self._selected_object_index = raycast_result.value

        if event.buttons() == Qt.RightButton:
            self._mouse_mode = MouseMode.SWAP_MODE
            self._handle_swap_release_event()
        elif event.buttons() == Qt.LeftButton:
            self._mouse_mode = MouseMode.OBJECT

    def mouseReleaseEvent(self, event):
        self.is_mouse_down = False
        self._mouse_mode = MouseMode.NONE
        self._selected_object_index = -1

    def _handle_swap_release_event(self):
        if self._swap_index_a == -1:
            self._swap_index_a = self._selected_object_index
            return

        swap_index_b = self._selected_object_index
        self._swap_photos(self._swap_index_a, swap_index_b)
        self._swap_index_a = -1

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.last_mouse_pos = event.pos()

        if event.buttons() == Qt.MiddleButton:
            self.camera.apply_movement_delta(delta)
        elif self._mouse_mode == MouseMode.OBJECT:
            self._apply_delta_to_photo(self._selected_object_index, Vector2(delta.x(), delta.y()))

    def _apply_delta_to_photo(self, index: int, delta: Vector2):
        if index >= len(self.photos) or index < 0:
            return

        photo = self.photos[index]
        delta.x *= 0.001
        delta.y *= 0.001
        photo.add_uv_offset(delta)
        self._layout_change_listener.image_offset_applied(index, photo.uv_offset)

    def _apply_zoom(self, index: int, delta: float):
        photo = self.photos[index]
        delta *= 0.0005
        photo.change_zoom(delta)
        # TODO: send an image_rect_update instead of image_zoom_applied
        self._layout_change_listener.image_zoom_applied(index, delta)

    def _swap_photos(self, a: int, b: int):
        photo_a = self.photos[a]
        rect_a = photo_a.get_rect()
        size_a = photo_a.get_size()
        photo_b = self.photos[b]
        rect_b = photo_b.get_rect()
        size_b = photo_b.get_size()

        photo_a.set_size(size_b)
        photo_b.set_size(size_a)
        photo_a.set_rect(rect_b)
        photo_b.set_rect(rect_a)
        self.photos[a] = photo_b
        self.photos[b] = photo_a

        self._layout_change_listener.image_swap(a, b)

    def _raycast_rects(self, mouse_position: QtCore.QPoint) -> RaycastResult:
        screen_point = Vector2(mouse_position.x(), mouse_position.y())
        return self._camera_raycast.raycast(screen_point, self.rects)

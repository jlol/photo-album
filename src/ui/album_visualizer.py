from OpenGL import GL as gl
from PyQt5.QtCore import QPoint, QSize, Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget

from src.layout_creation.image_provider import ImageProvider
from src.layout_creation.rect import Rect
from src.opengl.camera import Camera
from src.opengl.image_scene_object import ImageSceneObject


class AlbumVisualizer(QOpenGLWidget):
    def __init__(self, image_provider: ImageProvider):
        super().__init__()
        self.is_mouse_down = False
        self.last_mouse_pos = QPoint()
        bg_color = (0.5, 0.8, 0.7, 1.0)
        self.camera = Camera(bg_color)
        self.photos = []
        self._image_provider = image_provider

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
        self.photos.append(photo)

    def cleanup_photos(self):
        self.makeCurrent()
        for p in self.photos:
            p.dispose()

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
        self.camera.applyZoomDelta(event.angleDelta().y())

    def mousePressEvent(self, event):
        self.is_mouse_down = True
        self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.is_mouse_down = False

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.last_mouse_pos = event.pos()
        self.camera.applyMovementDelta(delta)
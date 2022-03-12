import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import OpenGL.GL as gl

from src.layout_creation.rect import Rect
from src.opengl.camera import Camera
from src.opengl.image_scene_object import ImageSceneObject


class AlbumVisualizer(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.is_mouse_down = False
        self.last_mouse_pos = QPoint()
        bg_color = (0.5, 0.8, 0.7, 1.0)
        self.camera = Camera(bg_color)
        self.photos = []

    def initializeGL(self):
        self.camera.initializeGL(self.size())

    def set_zoom(self, zoom):
        self.zoom = zoom

    def resizeGL(self, w, h):
        self.camera.resizeGL(QSize(w, h))

    def add_photo(self, rect: Rect, path):
        self.makeCurrent()
        photo = ImageSceneObject(rect, path)
        self.photos.append(photo)

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
        elif event.key() == Qt.Key_A and len(self.photos) == 0:
            test_img = "/home/woody/perfil.png"
            self.add_photo(Rect(0, 0, 2000, 1000), test_img)

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


def show_window():
    app = QApplication(sys.argv)
    #window = mainWindow()
    #window.setupUI()
    #window.show()
    album_visualizer = AlbumVisualizer()
    album_visualizer.resize(1024, 1024)
    album_visualizer.show()
    timer = QTimer(album_visualizer)
    timer.timeout.connect(album_visualizer.update)
    timer.start(50)
    sys.exit(app.exec_())
    return album_visualizer
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

import OpenGL.GL as gl        # python wrapping of OpenGL
from OpenGL.GLU import * # OpenGL Utility Library, extends OpenGL functionality

from OpenGL.arrays import vbo
import numpy as np


class AlbumVisualizer(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.is_mouse_down = False
        self.last_mouse_pos = QPoint()
        self.is_initialized = False
        self.zoom = 1
        self.camera_position = [0, 0, 0]
        self.ortho_size = 4
        self.vao = QOpenGLVertexArrayObject(self)

    def initializeGL(self):
        gl.glClearColor(0.5, 0.8, 0.7, 1.0)
        size = self.size()
        ratio = size.width() / size.height()
        gluOrtho2D(-self.ortho_size, self.ortho_size, -self.ortho_size, self.ortho_size)

    def set_zoom(self, zoom):
        self.zoom = zoom

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)

    def add_photo(self):
        self.makeCurrent()
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4])

        self.is_initialized = True

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        if not self.is_initialized:
            return

        gl.glPushMatrix()
        gl.glTranslate(self.camera_position[0], self.camera_position[1], 0)
        gl.glScale(self.zoom, self.zoom, 1.0)

        gl.glPushMatrix()    # push the current matrix to the current stack
        #
        # gl.glTranslate(0.0, 0.0, -50.0)    # third, translate cube to specified depth
        # gl.glScale(20.0, 20.0, 20.0)       # second, scale cube
        # gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        # gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        # gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        # gl.glTranslate(-0.5, -0.5, -0.5)   # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()    # restore the previous modelview matrix

        gl.glPopMatrix()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            if not self.is_initialized:
                self.add_photo()
        elif event.key() == Qt.Key_Q:
            self.window.close()
        elif event.key() == Qt.Key_A:
            self.set_zoom(self.zoom)

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.002
        if self.zoom <= 0:
            self.zoom = 1
        self.set_zoom(self.zoom)

    def mousePressEvent(self, event):
        self.is_mouse_down = True
        self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        self.is_mouse_down = False

    def mouseMoveEvent(self, event):
        delta = event.pos() - self.last_mouse_pos
        self.camera_position[0] += delta.x() * 0.005
        self.camera_position[1] -= delta.y() * 0.005
        self.last_mouse_pos = event.pos()


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
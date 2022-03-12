import OpenGL.GL as gl
from OpenGL.GLU import *

CAMERA_MOVEMENT_SPEED = 0.9
ZOOM_SPEED = 0.001


class Camera:
    def __init__(self, bg_color, ortho_size=1024):
        self.camera_position = [0, 0, 0]
        self.ortho_size = ortho_size
        self.zoom = 1
        self.bg_color = bg_color

    def initializeGL(self, widget_size):
        gl.glClearColor(self.bg_color[0], self.bg_color[1], self.bg_color[2], self.bg_color[3])
        ratio = widget_size.width() / widget_size.height()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gluOrtho2D(-self.ortho_size * ratio, self.ortho_size, -self.ortho_size * ratio, self.ortho_size)

    def resizeGL(self, widget_size):
        ratio = widget_size.width() / widget_size.height()
        gl.glLoadIdentity();
        gl.glMatrixMode(gl.GL_PROJECTION)
        gluOrtho2D(-self.ortho_size * ratio, self.ortho_size * ratio, -self.ortho_size, self.ortho_size)

    def paintGL(self):
        gl.glTranslate(self.camera_position[0], self.camera_position[1], 0)
        gl.glScale(self.zoom, self.zoom, 1.0)

    def applyZoomDelta(self, delta):
        self.zoom += delta * ZOOM_SPEED
        if self.zoom <= 0:
            self.zoom = 0.001

    def applyMovementDelta(self, delta):
        self.camera_position[0] += delta.x() * CAMERA_MOVEMENT_SPEED
        self.camera_position[1] -= delta.y() * CAMERA_MOVEMENT_SPEED
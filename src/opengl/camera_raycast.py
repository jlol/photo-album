from src.layout_creation.rect import Rect
from src.opengl.camera import Camera
from src.utils.MathUtils import Vector2


class RaycastResult:
    def __init__(self, is_ok: bool, value: int=-1):
        self.is_ok = is_ok
        self.value = value


def contains_point(world_point: Vector2, rect: Rect) -> bool:
    rect_max = rect.max()
    rect_min = rect.min()

    if world_point.x < rect_min.x or world_point.x > rect_max.x:
        return False
    if world_point.y < rect_min.y or world_point.y > rect_max.y:
        return False

    return True


class CameraRaycast:

    def __init__(self, camera: Camera):
        self._camera = camera

    def raycast(self, screen_point: Vector2,  rects: [Rect]) -> RaycastResult:

        if len(rects) == 0:
            return RaycastResult(False)

        world_point = self._camera.screen_to_world(screen_point)
        index = 0

        for r in rects:
            if contains_point(world_point, r):
                return RaycastResult(True, index)
            index = index + 1

        return RaycastResult(False)

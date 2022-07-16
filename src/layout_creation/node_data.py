from enum import Enum

from src.layout_creation.rect import Rect


class SplitType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    LEAF = 2


class NodeData:

    LEFT_NEIGHBOUR = 0b00000001
    TOP_NEIGHBOUR = 0b00000010
    RIGHT_NEIGHBOUR = 0b00000100
    BOTTOM_NEIGHBOUR = 0b00001000

    def __init__(self, r: Rect):
        self.rect = r
        self.split = SplitType.LEAF
        # Image path
        self.image = ""
        self.__neighbours_mask = 0

    def __str__(self):
        return str(self.split)

    def has_neighbour(self, location) -> bool:
        return bool(self.__neighbours_mask & location)

    def set_neighbour(self, neighbour, state: bool):
        if state:
            self.__neighbours_mask |= neighbour
            return

        if self.has_neighbour(neighbour):
            self.__neighbours_mask ^= neighbour

    def copy_neighbours_mask(self, other_node):
        self.__neighbours_mask = other_node.__neighbours_mask

    def get_mask(self) -> int:
        return self.__neighbours_mask

    def get_rect_after_borders_applied(self, border: float) -> Rect:
        rect = Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)

        if border == 0.0:
            return rect

        if self.has_neighbour(NodeData.LEFT_NEIGHBOUR):

            if self.has_neighbour(NodeData.RIGHT_NEIGHBOUR):
                rect.w -= border
            else:
                rect.w -= border
        else:
            rect.x += border

            if self.has_neighbour(NodeData.RIGHT_NEIGHBOUR):
                rect.w -= 2.0 * border
            else:
                rect.w -= 2.0 * border

        if self.has_neighbour(NodeData.TOP_NEIGHBOUR):

            if self.has_neighbour(NodeData.BOTTOM_NEIGHBOUR):
                rect.h -= border
            else:
                rect.h -= border
        else:
            rect.y += border

            if self.has_neighbour(NodeData.BOTTOM_NEIGHBOUR):
                rect.h -= 2.0 * border
            else:
                rect.h -= 2.0 * border

        return rect

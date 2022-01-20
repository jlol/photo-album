from enum import Enum
from rect import Rect
from typing import Final


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

from abc import ABC, abstractmethod
from src.utils.MathUtils import Vector2


class LayoutChangeListener(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def image_normalized_center_changed(self, index: int, normalized_center: Vector2):
        pass

    @abstractmethod
    def image_zoom_applied(self, index: int, zoom: float):
        pass

    @abstractmethod
    def image_swap(self, image_index_a: int, image_index_b: int):
        pass

from typing import Tuple
from src.utils.MathUtils import Vector2


def scale_size_respecting_ratio(self, original_size: Vector2, new_size: Vector2) -> Tuple[float, float]:
    assert(original_size.y != 0)
    assert(new_size.y != 0)

    original_ratio = original_size.x / original_size.y
    assert(original_ratio.y != 0)

    new_ratio = new_size.x / new_size.y
    scale_x = new_size.x
    scale_y = new_size.y

    if new_ratio > original_ratio:
        scale_y = scale_x / original_ratio
    else:
        scale_x = scale_y * original_ratio

    return scale_x, scale_y

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Rect:

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        output = "{0},{1},{2},{3}"
        return output.format(self.x, self.y, self.w, self.h)

    def get_ratio(self) -> float:
        return self.w / self.h

    def get_corners(self):
        return [
            Point(self.x, self.y + self.h),
            Point(self.x, self.y),
            Point(self.x + self.w, self.y),
            Point(self.x + self.w, self.y + self.h)
        ]

    def max(self):
        return Point(self.x + self.w, self.y + self.h)

    def min(self):
        return Point(self.x, self.y)

    @classmethod
    def clone(cls, other_rect):
        return cls(other_rect.x, other_rect.y, other_rect.w, other_rect.h)

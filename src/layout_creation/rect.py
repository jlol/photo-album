
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

    # Returns a 4-tuple with left, upper, right, lower
    def as_pil_paste_box(self) -> (int, int, int, int):
        # TODO: some encapsulation needed to certify that components are always int
        return int(self.x), int(self.y), self.x + int(self.w), self.y + int(self.h)

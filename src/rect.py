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

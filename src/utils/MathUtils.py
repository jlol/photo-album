class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    @classmethod
    def from_array(cls, source_array: [float]):
        return cls(source_array[0], source_array[1])

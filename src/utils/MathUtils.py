class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def clone(self):
        return Vector2(self.x, self.y)

    @classmethod
    def from_array(cls, source_array: [float]):
        return cls(source_array[0], source_array[1])

    @classmethod
    def divided_by(cls, vector, factor: float):
        return cls(vector.x / factor, vector.y / factor)

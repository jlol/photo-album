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

    @classmethod
    def multiply_by(cls, vector, multiplier: float):
        return cls(vector.x * multiplier, vector.y * multiplier)

    @classmethod
    def multiply_components(cls, vector1, vector2):
        return cls(vector1.x * vector2.x, vector1.y * vector2.y)
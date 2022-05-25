class Vec2:
    """Representa um vetor bidimensional."""

    def __init__(self, x: int, y: int, /) -> None:
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

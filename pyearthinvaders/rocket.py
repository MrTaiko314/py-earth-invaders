from pyearthinvaders.entity import Entity
from pyearthinvaders.vec2 import Vec2


class Rocket(Entity):
    """Representa um foguete invasor."""

    def __init__(
            self, position: Vec2, width: int, height: int, speed: Vec2,
            column: int, row: int) -> None:
        super().__init__(position, width, height, speed)
        self.column = column
        self.row = row

    def __str__(self) -> str:
        return (
            f'Rocket(pos={self.position}, w={self.width}, h={self.height}, '
            f'speed={self.speed}, column={self.column}, row={self.row})'
        )

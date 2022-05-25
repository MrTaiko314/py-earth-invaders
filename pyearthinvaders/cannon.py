from pyearthinvaders.entity import Entity
from pyearthinvaders.vec2 import Vec2


class Cannon(Entity):
    """Representa o canhão que o jogador controla."""

    def __init__(
            self, position: Vec2, width: int, height: int, speed: Vec2) -> None:
        super().__init__(position, width, height, speed)

    def __str__(self) -> str:
        return (
            f'Cannon(pos={self.position}, '
            f'w={self.width}, h={self.height}, speed={self.speed})'
        )

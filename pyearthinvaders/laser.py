from pyearthinvaders.entity import Entity
from pyearthinvaders.vec2 import Vec2


class Laser(Entity):
    """Representa um laser disparado pelo canhão."""

    def __init__(
            self, position: Vec2, width: int, height: int, speed: Vec2) -> None:
        super().__init__(position, width, height, speed)

    def __str__(self) -> str:
        return (
            f'Laser(pos={self.position}, w={self.width}, h={self.height}) '
            f'speed={self.speed}'
        )

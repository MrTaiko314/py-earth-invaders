from __future__ import annotations

from pyearthinvaders.vec2 import Vec2


class Entity:
    """Representa uma entidade do jogo, com posição, tamanho e velocidade."""

    def __init__(self, position: Vec2, width: int, height: int, speed: Vec2) -> None:
        """\
        :param position: posição do canto superior direito da entidade.
        """
        self.position = position
        self.width = width
        self.height = height
        self.speed = speed

    @property
    def left(self) -> int:
        return self.position.x

    @property
    def right(self) -> int:
        return self.position.x + self.width

    @property
    def top(self) -> int:
        return self.position.y

    @property
    def bottom(self) -> int:
        return self.position.y + self.height

    def update(self, delta: float) -> None:
        """Atualiza a posição atual de acordo com a velocidade e o
        tempo passado desde a última chamada.
        """

        self.position.x += int(delta * self.speed.x)
        self.position.y += int(delta * self.speed.y)

    def overlaps(self, other: Entity) -> bool:
        """Determina se esta entidade e `other` se sobrepõem."""
        return (
            (self.right >= other.left and other.right >= self.left)
            and (self.bottom >= other.top and other.bottom >= self.top)
        )

    def __str__(self) -> str:
        return (
            f'Entity(pos={self.position}, w={self.width}, h={self.height}) '
            f'speed={self.speed}'
        )

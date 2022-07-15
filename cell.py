from dataclasses import dataclass, field
import pygame as pg
from typing import ClassVar


@dataclass(order=True)
class Cell:
    screen: pg.Surface = field(repr=False)
    col: int = field()
    row: int = field()

    rect: pg.Rect = field(repr=False)

    possibilities: list[int] = field(default_factory=lambda: [1, 2, 3, 4, 5, 6, 7, 8, 9], init=False)

    large_tiles: ClassVar[dict[int, pg.Surface]] = field(init=False, repr=False)
    small_tiles: ClassVar[dict[int, pg.Surface]] = field(init=False, repr=False)

    margin: ClassVar[int] = field(init=False, default=5)
    _value: int = field(init=False, default=None, repr=False)
    sort_index: int = field(init=False, repr=False)

    def __post_init__(self):
        self.sort_index = self.entropy

    @property
    def entropy(self):
        return len(self.possibilities)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.possibilities = [self.value]

    def remove_possibility(self, value: int):
        try:
            self.possibilities.remove(value)
        except ValueError:
            pass

    def draw_possibilities(self):

        for row in range(3):
            # Draw left column i.e. 1, 4, 7
            value = 1 + row*3
            if value in self.possibilities:
                tile = self.small_tiles[value]
                tile_rect: pg.Rect = tile.get_rect()
                tile_rect.left = self.rect.left + self.margin
                tile_rect.top = self.rect.top + row*self.rect.height/3
                self.screen.blit(tile, tile_rect)

            # Draw middle column i.e. 2, 5, 8
            value = 2 + row * 3
            if value in self.possibilities:
                tile = self.small_tiles[value]
                tile_rect: pg.Rect = tile.get_rect()
                tile_rect.center = self.rect.center
                tile_rect.top = self.rect.top + row*self.rect.height/3
                self.screen.blit(tile, tile_rect)

            # Draw right column i.e. 3, 6, 9
            value = 3 + row * 3
            if value in self.possibilities:
                tile = self.small_tiles[value]
                tile_rect: pg.Rect = tile.get_rect()
                tile_rect.right = self.rect.right - self.margin
                tile_rect.top = self.rect.top + row * self.rect.height / 3
                self.screen.blit(tile, tile_rect)

    def draw(self):
        if self.value is None:
            # self.draw_possibilities()
            pass
        else:
            tile = self.large_tiles[self.value]
            tile_rect: pg.Rect = tile.get_rect()
            tile_rect.center = self.rect.center
            self.screen.blit(tile, tile_rect)

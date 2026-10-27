"""
Data models and layout definitions for MonaGEN.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class AspectRatio(str, Enum):
    SQUARE_1X1 = "1x1"
    LANDSCAPE_16X9 = "16x9"

    @property
    def dimensions(self) -> tuple[int, int]:
        if self == AspectRatio.SQUARE_1X1:
            return (1080, 1080)
        elif self == AspectRatio.LANDSCAPE_16X9:
            return (1920, 1080)
        raise ValueError(f"Unknown aspect ratio: {self}")


class SpritePosition(str, Enum):
    BOTTOM_RIGHT = "bottom_right"
    BOTTOM_LEFT = "bottom_left"
    CENTER = "center"
    DIALOG_LEFT = "dialog_left"


@dataclass
class BrandPalette:
    abyssal_void: tuple[int, int, int] = (21, 28, 55)       # #151C37
    deep_space: tuple[int, int, int] = (39, 51, 87)         # #273357
    velvet_rose: tuple[int, int, int] = (192, 94, 110)      # #C05E6E
    arcade_gold: tuple[int, int, int] = (234, 153, 90)      # #EA995A
    synthwave_violet: tuple[int, int, int] = (93, 75, 133)  # #5D4B85
    cyber_blue: tuple[int, int, int] = (49, 111, 160)       # #316FA0
    terminal_sage: tuple[int, int, int] = (121, 147, 134)   # #799386
    twilight_slate: tuple[int, int, int] = (89, 92, 127)    # #595C7F
    dark_slate: tuple[int, int, int] = (37, 41, 57)         # #252939
    parchment: tuple[int, int, int] = (239, 223, 210)       # #EFDFD2
    white: tuple[int, int, int] = (255, 255, 255)


@dataclass
class PostConfig:
    """Configuration to generate a social media post with MonaGEN."""
    title: str
    text: str
    ratio: AspectRatio | str = AspectRatio.SQUARE_1X1
    badge: str | None = None
    sprite: str | Path = "idle"
    sprite_position: SpritePosition | str = SpritePosition.BOTTOM_RIGHT
    sprite_scale: float = 2.6
    with_shadow: bool = True
    background: str | Path = "cosmic_galaxy"
    hud_score: str = "SCORE 99990"
    hud_stage: str = "STAGE 01"
    hud_lives: int = 3
    footer: str = "@cosmic_security  |  selene.io"
    palette: BrandPalette = field(default_factory=BrandPalette)

    def __post_init__(self):
        if isinstance(self.ratio, str):
            self.ratio = AspectRatio(self.ratio)
        if isinstance(self.sprite_position, str):
            self.sprite_position = SpritePosition(self.sprite_position)

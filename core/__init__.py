"""
MonaGEN Core Package.
A high-resolution 1080p social media graphic generator combining
Theatrical Stagecraft aesthetics with 16-bit 2.5D retrogame sprites.
"""

from .models import AspectRatio, SpritePosition, BrandPalette, PostConfig
from .renderer import render_post, resolve_background, resolve_sprite, get_font

__all__ = [
    "AspectRatio",
    "SpritePosition",
    "BrandPalette",
    "PostConfig",
    "render_post",
    "resolve_background",
    "resolve_sprite",
    "get_font",
]

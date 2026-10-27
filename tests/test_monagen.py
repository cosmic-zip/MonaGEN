"""
Unit tests for MonaGEN Core and CLI.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add root directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core.models import PostConfig, AspectRatio, SpritePosition
from core.renderer import render_post, resolve_background, resolve_sprite
from cli import build_parser, args_to_config


def test_models_default():
    cfg = PostConfig(title="Test", text="Hello world")
    assert cfg.ratio == AspectRatio.SQUARE_1X1
    assert cfg.ratio.dimensions == (1080, 1080)
    assert cfg.sprite_position == SpritePosition.BOTTOM_RIGHT


def test_models_16x9():
    cfg = PostConfig(title="Test", text="Hello world", ratio="16x9")
    assert cfg.ratio == AspectRatio.LANDSCAPE_16X9
    assert cfg.ratio.dimensions == (1920, 1080)


def test_sprite_resolution():
    sprite = resolve_sprite("cheer")
    assert sprite is not None
    assert sprite.width > 0 and sprite.height > 0


def test_background_resolution():
    bg_1x1 = resolve_background("cosmic_galaxy", AspectRatio.SQUARE_1X1)
    assert bg_1x1.size == (1080, 1080)

    bg_16x9 = resolve_background("cosmic_galaxy", AspectRatio.LANDSCAPE_16X9)
    assert bg_16x9.size == (1920, 1080)


def test_render_square():
    cfg = PostConfig(
        title="POST TESTE 1X1",
        text="Corpo do teste unitario",
        badge="UNIT TEST",
        sprite="idle",
        ratio=AspectRatio.SQUARE_1X1,
    )
    img = render_post(cfg)
    assert img.size == (1080, 1080)


def test_render_landscape():
    cfg = PostConfig(
        title="POST TESTE 16X9",
        text="Corpo do teste unitario 16x9",
        badge="UNIT TEST",
        sprite="magic",
        ratio=AspectRatio.LANDSCAPE_16X9,
    )
    img = render_post(cfg)
    assert img.size == (1920, 1080)


def test_cli_parser():
    parser = build_parser()
    args = parser.parse_args(["--ratio", "16x9", "--title", "CLI Test", "--sprite", "walk_front"])
    cfg = args_to_config(args)
    assert cfg.ratio == AspectRatio.LANDSCAPE_16X9
    assert cfg.title == "CLI Test"
    assert cfg.sprite == "walk_front"


if __name__ == "__main__":
    print("Running MonaGEN test suite...")
    test_models_default()
    test_models_16x9()
    test_sprite_resolution()
    test_background_resolution()
    test_render_square()
    test_render_landscape()
    test_cli_parser()
    print("All tests passed successfully!")

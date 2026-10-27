"""
CLI Module for MonaGEN.
Isolated command-line interface that translates CLI flags into PostConfig
and renders posts through the core engine.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from core.models import PostConfig, AspectRatio, SpritePosition
from core.renderer import render_post


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser for MonaGEN CLI."""
    parser = argparse.ArgumentParser(
        prog="monagen",
        description="MonaGEN: 1080p Social Media Graphic Generator (1x1 and 16x9) using 2.5D Foxxo Witch Sprites.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--ratio",
        "-r",
        choices=["1x1", "16x9"],
        default="1x1",
        help="Aspect ratio (1x1 = 1080x1080, 16x9 = 1920x1080).",
    )
    parser.add_argument(
        "--title",
        "-t",
        type=str,
        default="ALERTA DE SEGURANCA",
        help="Primary headline / title for the post card.",
    )
    parser.add_argument(
        "--text",
        "-m",
        type=str,
        default="A sentinela Foxxo Witch inspecionou as portas do castelo digital e todos os escudos magicos estao ativos!",
        help="Body text or dialogue content.",
    )
    parser.add_argument(
        "--badge",
        "-b",
        type=str,
        default="BUG HUNTING",
        help="Category badge text (e.g. BUG HUNTING, DICA DEV, NOVO MODULO).",
    )
    parser.add_argument(
        "--sprite",
        "-s",
        type=str,
        default="cheer",
        help="Foxxo Witch sprite pose alias (idle, cheer, magic, walk_front, dash, etc.) or path to PNG.",
    )
    parser.add_argument(
        "--position",
        "-p",
        choices=["bottom_right", "bottom_left", "center"],
        default="bottom_right",
        help="Position of sprite on the 2.5D floor.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2.6,
        help="Pixel art scale factor for the sprite (nearest-neighbor).",
    )
    parser.add_argument(
        "--background",
        "-bg",
        type=str,
        default="cosmic_galaxy",
        help="Background preset (cosmic_galaxy, pure_galaxy, cosmic_theatre) or custom image file path.",
    )
    parser.add_argument(
        "--score",
        type=str,
        default="SCORE 99990",
        help="Arcade HUD score banner on the top left.",
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="STAGE 01",
        help="Arcade HUD stage indicator on the top right.",
    )
    parser.add_argument(
        "--lives",
        type=int,
        default=3,
        help="Number of life hearts in the HUD.",
    )
    parser.add_argument(
        "--footer",
        "-f",
        type=str,
        default="@cosmic_security  |  selene.io",
        help="Footer or social handle text.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output_post.png",
        help="Destination path for generated PNG image.",
    )

    return parser


def args_to_config(args: argparse.Namespace) -> PostConfig:
    """Converts parsed command line arguments into a core PostConfig object."""
    sprite = args.sprite.strip() if (args.sprite and args.sprite.strip()) else "cheer"
    background = args.background.strip() if (args.background and args.background.strip()) else "cosmic_galaxy"
    badge = args.badge.strip() if (args.badge and args.badge.strip()) else None

    return PostConfig(
        title=args.title,
        text=args.text,
        ratio=AspectRatio(args.ratio),
        badge=badge,
        sprite=sprite,
        sprite_position=SpritePosition(args.position),
        sprite_scale=args.scale,
        background=background,
        hud_score=args.score,
        hud_stage=args.stage,
        hud_lives=args.lives,
        footer=args.footer,
    )


def run_cli(argv: list[str] | None = None) -> int:
    """
    Executes the CLI workflow: parses arguments, calls the rendering engine,
    and writes the resulting PNG to disk.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = args_to_config(args)
        print(f"[MonaGEN] Rendering post ({args.ratio} - {config.ratio.dimensions[0]}x{config.ratio.dimensions[1]})...")
        image = render_post(config)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")
        print(f"[MonaGEN] Generated successfully: {output_path.resolve()}")
        return 0
    except Exception as e:
        print(f"[MonaGEN Error] Failed to generate post: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run_cli())

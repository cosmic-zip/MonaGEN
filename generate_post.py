"""
Main Entry Point for MonaGEN.
Can be executed as a CLI script or imported into external pipelines.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add MonaGEN directory to python path for clean relative imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Re-export core capabilities for programmatic usage
from core import (
    render_post,
    PostConfig,
    AspectRatio,
    SpritePosition,
    BrandPalette,
    resolve_background,
    resolve_sprite,
    get_font,
)
from cli import run_cli

__all__ = [
    "render_post",
    "PostConfig",
    "AspectRatio",
    "SpritePosition",
    "BrandPalette",
    "resolve_background",
    "resolve_sprite",
    "get_font",
    "run_cli",
]

if __name__ == "__main__":
    sys.exit(run_cli())

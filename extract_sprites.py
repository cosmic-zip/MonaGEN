"""
Extractor of 2.5D sprites from spritesheet for MonaGEN.
Extracts clean, transparent PNG sprites of the Foxxo Witch (Bunny Witch) mascot.
"""

from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np


# Rows and columns corresponding to the Foxxo Witch (Bunny/Fox ears style)
# Rows 2, 3, 4 (all 8 cols)
# Row 5 (cols 5, 6, 7) - Cheering / victory
# Row 7 (cols 5, 6, 7) - Dynamic posing / magic casting
FOXXO_WITCH_FRAMES = [
    # (row, col, pose_name_or_none)
    (4, 0, "idle"),
    (4, 1, "look_left"),
    (4, 2, "look_front"),
    (4, 3, "look_right"),
    (4, 4, "stance_front"),
    (4, 5, "stance_side"),
    (4, 6, "stand_back"),
    (4, 7, "stand_diag"),
    (2, 0, "walk_front"),
    (2, 1, "walk_left"),
    (2, 2, "walk_diag"),
    (2, 3, "walk_diag_right"),
    (2, 4, "walk_right"),
    (2, 5, "walk_back_diag"),
    (2, 6, "walk_back"),
    (2, 7, "walk_turn"),
    (3, 0, "run_left"),
    (3, 1, "run_diag"),
    (3, 2, "dash"),
    (3, 3, "run_right"),
    (3, 4, "run_front"),
    (3, 5, "run_back_diag"),
    (3, 6, "run_back"),
    (3, 7, "run_sprint"),
    (5, 5, "cheer_start"),
    (5, 6, "cheer_mid"),
    (5, 7, "cheer"),           # Victory with raised arm
    (7, 5, "magic_prep"),
    (7, 6, "magic_cast"),
    (7, 7, "magic"),           # Casting / victory stance
]


def remove_white_background(cell_img: Image.Image, threshold: int = 228) -> Image.Image:
    """
    Flood fills from the outer border to make the background transparent,
    while preserving white pixels inside the character (eyes, hat flowers, collar).
    """
    img_rgba = cell_img.convert("RGBA")
    arr = np.array(img_rgba)
    w, h = img_rgba.size

    # Check which pixels are candidate background (very bright / white)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_bg_candidate = ((r > threshold) & (g > threshold) & (b > threshold)).astype(np.uint8) * 255

    mask = Image.fromarray(is_bg_candidate, mode="L").copy()

    # Flood fill all background connected to outer borders
    for x in range(w):
        if mask.getpixel((x, 0)) == 255:
            ImageDraw.floodfill(mask, (x, 0), 128)
        if mask.getpixel((x, h - 1)) == 255:
            ImageDraw.floodfill(mask, (x, h - 1), 128)
    for y in range(h):
        if mask.getpixel((0, y)) == 255:
            ImageDraw.floodfill(mask, (0, y), 128)
        if mask.getpixel((w - 1, y)) == 255:
            ImageDraw.floodfill(mask, (w - 1, y), 128)

    mask_arr = np.array(mask)
    # 128 = exterior background (transparent)
    # Any other value (0 or 255) = character (opaque)
    alpha = np.where(mask_arr == 128, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha

    res = Image.fromarray(arr, mode="RGBA")
    bbox = res.getbbox()
    if bbox:
        # Crop to tight bounding box with 2px padding for crisp rendering
        left = max(0, bbox[0] - 2)
        top = max(0, bbox[1] - 2)
        right = min(w, bbox[2] + 2)
        bottom = min(h, bbox[3] + 2)
        res = res.crop((left, top, right, bottom))
    return res


def extract_sprites(
    spritesheet_path: str | Path,
    output_dir: str | Path,
    grid_cols: int = 8,
    grid_rows: int = 8,
) -> dict[str, Path]:
    """
    Extracts all Foxxo Witch sprites and saves them with transparent background.
    Returns dictionary mapping pose names / frame IDs to their saved Path.
    """
    src_path = Path(spritesheet_path)
    if not src_path.is_file():
        raise FileNotFoundError(f"Spritesheet not found at: {src_path}")

    out_base = Path(output_dir)
    frames_dir = out_base / "all_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    sheet = Image.open(src_path)
    sheet_w, sheet_h = sheet.size
    cell_w = sheet_w // grid_cols
    cell_h = sheet_h // grid_rows

    extracted_map: dict[str, Path] = {}

    for row, col, pose_name in FOXXO_WITCH_FRAMES:
        box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
        cell = sheet.crop(box)
        sprite = remove_white_background(cell)

        # Save indexed frame
        frame_filename = f"foxxo_r{row}_c{col}.png"
        frame_path = frames_dir / frame_filename
        sprite.save(frame_path, format="PNG")
        extracted_map[f"r{row}_c{col}"] = frame_path

        # If it has a primary pose name, save a shortcut directly in out_base
        if pose_name:
            named_path = out_base / f"{pose_name}.png"
            sprite.save(named_path, format="PNG")
            extracted_map[pose_name] = named_path

    return extracted_map


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Foxxo Witch sprites from spritesheet.")
    parser.add_argument(
        "--source",
        "-s",
        type=str,
        default="company_kit/main/sprites.jpg",
        help="Path to spritesheet image (default: company_kit/main/sprites.jpg)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="MonaGEN/assets/sprites/foxxo_witch",
        help="Output directory for extracted sprites",
    )
    args = parser.parse_args()

    results = extract_sprites(args.source, args.output)
    print(f"Successfully extracted {len(results)} Foxxo Witch sprite frames/poses to: {args.output}")


if __name__ == "__main__":
    main()

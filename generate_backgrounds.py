"""
16-Bit Pixel Art Galaxy & Stagecraft Background Generator for MonaGEN.
Creates canonical Cosmic Security backgrounds in true 16-bit SNES/MegaDrive aesthetic
with Bayer dithering, pixel stars, cosmic nebulae, and 2.5D perspective grid.
"""

from __future__ import annotations
import math
import random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


# Official Brand-Aligned 16-Bit Cosmic Palette
COLOR_PALETTE_16BIT = [
    (13, 16, 33),    # 0: Deepest Abyssal Void (#0D1021)
    (21, 28, 55),    # 1: Abyssal Void (#151C37)
    (39, 51, 87),    # 2: Deep Space Navy (#273357)
    (58, 44, 95),    # 3: Dark Cosmic Violet
    (93, 75, 133),   # 4: Synthwave Violet (#5D4B85)
    (145, 75, 115),  # 5: Nebula Purple
    (192, 94, 110),  # 6: Velvet Theatre Rose (#C05E6E)
    (75, 130, 175),  # 7: Cyber Sky Blue (#316FA0)
    (120, 180, 220), # 8: Bright Cyan Stardust
    (234, 153, 90),  # 9: Arcade Gold (#EA995A)
    (250, 225, 200), # 10: Starlight Parchment (#EFDFD2)
]

COLOR_ARCADE_GOLD = (234, 153, 90)
COLOR_VELVET_ROSE = (192, 94, 110)
COLOR_SYNTHWAVE_VIOLET = (93, 75, 133)
COLOR_CYBER_BLUE = (49, 111, 160)


def create_16bit_galaxy_canvas(
    width: int,
    height: int,
    scale_factor: int = 3,
    add_ground: bool = True,
    seed: int = 1337,
) -> Image.Image:
    """
    Renders an authentic 16-bit pixel-art galaxy with Bayer dithering,
    multi-layered cosmic nebulae, a distant pixel planet with rings,
    twinkling cross stars, and an optional 2.5D retro perspective floor.
    """
    random.seed(seed)
    np.random.seed(seed)

    lw = width // scale_factor
    lh = height // scale_factor

    y, x = np.mgrid[0:lh, 0:lw]

    # Diagonal angle for sweeping galactic dust stream
    cross_proj = (x * 0.7 - y * 0.7) / (lw * 0.7)
    ridge = np.exp(-(cross_proj * cross_proj) * 11.0)

    # Multi-frequency organic cosmic clouds
    noise = (
        np.sin(x * 0.04 + y * 0.03) * 0.35
        + np.sin(x * 0.08 - y * 0.06 + 1.2) * 0.25
        + np.sin(x * 0.15 + y * 0.12 + 2.5) * 0.15
        + np.sin(x * 0.02 - y * 0.04 + 0.8) * 0.25
    )

    nebula = ridge * 0.75 + noise * 0.35 + 0.15
    nebula = np.clip(nebula, 0.0, 1.0)

    # 4x4 Bayer Dithering Matrix for classic 16-bit texture
    bayer4 = np.array(
        [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5],
        ],
        dtype=float,
    ) / 16.0 - 0.5

    bayer_tiled = np.tile(bayer4, (lh // 4 + 1, lw // 4 + 1))[:lh, :lw]
    val = nebula * (len(COLOR_PALETTE_16BIT) - 2) + bayer_tiled * 0.85
    idx = np.clip(val.astype(int), 0, len(COLOR_PALETTE_16BIT) - 1)

    rgba = np.zeros((lh, lw, 4), dtype=np.uint8)
    rgba[:, :, 3] = 255
    for i, c in enumerate(COLOR_PALETTE_16BIT):
        rgba[idx == i, :3] = c

    img_low = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img_low)

    # 16-Bit Distant Pixel Planet with Ring
    px = int(lw * 0.16)
    py = int(lh * 0.18)
    pr = int(min(lw, lh) * 0.058)

    # Ring behind planet
    for angle in range(-45, 135):
        rad = math.radians(angle)
        rx = px + int(math.cos(rad) * pr * 2.2)
        ry = py + int(math.sin(rad) * pr * 0.6)
        if 0 <= rx < lw and 0 <= ry < lh:
            draw.point((rx, ry), fill=(*COLOR_ARCADE_GOLD, 200))

    # Planet body with 16-bit stepped shading
    for y_p in range(-pr, pr + 1):
        for x_p in range(-pr, pr + 1):
            if x_p * x_p + y_p * y_p <= pr * pr:
                shade = (x_p + y_p) / (pr * 1.5)
                if shade < -0.3:
                    pc = (*COLOR_ARCADE_GOLD, 255)
                elif shade < 0.2:
                    pc = (*COLOR_VELVET_ROSE, 255)
                else:
                    pc = (39, 51, 87, 255)
                draw.point((px + x_p, py + y_p), fill=pc)

    # Ring in front of planet
    for angle in range(135, 315):
        rad = math.radians(angle)
        rx = px + int(math.cos(rad) * pr * 2.2)
        ry = py + int(math.sin(rad) * pr * 0.6)
        if 0 <= rx < lw and 0 <= ry < lh:
            draw.point((rx, ry), fill=(*COLOR_ARCADE_GOLD, 255))
            draw.point((rx, ry + 1), fill=(*COLOR_VELVET_ROSE, 200))

    # 16-Bit Background Stars
    star_count = int(lw * lh * 0.016)
    for _ in range(star_count):
        sx = random.randint(0, lw - 1)
        sy = random.randint(0, lh - 1)
        if (sx - px) ** 2 + (sy - py) ** 2 < (pr * 2.5) ** 2:
            continue
        sc = random.choice([
            (255, 255, 255, 255),
            (180, 220, 255, 255),
            (255, 230, 190, 255),
            (220, 180, 240, 255),
        ])
        draw.point((sx, sy), fill=sc)

    # 16-Bit Twinkling Cross Stars
    for _ in range(14):
        bx = random.randint(8, lw - 8)
        by = random.randint(8, lh - 8)
        if (bx - px) ** 2 + (by - py) ** 2 < (pr * 2.5) ** 2:
            continue
        glow = random.choice([(*COLOR_ARCADE_GOLD, 255), (120, 190, 255, 255), (240, 150, 200, 255)])
        draw.point((bx, by), fill=(255, 255, 255, 255))
        draw.point((bx - 1, by), fill=glow)
        draw.point((bx + 1, by), fill=glow)
        draw.point((bx, by - 1), fill=glow)
        draw.point((bx, by + 1), fill=glow)
        if random.random() > 0.5:
            draw.point((bx - 2, by), fill=glow)
            draw.point((bx + 2, by), fill=glow)
            draw.point((bx, by - 2), fill=glow)
            draw.point((bx, by + 2), fill=glow)

    # Optional 2.5D Retro Perspective Ground Deck
    if add_ground:
        ground_y = int(lh * 0.64)
        for gy in range(ground_y, lh):
            t = (gy - ground_y) / (lh - ground_y)
            for gx in range(lw):
                if (gx + gy) % 2 == 0:
                    draw.point((gx, gy), fill=(25, 29, 45, int(140 + t * 95)))

        # Horizon line
        for gx in range(lw):
            draw.point((gx, ground_y), fill=(*COLOR_ARCADE_GOLD, 255))
            if gx % 2 == 0:
                draw.point((gx, ground_y + 1), fill=(*COLOR_SYNTHWAVE_VIOLET, 200))

        # 2.5D grid lines
        center_x = lw // 2
        for i in range(-16, 17):
            bot_x = center_x + int(i * (lw / 12))
            draw.line([(center_x, ground_y), (bot_x, lh)], fill=(*COLOR_CYBER_BLUE, 120), width=1)
        for step in [2, 6, 12, 20, 30, 45, 65, 90]:
            hy = ground_y + step
            if hy < lh:
                draw.line([(0, hy), (lw, hy)], fill=(*COLOR_CYBER_BLUE, 80), width=1)

    # Upscale with NEAREST for crisp 16-bit pixels
    img_1080 = img_low.resize((width, height), Image.Resampling.NEAREST)

    # Outer decorative arcade frame
    draw_final = ImageDraw.Draw(img_1080)
    border_thickness = 8
    draw_final.rectangle([0, 0, width - 1, height - 1], outline=(*COLOR_ARCADE_GOLD, 255), width=border_thickness)

    return img_1080


def create_theatrical_background(width: int, height: int) -> Image.Image:
    """
    Combines the 16-bit Galaxy with Theatrical Velvet Curtains.
    """
    img = create_16bit_galaxy_canvas(width, height, add_ground=True)
    draw = ImageDraw.Draw(img)

    curtain_w = int(width * 0.08)

    # Left Curtain drape
    for cx in range(curtain_w):
        drape_shade = math.sin(cx / 12.0) * 0.25 + 0.75
        cr = int(COLOR_VELVET_ROSE[0] * drape_shade)
        cg = int(COLOR_VELVET_ROSE[1] * drape_shade)
        cb = int(COLOR_VELVET_ROSE[2] * drape_shade)
        draw.line([(cx, 0), (cx, int(height * 0.85))], fill=(cr, cg, cb, 255))

    # Right Curtain drape
    for cx in range(curtain_w):
        x = width - 1 - cx
        drape_shade = math.sin(cx / 12.0) * 0.25 + 0.75
        cr = int(COLOR_VELVET_ROSE[0] * drape_shade)
        cg = int(COLOR_VELVET_ROSE[1] * drape_shade)
        cb = int(COLOR_VELVET_ROSE[2] * drape_shade)
        draw.line([(x, 0), (x, int(height * 0.85))], fill=(cr, cg, cb, 255))

    draw.line([(curtain_w, 0), (curtain_w, int(height * 0.85))], fill=(*COLOR_ARCADE_GOLD, 255), width=2)
    draw.line([(width - curtain_w, 0), (width - curtain_w, int(height * 0.85))], fill=(*COLOR_ARCADE_GOLD, 255), width=2)

    valance_h = 32
    draw.rectangle([0, 0, width, valance_h], fill=(*COLOR_VELVET_ROSE, 255))
    draw.line([(0, valance_h), (width, valance_h)], fill=(*COLOR_ARCADE_GOLD, 255), width=2)

    border_thickness = 8
    draw.rectangle([0, 0, width - 1, height - 1], outline=(*COLOR_ARCADE_GOLD, 255), width=border_thickness)
    return img


def generate_all_backgrounds(output_dir: str | Path) -> dict[str, Path]:
    """Generates all 1080p backgrounds (1:1 and 16:9) into the output directory."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    configs = [
        # 16-Bit Galaxy (Primary)
        ("cosmic_galaxy_1x1.png", lambda w, h: create_16bit_galaxy_canvas(w, h, add_ground=True), 1080, 1080),
        ("cosmic_galaxy_16x9.png", lambda w, h: create_16bit_galaxy_canvas(w, h, add_ground=True), 1920, 1080),
        # 16-Bit Pure Galaxy (Deep space only, no ground)
        ("pure_galaxy_1x1.png", lambda w, h: create_16bit_galaxy_canvas(w, h, add_ground=False), 1080, 1080),
        ("pure_galaxy_16x9.png", lambda w, h: create_16bit_galaxy_canvas(w, h, add_ground=False), 1920, 1080),
        # Theatrical Stagecraft with 16-Bit Galaxy
        ("cosmic_theatre_1x1.png", create_theatrical_background, 1080, 1080),
        ("cosmic_theatre_16x9.png", create_theatrical_background, 1920, 1080),
    ]

    saved: dict[str, Path] = {}
    for filename, func, w, h in configs:
        target = out / filename
        img = func(w, h)
        img.save(target, format="PNG")
        saved[filename] = target
        print(f"Generated 16-bit background: {target} ({w}x{h})")

    return saved


if __name__ == "__main__":
    generate_all_backgrounds("MonaGEN/assets/backgrounds")

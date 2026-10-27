"""
Core Rendering Engine for MonaGEN.
Composites backgrounds, 2.5D pixel art sprites, retrogame HUD, JRPG dialogue boxes,
and typography into high-definition 1080p social media graphics.
"""

from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .models import PostConfig, AspectRatio, SpritePosition, BrandPalette


CORE_DIR = Path(__file__).resolve().parent
BASE_DIR = CORE_DIR.parent
ASSETS_DIR = BASE_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
SPRITES_DIR = ASSETS_DIR / "sprites" / "foxxo_witch"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"


def get_font(font_name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Loads a font from the assets directory or falls back to default."""
    font_path = FONTS_DIR / font_name
    if font_path.is_file():
        try:
            return ImageFont.truetype(str(font_path), size)
        except Exception:
            pass
    try:
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Wraps text into multiple lines so it doesn't exceed max_width."""
    words = text.split(" ")
    lines: list[str] = []
    current_line: list[str] = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(" ".join(current_line))
    return lines


def resolve_background(bg_spec: str | Path, ratio: AspectRatio) -> Image.Image:
    """Resolves background image from preset or direct path, ensuring exact target dimensions."""
    w, h = ratio.dimensions
    ratio_suffix = "1x1" if ratio == AspectRatio.SQUARE_1X1 else "16x9"

    # 1. Preset check
    preset_filename = f"{bg_spec}_{ratio_suffix}.png"
    preset_path = BACKGROUNDS_DIR / preset_filename
    if preset_path.is_file():
        return Image.open(preset_path).convert("RGBA")

    # 2. Direct path check
    direct_path = Path(bg_spec)
    if not direct_path.is_file():
        direct_path = BACKGROUNDS_DIR / f"{bg_spec}.png"

    if direct_path.is_file():
        bg = Image.open(direct_path).convert("RGBA")
        if bg.size != (w, h):
            bg = bg.resize((w, h), Image.Resampling.LANCZOS)
        return bg

    return Image.new("RGBA", (w, h), (21, 28, 55, 255))


def resolve_sprite(sprite_spec: str | Path) -> Image.Image:
    """Resolves sprite from pose alias or direct path."""
    if isinstance(sprite_spec, str):
        named_path = SPRITES_DIR / f"{sprite_spec}.png"
        if named_path.is_file():
            return Image.open(named_path).convert("RGBA")

        all_frames_path = SPRITES_DIR / "all_frames" / f"foxxo_{sprite_spec}.png"
        if all_frames_path.is_file():
            return Image.open(all_frames_path).convert("RGBA")

    path = Path(sprite_spec)
    if path.is_file():
        return Image.open(path).convert("RGBA")

    idle_path = SPRITES_DIR / "idle.png"
    if idle_path.is_file():
        return Image.open(idle_path).convert("RGBA")

    return Image.new("RGBA", (100, 100), (0, 0, 0, 0))


def draw_jrpg_dialog_box(
    canvas: Image.Image,
    box: tuple[int, int, int, int],
    palette: BrandPalette,
) -> None:
    """Draws an authentic JRPG translucent dialog box with gold border & rivets."""
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1

    overlay = Image.new("RGBA", (w, h), (*palette.deep_space, 230))
    canvas.alpha_composite(overlay, (x1, y1))

    draw = ImageDraw.Draw(canvas)

    border_w = 4
    draw.rectangle([x1, y1, x2, y2], outline=(*palette.arcade_gold, 255), width=border_w)

    inset = 6
    draw.rectangle(
        [x1 + inset, y1 + inset, x2 - inset, y2 - inset],
        outline=(*palette.synthwave_violet, 180),
        width=2,
    )

    rivet_size = 8
    corners = [
        (x1 + 3, y1 + 3),
        (x2 - rivet_size - 3, y1 + 3),
        (x1 + 3, y2 - rivet_size - 3),
        (x2 - rivet_size - 3, y2 - rivet_size - 3),
    ]
    for rx, ry in corners:
        draw.rectangle([rx, ry, rx + rivet_size, ry + rivet_size], fill=(*palette.arcade_gold, 255))


def draw_hud(
    canvas: Image.Image,
    width: int,
    config: PostConfig,
    palette: BrandPalette,
) -> None:
    """Renders top retro arcade HUD bar with dedicated translucent backing."""
    hud_h = 44
    hud_y = 12
    hud_overlay = Image.new("RGBA", (width - 60, hud_h), (*palette.abyssal_void, 210))
    canvas.alpha_composite(hud_overlay, (30, hud_y))

    draw = ImageDraw.Draw(canvas)
    # Subtle border under HUD bar
    draw.line([(30, hud_y + hud_h), (width - 30, hud_y + hud_h)], fill=(*palette.arcade_gold, 180), width=2)

    font_hud = get_font("PressStart2P-Regular.ttf", 15)

    # Score on left
    draw.text((55, hud_y + 14), config.hud_score, fill=(*palette.arcade_gold, 255), font=font_hud)

    # Lives / Hearts in center
    hearts = "♥ " * config.hud_lives
    bbox_h = draw.textbbox((0, 0), hearts.strip(), font=font_hud)
    hw = bbox_h[2] - bbox_h[0]
    draw.text(((width - hw) // 2, hud_y + 14), hearts.strip(), fill=(*palette.velvet_rose, 255), font=font_hud)

    # Stage on right
    bbox = draw.textbbox((0, 0), config.hud_stage, font=font_hud)
    stage_w = bbox[2] - bbox[0]
    draw.text((width - 55 - stage_w, hud_y + 14), config.hud_stage, fill=(*palette.parchment, 255), font=font_hud)


def draw_sprite_with_shadow(
    canvas: Image.Image,
    sprite: Image.Image,
    x: int,
    y: int,
    scale: float,
    palette: BrandPalette,
) -> None:
    """Scales sprite with nearest-neighbor and renders an elliptical 2.5D floor shadow."""
    new_w = int(sprite.width * scale)
    new_h = int(sprite.height * scale)
    scaled_sprite = sprite.resize((new_w, new_h), Image.Resampling.NEAREST)

    shadow_w = int(new_w * 0.78)
    shadow_h = int(new_w * 0.24)
    shadow_x = x + (new_w - shadow_w) // 2
    shadow_y = y + new_h - shadow_h // 2 - 8

    shadow_img = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.ellipse(
        [shadow_x, shadow_y, shadow_x + shadow_w, shadow_y + shadow_h],
        fill=(0, 0, 0, 130),
    )
    canvas.alpha_composite(shadow_img)
    canvas.alpha_composite(scaled_sprite, (x, y))


def render_post(config: PostConfig) -> Image.Image:
    """
    Main entry point of the rendering engine.
    Renders a complete, production-ready social media post graphic in 1080p.
    """
    palette = config.palette
    ratio = config.ratio if isinstance(config.ratio, AspectRatio) else AspectRatio(config.ratio)
    width, height = ratio.dimensions

    # 1. Base Canvas & Background
    canvas = resolve_background(config.background, ratio)

    # 2. Top HUD Bar
    draw_hud(canvas, width, config, palette)

    # 3. Fonts
    font_title = get_font("Silkscreen-Bold.ttf", 36 if ratio == AspectRatio.SQUARE_1X1 else 40)
    font_body = get_font("VT323-Regular.ttf", 38 if ratio == AspectRatio.SQUARE_1X1 else 42)
    font_badge = get_font("PressStart2P-Regular.ttf", 13)
    font_footer = get_font("Silkscreen-Bold.ttf", 15)

    # 4. Resolve Sprite
    sprite = resolve_sprite(config.sprite)

    if ratio == AspectRatio.SQUARE_1X1:
        # Layout 1:1 (Square 1080x1080)
        dialog_box = (60, 80, 1020, 560)
        draw_jrpg_dialog_box(canvas, dialog_box, palette)

        content_draw = ImageDraw.Draw(canvas)
        cursor_y = 115
        padding_x = 95
        max_text_w = (dialog_box[2] - dialog_box[0]) - 70

        # Badge
        if config.badge:
            badge_text = f"★ {config.badge.upper()} ★"
            bbox_badge = content_draw.textbbox((0, 0), badge_text, font=font_badge)
            badge_w = bbox_badge[2] - bbox_badge[0]
            badge_h = bbox_badge[3] - bbox_badge[1]
            badge_box = [padding_x, cursor_y - 4, padding_x + badge_w + 20, cursor_y + badge_h + 12]
            content_draw.rectangle(badge_box, fill=(*palette.velvet_rose, 255), outline=(*palette.arcade_gold, 255), width=2)
            content_draw.text((padding_x + 10, cursor_y + 2), badge_text, fill=(*palette.white, 255), font=font_badge)
            cursor_y += badge_h + 30

        # Title
        content_draw.text((padding_x, cursor_y), config.title, fill=(*palette.arcade_gold, 255), font=font_title)
        bbox_t = content_draw.textbbox((0, 0), config.title, font=font_title)
        cursor_y += (bbox_t[3] - bbox_t[1]) + 20

        # Body Text
        body_lines = wrap_text(config.text, font_body, max_text_w, content_draw)
        line_height = 42
        for line in body_lines:
            content_draw.text((padding_x, cursor_y), line, fill=(*palette.parchment, 255), font=font_body)
            cursor_y += line_height

        # Position Sprite on the lower 2.5D Stage floor
        sprite_scale = config.sprite_scale
        scaled_w = int(sprite.width * sprite_scale)
        scaled_h = int(sprite.height * sprite_scale)

        if config.sprite_position == SpritePosition.BOTTOM_LEFT:
            sp_x = 90
        elif config.sprite_position == SpritePosition.CENTER:
            sp_x = (width - scaled_w) // 2
        else:  # BOTTOM_RIGHT default
            sp_x = width - scaled_w - 90

        sp_y = height - scaled_h - 75
        draw_sprite_with_shadow(canvas, sprite, sp_x, sp_y, sprite_scale, palette)

        # Footer Badge at bottom left
        if config.footer:
            f_draw = ImageDraw.Draw(canvas)
            bbox_f = f_draw.textbbox((0, 0), config.footer, font=font_footer)
            fw = bbox_f[2] - bbox_f[0]
            fh = bbox_f[3] - bbox_f[1]
            footer_x = 60
            footer_y = height - 58
            # Badge pill for footer
            pill = Image.new("RGBA", (fw + 24, fh + 16), (*palette.abyssal_void, 220))
            canvas.alpha_composite(pill, (footer_x - 12, footer_y - 8))
            f_draw.rectangle([footer_x - 12, footer_y - 8, footer_x + fw + 12, footer_y + fh + 8], outline=(*palette.arcade_gold, 180), width=1)
            f_draw.text((footer_x, footer_y), config.footer, fill=(*palette.parchment, 255), font=font_footer)

    else:
        # Layout 16:9 (Landscape 1920x1080)
        dialog_box = (80, 85, 1260, 990)
        draw_jrpg_dialog_box(canvas, dialog_box, palette)

        content_draw = ImageDraw.Draw(canvas)
        cursor_y = 135
        padding_x = 125
        max_text_w = (dialog_box[2] - dialog_box[0]) - 90

        # Badge
        if config.badge:
            badge_text = f"★ {config.badge.upper()} ★"
            bbox_badge = content_draw.textbbox((0, 0), badge_text, font=font_badge)
            badge_w = bbox_badge[2] - bbox_badge[0]
            badge_h = bbox_badge[3] - bbox_badge[1]
            badge_box = [padding_x, cursor_y - 4, padding_x + badge_w + 24, cursor_y + badge_h + 16]
            content_draw.rectangle(badge_box, fill=(*palette.velvet_rose, 255), outline=(*palette.arcade_gold, 255), width=2)
            content_draw.text((padding_x + 12, cursor_y + 3), badge_text, fill=(*palette.white, 255), font=font_badge)
            cursor_y += badge_h + 38

        # Title
        content_draw.text((padding_x, cursor_y), config.title, fill=(*palette.arcade_gold, 255), font=font_title)
        bbox_t = content_draw.textbbox((0, 0), config.title, font=font_title)
        cursor_y += (bbox_t[3] - bbox_t[1]) + 28

        # Body Text
        body_lines = wrap_text(config.text, font_body, max_text_w, content_draw)
        line_height = 46
        for line in body_lines:
            content_draw.text((padding_x, cursor_y), line, fill=(*palette.parchment, 255), font=font_body)
            cursor_y += line_height

        # Footer inside dialog box
        if config.footer:
            content_draw.text((padding_x, dialog_box[3] - 50), config.footer, fill=(*palette.twilight_slate, 255), font=font_footer)

        # Right side: Foxxo Witch presentation
        sprite_scale = config.sprite_scale * 1.2
        scaled_w = int(sprite.width * sprite_scale)
        scaled_h = int(sprite.height * sprite_scale)
        sp_x = 1320 + (1920 - 1320 - scaled_w) // 2
        sp_y = height - scaled_h - 120
        draw_sprite_with_shadow(canvas, sprite, sp_x, sp_y, sprite_scale, palette)

    return canvas

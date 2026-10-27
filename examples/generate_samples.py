"""
Sample post generation demonstrating programmatic usage of MonaGEN Core API (No CLI required).
Generates both 1:1 and 16:9 posts for social media.
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from core import render_post, PostConfig, AspectRatio, SpritePosition


def generate_sample_posts():
    output_dir = BASE_DIR / "examples" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Instagram / LinkedIn Feed Post (1:1 - 1080x1080)
    config_1x1 = PostConfig(
        ratio=AspectRatio.SQUARE_1X1,
        badge="BUG HUNTING",
        title="O Que e Bug Hunting?",
        text=(
            "Como dizemos aos nossos clientes: nao e sobre telas pretas ou codigos assustadores. "
            "E como revistar o castelo antes do baile para garantir que nenhuma porta ficou destrancada. "
            "A Foxxo Witch rastreia falhas e protege seu sistema com escudos de protecao!"
        ),
        sprite="cheer",
        sprite_position=SpritePosition.BOTTOM_RIGHT,
        background="cosmic_galaxy",
        hud_score="SCORE 88420",
        hud_stage="WORLD 1-1",
        footer="@cosmic_security  |  selene.io",
    )

    img_1x1 = render_post(config_1x1)
    path_1x1 = output_dir / "sample_post_1x1.png"
    img_1x1.save(path_1x1, format="PNG")
    print(f"Generated 1:1 sample post: {path_1x1}")

    # 2. Twitter / YouTube Banner Post (16:9 - 1920x1080)
    config_16x9 = PostConfig(
        ratio=AspectRatio.LANDSCAPE_16X9,
        badge="DEV SOB MEDIDA",
        title="O Castelo Digital Seguro",
        text=(
            "Criamos aplicacoes robustas onde cada porta tem tranca digital de verdade. "
            "Com Row-Level Security (RLS), os dados de cada cliente ficam em um cofre individual "
            "com chave unica. Seguranca e performance em uma experiencia teatral sem complicacoes!"
        ),
        sprite="magic",
        background="retro_grid",
        hud_score="SCORE 99990",
        hud_stage="STAGE 04",
        hud_lives=3,
        footer="Cosmic Security & Development Services  •  selene.io",
    )

    img_16x9 = render_post(config_16x9)
    path_16x9 = output_dir / "sample_post_16x9.png"
    img_16x9.save(path_16x9, format="PNG")
    print(f"Generated 16:9 sample post: {path_16x9}")


if __name__ == "__main__":
    generate_sample_posts()

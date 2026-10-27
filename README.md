# MonaGEN — 1080p Social Post Graphic Generator

Motor de composição e geração de imagens PNG em alta resolução (**1080p**) nas proporções **1:1** (`1080x1080`) e **16:9** (`1920x1080`) para redes sociais, desenvolvido para a **Cosmic Security & Development Services**.

Combina a estética canônica **Theatrical Stagecraft** (palco teatral com cortinas de veludo e acabamento dourado) com **16-Bit Retrogame** (sprites 2.5D, HUD arcade, caixas de diálogo estilo JRPG e fontes clássicas).

---

## 📁 Estrutura do Projeto

```
MonaGEN/
├── assets/
│   ├── backgrounds/
│   │   ├── cosmic_theatre_1x1.png       # 1080x1080 palco teatral + grade 2.5D
│   │   ├── cosmic_theatre_16x9.png      # 1920x1080 palco teatral + grade 2.5D
│   │   ├── retro_grid_1x1.png           # 1080x1080 synthwave grid + sol retrô
│   │   └── retro_grid_16x9.png          # 1920x1080 synthwave grid + sol retrô
│   ├── sprites/
│   │   └── foxxo_witch/                 # 30+ poses recortadas com canal alpha transparente
│   │       ├── idle.png                 # Parada frente
│   │       ├── cheer.png                # Comemorando com braço levantado
│   │       ├── magic.png                # Conjurando magia / pose dinâmica
│   │       ├── walk_front.png           # Andando visão 2.5D
│   │       ├── walk_diag.png            # Andando diagonal 2.5D
│   │       ├── dash.png                 # Dash / corrida rápida
│   │       └── all_frames/              # Todos os frames individuais da Foxxo Witch
│   └── fonts/
│       ├── PressStart2P-Regular.ttf     # Títulos Arcade / HUD
│       ├── Silkscreen-Bold.ttf          # Badges / Subtítulos
│       └── VT323-Regular.ttf            # Diálogos / Corpo de texto
├── core/                                # Engine desacoplada (Core Library)
│   ├── __init__.py                      # Exporta render_post, PostConfig, AspectRatio, etc.
│   ├── models.py                        # Dataclasses, enums e paleta oficial da marca
│   └── renderer.py                      # Composição visual, sombras 2.5D, caixas JRPG e texto
├── cli.py                               # Interface de linha de comando isolada
├── generate_post.py                     # Entry point principal executável e importável
├── extract_sprites.py                   # Script de extração das sprites da Foxxo Witch
├── generate_backgrounds.py              # Script gerador dos planos de fundo procedurais
└── examples/
    └── generate_samples.py              # Exemplos de uso programático em Python
```

---

## 🚀 Como Usar

### 1. Via Linha de Comando (CLI)

O módulo `cli.py` foi construído de forma completamente separada do core, permitindo uso direto no terminal:

```bash
# Gerar post quadrado (1:1 - 1080x1080)
python3 MonaGEN/generate_post.py \
  --ratio 1x1 \
  --badge "BUG HUNTING" \
  --title "O QUE E BUG HUNTING?" \
  --text "E como revistar o castelo antes do baile para garantir que nenhuma porta ficou destrancada." \
  --sprite cheer \
  --output post_feed.png

# Gerar banner widescreen (16:9 - 1920x1080)
python3 MonaGEN/generate_post.py \
  --ratio 16x9 \
  --badge "DEV SOB MEDIDA" \
  --title "CASTELO DIGITAL SEGURO" \
  --text "Criamos aplicacoes com Row-Level Security onde cada cliente tem cofre proprio com chave unica." \
  --sprite magic \
  --background retro_grid \
  --output post_banner.png
```

#### Opções da CLI:
- `--ratio`, `-r`: `1x1` (1080x1080) ou `16x9` (1920x1080).
- `--title`, `-t`: Título em destaque do card.
- `--text`, `-m`: Mensagem / corpo do diálogo (com quebra de linha automática).
- `--badge`, `-b`: Tag de categoria (`BUG HUNTING`, `PENTEST`, `DICA DEV`, etc.).
- `--sprite`, `-s`: Apelido da pose da Foxxo Witch (`idle`, `cheer`, `magic`, `walk_front`, `dash`, etc.) ou caminho para imagem PNG.
- `--position`, `-p`: Posição da sprite no piso (`bottom_right`, `bottom_left`, `center`).
- `--scale`: Fator de escala pixel-art (padrão `2.6`).
- `--background`, `-bg`: Preset (`cosmic_theatre`, `retro_grid`) ou arquivo customizado.
- `--score`: Placar arcade no topo esquerdo (ex: `SCORE 99990`).
- `--stage`: Estágio arcade no topo direito (ex: `STAGE 01`).
- `--lives`: Quantidade de corações de vida no HUD (padrão `3`).
- `--footer`, `-f`: Assinatura / redes sociais no rodapé.
- `--output`, `-o`: Arquivo de destino PNG.

---

### 2. Uso Programático em Python (Sem CLI)

O `core` pode ser importado em APIs Web (FastAPI, Flask), bots do Discord/Telegram, cronjobs ou scripts de automação:

```python
from MonaGEN.core import render_post, PostConfig, AspectRatio, SpritePosition

# Configurar o post
config = PostConfig(
    ratio=AspectRatio.SQUARE_1X1,  # ou AspectRatio.LANDSCAPE_16X9
    title="PORTAS DESTRANCADAS",
    text="Uma vulnerabilidade nada mais e do que uma porta sem tranca no castelo digital. Nos encontramos antes dos invasores!",
    badge="CIBERSEGURANCA",
    sprite="walk_front",
    sprite_position=SpritePosition.BOTTOM_RIGHT,
    background="cosmic_theatre",
    hud_score="SCORE 75210",
    hud_stage="STAGE 02",
    footer="@cosmic_security | selene.io",
)

# Renderizar imagem PIL
imagem_post = render_post(config)

# Salvar ou enviar em buffer HTTP
imagem_post.save("meu_post.png", format="PNG")
```

---

## 🦊 Sprites da Foxxo Witch

As sprites foram extraídas diretamente de `company_kit/main/sprites.jpg` preservando os pixels originais e removendo o fundo branco para transparência alfa perfeita:
- Orelhinhas pontudas de coelho/raposa características da mascote.
- Chapéu de bruxa com flores e capa escura com cachecol listrado.
- Sombra elíptica 2.5D projetada automaticamente no chão do palco.

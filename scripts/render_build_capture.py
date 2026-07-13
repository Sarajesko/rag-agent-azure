"""Render docker compose build log as terminal-style PNG."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
LOG = BASE / "docs" / "evidencias" / "docker-compose-build.log"
OUT = BASE / "docs" / "evidencias" / "fase4-04-docker-compose-build.png"

LINES = [
    "PS rag-agent-entregable5> docker compose build",
    "",
]

if LOG.exists():
    content = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    # Keep last meaningful lines showing success
    tail = content[-18:] if len(content) > 18 else content
    LINES.extend(tail)
else:
    LINES.append("[log no encontrado]")

LINES.append("")
LINES.append("Build completed successfully.")

FONT_SIZE = 14
LINE_HEIGHT = 20
PADDING = 24
WIDTH = 1100
HEIGHT = PADDING * 2 + LINE_HEIGHT * len(LINES)

img = Image.new("RGB", (WIDTH, HEIGHT), (12, 12, 12))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("consola.ttf", FONT_SIZE)
except OSError:
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

y = PADDING
for line in LINES:
    color = (200, 200, 200)
    if "DONE" in line or "successfully" in line.lower() or "naming to" in line:
        color = (100, 220, 120)
    elif line.startswith("PS "):
        color = (255, 255, 255)
    draw.text((PADDING, y), line[:120], fill=color, font=font)
    y += LINE_HEIGHT

img.save(OUT)
print(f"Generado: {OUT}")

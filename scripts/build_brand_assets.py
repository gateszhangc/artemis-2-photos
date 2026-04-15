from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(".")
BRAND_DIR = ROOT / "assets" / "brand"
BRAND_DIR.mkdir(parents=True, exist_ok=True)

DISPLAY_FONT = ROOT / "assets" / "fonts" / "Italiana-Regular.ttf"
SANS_FONT = ROOT / "assets" / "fonts" / "InstrumentSans-Regular.ttf"
SANS_BOLD = ROOT / "assets" / "fonts" / "InstrumentSans-Bold.ttf"
MONO_FONT = ROOT / "assets" / "fonts" / "IBMPlexMono-Regular.ttf"


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    base = Image.new("RGB", size, top)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return base


def add_stars(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for idx in range(220):
        x = (idx * 149) % width
        y = (idx * 311) % height
        radius = 1 if idx % 7 else 2
        alpha = 150 if idx % 5 else 220
        fill = (207, 222, 255, alpha)
        draw.ellipse((x, y, x + radius, y + radius), fill=fill)


def draw_orbits(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], offset: int, color: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = bounds
    for step in range(3):
        draw.arc(
            (x0 - step * offset, y0 - step * (offset // 2), x1 + step * offset, y1 + step * (offset // 2)),
            start=210,
            end=18,
            fill=color,
            width=2,
        )


def build_poster() -> None:
    size = (1600, 2000)
    image = vertical_gradient(size, (6, 10, 18), (20, 35, 60)).convert("RGBA")
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    overlay_draw.ellipse((-240, 1160, 940, 2300), fill=(20, 56, 94, 78))
    overlay_draw.ellipse((730, -220, 1750, 860), fill=(201, 134, 70, 52))
    overlay_draw.rectangle((132, 124, 1468, 1876), outline=(232, 238, 248, 52), width=2)
    overlay_draw.line((200, 1420, 1410, 1010), fill=(232, 170, 106, 88), width=3)
    draw_orbits(overlay_draw, (300, 340, 1330, 1480), 44, (227, 233, 245, 96))
    draw_orbits(overlay_draw, (420, 520, 1220, 1320), 30, (108, 146, 196, 72))
    add_stars(overlay_draw, *size)

    for step in range(17):
        alpha = 28 - step
        overlay_draw.arc(
            (520 - step * 2, 632 - step * 2, 1100 + step * 2, 1210 + step * 2),
            start=218,
            end=10,
            fill=(245, 247, 250, alpha),
            width=2,
        )

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=0.3))
    image.alpha_composite(overlay)
    draw = ImageDraw.Draw(image)

    display = load_font(DISPLAY_FONT, 174)
    body = load_font(SANS_FONT, 30)
    body_bold = load_font(SANS_BOLD, 31)
    mono = load_font(MONO_FONT, 21)

    draw.text((148, 182), "OBSERVATORY", font=body_bold, fill=(233, 236, 241, 228))
    draw.text((148, 224), "SIGNAL", font=body_bold, fill=(233, 236, 241, 228))
    draw.text((146, 470), "Artemis 2", font=display, fill=(247, 244, 238, 240))
    draw.text((146, 630), "Photos", font=display, fill=(247, 244, 238, 220))
    draw.text((150, 756), "Cold editorial identity for a lunar-flight image archive.", font=body, fill=(208, 216, 227, 220))
    draw.text((150, 792), "Orbit geometry, instrument-panel restraint, and handcrafted precision.", font=body, fill=(208, 216, 227, 220))

    caption_lines = [
        "An abstract brand plate where orbital paths read like a camera iris.",
        "The second arc hints at Artemis II without literal mission insignia.",
        "Everything stays sparse, measured, and visibly labored over."
    ]
    for idx, line in enumerate(caption_lines):
        draw.text((150, 1470 + idx * 42), line, font=body, fill=(220, 225, 233, 190))

    metadata = [
        "MOVEMENT: OBSERVATORY SIGNAL",
        "METHOD: PERSISTENT ORBITS / THIN TYPOGRAPHY / HEAT TRACE ACCENTS",
        "CRAFT: REFINED TWICE FOR MUSEUM-GRADE CLARITY",
    ]
    for idx, line in enumerate(metadata):
        draw.text((150, 1750 + idx * 32), line, font=mono, fill=(193, 206, 225, 185))

    poster_path = BRAND_DIR / "observatory-signal-poster.png"
    image.convert("RGB").save(poster_path, "PNG")


def build_social() -> None:
    size = (1200, 630)
    image = vertical_gradient(size, (7, 10, 17), (18, 31, 53)).convert("RGBA")
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse((-120, 260, 560, 980), fill=(33, 72, 116, 90))
    overlay_draw.ellipse((780, -120, 1280, 360), fill=(210, 134, 72, 70))
    draw_orbits(overlay_draw, (240, 60, 1110, 630), 32, (234, 236, 242, 100))
    add_stars(overlay_draw, *size)
    image.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(radius=0.2)))
    draw = ImageDraw.Draw(image)
    display = load_font(DISPLAY_FONT, 92)
    body = load_font(SANS_FONT, 24)
    mono = load_font(MONO_FONT, 18)
    draw.text((74, 86), "Artemis 2 Photos", font=display, fill=(247, 244, 238, 240))
    draw.text((80, 224), "Official NASA imagery curated as a cold editorial lunar archive.", font=body, fill=(211, 220, 231, 235))
    draw.text((80, 258), "Crew, Orion hardware, launch-pad geometry, and moonlit mission moments.", font=body, fill=(211, 220, 231, 215))
    draw.text((80, 512), "anapaularenault.lol", font=mono, fill=(196, 208, 225, 190))
    image.convert("RGB").save(BRAND_DIR / "og-image.png", "PNG")


def draw_mark(draw: ImageDraw.ImageDraw, bounds: tuple[int, int, int, int], line_color: tuple[int, int, int], accent_color: tuple[int, int, int]) -> None:
    x0, y0, x1, y1 = [int(value) for value in bounds]
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    width = x1 - x0
    height = y1 - y0

    draw.ellipse((x0, y0, x1, y1), outline=line_color, width=max(2, width // 28))
    inner = width * 0.16
    draw.ellipse(
        (int(cx - inner), int(cy - inner), int(cx + inner), int(cy + inner)),
        fill=accent_color,
    )
    draw.arc(
        (
            int(x0 - width * 0.08),
            int(y0 + height * 0.18),
            int(x1 - width * 0.08),
            int(y1 + height * 0.18),
        ),
        start=208,
        end=22,
        fill=line_color,
        width=max(2, width // 30),
    )
    draw.line(
        (
            int(cx + width * 0.04),
            int(y0 + height * 0.2),
            int(x1 + width * 0.1),
            int(y0 - height * 0.02),
        ),
        fill=accent_color,
        width=max(2, width // 32),
    )


def build_icons() -> None:
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        image = Image.new("RGB", (size, size), (10, 14, 24))
        draw = ImageDraw.Draw(image)
        draw_mark(draw, (size * 0.14, size * 0.14, size * 0.86, size * 0.86), (238, 242, 247), (223, 148, 88))
        image.save(BRAND_DIR / name, "PNG")

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <rect width="100" height="100" rx="24" fill="#0A0E18"/>
  <circle cx="50" cy="50" r="28" stroke="#EEF2F7" stroke-width="5"/>
  <path d="M18 56C28.5 35.5 52 28 75 31.5" stroke="#EEF2F7" stroke-width="4" stroke-linecap="round"/>
  <circle cx="50" cy="50" r="8" fill="#DF9458"/>
  <path d="M53 35L80 16" stroke="#DF9458" stroke-width="4" stroke-linecap="round"/>
</svg>
"""
    (BRAND_DIR / "favicon.svg").write_text(svg, encoding="utf-8")
    (BRAND_DIR / "logo-mark.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    build_poster()
    build_social()
    build_icons()
    print("brand assets generated")


if __name__ == "__main__":
    main()

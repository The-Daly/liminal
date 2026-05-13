#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generated" / "ui" / "menu_operations_overlay.png"
W, H = 1920, 1080

FRAME = (166, 176, 124, 210)
FILL = (10, 14, 12, 184)
FILL_LIGHT = (18, 22, 19, 196)
TEXT_MAIN = (224, 228, 208, 255)
TEXT_MUTED = (134, 148, 111, 255)
TEXT_ACCENT = (239, 192, 84, 255)


def font(path: str, size: int):
    return ImageFont.truetype(path, size)


FONT_DIR = Path("C:/Windows/Fonts")
FONT_UI = font(str(FONT_DIR / "segoeui.ttf"), 18)
FONT_UI_LARGE = font(str(FONT_DIR / "segoeui.ttf"), 26)
FONT_TITLE = font(str(FONT_DIR / "bahnschrift.ttf"), 66)
FONT_HEAD = font(str(FONT_DIR / "consolab.ttf"), 28)
FONT_MONO = font(str(FONT_DIR / "consola.ttf"), 17)
FONT_MONO_BIG = font(str(FONT_DIR / "consolab.ttf"), 44)


def panel(draw: ImageDraw.ImageDraw, box, fill=FILL, frame=FRAME, inner_pad=2):
    draw.rounded_rectangle(box, radius=0, outline=frame, width=2, fill=fill)
    inner = (box[0] + inner_pad, box[1] + inner_pad, box[2] - inner_pad, box[3] - inner_pad)
    draw.rectangle(inner, fill=fill)


def txt(draw, xy, text, fill, font_obj, anchor="la"):
    draw.text(xy, text, font=font_obj, fill=fill, anchor=anchor)


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    panel(draw, (36, 26, 402, 154), fill=(8, 11, 9, 170))
    txt(draw, (58, 52), "REER-LIMINAL OPS NETWORK", TEXT_MUTED, FONT_UI)
    txt(draw, (58, 84), "CONNECTION: LOCAL", TEXT_MAIN, FONT_UI)
    txt(draw, (58, 114), "ZONE ACCESS: RESTRICTED", TEXT_ACCENT, FONT_UI)
    txt(draw, (58, 144), "SIGNAL STABILITY: DEGRADED", TEXT_MUTED, FONT_UI)

    txt(draw, (960, 76), "L I M I N A L", TEXT_MAIN, FONT_TITLE, anchor="ma")
    txt(draw, (960, 128), "<<<  OPERATIONS.HUB  >>>", TEXT_MUTED, FONT_UI_LARGE, anchor="ma")

    panel(draw, (1498, 26, 1848, 154), fill=(8, 11, 9, 170))
    txt(draw, (1524, 58), "KB/CTRL NAV ENABLED", TEXT_MAIN, FONT_UI)
    txt(draw, (1524, 96), "SFX_HOVER", TEXT_MUTED, FONT_UI)
    txt(draw, (1524, 132), "SFX_CLICK", TEXT_MUTED, FONT_UI)

    panel(draw, (22, 190, 426, 958))
    txt(draw, (42, 214), "// MAIN MENU", TEXT_MUTED, FONT_UI)
    nav_items = ["DEPLOY", "LOADOUT", "OPERATORS", "MARKET", "INTEL", "SETTINGS", "EXIT"]
    y = 250
    for idx, label in enumerate(nav_items):
        highlight = idx == 0
        panel(
            draw,
            (40, y, 406, y + 76),
            fill=(44, 31, 10, 205) if highlight else FILL_LIGHT,
            frame=TEXT_ACCENT if highlight else FRAME,
        )
        txt(draw, (72, y + 38), ">>" if highlight else "[]", TEXT_ACCENT if highlight else TEXT_MUTED, FONT_UI_LARGE, anchor="lm")
        txt(draw, (128, y + 38), label, TEXT_ACCENT if highlight else TEXT_MAIN, FONT_UI_LARGE, anchor="lm")
        y += 96
    txt(draw, (44, 928), "NAVIGATION SUPPORT: ON", TEXT_MUTED, FONT_UI)

    panel(draw, (452, 190, 1432, 958))
    txt(draw, (486, 234), "OPERATION: SERVICE HALLS", TEXT_MAIN, FONT_HEAD)
    panel(draw, (1216, 216, 1380, 258), fill=(16, 20, 16, 190))
    txt(draw, (1298, 237), "ZONE // SH-17", TEXT_MUTED, FONT_UI, anchor="mm")

    preview = (484, 278, 1400, 684)
    draw.rounded_rectangle(preview, radius=0, outline=(118, 126, 96, 140), width=2, fill=(8, 11, 9, 52))
    txt(draw, (514, 312), "LIVE FEED // LEVEL 1 SERVICE HALLS", TEXT_MUTED, FONT_UI)
    txt(draw, (514, 348), "Stable route active. Menu shell mounted over in-world feed.", TEXT_MAIN, FONT_UI)

    metrics = [
        ("THREAT LEVEL", "HIGH", "////"),
        ("EXTRACTION WINDOWS", "00:20-00:30", "00:50-01:00 | 01:20-01:30"),
        ("ENVIRONMENTAL ANOMALY", "DISORIENTATION", "SIGNAL INTERFERENCE"),
        ("RECOMMENDED TEAM SIZE", "1 - 3", "FIELD UNIT"),
        ("BRIEF OBJECTIVE", "INVESTIGATE SERVICE HALLS", "RECOVER DIAGNOSTICS FROM TERM-3 NODE"),
    ]
    panel(draw, (474, 704, 1404, 854), fill=FILL_LIGHT)
    x = 492
    width = 176
    for head, body, sub in metrics:
        txt(draw, (x, 730), head, TEXT_MUTED, FONT_MONO)
        txt(draw, (x, 772), body, TEXT_ACCENT if head == "THREAT LEVEL" else TEXT_MAIN, FONT_UI)
        txt(draw, (x, 808), sub, TEXT_MUTED, FONT_MONO)
        x += width

    panel(draw, (640, 876, 1238, 948), fill=(44, 31, 10, 224), frame=TEXT_ACCENT)
    txt(draw, (939, 905), "DEPLOY", TEXT_ACCENT, FONT_MONO_BIG, anchor="mm")
    txt(draw, (939, 936), "ENTER ZONE", TEXT_MAIN, FONT_UI_LARGE, anchor="mm")

    panel(draw, (1462, 190, 1852, 958))
    txt(draw, (1486, 214), "// OPERATOR STATUS", TEXT_MUTED, FONT_UI)
    cards = [
        ("OPERATOR NAME", "GHOST-7", "ID: 7GH-4X2-19K"),
        ("FACTION", "REER", "RESEARCH & EXTRACTION ENFORCEMENT REGIME"),
        ("HEALTH CONDITION", "GOOD", "100%"),
        ("REPUTATION", "TIER III - RELIANT", "2,458 / 5,000"),
        ("CURRENCY / RESOURCES", "18,420 CREDITS", "450 RESEARCH | 12 TOKENS"),
        ("CURRENT KIT SUMMARY", "M4A1 | G17 | 2 TACTICAL", "2 UTILITY | FIELD MED"),
    ]
    card_y = 242
    for title, body, sub in cards:
        panel(draw, (1484, card_y, 1830, card_y + 100), fill=FILL_LIGHT)
        txt(draw, (1508, card_y + 24), title, TEXT_MUTED, FONT_MONO)
        txt(draw, (1508, card_y + 56), body, TEXT_MAIN, FONT_UI_LARGE)
        txt(draw, (1508, card_y + 82), sub, TEXT_MUTED, FONT_MONO)
        card_y += 116

    panel(draw, (22, 978, 1852, 1058), fill=(8, 11, 9, 170))
    txt(draw, (44, 1018), "BUILD: V0.1.0", TEXT_MUTED, FONT_UI, anchor="lm")
    txt(draw, (356, 1018), "ENV: LOCAL TEST", TEXT_MUTED, FONT_UI, anchor="lm")
    txt(draw, (955, 1018), "ALL SYSTEMS NOMINAL... STANDBY", TEXT_MAIN, FONT_UI, anchor="mm")
    txt(draw, (1784, 1018), "22:47:16   LOCAL TIME", TEXT_MUTED, FONT_UI, anchor="rm")

    image = image.rotate(-90, expand=True).resize((W, H))
    image.save(OUT)


if __name__ == "__main__":
    build()

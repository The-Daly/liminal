#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "generated" / "ui"
DEFAULT_OUT = OUT_DIR / "menu_operations_overlay.png"
W, H = 1920, 1080

FRAME = (166, 176, 124, 210)
FILL = (10, 14, 12, 184)
FILL_LIGHT = (18, 22, 19, 196)
TEXT_MAIN = (224, 228, 208, 255)
TEXT_MUTED = (134, 148, 111, 255)
TEXT_ACCENT = (239, 192, 84, 255)

FONT_DIR = Path("C:/Windows/Fonts")
FONT_UI = ImageFont.truetype(str(FONT_DIR / "segoeui.ttf"), 18)
FONT_UI_LARGE = ImageFont.truetype(str(FONT_DIR / "segoeui.ttf"), 26)
FONT_TITLE = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 66)
FONT_HEAD = ImageFont.truetype(str(FONT_DIR / "consolab.ttf"), 28)
FONT_MONO = ImageFont.truetype(str(FONT_DIR / "consola.ttf"), 17)
FONT_MONO_BIG = ImageFont.truetype(str(FONT_DIR / "consolab.ttf"), 44)

BUTTONS = ["deploy", "loadout", "operators", "market", "intel", "settings", "exit"]

PANEL_COPY = {
    "deploy": {
        "title": "OPERATION: SERVICE HALLS",
        "tag": "ZONE // SH-17",
        "feed": "LIVE FEED // LEVEL 1 SERVICE HALLS",
        "body": "Stable route active. Enter the service halls test slice from the menu shell.",
        "metrics": [
            ("THREAT LEVEL", "HIGH", "////"),
            ("EXTRACTION WINDOWS", "00:20-00:30", "00:50-01:00 | 01:20-01:30"),
            ("ENVIRONMENTAL ANOMALY", "DISORIENTATION", "SIGNAL INTERFERENCE"),
            ("RECOMMENDED TEAM SIZE", "1 - 3", "FIELD UNIT"),
            ("BRIEF OBJECTIVE", "INVESTIGATE SERVICE HALLS", "RECOVER DIAGNOSTICS FROM TERM-3 NODE"),
        ],
        "cta": ("DEPLOY", "ENTER ZONE"),
    },
    "loadout": {
        "title": "LOADOUT // FIELD PREP",
        "tag": "KIT // ACTIVE",
        "feed": "CURRENT KIT // STAGING BENCH",
        "body": "Review the prototype kit before deployment. This is the loadout staging panel.",
        "metrics": [
            ("PRIMARY", "M4A1", "5.56 / MID RANGE"),
            ("SIDEARM", "G17", "9MM / BACKUP"),
            ("TACTICAL", "2 SLOTS", "FLASH + FRAG"),
            ("UTILITY", "2 SLOTS", "MEDKIT + LIGHT"),
            ("STATUS", "READY", "NO OVERWEIGHT WARNINGS"),
        ],
        "cta": ("CONFIRM KIT", "RETURN TO OPS"),
    },
    "operators": {
        "title": "OPERATORS // ROSTER",
        "tag": "FACTION // REER",
        "feed": "OPERATOR PROFILE // ACTIVE CHARACTER",
        "body": "Review the active operator identity, faction lock, and current service record.",
        "metrics": [
            ("CALLSIGN", "GHOST-7", "FIELD-CLEARED"),
            ("FACTION", "REER", "LOCKED TO REALM"),
            ("STATUS", "ACTIVE", "LAST LOGIN: TODAY"),
            ("REPUTATION", "TIER III", "RELIANT"),
            ("WIPE", "2-YEAR CYCLE", "NEXT WIPE TRACKED"),
        ],
        "cta": ("VIEW OPERATOR", "RETURN TO OPS"),
    },
    "market": {
        "title": "MARKET // B.N.T.G. ACCESS",
        "tag": "TRADE // LIMITED",
        "feed": "BLACK MARKET // SERVICES",
        "body": "Prototype trader access shell. Spend credits, review barter paths, and track shortages.",
        "metrics": [
            ("CREDITS", "18,420", "AVAILABLE"),
            ("RESEARCH", "450", "HOLDINGS"),
            ("TOKENS", "12", "CONTRACT"),
            ("HOT ITEM", "ALMOND WATER", "STOCK LOW"),
            ("STATUS", "OPEN", "FIELD CHANNEL ACTIVE"),
        ],
        "cta": ("OPEN TRADER", "RETURN TO OPS"),
    },
    "intel": {
        "title": "INTEL // INCIDENT BOARD",
        "tag": "ARCHIVE // LIVE",
        "feed": "MISSION FILES // SIGNAL THREADS",
        "body": "Prototype intel shell. Review objectives, anomalies, and route-specific warning data.",
        "metrics": [
            ("PRIMARY LEAD", "SERVICE HALLS", "ARCHIVE LOSS"),
            ("SECONDARY", "TICKET BOOTH", "HIDDEN EXTRACT"),
            ("ANOMALY", "DISORIENTATION", "PERSISTENT"),
            ("SIGNAL", "DEGRADED", "PARTIAL GAPS"),
            ("THREAT", "UNKNOWN ENTITY", "FLICKER STALKER"),
        ],
        "cta": ("OPEN FILES", "RETURN TO OPS"),
    },
    "settings": {
        "title": "SETTINGS // CONTROL ROOM",
        "tag": "LOCAL // UI",
        "feed": "SYSTEM PREFERENCES // TEST BUILD",
        "body": "Prototype settings shell. Adjust controls, display logic, and audio-state behavior.",
        "metrics": [
            ("DISPLAY", "1920x1080", "WINDOWED TEST"),
            ("INPUT", "KB / CTRL", "ACTIVE"),
            ("AUDIO", "SFX ENABLED", "VOICE LOW"),
            ("BUILD", "V0.1.0", "PROTOTYPE"),
            ("STATUS", "LOCAL PROFILE", "NO CLOUD SAVE"),
        ],
        "cta": ("APPLY SETTINGS", "RETURN TO OPS"),
    },
    "exit": {
        "title": "EXIT // STANDBY",
        "tag": "LOCAL // SAFE",
        "feed": "SESSION CONTROL // TERMINATE",
        "body": "Leave the current play session and return control to the editor.",
        "metrics": [
            ("SESSION", "LOCAL PIE", "ACTIVE"),
            ("SAVE", "FRONTEND STATE", "RETAINED"),
            ("WORLD", "NO LIVE SERVER", "SAFE TO EXIT"),
            ("RETURN", "EDITOR", "IMMEDIATE"),
            ("STATUS", "CONFIRM EXIT", "PRESS ENTER"),
        ],
        "cta": ("EXIT SESSION", "CLOSE PIE"),
    },
}


def panel(draw: ImageDraw.ImageDraw, box, fill=FILL, frame=FRAME, inner_pad=2):
    draw.rounded_rectangle(box, radius=0, outline=frame, width=2, fill=fill)
    inner = (box[0] + inner_pad, box[1] + inner_pad, box[2] - inner_pad, box[3] - inner_pad)
    draw.rectangle(inner, fill=fill)


def txt(draw, xy, text, fill, font_obj, anchor="la"):
    draw.text(xy, text, font=font_obj, fill=fill, anchor=anchor)


def build_state(selected: str) -> Image.Image:
    copy = PANEL_COPY[selected]
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
    y = 250
    for label in BUTTONS:
        highlight = label == selected
        panel(
            draw,
            (40, y, 406, y + 76),
            fill=(44, 31, 10, 205) if highlight else FILL_LIGHT,
            frame=TEXT_ACCENT if highlight else FRAME,
        )
        txt(draw, (72, y + 38), ">>" if highlight else "[]", TEXT_ACCENT if highlight else TEXT_MUTED, FONT_UI_LARGE, anchor="lm")
        txt(draw, (128, y + 38), label.upper(), TEXT_ACCENT if highlight else TEXT_MAIN, FONT_UI_LARGE, anchor="lm")
        y += 96
    txt(draw, (44, 928), "W/S OR CLICK TO NAVIGATE", TEXT_MUTED, FONT_UI)

    panel(draw, (452, 190, 1432, 958))
    txt(draw, (486, 234), copy["title"], TEXT_MAIN, FONT_HEAD)
    panel(draw, (1216, 216, 1380, 258), fill=(16, 20, 16, 190))
    txt(draw, (1298, 237), copy["tag"], TEXT_MUTED, FONT_UI, anchor="mm")

    preview = (484, 278, 1400, 684)
    draw.rounded_rectangle(preview, radius=0, outline=(118, 126, 96, 140), width=2, fill=(8, 11, 9, 52))
    txt(draw, (514, 312), copy["feed"], TEXT_MUTED, FONT_UI)
    txt(draw, (514, 348), copy["body"], TEXT_MAIN, FONT_UI)

    panel(draw, (474, 704, 1404, 854), fill=FILL_LIGHT)
    x = 492
    width = 176
    for head, body, sub in copy["metrics"]:
        txt(draw, (x, 730), head, TEXT_MUTED, FONT_MONO)
        txt(draw, (x, 772), body, TEXT_ACCENT if head in {"THREAT LEVEL", "PRIMARY", "CALLSIGN", "CREDITS", "PRIMARY LEAD", "DISPLAY", "SESSION"} else TEXT_MAIN, FONT_UI)
        txt(draw, (x, 808), sub, TEXT_MUTED, FONT_MONO)
        x += width

    cta_label, cta_sub = copy["cta"]
    panel(draw, (640, 876, 1238, 948), fill=(44, 31, 10, 224), frame=TEXT_ACCENT)
    txt(draw, (939, 905), cta_label, TEXT_ACCENT, FONT_MONO_BIG, anchor="mm")
    txt(draw, (939, 936), cta_sub, TEXT_MAIN, FONT_UI_LARGE, anchor="mm")

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
    txt(draw, (1784, 1018), "ENTER / CLICK TO CONFIRM", TEXT_MUTED, FONT_UI, anchor="rm")

    return image.rotate(-90, expand=True).resize((W, H))


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for state in BUTTONS:
        image = build_state(state)
        image.save(OUT_DIR / f"menu_{state}_overlay.png")
        if state == "deploy":
            image.save(DEFAULT_OUT)


if __name__ == "__main__":
    build()

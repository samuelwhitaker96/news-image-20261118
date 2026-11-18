#!/usr/bin/env python3
"""Render the Wednesday 18 November 2026 world-news front page.

Produces news.png (1024x1024) in this directory using only PIL. The render
is deterministic: no clocks, no random choices, no timestamps in the file,
so re-running it always yields the same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
OUTFILE = "news.png"

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
BOLD = DEJAVU + "DejaVuSans-Bold.ttf"
PLAIN = DEJAVU + "DejaVuSans.ttf"

BG = (250, 246, 238)          # paper
SLATE = (24, 40, 56)          # masthead
GOLD = (197, 148, 52)         # rule under masthead
CARD_BG = (255, 255, 255)
CARD_EDGE = (205, 200, 190)
BODY_GREY = (64, 64, 64)
MUTED = (96, 96, 96)
BLACK = (18, 18, 18)

MASTHEAD = "WEDNESDAY 18 NOVEMBER 2026"
KICKER = "THE DAY IN BRIEF  ·  WORLD NEWS IN ONE IMAGE"

# Five stories, all verified against reporting published on 18 November 2026.
ITEMS = [
    {
        "kicker": "ETHIOPIA  ·  BADME",
        "accent": (24, 110, 96),
        "head": "Ethiopia and Eritrea mass troops at border",
        "deck": "Monitors report shelling and clashes near Badme; who holds the town is disputed.",
        "credit": "Reuters",
    },
    {
        "kicker": "UKRAINE  ·  CRIMEA",
        "accent": (46, 84, 138),
        "head": "New video shows Crimea bridge road span gone",
        "deck": "Footage filmed from a train on 18 Nov shows the road arch gone; rail traffic resumes, road halted.",
        "credit": "Kyiv Independent",
    },
    {
        "kicker": "MIDDLE EAST  ·  GULF",
        "accent": (132, 46, 46),
        "head": "Iran says it targeted US bases in the Gulf",
        "deck": "Tehran says it targeted US installations at Ali Al Salem base; Bahrain intercepted attacks for a third time this week.",
        "credit": "Reuters",
    },
    {
        "kicker": "GAZA  ·  UNITED NATIONS",
        "accent": (90, 96, 40),
        "head": "Board of Peace faults Israel and Hamas",
        "deck": "Trump's Board of Peace tells the UN both sides failed their commitments; the ceasefire is in danger.",
        "credit": "Reuters",
    },
    {
        "kicker": "BANGLADESH  ·  DHAKA",
        "accent": (120, 70, 140),
        "head": "Paramilitary deployed as Hasina's return looms",
        "deck": "Hundreds of troops deployed nationwide; bomb blasts and arson in at least 28 districts, one killed.",
        "credit": "Reuters",
    },
]

ALSO_LINE = (
    "ALSO:  Trump lands in Shenzhen ahead of talks with Xi and Putin; "
    "Nvidia beats forecasts; GTA VI launches tomorrow.  —  Reuters"
)
NOTE_LINE = "All events happened or were first reported on 18 November 2026. Claims are labelled as claims."
CREDIT_LINE = "Sources: Reuters  ·  Kyiv Independent"


def load(path, size):
    return ImageFont.truetype(path, size)


def split_lines(canvas, text, face, width):
    """Break text into lines that fit `width` pixels, word by word."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if canvas.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def centred(canvas, text, face, y, colour):
    w = canvas.textlength(text, font=face)
    canvas.text(((CANVAS_W - w) / 2, y), text, font=face, fill=colour)


def draw_card(canvas, item, top, left, right, height):
    canvas.rectangle([left, top, right, top + height],
                     fill=CARD_BG, outline=CARD_EDGE, width=1)
    canvas.rectangle([left, top, left + 8, top + height], fill=item["accent"])
    text_x = left + 26
    text_w = right - text_x - 16
    tag_face = load(BOLD, 19)
    head_face = load(BOLD, 29)
    deck_face = load(PLAIN, 20)
    credit_face = load(PLAIN, 17)

    canvas.text((text_x, top + 11), item["kicker"], font=tag_face,
                fill=item["accent"])
    credit = "Source: " + item["credit"]
    cw = canvas.textlength(credit, font=credit_face)
    canvas.text((right - 16 - cw, top + 13), credit, font=credit_face,
                fill=MUTED)

    head = split_lines(canvas, item["head"], head_face, text_w)
    assert len(head) == 1, "headline must fit on one line: %r" % item["head"]
    canvas.text((text_x, top + 40), head[0], font=head_face, fill=BLACK)

    deck = split_lines(canvas, item["deck"], deck_face, text_w)
    assert len(deck) <= 2, "deck too long: %r" % item["deck"]
    row = top + 76
    for line in deck:
        canvas.text((text_x, row), line, font=deck_face, fill=BODY_GREY)
        row += 25


def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    c = ImageDraw.Draw(img)

    # Masthead band.
    c.rectangle([0, 0, CANVAS_W, 116], fill=SLATE)
    centred(c, MASTHEAD, load(BOLD, 54), 16, (255, 255, 255))
    centred(c, KICKER, load(PLAIN, 22), 82, (198, 204, 214))
    c.rectangle([0, 116, CANVAS_W, 122], fill=GOLD)

    # Story cards, one column.
    left, right = 36, 988
    card_h, gap = 132, 10
    y = 138
    for item in ITEMS:
        draw_card(c, item, y, left, right, card_h)
        y += card_h + gap

    # Also strip.
    strip_top = y + 2
    c.rectangle([left, strip_top, right, strip_top + 62], fill=SLATE)
    also_face = load(PLAIN, 20)
    lines = split_lines(c, ALSO_LINE, also_face, right - left - 32)
    assert len(lines) <= 2, "also strip too long"
    row = strip_top + 8
    for line in lines:
        c.text((left + 16, row), line, font=also_face, fill=(255, 255, 255))
        row += 24

    # Footer notes.
    foot_face = load(PLAIN, 16)
    fy = strip_top + 76
    centred(c, NOTE_LINE, foot_face, fy, MUTED)
    centred(c, CREDIT_LINE, foot_face, fy + 23, MUTED)

    img.save(OUTFILE, "PNG", optimize=True)
    print("wrote", OUTFILE)


if __name__ == "__main__":
    build()

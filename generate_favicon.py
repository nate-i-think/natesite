#!/usr/bin/env python3
"""
Generate animated favicon PNG frames for nathanmyers.co

Produces 7 frames: N, A, T, H, A, N, [blank]
Each letter is centered by its actual ink bounds (not cell metrics).

Output: assets/img/favicon/frame-0.png through frame-6.png
Usage:  python generate_favicon.py
Needs:  pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Pillow not found. Run: pip install Pillow")

from pathlib import Path

# -- Config -------------------------------------------------------------------

FONT_PATH     = Path("fonts/BigBlueTerm437NerdFontMono-Regular.ttf")
OUTPUT_DIR    = Path("assets/img/favicon")
CANVAS        = 64                    # px, square
PADDING       = 8                     # px each side
CORNER_RADIUS = 12                    # px
BG            = (35,  8,   8,  255)   # --crt body background
TEXT_COLOR    = (255, 225, 120, 255)  # --crt-core amber

# Fine-tuning: nudge text position after centering (+ = right/down)
X_ADJUST      = 0
Y_ADJUST      = 0

LETTERS = list("NATHAN")

# -- Helpers ------------------------------------------------------------------

def ink_bbox(font, text):
    """Tight bounding box of rendered ink (not cell metrics)."""
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    return probe.textbbox((0, 0), text, font=font)

def largest_fitting_font(font_path, text, max_w, max_h):
    """Largest font size where the ink of `text` fits within max_w x max_h."""
    for size in range(200, 4, -1):
        font = ImageFont.truetype(str(font_path), size)
        bb = ink_bbox(font, text)
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]
        if w <= max_w and h <= max_h:
            return font
    return ImageFont.truetype(str(font_path), 5)


def make_frame(letter, font):
    """Single letter centered by ink bounds in a rounded dark square."""
    img  = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))

    # Rounded-corner background
    bg   = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle([0, 0, CANVAS - 1, CANVAS - 1],
                           radius=CORNER_RADIUS, fill=BG)
    img = Image.alpha_composite(img, bg)

    # Center by ink bounds: place anchor so ink is exactly centered
    draw  = ImageDraw.Draw(img)
    bb    = draw.textbbox((0, 0), letter, font=font)
    ink_w = bb[2] - bb[0]
    ink_h = bb[3] - bb[1]
    x = (CANVAS - ink_w) // 2 - bb[0] + X_ADJUST
    y = (CANVAS - ink_h) // 2 - bb[1] + Y_ADJUST

    draw.text((x, y), letter, font=font, fill=TEXT_COLOR)
    return img


def make_blank():
    """Empty frame: just the rounded dark background."""
    img  = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    bg   = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    draw.rounded_rectangle([0, 0, CANVAS - 1, CANVAS - 1],
                           radius=CORNER_RADIUS, fill=BG)
    return Image.alpha_composite(img, bg)


# -- Main ---------------------------------------------------------------------

def main():
    if not FONT_PATH.exists():
        raise SystemExit("Font not found: %s" % FONT_PATH)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    max_w = CANVAS - 2 * PADDING
    max_h = CANVAS - 2 * PADDING

    # Size to fit 'M' (typically widest in monospace), constrained by ink bounds
    font = largest_fitting_font(FONT_PATH, "M", max_w, max_h)

    bb = ink_bbox(font, "M")
    print("Canvas: %dx%dpx  |  'M' ink: %dx%dpx" % (
        CANVAS, CANVAS, bb[2]-bb[0], bb[3]-bb[1]))

    # Letter frames
    for i, letter in enumerate(LETTERS):
        img      = make_frame(letter, font)
        filename = "frame-%d.png" % i
        img.save(OUTPUT_DIR / filename)
        print("  saved %s  (%s)" % (filename, letter))

    # Blank frame (breaks up N...N at loop boundary)
    blank = make_blank()
    blank.save(OUTPUT_DIR / ("frame-%d.png" % len(LETTERS)))
    print("  saved frame-%d.png  (blank)" % len(LETTERS))

    print("\nDone -- %d frames in %s" % (len(LETTERS) + 1, OUTPUT_DIR))
    print("To nudge position, adjust X_ADJUST / Y_ADJUST at the top of this script.")


if __name__ == "__main__":
    main()

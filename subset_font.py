#!/usr/bin/env python3
"""
Subset BigBlueTerm font to only include characters actually used on the site.
Outputs a compressed WOFF2 file.

Usage: python subset_font.py

Requires: pip install fonttools brotli
"""

from fontTools.subset import main as subset
import sys

# Source and output paths
INPUT_FONT = "fonts/BigBlueTerm437NerdFontMono-Regular.ttf"
OUTPUT_FONT = "fonts/BigBlueTerm-subset.woff2"

# Character set to include
CHARS = "".join([
    # Basic ASCII
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~",

    # Curly quotes and apostrophes
    "\u2018\u2019",  # ' '
    "\u201C\u201D",  # " "

    # Dashes
    "\u2013",  # en-dash –
    "\u2014",  # em-dash —

    # Common symbols
    "\u00A9",  # ©
    "\u00AE",  # ®
    "\u2122",  # ™
    "\u2026",  # …
    "\u00B0",  # °
    "\u2022",  # •
    "\u00D7",  # ×
    "\u00F7",  # ÷
    "\u00B1",  # ±

    # Accented Latin uppercase
    "\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5",  # ÀÁÂÃÄÅ
    "\u00C6\u00C7",                          # ÆÇ
    "\u00C8\u00C9\u00CA\u00CB",              # ÈÉÊË
    "\u00CC\u00CD\u00CE\u00CF",              # ÌÍÎÏ
    "\u00D0\u00D1",                          # ÐÑ
    "\u00D2\u00D3\u00D4\u00D5\u00D6\u00D8",  # ÒÓÔÕÖØ
    "\u00D9\u00DA\u00DB\u00DC",              # ÙÚÛÜ
    "\u00DD\u00DE",                          # ÝÞ

    # Accented Latin lowercase
    "\u00DF",                                # ß
    "\u00E0\u00E1\u00E2\u00E3\u00E4\u00E5",  # àáâãäå
    "\u00E6\u00E7",                          # æç
    "\u00E8\u00E9\u00EA\u00EB",              # èéêë
    "\u00EC\u00ED\u00EE\u00EF",              # ìíîï
    "\u00F0\u00F1",                          # ðñ
    "\u00F2\u00F3\u00F4\u00F5\u00F6\u00F8",  # òóôõöø
    "\u00F9\u00FA\u00FB\u00FC",              # ùúûü
    "\u00FD\u00FE\u00FF",                    # ýþÿ
])

if __name__ == "__main__":
    print(f"Subsetting {INPUT_FONT}...")
    print(f"Including {len(CHARS)} characters")

    sys.argv = [
        "",
        INPUT_FONT,
        f"--output-file={OUTPUT_FONT}",
        "--flavor=woff2",
        f"--text={CHARS}",
    ]
    subset()

    import os
    size = os.path.getsize(OUTPUT_FONT)
    print(f"Created {OUTPUT_FONT} ({size:,} bytes)")

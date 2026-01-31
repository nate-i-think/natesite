# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
bundle.bat install      # Install Ruby dependencies (use .bat on Windows/Cygwin)
jekyll serve            # Dev server at localhost:4000 (auto-rebuilds on changes)
python generate_noise.py  # Regenerate noise texture if needed
```

## Project Structure

```
/
├── _layouts/
│   └── default.html      # Base template with SVG filter, typewriter JS, lightbox
├── _site/                # Generated static output (do not edit)
├── assets/
│   ├── css/
│   │   └── style.css     # All styling
│   └── img/
│       ├── noise.png     # 64x64 tileable dither texture
│       └── mogging1.jpeg # Profile image
├── fonts/
│   └── VT323-Regular.ttf # Terminal monospace font
├── index.md              # Homepage content (two-column layout)
├── _config.yml           # Jekyll config (kramdown markdown)
├── Gemfile               # Dependencies (Jekyll 4.3 only)
└── generate_noise.py     # Noise texture generator script
```

## Architecture

Jekyll static site with 1970s amber CRT monitor aesthetic.

### Visual System

- **Font**: VT323 monospace (24px desktop, 18px mobile)
- **Color palette** (CSS custom properties):
  - `--crt-core`: RGB(255, 225, 120) - bright yellow center glow
  - `--crt-mid`: RGB(255, 176, 0) - amber main text (#ffb000)
  - `--crt-edge`: RGB(180, 60, 0) - dark red-orange outer bloom
- **Text glow**: 7-layer text-shadow creating phosphor bloom effect
- **Scanlines**: Soft gradient overlay (4px cycle, 0.12 opacity peak)
- **Noise dither**: Tileable PNG overlay (0.04 opacity) to reduce banding

### CRT Image Filter

SVG filter in `default.html` converts images to CRT style:
1. Grayscale with core yellow tint (255, 225, 120)
2. Posterization to 10 tonal levels
3. Gaussian blur bloom shifted to red-orange
4. Screen-mode blending
5. Edge feathering (blur alpha + remap for smooth glow blend)

Apply with class: `<img class="crt-image">`

CSS adds drop-shadow glow (amber inner, red-orange outer).

### Lightbox

Click any `.crt-image` to view full-color version:
- Dark overlay (90% black) with fade-in animation
- Image scales up from 85% to 100%
- Click outside or press Escape to close
- Respects `prefers-reduced-motion`

### Two-Column Layout

For profile/about pages, use the layout wrapper:
```html
<div class="about-layout">
  <div class="about-text" markdown="1">
    <!-- Markdown content here -->
  </div>
  <div class="about-image">
    <img src="..." class="crt-image profile-image">
  </div>
</div>
```

- `.about-layout`: Flexbox, centered, max-width 1100px
- `.about-text`: Constrained to 500px
- `.profile-image`: 525px width
- Stacks vertically on mobile (<900px)

### Typewriter Animation

Embedded JS in `default.html`:
- Character-by-character text reveal (~15 chars/frame)
- Blinking cursor follows text, stays inline with content
- Skip with click or keypress
- Respects `prefers-reduced-motion`

## Adding Pages

Create markdown file with front matter:
```yaml
---
layout: default
title: Page Title
---
```

## Important

Do NOT change CRT effect values without asking first:
- Phosphor colors and opacity layers
- Glow radius values
- Edge feather settings (stdDeviation, slope, intercept)
- Scanline intensity/spacing
- Animation timing

These have been carefully tuned for visual authenticity.

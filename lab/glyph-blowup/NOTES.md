# Blowing U+F169F up into character art

The glyph the loading screen wants is the surrogate pair `󱚟`,
i.e. **U+F169F**, a Nerd Fonts Private Use Area rune: a robot head with an
antenna, two round eyes, ear tabs, and an exclamation-and-question mark
floating off its right shoulder.  Everything here is that one rune, redrawn
at 4, 6, 8 and 12 rows tall out of characters instead of one PUA codepoint.

Nothing in here touches `go/` or `bin/`.  It is art plus the two scripts
that made it and check it.

## What is in this directory

| file | what it is |
|---|---|
| `gen.py` | renders the rune from a Nerd Font and packs it into art |
| `preview.py` | rasterises art at terminal cell size for inspection |
| `preview.png` | contact sheet: source glyph over the main variants |
| `source.png` | the rune's mask as rendered, for that comparison |
| `show.sh` | cats every variant to your terminal, labelled |
| `{full,head}-{braille,half}-{4,6,8,12}r.txt` | the art |

Variant naming:

- **full** — the whole rune downsampled, `!?` marks and all.
- **head** — the head only, with `!?` set as two literal characters at the
  top right.  The marks in the source are *already type*; at four rows a
  bitmapped `?` is three columns of noise, whereas a real `?` is a real `?`.
  This is the fastfetch trick of mixing bitmap and glyph in one logo.
- **braille** — U+2800–28FF, 2x4 dots per cell, the detail tier.
- **half** — U+2580/2584/2588, 1x2 subpixels per cell, the solid tier.

## The two numbers that matter

**Aspect.**  Terminal cells are tall, so a square-ish logo needs more
columns than rows or it comes out squashed.  Measured rather than assumed:
Hack Nerd Font Mono at size 100 advances 60.20px per cell over a 117px
line, h/w = 1.943; the rune's own ink box is 470x427, h/w = 0.9085.  So

    columns = rows * 1.943 / 0.9085 = 2.14 * rows

4 rows -> 9 columns, 8 rows -> 17.  `gen.py` computes this per source, so
the head-only crop (a different ink box) gets its own figure.

**Threshold.**  The eyes are negative space, and negative space is the
first thing a careless threshold eats.  Coverage is box-averaged from an 8x
supersample, then cut at 0.5, which keeps both eyes open at four rows in
both tiers.  A 0.35/0.5/0.65 sweep at 4 and 6 rows showed 0.35 thickening
the silhouette (the antenna and the `!?` blur into blobs) and 0.65 thinning
it (the antenna stalk breaks up); 0.5 sat between them with the eyes intact
at every size.  Sweep it yourself rather than taking that on trust:

    python3 gen.py 4 half 0.35
    python3 gen.py 4 braille 0.65

## Font coverage — the thing to know before shipping either tier

Checked with fontTools against the cmap of the fonts on this box:

| font | U+2800 braille | U+2580/2584 half blocks | U+F169F |
|---|---|---|---|
| Hack Nerd Font | **no** | yes | yes |
| JetBrainsMono Nerd Font Mono | **no** | yes | yes |
| Adwaita Mono, Symbola | yes | yes | no |

Patching a font with Nerd Font icons does **not** give it braille.  Braille
renders anyway because the terminal falls back to some other installed
font — at that other font's weight and metrics, which is exactly how
braille art ends up with seams or a different colour to the text beside it.
Half blocks live in the same Block Elements range as the `█` the TUTOR
wordmark is already built from, so they are proven on any machine the
wordmark already works on.

Coverage on the shipped audience's machines — stock macOS with SF Mono,
Menlo, or Monaco — is **not** verified by any of the above; this box is
Linux.  Verify there before choosing braille for anything that ships.
Display width is not a differentiator: `charWidth` (go/render.go) returns 1
for both ranges.

## Regenerating and checking

    python3 gen.py                      # rewrite every art file
    python3 gen.py 6 braille 0.5        # one-off to stdout
    bash show.sh                        # look at them in your terminal
    python3 preview.py preview.png "source U+F169F:source.png@8" \
        head-braille-8r:head-braille-8r.txt

`preview.py` draws the art at a real terminal cell size (~12px) and then
magnifies the whole sheet, rather than drawing it large in the first place:
blocky-when-huge and legible-in-a-terminal are different properties, and
only the second one matters.  It previews in Adwaita Mono because the Nerd
Fonts here cannot draw braille (above).  A spec of the form
`label:source.png@ROWS` pastes the source mask into the sheet scaled to the
pixel height ROWS of art occupies, so the comparison is like for like;
`gen.py` writes `source.png` on every no-args run.

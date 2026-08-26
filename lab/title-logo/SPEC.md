# Title-screen robot logo — specification

Replaces the single Nerd Font crest rune above the TUTOR wordmark with a
9-row x 20-column half-block robot logo placed to the LEFT of the wordmark,
with the wordmark vertically centred against it. This document is complete:
an implementer should not need to make any design decision. The art files in
this directory are the source of truth for the literal characters — copy
them, do not retype them by eye.

Files here:

- `robot-primary.txt` — half-block tier, 9 rows x 20 columns
- `robot-fallback.txt` — printable-ASCII tier, 9 rows x 20 columns
- `measure.py` — verification script (see "Verification" at the end)

---

## 1. Recon findings (ground truth as of this spec)

All in `go/splash.go` unless noted. The splash is NOT a Bubble Tea/lipgloss
view — it is plain `fmt.Println` text written to stdout by `printSplash`
before raw mode and before the alternate screen, so it lands in ordinary
shell scrollback. Composition is string concatenation; `go.mod` has zero
dependencies. There is no Python counterpart: `tui/` has no splash module
and `bin/parity.sh` does not cover the launch screen — the Go side is the
only implementation. `bin/banner-preview.sh:122-141` is a shell mirror for
eyeballing that hardcodes the old robot as UTF-8 bytes
(`printf '\xf3\xb1\x9a\xa0'`, line 139); it must receive the new art too.

- **Wordmark**: per-letter table `glyphs` (T, U, O, R), each letter 8 cols x
  5 rows, built from space and `█` U+2588 FULL BLOCK only. Assembled by
  `artworkRowPlain(row)` / `artworkRowColored(row)`: one leading space, then
  the five letters of `word` joined by 3-space gaps. 5 rows tall, every row
  exactly `splashWidth = 53` display columns; visible letters occupy columns
  2–53 of that field.
- **Current glyph**: `robotRune = '\U000F16A0'` (nf-md-robot-confused, a
  Nerd Fonts Private Use Area codepoint), a single 1-column rune centred on
  its own line ABOVE the wordmark, coloured 81 bold. This is the
  "minuscule" element being replaced. On a stock Mac without a Nerd Font it
  is tofu; `packaging/README.md:107-109` documents `TUTOR_ASCII=1` as the
  hatch that hides it.
- **Colour**: raw SGR 256-colour via `colorRun(text, color int, bold bool)`
  emitting `\x1b[38;5;Nm` / `\x1b[1;38;5;Nm`, gated on `noColor`
  (`$NO_COLOR`). Palette: `headColors = {81,115,150,215,209}` bold, one per
  letter left to right; `tailColors` reversed for the subtitle sweep;
  `tagColor = 81`. All values also exist in `styles` (go/term.go): 81=h1,
  115=h3, 150=h4, 215=code fg, 209=warn.
- **Width logic**: `detectWidth()` defaults to 80 on error;
  `splashLines(width)` switches to a plain-text fallback below
  `narrowThreshold = 55`. Height is NOT a constraint — this is scrollback
  output, not an alternate-screen layout; the screen may grow by a few
  lines freely. The budget is horizontal: 80 columns by default.
- **Width measurement**: `charWidth` (go/render.go:46-57) is a wide-ranges
  table — anything not listed returns 1. `width_table.go` contains no range
  overlapping U+2580–259F or U+2800–28FF, and `bin/gen-width.py:38-39`
  counts East Asian "A" (Ambiguous) as width 1. So half blocks, shade
  blocks, quadrants AND braille all measure exactly 1 column in both
  implementations. Width is therefore NOT a differentiator between
  techniques; the choice is made on legibility and font coverage alone.
- **Stated constraints**: the shipped audience is non-developer Mac users on
  default terminals (ZIP download, no git). The old crest's Nerd Font
  assumption leaned on a mid-course article
  (content/03-the-cli/13-powerline-themes.md), but the splash shows at
  FIRST launch, before any lesson. This design removes the Nerd Font
  dependency entirely.
- **Repo precedent**: block elements already ship and are proven on target
  machines — `█` U+2588 in the wordmark itself, `▌` U+258C and `░` U+2591
  elsewhere in the repo. There is zero braille precedent anywhere.

## 2. Technique choice

Decided on legibility and font coverage (width is a non-issue, above), for
stock macOS Terminal.app and iTerm2 with default fonts (SF Mono / Menlo /
Monaco):

- **Half blocks (▀ U+2580, ▄ U+2584, █ U+2588) — CHOSEN as primary.**
  1x2 subpixels per cell turn the 20x9 cell budget into a 20x18 subpixel
  grid with approximately square subpixels (cells are ~1:2), so the art has
  no aspect distortion. Solid fill matches the wordmark's own █ mass
  exactly. The decisive property: the logo is drawn from the same Block
  Elements repertoire the repo already ships and proves at runtime (█ in
  the wordmark, ▌ and ░ elsewhere), so it cannot fail to render anywhere
  the wordmark succeeds. That one property dissolves the font-detection
  problem and the tier-selection problem together. Marginal risk over the
  shipped screen is exactly two codepoints, U+2580/U+2584, in the same
  Block Elements range, present in SF Mono, Menlo, Monaco, and Hack.
- **Quadrant blocks (U+2596–259F) — REJECTED.** The natural step up if more
  resolution were needed, but 20x18 subpixels is already ample for head,
  eyes, antenna, torso panel, arms and feet; quadrants would only double
  horizontal resolution while stepping outside the proven repertoire
  (quadrant coverage in Apple's stock monospace fonts is uncertain, and a
  fallback-font substitution risks mismatched glyph metrics — ragged fill).
  No needed benefit, nonzero risk.
- **Braille (U+2800–28FF) — REJECTED, burden not met.** Highest resolution
  (40x18 dots at this size), but: zero braille precedent in the repo; none
  of Apple's default monospace fonts covers the braille block, so macOS
  falls back to Apple Braille, which is not metrically matched to the
  terminal font and renders unraised dot positions as faint hollow rings —
  the well-known "dot haze" on braille-graph TUIs on Macs; and even
  rendering perfectly, braille is a dot matrix that cannot match the solid
  mass of a █-built wordmark sitting 3 columns away. The user's phrase
  "braille-like" describes density, not codepoints — half blocks at 20x18
  deliver the density. Would not ship it.
- **Box drawing / shade (░▒▓ ─│┌┐) — REJECTED as primary.** Outline or
  texture only; cannot match the wordmark's fill. The ASCII tier covers the
  bulletproof role.
- **Plain ASCII — kept as the explicit-opt-in fallback tier** (section 5).

## 3. Dimensions

- **Robot: 9 rows x 20 display columns** (both tiers identical in size).
  Drawn on a 20x18 subpixel grid — 180 cells of ink budget.
- **Gutter: 3 columns** between the robot's right edge and the wordmark
  field (the field's own 1-column leading margin makes the visible gap to
  the letters 4 columns, comfortably wider than the 3-column inter-letter
  gap, so the robot cannot read as a sixth letter).
- **Composed block: 76 columns x 9 rows** (20 + 3 + 53), inside the
  80-column default with margin to spare. The wordmark stays 5 rows and is
  vertically centred: it occupies composed rows 2–6 (0-indexed), with two
  blank 53-space filler rows above (rows 0–1) and two below (rows 7–8).
- Height cost: the full screen grows from ~10 printed lines to 13
  (blank, 9 composed rows, blank, subtitle, version). Free — this is
  scrollback, not a fixed-height layout.

## 4. The art

`robot-primary.txt` (half blocks; the FILE is the source of truth, shown
here for review — note rows carry trailing spaces to exactly 20 columns):

```
        ████        
  ▄▄▄▄▄▄▄██▄▄▄▄▄▄▄  
  ███▀▀▀████▀▀▀███  
  ███   ████   ███  
  ████▀▀▀▀▀▀▀▀████  
  ▀▀▀▀▀▀████▀▀▀▀▀▀  
██  ████▀▀▀▀████  ██
▀▀  ████▄▄▄▄████  ▀▀
     ▄███  ███▄     
```

Anatomy: antenna bulb (row 0) on a stem merging into the head top (row 1);
16-wide solid head with two 3x3-subpixel dark eyes (rows 2–3) and an
8-subpixel-wide mouth slot (row 4); head bottom edge and neck (row 5);
12-wide torso with a dark 4x4 chest panel and two detached 2-wide arms at
the sides (rows 6–7); two out-turned feet (row 8).

It is generated, not hand-drawn, from this 20x18 pixel grid (`#` = lit),
packing pixel rows 2k/2k+1 per output row as ▀ (top only), ▄ (bottom only),
█ (both), space (neither) — regenerate rather than hand-edit if the design
ever changes:

```
........####........   p0  antenna bulb
........####........   p1  antenna bulb
.........##.........   p2  antenna stem
..################..   p3  head top
..################..   p4  head fill
..###...####...###..   p5  eyes (3x3 dark)
..###...####...###..   p6  eyes
..###...####...###..   p7  eyes
..################..   p8  head fill
..####........####..   p9  mouth slot
..################..   p10 head bottom
........####........   p11 neck
##..############..##   p12 shoulders + arms
##..####....####..##   p13 torso panel + arms
##..####....####..##   p14 torso panel + arms
....############....   p15 torso bottom
......###..###......   p16 legs
.....####..####.....   p17 feet
```

`robot-fallback.txt` (printable ASCII only, same 9x20 box, same anatomy at
the same coordinates — bulb over stem, boxed head with `[o]` eyes at
columns 5–7/12–14 matching the primary's eyes, `====` mouth, torso with
`[##]` panel, side arms, two feet):

```
        (__)        
         ||         
  .--------------.  
  |  [o]    [o]  |  
  |     ====     |  
  '--------------'  
 __ .----------. __ 
|  ||   [##]   ||  |
'--' '--'  '--' '--'
```

Repertoire is pure printable ASCII (0x20–0x7E): it can never render as tofu
in any terminal that can show the subtitle text.

No third robot variant exists: below the logo threshold (section 6) the
robot is dropped entirely, not shrunk — a small robot in a cramped terminal
would recreate the "tiny smudge" failure this redesign removes.

## 5. Tier rule

Runtime font detection is impossible from a TUI (the existing code comments
establish this), so the rule uses none:

- **Default: primary (half-block) tier.** Repertoire {space, ▀, ▄, █} —
  guaranteed to render anywhere the wordmark itself renders, which is the
  strongest guarantee available without detection.
- **`TUTOR_ASCII` set to any non-empty value: ASCII tier.** This CHANGES
  the hatch's behaviour from "hide the robot" to "draw the robot in plain
  ASCII". The variable keeps a reason to exist: it remains the one explicit
  user-side override for any environment where block glyphs render badly
  (mismatched fallback-font metrics, exotic terminals, personal taste), and
  its guarantee is now stronger — a robot that cannot tofu, instead of no
  robot. `packaging/README.md:107-109` must be reworded; replacement copy:

  > If the robot beside the TUTOR wordmark on the launch screen looks
  > broken or misaligned, run `TUTOR_ASCII=1 tutor` — it redraws the robot
  > in plain characters and leaves everything else exactly as it was.

  (The old copy's "shows up as an empty box" no longer applies: the new art
  cannot tofu where the wordmark renders.)
- `NO_COLOR` stays orthogonal: strips colour from whichever tier is active
  (Plain forms), exactly as today.

## 6. Composition (function-level, against go/splash.go names)

Art lives as literal tables inside `splash.go`, in the same shape as the
existing `glyphs` table. Do NOT use `go:embed` pointing at
`lab/title-logo/` — `install.sh` strips authoring machinery from shipped
copies; this directory is provenance and a transcription source only.

New data, transcribed verbatim from the art files (keep every trailing
space; each string is exactly 20 runes; re-run `measure.py` after
transcription — the ▀▄█ characters may appear literally in Go source, as █
already does in `glyphs`; the escape-only discipline applied to the PUA
rune because a mangled PUA codepoint is invisible to the eye, which is not
true of these):

```go
// robotArt is the half-block robot, 9 rows x 20 columns. Source of truth:
// lab/title-logo/robot-primary.txt.
var robotArt = [9]string{ ... }

// robotAscii is the plain-ASCII robot, same box. Source of truth:
// lab/title-logo/robot-fallback.txt.
var robotAscii = [9]string{ ... }

func robotRow(row int) string {
    if asciiOnly { return robotAscii[row] }
    return robotArt[row]
}
```

Constants:

```go
// composedWidth is the logo screen's row width: a 20-column robot, a
// 3-column gutter, and the 53-column wordmark field.
const composedWidth = 76 // 20 + 3 + splashWidth

// logoThreshold is the terminal width at and above which the robot is
// shown beside the wordmark; 76 fits exactly, and detectWidth's 80-column
// fallback clears it.
const logoThreshold = 76

// wordmarkTopRow is the composed row (0-indexed, of 9) on which the
// 5-row wordmark starts, centring it against the 9-row robot.
const wordmarkTopRow = 2
```

`splashWidth = 53`, `narrowThreshold = 55`, `subtitle`, `subtitleIndent = 5`
all stay as they are (the mid screen still uses them unchanged).

Row assembly — `artworkRowPlain` / `artworkRowColored` stay UNCHANGED:

```go
func composedRowPlain(row int) string { // row 0..8
    right := strings.Repeat(" ", splashWidth)
    if row >= wordmarkTopRow && row < wordmarkTopRow+5 {
        right = artworkRowPlain(row - wordmarkTopRow)
    }
    return robotRow(row) + "   " + right
}

func composedRowColored(row int) string {
    right := strings.Repeat(" ", splashWidth)
    if row >= wordmarkTopRow && row < wordmarkTopRow+5 {
        right = artworkRowColored(row - wordmarkTopRow)
    }
    return colorRun(robotRow(row), robotColors[row], true) + "   " + right
}
```

The filler rows are full 53-space strings, deliberately: every one of the 9
composed rows then measures exactly `composedWidth` (76), so the layout
test stays a single uniform assertion. (Trailing spaces printed to a
terminal are harmless.)

Logo-screen text lines below the block:

- Subtitle: the wordmark's visible letters now start at column 25
  (20 robot + 3 gutter + 1 field margin + 1), shifted right by 23 from
  today's column 2, so the subtitle keeps its position relative to the
  wordmark with `strings.Repeat(" ", subtitleIndent+23)` — i.e. indent 28.
- Version tag: right edge at column 76 = the wordmark's right edge:
  `strings.Repeat(" ", composedWidth-dwidth(versionTag())) + versionTag()`
  (clamped at 0 like today's `versionPad`).

Width switch — `splashLines(width)` becomes three-way. Do NOT raise
`narrowThreshold`: demoting 55–75-column terminals to the plain-text
fallback would be a new bug shipped with the fix.

| terminal width | screen |
|---|---|
| `width >= 76` | **logo screen**, 13 lines: `""`, 9 x `composedRowColored`, `""`, subtitle at indent 28, version right-aligned to column 76 |
| `55 <= width < 76` | **mid screen**: exactly today's full screen minus the crest lines — `""`, 5 x `artworkRowColored`, `""`, subtitle at indent 5, version right-aligned to column 53. No robot; the band is too narrow for one that is not a smudge. |
| `width < 55` | **narrow screen**: today's narrow fallback WITHOUT any glyph line — word, narrow subtitle, version tag |

Vertical alignment inside the logo screen is fixed by `wordmarkTopRow`; the
implementer computes nothing.

**Deletions**: `robotRune`, `robotGlyph`, `glyphPad`, `glyphLinePlain`,
`glyphLineColored`, `narrowGlyphLinePlain`, `narrowGlyphLineColored`, and
the old glyph + spacer lines in `fullSplash*` / `narrowSplash*`. The
`asciiOnly` variable stays — it now selects the tier. After this change the
binary contains no Private Use Area codepoint and no Nerd Font dependency;
the splash's rune set is printable ASCII plus U+2580/U+2584/U+2588. Update
the package comment and the crest comment block accordingly.

**Also update** `bin/banner-preview.sh:122-141`: replace the hardcoded
`printf '\xf3\xb1\x9a\xa0'` crest (line 139) with the 9 new art rows
composed per this section, so the preview mirrors the shipped screen.

## 7. Colour

Two-tone, both values already in the splash palette, applied identically to
both tiers via `composedRowColored`:

```go
// robotColors is one colour per robot row, bold, mirroring how headColors
// works for the wordmark: row 0 is the antenna bulb — the robot's "power
// light", warn amber; the rest is chassis in the same cyan as the T beside
// it, so the robot begins the wordmark's left-to-right 81->209 sweep and
// the bulb echoes the sweep's far end.
var robotColors = [9]int{209, 81, 81, 81, 81, 81, 81, 81, 81}
```

- Chassis (rows 1–8): **256-colour 81, bold** — identical to `tagColor`,
  `h1`, and `headColors[0]`.
- Antenna bulb (row 0): **256-colour 209, bold** — `warn` amber. (The eyes
  and chest panel cannot carry an accent: they are negative space — unlit
  subpixels — by design.)
- `noColor` → Plain forms, no SGR, as everywhere else on this screen.
- **Not adaptive light/dark**: the codebase uses fixed 256-colour indices
  throughout, with no adaptivity mechanism; both values are already proven
  against reader backgrounds by the wordmark and warnings.

## 8. Test changes — all seven tests in go/splash_test.go, one by one

1. `TestSplashRuneWhitelist` (68-78) — BROKEN (glyph-line calls removed;
   new runes). Replace: `splashRunes` drops `'\U000F16A0'`, gains
   `'▀': "U+2580 UPPER HALF BLOCK"` and `'▄': "U+2584 LOWER HALF BLOCK"`
   (█ stays). Check the 9 `composedRowPlain` rows in BOTH tier states
   (flip `asciiOnly` directly with defer-restore, the established
   pattern); keep the subtitle/word/version checks; drop glyph-line
   checks.
2. `TestBlockCharWidth` (88-92) — KEPT, EXTENDED: also assert
   `charWidth('▀') == 1` and `charWidth('▄') == 1` (both East Asian
   Ambiguous — the same silent-doubling trap the test already documents
   for █).
3. `TestSplashLayout` (98-110) — BROKEN (rows are no longer all 53).
   Replace: all 9 `composedRowPlain` rows measure `composedWidth` (76) in
   both tier states; the logo-screen version line measures 76; the mid
   screen's 5 `artworkRowPlain` rows and its version line still measure
   `splashWidth` (53).
4. `TestGlyphCodepoint` (118-129) — DELETE: the codepoint it pins no
   longer exists anywhere in the program.
5. `TestGlyphCharWidth` (138-142) — DELETE: same reason.
6. `TestGlyphLineCentred` (153-171) — DELETE: there is no glyph line; the
   robot's vertical placement is covered by a new assertion that
   `composedRowPlain(wordmarkTopRow+k)` has suffix `artworkRowPlain(k)`
   for k in 0..4 and that rows 0,1,7,8 end in 53 spaces.
7. `TestAsciiOnlySuppressesGlyph` (184-215) — BROKEN by design (the hatch
   now swaps tiers instead of suppressing). Replace with
   `TestAsciiOnlySwapsTier`: with `asciiOnly = true`, every composed row
   is pure printable ASCII and still 76 columns; the narrow screen
   contains no robot in either state; and the mid screen is byte-identical
   in both states (the hatch touches nothing but the robot).

## 9. Measurement output (verification record)

Produced by `measure.py` (display width from Python `unicodedata`, the same
source `bin/gen-width.py` uses, with East Asian Ambiguous = 1 to match
`charWidth`):

```
robot-primary.txt  (want 9 rows x 20 cols, tier=halfblock)
  row 0: runes=20 display_width=20
  row 1: runes=20 display_width=20
  row 2: runes=20 display_width=20
  row 3: runes=20 display_width=20
  row 4: runes=20 display_width=20
  row 5: runes=20 display_width=20
  row 6: runes=20 display_width=20
  row 7: runes=20 display_width=20
  row 8: runes=20 display_width=20
  OK
robot-fallback.txt  (want 9 rows x 20 cols, tier=ascii)
  row 0: runes=20 display_width=20
  row 1: runes=20 display_width=20
  row 2: runes=20 display_width=20
  row 3: runes=20 display_width=20
  row 4: runes=20 display_width=20
  row 5: runes=20 display_width=20
  row 6: runes=20 display_width=20
  row 7: runes=20 display_width=20
  row 8: runes=20 display_width=20
  OK
```

Composition was simulated against the real `glyphs` table with the exact
rule from section 6: all 9 composed rows measure 76 columns in both tiers,
wordmark on rows 2–6, subtitle at indent 28, version tag ending at
column 76.

## Verification (for the implementer)

After transcribing the art into Go, re-run from this directory:

```
python3 measure.py robot-primary.txt 9 20 halfblock
python3 measure.py robot-fallback.txt 9 20 ascii
```

then `tutor splash 80` (logo screen), `tutor splash 76` (exact fit),
`tutor splash 75` and `tutor splash 60` (mid screen), `tutor splash 50`
(narrow screen), `TUTOR_ASCII=1 tutor splash 80` (ASCII tier), `NO_COLOR=1`
variants of each, and `go test ./go/...`.

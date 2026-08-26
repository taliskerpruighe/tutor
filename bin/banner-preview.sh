#!/bin/sh
# Prints the tutor launch screen: font F4 (letterspaced solid-block TUTOR),
# the reader's own 256-colour palette swept one way across the headline and
# the other way across the subtitle, and the version tag.
#
#   sh bin/banner-preview.sh
#
# This design is SETTLED, not a menu. Every rejected letterform, colour
# scheme and subtitle treatment that used to live in this file has been
# deleted on purpose, so there is nothing left here to switch to.
#
# The authoritative implementation is go/splash.go — this script exists only
# so the design can be eyeballed without rebuilding the binary. If the two
# ever disagree, the Go source wins.
#
# The colours below are fixed 256-colour shades, not the terminal's own
# sixteen, so they look identical on any terminal theme.

set -eu

# Build the escape sequences with a real ESC byte in them. Writing them as
# the literal string \033 would not do: these are passed to printf as
# *arguments*, and printf only expands backslash escapes in its format
# string, so they would print as the four characters they are spelled with.
E=$(printf '\033')

B="$E[1m"        # bold
R="$E[0m"        # back to normal

# Fixed shades from the 256-colour palette.
c() { printf '%s[38;5;%sm' "$E" "$1"; }

# Headline colours, one per letter of T U T O R, bold.
HEAD_T1=$(c 81)
HEAD_U=$(c 115)
HEAD_T2=$(c 150)
HEAD_O=$(c 215)
HEAD_R=$(c 209)

# Subtitle colours: the same five, run backwards, plain weight.
SUB_A=$(c 209)
SUB_B=$(c 215)
SUB_C=$(c 150)
SUB_D=$(c 115)
SUB_E=$(c 81)

# Version tag colour.
TAG_COL=$(c 81)

SUB='A G E N T I C   A I   C R A S H   C O U R S E'
IND='                         '   # 25 spaces: the robot's 17 columns, the
              # 3-column gutter, and the wordmark field's own 5-column
              # indent (matches Go's subtitleIndent+logoOffset).

# ===========================================================================
# The F4 letterforms, a glyph at a time. Colouring a letter differently from
# its neighbour means the row can no longer be one string, so the word is
# built here from one row of one letter at a time and stitched back together
# with an escape sequence wherever the colour changes. Every glyph is eight
# columns wide and the gap between letters is three, which is what keeps the
# rows in line: 1 + 8x5 + 3x4 = 53 columns.
#
# These shapes are the reference the Go implementation is being written
# from — keep them exactly, do not redraw them.
# ===========================================================================

glyph() {
    case "$1$2" in
        T1)          printf '████████' ;;
        T2|T3|T4|T5) printf '   ██   ' ;;
        U1|U2|U3|U4) printf '██    ██' ;;
        U5)          printf ' ██████ ' ;;
        O1|O5)       printf ' ██████ ' ;;
        O2|O3|O4)    printf '██    ██' ;;
        R1|R3)       printf '███████ ' ;;
        R2|R5)       printf '██    ██' ;;
        R4)          printf '██   ██ ' ;;
    esac
}

# One row of the wordmark, coloured per letter. row is 1..5, matching the
# glyph() row numbering above; the caller passes one colour per letter.
wordmark_row() {
    row=$1; shift
    printf ' '
    i=1
    for L in T U T O R; do
        eval "col=\${$i}"
        printf '%s%s%s' "$col" "$(glyph "$L" "$row")" "$R"
        [ "$i" -lt 5 ] && printf '   '
        i=$((i + 1))
    done
}

# spread <string> <colour> [<colour> ...]
# Walks the string a character at a time and hands each one the colour whose
# share of the width it falls in. With five colours and a forty-five
# character string that is nine characters a colour, which is a gradient at
# this size — the eye reads a sweep, not five blocks.
spread() {
    s=$1; shift
    n=$#
    len=${#s}
    [ "$len" -eq 0 ] && return
    rest=$s
    i=0
    while [ -n "$rest" ]; do
        ch=${rest%"${rest#?}"}
        rest=${rest#?}
        j=$(( i * n / len + 1 ))
        [ "$j" -gt "$n" ] && j=$n
        eval "col=\${$j}"
        printf '%s%s' "$col" "$ch"
        i=$((i + 1))
    done
    printf '%s' "$R"
}

# ===========================================================================
# The robot, a braille row at a time. Braille (U+2800-28FF) packs 2x4 dots
# into every cell, which is what lets a 17x8 box hold the antenna, two open
# eyes, the ear tabs and the "!?" -- four times the vertical detail of the
# half blocks the wordmark is built from.
#
# Unlike those half blocks, braille is NOT proven wherever the wordmark
# renders: it is outside the Nerd Fonts repertoire, so the terminal draws it
# from whatever fallback font the machine has (lab/glyph-blowup/NOTES.md).
# If it looks wrong here, that is a font question, not a script bug.
#
# These rows are copied byte-for-byte from
# lab/glyph-blowup/full-braille-8r.txt -- never retyped by eye, and here
# that matters more than usual: the blank cells are U+2800 BRAILLE PATTERN
# BLANK, not spaces. They are invisible, they are not whitespace, and
# nothing in an editor will show you when one has been lost.
#
# Colour is headColors -- the wordmark's own five stops -- swept top to
# bottom down the rows instead of left to right across the letters, so the
# crown opens on the same 81 the T beside it opens on and the jaw arrives at
# the same 209 the R closes on. Mirrors robotColors in go/splash.go.
# ===========================================================================

robot_color() {
    case "$1" in
        0|1)   c 81  ;;
        2|3)   c 115 ;;
        4)     c 150 ;;
        5|6)   c 215 ;;
        7)     c 209 ;;
    esac
}

robot_row() {
    case "$1" in
        0) printf '⠀⠀⠀⠀⠀⠀⠀⣾⣿⣷⠀⢠⡄⠤⢤⡄⠀' ;;
        1) printf '⠀⠀⠀⠀⠀⠀⠀⢹⣿⡏⠀⢸⡇⠀⡾⠃⠀' ;;
        2) printf '⠀⠀⠀⣠⣶⣾⣿⣿⣿⣿⣿⠠⠄⠀⠄⠀⠀' ;;
        3) printf '⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣦⠀⠀' ;;
        4) printf '⢀⣸⣿⡿⠛⠛⢿⣿⣿⣿⡿⠛⠛⢿⣿⣇⡀' ;;
        5) printf '⣿⣿⣿⡀⠀⠀⢀⣿⣿⣿⡀⠀⠀⢀⣿⣿⣿' ;;
        6) printf '⠿⢿⣿⣷⣦⣴⣾⣿⣿⣿⣷⣦⣴⣾⣿⡿⠿' ;;
        7) printf '⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀' ;;
    esac
}

# One full row of the logo screen: the robot (17 columns, its own colour),
# a 3-column gutter, then either a wordmark row (composed rows 2-6, which
# are glyph rows 1-5) or 53 spaces of filler (composed rows 0, 1 and 7), so
# every one of the 8 rows this prints is 73 columns wide -- 17 robot + 3
# gutter + 53 wordmark field -- exactly mirroring composedRowColored in
# go/splash.go.
composed_row() {
    # cr (not "row") on purpose: this script has no variable scoping, and
    # wordmark_row below also assigns its own argument to a plain variable
    # -- sharing the name "row" here let that inner assignment clobber the
    # outer 0..7 loop counter in the main body, freezing the loop on row 2.
    cr=$1
    rc=$(robot_color "$cr")
    printf '%s%s' "$B" "$rc"
    robot_row "$cr"
    printf '%s' "$R"
    printf '   '
    case "$cr" in
        2) wordmark_row 1 "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R" ;;
        3) wordmark_row 2 "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R" ;;
        4) wordmark_row 3 "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R" ;;
        5) wordmark_row 4 "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R" ;;
        6) wordmark_row 5 "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R" ;;
        *) printf '%53s' '' ;;
    esac
    printf '\n'
}

# ===========================================================================
# The screen itself: blank, 8 composed rows (robot beside the wordmark),
# blank, subtitle, version tag.
# ===========================================================================

printf '\n'
n=0
while [ "$n" -le 7 ]; do
    composed_row "$n"
    n=$((n + 1))
done
printf '\n'
printf '%s' "$IND"
spread "$SUB" "$SUB_A" "$SUB_B" "$SUB_C" "$SUB_D" "$SUB_E"
printf '\n'
printf '%66s%s%s%s\n' '' "$TAG_COL" 'v0.2.14' "$R"

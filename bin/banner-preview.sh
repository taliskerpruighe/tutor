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
IND='     '   # the artwork's letters start one column in; the subtitle
              # sits five columns in to match.

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

# One colour per letter. Give it five.
by_letter() {
    r=1
    while [ "$r" -le 5 ]; do
        printf ' '
        i=1
        for L in T U T O R; do
            eval "col=\${$i}"
            printf '%s%s%s' "$col" "$(glyph "$L" "$r")" "$R"
            [ "$i" -lt 5 ] && printf '   '
            i=$((i + 1))
        done
        printf '\n'
        r=$((r + 1))
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
# The screen itself: blank, five artwork rows, blank, subtitle, version tag.
# ===========================================================================

printf '\n'
by_letter "$B$HEAD_T1" "$B$HEAD_U" "$B$HEAD_T2" "$B$HEAD_O" "$B$HEAD_R"
printf '\n'
printf '%s' "$IND"
spread "$SUB" "$SUB_A" "$SUB_B" "$SUB_C" "$SUB_D" "$SUB_E"
printf '\n'
printf '%47s%s%s%s\n' '' "$TAG_COL" 'v0.2.1' "$R"

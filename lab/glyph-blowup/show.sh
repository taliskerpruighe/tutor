#!/usr/bin/env bash
# Cat every art variant in this directory to the terminal, labelled, in the
# splash's own cyan.  This is the only check that uses your actual terminal
# font and cell metrics, so disagreements between it and preview.png are the
# preview font's fault, not the art's.
cd "$(dirname "$0")" || exit 1
cyan=$'\e[1;38;5;81m'; dim=$'\e[38;5;245m'; off=$'\e[0m'
[ -n "$NO_COLOR" ] && cyan="" && dim="" && off=""
for f in $(ls *r.txt | sort -t- -k3,3V -k1,1 -k2,2); do
    printf '%s== %s%s\n' "$dim" "$f" "$off"
    printf '%s' "$cyan"; cat "$f"; printf '%s\n' "$off"
done

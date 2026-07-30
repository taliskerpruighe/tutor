#!/bin/sh
# Install the `tutor` command.
#
# Safe to run as many times as you like — it overwrites rather than appends,
# so re-running after a change or a re-download simply brings things up to
# date. Nothing outside your home folder is touched, and nothing needs sudo.
#
#   bash ~/tutor/install.sh
#
# Invoke it with `bash` rather than `./install.sh` for two reasons: a folder
# that arrived as a download may have lost its execute bit, and a script run
# *through* an interpreter is never checked by Gatekeeper. Both problems
# disappear the moment you put `bash` in front.

set -eu

TUTOR_HOME=$(cd "$(dirname "$0")" && pwd)
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/tutor"
STATE_DIR="$HOME/.local/share/tutor"
MARK_START="# >>> tutor >>>"
MARK_END="# <<< tutor <<<"

say() { printf '%s\n' "$*"; }
fail() { printf '\n%s\n' "$*" >&2; exit 1; }

say ""
say "Installing the tutor from $TUTOR_HOME"
say ""

mkdir -p "$BIN_DIR" "$STATE_DIR"

# --- 1. The reader ---------------------------------------------------------
# The reader is a self-contained binary, so there is nothing to download and
# nothing to install first.

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
case "$(uname -m)" in
    arm64|aarch64) ARCH=arm64 ;;
    x86_64|amd64)  ARCH=amd64 ;;
    *)             ARCH="" ;;
esac

BIN=""
[ -n "$ARCH" ] && BIN="$TUTOR_HOME/tui/bin/tutor-$OS-$ARCH"

if [ -n "$BIN" ] && [ -f "$BIN" ]; then
    # Copy through a shell redirect rather than with `cp`.
    #
    # Anything unpacked by Archive Utility carries com.apple.quarantine, and
    # macOS refuses to execute a quarantined binary. `cp` would preserve the
    # attribute (it uses copyfile()), and `xattr -d` is not an option either —
    # /usr/bin/xattr is itself a python3 script, so it would demand the very
    # Command Line Tools install this binary exists to avoid. Writing the bytes
    # into a brand new file sidesteps all of it: the destination is created
    # here and has no extended attributes at all.
    #
    # Write to a temporary name and rename it into place, rather than writing
    # over the launcher directly. She is told to keep the reader open in a tab
    # of its own, and re-installing while it runs would otherwise fail with
    # "Text file busy" — the kernel refuses to write to a file it is executing.
    # A rename swaps the directory entry instead, so the running copy carries
    # on untouched and the next launch gets the new one.
    cat "$BIN" > "$LAUNCHER.new"
    chmod +x "$LAUNCHER.new"
    mv -f "$LAUNCHER.new" "$LAUNCHER"
    printf '%s\n' "$TUTOR_HOME" > "$STATE_DIR/home"
    say "  reader      $LAUNCHER ($(basename "$BIN"))"
else
    # No matching binary. On a Mac this branch is unreachable — binaries for
    # both architectures ship — so it exists for anyone running from the
    # source repo on another platform.
    [ -f "$TUTOR_HOME/tui/tutor.py" ] || fail "No reader for $(uname -s)/$(uname -m).

Expected a binary at:

    $BIN

Build one with:  sh bin/build-tui.sh"

    PY=""
    for candidate in python3 /usr/bin/python3 python3.13 python3.12 python3.11 python3.10 python3.9; do
        if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1; then
            PY=$(command -v "$candidate")
            break
        fi
    done

    if [ -z "$PY" ]; then
        fail "No reader for $(uname -s)/$(uname -m), and no Python 3.9+ to fall back on.

On a Mac, install Apple's command line tools and then run this again:

    xcode-select --install
    bash $TUTOR_HOME/install.sh"
    fi

    cat > "$LAUNCHER.new" <<EOF
#!/bin/sh
# Written by $TUTOR_HOME/install.sh — re-run that script to update this.
TUTOR_HOME="$TUTOR_HOME"
export TUTOR_HOME
if [ ! -d "\$TUTOR_HOME" ]; then
    echo "The tutor folder has moved or been deleted:" >&2
    echo "    \$TUTOR_HOME" >&2
    echo "Put it back, or re-run install.sh from wherever it now lives." >&2
    exit 1
fi
exec "$PY" "\$TUTOR_HOME/tui/tutor.py" "\$@"
EOF
    chmod +x "$LAUNCHER.new"
    mv -f "$LAUNCHER.new" "$LAUNCHER"
    printf '%s\n' "$TUTOR_HOME" > "$STATE_DIR/home"
    say "  reader      $LAUNCHER (python $("$PY" -c 'import platform; print(platform.python_version())'))"
fi

# --- 2. PATH ---------------------------------------------------------------
# Bracketed by markers so a second run replaces the block instead of stacking
# another copy of it on the end of the file.

add_path_block() {
    rc="$1"
    [ -e "$rc" ] || : > "$rc"
    if grep -qF "$MARK_START" "$rc" 2>/dev/null; then
        return 0
    fi
    {
        printf '\n%s\n' "$MARK_START"
        printf '%s\n' 'case ":$PATH:" in'
        printf '%s\n' '    *":$HOME/.local/bin:"*) ;;'
        printf '%s\n' '    *) PATH="$HOME/.local/bin:$PATH" ;;'
        printf '%s\n' 'esac'
        printf '%s\n' 'export PATH'
        printf '%s\n' "$MARK_END"
    } >> "$rc"
    say "  PATH        added to $rc"
}

case ":${PATH}:" in
    *":$BIN_DIR:"*) say "  PATH        $BIN_DIR already on PATH" ;;
    *)
        add_path_block "$HOME/.zshrc"
        [ -e "$HOME/.bash_profile" ] && add_path_block "$HOME/.bash_profile"
        ;;
esac

# --- 3. Content index ------------------------------------------------------
# Run the installed copy, never the one still sitting in the unpacked folder:
# that one is still quarantined, and macOS would refuse it.

"$LAUNCHER" index | sed 's/^/  /'

# --- 4. Done ---------------------------------------------------------------

say ""
say "Done."
say ""
say "Open a NEW terminal window or tab, then type:"
say ""
say "    tutor"
say ""
say "The tutor needs a terminal of its own, so keep it in its own tab and"
say "read alongside whatever else you are doing."
say ""

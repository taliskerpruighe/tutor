"""Terminal control for the tutor TUI.

Owns everything that touches the tty: raw mode, the alternate screen, mouse
reporting, input decoding, resize detection, and frame output.

Two invariants this module exists to guarantee:

1. The terminal is *always* restored. Raw mode, the alternate screen, the
   hidden cursor and mouse reporting are undone by a normal exit, an
   exception, ``atexit``, ``SIGTERM`` and ``SIGHUP`` alike. Leaving a user's
   shell in raw mode is the one unforgivable bug in a TUI.

2. A frame is written in a *single* ``write`` call. Assembling the whole
   screen into one string and flushing it once removes tearing without the
   complexity of cell-level diffing, which these screen sizes do not need.

Standard library only, Python 3.9+.
"""

import atexit
import os
import re
import select
import shutil
import signal
import sys
import termios
import tty

# --------------------------------------------------------------------------
# Styles
#
# A style is an SGR parameter string (without the leading escape or trailing
# 'm'). Renderers and layout emit ``(text, style_name)`` spans; this table is
# the single place colour is decided. Honours NO_COLOR.
# --------------------------------------------------------------------------

RESET = "\x1b[0m"

STYLES = {
    "": "",
    "body": "38;5;252",
    "dim": "38;5;245",
    "faint": "38;5;240",
    "bold": "1;38;5;255",
    "italic": "3;38;5;252",
    "bolditalic": "1;3;38;5;255",
    "h1": "1;38;5;81",
    "h2": "1;38;5;80",
    "h3": "1;38;5;115",
    "h4": "1;38;5;150",
    "code": "38;5;215;48;5;236",
    "codeblock": "38;5;223;48;5;235",
    "codelang": "38;5;108;48;5;235",
    "link": "4;38;5;117",
    "linkurl": "38;5;244",
    "rule": "38;5;238",
    "quote": "3;38;5;250",
    "quotebar": "38;5;72",
    "bullet": "1;38;5;81",
    "tablehead": "1;38;5;81",
    "tableborder": "38;5;240",
    # chrome
    "tab_active": "1;4;38;5;81",
    "tab_idle": "38;5;245",
    "tab_arrow": "38;5;240",
    "sep": "38;5;238",
    "sel_bar": "1;38;5;81",
    "sel_row": "1;38;5;231;48;5;238",
    "row_num": "38;5;109",
    "row": "38;5;250",
    "status": "38;5;245;48;5;235",
    "status_key": "38;5;81;48;5;235",
    "warn": "1;38;5;209",
    "search": "1;38;5;16;48;5;186",
}

_NO_COLOR = bool(os.environ.get("NO_COLOR"))


def sgr(style):
    """Return the escape sequence that turns *style* on, or '' if none."""
    if _NO_COLOR:
        return ""
    params = STYLES.get(style, "")
    return "\x1b[" + params + "m" if params else ""


# --------------------------------------------------------------------------
# Input decoding
#
# Events are either a string token ('up', 'q', 'enter', ...) or a Mouse
# namedtuple-ish tuple ('mouse', kind, col, row) with 0-based coordinates.
# --------------------------------------------------------------------------

# Terminals disagree about arrow keys: xterm emits CSI A, some emit SS3 A.
_CSI_KEYS = {
    "A": "up",
    "B": "down",
    "C": "right",
    "D": "left",
    "H": "home",
    "F": "end",
    "Z": "shift-tab",
}

_TILDE_KEYS = {
    "1": "home",
    "3": "delete",
    "4": "end",
    "5": "pgup",
    "6": "pgdn",
    "7": "home",
    "8": "end",
}

_CTRL = {
    "\r": "enter",
    "\n": "enter",
    "\t": "tab",
    "\x7f": "backspace",
    "\x08": "backspace",
    "\x03": "ctrl-c",
    "\x04": "ctrl-d",
    "\x1b": "esc",
}

# SGR mouse report: CSI < button ; col ; row (M=press, m=release)
_MOUSE_RE = re.compile(r"^\x1b\[<(\d+);(\d+);(\d+)([Mm])")
# CSI sequence: ESC [ params intermediates final
_CSI_RE = re.compile(r"^\x1b\[([0-9;?]*)([ -/]*)([@-~])")
# SS3 sequence: ESC O final
_SS3_RE = re.compile(r"^\x1bO([@-~])")


def _decode(buf):
    """Pull one event off the front of *buf*.

    Returns ``(event, rest)``. ``event`` is None when *buf* holds only the
    prefix of an incomplete escape sequence and we should wait for more bytes.
    """
    if not buf:
        return None, buf

    if buf[0] != "\x1b":
        ch = buf[0]
        if ch in _CTRL:
            return _CTRL[ch], buf[1:]
        if ch < " ":
            return "ctrl-" + chr(ord(ch) + 96), buf[1:]
        return ch, buf[1:]

    # Lone ESC with nothing after it yet: caller decides whether to wait.
    if len(buf) == 1:
        return None, buf

    m = _MOUSE_RE.match(buf)
    if m:
        button, col, row, kind = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
        rest = buf[m.end():]
        if button == 64:
            return ("mouse", "wheel-up", col - 1, row - 1), rest
        if button == 65:
            return ("mouse", "wheel-down", col - 1, row - 1), rest
        if kind == "M" and (button & 0b11000011) == 0:
            return ("mouse", "click", col - 1, row - 1), rest
        return ("mouse", "other", col - 1, row - 1), rest

    m = _SS3_RE.match(buf)
    if m:
        return _CSI_KEYS.get(m.group(1), "unknown"), buf[m.end():]

    m = _CSI_RE.match(buf)
    if m:
        params, final = m.group(1), m.group(3)
        rest = buf[m.end():]
        if final == "~":
            return _TILDE_KEYS.get(params.split(";")[0], "unknown"), rest
        if final in _CSI_KEYS:
            # Modified keys arrive as CSI 1;5A etc. Modifiers are ignored;
            # the base key is what the keymap acts on.
            return _CSI_KEYS[final], rest
        return "unknown", rest

    if buf[1] == "[" or buf[1] == "O" or buf[1] == "<":
        # Incomplete CSI/SS3 still arriving.
        return None, buf

    # ESC followed by a plain key: alt-modified. Treated as bare ESC so that
    # pressing escape twice quickly never gets swallowed.
    return "esc", buf[1:]


# --------------------------------------------------------------------------
# Terminal
# --------------------------------------------------------------------------


class Terminal:
    """Context manager owning the tty for the lifetime of the TUI."""

    def __init__(self, mouse=True):
        self.fd = sys.stdin.fileno()
        self._saved = None
        self._mouse = mouse
        self._buf = ""
        self._raw_bytes = b""
        self.resized = True  # force an initial layout pass
        self._prev_winch = None
        self._wake_r = -1
        self._wake_w = -1

    # -- lifecycle ---------------------------------------------------------

    def __enter__(self):
        self._saved = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        out = "\x1b[?1049h\x1b[?25l\x1b[2J\x1b[H"
        if self._mouse:
            # 1000 = button events, 1006 = SGR coordinates (needed above 223
            # columns, which any modern terminal exceeds).
            out += "\x1b[?1000h\x1b[?1006h"
        self._write(out)
        atexit.register(self.restore)

        # A self-pipe is what makes resizing work. Python retries an
        # interrupted select() automatically (PEP 475), so a SIGWINCH handler
        # that merely sets a flag would never wake a blocking read — the
        # window would not repaint until the next keypress. Routing signals
        # through a pipe gives select() something real to notice.
        self._wake_r, self._wake_w = os.pipe()
        os.set_blocking(self._wake_r, False)
        os.set_blocking(self._wake_w, False)
        signal.set_wakeup_fd(self._wake_w, warn_on_full_buffer=False)

        self._prev_winch = signal.signal(signal.SIGWINCH, self._on_winch)
        for s in (signal.SIGTERM, signal.SIGHUP):
            signal.signal(s, self._on_terminate)
        return self

    def __exit__(self, *exc):
        self.restore()
        return False

    def _on_winch(self, *_):
        self.resized = True

    def _on_terminate(self, *_):
        self.restore()
        os._exit(0)

    def restore(self):
        """Undo every terminal mutation. Safe to call more than once."""
        if self._saved is None:
            return
        saved, self._saved = self._saved, None
        try:
            signal.set_wakeup_fd(-1)
        except (ValueError, OSError):
            pass  # not the main thread, or already torn down
        for fd in (self._wake_r, self._wake_w):
            if fd >= 0:
                try:
                    os.close(fd)
                except OSError:
                    pass
        self._wake_r = self._wake_w = -1
        out = ""
        if self._mouse:
            out += "\x1b[?1006l\x1b[?1000l"
        out += "\x1b[?25h\x1b[?1049l" + RESET
        try:
            self._write(out)
        except Exception:
            pass
        try:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, saved)
        except Exception:
            pass

    # -- output ------------------------------------------------------------

    @staticmethod
    def _write(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def size(self):
        # Ask the tty itself. shutil.get_terminal_size() consults $COLUMNS and
        # $LINES first, and a stale exported value would freeze the layout at
        # the size the shell started at, so it is only the fallback here.
        try:
            cols, rows = os.get_terminal_size(self.fd)
        except OSError:
            cols, rows = shutil.get_terminal_size(fallback=(80, 24))
        return max(cols, 1), max(rows, 1)

    def draw(self, rows):
        """Paint *rows*: a list of rows, each a list of ``(text, style)``.

        Rows beyond the list are blanked, so callers never have to pad the
        frame to the full screen height themselves.
        """
        _, height = self.size()
        out = ["\x1b[H"]
        for y in range(height):
            out.append("\x1b[%d;1H\x1b[2K" % (y + 1))
            if y < len(rows):
                for text, style in rows[y]:
                    if not text:
                        continue
                    esc = sgr(style)
                    out.append(esc + text + RESET if esc else text)
        out.append("\x1b[%d;1H" % height)
        self._write("".join(out))

    # -- input -------------------------------------------------------------

    def read_event(self, timeout=None):
        """Block for one event. Returns None on timeout or a pending resize.

        Callers loop on this; a None return simply means "redraw and ask
        again", which is exactly what a resize needs.
        """
        while True:
            event, self._buf = _decode(self._buf)
            if event is not None:
                return event

            # A lone ESC in the buffer is ambiguous: it may be the start of a
            # sequence still in flight, or the escape key. Poll briefly; if
            # nothing follows, it was the key.
            poll = 0.05 if self._buf else timeout
            watch = [self.fd] + ([self._wake_r] if self._wake_r >= 0 else [])
            ready, _, _ = select.select(watch, [], [], poll)
            if not ready:
                if self._buf:
                    event, self._buf = "esc", self._buf[1:]
                    return event
                return None

            if self._wake_r in ready:
                try:
                    os.read(self._wake_r, 4096)
                except OSError:
                    pass
                if self.resized:
                    return None  # caller repaints at the new size
                if self.fd not in ready:
                    continue

            try:
                chunk = os.read(self.fd, 4096)
            except OSError:
                return "quit"
            if not chunk:
                return "quit"
            self._raw_bytes += chunk
            # Decode conservatively so a multi-byte character split across
            # reads is not mangled into replacement characters.
            try:
                text = self._raw_bytes.decode("utf-8")
                self._raw_bytes = b""
            except UnicodeDecodeError:
                if len(self._raw_bytes) > 8:
                    text = self._raw_bytes.decode("utf-8", "replace")
                    self._raw_bytes = b""
                else:
                    continue
            self._buf += text

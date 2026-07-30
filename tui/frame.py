"""Headless whole-screen dump: python3 -m tui.frame <cols> <rows> [id] [mode] [query]

The twin of ``python3 -m tui.render``, and the reference the Go side's
``tutor frame`` is diffed against. Article renders only cover the middle of
the screen; this composes the whole frame — tab bar, sidebar, status line —
so the chrome is verified too.

Root comes from ``$TUTOR_HOME`` when set, matching how the Go binary resolves
it, so both implementations are guaranteed to be reading the same corpus.
"""

import os
import sys

if __package__ in (None, ""):  # invoked as a plain script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tui import content, layout, term
    from tui.app import App
else:
    from . import content, layout, term
    from .app import App


def repo_root():
    return os.environ.get("TUTOR_HOME") or os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


def build_frame(root, cols, rows, article_id="", mode="normal", query=""):
    app = App(root, content.load_index(root, rebuild=False))
    if article_id:
        for pi, ai, _part, article in content.flatten(app.index):
            if article["id"] == article_id:
                app.go(pi, ai)
                break
    app._pane_w = layout.pane_width(cols)
    app._pane_h = max(1, rows - layout.CHROME_ROWS)
    if mode == "help":
        app.mode = "help"
    elif mode == "search":
        app.mode = "search"
        app.set_query(query)
    return layout.build(app, cols, rows)


def main(argv):
    if len(argv) < 2:
        print("usage: python3 -m tui.frame <cols> <rows> [article-id] [mode] [query]",
              file=sys.stderr)
        return 1
    cols, rows = int(argv[0]), int(argv[1])
    article_id = argv[2] if len(argv) > 2 else ""
    mode = argv[3] if len(argv) > 3 else "normal"
    query = " ".join(argv[4:]) if len(argv) > 4 else ""
    frame = build_frame(repo_root(), cols, rows, article_id, mode, query)
    for row in frame.rows:
        out = []
        for text, style in row:
            esc = term.sgr(style)
            out.append(esc + text + term.RESET if esc else text)
        print("".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

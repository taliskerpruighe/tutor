"""Application state and the key map.

Everything the reader can do lives here: where they are in the course, how far
down the page they have scrolled, and what each key means in each of the three
modes (reading, searching, help).

The design rule throughout is that no key is destructive and no key is a dead
end — `esc` always backs out, `q` always leaves, and an unknown key is
silently ignored rather than beeping or bailing.
"""

from . import content, layout
from .render import render


class App:
    def __init__(self, root, index=None, query=None):
        self.root = root
        self.index = index if index is not None else content.load_index(root)
        self.part_i = 0
        self.article_i = 0
        self.scroll = 0
        self.mode = "normal"
        self.query = ""
        self.results = []
        self.result_i = 0
        self.running = True
        self.status_note = ""
        self._cache = {}
        self._help_cache = {}
        self._pane_w = 72
        self._pane_h = 20
        self._return_to = None
        if query:
            self.mode = "search"
            self._return_to = (self.part_i, self.article_i, self.scroll)
            self.set_query(query)

    # -- current position --------------------------------------------------

    def parts(self):
        return self.index.get("parts", [])

    def part(self):
        parts = self.parts()
        return parts[self.part_i] if 0 <= self.part_i < len(parts) else None

    def article(self):
        part = self.part()
        if not part:
            return None
        articles = part.get("articles", [])
        return articles[self.article_i] if 0 <= self.article_i < len(articles) else None

    # -- rendering ---------------------------------------------------------

    def pane_lines(self, width):
        self._pane_w = width
        article = self.article()
        if not article:
            return render(_EMPTY_DOC, width)
        key = (article["path"], width)
        if key not in self._cache:
            if len(self._cache) > 24:
                self._cache.clear()
            self._cache[key] = render(content.read_article(self.root, article), width)
        return self._cache[key]

    def help_lines(self, width):
        if width not in self._help_cache:
            self._help_cache = {width: render(layout.HELP, width)}
        return self._help_cache[width]

    def _current_lines(self):
        if self.mode == "help":
            return self.help_lines(max(20, self._pane_w))
        return self.pane_lines(self._pane_w)

    def max_scroll(self):
        return max(0, len(self._current_lines()) - self._pane_h)

    def scroll_percent(self):
        top = self.max_scroll()
        if top <= 0:
            return 100
        return min(100, int(round(100 * self.scroll / top)))

    # -- navigation --------------------------------------------------------

    def _clamp_scroll(self):
        self.scroll = max(0, min(self.scroll, self.max_scroll()))

    def go(self, part_i, article_i=0):
        parts = self.parts()
        if not parts:
            return
        self.part_i = max(0, min(part_i, len(parts) - 1))
        articles = self.part().get("articles", [])
        self.article_i = max(0, min(article_i, max(0, len(articles) - 1)))
        self.scroll = 0

    def step_part(self, delta):
        self.go(self.part_i + delta, 0)

    def sections(self):
        """The current part's sections and where the cursor sits in them.

        The open section is derived from ``article_i`` rather than stored, so
        every existing way of moving — ``n``, search, a click — opens the
        right one without knowing sections exist.
        """
        part = self.part()
        if not part:
            return [], None
        secs = content.part_sections(part)
        if not secs:
            return [], None
        return secs, content.section_at(part, self.article_i)

    def step_section(self, delta):
        """Move to the neighbouring section's first article.

        Clamps at the part's edges: ← and → are already the way out of a part.
        """
        secs, si = self.sections()
        if si is None:
            return
        target = max(0, min(si + delta, len(secs) - 1))
        self.go(self.part_i, secs[target][1])

    def open_section(self, index):
        """Jump to a section by index — what a click on its header does."""
        secs, _si = self.sections()
        if 0 <= index < len(secs):
            self.go(self.part_i, secs[index][1])

    def step_article(self, delta):
        """Move one article, carrying on into the neighbouring part at the ends.

        Linear reading is the whole point of a course, so `n` should never
        stop dead at a part boundary.
        """
        flat = content.flatten(self.index)
        if not flat:
            return
        here = 0
        for k, (pi, ai, _p, _a) in enumerate(flat):
            if pi == self.part_i and ai == self.article_i:
                here = k
                break
        target = max(0, min(here + delta, len(flat) - 1))
        pi, ai, _p, _a = flat[target]
        self.go(pi, ai)

    # -- search ------------------------------------------------------------

    def set_query(self, query):
        self.query = query
        self.results = content.search(self.root, self.index, query)
        self.result_i = 0
        self._preview_result()

    def _preview_result(self):
        """Show the highlighted match immediately, so search is a live preview."""
        if not self.results:
            return
        self.result_i = max(0, min(self.result_i, len(self.results) - 1))
        pi, ai, _p, _a = self.results[self.result_i]
        self.part_i, self.article_i, self.scroll = pi, ai, 0

    def open_result(self):
        if self.results:
            self._preview_result()
        self.mode = "normal"
        self._return_to = None

    def cancel_search(self):
        if self._return_to:
            self.part_i, self.article_i, self.scroll = self._return_to
        self.mode = "normal"
        self.query = ""
        self.results = []
        self._return_to = None

    def reload(self):
        self.index = content.load_index(self.root)
        self._cache.clear()
        self.go(self.part_i, self.article_i)
        self.status_note = "reloaded"

    # -- events ------------------------------------------------------------

    def handle(self, event, frame):
        if isinstance(event, tuple) and event and event[0] == "mouse":
            return self._handle_mouse(event, frame)
        if self.mode == "search":
            return self._handle_search(event)
        if self.mode == "help":
            return self._handle_help(event)
        return self._handle_normal(event)

    def _handle_normal(self, key):
        if key in ("q", "ctrl-c", "quit"):
            self.running = False
        elif key == "?":
            self.mode = "help"
            self._return_to = (self.part_i, self.article_i, self.scroll)
            self.scroll = 0
        elif key == "/":
            self.mode = "search"
            self._return_to = (self.part_i, self.article_i, self.scroll)
            self.set_query("")
        elif key in ("left", "h"):
            self.step_part(-1)
        elif key in ("right", "l"):
            self.step_part(1)
        elif key == "shift-tab":
            self.step_section(-1)
        elif key == "tab":
            self.step_section(1)
        elif key == "n":
            self.step_article(1)
        elif key == "p":
            self.step_article(-1)
        elif key in ("down", "j"):
            self.scroll += 1
        elif key in ("up", "k"):
            self.scroll -= 1
        elif key in (" ", "pgdn", "ctrl-f"):
            self.scroll += max(1, self._pane_h - 2)
        elif key in ("b", "pgup", "ctrl-b"):
            self.scroll -= max(1, self._pane_h - 2)
        elif key in ("g", "home"):
            self.scroll = 0
        elif key in ("G", "end"):
            self.scroll = self.max_scroll()
        elif key == "r":
            self.reload()
        elif key and len(key) == 1 and key.isdigit() and key != "0":
            # 1-9 count within the open section, so a part with more than nine
            # articles in it still has every page one keypress away.
            part = self.part()
            wanted = int(key) - 1
            if part:
                first, last = 0, len(part.get("articles", []))
                secs, si = self.sections()
                if si is not None:
                    first, last = secs[si][1], secs[si][2]
                if first + wanted < last:
                    self.go(self.part_i, first + wanted)
        self._clamp_scroll()
        return self.running

    def _handle_search(self, key):
        if key == "esc":
            self.cancel_search()
        elif key == "enter":
            self.open_result()
        elif key == "backspace":
            self.set_query(self.query[:-1])
        elif key in ("down", "ctrl-n"):
            self.result_i += 1
            self._preview_result()
        elif key in ("up", "ctrl-p"):
            self.result_i -= 1
            self._preview_result()
        elif key == "ctrl-c":
            self.running = False
        elif isinstance(key, str) and len(key) == 1 and key >= " ":
            self.set_query(self.query + key)
        self._clamp_scroll()
        return self.running

    def _handle_help(self, key):
        if key in ("esc", "?", "q"):
            self.mode = "normal"
            if self._return_to:
                self.part_i, self.article_i, self.scroll = self._return_to
                self._return_to = None
        elif key == "ctrl-c":
            self.running = False
        elif key in ("down", "j"):
            self.scroll += 1
        elif key in ("up", "k"):
            self.scroll -= 1
        elif key in (" ", "pgdn"):
            self.scroll += max(1, self._pane_h - 2)
        elif key in ("b", "pgup"):
            self.scroll -= max(1, self._pane_h - 2)
        elif key in ("g", "home"):
            self.scroll = 0
        elif key in ("G", "end"):
            self.scroll = self.max_scroll()
        self._clamp_scroll()
        return self.running

    def _handle_mouse(self, event, frame):
        _tag, kind, x, y = event
        if kind == "wheel-up":
            self.scroll -= 3
        elif kind == "wheel-down":
            self.scroll += 3
        elif kind == "click":
            tab = frame.tab_at(x, y)
            if tab is not None:
                if self.mode == "search":
                    self.cancel_search()
                self.go(tab, 0)
            else:
                hit = frame.item_at(x, y)
                if hit is not None:
                    item_kind, item = hit
                    if self.mode == "search":
                        if item < len(self.results):
                            self.result_i = item
                            self.open_result()
                    elif item_kind == "section":
                        self.open_section(item)
                    else:
                        self.go(self.part_i, item)
        self._clamp_scroll()
        return self.running

    # -- main loop ---------------------------------------------------------

    def run(self, terminal):
        frame = None
        while self.running:
            cols, rows = terminal.size()
            self._pane_w = layout.pane_width(cols)
            self._pane_h = max(1, rows - layout.CHROME_ROWS)
            self._clamp_scroll()
            frame = layout.build(self, cols, rows)
            terminal.draw(frame.rows)
            terminal.resized = False

            event = terminal.read_event(timeout=None)
            if event is None:
                continue  # resize: fall through and repaint
            self.handle(event, frame)


_EMPTY_DOC = """
# Nothing here yet

This part has no articles in it.

Content lives in `content/`, one folder per part and one markdown file per
article. Add a file there and press `r` to reload.
"""

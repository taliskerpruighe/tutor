"""Application state and the key map.

Everything the reader can do lives here: where they are in the course, how far
down the page they have scrolled, and what each key means in each of the three
modes (reading, searching, help).

The design rule throughout is that no key is destructive and no key is a dead
end — `esc` always backs out, `q` always leaves, and an unknown key is
silently ignored rather than beeping or bailing.
"""

from . import content, layout, state
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
        # read is the set of article ids marked read, and read_path is where
        # it is written back. An empty read_path means "hold this in memory
        # and do not persist" -- which is what build_frame wants, for the
        # determinism reason set out there.
        self.read = {}
        self.read_path = None
        # installed is the version the reader first installed at, loaded
        # once from $STATE_DIR/installed (state.installed_path) by tutor.py
        # and never written by this program -- install.sh owns the write,
        # this side only reads it back. An empty value means "unknown, treat
        # everything new as new": that covers both a genuinely absent file
        # (every reader who was here before this feature existed) and
        # frame.py's deliberate choice not to read the real state directory
        # at all.
        self.installed = ""
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

    def toggle_read(self):
        article = self.article()
        if not article:
            return
        if article["id"] in self.read:
            del self.read[article["id"]]
        else:
            self.read[article["id"]] = True
        if self.read_path:
            # A failure here costs the mark at the next launch and nothing
            # more, so it must not interrupt reading. `tutor doctor` is
            # where an unwritable state directory is meant to surface.
            try:
                state.save_marks(self.read_path, self.read)
            except OSError:
                pass

    def levels(self):
        """The index's levels, and which one the cursor is in.

        Like sections, the open level is derived from where the cursor sits
        rather than stored, so ``n``, a search hit and a click all open the
        right tab without knowing levels exist.
        """
        lv = content.index_levels(self.index)
        if not lv:
            return [], None
        return lv, content.level_at(self.index, self.part_i)

    def step_level(self, delta):
        """Move to the neighbouring level's first article.

        What ← and → do now that the tabs along the top are levels rather
        than parts.
        """
        lv, li = self.levels()
        if li is None:
            return
        target = max(0, min(li + delta, len(lv) - 1))
        self.go(lv[target][1], 0)

    def open_level(self, index):
        """Jump to a level by index — what a click on a tab does."""
        lv, _li = self.levels()
        if 0 <= index < len(lv):
            self.go(lv[index][1], 0)

    def step_part(self, delta):
        """Move one part, clamping at the level's edges.

        ← and → are the way out of a level, so ``[`` and ``]`` never carry
        the reader across a tab boundary by accident.
        """
        lv, li = self.levels()
        if li is None:
            self.go(self.part_i + delta, 0)
            return
        _title, first, last = lv[li]
        self.go(max(first, min(self.part_i + delta, last - 1)), 0)

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

    def level_sections(self):
        """Flatten every section of every part in the current level into one list.

        So ``Tab`` walks the left column top to bottom the way it looks — on
        into the next part's first section rather than stopping dead at a
        part boundary. It clamps at the level's edges, because ← and → are
        the way out.
        """
        lv, li = self.levels()
        if li is None:
            return [], 0
        _title, first, last = lv[li]
        out, here = [], 0
        for pi in range(first, last):
            part = self.parts()[pi]
            for _title, start, stop in content.part_sections(part):
                if pi == self.part_i and start <= self.article_i < stop:
                    here = len(out)
                out.append((pi, start))
        return out, here

    def step_section(self, delta):
        """Move to the neighbouring section's first article."""
        secs, here = self.level_sections()
        if not secs:
            return
        target_pi, target_ai = secs[max(0, min(here + delta, len(secs) - 1))]
        self.go(target_pi, target_ai)

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
            self.step_level(-1)
        elif key in ("right", "l"):
            self.step_level(1)
        elif key == "[":
            self.step_part(-1)
        elif key == "]":
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
        elif key == "m":
            self.toggle_read()
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
                self.open_level(tab)
            else:
                hit = frame.item_at(x, y)
                if hit is not None:
                    item_kind, item = hit
                    if self.mode == "search":
                        if item < len(self.results):
                            self.result_i = item
                            self.open_result()
                    elif item_kind == "part":
                        # A part header carries the part's own index, so
                        # clicking a collapsed one opens it at its first
                        # article.
                        self.go(item, 0)
                    else:
                        # Section headers and articles both carry an article
                        # index within the part standing open, so one branch
                        # serves both.
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

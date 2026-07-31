"""The content corpus: frontmatter parsing and the generated index.

``content/`` is the single source of truth for the whole tutor. Two very
different readers consume it:

* this TUI, which needs an ordered navigation tree, and
* the Claude Code skill, which needs a lookup table to find the one file that
  answers a question.

Both read ``content/index.json``, generated here. Neither copies prose, so
there is exactly one place a fact can live and exactly one place to edit it.

The index rebuilds itself whenever any article is newer than it, so authoring
is "drop a markdown file in and reopen" — there is no build step to forget.
"""

import json
import os
import re

INDEX_NAME = "index.json"

# Frontmatter is a deliberately tiny subset: `key: scalar` and `key: [a, b]`.
# Hand-parsing it avoids a PyYAML dependency, which would otherwise be the
# only thing standing between her and a working install.
_FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)
_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")
_INT_KEYS = ("order",)
_LIST_KEYS = ("keywords",)


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text):
    """Return ``(meta, body)``. Missing or malformed frontmatter yields ``{}``."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split("\n"):
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        km = _KEY_RE.match(line)
        if not km:
            continue
        key, raw = km.group(1), km.group(2).strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            meta[key] = [_unquote(v.strip()) for v in inner.split(",") if v.strip()]
        else:
            value = _unquote(raw)
            if key in _INT_KEYS:
                try:
                    value = int(value)
                except ValueError:
                    pass
            meta[key] = value
    for key in _LIST_KEYS:
        if isinstance(meta.get(key), str):
            meta[key] = [v.strip() for v in meta[key].split(",") if v.strip()]
    return meta, text[m.end():]


def deslug(slug):
    """``01-the-terminal`` -> ``The Terminal``. A fallback, not the rule."""
    slug = re.sub(r"^\d+[-_]", "", slug)
    words = re.split(r"[-_\s]+", slug)
    return " ".join(w[:1].upper() + w[1:] for w in words if w)


def _sort_key(prefix_source, order, title):
    """Order by explicit `order`, then by filename prefix, then by title."""
    m = re.match(r"^(\d+)", prefix_source)
    numeric = int(m.group(1)) if m else 10 ** 6
    return (order if isinstance(order, int) else numeric, numeric, title.lower())


def content_dir(root):
    return os.path.join(root, "content")


def index_path(root):
    return os.path.join(content_dir(root), INDEX_NAME)


def iter_markdown(root):
    base = content_dir(root)
    if not os.path.isdir(base):
        return
    for slug in sorted(os.listdir(base)):
        part_dir = os.path.join(base, slug)
        if not os.path.isdir(part_dir) or slug.startswith((".", "_")):
            continue
        for name in sorted(os.listdir(part_dir)):
            if name.endswith(".md") and not name.startswith((".", "_")):
                yield slug, name, os.path.join(part_dir, name)


def build_index(root):
    """Scan ``content/`` and return the index structure."""
    parts = {}
    for slug, name, path in iter_markdown(root):
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        meta, body = parse_frontmatter(text)

        title = meta.get("title") or _first_heading(body) or deslug(name[:-3])
        part_title = meta.get("part") or deslug(slug)
        article = {
            "id": meta.get("id") or "%s/%s" % (re.sub(r"^\d+[-_]", "", slug), name[:-3]),
            "title": title,
            "section": meta.get("section", ""),
            "summary": meta.get("summary", ""),
            "keywords": meta.get("keywords", []),
            "path": os.path.relpath(path, root).replace(os.sep, "/"),
            "_sort": _sort_key(name, meta.get("order"), title),
        }
        part = parts.setdefault(
            slug,
            {"slug": slug, "title": part_title, "level": meta.get("level", ""), "articles": []},
        )
        # The first article carrying an explicit `part:` names the part; later
        # ones do not get to rename it out from under the earlier files.
        if meta.get("part") and part["title"] == deslug(slug):
            part["title"] = meta["part"]
        # `level:` follows the same first-one-wins rule.
        if not part["level"]:
            part["level"] = meta.get("level", "")
        part["articles"].append(article)

    ordered = []
    for slug in sorted(parts, key=lambda s: _sort_key(s, None, parts[s]["title"])):
        part = parts[slug]
        part["articles"].sort(key=lambda a: a["_sort"])
        for article in part["articles"]:
            del article["_sort"]
        ordered.append(part)
    return {"parts": ordered}


def _first_heading(body):
    for line in body.split("\n"):
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def write_index(root):
    index = build_index(root)
    target = index_path(root)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return index


def is_stale(root):
    """True when any article, or the set of articles, is newer than the index."""
    target = index_path(root)
    if not os.path.exists(target):
        return True
    stamp = os.path.getmtime(target)
    base = content_dir(root)
    if os.path.isdir(base) and os.path.getmtime(base) > stamp:
        return True
    for _slug, _name, path in iter_markdown(root):
        if os.path.getmtime(path) > stamp:
            return True
        # A rename or deletion changes the directory's own mtime.
        if os.path.getmtime(os.path.dirname(path)) > stamp:
            return True
    return False


def load_index(root, rebuild=True):
    """Load the index, regenerating it first if the content has moved on."""
    if rebuild and is_stale(root):
        try:
            return write_index(root)
        except OSError:
            # A read-only install still works; it just cannot cache.
            return build_index(root)
    try:
        with open(index_path(root), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return build_index(root)


def read_article(root, article):
    """Return the markdown body of *article* with frontmatter stripped."""
    path = os.path.join(root, article["path"])
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return "# Missing article\n\n`%s` could not be read.\n\n    %s\n" % (
            article.get("path", "?"),
            exc,
        )
    _meta, body = parse_frontmatter(text)
    return body


def part_sections(part):
    """Group a part's articles into ``(title, from, to)`` runs.

    A section is a run of consecutive articles sharing a ``section:`` value,
    the empty one included. It is derived here rather than stored, so the
    index stays a flat list of articles and search, :func:`flatten` and the
    Claude Code skill all carry on reading it exactly as before. A part where
    no article carries ``section:`` is a single untitled run spanning the
    lot, which draws as the plain numbered list it has always been.
    """
    out = []
    for i, article in enumerate(part.get("articles", [])):
        title = article.get("section", "")
        if out and out[-1][0] == title and out[-1][2] == i:
            out[-1] = (title, out[-1][1], i + 1)
            continue
        out.append((title, i, i + 1))
    return out


def section_at(part, i):
    """The index of the section holding article *i*, or ``None``."""
    for si, (_title, start, stop) in enumerate(part_sections(part)):
        if start <= i < stop:
            return si
    return None


def level_of(part):
    """A part's level, falling back to its own title.

    That fallback is what makes a corpus carrying no ``level:`` at all
    degrade to the old behaviour exactly — every part becomes its own
    single-part level, so the tab bar still reads as the list of parts and
    the sidebar suppresses the redundant part heading.
    """
    return part.get("level") or part["title"]


def index_levels(index):
    """Group the index's parts into runs of equal ``level:`` as ``(title, from, to)``.

    A level is a run of consecutive parts sharing a ``level:`` value — the
    tabs along the top. It is derived the same way a section is, and for the
    same reason: the index stays a flat list of parts holding a flat list of
    articles, so search, :func:`flatten` and the Claude Code skill never
    learnt that levels exist.
    """
    out = []
    for i, part in enumerate(index.get("parts", [])):
        title = level_of(part)
        if out and out[-1][0] == title and out[-1][2] == i:
            out[-1] = (title, out[-1][1], i + 1)
            continue
        out.append((title, i, i + 1))
    return out


def level_at(index, i):
    """The index of the level holding part *i*, or ``None``."""
    for li, (_title, start, stop) in enumerate(index_levels(index)):
        if start <= i < stop:
            return li
    return None


def flatten(index):
    """All articles in reading order as ``(part_i, article_i, part, article)``."""
    out = []
    for pi, part in enumerate(index.get("parts", [])):
        for ai, article in enumerate(part.get("articles", [])):
            out.append((pi, ai, part, article))
    return out


def search(root, index, query):
    """Rank articles against *query*. Title and keyword hits outrank body hits."""
    query = query.strip().lower()
    if not query:
        return []
    terms = query.split()
    results = []
    for pi, ai, part, article in flatten(index):
        haystacks = (
            article["title"].lower(),
            " ".join(article.get("keywords", [])).lower(),
            article.get("summary", "").lower(),
            read_article(root, article).lower(),
        )
        weights = (10, 6, 4, 1)
        score = 0
        for term in terms:
            hit = 0
            for hay, weight in zip(haystacks, weights):
                if term in hay:
                    hit = max(hit, weight)
            if not hit:
                score = 0
                break  # every term must appear somewhere
            score += hit
        if score:
            results.append((score, pi, ai, part, article))
    results.sort(key=lambda r: (-r[0], r[1], r[2]))
    return [(pi, ai, part, article) for _s, pi, ai, part, article in results]

"""Read marks: the one thing tutor writes outside its own folder.

Everything else this reader touches -- content/, content/index.json, the
caches in app.py -- lives inside the tutor tree, because the tree itself is
disposable: an update renames the whole thing aside and removes it wholesale
on every upgrade. A mark file kept inside that tree would be destroyed the
moment she updated, which defeats the entire point of remembering what she
has read.

So marks live in ``$TUTOR_STATE`` if set, else ``~/.local/share/tutor`` --
the directory install.sh already creates and already writes one file into,
the "home" pointer tutor.py's root resolution reads back. read.json sits
beside it. ``$TUTOR_STATE`` is the counterpart to the existing
``$TUTOR_HOME``: it exists so bin/parity.sh can pin state the same
deterministic way it already pins the corpus.
"""

import json
import os


def state_dir():
    env = os.environ.get("TUTOR_STATE")
    if env:
        return env
    return os.path.expanduser(os.path.join("~", ".local", "share", "tutor"))


def marks_path():
    return os.path.join(state_dir(), "read.json")


def load_marks(path):
    """Read the set of read article ids, keyed on an article's ``id`` rather
    than its ``path``, because an id survives renumbering a directory and a
    path does not.

    A missing file, an unreadable one, or malformed JSON all return an
    empty, non-``None`` dict rather than raising: a corrupt marks file must
    never be the reason the reader fails to open. There is precedent for
    that posture elsewhere in this codebase -- a failed probe for image
    support costs nothing worse than a missing picture, a failed splash
    screen must never be the reason the reader fails to open, and a
    read-only install still works, it just cannot cache.

    Ids naming articles that no longer exist are kept, not pruned: nothing
    looks them up against the current index, and pruning would lose marks
    made against a temporary checkout of an older corpus.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    out = {}
    if isinstance(data, dict):
        for id_ in data.get("read", []) or []:
            out[id_] = True
    return out


def save_marks(path, ids):
    """Write the set back, sorted so the file is stable and diffable from
    one save to the next.

    Encoding matches ``write_index`` (content.py) exactly -- ``json.dump``
    with ``indent=2, ensure_ascii=False``, then a trailing newline written
    by hand -- for the same reason: Go and Python must produce identical
    bytes. An empty set still encodes as ``[]``, never ``null``.

    The write itself goes to ``path + ".new"`` and is then renamed into
    place, the same insurance install.sh takes over the launcher (it writes
    to a temp name and renames it into place) -- a crash or a power cut mid
    write leaves the old, still-valid file where it was instead of a
    half-written one.
    """
    payload = {"read": sorted(ids)}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".new"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)

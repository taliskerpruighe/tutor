#!/usr/bin/env python3
"""Entry point for the tutor TUI.

    tutor              open the course
    tutor <words>      open it with a search already running
    tutor index        rebuild content/index.json
    tutor doctor       check the install and report what is wrong
    tutor --version

Runs equally as ``python3 tui/tutor.py`` and ``python3 -m tui.tutor``; the
launcher installed on PATH uses the former, and the import shim below is what
makes that work without installing a package.

The two headless views the parity harness diffs are modules of their own, not
subcommands here — anything unrecognised on this command line is a search
query, so they have to be:

    python3 -m tui.render <file.md> [width]        one article
    python3 -m tui.frame <cols> <rows> [id] …      a whole screen
"""

import os
import sys

if __package__ in (None, ""):  # invoked as a plain script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tui import content, state, term
    from tui.app import App
else:
    from . import content, state, term
    from .app import App

VERSION = "0.2.10"

MIN_PYTHON = (3, 9)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------------
# Subcommands
# --------------------------------------------------------------------------


def cmd_index(root):
    index = content.write_index(root)
    parts = index.get("parts", [])
    total = sum(len(p.get("articles", [])) for p in parts)
    print("Indexed %d article%s across %d part%s -> %s"
          % (total, "" if total == 1 else "s",
             len(parts), "" if len(parts) == 1 else "s",
             os.path.relpath(content.index_path(root), root)))
    for part in parts:
        print("  %-24s %d" % (part["title"], len(part.get("articles", []))))
    return 0


def cmd_doctor(root):
    checks = []

    ok_py = sys.version_info >= MIN_PYTHON
    checks.append((ok_py, "python %d.%d" % sys.version_info[:2],
                   "need %d.%d or newer — run: xcode-select --install" % MIN_PYTHON))

    content_dir = content.content_dir(root)
    ok_content = os.path.isdir(content_dir)
    checks.append((ok_content, "content/ found at %s" % content_dir,
                   "no content/ directory — is TUTOR_HOME right?"))

    index = content.load_index(root) if ok_content else {"parts": []}
    total = sum(len(p.get("articles", [])) for p in index.get("parts", []))
    checks.append((total > 0, "%d article%s in %d part%s"
                   % (total, "" if total == 1 else "s",
                      len(index.get("parts", [])), "" if len(index.get("parts", [])) == 1 else "s"),
                   "no articles found under content/"))

    ok_index = os.path.exists(content.index_path(root))
    checks.append((ok_index, "content/index.json present",
                   "index missing — run: tutor index"))

    launcher = os.path.expanduser("~/.local/bin/tutor")
    ok_launcher = os.path.isfile(launcher)
    checks.append((ok_launcher, "launcher at %s" % launcher,
                   "not installed — run: bash %s" % os.path.join(root, "install.sh")))

    bindir = os.path.dirname(launcher)
    ok_path = any(os.path.abspath(p) == bindir for p in os.environ.get("PATH", "").split(os.pathsep) if p)
    checks.append((ok_path, "%s is on PATH" % bindir,
                   "%s is not on PATH — open a new terminal, or run: bash %s"
                   % (bindir, os.path.join(root, "install.sh"))))

    failures = 0
    for ok, good, bad in checks:
        if ok:
            print("  ok    %s" % good)
        else:
            failures += 1
            print("  FAIL  %s" % bad)

    # Not a check. An agent runs doctor from a tool call, where there is no tty
    # by definition; counting that as a failure would send it chasing a
    # problem that does not exist.
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("  note  no terminal attached here — run `tutor` in a terminal of its own")

    print()
    if failures:
        print("%d check%s failed." % (failures, "" if failures == 1 else "s"))
    else:
        print("All good. Run `tutor` to start.")
    return 1 if failures else 0


def cmd_run(root, query=None):
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        # Claude Code owns its own terminal, so an agent calling this from a
        # tool would otherwise hang forever waiting on a keypress. Say what to
        # do instead of failing silently.
        sys.stderr.write(
            "tutor needs a terminal of its own.\n\n"
            "Open a new terminal window or tab and run:\n\n"
            "    tutor\n\n"
        )
        return 1

    index = content.load_index(root)
    app = App(root, index, query)
    app.read_path = state.marks_path()
    app.read = state.load_marks(app.read_path)
    app.installed = state.load_installed(state.installed_path())
    with term.Terminal() as terminal:
        app.run(terminal)
    return 0


# --------------------------------------------------------------------------


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = os.environ.get("TUTOR_HOME") or repo_root()

    if argv and argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0
    if argv and argv[0] in ("-V", "--version", "version"):
        print("tutor %s" % VERSION)
        return 0
    if argv and argv[0] == "index":
        return cmd_index(root)
    if argv and argv[0] == "doctor":
        return cmd_doctor(root)
    if argv and argv[0] == "run":
        argv = argv[1:]

    if sys.version_info < MIN_PYTHON:
        sys.stderr.write("tutor needs Python %d.%d or newer.\n" % MIN_PYTHON)
        return 1

    return cmd_run(root, " ".join(argv) if argv else None)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)

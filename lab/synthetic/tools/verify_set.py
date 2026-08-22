#!/usr/bin/env python3
"""verify_set.py — the set-level barrier across all six clients.

    python3 verify_set.py [--outdir-pattern PATTERN]

Checks:
   1  LEAKAGE — the four-filter, whole-token scan of SPEC-DELTA D-F / D-J, run
      over the masterkeys AND over the rendered page text of every packet.
   2  registry collisions — no two clients share an identifier
   3  coverage matrix — both bases, every conditional trigger exercised,
      six distinct voices, demonstrated-before-tested

THE LEAKAGE ALGORITHM IS NOT NEW. It is validate_masterkeys.py's section 11,
copied faithfully (its four filters, its ALWAYS_FLAG set, its
blocklist-exclusions.txt). SPEC-DELTA D-J is explicit that a third independent
leakage algorithm is worse than a copied one: a scan that red-lights every
client on every run is a scan nobody reads, and two derivations of one rule is
how a verifier ends up agreeing with a renderer's shared mistake. The only
extension here is the SURFACE — this one also reads the rendered PDFs, which
is what actually ships.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

import yaml

import mklib

FAILS, WARNS, OKS = [], [], []


def ok(c, m):   OKS.append(f"[ok]   {c}: {m}")
def fail(c, m): FAILS.append(f"[FAIL] {c}: {m}")
def warn(c, m): WARNS.append(f"[warn] {c}: {m}")


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}.{i}")
    else:
        yield path, o


# =====================================================================
# 1. LEAKAGE — validate_masterkeys.py section 11, copied faithfully
# =====================================================================
def form_vocab():
    v = set()
    for f in ("n-400.pdf", "f1040.pdf", "f1040--2024.pdf"):
        fp = os.path.join(mklib.BLANKS, f)
        if not os.path.exists(fp):
            continue
        t = subprocess.run(["pdftotext", "-layout", fp, "-"],
                           capture_output=True, text=True).stdout
        v |= {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", t)}
    return v


def spec_vocab():
    fp = os.path.join(mklib.SPEC, "STYLE-SPEC.md")
    t = open(fp).read() if os.path.exists(fp) else ""
    sec = t[t.index("## 11."):t.index("## 12.")] if "## 11." in t and "## 12." in t else t
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", sec)}


def english_words():
    """Any ordinary English word is excused: it cannot be a distinctive corpus
    identifier. Verified discrimination (D-J): this list contains 'engineering',
    'circuit', 'pharmacy', 'republic', 'district' and 'seal', and does NOT
    contain 'Oliveira', 'Izaguirre', 'Zhu' or 'Symple'."""
    for fp in ("/usr/share/dict/words", "/usr/share/dict/linux.words"):
        if os.path.exists(fp):
            return {w.strip().lower() for w in open(fp, errors="ignore")
                    if len(w.strip()) > 2}
    warn("SET", "no system wordlist — leakage scan is weaker than D-J specifies")
    return set()


# Force-flagged whatever the dictionary says: the corpus's own distinctive
# nouns. 'Malone' IS an ordinary dictionary word and would otherwise be excused.
ALWAYS_FLAG = {"oliveira", "izaguirre", "symple", "trysymple", "ossola", "ylenia",
               "luwilyn", "xuying", "zhu", "malone", "jacobs", "garth", "braun",
               "nowakowski", "paz", "vivian", "brent", "kyle", "jesus", "marcel"}


def exclusions():
    fp = os.path.join(mklib.TOOLS, "blocklist-exclusions.txt")
    if not os.path.exists(fp):
        return set()
    return {l.strip().lower() for l in open(fp)
            if l.strip() and not l.startswith("#")}


def lockbox_vocab():
    """Every token of every lockbox block, all four boxes x both carriers.

    STYLE-SPEC §11 lists the lockbox blocks as strings the house style REQUIRES
    every packet to contain, and §7 makes them f(state, carrier). But filters
    (2) and (3) only ever admitted ALPHABETIC vocabulary, so the ZIPs and box
    numbers -- 60603, 60680, 4060, 21251 -- were never excused, and the cover
    letter was red-flagged on four clients out of six for printing the address
    it is required to print. SPEC-DELTA D-F: that is an exclusion-set bug to be
    recorded, not a halt.

    Derived from mklib.lockbox_block, which is the one place §7's table lives,
    so this cannot drift from what the cover letter actually renders.
    """
    v = set()
    for box in mklib.LOCKBOX_STATES:
        state = mklib.LOCKBOX_STATES[box][0]
        for carrier in mklib.CARRIERS:
            for line in mklib.lockbox_block(state, carrier):
                for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", line):
                    v.add(tok.lower())
                    for part in re.split(r"[-]", tok):
                        if part:
                            v.add(part.lower())
    return v


ALLOW = (form_vocab() | spec_vocab() | english_words() | exclusions()
         | lockbox_vocab())
ALLOW |= {w.lower() for w in re.findall(
    r"[A-Za-z]{3,}",
    open(os.path.join(mklib.TEMPLATES, "document-catalog.yaml")).read())}


def allowed(tok):
    t = tok.lower().strip()
    if t in ALWAYS_FLAG:
        return False
    if t in ALLOW:
        return True
    t = re.sub(r"[’']s$", "", t)
    if t in ALLOW:
        return True
    parts = [x for x in re.split(r"[-/]", t) if x]
    return bool(parts) and all(x in ALLOW for x in parts)


FACTY = re.compile(r"(name|street|address|city|employer|school|occupation|email|"
                   r"phone|telephone|number|ssn|court|judge|clerk|docket|police|"
                   r"insurer|policy|instrument|county|issuer|authority|preparer|"
                   r"grantor|grantee|title|domain|slug|password)", re.I)
NOISE = re.compile(r"^_authored_notes|^consistency_locks|^input_surfaces|^mess_events|"
                   r"_derived|\.why$|\.note$|\.notes$|\.text$|\.explanation$|"
                   r"\.reconciliation$|\.lock$|\.detail$|\.desc|comment", re.I)

BLOCKED = {l.strip().lower() for l in open(os.path.join(mklib.ROOT, "blocklist.txt"))
           if len(l.strip()) >= 4}


def scan_masterkey(slug, mk):
    hits, excused = set(), set()
    for p, v in walk(mk):
        if not isinstance(v, str) or NOISE.search(p) or not FACTY.search(p):
            continue
        for tok in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}|\d{5,}", v):
            if tok.lower() not in BLOCKED:
                continue
            (excused if allowed(tok) else hits).add((tok, p))
    for p, v in walk(mk):
        if isinstance(v, str) and not NOISE.search(p) and FACTY.search(p) \
           and 4 <= len(v) <= 60 and v.strip().lower() in BLOCKED \
           and not all(allowed(w) for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", v)):
            hits.add((v.strip(), p + " [whole value]"))
    return hits, excused


def scan_text(label, text):
    """The same token rule, applied to what actually ships: rendered page text.

    There is no path to filter on here, so every token is in scope; the three
    vocabulary filters carry the whole load, exactly as D-J intends.
    """
    hits, excused = set(), set()
    for tok in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}|\d{5,}", text):
        if tok.lower() not in BLOCKED:
            continue
        (excused if allowed(tok) else hits).add((tok, label))
    return hits, excused


# =====================================================================
def main(outdir_for):
    keys = {s: mklib.load_masterkey(s) for s in mklib.all_slugs()}
    registry = yaml.safe_load(open(os.path.join(mklib.ROOT, "registry.yaml")))
    reg = {c["slug"]: c for c in registry["clients"]}

    # ------------------------------------------------ 1 leakage
    for slug, mk in keys.items():
        hits, excused = scan_masterkey(slug, mk)
        if hits:
            fail(slug, f"LEAKAGE in masterkey — {len(hits)} distinctive blocklist "
                       f"token(s): {sorted(hits)[:8]}")
        else:
            ok(slug, f"masterkey leakage: 0 distinctive hits "
                     f"({len(excused)} house-style token(s) excused per §11)")

    scanned_pages = 0
    for slug, mk in keys.items():
        outdir = outdir_for(slug)
        hits, excused = set(), set()
        pdfs = []
        for d in mklib.doc_entries(mk):
            pdfs += [mklib.component_path(outdir, d, "pdf"),
                     mklib.divider_path(outdir, d)]
        pdfs.append(os.path.join(outdir, "00. Applicant Cover Page.pdf"))
        found = [p for p in pdfs if os.path.exists(p)]
        if not found:
            warn(slug, "no rendered pdf components — packet leakage not scanned")
            continue
        for p in found:
            h, e = scan_text(os.path.basename(p), mklib.pdf_text(p))
            hits |= h
            excused |= e
        scanned_pages += len(found)
        if hits:
            fail(slug, f"LEAKAGE in rendered output — {len(hits)} token(s): "
                       f"{sorted(hits)[:8]}")
        else:
            ok(slug, f"rendered-output leakage: 0 distinctive hits across "
                     f"{len(found)} component(s) ({len(excused)} excused)")

    # ------------------------------------------------ 2 registry collisions
    IDENTIFIERS = {
        "a_number": lambda k: k["immigration"]["a_number"],
        "ssn": lambda k: k["identity"].get("ssn"),
        "email": lambda k: k["contact"].get("email"),
        "daytime_phone": lambda k: k["contact"].get("daytime_phone"),
        "full_legal_name": lambda k: mklib.full_legal_name(k),
        "family_name": lambda k: k["identity"]["family_name"],
        "passport_number": lambda k: (k["documents"].get("applicant_passport") or {}).get("number"),
        "current_address": lambda k: ", ".join(
            str([a for a in k["addresses"] if a.get("present")][0].get(f) or "")
            for f in ("street", "city", "state", "zip")),
    }
    for label, fn in IDENTIFIERS.items():
        seen = {}
        for slug, mk in keys.items():
            try:
                v = fn(mk)
            except Exception:
                v = None
            if not v:
                continue
            seen.setdefault(str(v).strip().lower(), []).append(slug)
        dupes = {v: s for v, s in seen.items() if len(s) > 1}
        if dupes:
            fail("SET", f"registry collision on {label}: {dupes}")
        else:
            ok("SET", f"no collision on {label} across {len(seen)} client value(s)")

    for slug, mk in keys.items():
        r = reg.get(slug)
        if not r:
            fail(slug, "no registry entry")
            continue
        pairs = [("a_number", r["immigration"]["a_number"], mk["immigration"]["a_number"]),
                 ("basis", r["immigration"]["basis"], mk["immigration"]["basis"]),
                 ("lockbox", r["residence"]["lockbox"], mk["matter"]["lockbox"]),
                 ("carrier", r["residence"]["carrier"], mk["matter"]["carrier"]),
                 ("state", r["residence"]["state"], mklib.residence_state(mk))]
        bad = [(l, a, b) for l, a, b in pairs if str(a) != str(b)]
        if bad:
            fail(slug, f"registry/masterkey disagree: {bad}")
        else:
            ok(slug, "registry and masterkey agree on the facts both hold")

    # ------------------------------------------------ 3 coverage matrix
    bases = {mklib.basis_key(mk) for mk in keys.values()}
    if bases != {"316a", "319a"}:
        fail("SET", f"coverage: bases exercised = {sorted(bases)}, need both")
    else:
        ok("SET", "coverage: both bases exercised (316(a) and 319(a))")

    TRIG = ["c1_fires", "c2_fires", "c3a_fires", "c3b_fires", "c3c_fires",
            "c4_fires", "c5_fires", "c6_fires"]
    fired = {t: [s for s, k in keys.items() if (k.get("rule_inputs") or {}).get(t)]
             for t in TRIG}
    never = [t for t, s in fired.items() if not s]
    if never:
        fail("SET", f"coverage: conditional trigger(s) never exercised: "
                    f"{[t[:-6].upper() for t in never]}")
    else:
        ok("SET", "coverage: all eight conditional triggers C1-C6 exercised "
                  + ", ".join(f"{t[:-6].upper()}={len(s)}" for t, s in fired.items()))

    voices = {s: (reg.get(s) or {}).get("voice_register") for s in keys}
    distinct = {v for v in voices.values() if v}
    if len(distinct) != len(keys):
        fail("SET", f"coverage: {len(distinct)} distinct voice registers for "
                    f"{len(keys)} clients: {voices}")
    else:
        ok("SET", f"coverage: {len(distinct)} distinct voice registers, one per client")

    # demonstrated-before-tested, at TRIGGER-FAMILY level (validate_masterkeys §9)
    FAMILY = {"c1_fires": "C1", "c2_fires": "C2", "c3a_fires": "C3",
              "c3b_fires": "C3", "c3c_fires": "C3", "c4_fires": "C4",
              "c5_fires": "C5", "c6_fires": "C6"}
    worked = set()
    for s, k in keys.items():
        if str(k.get("ships_as", "")).startswith("example"):
            worked |= {FAMILY[t] for t in TRIG if (k.get("rule_inputs") or {}).get(t)}
    for s, k in keys.items():
        if str(k.get("ships_as", "")).startswith("example"):
            continue
        fams = {FAMILY[t] for t in TRIG if (k.get("rule_inputs") or {}).get(t)}
        undem = fams - worked
        if undem:
            fail(s, f"uses trigger families never demonstrated in a worked pair: "
                    f"{sorted(undem)}")
        else:
            ok(s, f"demonstrated-before-tested holds "
                  f"({','.join(sorted(fams)) or 'core only'})")

    # exhibit sets pairwise distinct (BUILD-PLAN §7)
    CORE = {"table_of_contents", "cover_letter", "n400", "applicant_passport",
            "green_card", "tax_return"}
    sets = {s: frozenset(d["id"] for d in mklib.doc_entries(k)) - CORE
            for s, k in keys.items()}
    pairs = list(sets.items())
    dupes = [(a, b) for i, (a, sa) in enumerate(pairs) for b, sb in pairs[i + 1:]
             if sa == sb]
    if dupes:
        for a, b in dupes:
            fail("SET", f"{a} and {b} have identical conditional sets (BUILD-PLAN §7)")
    else:
        ok("SET", f"all {len(pairs) * (len(pairs) - 1) // 2} client pairs have "
                  f"distinct conditional exhibit sets")

    if scanned_pages:
        ok("SET", f"leakage scan covered {scanned_pages} rendered page component(s)")


if __name__ == "__main__":
    pattern = None
    if "--outdir-pattern" in sys.argv:
        pattern = sys.argv[sys.argv.index("--outdir-pattern") + 1]

    def outdir_for(slug):
        if pattern:
            return pattern.replace("{slug}", slug)
        return os.path.join(mklib.CLIENTS, slug, "output")

    main(outdir_for)
    print("\n".join(OKS))
    if WARNS:
        print()
        print("\n".join(WARNS))
    if FAILS:
        print()
        print("\n".join(FAILS))
        print(f"\n=== SET RED: {len(FAILS)} failure(s), {len(WARNS)} warning(s) ===")
        sys.exit(1)
    print(f"\n=== SET GREEN: {len(OKS)} checks passed, {len(WARNS)} warning(s) ===")

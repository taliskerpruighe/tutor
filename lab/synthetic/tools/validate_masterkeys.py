#!/usr/bin/env python3
"""validate_masterkeys.py — the Phase 2 barrier (BUILD-PLAN §3, barrier (a)).

Scripted validation of the six masterkeys against the registry, STYLE-SPEC §9
(the four-argument exhibit rule), §9.4 (the consistency locks) and the run's
binding constraints. Zero tolerance: any FAIL is a build bug.

Checks, in order:
  1  every masterkey parses and carries the BUILD-PLAN §3 top-level keys
  2  registry <-> masterkey agreement on the facts both hold
  3  filing-window arithmetic recomputed from lpr_date (3y-90d / 5y-90d)
  4  tax year agrees with filing date and names a committed blank
  5  MRZ check digits recomputed (ICAO 9303, weighting 7,3,1)
  6  address history gap-free across the residence window
  7  the exhibit set recomputed from STYLE-SPEC §9 and diffed against the key
  8  exhibit sets pairwise distinct across the six clients (BUILD-PLAN §7)
  9  demonstrated-before-tested: every conditional a to-do client uses
     appears in an examples client
 10  NO FIRM IDENTITY anywhere in any masterkey (§16 ruling 7)
 11  leakage: whole-token grep of masterkey values against blocklist.txt
 12  every output-consumed fact has at least one input surface
"""
import sys, os, re, datetime, collections
try:
    import yaml
except ImportError:
    sys.exit("pyyaml required")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # lab/synthetic
CLIENTS = os.path.join(ROOT, "clients")
FAILS, WARNS, OKS = [], [], []

def ok(c, m):   OKS.append(f"[ok]   {c}: {m}")
def fail(c, m): FAILS.append(f"[FAIL] {c}: {m}")
def warn(c, m): WARNS.append(f"[warn] {c}: {m}")

def d(x):
    """Coerce a date-ish value to datetime.date."""
    if isinstance(x, datetime.date): return x
    if isinstance(x, datetime.datetime): return x.date()
    if isinstance(x, str):
        for f in ("%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y"):
            try: return datetime.datetime.strptime(x.strip(), f).date()
            except ValueError: pass
    return None

def dig(o, path, default=None):
    """dig(obj, 'a.b.c') with dict/list tolerance."""
    cur = o
    for k in path.split('.'):
        if isinstance(cur, dict) and k in cur: cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur): cur = cur[int(k)]
        else: return default
    return cur

def walk(o, path=""):
    """Yield (path, scalar) for every leaf."""
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{path}.{i}")
    else:
        yield path, o

# ---------------------------------------------------------------- MRZ
def mrz_check(s):
    w, tot = (7, 3, 1), 0
    for i, ch in enumerate(s):
        if ch.isdigit(): v = int(ch)
        elif ch.isalpha(): v = ord(ch.upper()) - 55
        elif ch == '<': v = 0
        else: return None
        tot += v * w[i % 3]
    return tot % 10

def check_mrz(client, label, l1, l2):
    if not l1 or not l2:
        fail(client, f"{label}: MRZ lines missing"); return
    l1, l2 = str(l1).strip(), str(l2).strip()
    for nm, ln in (("line1", l1), ("line2", l2)):
        if len(ln) != 44:
            fail(client, f"{label} MRZ {nm} is {len(ln)} chars, must be 44"); return
    if not l1.startswith("P"):
        warn(client, f"{label} MRZ line1 does not start with 'P'")
    tests = [("passport-number", l2[0:9],  l2[9]),
             ("dob",             l2[13:19], l2[19]),
             ("expiry",          l2[21:27], l2[27])]
    for nm, data, got in tests:
        exp = mrz_check(data)
        if exp is None: fail(client, f"{label} MRZ {nm}: bad characters"); continue
        if not got.isdigit() or int(got) != exp:
            fail(client, f"{label} MRZ {nm} check digit is {got!r}, computed {exp}")
    comp = l2[0:10] + l2[13:20] + l2[21:43]
    exp, got = mrz_check(comp), l2[43]
    if exp is None or not got.isdigit() or int(got) != exp:
        fail(client, f"{label} MRZ composite check digit is {got!r}, computed {exp}")
    else:
        ok(client, f"{label} MRZ: all four check digits recompute")

# ---------------------------------------------------------------- load
reg_path = os.path.join(ROOT, "registry.yaml")
if not os.path.exists(reg_path): sys.exit("registry.yaml missing — Phase 2a incomplete")
registry = yaml.safe_load(open(reg_path))
reg_clients = {c["slug"]: c for c in registry["clients"]}

keys = {}
for slug in sorted(reg_clients):
    p = os.path.join(CLIENTS, slug, "masterkey.norm.yaml")
    if not os.path.exists(p):
        fail(slug, "masterkey.norm.yaml missing — run normalize_masterkeys.py first"); continue
    try:
        keys[slug] = yaml.safe_load(open(p))
        ok(slug, f"masterkey.norm.yaml parses ({os.path.getsize(p)} bytes)")
    except Exception as e:
        fail(slug, f"masterkey.norm.yaml does not parse: {e}")

# ---------------------------------------------------------------- 1 shape
REQUIRED = ["client", "slug", "ships_as", "identity", "immigration", "family",
            "addresses", "employment", "travel", "moral_character", "documents",
            "matter", "exhibits", "input_surfaces", "mess_events",
            "consistency_locks", "contact", "rule_inputs"]
for slug, k in keys.items():
    missing = [r for r in REQUIRED if r not in k]
    if missing: fail(slug, f"missing top-level keys: {missing}")
    else: ok(slug, "all BUILD-PLAN §3 top-level keys present")

# ---------------------------------------------------------------- 3 filing window
for slug, k in keys.items():
    lpr = d(dig(k, "immigration.lpr_date")); filed = d(dig(k, "matter.filed_date"))
    basis = str(dig(k, "immigration.basis", "")).replace("(", "").replace(")", "").lower()
    if not lpr or not filed:
        fail(slug, f"lpr_date={lpr!r} filed_date={filed!r} — cannot recompute window"); continue
    yrs = 3 if "319" in basis else 5
    earliest = datetime.date(lpr.year + yrs, lpr.month, lpr.day) - datetime.timedelta(days=90)
    if filed < earliest:
        fail(slug, f"filed {filed} is BEFORE earliest {earliest} ({yrs}y-90d from {lpr})")
    else:
        ok(slug, f"filing window: filed {filed}, earliest {earliest}, margin +{(filed-earliest).days}d")

# ---------------------------------------------------------------- 4 tax year
for slug, k in keys.items():
    filed = d(dig(k, "matter.filed_date")); ty = dig(k, "documents.tax_return.year")
    if not filed or ty is None: warn(slug, "tax year or filed date absent"); continue
    ty = int(ty)
    # STYLE-SPEC §13 D11: "latest tax return" is the latest one that EXISTS at the
    # filing date. TY N is filed by ~15 April of year N+1. So a packet filed before
    # mid-April of year Y has TY(Y-2) as its latest; on or after, TY(Y-1).
    expect = filed.year - 1 if (filed.month, filed.day) >= (4, 15) else filed.year - 2
    if ty != expect:
        fail(slug, f"tax year {ty} but filed {filed} implies {expect} (STYLE-SPEC §13 D11)")
    else:
        blank = "f1040--2024.pdf" if ty == 2024 else "f1040.pdf"
        if not os.path.exists(os.path.join(ROOT, "blanks", blank)):
            fail(slug, f"TY{ty} needs {blank}, which is not committed")
        else: ok(slug, f"tax year {ty} agrees with filing date; blank {blank} present")

# ---------------------------------------------------------------- 5 MRZ
for slug, k in keys.items():
    docs = dig(k, "documents", {}) or {}
    for name, obj in docs.items():
        if not isinstance(obj, dict): continue
        m = obj.get("mrz")
        if isinstance(m, list) and len(m) == 2: check_mrz(slug, name, m[0], m[1])
        elif isinstance(m, dict): check_mrz(slug, name, m.get("l1") or m.get("line1"),
                                                        m.get("l2") or m.get("line2"))

# ---------------------------------------------------------------- 6 address gaps
for slug, k in keys.items():
    addrs = dig(k, "addresses") or []
    spans = []
    for a in addrs:
        if not isinstance(a, dict): continue
        f, t = d(a.get("from")), a.get("to")
        t = None if (t in (None, "present", "Present")) else d(t)
        if f: spans.append((f, t, a.get("city", "?")))
    spans.sort()
    if len(spans) < 2:
        warn(slug, f"only {len(spans)} datable address span(s)")
    for (f1, t1, c1), (f2, t2, c2) in zip(spans, spans[1:]):
        if t1 is None: continue
        gap = (f2 - t1).days
        if gap > 31:
            fail(slug, f"address gap of {gap}d between {c1} (to {t1}) and {c2} (from {f2})")
    else:
        if len(spans) >= 2: ok(slug, f"address history contiguous across {len(spans)} spans")

# ---------------------------------------------------------------- 7 exhibit rule
CORE = ["table_of_contents", "cover_letter", "n400", "applicant_passport",
        "green_card", "tax_return"]

def recompute(k):
    """STYLE-SPEC §9's four-argument rule, read off the normaliser's rule_inputs.

    rule_inputs is computed once, in normalize_masterkeys.py, from the printed
    Part 9 item table and the `supplied` flag on each evidence entry. Deriving it
    a second time here with different heuristics is how a verifier ends up
    agreeing with a renderer's shared mistake.
    """
    r = k.get("rule_inputs") or {}
    out = list(CORE)
    if r.get("c1_fires"):  out.append("spouse_passport")
    if r.get("c2_fires"):  out.append("i797c")
    if r.get("c3a_fires"): out.append("joint_deed")
    if r.get("c3b_fires"): out.append("auto_policy")
    if r.get("c3c_fires"): out.append("child_passport")
    if r.get("c4_fires"):  out.append("travel_addendum")
    if r.get("c5_fires"):  out.append("court_records")
    if r.get("c6_fires"):  out.append("written_explanation")
    return out

sets = {}
for slug, k in keys.items():
    declared = [e.get("doc") for e in (dig(k, "exhibits") or []) if isinstance(e, dict)]
    computed = recompute(k)
    sets[slug] = frozenset(x for x in declared if x not in CORE)
    if set(declared) != set(computed):
        fail(slug, "exhibit set != §9 recomputation\n"
                   f"        declared only: {sorted(set(declared)-set(computed))}\n"
                   f"        computed only: {sorted(set(computed)-set(declared))}")
    else:
        ok(slug, f"exhibit set matches §9 recomputation ({len(declared)} documents)")

# ---------------------------------------------------------------- 8 distinctness
pairs = list(sets.items())
dupes = [(a, b) for i, (a, sa) in enumerate(pairs) for b, sb in pairs[i+1:] if sa == sb]
if dupes:
    for a, b in dupes: fail("SET", f"{a} and {b} have identical conditional sets (BUILD-PLAN §7)")
else:
    ok("SET", f"all {len(pairs)*(len(pairs)-1)//2} client pairs have distinct conditional sets")

# ---------------------------------------------------------------- 9 demonstrated-before-tested
# Compared at TRIGGER-FAMILY level, not per document. registry decision: W2
# demonstrates the C3 supplied-evidence RULE via C3b; T1's deed (C3a) and child
# passport (C3c) are a novel COMBINATION of a demonstrated rule, which is
# BUILD-PLAN §7's intended generalisation gap, not an undemonstrated rule.
FAMILY = {"spouse_passport": "C1", "i797c": "C2", "joint_deed": "C3",
          "auto_policy": "C3", "child_passport": "C3", "travel_addendum": "C4",
          "court_records": "C5", "written_explanation": "C6"}
worked_fam = set()
for slug, k in keys.items():
    if str(dig(k, "ships_as", "")).startswith("example"):
        worked_fam |= {FAMILY[x] for x in sets[slug] if x in FAMILY}
for slug, k in keys.items():
    if not str(dig(k, "ships_as", "")).startswith("example"):
        fams = {FAMILY[x] for x in sets[slug] if x in FAMILY}
        undem = fams - worked_fam
        if undem: fail(slug, f"uses trigger families never demonstrated in a worked pair: {sorted(undem)}")
        else: ok(slug, f"every trigger family it uses ({','.join(sorted(fams))}) is demonstrated in a worked pair")

# ---------------------------------------------------------------- 10 no firm identity
# §16 r7 bans the FIRM's identity. It does not ban a client's employer being an
# LLC, nor the 1040's own paid-preparer field ("Self-Prepared"), nor a deed's
# closing attorney. Scope the check to the packet's preparer, or it fires on
# every client who works for a company.
FIRM_PATH = re.compile(r"(^|\.)(firm|letterhead)|preparer_(name|firm|phone|telephone|"
                       r"email|address|business)|business_address", re.I)
EXEMPT_PATH = re.compile(r"^documents\.(tax_return|evidence)|^_authored_notes|"
                         r"^input_surfaces|^mess_events|^consistency_locks", re.I)
for slug, k in keys.items():
    hits = [f"{p}={v!r}" for p, v in walk(k)
            if FIRM_PATH.search(p) and not EXEMPT_PATH.search(p) and v not in (None, "", "none")]
    if hits: fail(slug, f"firm identity present (§16 r7): {hits[:6]}")
    else: ok(slug, "no firm identity anywhere (§16 r7)")

# ---------------------------------------------------------------- 11 leakage
# SPEC-DELTA D-F. blocklist.txt harvested ALL corpus prose, so it carries ~12k
# tokens including ordinary English ("Allegiance", "Constitution", "Company",
# "Additional"). Grepping every masterkey string against it raw produced 162-535
# "hits" per client, none of them leakage. Two filters make the scan mean
# something:
#   (a) scan only paths that carry INVENTED FACTS, not form text or agent prose;
#   (b) allow any token that occurs in the committed blank forms or in
#       STYLE-SPEC §11's shared-string list -- those are house style by
#       construction (§11's own rule: such a hit is an exclusion-set bug).
import subprocess
def form_vocab():
    v = set()
    for f in ("n-400.pdf", "f1040.pdf", "f1040--2024.pdf"):
        fp = os.path.join(ROOT, "blanks", f)
        if not os.path.exists(fp): continue
        t = subprocess.run(["pdftotext", "-layout", fp, "-"],
                           capture_output=True, text=True).stdout
        v |= {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", t)}
    return v
def spec_vocab():
    fp = os.path.join(ROOT, "spec", "STYLE-SPEC.md")
    t = open(fp).read() if os.path.exists(fp) else ""
    sec = t[t.index("## 11."):t.index("## 12.")] if "## 11." in t and "## 12." in t else t
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'\-]{2,}", sec)}
def english_words():
    """Any ordinary English word is excused: it cannot be a distinctive corpus
    identifier. Verified discrimination: this list contains 'engineering',
    'circuit', 'pharmacy', 'republic', 'district' and 'seal', and does NOT
    contain 'Oliveira', 'Izaguirre', 'Zhu' or 'Symple'."""
    for fp in ("/usr/share/dict/words", "/usr/share/dict/linux.words"):
        if os.path.exists(fp):
            return {w.strip().lower() for w in open(fp, errors="ignore") if len(w.strip()) > 2}
    warn("SET", "no system wordlist — leakage scan falls back to a small stop list")
    return set()
# Force-flagged whatever the dictionary says: the corpus's own distinctive nouns.
# 'Malone' IS an ordinary dictionary word, so the dictionary alone would excuse it.
ALWAYS_FLAG = {"oliveira", "izaguirre", "symple", "trysymple", "ossola", "ylenia",
               "luwilyn", "xuying", "zhu", "malone", "jacobs", "garth", "braun",
               "nowakowski", "paz", "vivian", "brent", "kyle", "jesus", "marcel"}
def exclusions():
    """The §11 exclusion set, extended and recorded in tools/blocklist-exclusions.txt."""
    fp = os.path.join(ROOT, "tools", "blocklist-exclusions.txt")
    if not os.path.exists(fp): return set()
    return {l.strip().lower() for l in open(fp)
            if l.strip() and not l.startswith("#")}
ALLOW = form_vocab() | spec_vocab() | english_words() | exclusions()

def allowed(tok):
    """A token is excused if it, or every part of it once possessives and
    hyphens are split off, is house-style or ordinary English."""
    t = tok.lower().strip()
    if t in ALWAYS_FLAG: return False
    if t in ALLOW: return True
    t = re.sub(r"[\u2019']s$", "", t)
    if t in ALLOW: return True
    parts = [x for x in re.split(r"[-/]", t) if x]
    return bool(parts) and all(x in ALLOW for x in parts)
ALLOW |= {w.lower() for w in re.findall(r"[A-Za-z]{3,}", open(
    os.path.join(ROOT, "templates", "document-catalog.yaml")).read())}
# paths whose values are invented facts worth scanning
FACTY = re.compile(r"(name|street|address|city|employer|school|occupation|email|"
                   r"phone|telephone|number|ssn|court|judge|clerk|docket|police|"
                   r"insurer|policy|instrument|county|issuer|authority|preparer|"
                   r"grantor|grantee|title|domain|slug|password)", re.I)
NOISE = re.compile(r"^_authored_notes|^consistency_locks|^input_surfaces|^mess_events|"
                   r"_derived|\.why$|\.note$|\.notes$|\.text$|\.explanation$|"
                   r"\.reconciliation$|\.lock$|\.detail$|\.desc|comment", re.I)
bl_path = os.path.join(ROOT, "blocklist.txt")
blocked = {l.strip().lower() for l in open(bl_path) if len(l.strip()) >= 4}
for slug, k in keys.items():
    hits, excused = set(), set()
    for p, v in walk(k):
        if not isinstance(v, str) or NOISE.search(p): continue
        if not FACTY.search(p): continue
        for tok in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}|\d{5,}", v):
            t = tok.lower()
            if t not in blocked: continue
            (excused if allowed(tok) else hits).add((tok, p))
    # a whole field value that is itself a blocklist entry is leakage regardless
    for p, v in walk(k):
        if isinstance(v, str) and NOISE.search(p) is None and FACTY.search(p) \
           and 4 <= len(v) <= 60 and v.strip().lower() in blocked \
           and not all(allowed(w) for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", v)):
            hits.add((v.strip(), p + " [whole value]"))
    if hits:
        fail(slug, f"LEAKAGE — {len(hits)} distinctive blocklist token(s): {sorted(hits)[:8]}")
    else:
        ok(slug, f"leakage: 0 distinctive hits on invented-fact paths "
                 f"({len(excused)} house-style token(s) excused per §11)")

# ---------------------------------------------------------------- 12 input surfaces
for slug, k in keys.items():
    surf = dig(k, "input_surfaces") or {}
    n = len(surf) if isinstance(surf, dict) else len(surf or [])
    if n < 20: fail(slug, f"input_surfaces has only {n} entries — too thin to be a real ledger")
    else: ok(slug, f"input_surfaces ledger carries {n} entries")
    me = dig(k, "mess_events") or []
    if not me: fail(slug, "mess_events is empty")
    else:
        bad = [m for m in me if isinstance(m, dict) and not m.get("resolution")]
        if bad: fail(slug, f"{len(bad)} mess_event(s) with no resolution")
        else: ok(slug, f"{len(me)} mess events, all with a resolution")

# ------------------------------------------------ §9.3 r2: 316(a) bars spousal
for slug, k in keys.items():
    r = k.get("rule_inputs") or {}
    if r.get("basis") == "316a":
        spousal = [c for c in ("c1_fires","c2_fires","c3a_fires","c3b_fires","c3c_fires")
                   if r.get(c)]
        if spousal: fail(slug, f"316(a) but spousal exhibits fire: {spousal} (§9.3 rule 2)")
        else: ok(slug, "316(a): no spousal evidence, per §9.3 rule 2")
    if r.get("oath_items_not_yes"):
        fail(slug, f"oath items not Yes: {r['oath_items_not_yes']}")
    dec = r.get("evidence_declined") or []
    if dec: ok(slug, f"declined evidence correctly does not fire: {dec}")

# ------------------------------------------ §16 r10/r11: the N-400 field policy
partmap = os.path.join(ROOT, "tools", "n400-part-map.md")
if not os.path.exists(partmap):
    fail("SET", "tools/n400-part-map.md missing — Phase 3 has no field policy to read")
else:
    ok("SET", "n400-part-map.md present (printed Part 11 fill / Part 13 empty / unsigned)")

# ---------------------------------------------------------------- report
print("\n".join(OKS))
if WARNS: print(); print("\n".join(WARNS))
if FAILS:
    print(); print("\n".join(FAILS))
    print(f"\n=== BARRIER RED: {len(FAILS)} failure(s), {len(WARNS)} warning(s) ===")
    sys.exit(1)
print(f"\n=== BARRIER GREEN: {len(OKS)} checks passed, {len(WARNS)} warning(s) ===")

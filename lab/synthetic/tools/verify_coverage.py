#!/usr/bin/env python3
"""verify_coverage.py — the DIFFERENTIAL COVERAGE SWEEP.

Why this exists, and why the round trip is not enough.

`render_n400.py`'s round trip fills the form from a masterkey, reads the fields
back, and diffs. It reported **0 diffs on all six clients while five real bugs
were shipping**: where a masterkey spelled a fact `cob` and the fieldmap looked
for `country_of_birth`, the renderer wrote nothing, the extractor read nothing,
and the diff compared an absent key against an absent value and called it a
match. Printed Part 2 items 10 and 11 were blank on two clients; Part 1's
"Reason for Filing" — the single most important control on the form — was
UNCHECKED on five of six; Part 4 item 2 answered "No" on five of six, promising
a mailing address that was never supplied.

A self-consistent silence passes any check that only compares intent to result.
What catches it is comparing the six clients **to each other**: they are six
renders of one form by one toolchain, so a field that carries a value for five
clients and is empty for the sixth is a defect until someone explains why.

Two sweeps:
  A. DIFFERENTIAL — any field filled for >= THRESHOLD clients but empty for
     another. Reported per client, with the peers that do fill it.
  B. MUST-FILL — a hand-written list of fields no packet may ever leave blank,
     each identified by *printed* Part (never by /TU tooltip or field-name
     prefix, both of which are unreliable on this blank — see n400-part-map.md).

Exit non-zero on any sweep-A hit that is not in EXPECTED_DIVERGENCE, or on any
sweep-B miss.
"""
import os, sys, re, glob, collections
try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf required")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENTS = os.path.join(ROOT, "clients")
THRESHOLD = 5            # filled for this many peers => expected everywhere

# Fields that legitimately differ between clients, with the rule that explains
# each. Anything here is excused; anything not here is a defect.
EXPECTED_DIVERGENCE = {
    # basis-driven: printed Part 5 items 4.a-8 are gated to 319(a) by the
    # blank's own printed skip instruction, so 316(a) clients leave them blank.
    "spouse": "319(a) only — Part 5 spousal block is skipped for 316(a)",
    "Spouse": "319(a) only",
    "P5_": "319(a) only — Part 5 marital detail",
    # family-shape-driven
    "Child": "only clients with children",
    "P6_": "only clients with children — Part 6 children table",
    # moral-character-driven
    "Part9": "only clients with a Part 9 Yes",
    "Pt9": "only clients with a Part 9 Yes",
    "P9_": "only clients with a Part 9 Yes",
    # travel-driven: the Part 8 table has 6 rows and clients have 3-9 trips
    "P8_": "trip count varies 3-9 across the set",
    "Line8": "trip count varies",
    # name-change is one client only
    "NameChange": "tran_daniel only",
    "P2_Line5": "name-change block — tran_daniel only",
    # prior-address depth varies with the residence window
    "P4_": "address history depth varies with the 3y/5y window",
}

# Printed Part -> fields every client must fill. Identified by printed Part from
# the page text, per n400-part-map.md.
MUST_FILL = [
    ("Part 1  Reason for Filing (eligibility)", ["Part1_Eligibility"]),
    ("Part 2  applicant legal name",            ["P2_Line1_FamilyName", "P2_Line1_GivenName"]),
    ("Part 11 applicant contact (§16 r10)",     ["P12_Line3_Telephone", "P12_Line5_Email"]),
]

# Printed Part 13 preparer + the applicant signature: must be EMPTY (§16 r10/r11)
MUST_BE_EMPTY = ["P15_Line1_Preparer", "P15_Line2_NameofBusinessorOrgName",
                 "P15_Line4_Telephone", "P15_Line5_Mobile", "P15_Line6_Email",
                 "P15_DateofSignature", "P12_SignatureApplicant",
                 "P13_DateofSignature"]

def filled_map(path):
    """Field -> was it given a value.

    RADIO GROUPS ARE COLLAPSED. The N-400 renders a choice like eye colour as
    nine sibling widgets `P7_Line5_Eye[0..8]`, and WHICH index carries the /V
    depends on the answer: Brown lands on [0], Blue on [1]. Treating the
    widgets as independent fields made the first draft of this sweep report
    every client with blue eyes as "missing a field five peers have" — a false
    positive that would have taught the reader to ignore the sweep. Collapse
    each `name[i]` family to `name[]` and call the group filled if ANY widget
    in it is on.
    """
    r = PdfReader(path)
    f = r.get_fields() or {}
    out = {}
    for k, v in f.items():
        base = re.sub(r"\[\d+\]$", "[]", k)
        on = v.get("/V") not in (None, "", "/Off")
        out[base] = out.get(base, False) or on
    return out

def excuse(field):
    for frag, why in EXPECTED_DIVERGENCE.items():
        if frag in field: return why
    return None

def main():
    forms = {}
    for d in sorted(os.listdir(CLIENTS)):
        hits = glob.glob(os.path.join(CLIENTS, d, "output", "**", "*Form N-400*.pdf"),
                         recursive=True)
        if hits: forms[d] = filled_map(hits[0])
    if len(forms) < 2:
        sys.exit(f"need at least 2 rendered N-400s, found {len(forms)}")

    # A field is not "missing" when the fact behind it is legitimately absent:
    # stavros_daphne simply has no middle name. Load each masterkey and let an
    # empty source value excuse an empty field.
    empties = {}
    try:
        import yaml
        for slug in forms:
            mk = yaml.safe_load(open(os.path.join(CLIENTS, slug, "masterkey.norm.yaml")))
            ident = mk.get("identity") or {}
            empties[slug] = {k for k, v in ident.items()
                             if v in ("", None, [], {})}
    except Exception:
        empties = {s: set() for s in forms}

    def fact_is_empty(slug, field):
        f = field.lower()
        for key in empties.get(slug, ()):
            tail = key.split("_")[0]
            if len(tail) > 3 and tail in f: return key
            if key.replace("_", "") in f.replace("_", ""): return key
        return None

    fails, notes = [], []
    print(f"=== coverage sweep over {len(forms)} rendered N-400s ===\n")
    for slug, m in sorted(forms.items()):
        print(f"{slug:16} {sum(m.values()):3} of {len(m)} fields carry a value")

    # ---- sweep A: differential -------------------------------------------
    allf = set().union(*[set(m) for m in forms.values()])
    print(f"\n--- sweep A: differential (a field filled for >={THRESHOLD} peers "
          f"but empty here) ---")
    hits_by_slug = collections.defaultdict(list)
    for fld in sorted(allf):
        who = [s for s, m in forms.items() if m.get(fld)]
        if len(who) >= THRESHOLD:
            for s in forms:
                if not forms[s].get(fld):
                    why = excuse(fld) or (
                        f"masterkey value is empty ({fact_is_empty(s, fld)})"
                        if fact_is_empty(s, fld) else None)
                    if why: notes.append((s, fld, why))
                    else: hits_by_slug[s].append((fld, who))
    if hits_by_slug:
        for s, items in sorted(hits_by_slug.items()):
            for fld, who in items:
                fails.append(f"[FAIL] {s}: {fld.split('.')[-1]} is EMPTY but filled "
                             f"for {len(who)} peers {sorted(set(who) - {s})[:3]}")
    else:
        print("  none — no unexplained blank")
    if notes:
        print(f"  {len(notes)} divergence(s) excused by a stated rule")

    # ---- sweep B: must-fill / must-be-empty -------------------------------
    print("\n--- sweep B: must-fill and must-be-empty ---")
    for slug, m in sorted(forms.items()):
        for label, frags in MUST_FILL:
            for frag in frags:
                match = [k for k in m if frag in k]
                if not match:
                    fails.append(f"[FAIL] {slug}: no field matching {frag!r} exists "
                                 f"({label}) — edition drift, not a pass")
                elif not any(m[k] for k in match):
                    fails.append(f"[FAIL] {slug}: {label} is BLANK ({frag})")
        for frag in MUST_BE_EMPTY:
            match = [k for k in m if frag in k]
            if not match:
                fails.append(f"[FAIL] {slug}: control field {frag!r} does not exist — "
                             f"the emptiness assertion would pass vacuously")
            elif any(m[k] for k in match):
                fails.append(f"[FAIL] {slug}: {frag} is FILLED but §16 r10/r11 "
                             f"require it empty")
    if not fails:
        print("  all must-fill fields carry a value; all must-be-empty fields are empty")

    print()
    if fails:
        print("\n".join(sorted(set(fails))))
        print(f"\n=== COVERAGE RED: {len(set(fails))} failure(s) ===")
        sys.exit(1)
    print(f"=== COVERAGE GREEN: {len(forms)} clients, "
          f"{len(allf)} fields swept, {len(notes)} excused divergence(s) ===")

if __name__ == "__main__":
    main()

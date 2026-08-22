#!/usr/bin/env python3
"""normalize_masterkeys.py — one shape for six masterkeys.

The six Phase 2b agents wrote correct CONTENT in six different SHAPES: `exhibits`
is a bare list in two keys and `{list: [...]}` in four; `travel` is a list, a
`{list:}`, a `{trips:}` and a `{countable_trips:}`; moral-character keys are
`q1` in three and `q_1` in three; `documents.passport` is `applicant_passport`
in one. Renderers must not each re-derive that.

    in : clients/<slug>/masterkey.yaml      (authored, kept as provenance)
    out: clients/<slug>/masterkey.norm.yaml (canonical; the ONLY file downstream reads)

Everything from Phase 3 onward — every renderer, verify_client.py, verify_set.py,
the Phase 4 fabricators, the Phase 5 reviewers — reads `.norm.yaml`. Loading the
raw file downstream is a bug: a missing `on_form` flag silently reads as None,
C4 quietly stops firing, and the verifier compares the packet against the same
wrong recomputation and passes.

Fails loudly, once, here — rather than silently, later, in six contexts.
"""
import sys, os, re, glob, datetime
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS = []

def problem(slug, msg): PROBLEMS.append(f"[{slug}] {msg}")

# --------------------------------------------------------------- alias tables
# Add a line here when a seventh shape appears. Do not scatter `if` branches.
LIST_UNWRAP = {                      # key -> candidate inner keys holding the list
    "exhibits":          ["list", "documents", "items"],
    "travel":            ["list", "trips", "countable_trips", "items"],
    "addresses":         ["list", "history", "items"],
    "employment":        ["list", "history", "items"],
    "mess_events":       ["list", "events", "items"],
    "consistency_locks": ["list", "locks", "items"],
}
DOC_ALIAS = {
    "passport": "applicant_passport",
    "applicant_passport": "applicant_passport",
    "spouse_passport": "spouse_passport",
    "child_passport": "child_passport",
    "green_card": "green_card",
    "tax_return": "tax_return",
    "resume": "resume",
    "evidence": "evidence",
}
CONTACT_ALIAS = {
    "daytime_telephone": "daytime_phone", "daytime_phone": "daytime_phone",
    "telephone": "daytime_phone",
    "mobile_telephone": "mobile_phone",  "mobile_phone": "mobile_phone",
    "mobile": "mobile_phone",
    "email": "email", "email_address": "email",
}

# --------------------------------------------------------- Part 9 item table
# Read off the PRINTED page text of the committed 01/20/25 blank
# (`pdftotext -f 6 -l 11 -layout`), never off the stale /TU tooltips.
#   arrest        -> STYLE-SPEC §9.2 C5, court records
#   part14        -> the form routes the explanation to Part 14, so its own
#                    table cannot carry it: §9.2 C6, written explanation
#   oath          -> Part 12 willingness answers; "Yes" here is NORMAL and must
#                    never be read as a moral-character disclosure
ITEM_CLASS = {
    "15a": "arrest", "15b": "arrest", "16": "arrest",
    "8a": "part14", "8b": "part14", "12": "part14", "20": "part14", "21": "part14",
    "30a": "part14", "30b": "part14",
    "31": "oath", "32": "oath", "34": "oath", "35": "oath", "36": "oath", "37": "oath",
}
ITEM_TEXT = {
    "8a":  "EVER served in, been a member of, assisted, or participated in any military or police unit",
    "8b":  "EVER served in, been a member of, assisted, or participated in any armed group",
    "12":  "EVER received any weapons training, paramilitary training, or other military-type training",
    "15a": "EVER committed, agreed to commit, asked someone else to commit, helped commit, or tried to commit a crime or offense",
    "15b": "EVER been arrested, cited, detained or confined by any law enforcement officer",
    "16":  "If you received a suspended sentence, were placed on probation, or were paroled, have you completed it",
    "20":  "EVER been placed in removal, rescission, or deportation proceedings",
    "21":  "EVER been removed or deported from the United States",
    "31":  "Do you support the Constitution and form of Government of the United States",
    "32":  "Do you understand the full Oath of Allegiance to the United States",
    "34":  "Are you willing to take the full Oath of Allegiance to the United States",
    "35":  "If the law requires it, are you willing to bear arms on behalf of the United States",
    "36":  "If the law requires it, are you willing to perform noncombatant services",
    "37":  "If the law requires it, are you willing to perform work of national importance",
}

def norm_item_key(k):
    """q_15b / q15b / Q_15_b -> 15b"""
    s = str(k).lower().replace("q", "", 1) if str(k).lower().startswith("q") else str(k).lower()
    return re.sub(r"[^0-9a-z]", "", s)

def is_yes(v):
    a = v.get("answer") if isinstance(v, dict) else v
    return str(a).strip().lower() in ("yes", "y", "true")

def unwrap_list(slug, key, val):
    if val is None: return []
    if isinstance(val, list): return val
    if isinstance(val, dict):
        for cand in LIST_UNWRAP.get(key, []) + ["list"]:
            if isinstance(val.get(cand), list):
                return val[cand]
        # a dict-of-dicts used as a list (almeida's consistency_locks)
        if all(isinstance(v, (dict, str)) for v in val.values()):
            out = []
            for k, v in val.items():
                out.append({"lock": k, **v} if isinstance(v, dict) else {"lock": k, "detail": v})
            return out
    problem(slug, f"cannot unwrap {key!r} (type {type(val).__name__}) — add an alias")
    return []

def sidecar(slug, key, val):
    """Everything in a wrapper dict that is NOT the list itself."""
    if not isinstance(val, dict): return {}
    inner = set(LIST_UNWRAP.get(key, [])) | {"list"}
    return {k: v for k, v in val.items() if k not in inner}

def normalise(slug, k):
    n = {}
    n["client"]   = k.get("client", slug)
    n["slug"]     = slug
    n["ships_as"] = k.get("ships_as")
    for passthru in ("identity", "immigration", "family", "matter", "input_surfaces",
                     "documents", "derived", "correspondent", "fee_reduction"):
        if passthru in k: n[passthru] = k[passthru]

    # --- lists -------------------------------------------------------------
    for key in ("exhibits", "travel", "addresses", "employment",
                "mess_events", "consistency_locks"):
        raw = k.get(key)
        n[key] = unwrap_list(slug, key, raw)
        side = sidecar(slug, key, raw)
        # agents also parked metadata in siblings like travel_meta / exhibit_notes
        for extra in (f"{key}_meta", f"{key[:-1]}_notes", f"{key}_notes"):
            if isinstance(k.get(extra), dict): side = {**side, **k[extra]}
        if side: n[f"{key}_derived"] = side

    # --- contact -----------------------------------------------------------
    c = dict(k.get("contact") or {})
    for alt in ("identity", "matter"):
        for kk, vv in (k.get(alt) or {}).items():
            if kk in CONTACT_ALIAS and kk not in c: c[kk] = vv
    n["contact"] = {CONTACT_ALIAS.get(kk, kk): vv for kk, vv in c.items()}
    for req in ("daytime_phone", "mobile_phone", "email"):
        if not n["contact"].get(req):
            problem(slug, f"contact.{req} missing — printed Part 11 items 3/4/5 need it")

    # --- exhibits entries --------------------------------------------------
    # adeyemi wrote {doc: <int seq>, id: <catalog id>}; everyone else wrote
    # {doc: <catalog id>, seq: <int>}. Canonical is doc=<catalog id>, seq=<int>.
    fixed = []
    for e in n["exhibits"]:
        if not isinstance(e, dict): continue
        e = dict(e)
        if isinstance(e.get("doc"), int) and isinstance(e.get("id"), str):
            e["seq"], e["doc"] = e["doc"], e["id"]
        e.setdefault("seq", None)
        fixed.append(e)
    n["exhibits"] = fixed

    # --- documents ---------------------------------------------------------
    docs = {}
    for kk, vv in (k.get("documents") or {}).items():
        docs[DOC_ALIAS.get(kk, kk)] = vv
    tr = docs.get("tax_return")
    if isinstance(tr, dict):
        tr = dict(tr)
        for a, b in (("tax_year", "year"), ("tax_blank", "blank"), ("blank_pdf", "blank")):
            if a in tr and b not in tr: tr[b] = tr.pop(a)
        docs["tax_return"] = tr
    n["documents"] = docs
    if "applicant_passport" not in docs:
        problem(slug, "documents has no applicant passport under any known alias")

    # --- moral character ---------------------------------------------------
    mc, raw_mc = {}, k.get("moral_character") or {}
    if not isinstance(raw_mc, dict):
        problem(slug, "moral_character is not a mapping")
        raw_mc = {}
    for kk, vv in raw_mc.items():
        item = norm_item_key(kk)
        if not re.match(r"^\d", item): continue
        v = dict(vv) if isinstance(vv, dict) else {"answer": vv}
        v["item"] = item
        v["classification"] = ITEM_CLASS.get(item, "standard")
        if item in ITEM_TEXT: v.setdefault("text", ITEM_TEXT[item])
        mc[f"q{item}"] = v
    n["moral_character"] = mc

    # --- the derived booleans the exhibit rule actually needs --------------
    arrests = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "arrest" and is_yes(v))
    part14  = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "part14" and is_yes(v))
    oath_no = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "oath" and not is_yes(v))
    trips = n["travel"]
    on_form = [t for t in trips if isinstance(t, dict) and t.get("on_form") is True]
    trimmed = [t for t in trips if isinstance(t, dict) and t.get("on_form") is False]
    cr  = (k.get("immigration") or {}).get("conditional_resident") or {}
    basis = str((k.get("immigration") or {}).get("basis", "")).lower()
    spousal = "319" in basis
    in_hand = cr.get("unconditional_card_in_hand_at_filing")
    if in_hand is None:                       # kavanagh expressed it by dates
        in_hand = not bool(cr.get("was_cr")) or bool(cr.get("i751_approved_before_filing"))
    # §9.3 rule 3: C3a-C3c are a function of SUPPLIED evidence, not of the basis.
    # An evidence entry carrying `supplied: false` is a deliberate negative control
    # (tran_daniel asks for a joint auto policy and is told there is none) and must
    # NOT fire its exhibit. Reading the type alone here was a real false positive.
    ev = {str(e.get("type", "")).lower() for e in (n["documents"].get("evidence") or [])
          if isinstance(e, dict) and e.get("supplied") is not False}
    ev_declined = {str(e.get("type", "")).lower() for e in (n["documents"].get("evidence") or [])
                   if isinstance(e, dict) and e.get("supplied") is False}
    n["rule_inputs"] = {
        "basis": "319a" if spousal else "316a",
        "was_cr": bool(cr.get("was_cr")),
        "unconditional_card_in_hand_at_filing": bool(in_hand),
        "arrest_items_yes": arrests,
        "part14_items_yes": part14,
        "oath_items_not_yes": oath_no,
        "trip_count": len(trips),
        "trips_on_form": len(on_form),
        "trips_trimmed": len(trimmed),
        "part8_rows": 6,
        "evidence_types": sorted(ev),
        "evidence_declined": sorted(ev_declined),
        "c1_fires": spousal,
        "c2_fires": bool(spousal and cr.get("was_cr") and not in_hand),
        "c3a_fires": bool(spousal and any("deed" in t for t in ev)),
        "c3b_fires": bool(spousal and any(("policy" in t or "auto" in t or "insur" in t) for t in ev)),
        "c3c_fires": bool(spousal and any("child" in t for t in ev)),
        "c4_fires": bool(len(trips) > 6 or len(on_form) > 6 or trimmed),
        "c5_fires": bool(arrests),
        "c6_fires": bool(part14),
    }
    if oath_no:
        problem(slug, f"oath items not Yes: {oath_no} — check before shipping")
    for extra in ("self_check", "_notes", "n400_numbering_note", "disagreements",
                  "leakage", "exhibit_notes", "signature_policy"):
        if extra in k: n.setdefault("_authored_notes", {})[extra] = k[extra]
    return n

def main():
    slugs = sorted(os.path.basename(os.path.dirname(p))
                   for p in glob.glob(os.path.join(ROOT, "clients", "*", "masterkey.yaml")))
    if len(slugs) != 6:
        print(f"expected 6 masterkeys, found {len(slugs)}: {slugs}", file=sys.stderr)
    shapes = {}
    for slug in slugs:
        src = os.path.join(ROOT, "clients", slug, "masterkey.yaml")
        try:
            k = yaml.safe_load(open(src))
        except Exception as e:
            problem(slug, f"does not parse: {e}"); continue
        n = normalise(slug, k)
        dst = os.path.join(ROOT, "clients", slug, "masterkey.norm.yaml")
        with open(dst, "w") as fh:
            fh.write("# GENERATED by tools/normalize_masterkeys.py — do not hand-edit.\n"
                     "# Edit clients/%s/masterkey.yaml and re-run.\n"
                     "# Everything from Phase 3 onward reads THIS file, never the raw one.\n\n" % slug)
            yaml.safe_dump(n, fh, sort_keys=False, allow_unicode=True, width=100, default_flow_style=False)
        shapes[slug] = {kk: (f"list[{len(vv)}]" if isinstance(vv, list)
                             else f"dict[{len(vv)}]" if isinstance(vv, dict) else type(vv).__name__)
                        for kk, vv in n.items()}
        r = n["rule_inputs"]
        fires = [c.upper()[:-6] for c in ("c1_fires","c2_fires","c3a_fires","c3b_fires",
                                          "c3c_fires","c4_fires","c5_fires","c6_fires") if r[c]]
        print(f"{slug:16} {r['basis']}  exhibits={len(n['exhibits']):2}  trips={r['trip_count']:2} "
              f"on_form={r['trips_on_form']}  fires={','.join(fires) or '-'}")

    # prove one shape
    ref = None
    for slug, sh in shapes.items():
        if ref is None: ref, refslug = sh, slug; continue
        diff = {kk for kk in set(ref) | set(sh)
                if ref.get(kk, "-").split("[")[0] != sh.get(kk, "-").split("[")[0]}
        diff -= {"derived", "correspondent", "fee_reduction", "_authored_notes",
                 "exhibits_derived", "travel_derived", "addresses_derived",
                 "employment_derived", "mess_events_derived", "consistency_locks_derived"}
        if diff: problem(slug, f"container types still differ from {refslug} on: {sorted(diff)}")

    print()
    if PROBLEMS:
        print("\n".join("[problem] " + p for p in PROBLEMS))
        print(f"\n=== NORMALISE: {len(shapes)} written, {len(PROBLEMS)} problem(s) ===")
        sys.exit(1)
    print(f"=== NORMALISE GREEN: {len(shapes)} masterkeys, one shape, 0 problems ===")

if __name__ == "__main__":
    main()

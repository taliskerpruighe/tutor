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

def as_day(v):
    """Coerce a trip date to datetime.date, or None."""
    if isinstance(v, datetime.date): return v
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, str):
        for f in ("%Y-%m-%d", "%m/%d/%Y"):
            try: return datetime.datetime.strptime(v.strip(), f).date()
            except ValueError: pass
    return None


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

    # --- passport document number ------------------------------------------
    # Sixth shape collision of this run: almeida and stavros wrote
    # documents.<passport>.number; the other four wrote passport_number. The ID
    # fabricator reads one of them and silently renders a blank MRZ for two
    # clients out of six. CANONICAL IS `number`; `passport_number` is MIRRORED,
    # not dropped, because fabricate_ids.py is being built concurrently against
    # whichever spelling its author happened to read. See RENDER-CONTRACT §2.3.
    for dname, dobj in (n.get("documents") or {}).items():
        if not isinstance(dobj, dict) or "passport" not in dname:
            continue
        num = dobj.get("number") or dobj.get("passport_number")
        if num:
            dobj["number"] = num
            dobj["passport_number"] = num
        elif dname != "evidence":
            problem(slug, f"documents.{dname} has no passport number")

    # --- green card A-number -------------------------------------------------
    # Eighth shape collision, found rendering all six in Phase 3: STYLE-SPEC
    # §9.4 defines the A-number as "9 digits" and locks it identical across
    # immigration.a_number, the green card and every N-400 page header. Two
    # collisions were live at once: the KEY (almeida/kavanagh/tran spell it
    # `a_number`; stavros/adeyemi spell it `uscis_number`) and the VALUE
    # (kavanagh/tran authored it "A-123456789", nowak "A123456789" — a real
    # green card prints the leading "A", but the locked fact is the bare
    # 9 digits, same as immigration.a_number, which is what the N-400 comb
    # field and the cover letter print). CANONICAL IS immigration.a_number,
    # bare digits; `a_number` and `uscis_number` are both MIRRORED to it on
    # documents.green_card, not dropped, for the same reason as the passport
    # number above. A stray leading "A"/"a" and any dash is stripped, never
    # invented — if the digits underneath disagree with immigration.a_number,
    # that is left as a genuine mismatch for verify_client.py to catch.
    gc = (n.get("documents") or {}).get("green_card")
    if isinstance(gc, dict):
        raw_a = gc.get("a_number") or gc.get("uscis_number")
        canon_a = (n.get("immigration") or {}).get("a_number")
        if raw_a is not None:
            stripped = re.sub(r"^[Aa]-?", "", str(raw_a)).strip()
            value = canon_a if canon_a and stripped == canon_a else stripped
            gc["a_number"] = value
            gc["uscis_number"] = value
        elif canon_a:
            problem(slug, "documents.green_card has no a_number/uscis_number "
                          "— falling back to immigration.a_number is NOT done "
                          "automatically; report and fix the masterkey")

    # --- printed Part 3 height and weight -----------------------------------
    # Four shapes for two facts: height as {feet, inches} (almeida, nowak,
    # stavros, adeyemi), height_ft/height_in (kavanagh), height_feet/height_inches
    # (tran); weight_lbs (five) and weight_lb (adeyemi). All six are printed
    # Part 3 items 3 and 4 (STYLE-SPEC §12.1). Canonical:
    # identity.height.{feet,inches} and identity.weight_lbs.
    ident = n.get("identity") or {}
    if ident:
        for _short, _long in (("cob", "country_of_birth"),
                              ("coc", "country_of_citizenship")):
            _v = ident.get(_short) or ident.get(_long)
            if _v:
                ident[_short] = _v
                ident[_long] = _v
            else:
                problem(slug, f"identity.{_short} missing — printed Part 2 needs it")
        if not ident.get("cover_page_cob_con"):
            ident["cover_page_cob_con"] = ident.get("cob")
        h = ident.get("height")
        if not isinstance(h, dict):
            ft = ident.get("height_ft", ident.get("height_feet"))
            inch = ident.get("height_in", ident.get("height_inches"))
            if ft is not None or inch is not None:
                h = {"feet": ft, "inches": inch}
        if isinstance(h, dict):
            ident["height"] = {"feet": h.get("feet"), "inches": h.get("inches")}
        if ident.get("weight_lbs") is None:
            for alt in ("weight_lb", "weight_pounds", "weight"):
                if ident.get(alt) is not None:
                    ident["weight_lbs"] = ident[alt]; break
        for req, label in (("height", "printed Part 3 item 3"),
                           ("weight_lbs", "printed Part 3 item 4"),
                           ("eye_color", "printed Part 3 item 5"),
                           ("hair_color", "printed Part 3 item 6")):
            if not ident.get(req):
                problem(slug, f"identity.{req} missing — {label} has no value")

    # --- three more SILENT collisions, same class as cob/coc ----------------
    # Found by a COVERAGE check (which fieldmap entries produced no value?),
    # not by the round trip: the round trip diffed an absent key against an
    # absent value and reported agreement. Each of these printed a BLANK cell
    # on the N-400 for one or two clients.
    #
    #  * Part 5 item 3, times married: tran wrote times_married_applicant.
    #  * Part 6 children, the name cell: adeyemi and stavros wrote a single
    #    `name`; nowak and tran wrote given_name/middle_name/family_name.
    #  * Part 7, the occupation column: nowak wrote `title`.
    fam = n.get("family") or {}
    if fam.get("times_married") is None:
        for alt in ("times_married_applicant", "applicant_times_married"):
            if fam.get(alt) is not None:
                fam["times_married"] = fam[alt]; break
    # --- printed Part 1 item 1, Reason for Filing ---------------------------
    # ONLY almeida carried part1_eligibility_box. On the other five clients
    # render_n400 read None and checked NO BOX AT ALL -- on the single most
    # important control on the form. Nothing caught it: the round trip agreed
    # (absent vs absent) and the coverage sweep initially only walked text
    # fields, not button groups.
    # The box is a pure function of the basis and the printed page says so:
    #   A = General Provision            -> INA 316(a)
    #   B = Spouse of U.S. Citizen       -> INA 319(a)
    imm = n.get("immigration") or {}
    if not imm.get("part1_eligibility_box"):
        _bs = str(imm.get("basis", "")).lower()
        imm["part1_eligibility_box"] = "B" if "319" in _bs else "A"

    sp2 = fam.get("spouse")
    if isinstance(sp2, dict):
        # adeyemi wrote the spouse as a single `name`; everyone else split it.
        if not sp2.get("full_name") and sp2.get("name"):
            sp2["full_name"] = sp2["name"]
        if sp2.get("full_name") and not sp2.get("name"):
            sp2["name"] = sp2["full_name"]
        _b = str((k.get("immigration") or {}).get("basis", "")).lower()
        if "319" in _b and not (sp2.get("family_name") and sp2.get("given_name")):
            problem(slug, "319(a) spouse lacks family_name/given_name — printed "
                          "Part 5 item 4.a needs them split")

    for kid in (fam.get("children") or []):
        if not isinstance(kid, dict): continue
        nm = kid.get("name") or kid.get("full_name") or " ".join(
            x for x in (kid.get("given_name"), kid.get("middle_name"),
                        kid.get("family_name")) if x)
        if nm:
            kid["name"] = nm
            kid["full_name"] = nm
        else:
            problem(slug, "a child row has no usable name — printed Part 6 needs one")
    for job in (n.get("employment") or []):
        if not isinstance(job, dict): continue
        occ = job.get("occupation") or job.get("title") or job.get("field_of_study")
        if occ:
            job["occupation"] = occ
        elif not re.search(r"not employed|unemploy|homemaker|retired|student",
                           str(job.get("employer", "")), re.I):
            problem(slug, f"employment {job.get('employer')!r} has no occupation "
                          "— printed Part 7 needs one")
        # An unemployment row legitimately has no occupation: the printed Part 7
        # instruction puts "unemployed"/"retired" in the EMPLOYER NAME column,
        # which is where tran's masterkey correctly put it. Its explicit
        # `occupation: null` is a decision, not a gap.
    ide = n.get("identity") or {}
    if ide.get("other_names_used_since_birth") is None:
        ide["other_names_used_since_birth"] = ide.get("other_names_used") or []

    # --- the "is this the current one?" flag -------------------------------
    # Phase 3 gap, same class as D-I. Three shapes were in play: almeida and
    # nowak wrote `present: true`, tran/kavanagh/stavros wrote `current: true`,
    # adeyemi wrote neither and relied on `to: null`. A renderer that reads one
    # spelling gets the wrong lockbox on two clients out of six, silently — the
    # cover letter still renders, it just goes to the wrong lockbox.
    # Canonical key is `present`. `current` is preserved for provenance.
    for key in ("addresses", "employment"):
        for row in n.get(key) or []:
            if not isinstance(row, dict): continue
            flag = row.get("present", row.get("current"))
            if flag is None:
                flag = row.get("to") in (None, "", "present", "Present")
            row["present"] = bool(flag)
        # printed Part 4 item 2: "Is your current physical address also your
        # current mailing address?" Only almeida carried the flag; on the other
        # five `bool(None)` answered NO, which obliges a Part 4 item 3 mailing
        # address that no masterkey has. None of the six has a separate mailing
        # address, so the honest default is YES. A client that ever gains one
        # must set this False AND carry `mailing_address`.
        if key == "addresses":
            for row in n.get(key) or []:
                if isinstance(row, dict) and row.get("present") \
                        and row.get("is_mailing_address") is None:
                    row["is_mailing_address"] = not bool(n.get("mailing_address"))
        rows = [r for r in (n.get(key) or []) if isinstance(r, dict)]
        cur = [r for r in rows if r["present"]]
        if rows and len(cur) != 1:
            problem(slug, f"{key}: {len(cur)} entries flagged present, expected exactly 1")

    # --- the 319(a) spouse the eligibility clause names ---------------------
    # STYLE-SPEC §5.1's 319(a) clause ends "... spouse, {HONORIFIC} {FULL NAME}".
    # Two shapes carried that one fact: tran wrote family.spouse.honorific +
    # family.spouse.full_name; kavanagh wrote the whole rendered string at
    # immigration.eligibility_clause_spouse ("Mr. Liam Patrick Kavanagh") and
    # left the spouse block without an honorific. Canonicalise to the spouse
    # block. A 319(a) client that resolves to neither is a masterkey bug and
    # must stop the build here, not produce a cover letter reading
    # "spouse, None None".
    basis = str((k.get("immigration") or {}).get("basis", "")).lower()
    sp = n.get("family", {}).get("spouse")
    if isinstance(sp, dict):
        if not sp.get("full_name"):
            built = " ".join(x for x in (sp.get("given_name"), sp.get("middle_name"),
                                         sp.get("family_name")) if x)
            if built: sp["full_name"] = built
        blob = str((k.get("immigration") or {}).get("eligibility_clause_spouse") or "")
        m = re.match(r"\s*(Mr\.|Ms\.)\s+(.+?)\s*$", blob)
        if m:
            sp.setdefault("honorific", m.group(1))
            if not sp.get("full_name"): sp["full_name"] = m.group(2)
        if "319" in basis and not (sp.get("honorific") and sp.get("full_name")):
            problem(slug, "319(a) but spouse honorific/full_name unresolvable — "
                          "STYLE-SPEC §5.1's clause names the spouse")
    elif "319" in basis:
        problem(slug, "319(a) but family.spouse is absent")

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

    # --- the Part 9 item-15 arrest detail row -------------------------------
    # Two shapes again: nowak wrote `arrest_detail` with crime_or_offense /
    # offence_date / conviction_or_plea_date; adeyemi wrote `detail_row` with
    # offense / date_of_offense / date_of_conviction_or_plea. Both feed the SAME
    # six printed cells of the item-15 table. Canonical: `arrest_detail`, keys
    # below. Column order on the blank is NOT the field-index order — see
    # fieldmap_n400.yaml part9_arrest_table.
    ARREST_ALIAS = {
        "crime_or_offense": "offense", "offense": "offense", "offence": "offense",
        "offence_date": "offense_date", "date_of_offense": "offense_date",
        "offense_date": "offense_date",
        "conviction_or_plea_date": "conviction_date",
        "date_of_conviction_or_plea": "conviction_date",
        "conviction_date": "conviction_date",
        "place": "place", "disposition": "disposition", "sentence": "sentence",
    }
    for qk, qv in (n.get("moral_character") or {}).items():
        if not isinstance(qv, dict): continue
        row = qv.get("arrest_detail") or qv.get("detail_row")
        if not isinstance(row, dict): continue
        canon = {}
        for kk, vv in row.items():
            canon[ARREST_ALIAS.get(kk, kk)] = vv
        for cell in ("offense", "offense_date", "conviction_date", "place",
                     "disposition", "sentence"):
            canon.setdefault(cell, None)
        qv["arrest_detail"] = canon
        qv.pop("detail_row", None)
        if not (canon["offense"] and canon["offense_date"] and canon["place"]
                and canon["disposition"]):
            problem(slug, f"moral_character.{qk} arrest_detail missing a printed "
                          "cell (offense / offense_date / place / disposition)")


    # --- the derived booleans the exhibit rule actually needs --------------
    arrests = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "arrest" and is_yes(v))
    def _item_sort(i):
        """8a before 12 before 20. A plain sorted() on the label strings gives
        "12" < "20" < "8a", which is how the T2 written explanation came out
        opening on the military-training paragraph instead of the removal
        proceedings — inverting the document's whole point on the first dogfood
        target. Sort on the numeric part, then the letter."""
        m = re.match(r"(\d+)([a-z]*)", i)
        return (int(m.group(1)), m.group(2)) if m else (999, i)
    part14 = sorted((i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "part14" and is_yes(v)),
                    key=_item_sort)
    # An explicit authored order always wins over the numeric default: the
    # written explanation is prose, and which paragraph leads is a judgement
    # the masterkey is entitled to make (stavros_daphne pins [q20, q8a, q12]).
    _struct = (k.get("immigration") or {}).get("written_explanation_structure") or {}
    _order = [str(x).lstrip("q") for x in (_struct.get("order") or [])]
    if _order:
        part14 = ([i for i in _order if i in part14]
                  + [i for i in part14 if i not in _order])
    oath_no = sorted(i for i, v in ((v["item"], v) for v in mc.values())
                     if v["classification"] == "oath" and not is_yes(v))
    trips = n["travel"]
    on_form = [t for t in trips if isinstance(t, dict) and t.get("on_form") is True]
    trimmed = [t for t in trips if isinstance(t, dict) and t.get("on_form") is False]
    # Phase 2 review finding 3: `trips_trimmed` conflated the two C4 disjuncts.
    # A trip can be off the Part 8 table because the table ran out of rows, or
    # because it is a day trip the firm's instruction excludes (registry D7 —
    # a day trip appears on NEITHER the form nor the addendum). Only the first
    # is "trimmed from the form"; split them so Phase 5 can assert each.
    def _is_daytrip(t):
        """STRUCTURAL test: a day trip is one that departs and returns on the
        same date. The first draft substring-matched "day trip" in
        `why_excluded` and was WRONG on tran_daniel and adeyemi_tunde, whose
        overflow trips carry prose saying explicitly "NOT a day trip" — the
        match fired on the negation. Caught by render_addendum.py, which
        cross-checked this block against the trip rows themselves."""
        if t.get("day_trip") is True: return True
        dep, ret = as_day(t.get("depart")), as_day(t.get("return"))
        if dep and ret and dep == ret: return True
        return t.get("days") == 0
    daytrips = [t for t in trips if isinstance(t, dict) and _is_daytrip(t)]
    overflow = [t for t in trimmed if t not in daytrips]
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
        "part14_order_source": ("authored (written_explanation_structure.order)"
                                if _order else "numeric"),
        "oath_items_not_yes": oath_no,
        "trip_count": len(trips),
        "trips_on_form": len(on_form),
        "trips_trimmed": len(trimmed),
        "trips_overflow_from_part8": len(overflow),
        "trips_day_excluded": len(daytrips),
        "part8_rows": 6,
        "evidence_types": sorted(ev),
        "evidence_declined": sorted(ev_declined),
        "c1_fires": spousal,
        "c2_fires": bool(spousal and cr.get("was_cr") and not in_hand),
        "c3a_fires": bool(spousal and any("deed" in t for t in ev)),
        "c3b_fires": bool(spousal and any(("policy" in t or "auto" in t or "insur" in t) for t in ev)),
        "c3c_fires": bool(spousal and any("child" in t for t in ev)),
        "c4_fires": bool(len(trips) > 6 or len(on_form) > 6 or overflow),
        "c4_reason": ("row-count overflow" if (len(trips) > 6 or overflow)
                      else "day-trip trim" if daytrips else "does not fire"),
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

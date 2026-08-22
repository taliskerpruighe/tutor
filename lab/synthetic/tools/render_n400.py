#!/usr/bin/env python3
"""render_n400.py — DOCUMENT 3, Form N-400, from the committed 01/20/25 blank.

Contract: tools/RENDER-CONTRACT.md. Field map: tools/fieldmap_n400.yaml.
Part policy: tools/n400-part-map.md (the ONLY authority; never a /TU tooltip,
never a field-name prefix).

STYLE-SPEC §16 rulings 10 and 11, BINDING:
  * printed Part 11 items 3/4/5 (the applicant's own phone, mobile, email) FILLED
  * printed Part 11 signature and signature date  EMPTY  — the form ships UNSIGNED
  * printed Part 13 preparer block                EMPTY  — no firm identity, ever
  * printed Part 12 interpreter, Parts 15 and 16  EMPTY
Z003 is not used. There is no signature path in this file.

Born-digital (§8): fill with pypdf, delete /XFA, set NeedAppearances.
"""
from __future__ import annotations

import os
import sys

import yaml

import mklib

HANDLES = {"n400"}

FIELDMAP = os.path.join(mklib.TOOLS, "fieldmap_n400.yaml")


# --------------------------------------------------------------- helpers
def _load_fieldmap() -> dict:
    with open(FIELDMAP) as fh:
        return yaml.safe_load(fh)


def _dig(obj, path, default=None):
    cur = obj
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and k.isdigit() and int(k) < len(cur):
            cur = cur[int(k)]
        else:
            return default
    return default if cur is None else cur


def _split_unit(unit):
    """'Apt 3' -> ('Apt', '3'). None -> (None, None)."""
    if not unit:
        return None, None
    parts = str(unit).split(None, 1)
    if len(parts) == 2:
        return parts[0].strip(".").title(), parts[1]
    return None, str(unit)


def _state_opt(state):
    """The /Ch state dropdown's options carry a LEADING SPACE (' MA'), so the
    bare two-letter code does not match an option and the widget stays blank."""
    return f" {str(state).strip().upper()}" if state else None


class _Buttons:
    """Resolve a button group to (field, value) pairs.

    A /Btn on this blank carries exactly ONE appearance state, and the widget
    index does not encode the answer. So: find the sibling whose state is the
    one wanted, set that sibling to its state, and set every other sibling to
    /Off. Never write "Yes", "On" or "/1".
    """

    def __init__(self, blank):
        self.states = mklib.btn_on_states(blank)
        self.siblings = {}
        for name in self.states:
            if name.endswith("]"):
                base, _, idx = name.rpartition("[")
                self.siblings.setdefault(base, []).append(int(idx.rstrip("]")))

    def by_state(self, group, wanted, out):
        idxs = sorted(self.siblings.get(group, []))
        if not idxs:
            raise KeyError(f"button group {group!r} has no widgets on the blank")
        hit = None
        for i in idxs:
            if self.states.get(f"{group}[{i}]") == wanted:
                hit = i
                break
        if hit is None:
            raise ValueError(
                f"{group}: no widget carries state {wanted!r}; "
                f"available {[self.states.get(f'{group}[{i}]') for i in idxs]}")
        for i in idxs:
            out[f"{group}[{i}]"] = wanted if i == hit else "/Off"

    def by_index(self, group, indices, out):
        for i in sorted(self.siblings.get(group, [])):
            st = self.states.get(f"{group}[{i}]")
            out[f"{group}[{i}]"] = st if i in indices else "/Off"

    def clear(self, group, out):
        for i in sorted(self.siblings.get(group, [])):
            out[f"{group}[{i}]"] = "/Off"


# --------------------------------------------------------------- the fill
def build_values(mk: dict) -> dict:
    """Every field this build writes, as {field name: value}. Deterministic."""
    fm = _load_fieldmap()
    btn = _Buttons(mklib.N400_BLANK)
    v: dict = {}
    ident = mk["identity"]
    imm = mk["immigration"]
    fam = mk.get("family") or {}
    spouse = fam.get("spouse") or {}

    # ---- A-number on every page header (§8, §9.4) ------------------------
    for f in fm["a_number_headers"]["fields"]:
        v[f] = str(imm["a_number"])

    # ---- simple text -----------------------------------------------------
    others = ident.get("other_names_used_since_birth") or []
    weight = f"{int(mk['identity']['weight_lbs']):03d}"
    for path, field in fm["text"].items():
        if path.startswith("other_names."):
            _, idx, key = path.split(".")
            row = others[int(idx)] if int(idx) < len(others) else {}
            val = row.get(key) if isinstance(row, dict) else None
        elif path.startswith("identity.weight_lbs."):
            val = weight[int(path.rsplit(".", 1)[1])]
        elif path == "family.children_under_18_count":
            val = _children_under_18(mk)
        else:
            val = _dig(mk, path)
        # The SSN and A-number widgets are 9-character COMB fields: the
        # formatted "037-84-2196" overflows and pypdf truncates it silently.
        if val and path in ("identity.ssn", "family.spouse.a_number"):
            val = "".join(ch for ch in str(val) if ch.isdigit())
        if val not in (None, ""):
            v[field] = str(val)

    for path, field in fm["dates"].items():
        raw = _dig(mk, path)
        if raw:
            v[field] = mklib.fmt_numeric(raw)

    for path, field in fm["countries"].items():
        raw = _dig(mk, path)
        if raw:
            v[field] = str(raw)

    # ---- height (/Ch dropdowns) ------------------------------------------
    h = ident.get("height") or {}
    if h.get("feet") is not None:
        v["form1[0].#subform[2].P7_Line3_HeightFeet[0]"] = str(h["feet"])
    if h.get("inches") is not None:
        v["form1[0].#subform[2].P7_Line3_HeightInches[0]"] = str(h["inches"])

    # ---- button groups ---------------------------------------------------
    cur_addr = _current_address(mk)
    unit_type, unit_number = _split_unit(cur_addr.get("unit"))
    sources = {
        "part1_eligibility": imm.get("part1_eligibility_box"),
        "name_change_requested": bool(_dig(ident, "name_change.requested", False)),
        "sex": ident.get("sex"),
        "ethnicity": ident.get("ethnicity"),
        "race": ident.get("race"),
        "eye_color": ident.get("eye_color"),
        "hair_color": ident.get("hair_color"),
        "current_unit_type": unit_type,
        "mailing_same_as_physical": bool(cur_addr.get("is_mailing_address", True)
                                         if cur_addr.get("is_mailing_address") is not None
                                         else True),
        "mailing_unit_type": None,
        "marital_status": fam.get("marital_status"),
        # printed Part 5 item 2 sits BEFORE the "skip to Part 6" instruction,
        # so every currently-married applicant answers it regardless of basis.
        # No masterkey carries the fact; none of the three married applicants
        # has a service spouse, so it is No when married and blank when not.
        "spouse_armed_forces": (spouse.get("armed_forces")
                                or ("No" if str(fam.get("marital_status", ""))
                                    .lower().startswith("married") else None)),
        "spouse_address_same": spouse.get("address_same_as_applicant"),
        "spouse_usc_when": spouse.get("usc_since"),
    }
    for key, g in fm["button_groups"].items():
        if g.get("by") == "index":
            wanted = sources.get(key) or []
            if isinstance(wanted, str):
                wanted = [wanted]
            idxs = {g["values"][w] for w in wanted if w in g["values"]}
            btn.by_index(g["group"], idxs, v)
            continue
        raw = g["const"] if "const" in g else sources.get(key, g.get("default"))
        if raw is None or raw == "":
            btn.clear(g["group"], v)
            continue
        if raw not in g["values"]:
            raise ValueError(f"button group {key}: masterkey value {raw!r} is not "
                             f"one of {sorted(map(str, g['values']))}")
        btn.by_state(g["group"], g["values"][raw], v)

    # ---- printed Part 5 items 4.a-8 are 319(a)-ONLY ----------------------
    # The printed page (page 4, read with pdftotext -layout) says: "If you are
    # filing under one of the categories below, answer Item Numbers 4.a. - 8.:
    # Spouse of U.S. Citizen, Part 1., Item Number 1.b.; or ... 1.d. If you are
    # not filing under one of the categories above, skip to Part 6."
    # So a 316(a) filer leaves the whole current-spouse block blank EVEN IF
    # MARRIED. adeyemi is 316(a) and married; before this gate his block was
    # blank only by accident (a masterkey key-name mismatch), which is not the
    # same thing as blank by rule. Items 1, 2 and 3 are answered by everyone.
    if str(imm.get("part1_eligibility_box", "")).upper() not in ("B", "D"):
        for path in ("family.spouse.family_name", "family.spouse.given_name",
                     "family.spouse.middle_name", "family.spouse.a_number",
                     "family.spouse.times_married", "family.spouse.employer"):
            if path in fm["text"]:
                v[fm["text"][path]] = ""
        for path in ("family.spouse.dob", "family.marriage_date",
                     "family.spouse.naturalization_date"):
            if path in fm["dates"]:
                v[fm["dates"][path]] = ""
        for key in ("spouse_address_same", "spouse_usc_when"):
            btn.clear(fm["button_groups"][key]["group"], v)

    # ---- printed Part 4, residence --------------------------------------
    c = fm["part4_current_address"]
    v[c["street"]] = _street(cur_addr)
    if unit_number:
        v[c["unit_number"]] = unit_number
    v[c["city"]] = cur_addr["city"]
    v[c["state"]] = _state_opt(cur_addr["state"])
    v[c["zip"]] = str(cur_addr["zip"])
    v[c["country"]] = cur_addr.get("country", "United States")
    v[c["from"]] = mklib.fmt_numeric(cur_addr["from"])
    v[c["to"]] = "PRESENT"

    hist = _prior_addresses(mk)
    hrows = fm["part4_address_history"]["fields"]
    for i in range(1, fm["part4_address_history"]["rows"] + 1):
        f = hrows[i]
        if i > len(hist):
            for k in ("street", "city", "state", "zip", "country", "from", "to"):
                v[f[k]] = ""
            continue
        a = hist[i - 1]
        v[f["street"]] = _street(a, with_unit=True)
        v[f["city"]] = a["city"]
        # NOTE the asymmetry with the current address above, which is correct:
        # the current address's state is a /Ch DROPDOWN whose options carry a
        # leading space (_state_opt), while the history rows' state cells are
        # plain /Tx and take the bare code.
        v[f["state"]] = str(a["state"])
        v[f["zip"]] = str(a["zip"])
        v[f["country"]] = a.get("country", "United States")
        v[f["from"]] = mklib.fmt_numeric(a["from"])
        v[f["to"]] = mklib.fmt_numeric(a["to"]) if a.get("to") else "PRESENT"

    # ---- printed Part 6, children ---------------------------------------
    kids = fam.get("children") or []
    for i, f in fm["part6_children"]["fields"].items():
        i = int(i)
        if i > len(kids):
            for k in ("name", "dob", "residence", "relationship"):
                v[f[k]] = ""
            btn.clear(f["support_group"], v)
            continue
        kid = kids[i - 1]
        v[f["name"]] = kid.get("full_name") or " ".join(
            x for x in (kid.get("given_name"), kid.get("family_name")) if x)
        v[f["dob"]] = mklib.fmt_numeric(kid["dob"]) if kid.get("dob") else ""
        v[f["residence"]] = kid.get("residence", "resides with me")
        v[f["relationship"]] = kid.get("relationship", "biological son or daughter")
        ans = kid.get("providing_support")
        if ans is None:
            btn.clear(f["support_group"], v)
        else:
            btn.by_state(f["support_group"],
                         fm["part6_children"]["support_values"][
                             "Yes" if ans in (True, "Yes") else "No"], v)

    # ---- printed Part 7, employment -------------------------------------
    jobs = _employment(mk)
    for i, f in fm["part7_employment"]["fields"].items():
        i = int(i)
        if i > len(jobs):
            for k in ("employer", "city", "state", "zip", "country", "occupation"):
                v[f[k]] = ""
            if f.get("to"):
                v[f["to"]] = ""
            v[f["from"]] = ""
            continue
        j = jobs[i - 1]
        v[f["employer"]] = j["employer"]
        v[f["city"]] = j.get("city", "")
        v[f["state"]] = str(j.get("state", ""))
        v[f["zip"]] = str(j.get("zip", ""))
        v[f["country"]] = j.get("country", "United States")
        v[f["occupation"]] = j.get("occupation", "")
        v[f["from"]] = mklib.fmt_numeric(j["from"])
        if f.get("to"):
            v[f["to"]] = mklib.fmt_numeric(j["to"]) if j.get("to") else "PRESENT"

    # ---- printed Part 8, travel table (6 rows, most recent first) --------
    trips = _form_trips(mk)
    rows = fm["part8_travel"]["rows"]
    if len(trips) > rows:
        raise ValueError(f"{len(trips)} trips flagged on_form but the table holds "
                         f"{rows} — the masterkey and STYLE-SPEC §9.2 C4 disagree")
    for i, f in fm["part8_travel"]["fields"].items():
        i = int(i)
        if i > len(trips):
            v[f["left"]] = v[f["returned"]] = v[f["countries"]] = ""
            continue
        t = trips[i - 1]
        v[f["left"]] = mklib.fmt_numeric(t["depart"])
        v[f["returned"]] = mklib.fmt_numeric(t["return"])
        v[f["countries"]] = ", ".join(t.get("countries") or [])

    # ---- printed Part 9, every item -------------------------------------
    mc = mk.get("moral_character") or {}
    for item, base in fm["part9_items"].items():
        q = mc.get(f"q{item}")
        ans = q.get("answer") if isinstance(q, dict) else q
        if str(ans).strip() in ("None", "", "null", "N/A", "n/a"):
            btn.clear(base, v)          # gated / not reached
        else:
            btn.by_state(base, fm["part9_item_values"][str(ans)], v)

    # ---- printed Part 9, the item-15 crime/offense table -----------------
    details = [q["arrest_detail"] for k, q in sorted(mc.items())
               if isinstance(q, dict) and isinstance(q.get("arrest_detail"), dict)]
    for i, f in fm["part9_arrest_table"]["fields"].items():
        i = int(i)
        if i > len(details):
            for k in ("offense", "offense_date", "conviction_date", "place",
                      "disposition", "sentence"):
                v[f[k]] = ""
            continue
        d = details[i - 1]
        v[f["offense"]] = d.get("offense") or ""
        v[f["offense_date"]] = mklib.fmt_numeric(d["offense_date"]) if d.get("offense_date") else ""
        v[f["conviction_date"]] = mklib.fmt_numeric(d["conviction_date"]) if d.get("conviction_date") else ""
        v[f["place"]] = d.get("place") or ""
        v[f["disposition"]] = d.get("disposition") or ""
        v[f["sentence"]] = d.get("sentence") or ""

    # ---- printed Part 10, fee reduction: No, and its cells stay empty ----
    p10 = fm["part10_fee_reduction"]
    btn.by_state(p10["answer_group"], p10["answer_values"][p10["answer_const"]], v)
    for f in p10["leave_empty"]:
        v[f] = ""
    for g in p10["leave_empty_groups"]:
        btn.clear(g, v)

    # ---- printed Part 11 items 3/4/5 — FILLED (§16 r10) ------------------
    for path, field in fm["part11_fill"].items():
        val = _dig(mk, path)
        if not val:
            raise ValueError(f"{path} is empty — printed Part 11 item is required "
                             "by §16 ruling 10")
        v[field] = str(val)

    # ---- LEAVE EMPTY — written explicitly, not merely omitted ------------
    # §16 r10 (Part 13 preparer), r11 (unsigned), plus Part 12 and Parts 15/16.
    for group, fields in fm["leave_empty"].items():
        for f in fields:
            v[f] = ""

    return v


# --------------------------------------------------------------- masterkey views
def _current_address(mk):
    for a in mk["addresses"]:
        if a.get("present"):
            return a
    raise ValueError("no present address")


def _prior_addresses(mk):
    prior = [a for a in mk["addresses"] if not a.get("present")]
    return sorted(prior, key=lambda a: str(a.get("from") or ""), reverse=True)


def _street(a, with_unit=False):
    s = a["street"]
    if with_unit and a.get("unit"):
        s = f"{s}, {a['unit']}"
    return s


def _employment(mk):
    jobs = list(mk.get("employment") or [])
    return sorted(jobs, key=lambda j: (j.get("present", False),
                                       str(j.get("from") or "")), reverse=True)


def _form_trips(mk):
    trips = [t for t in (mk.get("travel") or []) if t.get("on_form")]
    return sorted(trips, key=lambda t: str(t["depart"]), reverse=True)


def _children_under_18(mk):
    kids = (mk.get("family") or {}).get("children") or []
    n = (mk.get("family") or {}).get("children_under_18_count")
    return str(n) if n is not None else str(len(kids))


# --------------------------------------------------------------- the contract
def render(masterkey: dict, outdir: str, doc: dict) -> list:
    if doc["id"] not in HANDLES:
        raise ValueError(f"render_n400.py does not handle {doc['id']!r}")
    out = mklib.component_path(outdir, doc, "pdf")
    mklib.fill_acroform(mklib.N400_BLANK, out, build_values(masterkey))
    return [out]


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        mklib.CLIENTS, slug, "output")
    mk = mklib.load_masterkey(slug)
    mklib.ensure_outdir(outdir)
    paths = render(mk, outdir, mklib.doc_by_id(mk, "n400"))
    for p in paths:
        print(f"{mklib.pdf_pagecount(p):>3} pp  {p}")

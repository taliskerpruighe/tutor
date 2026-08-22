#!/usr/bin/env python3
"""render_1040.py — Phase 3 renderer for the `tax_return` DOCUMENT.

Contract: RENDER-CONTRACT.md. Fills the committed blank Form 1040 (pages 1-2)
from `masterkey.norm.yaml`'s `documents.tax_return` fact block, using pypdf's
`update_page_form_field_values` (mklib.fill_acroform), NeedAppearances, and no
/XFA — the same approach the N-400 renderer uses.

Two blanks, two field maps (RENDER-CONTRACT "WHAT TO BUILD"):
  TY2024 -> blanks/f1040--2024.pdf   (2 pp, 155 AcroForm fields)
  TY2025 -> blanks/f1040.pdf         (2 pp, 229 AcroForm fields, IRS draft
                                       redesign: dependents become 4 COLUMNS
                                       instead of 4 ROWS, AGI is renumbered
                                       11a/11b, deduction lines move to p.2)

Neither blank carries /TU tooltips (all None) and the field names are opaque
IRS "Designer 6.5" XFA names (f1_NN / c1_NN). The maps below were derived by
cross-referencing `pdftotext -bbox` word positions against each field's
/Rect, one printed line at a time — see the worked derivation in the Phase 3
report. Do not trust the field-name *number* to mean the same line across the
two blanks; they do not line up (verified empirically, both blanks reshuffle
line numbers relative to the field index around lines 4a-11).
"""
from __future__ import annotations

import os

import mklib

HANDLES = {"tax_return"}

# ---------------------------------------------------------------------
# Which blank a tax year selects (RENDER-CONTRACT "WHAT TO BUILD" / STYLE-SPEC
# §13 D11). The masterkey also carries `documents.tax_return.blank`; render()
# asserts the two agree and fails loudly if not, per the task brief.
BLANK_FOR_YEAR = {2024: "f1040--2024.pdf", 2025: "f1040.pdf"}

# ---------------------------------------------------------------------
# Filing-status checkboxes. Each is a SEPARATE /Btn field with one "on"
# state (mklib §5.6.2) — never hardcode the state, always read it from
# mklib.btn_on_states(). The dotted names below were confirmed against the
# printed "Single / Married filing jointly / Married filing separately /
# Head of household / Qualifying surviving spouse" row on page 1.
FILING_STATUS_FIELDS = {
    "f1040--2024.pdf": {
        "single": "topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[0]",
        "mfj":    "topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[1]",
        "mfs":    "topmostSubform[0].Page1[0].FilingStatus_ReadOrder[0].c1_3[2]",
        "hoh":    "topmostSubform[0].Page1[0].c1_3[0]",
        "qss":    "topmostSubform[0].Page1[0].c1_3[1]",
    },
    "f1040.pdf": {
        "single": "topmostSubform[0].Page1[0].Checkbox_ReadOrder[0].c1_8[0]",
        "mfj":    "topmostSubform[0].Page1[0].Checkbox_ReadOrder[0].c1_8[1]",
        "mfs":    "topmostSubform[0].Page1[0].Checkbox_ReadOrder[0].c1_8[2]",
        "hoh":    "topmostSubform[0].Page1[0].c1_8[0]",
        "qss":    "topmostSubform[0].Page1[0].c1_8[1]",
    },
}

FILING_STATUS_KEY = {
    "single": "single",
    "married filing jointly": "mfj",
    "married filing separately": "mfs",
    "head of household": "hoh",
    "qualifying surviving spouse": "qss",
}

# ---------------------------------------------------------------------
# Text-field maps. "dependent_mode" records the structural difference
# RENDER-CONTRACT calls out: the 2024 blank holds one dependent's full name
# in a single field; the 2025 blank splits first/last into two fields and
# arranges dependents as four COLUMNS rather than four rows.
_P1 = "topmostSubform[0].Page1[0]."
_P2 = "topmostSubform[0].Page2[0]."

FIELDS_2024 = {
    "dependent_mode": "combined",
    "taxpayer_first_mi": _P1 + "f1_04[0]",
    "taxpayer_last":     _P1 + "f1_05[0]",
    "taxpayer_ssn":      _P1 + "f1_06[0]",
    "spouse_first_mi":   _P1 + "f1_07[0]",
    "spouse_last":       _P1 + "f1_08[0]",
    "spouse_ssn":        _P1 + "f1_09[0]",
    "street":  _P1 + "Address_ReadOrder[0].f1_10[0]",
    "apt":     _P1 + "Address_ReadOrder[0].f1_11[0]",
    "city":    _P1 + "Address_ReadOrder[0].f1_12[0]",
    "state":   _P1 + "Address_ReadOrder[0].f1_13[0]",
    "zip":     _P1 + "Address_ReadOrder[0].f1_14[0]",
    "dep_name":         _P1 + "Table_Dependents[0].Row1[0].f1_20[0]",
    "dep_ssn":          _P1 + "Table_Dependents[0].Row1[0].f1_21[0]",
    "dep_relationship": _P1 + "Table_Dependents[0].Row1[0].f1_22[0]",
    "line1a_wages":           _P1 + "f1_32[0]",
    "line1z_wages":           _P1 + "f1_41[0]",
    # lines 4a-11 (IRA/pensions/SS/AGI) all nest under this ReadOrder group
    # on the 2024 blank -- easy to miss since f1_57..f1_60 (12-15) do not.
    "line5a_pension_gross":   _P1 + "Line4a-11_ReadOrder[0].f1_48[0]",
    "line5b_pension_taxable": _P1 + "Line4a-11_ReadOrder[0].f1_49[0]",
    "line6a_ss_gross":        _P1 + "Line4a-11_ReadOrder[0].f1_50[0]",
    "line6b_ss_taxable":      _P1 + "Line4a-11_ReadOrder[0].f1_51[0]",
    "line9_total_income":     _P1 + "Line4a-11_ReadOrder[0].f1_54[0]",
    "line11_agi":             _P1 + "Line4a-11_ReadOrder[0].f1_56[0]",
    "line24_total_tax":       _P2 + "f2_10[0]",
    "line25d_withholding":    _P2 + "f2_14[0]",
    "line33_total_payments":  _P2 + "f2_22[0]",
    "line34_overpayment":     _P2 + "f2_23[0]",
    "line35a_refund":         _P2 + "f2_24[0]",
    "line37_owe":             _P2 + "f2_28[0]",
    "preparer_name":          _P2 + "f2_39[0]",
}

FIELDS_2025 = {
    "dependent_mode": "split",
    "taxpayer_first_mi": _P1 + "f1_14[0]",
    "taxpayer_last":     _P1 + "f1_15[0]",
    "taxpayer_ssn":      _P1 + "f1_16[0]",
    "spouse_first_mi":   _P1 + "f1_17[0]",
    "spouse_last":       _P1 + "f1_18[0]",
    "spouse_ssn":        _P1 + "f1_19[0]",
    "street":  _P1 + "Address_ReadOrder[0].f1_20[0]",
    "apt":     _P1 + "Address_ReadOrder[0].f1_21[0]",
    "city":    _P1 + "Address_ReadOrder[0].f1_22[0]",
    "state":   _P1 + "Address_ReadOrder[0].f1_23[0]",
    "zip":     _P1 + "Address_ReadOrder[0].f1_24[0]",
    # dependent-1 is the leftmost of four COLUMNS; rows are (1)First name,
    # (2)Last name, (3)SSN, (4)Relationship.
    "dep_first":        _P1 + "Table_Dependents[0].Row1[0].f1_31[0]",
    "dep_last":         _P1 + "Table_Dependents[0].Row2[0].f1_35[0]",
    "dep_ssn":          _P1 + "Table_Dependents[0].Row3[0].f1_39[0]",
    "dep_relationship": _P1 + "Table_Dependents[0].Row4[0].f1_43[0]",
    "line1a_wages":           _P1 + "f1_47[0]",
    "line1z_wages":           _P1 + "f1_57[0]",
    "line5a_pension_gross":   _P1 + "f1_65[0]",
    "line5b_pension_taxable": _P1 + "f1_66[0]",
    "line6a_ss_gross":        _P1 + "f1_68[0]",
    "line6b_ss_taxable":      _P1 + "f1_69[0]",
    "line9_total_income":     _P1 + "f1_73[0]",
    "line11_agi":             _P1 + "f1_75[0]",
    "line11b_agi":            _P2 + "f2_01[0]",
    "line24_total_tax":       _P2 + "f2_16[0]",
    "line25d_withholding":    _P2 + "f2_20[0]",
    "line33_total_payments":  _P2 + "f2_29[0]",
    "line34_overpayment":     _P2 + "f2_30[0]",
    "line35a_refund":         _P2 + "f2_31[0]",
    "line37_owe":             _P2 + "f2_35[0]",
    "preparer_name":          _P2 + "f2_46[0]",
}

FIELDS_BY_BLANK = {"f1040--2024.pdf": FIELDS_2024, "f1040.pdf": FIELDS_2025}


# =====================================================================
# masterkey fact extraction — tolerant of the per-client variation in
# `documents.tax_return`'s own keys (this sub-block is NOT normalised
# beyond `year`/`blank` by normalize_masterkeys.py; see SPEC-DELTA D-I).
# =====================================================================
def _first(tr: dict, *keys):
    for k in keys:
        if k in tr and tr[k] not in (None, ""):
            return tr[k]
    return None


def _num(v):
    """Format a number the way a filled-in 1040 line prints it: no cents."""
    if v is None:
        return None
    return f"{int(round(float(v))):,}"


def _ssn(v):
    """Strip formatting — the SSN field is a 9-char comb, maxlen 9, and
    rejects (truncates) a dashed "123-45-6789" string."""
    if v is None:
        return None
    return "".join(ch for ch in str(v) if ch.isdigit())


def split_first_last(full_name: str, family_name: str) -> tuple:
    """Split `full_name` into (first-and-middle, last) using the KNOWN
    family name, rather than guessing from word order.

    Necessary because tran_daniel's applicant name prints in Vietnamese
    family-given-middle order ("Vu Thanh Ha", family=Vu) — a naive
    last-token split would misfile "Ha" as the family name (RENDER-CONTRACT
    WHAT TO BUILD, name_lock_rule in the masterkey).
    """
    full_name = full_name.strip()
    fam = (family_name or "").strip()
    if fam and full_name.lower().endswith(fam.lower()):
        return full_name[: -len(fam)].strip(), fam
    if fam and full_name.lower().startswith(fam.lower()):
        return full_name[len(fam):].strip(), fam
    parts = full_name.split()
    if len(parts) > 1:
        return " ".join(parts[:-1]), parts[-1]
    return full_name, ""


def resolve_family_name(mk: dict, name_str: str):
    """Match `name_str` (a tax_return name string) against the masterkey's
    structured identity/spouse blocks to recover the correct family name,
    regardless of which of taxpayer/spouse slot on the return each person
    landed in (masterkeys disagree client to client — kavanagh puts the
    applicant first, tran puts the USC spouse first).
    """
    toks = {t.lower() for t in name_str.split()}

    ident = mk.get("identity") or {}
    if ident.get("given_name") and ident.get("family_name"):
        if ident["given_name"].lower() in toks and ident["family_name"].lower() in toks:
            return ident["family_name"]

    spouse = (mk.get("family") or {}).get("spouse") or {}
    if spouse.get("given_name") and spouse.get("family_name"):
        if spouse["given_name"].lower() in toks and spouse["family_name"].lower() in toks:
            return spouse["family_name"]

    return None


def resolve_person(mk: dict, name_str: str) -> tuple:
    family = resolve_family_name(mk, name_str)
    return split_first_last(name_str, family)


def parse_address(addr: str) -> tuple:
    """"806 Brightwood Terrace, Ann Arbor, MI 48104" -> street, "", city, state, zip.
    "47 Larkspur Street, Apt 3, Somerville, MA 02143" -> street, apt, city, state, zip.

    4 comma-separated segments means an embedded apartment/unit segment
    (almeida_paulo); 3 means there is none. The last segment is always
    "STATE ZIP".
    """
    import re

    parts = [p.strip() for p in addr.split(",")]
    state_zip = parts[-1] if parts else ""
    state, _, zipc = state_zip.rpartition(" ")
    street = parts[0] if parts else ""
    apt = ""
    city = ""
    if len(parts) == 4:
        apt = re.sub(r"(?i)^(apt\.?|apartment|unit|#)\s*", "", parts[1]).strip()
        city = parts[2]
    elif len(parts) >= 2:
        city = parts[-2]
    return street, apt, city, state.strip(), zipc.strip()


def get_wages(tr: dict):
    w = tr.get("wages")
    if isinstance(w, dict):
        w = w.get("total")
    if not w:
        return None
    return w


def get_refund_or_owed(tr: dict):
    """-> (kind, amount) with kind in {"refund","owed"}, or (None, None)."""
    combo = tr.get("refund_or_owed")
    if isinstance(combo, dict):
        kind = (combo.get("direction") or combo.get("type") or "").strip().lower()
        amount = combo.get("amount")
        if kind.startswith("owe"):
            return "owed", amount
        return "refund", amount
    if tr.get("refund") is not None:
        return "refund", tr["refund"]
    if tr.get("amount_owed") is not None:
        return "owed", tr["amount_owed"]
    return None, None


def get_dependent(tr: dict):
    dep = tr.get("dependent") or tr.get("dependents")
    if isinstance(dep, list):
        dep = dep[0] if dep else None
    return dep


# =====================================================================
def render(masterkey: dict, outdir: str, doc: dict) -> list:
    if doc["id"] not in HANDLES:
        raise ValueError(f"render_1040.py cannot handle doc id {doc['id']!r}")

    mk = masterkey
    tr = (mk.get("documents") or {}).get("tax_return")
    if not tr:
        raise KeyError("masterkey has no documents.tax_return")

    year = int(tr["year"])
    blank_name = tr["blank"]
    expected = BLANK_FOR_YEAR.get(year)
    if expected is None:
        raise ValueError(f"no known 1040 blank for tax year {year}")
    if blank_name != expected:
        raise ValueError(
            f"masterkey tax_return.blank={blank_name!r} disagrees with "
            f"tax_return.year={year} (expected {expected!r}) — this is a "
            "masterkey data bug that validate_masterkeys.py's tax-year "
            "check should have caught (RENDER-CONTRACT WHAT TO BUILD)."
        )

    blank_path = os.path.join(mklib.BLANKS, blank_name)
    fmap = FIELDS_BY_BLANK[blank_name]
    on_states = mklib.btn_on_states(blank_path)

    values = {}

    # -- filing status --------------------------------------------------
    status_key = FILING_STATUS_KEY.get(str(tr["filing_status"]).strip().lower())
    if status_key is None:
        raise ValueError(f"unrecognised filing_status {tr['filing_status']!r}")
    status_field = FILING_STATUS_FIELDS[blank_name][status_key]
    values[status_field] = on_states[status_field]
    is_joint = status_key == "mfj"

    # -- names / SSNs -----------------------------------------------------
    taxpayer_name = _first(tr, "taxpayer_name")
    taxpayer_ssn = _first(tr, "taxpayer_ssn", "ssn")
    first_mi, last = resolve_person(mk, taxpayer_name)
    values[fmap["taxpayer_first_mi"]] = first_mi
    values[fmap["taxpayer_last"]] = last
    values[fmap["taxpayer_ssn"]] = _ssn(taxpayer_ssn)

    spouse_name = _first(tr, "spouse_name")
    spouse_ssn = _first(tr, "spouse_ssn")
    if is_joint and spouse_name:
        sfirst_mi, slast = resolve_person(mk, spouse_name)
        values[fmap["spouse_first_mi"]] = sfirst_mi
        values[fmap["spouse_last"]] = slast
        if spouse_ssn:
            values[fmap["spouse_ssn"]] = _ssn(spouse_ssn)

    # -- address (STYLE-SPEC §9.4 lock: printed verbatim from the masterkey) --
    addr = _first(tr, "address_as_printed", "address_printed")
    if addr:
        street, apt, city, state, zipc = parse_address(addr)
        values[fmap["street"]] = street
        if apt:
            values[fmap["apt"]] = apt
        values[fmap["city"]] = city
        values[fmap["state"]] = state
        values[fmap["zip"]] = zipc

    # -- dependent (only when the tax_return fact block itself names one;
    # family.children existing is not sufficient — see report) ------------
    dep = get_dependent(tr)
    if dep:
        dep_name = dep.get("name") or dep.get("full_name")
        dep_ssn = dep.get("ssn")
        dep_rel = dep.get("relationship")
        if fmap["dependent_mode"] == "combined":
            values[fmap["dep_name"]] = dep_name
        else:
            fam = resolve_family_name(mk, dep_name) if dep_name else None
            dfirst, dlast = split_first_last(dep_name, fam) if dep_name else ("", "")
            values[fmap["dep_first"]] = dfirst
            values[fmap["dep_last"]] = dlast
        if dep_ssn:
            values[fmap["dep_ssn"]] = _ssn(dep_ssn)
        if dep_rel:
            values[fmap["dep_relationship"]] = dep_rel

    # -- income lines -------------------------------------------------------
    wages = get_wages(tr)
    if wages:
        values[fmap["line1a_wages"]] = _num(wages)
        values[fmap["line1z_wages"]] = _num(wages)

    pension = tr.get("pension_income")
    if pension:
        values[fmap["line5a_pension_gross"]] = _num(pension)
        values[fmap["line5b_pension_taxable"]] = _num(pension)

    ss_gross = tr.get("social_security_benefits_gross")
    ss_taxable = tr.get("social_security_benefits_taxable")
    if ss_gross is not None:
        values[fmap["line6a_ss_gross"]] = _num(ss_gross)
    if ss_taxable is not None:
        values[fmap["line6b_ss_taxable"]] = _num(ss_taxable)

    agi = _first(tr, "adjusted_gross_income", "agi")
    if agi is not None:
        # No `adjustments to income` fact is carried by any client's
        # masterkey, so line 9 (total income) is set equal to line 11/11a
        # (AGI) — arithmetically consistent with adjustments = 0, and not
        # an invented figure (RENDER-CONTRACT §7: report a missing fact,
        # don't invent one).
        values[fmap["line9_total_income"]] = _num(agi)
        values[fmap["line11_agi"]] = _num(agi)
        if "line11b_agi" in fmap:
            values[fmap["line11b_agi"]] = _num(agi)

    total_tax = tr.get("total_tax")
    if total_tax is not None:
        values[fmap["line24_total_tax"]] = _num(total_tax)

    withholding = _first(tr, "federal_withholding", "withholding", "federal_tax_withheld")
    if withholding is not None:
        values[fmap["line25d_withholding"]] = _num(withholding)
        # These are simple W-2/pension/SS returns with no estimated-tax
        # payments in any masterkey (line 26 is never populated), so total
        # payments (line 33 = 25d + 26 + 32) equals withholding alone. Left
        # BLANK, not derived from total_tax+refund, when withholding itself
        # is unknown (tran_daniel) — a filled line 33 whose own inputs (25d)
        # are blank is exactly the kind of unexplained figure a text-extraction
        # reviewer would flag; see the report for that data gap.
        values[fmap["line33_total_payments"]] = _num(withholding)

    kind, amount = get_refund_or_owed(tr)
    if kind == "refund" and amount is not None:
        values[fmap["line34_overpayment"]] = _num(amount)
        values[fmap["line35a_refund"]] = _num(amount)
    elif kind == "owed" and amount is not None:
        values[fmap["line37_owe"]] = _num(amount)

    # -- preparer (the ONE exempted preparer identity, §16 r7 / §0.1) -------
    preparer = _first(tr, "preparer", "preparer_name")
    if preparer:
        values[fmap["preparer_name"]] = preparer

    dst = mklib.component_path(outdir, doc, "pdf")
    mklib.fill_acroform(blank_path, dst, values)
    return [dst]


if __name__ == "__main__":
    import sys

    slug = sys.argv[1] if len(sys.argv) > 1 else "nowak_agata"
    mk = mklib.load_masterkey(slug)
    doc = mklib.doc_by_id(mk, "tax_return")
    outdir = mklib.ensure_outdir(os.path.join(mklib.CLIENTS, slug, "output"))
    for p in render(mk, outdir, doc):
        print(p)

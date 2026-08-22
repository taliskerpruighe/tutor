#!/usr/bin/env python3
"""render_addendum.py — the travel addendum exhibit (C4).

Contract: RENDER-CONTRACT.md. Owns doc["id"] in HANDLES below (§7).

Firm-authored, so it ships docx + pdf (SPEC-DELTA D-D), via
`mklib.new_docx()` / `mklib.add_para()` then `mklib.docx_to_pdf()` — the same
path as every other firm page. STYLE-SPEC §4.5 fixes the layout exactly; this
module does not improvise it. BUILD-PLAN §4's openpyxl/spreadsheet shape is
superseded (RENDER-CONTRACT §7, `tools/README.md`) — this is a prose-and-list
docx, not a workbook.

THE DAY-TRIP TEST, AND WHY IT IS NOT A SUBSTRING MATCH ON `why_excluded`.
Two of the four addendum clients word a NON-day-trip exclusion using the
literal words "day trip" while explicitly negating them:

  tran_daniel   (7th, oldest, row-count only): "...this trip is not a day
                trip and is not trimmed for any other reason..."
  adeyemi_tunde (oldest, row-count only):      "...Not a day trip; §9.2 C4's
                day-trip disjunct (registry D7) is not in play..."

A substring match on "day trip" flags both as day trips, silently drops a
real countable trip from each of those two addenda, and then agrees with
`rule_inputs.trips_day_excluded` (which — see below — is ALSO wrong on
exactly those two clients) for a green self-check on a wrong artefact. The
test used here is structural instead: a trip is a day trip iff its depart
and return dates are the same day. Verified against every supplied trip in
all four addendum masterkeys: the only same-date trips are almeida_paulo's
2024-05-14 Canada trip and stavros_daphne's 2023-08-12 Canada trip, and both
are exactly the two rows independently marked `on_addendum: false` where that
field exists.

THE `rule_inputs.trips_day_excluded` BUG (reported, not silently patched
around — RENDER-CONTRACT §7: a masterkey fact this renderer cannot trust is
reported, not invented around, and this module owns neither the masterkey
nor the normaliser). On `tran_daniel` and `adeyemi_tunde`,
`rule_inputs.trips_day_excluded == 1` even though neither client supplied a
day trip — both have exactly one trip trimmed from the Part 8 table by the
row-count disjunct alone, and the normaliser appears to have miscounted that
trip into the day-trip bucket instead of the overflow bucket. Both
masterkeys say so themselves elsewhere and agree with the per-trip data:
`tran_daniel.travel_derived.derived.countable_trip_count == 7` and
`adeyemi_tunde.travel_derived.derived.countable_trips == 7`, i.e. ALL seven
supplied trips are countable on both. Primary per-trip data
(`why_excluded` + the structural date test) wins over the derived counter,
the same principle SPEC-DELTA D-H2 already applied ("prefer the printed page
over any extracted label"). `_render_trips()` below computes the rendered
set from the trip rows, and separately, loudly, reports (never raises on)
any disagreement with `rule_inputs.trips_day_excluded` by name and number.

PART 8 PAGE NUMBER — four different key paths across the four masterkeys
(`travel_derived.derived.part8_page_number`, `.part8_page`, `.part_8_page`,
`.addendum_meta.part_8_page`). `_part8_page()` tries all four and RAISES if
none is present — all four happen to equal 6 on the current clients, so a
silent default of 6 would pass every test here and be wrong on a fifth
client with a genuinely different page.

RESIDENCE WINDOW — not read from the masterkey at all. STYLE-SPEC §4.5 is
explicit that the window is a fixed function of the eligibility basis alone
(5 years for 316(a), 3 years for 319(a)), and `mklib.basis_key()` already
carries that fact; a masterkey-supplied residence-window field would be a
second, independently-drifting source of the same number (the same
objection SPEC-DELTA D-I raises about re-deriving a rule two ways). Where a
masterkey happens to also carry the derived sentence
(`adeyemi_tunde.travel_derived.addendum_meta.intro_sentence`), this module's
own construction is asserted to match it, as a free cross-check — never as
the source.
"""
from __future__ import annotations

import os
import sys

import mklib

HANDLES = {"travel_addendum"}

TITLE_PT = 12.0
INDENT_IN = 0.25


# =====================================================================
# facts
# =====================================================================
def _part8_page(mk: dict) -> int:
    td = mk.get("travel_derived") or {}
    for getter in (
        lambda: td["derived"]["part8_page_number"],
        lambda: td["part8_page"],
        lambda: td["part_8_page"],
        lambda: td["addendum_meta"]["part_8_page"],
    ):
        try:
            v = getter()
        except (KeyError, TypeError):
            continue
        if v not in (None, ""):
            return int(v)
    raise KeyError(
        "travel_derived carries none of the known Part 8 page-number paths "
        "(derived.part8_page_number / part8_page / part_8_page / "
        "addendum_meta.part_8_page) — masterkey bug, report it")


def _is_day_trip(trip: dict) -> bool:
    """Structural test: same depart/return date. See module docstring for
    why this is NOT a substring match on why_excluded."""
    return mklib.as_date(trip["depart"]) == mklib.as_date(trip["return"])


def _country(trip: dict) -> str:
    countries = trip.get("countries")
    if not countries:
        raise KeyError(f"travel[]: trip {trip.get('depart')!r} has no countries")
    return ", ".join(countries)


def _select_addendum_trips(mk: dict, client_label: str) -> list:
    """The countable (non-day-trip) trips, most recent first.

    Hard checks (raise): every trip claiming `on_addendum` disagrees with
    nothing; no selected trip is structurally a day trip.
    Soft check (report, never raise): the selected count agrees with
    `rule_inputs.trips_day_excluded` — known wrong on two clients (see module
    docstring); mismatches are printed as a named finding and rendering
    proceeds from the trip rows regardless.
    """
    trips = mk.get("travel") or []
    if not trips:
        raise KeyError("travel is empty — nothing to render an addendum from")

    selected = []
    for t in trips:
        day_trip = _is_day_trip(t)
        if "on_addendum" in t and bool(t["on_addendum"]) == day_trip:
            raise ValueError(
                f"travel[] trip {t.get('depart')}: on_addendum="
                f"{t['on_addendum']!r} disagrees with the structural "
                f"day-trip test (depart==return: {day_trip})")
        if not day_trip:
            selected.append(t)

    for t in selected:
        assert not _is_day_trip(t), "day trip leaked into the addendum selection"

    selected.sort(key=lambda t: mklib.as_date(t["depart"]), reverse=True)

    ri = mk.get("rule_inputs") or {}
    trip_count = ri.get("trip_count")
    day_excluded = ri.get("trips_day_excluded")
    if trip_count is not None and day_excluded is not None:
        expected = trip_count - day_excluded
        if expected != len(selected):
            print(
                f"MASTERKEY BUG ({client_label}): rule_inputs says "
                f"trip_count={trip_count} - trips_day_excluded={day_excluded} "
                f"= {expected} countable trips, but the per-trip structural "
                f"day-trip test on travel[] (depart==return) selects "
                f"{len(selected)}. Rendering {len(selected)} from the trip "
                f"rows — primary data — per SPEC-DELTA D-H2's precedent.",
                file=sys.stderr)

    return selected


def _addendum_facts(mk: dict, client_label: str) -> dict:
    basis = mklib.basis_key(mk)
    years = 3 if basis == "319a" else 5
    page = _part8_page(mk)
    trips = _select_addendum_trips(mk, client_label)

    intro = (
        "The following is a full list of the Applicant's trips to countries "
        f"other than the United States within the last {years} years, "
        "excluding day trips. It combines the trips listed in Page "
        f"{page}, Part 8, Question 1, with the trips listed in the "
        "addendum thereto."
    )

    stored = (((mk.get("travel_derived") or {}).get("addendum_meta") or {})
             .get("intro_sentence"))
    if stored and stored.strip() != intro.strip():
        print(f"NOTE ({client_label}): constructed intro sentence differs "
              f"from travel_derived.addendum_meta.intro_sentence:\n"
              f"  constructed: {intro!r}\n  stored:      {stored.strip()!r}",
              file=sys.stderr)

    items = []
    for t in trips:
        items.append(
            f"{mklib.fmt_numeric(t['depart'])}-{mklib.fmt_numeric(t['return'])} "
            f"– {_country(t)}")

    return {"intro": intro, "items": items}


# =====================================================================
# docx — determinism
# =====================================================================
# python-docx's `Document.save()` writes the .docx zip container through
# `zipfile.ZipFile` with no `date_time` on the entries, so each member gets
# `time.localtime()` at save time — the docProps/core.xml content itself is
# python-docx's own fixed built-in placeholder (2013-12-23T23:15:00Z,
# unaffected by masterkey or clock) but the ZIP LOCAL FILE HEADERS are not,
# and that alone made two consecutive renders differ at byte 11. RENDER-
# CONTRACT §6 requires byte-identical output and provides no docx-level
# equivalent of `stamp_deterministic` for this (that helper is PDF-only), so
# this module fixes it locally: save to memory, then rewrite every zip entry
# with a fixed `date_time` matching `mklib.FIXED_PDF_DATE`, byte-for-byte
# content unchanged. `render_docs.py` (`table_of_contents`, `cover_letter`,
# `written_explanation`) calls `document.save()` the same way and will hit
# the same nondeterminism; worth flagging to the toolsmith, not something
# this module can fix outside its own two files.
import re
import zipfile
import io as _io

_FIXED_ZIP_DT = tuple(
    int(x) for x in re.match(
        r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})",
        mklib.FIXED_PDF_DATE).groups())


def _save_docx_deterministic(document, outpath: str) -> str:
    buf = _io.BytesIO()
    document.save(buf)
    buf.seek(0)
    zin = zipfile.ZipFile(buf)
    os.makedirs(os.path.dirname(os.path.abspath(outpath)) or ".", exist_ok=True)
    tmp = outpath + ".det.tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            zi = zipfile.ZipInfo(item.filename, date_time=_FIXED_ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = item.external_attr
            zout.writestr(zi, data)
    os.replace(tmp, outpath)
    return outpath


def _build_docx(facts: dict, outpath: str) -> str:
    from docx.shared import Inches

    d = mklib.new_docx()
    mklib.add_para(d, "TRAVEL ADDENDUM", align="center", size_pt=TITLE_PT)
    mklib.add_blank(d)

    p = mklib.add_para(d, facts["intro"], align="both", indent_in=INDENT_IN)
    p.paragraph_format.right_indent = Inches(INDENT_IN)
    mklib.add_blank(d)

    n = len(facts["items"])
    for i, line in enumerate(facts["items"], start=1):
        p = mklib.add_para(d, f"{i}. {line}", align="both", indent_in=INDENT_IN)
        p.paragraph_format.right_indent = Inches(INDENT_IN)
        if i != n:
            mklib.add_blank(d)

    return _save_docx_deterministic(d, outpath)


def _scrub_pdf_xmp(pdf_path: str) -> None:
    """Strip the /Metadata XMP stream `soffice` embeds on conversion.

    `mklib.docx_to_pdf()` already calls `stamp_deterministic()` on its
    output, which fixes the classic /Info dict (/CreationDate, /ModDate) —
    but `soffice`'s converter separately stamps a real wall-clock time into
    an XMP metadata packet (xmp:CreateDate / xmp:ModifyDate /
    xap:MetadataDate, several times over) that /Info-level stamping never
    touches, and that alone made two consecutive PDF renders differ even
    with a byte-identical input .docx. The fact this survives
    `docx_to_pdf()` unchanged suggests every OTHER firm-authored docx page
    built through the same helper (table of contents, cover letter, written
    explanation) has the same latent nondeterminism; this module fixes only
    its own output, since it owns render_addendum.py and not mklib.py.
    """
    from pypdf import PdfWriter
    w = PdfWriter(clone_from=pdf_path)
    root = w._root_object
    meta_ref = root.get("/Metadata")
    if meta_ref is not None:
        # Deleting the /Metadata key alone leaves the stream OBJECT itself
        # still cloned into the writer (PdfWriter.clone_from copies every
        # object, referenced or not, and .write() does not garbage-collect
        # orphans), so the timestamped bytes still land in the file even
        # with no live reference to them. Overwrite the stream's own data
        # instead, in place, so the object that gets written is fixed.
        meta_ref.get_object().set_data(b"")
    mklib.stamp_deterministic(w)
    tmp = pdf_path + ".xmp.tmp"
    with open(tmp, "wb") as fh:
        w.write(fh)
    os.replace(tmp, pdf_path)


def render(masterkey: dict, outdir: str, doc: dict) -> list:
    """RENDER-CONTRACT §1. One DOCUMENT per call; docx + pdf (firm-authored)."""
    if doc["id"] not in HANDLES:
        raise ValueError(f"render_addendum.py does not handle {doc['id']!r}; "
                         f"HANDLES = {sorted(HANDLES)}")
    client_label = masterkey.get("slug") or masterkey.get("client") or "?"
    facts = _addendum_facts(masterkey, client_label)
    docx_path = mklib.component_path(outdir, doc, "docx")
    _build_docx(facts, docx_path)
    pdf_path = mklib.docx_to_pdf(docx_path, os.path.dirname(docx_path))
    _scrub_pdf_xmp(pdf_path)
    return [docx_path, pdf_path]


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    mk = mklib.load_masterkey(slug)
    outdir = mklib.ensure_outdir(os.path.join(mklib.CLIENTS, slug, "output"))
    for d in mklib.doc_entries(mk):
        if d["id"] in HANDLES:
            paths = render(mk, outdir, d)
            print(d["id"], "->", paths)

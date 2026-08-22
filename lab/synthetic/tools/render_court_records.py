#!/usr/bin/env python3
"""render_court_records.py — the certified court-record exhibit (C5).

Contract: RENDER-CONTRACT.md. Owns doc["id"] in HANDLES below (§7).

Ships PDF only (SPEC-DELTA D-D — exhibit, not firm-authored). No firm
identity anywhere (§0.1): a real court record names a filing attorney, ours
does not, because no masterkey supplies one for either test client. No
`datetime.now()`; every date comes from the masterkey via `mklib.fmt_numeric`.

Field-name landmine, same shape as `fabricate_ids.py`'s note: the two agents
who wrote `nowak_agata` and `adeyemi_tunde` shaped `documents.court_records`
differently.

- `nowak_agata` carries `documents.court_records` as a single dict, with
  `court_name` and `court_location` as two separate fields, each charge
  spelling the description `description` and the date `offence_date`, and
  the clerk's name under `clerk_name`.
- `adeyemi_tunde` carries the SAME fact set one level down, inside
  `documents.evidence[]` as the list entry whose `type == "court_records"`,
  with `court_name` and `court_location` already combined into
  `court_name_and_location`, each charge spelling the description `offense`
  and the date `offense_date`, and the clerk's name under `clerk`.

`_pick()` resolves a closed, explicit alias list per fact and raises loudly
on a miss (RENDER-CONTRACT §7: an absent fact is a masterkey bug to report,
never a value to invent).

The seal legend is DERIVED from `court_name`/`court_location` (a fact already
in the masterkey), not printed from the raw `seal` field verbatim: nowak's
`seal` value already IS that derived legend ("Seal of the 15th District
Court, Washtenaw County, Michigan"), but adeyemi's `seal` value is prose
about a supplied photograph ("raised court seal present on the certified
copy, visible in the supplied photograph") — a stage direction, not a legend,
and printing it verbatim would read like one. Deriving the legend the same
way for both clients keeps the two exhibits' furniture identical, which is
what a certified-copy series from two different courts should look like
(same certification shape, different facts), and sidesteps simulating "the
supplied photograph" outright, which born-digital §0.1 forbids anyway.
"""
from __future__ import annotations

import os

import mklib

HANDLES = {"court_records"}

TITLE_PT = 14.0


# =====================================================================
# field alias resolution — closed lists only, raise loudly on a miss
# =====================================================================
def _pick(d: dict, keys: tuple, ctx: str):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            return v
    raise KeyError(f"{ctx}: none of {keys} present (have {sorted(d.keys())})")


def _find_record(mk: dict) -> dict:
    """Locate the court-records fact block, whichever of the two shapes."""
    docs = mk.get("documents") or {}
    rec = docs.get("court_records")
    if isinstance(rec, dict):
        return rec
    for item in (docs.get("evidence") or []):
        if isinstance(item, dict) and item.get("type") == "court_records":
            return item
    raise KeyError("documents.court_records (or documents.evidence[type="
                    "court_records]) missing from masterkey")


def _court_name_location(rec: dict, ctx: str) -> str:
    combined = rec.get("court_name_and_location")
    if combined:
        return combined
    name = _pick(rec, ("court_name",), ctx)
    loc = _pick(rec, ("court_location",), ctx)
    return f"{name}, {loc}"


def _charge_facts(ch: dict, ctx: str) -> dict:
    return {
        "statute": _pick(ch, ("statute",), ctx),
        "description": _pick(ch, ("description", "offense"), ctx),
        "offence_date": _pick(ch, ("offence_date", "offense_date"), ctx),
    }


def _clerk_facts(cc: dict, ctx: str) -> dict:
    return {
        "clerk_name": _pick(cc, ("clerk_name", "clerk"), ctx),
        "certification_date": _pick(cc, ("certification_date",), ctx),
    }


def _court_facts(mk: dict) -> dict:
    rec = _find_record(mk)
    ctx = "documents.court_records"
    charges_raw = rec.get("charges")
    if not charges_raw:
        raise KeyError(f"{ctx}.charges missing or empty")
    cc = rec.get("clerk_certification")
    if not cc:
        raise KeyError(f"{ctx}.clerk_certification missing")
    court = _court_name_location(rec, ctx)
    return {
        "court": court,
        "police_case_number": _pick(rec, ("police_case_number",), ctx),
        "docket_number": _pick(rec, ("docket_number",), ctx),
        "charges": [_charge_facts(ch, f"{ctx}.charges[]") for ch in charges_raw],
        "plea": _pick(rec, ("plea",), ctx),
        "disposition": _pick(rec, ("disposition",), ctx),
        "disposition_date": _pick(rec, ("disposition_date",), ctx),
        "judge": _pick(rec, ("judge",), ctx),
        "clerk": _clerk_facts(cc, f"{ctx}.clerk_certification"),
        "seal_legend": f"Seal of the {court}",
    }


# =====================================================================
# text wrapping — frame_text draws single lines only; a certification
# sentence is long enough to need real wrapping at body width.
# =====================================================================
def _wrap(c, text: str, font: str, size: float, max_width: float) -> list:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        cand = f"{cur} {w}".strip()
        if c.stringWidth(cand, font, size) <= max_width:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# =====================================================================
# rendering
# =====================================================================
def _draw(mk: dict, outpath: str) -> str:
    f = _court_facts(mk)
    c = mklib.new_canvas(outpath)
    body_width = mklib.PAGE_W - 2 * mklib.MARGIN

    lines = [
        (f["court"].upper(), {"bold": True, "size": TITLE_PT}),
        ("CERTIFIED COPY OF COURT RECORD", {"bold": True, "size": 12}),
        "",
        (f"Police Case No.: {f['police_case_number']}", {}),
        (f"Docket No.: {f['docket_number']}", {}),
        "",
        ("CHARGES", {"bold": True}),
        "",
    ]
    for ch in f["charges"]:
        lines.append((f"Statute: {ch['statute']}", {}))
        lines.append((f"Offense: {ch['description']}", {}))
        lines.append((f"Offense Date: {mklib.fmt_numeric(ch['offence_date'])}", {}))
        lines.append("")
    lines += [
        (f"Plea: {f['plea']}", {}),
        "",
        (f"Disposition: {f['disposition']}", {}),
        (f"Disposition Date: {mklib.fmt_numeric(f['disposition_date'])}", {}),
        "",
        (f"Judge: {f['judge']}", {}),
    ]

    y = mklib.frame_text(c, lines, align="left",
                         top=mklib.PAGE_H - mklib.MARGIN - TITLE_PT)

    # ---- clerk's certification, with a drawn seal --------------------
    y -= 20
    y = mklib.frame_text(c, [("CLERK'S CERTIFICATION", {"bold": True})],
                         align="left", top=y)
    y -= mklib.LEADING

    clerk_name = f["clerk"]["clerk_name"]
    # Some masterkeys spell the clerk's title into the name itself
    # ("Ellen Voss, Deputy Clerk of Circuit Court"); don't double it with our
    # own "Clerk of {court}" in that case.
    clerk_id = (clerk_name if "clerk" in clerk_name.lower()
               else f"{clerk_name}, Clerk of {f['court']}")
    cert_sentence = (
        f"I, {clerk_id}, certify that "
        "the foregoing is a true and correct copy of the record of this case "
        "as it appears in the official files of this court."
    )
    wrapped = _wrap(c, cert_sentence, mklib.BODY_FONT, mklib.BODY_PT, body_width)
    y = mklib.frame_text(c, wrapped, align="left", top=y)

    y -= 30
    seal_cy = y - 34
    seal_r = 34
    c.saveState()
    c.setLineWidth(1.2)
    c.circle(mklib.PAGE_W / 2.0, seal_cy, seal_r, stroke=1, fill=0)
    c.circle(mklib.PAGE_W / 2.0, seal_cy, seal_r - 5, stroke=1, fill=0)
    c.setFont(mklib.BODY_FONT_BOLD, 9)
    c.drawCentredString(mklib.PAGE_W / 2.0, seal_cy + 3, "SEAL")
    c.setFont(mklib.BODY_FONT, 6.5)
    c.drawCentredString(mklib.PAGE_W / 2.0, seal_cy - 9, "OF THE COURT")
    c.restoreState()

    y = seal_cy - seal_r - 18
    y = mklib.frame_text(c, [(f["seal_legend"], {})], align="center", top=y, size=9)
    y -= mklib.LEADING
    y = mklib.frame_text(
        c, [(f"Certification Date: {mklib.fmt_numeric(f['clerk']['certification_date'])}",
             {})],
        align="left", top=y)

    c.showPage()
    c.save()
    mklib.stamp_deterministic(outpath)
    return outpath


def render(masterkey: dict, outdir: str, doc: dict) -> list:
    """RENDER-CONTRACT §1. One DOCUMENT per call; PDF only (exhibit)."""
    if doc["id"] not in HANDLES:
        raise ValueError(f"render_court_records.py does not handle {doc['id']!r}; "
                         f"HANDLES = {sorted(HANDLES)}")
    outpath = mklib.component_path(outdir, doc, "pdf")
    _draw(masterkey, outpath)
    return [outpath]


if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else "nowak_agata"
    mk = mklib.load_masterkey(slug)
    outdir = mklib.ensure_outdir(os.path.join(mklib.CLIENTS, slug, "output"))
    for d in mklib.doc_entries(mk):
        if d["id"] in HANDLES:
            paths = render(mk, outdir, d)
            print(d["id"], "->", paths)

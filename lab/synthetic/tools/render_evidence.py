#!/usr/bin/env python3
"""render_evidence.py — Form I-797C, joint deed, joint automobile policy.

Contract: RENDER-CONTRACT.md. Owner: worker (RENDER-CONTRACT §7).
Field sets: STYLE-SPEC §12.10. No fact is invented; every value on a page
comes from the masterkey. NO FIRM IDENTITY, ANYWHERE (§0.1) — a deed's real
"prepared by" line and an insurance declarations page's real agency are both
omitted here on purpose; only the government agency identity on the I-797C
(a genuine USCIS notice) is printed, and only via mklib.DHS_LINES.
"""
from __future__ import annotations

import os

import mklib

HANDLES = {"i797c", "joint_deed", "auto_policy"}


# =====================================================================
# small local helpers — content-shaping only, no geometry/date reinvention
# =====================================================================
def _evidence(mk: dict, ev_type: str) -> dict | None:
    for e in (mk.get("documents", {}).get("evidence") or []):
        if isinstance(e, dict) and e.get("type") == ev_type:
            return e
    return None


def _wrap(c, text: str, font: str, size: float, max_width: float) -> list[str]:
    """Word-wrap text to max_width at (font, size). No house geometry here —
    frame_text still owns line placement and leading."""
    words = str(text).split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _paragraph(c, mk_text, top_y, max_width=None, size=mklib.BODY_PT):
    max_width = max_width if max_width is not None else (mklib.PAGE_W - 2 * mklib.MARGIN)
    lines = _wrap(c, mk_text, mklib.BODY_FONT, size, max_width)
    return mklib.frame_text(c, lines, top=top_y, size=size)


def _draw_table(c, x0, y_top, rows, row_h=34):
    """rows: list of rows; each row is a list of (label, value, width) cells,
    left to right, widths summing to the table width. Returns bottom y."""
    y = y_top
    for row in rows:
        x = x0
        for label, value, w in row:
            c.rect(x, y - row_h, w, row_h, stroke=1, fill=0)
            c.setFont(mklib.BODY_FONT_BOLD, 7)
            c.drawString(x + 4, y - 12, label)
            c.setFont(mklib.BODY_FONT, 11)
            c.drawString(x + 4, y - 27, "" if value is None else str(value))
            x += w
        y -= row_h
    return y


def _finish(path: str) -> str:
    """Stamp the house PDF metadata, then run the no-firm-identity self-check.

    History, kept because it explains the shape of this function: when this
    renderer was written, `mklib.stamp_deterministic` crashed on pypdf 6.14.2 —
    `w._ID` was assigned a plain list where `_write_trailer` requires an
    `ArrayObject`, and because the assignment itself raised nothing the
    surrounding try/except never fired; the failure surfaced later at
    `w.write()`. That was reported rather than patched around (a worker scoped
    to one file does not edit mklib), and the toolsmith has since fixed it.
    Stamping is therefore re-enabled: reportlab's `invariant=1` already gives
    byte-identical output, but only stamping gives the house `/CreationDate`
    and `/Producer` that RENDER-CONTRACT §6 asks for.
    """
    mklib.stamp_deterministic(path)
    hits = mklib.firm_identity_hits(mklib.pdf_text(path))
    if hits:
        raise AssertionError(f"firm-identity guard tripped on {path}: {hits}")
    return path


# =====================================================================
# dispatch
# =====================================================================
def render(masterkey: dict, outdir: str, doc: dict) -> list[str]:
    doc_id = doc["id"]
    if doc_id not in HANDLES:
        raise ValueError(
            f"render_evidence.py cannot render {doc_id!r}; HANDLES={HANDLES}")
    if doc_id == "i797c":
        return _render_i797c(masterkey, outdir, doc)
    if doc_id == "joint_deed":
        return _render_joint_deed(masterkey, outdir, doc)
    if doc_id == "auto_policy":
        return _render_auto_policy(masterkey, outdir, doc)
    raise ValueError(doc_id)  # pragma: no cover — HANDLES guard already caught this


# =====================================================================
# Form I-797C, Notice of Action
# =====================================================================
def _render_i797c(mk: dict, outdir: str, doc: dict) -> list[str]:
    d = mk.get("documents", {}).get("i797c")
    if not d:
        raise ValueError("masterkey has no documents.i797c for an i797c DOCUMENT")

    applicant_name = d["applicant_name"]
    expected = mklib.full_legal_name(mk)
    if applicant_name != expected:
        raise ValueError(
            f"documents.i797c.applicant_name {applicant_name!r} != "
            f"identity-derived full legal name {expected!r} — masterkey mismatch, "
            "not resolved here (§9.4 cross-document lock)")

    path = mklib.component_path(outdir, doc, "pdf")
    c = mklib.new_canvas(path)

    # -- header band: genuine agency identity, the one exception to §0.1 --
    y = mklib.frame_text(c, mklib.DHS_LINES, size=10)
    c.setFont(mklib.BODY_FONT_BOLD, 14)
    c.drawRightString(mklib.PAGE_W - mklib.MARGIN, mklib.PAGE_H - mklib.MARGIN - 4,
                       "I-797C, Notice of Action")
    y -= 4
    c.line(mklib.MARGIN, y, mklib.PAGE_W - mklib.MARGIN, y)
    y -= 18

    c.setFont(mklib.BODY_FONT_BOLD, 11)
    c.drawString(mklib.MARGIN, y, f"Notice Type: {d['notice_type']}")
    y -= 22

    # -- the four-cell top table --
    col = (mklib.PAGE_W - 2 * mklib.MARGIN) / 2.0
    rows = [
        [("RECEIPT NUMBER", d["receipt_number"], col),
         ("CASE TYPE", d["case_type"], col)],
        [("RECEIVED DATE", mklib.fmt_long(d["received_date"]), col),
         ("PRIORITY DATE", "", col)],
        [("NOTICE DATE", mklib.fmt_long(d["notice_date"]), col),
         ("PAGE", "1 of 1", col)],
        [("APPLICANT", applicant_name, col + 96),
         ("A-NUMBER", d["a_number"], col - 96)],
    ]
    y = _draw_table(c, mklib.MARGIN, y, rows) - 24

    # -- notice body --
    body = (
        f"This notice confirms receipt of Form I-751, Petition to Remove "
        f"Conditions on Residence, filed by the above-named applicant. "
        f"Please verify the information above is correct and retain this "
        f"notice; refer to the receipt number in any correspondence "
        f"regarding this case."
    )
    y = _paragraph(c, body, y)
    y -= mklib.LEADING
    c.setFont(mklib.BODY_FONT, mklib.BODY_PT)
    c.drawString(mklib.MARGIN, y, f"Fee Paid: ${d['fee_paid']}")

    c.save()
    return [_finish(path)]


# =====================================================================
# Joint deed
# =====================================================================
def _render_joint_deed(mk: dict, outdir: str, doc: dict) -> list[str]:
    ev = _evidence(mk, "deed")
    if ev is None or ev.get("supplied", True) is False:
        raise ValueError(
            "documents.evidence has no supplied 'deed' entry for a joint_deed "
            "DOCUMENT — refusing to render (SPEC-DELTA D-I)")

    path = mklib.component_path(outdir, doc, "pdf")
    c = mklib.new_canvas(path)
    width = mklib.PAGE_W - 2 * mklib.MARGIN

    c.setFont(mklib.BODY_FONT_BOLD, 16)
    c.drawCentredString(mklib.PAGE_W / 2.0, mklib.PAGE_H - mklib.MARGIN - 4,
                         "WARRANTY DEED")
    y = mklib.PAGE_H - mklib.MARGIN - 40

    granting = (
        f"KNOW ALL PERSONS BY THESE PRESENTS, that {ev['grantors']} "
        f"(\"Grantor\"), for valuable consideration paid, the receipt of "
        f"which is hereby acknowledged, in the amount of {ev['consideration']}, "
        f"do(es) hereby grant, bargain, sell and convey unto "
        f"{ev['grantees']} (\"Grantee\"), the following described real "
        f"property:"
    )
    y = _paragraph(c, granting, y, max_width=width)
    y -= mklib.LEADING

    y = mklib.frame_text(c, [
        ev["property_address"],
    ], top=y)
    y -= mklib.LEADING

    y = mklib.frame_text(c, [
        f"Situated in: {ev['county']}",
    ], top=y)
    y -= mklib.LEADING * 2

    closing = (
        "TO HAVE AND TO HOLD the above-described premises, together with "
        "all the appurtenances thereunto belonging, unto the Grantee, "
        "and Grantee's heirs and assigns forever."
    )
    y = _paragraph(c, closing, y, max_width=width)

    # -- recorder's stamp block --
    box_w, box_h = 260.0, 96.0
    box_x = mklib.PAGE_W - mklib.MARGIN - box_w
    box_y = mklib.MARGIN
    c.rect(box_x, box_y, box_w, box_h, stroke=1, fill=0)
    indent = box_x - mklib.MARGIN + 6
    stamp_lines = [
        ("RECORDED", {"bold": True, "indent": indent}),
        (f"Instrument No. {ev['instrument_number']}", {"indent": indent}),
        (f"Recording Date: {mklib.fmt_long(ev['recording_date'])}",
         {"indent": indent}),
        (f"{ev['county']} Recorder", {"indent": indent}),
    ]
    mklib.frame_text(c, stamp_lines, top=box_y + box_h - 16, size=10,
                      leading=18)

    c.save()
    return [_finish(path)]


# =====================================================================
# Joint automobile insurance policy — declarations page
# =====================================================================
def _render_auto_policy(mk: dict, outdir: str, doc: dict) -> list[str]:
    ev = _evidence(mk, "auto_policy")
    if ev is None or ev.get("supplied", True) is False:
        raise ValueError(
            "documents.evidence has no supplied 'auto_policy' entry for an "
            "auto_policy DOCUMENT — refusing to render (SPEC-DELTA D-I, T1 "
            "negative control)")

    path = mklib.component_path(outdir, doc, "pdf")
    c = mklib.new_canvas(path)

    c.setFont(mklib.BODY_FONT_BOLD, 15)
    c.drawCentredString(mklib.PAGE_W / 2.0, mklib.PAGE_H - mklib.MARGIN - 4,
                         ev["insurer"].upper())
    c.setFont(mklib.BODY_FONT_BOLD, 12)
    c.drawCentredString(mklib.PAGE_W / 2.0, mklib.PAGE_H - mklib.MARGIN - 22,
                         "DECLARATIONS PAGE")
    y = mklib.PAGE_H - mklib.MARGIN - 50
    c.line(mklib.MARGIN, y, mklib.PAGE_W - mklib.MARGIN, y)
    y -= 20

    lines = [f"Policy Number: {ev['policy_number']}",
             "",
             ("Named Insureds:", {"bold": True})]
    for name in ev["named_insureds"]:
        lines.append((name, {"bold": True, "indent": 18}))
    lines += [
        "",
        f"Policy Period: {mklib.fmt_long(ev['policy_period']['effective'])} "
        f"to {mklib.fmt_long(ev['policy_period']['expiry'])}",
        "",
        f"Garaging Address: {ev['garaging_address']}",
        "",
        ("Vehicles:", {"bold": True}),
    ]
    for v in ev["vehicles"]:
        lines.append((v, {"indent": 18}))
    lines += ["", ("Coverages:", {"bold": True})]
    for cov in ev["coverages"]:
        lines.append((cov, {"indent": 18}))

    mklib.frame_text(c, lines, top=y)

    c.save()
    return [_finish(path)]


if __name__ == "__main__":
    import sys
    slug = sys.argv[1] if len(sys.argv) > 1 else "kavanagh_liam"
    doc_id = sys.argv[2] if len(sys.argv) > 2 else "i797c"
    mk = mklib.load_masterkey(slug)
    outdir = mklib.ensure_outdir(os.path.join(mklib.CLIENTS, slug, "output"))
    doc = mklib.doc_by_id(mk, doc_id)
    print(render(mk, outdir, doc))

#!/usr/bin/env python3
"""render_docs.py — every firm-authored page, plus EVERY DIVIDER.

Contract: tools/RENDER-CONTRACT.md. Strings: templates/*.yaml joined through
templates/document-catalog.yaml (SPEC-DELTA D-C: one join table, never prose).

Owns:
  pre-documents  00. Applicant Cover Page        (docx + pdf)   STYLE-SPEC §4.1
                 A-0 / B-0. Tab Cover Page       (docx + pdf)   §4.2, §16 r2
  DOCUMENT 1     A-1. Table of Contents          (docx + pdf)   §4.4
  DOCUMENT 2     A-2. Cover Letter               (docx + pdf)   §5, §7, §16 r7/r8
  C6             B-n. Written Explanation        (docx + pdf)   §9.2 C6
  ALL DIVIDERS   <TAB>-<n>.pdf, one per DOCUMENT (pdf)          §4.3, §16 r3

WHY THE DIVIDERS LIVE HERE. Fifteen divider titles, five renderers: if each
renderer emitted its own divider they would drift, and §4.4's count lock would
catch it only after a full build. One writer, one loop, one source
(document-catalog.yaml). RENDER-CONTRACT §0.4 forbids anyone else writing a
bare numbered pdf.

NO FIRM IDENTITY ANYWHERE (§16 r7). The cover letter's signature block is
`Sincerely,` / blank / blank / `Petition Preparer` — a role, never a name.
"""
from __future__ import annotations

import os
import sys

import mklib

HANDLES = {"table_of_contents", "cover_letter", "written_explanation"}


# =====================================================================
# dividers  — §4.3 as amended by §16 ruling 3 (12 pt, not 24)
# =====================================================================
def render_divider(outdir: str, doc: dict) -> str:
    """The bare numbered pdf. STYLE-SPEC §2's naming collision lives here."""
    path = mklib.divider_path(outdir, doc)
    c = mklib.new_canvas(path)
    size = mklib.DIVIDER_PT
    top = mklib.PAGE_H - mklib.MARGIN - size
    lead = size * 1.15
    c.setFont(mklib.BODY_FONT_BOLD, size)
    c.drawCentredString(mklib.PAGE_W / 2.0, top, f"DOCUMENT {doc['seq']}")
    c.setFont(mklib.BODY_FONT, size)
    c.drawCentredString(mklib.PAGE_W / 2.0, top - 2 * lead, doc["divider_title"])
    c.showPage()
    c.save()
    return path


def render_all_dividers(mk: dict, outdir: str) -> list:
    return [render_divider(outdir, d) for d in mklib.doc_entries(mk)]


# =====================================================================
# pre-documents
# =====================================================================
def render_applicant_cover_page(mk: dict, outdir: str) -> list:
    """STYLE-SPEC §4.1. Note COB/CON, not COB/COC. Mixed case with honorific."""
    ident = mk["identity"]
    d = mklib.new_docx()
    mklib.add_para(d, "APPLICATION FOR NATURALIZATION", align="center", underline=True)
    mklib.add_blank(d)
    mklib.add_blank(d)
    mklib.add_para(d, "APPLICANT:")
    mklib.add_blank(d)
    mklib.add_para(d, f"{ident['honorific']} {mklib.full_legal_name(mk)}")
    mklib.add_para(d, f"DOB: {mklib.fmt_numeric(ident['dob'])}")
    mklib.add_para(d, f"COB/CON: {ident.get('cover_page_cob_con') or ident['cob']}")
    mklib.add_blank(d)
    mklib.add_para(d, f"Classification Basis: {mklib.classification_basis(mk)}")
    docx_path = os.path.join(mklib.ensure_outdir(outdir), "00. Applicant Cover Page.docx")
    mklib.save_docx(d, docx_path)
    return [docx_path, mklib.docx_to_pdf(docx_path)]


def render_tab_cover_page(mk: dict, outdir: str, tab: str) -> list:
    """§4.2 as amended by §16 ruling 2: TAB A/SUMMARY, TAB B/BIOGRAPHICAL
    INFORMATION. The plural SUMMARIES and the bare BIOGRAPHICAL are DEAD.
    Tab covers stay at 24 pt — §16 r3 lowered the DIVIDERS only."""
    cat = {p["id"]: p for p in mklib.pre_documents()}
    entry = cat["tab_a_cover" if tab == "A" else "tab_b_cover"]
    pt = mklib.TAB_COVER_PT
    d = mklib.new_docx()
    mklib.add_para(d, entry["strings"]["line1"], align="center", bold=True, size_pt=pt)
    mklib.add_blank(d, size_pt=pt)
    mklib.add_para(d, entry["strings"]["line2"], align="center", size_pt=pt)
    docx_path = os.path.join(mklib.tab_dir(outdir, tab), f"{tab}-0. Tab Cover Page.docx")
    mklib.save_docx(d, docx_path)
    return [docx_path, mklib.docx_to_pdf(docx_path)]


# =====================================================================
# DOCUMENT 1 — table of contents (§4.4)
# =====================================================================
def _toc_paragraph(d, number, text):
    """List geometry from §4.4: number at 0.25", text at 0.5".

    Rendered as a hanging-indent paragraph with a literal number rather than a
    Word numbering definition. Same measured geometry, and it survives
    `soffice --convert-to pdf` unchanged; a numId/ilvl list does not reliably.
    Recorded as a Phase 3 decision.
    """
    from docx.shared import Inches
    p = mklib.add_para(d, f"{number}.\t{text}", indent_in=0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    return p


def render_toc(mk: dict, outdir: str, doc: dict) -> list:
    docs = mklib.doc_entries(mk)
    d = mklib.new_docx()
    mklib.add_para(d, "TABLE OF CONTENTS", align="center", bold=True, underline=True)
    mklib.add_blank(d)
    for tab, heading in (("A", "Tab A (Summary)"),
                         ("B", "Tab B (Biographical Information)")):
        mklib.add_para(d, heading, bold=True, indent_in=0.25)
        mklib.add_blank(d)
        for e in docs:
            if e["tab"] != tab:
                continue
            _toc_paragraph(d, e["seq"], e["toc_line"])
            mklib.add_blank(d)
    docx_path = mklib.component_path(outdir, doc, "docx")
    mklib.save_docx(d, docx_path)
    return [docx_path, mklib.docx_to_pdf(docx_path)]


# =====================================================================
# DOCUMENT 2 — cover letter (§5, §5.1, §5.2, §7)
# =====================================================================
def render_cover_letter(mk: dict, outdir: str, doc: dict) -> list:
    ident = mk["identity"]
    matter = mk["matter"]
    carrier = matter["carrier"]
    block = mklib.lockbox_block(mklib.residence_state(mk), carrier)
    honorific = ident["honorific"]
    full = mklib.full_legal_name(mk)

    d = mklib.new_docx()
    mklib.add_para(d, mklib.fmt_long(matter["filed_date"]))
    mklib.add_blank(d)

    mklib.add_para(d, f"VIA {carrier}", bold=True, underline=True, spacing_after=0)
    for line in block:
        mklib.add_para(d, line, spacing_after=0)
    mklib.add_blank(d)

    tabs = (0.5, 1.0, 1.5, 2.0)
    mklib.add_para(d, "\tRe:\tForm N-400, Application for Naturalization", tab_stops_in=tabs)
    mklib.add_blank(d)
    mklib.add_para(d, f"\t\tApplicant:\t{honorific} {full}", tab_stops_in=tabs)
    mklib.add_para(d, f"\t\tDOB:\t\t{mklib.fmt_long(ident['dob'])}", tab_stops_in=tabs)
    mklib.add_para(d, f"\t\tCOB/CON:\t{ident.get('cover_page_cob_con') or ident['cob']}",
                   tab_stops_in=tabs)
    mklib.add_blank(d)

    mklib.add_para(d, "To Whom It May Concern:")
    mklib.add_blank(d)

    article = ident.get("nationality_article") or (
        "an" if str(ident["nationality_adjective"])[0].upper() in "AEIOU" else "a")
    mklib.add_para(
        d,
        "Enclosed please find one (1) Form N-400, Application for Naturalization, "
        f"along with the accompanying filing fee of ${matter['fee']} and supporting "
        f"documentation, for {honorific} {full}, {article} "
        f"{ident['nationality_adjective']} national. {honorific} "
        f"{ident['family_name']} is eligible for naturalization "
        f"{mklib.eligibility_clause(mk)}. See {mklib.citation(mk)}.",
        align="both", spacing_after=0)
    mklib.add_blank(d)

    mklib.add_para(
        d,
        "All supporting documents in this packet are photocopies of originals. "
        f"{honorific} {ident['family_name']} understands that "
        f"{ident['pronoun_subject']} may have to present originals as part of the "
        "adjudication process.", align="both", spacing_after=0)
    mklib.add_blank(d)

    mklib.add_para(d, "We look forward to your speedy and favorable adjudication of "
                      "this application.", align="both", spacing_after=0)
    mklib.add_blank(d)

    # §16 r7 / SPEC-DELTA D-B: role only. No firm name, no preparer name, no "By:".
    mklib.add_para(d, "Sincerely,", spacing_after=0)
    mklib.add_blank(d)
    mklib.add_blank(d)
    mklib.add_blank(d)
    mklib.add_para(d, "Petition Preparer", spacing_after=0)

    docx_path = mklib.component_path(outdir, doc, "docx")
    mklib.save_docx(d, docx_path)
    return [docx_path, mklib.docx_to_pdf(docx_path)]


# =====================================================================
# C6 — written explanation (§9.2 C6)
# =====================================================================
def render_written_explanation(mk: dict, outdir: str, doc: dict) -> list:
    """One titled page carrying the Part 9 answers the form's own table cannot.

    Which items those are is NOT re-derived here: rule_inputs.part14_items_yes
    is computed once, in the normaliser, from the printed Part 9 item table.
    """
    ident = mk["identity"]
    items = (mk.get("rule_inputs") or {}).get("part14_items_yes") or []
    mc = mk.get("moral_character") or {}

    d = mklib.new_docx()
    mklib.add_para(d, "WRITTEN EXPLANATION", align="center")
    mklib.add_blank(d)
    mklib.add_para(
        d,
        f"The following explanation is submitted on behalf of {ident['honorific']} "
        f"{mklib.full_legal_name(mk)} in support of {ident['pronoun_possessive']} "
        "Form N-400, Application for Naturalization, and responds to the items "
        "indicated in Part 9. Additional Information About You.",
        align="both", spacing_after=0)
    mklib.add_blank(d)
    for item in items:
        q = mc.get(f"q{item}") or {}
        mklib.add_para(d, f"Part 9., Item Number {item}.", bold=True, spacing_after=0)
        mklib.add_blank(d)
        text = q.get("explanation") or q.get("text") or ""
        mklib.add_para(d, " ".join(str(text).split()), align="both", spacing_after=0)
        mklib.add_blank(d)
    docx_path = mklib.component_path(outdir, doc, "docx")
    mklib.save_docx(d, docx_path)
    return [docx_path, mklib.docx_to_pdf(docx_path)]


# =====================================================================
# the contract
# =====================================================================
_DISPATCH = {
    "table_of_contents": render_toc,
    "cover_letter": render_cover_letter,
    "written_explanation": render_written_explanation,
}


def render(masterkey: dict, outdir: str, doc: dict) -> list:
    if doc["id"] not in HANDLES:
        raise ValueError(f"render_docs.py does not handle {doc['id']!r}")
    return _DISPATCH[doc["id"]](masterkey, outdir, doc)


def render_pre_documents(mk: dict, outdir: str) -> list:
    out = render_applicant_cover_page(mk, outdir)
    for tab in ("A", "B"):
        out += render_tab_cover_page(mk, outdir, tab)
    return out


def render_firm_pages(mk: dict, outdir: str) -> list:
    """Everything this module owns: pre-documents, its DOCUMENTs, all dividers."""
    out = render_pre_documents(mk, outdir)
    for doc in mklib.doc_entries(mk):
        if doc["id"] in HANDLES:
            out += render(mk, outdir, doc)
    out += render_all_dividers(mk, outdir)
    return out


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        mklib.CLIENTS, slug, "output")
    mk = mklib.load_masterkey(slug)
    mklib.ensure_outdir(outdir)
    for p in render_firm_pages(mk, outdir):
        if p.endswith(".pdf"):
            print(f"{mklib.pdf_pagecount(p):>3} pp  {os.path.relpath(p, outdir)}")
        else:
            print(f"       {os.path.relpath(p, outdir)}")

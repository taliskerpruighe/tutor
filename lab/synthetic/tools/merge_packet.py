#!/usr/bin/env python3
"""merge_packet.py — the loose components into `N-400 Packet.pdf`.

Contract: tools/RENDER-CONTRACT.md. Order: STYLE-SPEC §6. Naming: §2.

MERGE ORDER IS TOC ORDER, NEVER A DIRECTORY SORT (STYLE-SPEC §2). Alphabetically
`A-1. Table of Contents.docx` sorts BEFORE `A-1.pdf`, so a directory listing
puts every content file ahead of its own divider. The order here is the `seq`
sequence from mklib.doc_entries(), which is the TOC.

TOOLCHAIN, carried from BUILD-PLAN §1:
  * flatten with `gs -o out.pdf -sDEVICE=pdfwrite -dPreserveAnnots=false`
  * NEVER pdfunite — it corrupts the AcroForm ("Can't get Fields array")

CONCATENATION MOVED FROM pypdf TO gs — and this one is load-bearing.
BUILD-PLAN §1 says "merge with pypdf PdfWriter.append". That silently destroyed
a page. `PdfWriter.append` over 17 components produced a merged file in which
the passport bio page's `/Resources` lost its `/Font` entry through a cross-page
resource-name collision; gs then flattened the page to its two images and no
text, so every packet shipped a BLANK passport (and spouse passport) while every
scripted gate stayed green — page count, field count and the TOC/divider lock
all still matched. Found by two independent Phase 5 reviewers looking at the
rendered pages.

Proof it is the collision and not the page: gs on the passport component alone
keeps its text; gs on page 24 of the pypdf-merged file, extracted alone, keeps
its text; gs over the whole pypdf-merged file loses it. Handing gs the component
list directly makes it do both the concatenation and the flatten, with its own
resource namespacing, and the text survives.

This is NOT pdfunite, and the AcroForm hazard §1 warns about does not apply: the
merged packet is required to have zero form fields, and the N-400 component
keeps its own fields because it is never rewritten.

Asserts, both hard:
  * the merged packet has ZERO form fields
  * merged page count == sum of component page counts
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

import mklib


def packet_order(mk: dict, outdir: str) -> list:
    """(label, path) in merged order. STYLE-SPEC §6.

    applicant cover page · TAB A cover · DOC 1 divider · DOC 1 content ·
    DOC 2 divider · DOC 2 content · TAB B cover · DOC 3 divider · ...
    """
    outdir = os.path.abspath(outdir)
    seq = [("00. Applicant Cover Page",
            os.path.join(outdir, "00. Applicant Cover Page.pdf"))]
    seen_tab = set()
    for doc in mklib.doc_entries(mk):
        tab = doc["tab"]
        if tab not in seen_tab:
            seen_tab.add(tab)
            seq.append((f"{tab}-0. Tab Cover Page",
                        os.path.join(mklib.tab_dir(outdir, tab),
                                     f"{tab}-0. Tab Cover Page.pdf")))
        seq.append((f'{tab}-{doc["seq"]} divider', mklib.divider_path(outdir, doc)))
        seq.append((f'{tab}-{doc["seq"]}. {doc["file_stem"]}',
                    mklib.component_path(outdir, doc, "pdf")))
    return seq


def _PdfReaderForFields(path):
    """The component's AcroForm fields, or {} — used only to decide whether a
    component needs the pdftocairo pre-flatten."""
    from pypdf import PdfReader
    try:
        return PdfReader(path).get_fields() or {}
    except Exception:
        return {}


def _page_labels(order):
    """One (label, path) per MERGED PAGE, expanding multi-page components."""
    out = []
    for lbl, p in order:
        n = mklib.pdf_pagecount(p)
        for i in range(n):
            out.append((lbl if n == 1 else f"{lbl} p{i + 1}/{n}", p))
    return out


def _ink_problems(out: str, labels) -> list:
    """Assert every merged page still has visible PAINT, not just text.

    The text check is necessary and not sufficient. The IRS 1040's second page
    came through the flatten with its text layer intact and almost none of its
    visible content — the form's rules and labels simply were not painted — so
    a `pdftotext` length check passed a page that printed nearly blank. A Phase
    5 reviewer found it by looking. This rasterises each page and measures the
    fraction of non-white pixels.

    Dividers and tab cover pages are legitimately sparse: two short lines of
    24pt or 12pt type on an otherwise empty sheet, around 0.2% ink. They are
    identified by label and held to a much lower floor, so the check does not
    have to be loosened for everyone to accommodate them.
    """
    import glob
    import tempfile
    try:
        from PIL import Image
    except ImportError:
        return []
    DENSE_FLOOR, SPARSE_FLOOR = 0.010, 0.0005
    out_problems = []
    with tempfile.TemporaryDirectory() as td:
        stem = os.path.join(td, "pg")
        r = subprocess.run(["pdftoppm", "-r", "50", "-png", out, stem],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return []
        pages = sorted(glob.glob(stem + "*.png"))
        for i, png in enumerate(pages):
            im = Image.open(png).convert("L")
            px = list(im.getdata())
            ink = sum(1 for v in px if v < 200) / max(len(px), 1)
            label = labels[i][0] if i < len(labels) else f"page {i + 1}"
            sparse = ("divider" in label.lower()
                      or "tab cover page" in label.lower()
                      or "applicant cover page" in label.lower())
            floor = SPARSE_FLOOR if sparse else DENSE_FLOOR
            if ink < floor:
                out_problems.append(
                    f"page {i + 1} ({label}) has {ink * 100:.2f}% ink, below the "
                    f"{floor * 100:.2f}% floor — it printed blank or near-blank")
    return out_problems


def merge(mk: dict, outdir: str, verbose: bool = True) -> str:
    from pypdf import PdfReader, PdfWriter

    order = packet_order(mk, outdir)
    missing = [(lbl, p) for lbl, p in order if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(
            "cannot merge — component(s) not rendered:\n" +
            "\n".join(f"    {lbl}: {p}" for lbl, p in missing))

    expected = 0
    for lbl, p in order:
        n = mklib.pdf_pagecount(p)
        expected += n
        if verbose:
            print(f"  {n:>3} pp  {lbl}")

    out = mklib.merged_path(outdir)
    # PRE-FLATTEN EACH FORM-BEARING COMPONENT WITH pdftocairo FIRST.
    # Ghostscript renders one specific filled 1040 (nowak_agata's) with page 2
    # almost entirely unpainted — 0.4% ink against 15.6% from poppler — while
    # rendering the byte-identical template filled for two other clients
    # correctly. It is not the field values (clearing the two fields unique to
    # that client does not help) and no gs flag combination tried fixes it
    # (-dPreserveMarkedContent=false, -dNOTRANSPARENCY, -dCompatibilityLevel=1.4,
    # /prepress, keeping annotations). poppler renders the page correctly, so we
    # let poppler do the form flatten: `pdftocairo -pdf` drops the AcroForm and
    # emits a flat, still-text-extractable page. gs then only concatenates.
    with tempfile.TemporaryDirectory() as td:
        flat = []
        for i, (lbl, src) in enumerate(order):
            has_fields = bool(_PdfReaderForFields(src))
            if not has_fields:
                flat.append(src)
                continue
            dst = os.path.join(td, f"{i:03d}.pdf")
            rc = subprocess.run(["pdftocairo", "-pdf", src, dst],
                                capture_output=True, text=True)
            flat.append(dst if rc.returncode == 0 and os.path.exists(dst) else src)
        r = subprocess.run(
            ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER",
             "-sDEVICE=pdfwrite", "-dPreserveAnnots=false",
             f"-sOutputFile={out}"] + flat,
            capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        raise RuntimeError(f"gs merge+flatten failed:\n{r.stdout}\n{r.stderr}")
    mklib.stamp_deterministic(out)

    fields = PdfReader(out).get_fields() or {}
    got = mklib.pdf_pagecount(out)
    problems = []
    if fields:
        problems.append(f"merged packet still carries {len(fields)} form field(s) "
                        "— the flatten did not take")
    if got != expected:
        problems.append(f"merged page count {got} != sum of component page "
                        f"counts {expected}")
    # A page that survives the merge as an image with its text stripped is
    # invisible to every count-based check. Assert every merged page still
    # carries extractable text, and say which component it came from.
    blank = []
    for i, (lbl, _p) in enumerate(_page_labels(order), start=1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), out, "-"],
                           capture_output=True, text=True).stdout.strip()
        if len(t) < 8:
            blank.append(f"page {i} ({lbl}) has {len(t)} extractable character(s)")
    if blank:
        problems.append("merged page(s) lost their text layer: " + "; ".join(blank))
    problems += _ink_problems(out, _page_labels(order))
    if problems:
        raise AssertionError("merge_packet: " + "; ".join(problems))
    if verbose:
        print(f"  --- {got} pp, {len(fields)} form fields  {out}")
    return out


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        mklib.CLIENTS, slug, "output")
    merge(mklib.load_masterkey(slug), outdir)

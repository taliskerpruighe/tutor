#!/usr/bin/env python3
"""render_all.py — Phase 3 driver. One client, start to finish.

Contract: tools/RENDER-CONTRACT.md. For one slug, in order:

  1. load the masterkey via mklib.load_masterkey(slug) (.norm.yaml only)
  2. render the pre-documents and every divider (render_docs.py)
  3. walk mklib.doc_entries(mk) and dispatch each document to the renderer
     whose HANDLES set claims its doc["id"]
  4. run merge_packet.merge() to produce N-400 Packet.pdf
  5. write render-manifest.json: file list, page count + sha256 per file,
     and the N-400 field-fill dump

    python3 render_all.py <slug>
    python3 render_all.py --all

Runs strictly serially — mklib.docx_to_pdf() drives soffice against one fixed
UserInstallation profile (mklib._SOFFICE_PROFILE); concurrent soffice calls
against that profile corrupt or fail. Never parallelise --all.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import mklib
import render_1040
import render_addendum
import render_court_records
import render_docs
import render_evidence
import render_n400
import fabricate_ids
import merge_packet

# --------------------------------------------------------------- route table
# Built from the modules, not hardcoded, so a HANDLES collision or gap is
# caught at import time rather than mid-render.
_RENDERERS = [render_n400, render_docs, render_1040, render_evidence,
              render_court_records, render_addendum, fabricate_ids]

ROUTE: dict[str, object] = {}
for _mod in _RENDERERS:
    for _id in _mod.HANDLES:
        if _id in ROUTE:
            raise RuntimeError(
                f"HANDLES collision: {_id!r} claimed by both "
                f"{ROUTE[_id].__name__} and {_mod.__name__}")
        ROUTE[_id] = _mod

# render_docs.py's own DOCUMENT ids (table_of_contents, cover_letter,
# written_explanation) are rendered via render_docs.render_firm_pages(), which
# also owns the pre-documents and every divider (RENDER-CONTRACT §0.4/§1.1).
# Route everything else through ROUTE so a route gap raises loudly.
_DOCS_OWNED = render_docs.HANDLES


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def preflight(mk: dict, slug: str) -> None:
    """Every doc["id"] the client actually uses must have a route."""
    ids = {d["id"] for d in mklib.doc_entries(mk)}
    unrouted = [i for i in ids if i not in ROUTE and i not in _DOCS_OWNED]
    if unrouted:
        raise RuntimeError(f"{slug}: no renderer HANDLES {unrouted}")


def render_client(slug: str, verbose: bool = True) -> str:
    mk = mklib.load_masterkey(slug)
    outdir = os.path.join(mklib.CLIENTS, slug, "output")
    mklib.ensure_outdir(outdir)
    preflight(mk, slug)

    written: list[str] = []

    # pre-documents (00. Applicant Cover Page, A-0/B-0 tab covers) and every
    # divider. render_docs.py owns these centrally (RENDER-CONTRACT §0.4).
    written += render_docs.render_pre_documents(mk, outdir)
    written += render_docs.render_all_dividers(mk, outdir)

    for doc in mklib.doc_entries(mk):
        doc_id = doc["id"]
        if doc_id in _DOCS_OWNED:
            mod = render_docs
        else:
            mod = ROUTE[doc_id]
        got = mod.render(mk, outdir, doc)
        written += got
        if verbose:
            for p in got:
                pp = mklib.pdf_pagecount(p) if p.endswith(".pdf") else "  -"
                print(f"  {pp:>3}  {os.path.relpath(p, outdir)}  [{mod.__name__}]")

    merged = merge_packet.merge(mk, outdir, verbose=verbose)
    written.append(merged)

    write_manifest(slug, mk, outdir, written)
    return outdir


def write_manifest(slug: str, mk: dict, outdir: str, written: list[str]) -> str:
    files = []
    for p in sorted(set(written)):
        entry = {"path": os.path.relpath(p, outdir), "sha256": _sha256(p)}
        if p.endswith(".pdf"):
            entry["pages"] = mklib.pdf_pagecount(p)
        files.append(entry)

    n400_doc = mklib.doc_by_id(mk, "n400")
    n400_path = mklib.component_path(outdir, n400_doc, "pdf")
    field_dump = mklib.field_values(n400_path) if os.path.exists(n400_path) else {}

    manifest = {
        "slug": slug,
        "document_count": len(mklib.doc_entries(mk)),
        "files": files,
        "n400_field_dump": field_dump,
    }
    path = os.path.join(outdir, "render-manifest.json")
    with open(path, "w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return path


def main(argv: list[str]) -> int:
    if not argv or argv[0] == "--all":
        slugs = mklib.all_slugs()
    else:
        slugs = [argv[0]]
    for slug in slugs:
        print(f"=== {slug} ===")
        render_client(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

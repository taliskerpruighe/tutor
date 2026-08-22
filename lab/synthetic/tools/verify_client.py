#!/usr/bin/env python3
"""verify_client.py — the Phase 5 layer-1 engine. Written in Phase 3, run from
Phase 3 onward (BUILD-PLAN §4, §6). Zero tolerance: any FAIL is a build bug.

    python3 verify_client.py <slug> [outdir]

Checks, in order:
   1  the rendered component set matches the client's DOCUMENT list
   2  N-400 field values re-extracted from the UNFLATTENED component and
      diffed against the masterkey
   3  THE POSITIVE CONTROL (SPEC-DELTA D-E): prove every Part 11 / Part 13 /
      signature field name EXISTS in the blank's 488-name set, and only THEN
      assert Part 13 + signatures empty and Part 11 populated
   4  printed-page evidence: the values actually PRINT, not merely store
   5  TOC line count == divider count == DOCUMENT count, and TOC line n names
      the same document as divider n
   6  cover-letter facts: date, Re: block, lockbox == f(state, carrier),
      eligibility clause and citation match the basis
   7  NO FIRM OR PREPARER IDENTITY anywhere in the packet (§16 r7)
   8  A-numbers agree across green card, every N-400 page header, cover letter
   9  MRZ check digits recompute (ICAO 9303)
  10  filing-window arithmetic (3y-90d / 5y-90d)
  11  the exhibit set matches rule_inputs (never re-derived here)
  12  merged packet: 0 form fields, page count == sum of components
"""
from __future__ import annotations

import os
import re
import sys

import yaml

import mklib

FAILS, WARNS, OKS = [], [], []


def ok(c, m):   OKS.append(f"[ok]   {c}: {m}")
def fail(c, m): FAILS.append(f"[FAIL] {c}: {m}")
def warn(c, m): WARNS.append(f"[warn] {c}: {m}")


def _norm(s):
    """Comb fields extract space-separated under pdftotext; strip whitespace."""
    return re.sub(r"\s+", "", str(s or ""))


def verify(slug: str, outdir: str) -> None:
    mk = mklib.load_masterkey(slug)
    outdir = os.path.abspath(outdir)
    docs = mklib.doc_entries(mk)
    ident, imm, matter = mk["identity"], mk["immigration"], mk["matter"]

    # ---------------------------------------------------- 1 component set
    present, absent = [], []
    for d in docs:
        for ext in d["ships"]:
            p = mklib.component_path(outdir, d, ext)
            (present if os.path.exists(p) else absent).append((d, ext, p))
        dv = mklib.divider_path(outdir, d)
        (present if os.path.exists(dv) else absent).append((d, "divider", dv))
    if absent:
        for d, ext, p in absent:
            fail(slug, f"component missing: {os.path.relpath(p, outdir)} "
                       f"({d['id']}, {ext})")
    else:
        ok(slug, f"all {len(present)} components present for {len(docs)} DOCUMENTs")

    # ---------------------------------------------------- 2 N-400 round trip
    n400_doc = next((d for d in docs if d["id"] == "n400"), None)
    n400 = mklib.component_path(outdir, n400_doc, "pdf") if n400_doc else None
    if not n400 or not os.path.exists(n400):
        fail(slug, "N-400 component absent — cannot verify the form")
        n400 = None
    else:
        import render_n400
        wanted = render_n400.build_values(mk)
        got = mklib.field_values(n400)
        diffs = [(k, v, got.get(k, "")) for k, v in wanted.items()
                 if str(got.get(k, "")).strip() != str(v).strip()]
        if diffs:
            fail(slug, f"N-400 round trip: {len(diffs)} field(s) differ from the "
                       f"masterkey, e.g. {diffs[:3]}")
        else:
            filled = sum(1 for v in wanted.values() if v not in ("", "/Off"))
            ok(slug, f"N-400 round trip: {len(wanted)} fields written, "
                     f"{filled} non-empty, 0 diffs against the masterkey")

    # -------------------------------------- 3 THE POSITIVE CONTROL (D-E)
    # An assertion against a field name that does not exist on this edition
    # passes VACUOUSLY while a filled preparer block ships. So: prove the names
    # exist FIRST, from the blank itself, and only then assert their values.
    fm = yaml.safe_load(open(os.path.join(mklib.TOOLS, "fieldmap_n400.yaml")))
    blank_names = mklib.field_names(mklib.N400_BLANK)
    if len(blank_names) != fm["meta"]["fields"]:
        fail(slug, f"blank carries {len(blank_names)} fields, fieldmap expects "
                   f"{fm['meta']['fields']} — edition drift")

    controlled = {}
    for group, fields in fm["leave_empty"].items():
        controlled[group] = list(fields)
    controlled["part11_fill"] = list(fm["part11_fill"].values())

    ghosts = {g: [f for f in fs if f not in blank_names]
              for g, fs in controlled.items()}
    ghosts = {g: fs for g, fs in ghosts.items() if fs}
    if ghosts:
        for g, fs in ghosts.items():
            fail(slug, f"POSITIVE CONTROL FAILED — {g}: {len(fs)} asserted field "
                       f"name(s) do NOT exist on the 01/20/25 blank, so any "
                       f"emptiness assertion about them passes vacuously: {fs}")
    else:
        total = sum(len(v) for v in controlled.values())
        ok(slug, f"positive control: all {total} controlled field names EXIST in "
                 f"the blank's {len(blank_names)}-name set "
                 f"({len(fm['part11_fill'])} Part 11 fill, "
                 f"{sum(len(v) for g, v in controlled.items() if g != 'part11_fill')} "
                 f"leave-empty across Parts 11/12/13/15/16)")

    if n400 and not ghosts:
        got = mklib.field_values(n400)
        # Part 13 preparer + Part 11 signature + Part 12 + Parts 15/16: EMPTY
        for group, fields in fm["leave_empty"].items():
            dirty = [(f, got.get(f, "")) for f in fields
                     if str(got.get(f, "")).strip() not in ("", "/Off")]
            if dirty:
                fail(slug, f"§16 r10/r11 VIOLATED — {group} is not empty: {dirty}")
            else:
                ok(slug, f"{group}: all {len(fields)} field(s) empty, as §16 requires")
        # Part 11 items 3/4/5: POPULATED, and equal to contact.*
        for path, field in fm["part11_fill"].items():
            want = str(_dig(mk, path))
            have = str(got.get(field, "")).strip()
            if not have:
                fail(slug, f"§16 r10 VIOLATED — printed Part 11 field {field} is "
                           f"EMPTY; it must carry {path} = {want!r}")
            elif have != want:
                fail(slug, f"printed Part 11 {path}: form has {have!r}, "
                           f"masterkey has {want!r}")
            else:
                ok(slug, f"printed Part 11 {path} filled and equals the masterkey "
                         f"({have})")

    # ------------------------------------------ 4 printed-page evidence
    # A field-value diff passes for a checkbox set to a bogus export value: the
    # value stores, the box prints blank. Only the text layer discriminates.
    if n400:
        p1 = mklib.pdf_text(n400, 1, 1)
        if _norm(imm["a_number"]) not in _norm(p1):
            fail(slug, "A-number does not PRINT on N-400 page 1 (comb field empty)")
        else:
            ok(slug, "A-number prints on N-400 page 1")
        p11 = mklib.pdf_text(n400, 11, 12)
        for path, _ in fm["part11_fill"].items():
            val = _dig(mk, path)
            if val and _norm(val) not in _norm(p11):
                fail(slug, f"printed Part 11 {path} = {val!r} stores but does not "
                           "PRINT on page 11")
        if not any(f.startswith("printed Part 11") and "does not" in f for f in FAILS):
            ok(slug, "printed Part 11 contact values appear in the page text layer")

    # ------------------------------- 5 TOC == dividers == DOCUMENT count
    toc_doc = next((d for d in docs if d["id"] == "table_of_contents"), None)
    toc_pdf = mklib.component_path(outdir, toc_doc, "pdf") if toc_doc else None
    if toc_pdf and os.path.exists(toc_pdf):
        text = mklib.pdf_text(toc_pdf)
        lines = re.findall(r"^\s*(\d+)\.\s+(.*\S)\s*$", text, re.M)
        if len(lines) != len(docs):
            fail(slug, f"TOC has {len(lines)} numbered line(s), DOCUMENT count is "
                       f"{len(docs)} (§4.4 lock)")
        else:
            bad = [(n, t, d["toc_line"]) for (n, t), d in zip(lines, docs)
                   if int(n) != d["seq"] or t.strip() != d["toc_line"]]
            if bad:
                fail(slug, f"TOC line/document mismatch: {bad[:3]}")
            else:
                ok(slug, f"TOC: {len(lines)} lines, numbering and wording match the "
                         f"{len(docs)} DOCUMENTs in order")
    else:
        fail(slug, "table of contents pdf absent — cannot check the §4.4 lock")

    dividers = [d for d in docs if os.path.exists(mklib.divider_path(outdir, d))]
    if len(dividers) != len(docs):
        fail(slug, f"{len(dividers)} divider(s) on disk, {len(docs)} DOCUMENTs")
    else:
        bad = []
        for d in docs:
            t = mklib.pdf_text(mklib.divider_path(outdir, d))
            if f"DOCUMENT {d['seq']}" not in t or d["divider_title"] not in t:
                bad.append((d["seq"], d["divider_title"], " ".join(t.split())[:40]))
        if bad:
            fail(slug, f"divider text wrong: {bad[:3]}")
        else:
            ok(slug, f"dividers: {len(docs)} present, each reads DOCUMENT n over "
                     f"its catalog title")

    # ------------------------------------------------ 6 cover-letter facts
    cl_doc = next((d for d in docs if d["id"] == "cover_letter"), None)
    cl_pdf = mklib.component_path(outdir, cl_doc, "pdf") if cl_doc else None
    letter = ""
    if cl_pdf and os.path.exists(cl_pdf):
        letter = mklib.pdf_text(cl_pdf)
        flat = " ".join(letter.split())
        checks = [
            ("filing date", mklib.fmt_long(matter["filed_date"])),
            ("VIA carrier", f"VIA {matter['carrier']}"),
            ("Re: line", "Re: Form N-400, Application for Naturalization"),
            ("applicant", f"{ident['honorific']} {mklib.full_legal_name(mk)}"),
            ("DOB long", mklib.fmt_long(ident["dob"])),
            ("fee", f"${matter['fee']}"),
            ("eligibility clause", mklib.eligibility_clause(mk)),
            ("citation", mklib.citation(mk)),
            ("closing", "Sincerely,"),
            ("role line", "Petition Preparer"),
            ("To Whom", "To Whom It May Concern:"),
        ]
        for label, needle in checks:
            if " ".join(str(needle).split()) not in flat:
                fail(slug, f"cover letter: {label} not found — expected "
                           f"{' '.join(str(needle).split())!r}")
        if not any("cover letter:" in f for f in FAILS):
            ok(slug, f"cover letter carries all {len(checks)} required facts "
                     f"(date, Re: block, fee, {mklib.basis_key(mk)} clause + citation)")
        # lockbox is f(state, carrier) — §7
        block = mklib.lockbox_block(mklib.residence_state(mk), matter["carrier"])
        miss = [l for l in block if " ".join(l.split()) not in flat]
        if miss:
            fail(slug, f"lockbox block wrong for ({mklib.residence_state(mk)}, "
                       f"{matter['carrier']}) — missing lines {miss}")
        else:
            ok(slug, f"lockbox block == f({mklib.residence_state(mk)}, "
                     f"{matter['carrier']}) = {matter['lockbox']} (§7), all "
                     f"{len(block)} lines")
    else:
        fail(slug, "cover letter pdf absent")

    # ---------------------------------- 7 NO FIRM OR PREPARER IDENTITY
    # §16 r7 killed the firm identity question outright, so there is no name to
    # search for. What we can search for is the SHAPES a preparer line takes,
    # across every rendered page.
    scanned, hits = 0, []
    for d in docs:
        for p in [mklib.component_path(outdir, d, "pdf"),
                  mklib.divider_path(outdir, d)]:
            if not os.path.exists(p):
                continue
            scanned += 1
            for pat, txt in mklib.firm_identity_hits(mklib.pdf_text(p)):
                hits.append((os.path.basename(p), txt))
    cover = os.path.join(outdir, "00. Applicant Cover Page.pdf")
    if os.path.exists(cover):
        scanned += 1
        for pat, txt in mklib.firm_identity_hits(mklib.pdf_text(cover)):
            hits.append(("00. Applicant Cover Page.pdf", txt))
    # the client's own tax preparer is a third party and may appear on the 1040,
    # but must appear NOWHERE else (RENDER-CONTRACT §0.1)
    tax_prep = _dig(mk, "documents.tax_return.preparer_name")
    if tax_prep:
        for d in docs:
            if d["id"] == "tax_return":
                continue
            p = mklib.component_path(outdir, d, "pdf")
            if os.path.exists(p) and str(tax_prep) in mklib.pdf_text(p):
                hits.append((os.path.basename(p), f"tax preparer {tax_prep!r}"))
    if hits:
        fail(slug, f"§16 r7 VIOLATED — firm/preparer identity on {len(hits)} "
                   f"page(s): {hits[:5]}")
    else:
        ok(slug, f"no firm or preparer identity on any of {scanned} rendered "
                 f"component(s) (§16 r7)")
    if letter and re.search(r"\bBy:\s*\S", letter):
        fail(slug, "cover letter signature block still carries a 'By:' line "
                   "(SPEC-DELTA D-B: role only)")

    # ------------------------------------------------ 8 A-number agreement
    a = _norm(imm["a_number"])
    gc = _norm(_dig(mk, "documents.green_card.a_number"))
    if gc and gc != a:
        fail(slug, f"green card A-number {gc} != immigration.a_number {a} (§9.4)")
    else:
        ok(slug, f"A-number {imm['a_number']} agrees across masterkey and green card")
    if n400:
        got = mklib.field_values(n400)
        badhdr = [f for f in fm["a_number_headers"]["fields"]
                  if _norm(got.get(f, "")) != a]
        if badhdr:
            fail(slug, f"{len(badhdr)} of 14 N-400 page headers carry the wrong "
                       f"A-number")
        else:
            ok(slug, "A-number present and correct on all 14 N-400 page headers")

    # ------------------------------------------------ 9 MRZ
    for name, obj in (mk.get("documents") or {}).items():
        if not isinstance(obj, dict) or not isinstance(obj.get("mrz"), dict):
            continue
        m = obj["mrz"]
        probs = mklib.mrz_verify(str(m.get("line1", "")), str(m.get("line2", "")))
        if probs:
            fail(slug, f"{name}: " + "; ".join(probs))
        else:
            ok(slug, f"{name}: MRZ all four ICAO 9303 check digits recompute")

    # ------------------------------------------------ 10 filing window
    lpr = mklib.as_date(imm["lpr_date"])
    filed = mklib.as_date(matter["filed_date"])
    yrs = 3 if mklib.basis_key(mk) == "319a" else 5
    import datetime
    earliest = datetime.date(lpr.year + yrs, lpr.month, lpr.day) - datetime.timedelta(days=90)
    if filed < earliest:
        fail(slug, f"filed {filed} is BEFORE the earliest filing date {earliest} "
                   f"({yrs}y-90d from LPR {lpr})")
    else:
        ok(slug, f"filing window: filed {filed}, earliest {earliest}, "
                 f"margin +{(filed - earliest).days}d ({yrs}y-90d)")

    # ------------------------------------------------ 11 exhibit set
    CORE = ["table_of_contents", "cover_letter", "n400", "applicant_passport",
            "green_card", "tax_return"]
    r = mk.get("rule_inputs") or {}
    expect = list(CORE)
    for flag, doc_id in (("c1_fires", "spouse_passport"), ("c2_fires", "i797c"),
                         ("c3a_fires", "joint_deed"), ("c3b_fires", "auto_policy"),
                         ("c3c_fires", "child_passport"),
                         ("c4_fires", "travel_addendum"),
                         ("c5_fires", "court_records"),
                         ("c6_fires", "written_explanation")):
        if r.get(flag):
            expect.append(doc_id)
    have = [d["id"] for d in docs]
    if set(have) != set(expect):
        fail(slug, "rendered DOCUMENT set != rule_inputs\n"
                   f"        rendered only: {sorted(set(have) - set(expect))}\n"
                   f"        rule only    : {sorted(set(expect) - set(have))}")
    else:
        ok(slug, f"DOCUMENT set matches rule_inputs ({len(have)} documents; "
                 f"fires {','.join(k[:-6].upper() for k in r if k.endswith('_fires') and r[k]) or '-'})")
    for declined in (r.get("evidence_declined") or []):
        if declined in have:
            fail(slug, f"{declined} was DECLINED (supplied: false) but is in the packet")
        else:
            ok(slug, f"negative control holds: declined evidence {declined} is absent")

    # ------------------------------------------------ 12 merged packet
    merged = mklib.merged_path(outdir)
    if not os.path.exists(merged):
        warn(slug, "N-400 Packet.pdf not merged yet — skipping merged checks")
    else:
        from pypdf import PdfReader
        import merge_packet
        fields = PdfReader(merged).get_fields() or {}
        if fields:
            fail(slug, f"merged packet carries {len(fields)} form field(s); "
                       "it must carry 0 (flatten did not take)")
        else:
            ok(slug, "merged packet carries 0 form fields")
        expected = sum(mklib.pdf_pagecount(p)
                       for _, p in merge_packet.packet_order(mk, outdir)
                       if os.path.exists(p))
        got_pages = mklib.pdf_pagecount(merged)
        if got_pages != expected:
            fail(slug, f"merged page count {got_pages} != sum of component page "
                       f"counts {expected} (§9.4)")
        else:
            ok(slug, f"merged page count {got_pages} == sum of component page counts")


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


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "almeida_paulo"
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        mklib.CLIENTS, slug, "output")
    verify(slug, outdir)
    print("\n".join(OKS))
    if WARNS:
        print()
        print("\n".join(WARNS))
    if FAILS:
        print()
        print("\n".join(FAILS))
        print(f"\n=== CLIENT RED: {len(FAILS)} failure(s), {len(WARNS)} warning(s) ===")
        sys.exit(1)
    print(f"\n=== CLIENT GREEN: {len(OKS)} checks passed, {len(WARNS)} warning(s) ===")

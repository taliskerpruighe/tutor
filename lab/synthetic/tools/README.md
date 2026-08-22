# `lab/synthetic/tools/` — the build tree

Skeleton written in Phase 1. **Phase 3's toolsmith writes the code**; this file
fixes the file list, the contract of each file, and which section of
`../spec/STYLE-SPEC.md` governs it. Nothing here is a renderer.

Everything is driven by one masterkey per client
(`../clients/<slug>/masterkey.yaml`). No tool reads `lab/<real client>/` — the
corpus quarantine (BUILD-PLAN §0.2) allows exactly one exception, and it is
already built: `build_blocklist.py`.

Committed blanks live in `../blanks/`:

| file | what | fetched |
|---|---|---|
| `n-400.pdf` | blank N-400, **edition 01/20/25**, 14 pp, 488 AcroForm fields, 776,244 B | 2026-08-21, uscis.gov |
| `f1040.pdf` | blank 1040, tax year **2025**, 2 pp, 229 fields | 2026-08-21, irs.gov |
| `f1040--2024.pdf` | blank 1040, tax year **2024**, 2 pp, 155 fields | 2026-08-21, irs.gov |

BUILD-PLAN §1 records the N-400 blank as edition 04/01/24. It is not; see
STYLE-SPEC §13 D1. Two 1040 years are committed because "latest tax return"
depends on the filing date (STYLE-SPEC §13 D11).

---

## Already built (Phase 1)

### `build_blocklist.py`
- **in:** every `.txt` sidecar, every email body, every `.md` report and every
  file and directory name under `lab/`, excluding `lab/synthetic/` and
  `lab/BUILD-PLAN.md` (which names the six *synthetic* clients); **plus an OCR
  pass over the 54 image-only PDFs** whose sidecars are the stub
  `[NO TEXT LAYER — …]`, via `pdftoppm -r 200 -gray` and `tesseract`.
- **out:** `../blocklist.txt` — one token per line, deduped, sorted.
- **governed by:** STYLE-SPEC §11 (SHARED STRINGS — NOT LEAKAGE) and §11.1
  (what the list can and cannot see). The exclusion sets in the script and
  §11 must stay in step: anything the house style requires every packet to
  contain must never reach the list, or the Phase 5 gate fails on all six
  clients by construction.
- **DO NOT RERUN IN PHASE 2-6.** `../blocklist.txt` (12,454 tokens) and
  `.ocr-cache/` are committed Phase-1 artefacts and are consumed as-is. Rerunning
  invokes the OCR path, which the Phase 2-6 run order forbids.
- **rerun (historical):** `python3 build_blocklist.py` (add `--no-ocr` on a
  machine without tesseract). OCR output is cached by file hash in `.ocr-cache/`, so reruns
  are offline and byte-identical; deleting the cache may shift the token list
  slightly, because tesseract's version is not pinned.
- **known hole, recorded not closed:** OCR of a photographed card or a
  hand-annotated court form is imperfect, so the leakage scan is necessary but
  not sufficient (STYLE-SPEC §11.1). BUILD-PLAN §10 never cuts the scan; this
  limit travels with it into Phase 6.

---

## Phase 3 must build

### `fieldmap_n400.yaml`
- **in:** `../blanks/n-400.pdf` field dump (488 names) + the masterkey schema.
- **out:** a masterkey-path → PDF-field-name map, including the Part 8 travel
  table's row count (which sets the addendum threshold) and the Part 9
  question set.
- **governed by:** STYLE-SPEC §8, §12.
- **build from the committed blank, never from zhu's filed form** — zhu's copy
  is the older 04/01/24 edition and the parts were renumbered.
- **verified by:** scripted round trip (fill → extract → diff) plus one
  page-by-page `pdftoppm` visual pass.

### `render_n400.py`
- **in:** masterkey + `fieldmap_n400.yaml` + `../blanks/n-400.pdf`.
- **out:** `B-3. Form N-400, Application for Naturalization.pdf`, 14 pp, fields
  populated, `/XFA` deleted, `NeedAppearances` set. **NO signature, NO signature
  date, Z003 unused** (§16 ruling 11). **Part 13 preparer block written NOWHERE**
  (§16 ruling 10). **Part 11 — the applicant's own phone and email — IS filled.**
- **governed by:** STYLE-SPEC §16 rulings 10 and 11 (BINDING, they overturn §8
  and taste calls 10/11), then §8 (edition, born-digital) and §12.
- **verifier contract:** `verify_client.py` must PROVE the Part 13 and signature
  field names exist on the 01/20/25 blank (positive control) and THEN assert
  they are empty. An assertion against a non-existent field name passes
  vacuously — the parts were renumbered between editions (§13 D1).

### `render_docs.py`
- **in:** masterkey + `../templates/{cover-page,toc,cover-letter.docx,divider}.yaml`.
- **out:** every firm-authored page as docx **and** pdf via
  `soffice --headless --convert-to pdf` — `00. Applicant Cover Page`,
  `A-0`/`B-0. Tab Cover Page`, `A-1. Table of Contents`, `A-2. Cover Letter`,
  and one bare-numbered divider pdf per DOCUMENT (`A-1.pdf`, `B-3.pdf`, …).
- **governed by:** STYLE-SPEC §2 (file names, the divider/content collision),
  §3 (typography — plain paragraphs only), §4 (every literal string), §5
  (cover letter), §7 (lockbox as `f(state, carrier)`), §9 (which TOC lines
  exist).

### `render_addendum.py`
- **in:** masterkey travel list + the filled N-400's Part 8 page number.
- **out:** `B-n. Travel Addendum.docx` / `.pdf`.
- **governed by:** STYLE-SPEC §4.5 (verbatim intro sentence, en-dash
  separator, most-recent-first order) and §9.2 C4 (when it exists at all).
- BUILD-PLAN §4 proposes openpyxl in the izaguirre shape. **Diverge:** zhu's
  addendum — the modern generation, and the one format source — is a
  firm-authored prose-and-list page, not a spreadsheet. Render it with the
  same python-docx → soffice path as the other firm pages.

### `render_1040.py`
- **in:** masterkey tax facts + `../blanks/f1040.pdf` or `f1040--2024.pdf`.
- **out:** `B-n. {YEAR} Income Tax Return.pdf`, pp. 1–2 filled.
- **governed by:** STYLE-SPEC §12.10 (fact set), §9.1 (it is a core document),
  §13 D11 (which year).

### `render_evidence.py`
- **in:** masterkey `documents.evidence[]`.
- **out:** one PDF per supplied-evidence exhibit, via reportlab — joint deed
  with recorder stamp, auto-policy declarations page, Form I-797C receipt
  notice.
- **governed by:** STYLE-SPEC §9.2 C2/C3 (triggers) and §12.10 (fields).

### `render_court_records.py`
- **in:** masterkey moral-character detail rows.
- **out:** `B-n. Court Records.pdf` — a certified copy of a state court
  charging document showing the disposition (the corpus example is a
  Connecticut Superior Court "Information" with three counts, all `dismissed`,
  a clerk's certification and a raised seal).
- **governed by:** STYLE-SPEC §9.2 C5 and §12.10.

### `fabricate_ids.py`
- **in:** masterkey passport/green-card facts.
- **out:** passport bio-page and Form I-551 (front and back) images and PDFs
  for the **applicant, spouse and child**, with MRZ check digits computed.
  Two finishes: clean flat scan (the acceptable floor) and phone photo
  (perspective, desk texture, shadow, JPEG noise).
- **governed by:** STYLE-SPEC §9.1 (core exhibits 4 and 5), §9.2 C1/C3c,
  §9.4 (MRZ and A-number locks), §12.10.
- **not named in BUILD-PLAN §4**, which mentions "the card/passport
  fabricator" without giving it a file. Named here because the packet's two
  core exhibits depend on it: it is an output tool that Phase 4 also reuses on
  the input side.

### `merge_packet.py`
- **in:** the rendered components + the TOC order.
- **out:** `N-400 Packet.pdf` — merged and flattened, **0 form fields**.
- **governed by:** STYLE-SPEC §2 (merge order is TOC order, never a directory
  sort — `A-1. Table of Contents.docx` sorts *before* `A-1.pdf`), §6 (the page
  sequence, dividers before documents, tab covers before tabs, applicant cover
  page first).
- **toolchain constraints carried from BUILD-PLAN §1, because a Phase 3 agent
  reading only this tree will not otherwise have them:** merge with pypdf
  `PdfWriter.append`; flatten with
  `gs -o out.pdf -sDEVICE=pdfwrite -dPreserveAnnots=false`.
  **Never `pdfunite`** — it corrupts the AcroForm ("Can't get Fields array").

### `verify_client.py`
- **in:** one masterkey + that client's rendered output folder.
- **out:** a pass/fail report; any diff is a build bug, zero tolerance.
- **checks:** re-extract N-400 field values from the unflattened component and
  diff against the masterkey · TOC lines vs actual packet contents vs divider
  numbers · cover-letter facts, dates, citation and lockbox block · A-numbers ·
  MRZ checksums · the exhibit set recomputed from the four-argument rule ·
  filing-window arithmetic · merged page count == sum of component page counts
  · merged text contains each component's fingerprint line.
- **governed by:** STYLE-SPEC §9.4 (the lock list) and §12 (the fact list).
- Written in Phase 3, run from Phase 3 onward (BUILD-PLAN §4, §6).

### `verify_set.py`
- **in:** all six masterkeys + `../registry.yaml` + the six rendered sets.
- **out:** a set-level report.
- **checks:** leakage — every synthetic proper noun and digit-string grepped
  against `../blocklist.txt` **in both directions**, zero hits · registry
  collisions · coverage matrix (both bases, all conditional exhibits
  exercised, six distinct voices, mess catalogue demonstrated-before-tested).
- **governed by:** STYLE-SPEC §11 — a hit on a string listed there is a
  house-style collision, not leakage, and means `build_blocklist.py`'s
  exclusion set needs extending, not the packet changing.

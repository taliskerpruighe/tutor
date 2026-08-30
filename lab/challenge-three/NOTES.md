# Challenge Three — Corpus Notes

This is the working note for the challenge-three accounting materials: three
invented New York small businesses, each generated deterministically from
its own ledger per `lab/challenge-three/SPEC.md`. All three companies
currently pass all nine `validate.py` checks — including check 6 (the
explicit, required-empty unevidenced-entries list) and check 8 (forbidden
derived-summary documents and stray files) — confirmed for this note with
`CHALLENGE3_BASELINE_MANIFEST=<fresh-manifest> python3
lab/challenge-three/validate.py <slug>` against a manifest built fresh for
the tree on disk. This note describes the corpus as it stands after
remediation — do not trust figures from an older copy of this file, they
have moved.

## The three companies

**Ferrone Provisions LLC** (`ferrone-provisions-llc`) is a New York limited
liability company at 4102 3rd Avenue, Sunset Park, Brooklyn. It is a
specialty Italian food importer and wholesaler selling to restaurants and
small grocers, with a minority of taxable direct sales. Two members —
Antonio and Lucia Ferrone — and four employees. Its period is the full
calendar year, 1 January – 31 December 2025. This is "the trader with
stock": inventory, cost of goods sold, supplier payables, two physical
stock counts (opening and closing), and NY sales tax collected on the
taxable slice of sales and remitted quarterly on the state's own filing
calendar (not calendar quarters). The shipped tree is foldered by kind and
month — `bank/operating/`, `bank/payroll/`, `invoices-out/YYYY-MM/`,
`bills-in/YYYY-MM/`, `receipts/`, `payroll/`, `inventory/`, `opening/` —
the tidy client.

**Halloran & Vance Design Partners** (`halloran-vance-design`) is a New
York general partnership in the Flatiron District, an interior
architecture consultancy with two partners (Margaret Halloran, Owen Vance),
one salaried employee, and several subcontractors of varying regularity.
Its books run on a fiscal year ending 30 June: the period is 1 July 2024 –
30 June 2025, but the shipped documents deliberately run through August
2025 as a trailing stub — two more months of ordinary, bank-reconciled,
fully evidenced activity that sits outside the period and is excluded from
every figure below. This is the service business with no stock and no
fixed assets. It ships as roughly 29 dated email batches
(`NNNNNN_YYYY-MM-DD_slug/`), each a `body.txt` plus its attachments, with
nothing foldered by document kind — the email client.

**Bright Harbor Fabrication Inc.** (`bright-harbor-fabrication`) is a New
York business corporation with an S election, in Long Island City, Queens,
doing architectural metal fabrication. One officer-shareholder (Peter
Vasquez, paid as a W-2 employee — the standard S-corp pattern) plus a
minority shareholder, and six employees. Period 1 January – 31 December
2025. This is "the one with a loan": an equipment term loan drawn in Q2
2025 to buy a CNC press brake, an older vehicle loan running off to zero
during the year, a business credit card, and fixed assets with accumulated
depreciation. It ships as a flat directory with no subdirectories at all,
human-chosen filenames (`bank apr.pdf`, `IMG_4406.jpg`, `Statement (5).pdf`,
`Copy of card statement.pdf`), several PDFs that bundle multiple unrelated
documents into one scanned pass, and one statement (August) deliberately
split across two files — the shoebox.

## Headline figures (from the current answer keys)

| | Ferrone | Halloran & Vance (FY, excl. stub) | Bright Harbor |
|---|---:|---:|---:|
| Revenue | $1,705,000.00 | $714,000.00 | $1,105,058.67 |
| Net income | $152,331.22 | $203,924.54 | $117,669.01 |
| Total assets | $720,336.72 | $289,942.54 | $533,366.97 |
| Closing cash | $98,420.72 operating + $30,000.00 payroll | $154,942.54 | $14,228.09 |

Each of these ties, in its own answer key, to `validate.py` check 7's
identity (assets = liabilities + equity + income − expense) as of the
company's own period end.

## File count and bytes

Verified directly against the shipped tree, not copied from any answer
key:

| | Files | Bytes | Budget (SPEC §2) |
|---|---:|---:|---|
| Ferrone | 102 | 2,781,351 (2.65 MB) | ≤110 files, ≤12 MB |
| Halloran & Vance | 105 | 4,458,100 (4.25 MB) | ≤110 files, ≤10 MB |
| Bright Harbor | 128 | 9,309,485 (8.88 MB) | ≤130 files, ≤16 MB |
| **Total** | **335** | **16,548,936 (15.8 MB)** | **250–400 files, ≤40 MB** |

All three companies and the corpus as a whole sit comfortably inside
budget. The growth since the last pass (Bright Harbor gained one file,
everyone's bytes rose) is the receipt-photograph upscale to a 1900px
minimum width (see "OCR verification" below) and is expected, not a
regression: no single rasterised page exceeds the 500 KB per-page cap
(checked directly against every JPEG/PNG in all three trees and every
image embedded in every shipped PDF; the largest photographed receipt
lands around 150 KB).

## Mandated defects and where each lives

All ten items from SPEC §6 are recorded, with correct treatment, in each
company's own `answer-key.md` (its own §6). Quick index of current
figures:

1. **Duplicate receipt, same purchase shipped twice.** Ferrone: Molino
   d'Oro Pasta Imports LLC delivery, $39,279.00, both a text-PDF bill
   (`bills-in/2025-02/FP-4007.pdf`, the one actually cited by the ledger)
   and a photographed packing slip (`receipts/receipt-molino-doro-delivery.jpg`,
   registered but never cited). Halloran & Vance: Tribeca Paper & Print Co,
   $215.00. Bright Harbor: Gotham Fastener & Hardware, $118.40, as
   `receipt_001.jpeg` plus `Scanned Documents 3.pdf` — the collision that
   used to put this PDF half at the already-taken path `scan0021.pdf` is
   fixed; see "Corrections made during the build."
2. **Personal expense misfiled as business / owner draw.** Ferrone: A.
   Ferrone's JetAzzurro Airlines flight, $1,850.00, to Member
   Distributions. Halloran & Vance: M. Halloran's Atlantic Crest Airlines
   flight, $612.00, to Partner Draws. Bright Harbor: a Skyline Atlantic
   Airways flight, $2,800.00, charged to the business credit card, to
   Shareholder Distributions.
3. **Inter-account transfers.** Ferrone only: twelve monthly
   operating→payroll transfers, no income or expense leg on either side.
4. **≥4 unpaid AR / ≥4 unpaid AP at period end, all three companies.**
   Ferrone: 4 invoices / 4 bills, $495,325.00 / $208,393.00. Halloran &
   Vance: 5 clients / 8 vendors (12 individual bills), $135,000.00 /
   $58,750.00. Bright Harbor: 5 invoices / 5 bills, enumerated by number in
   its answer key §6.
5. **Cancelled invoice via credit note.** Ferrone only: INV-1025 to Ponte
   Vecchio Ristorante, fully reversed by CN-2025, net zero effect on 2025
   revenue, COGS and AR.
6. **Inconsistent date formats**, confined to `documents.jsonl`'s
   `issued_date` and the rendered documents themselves — all three
   companies rotate through US, ISO and prose date styles on their source
   documents while `ledger.jsonl`, `statements.jsonl` and
   `opening_position.json` stay ISO throughout, no exceptions.
7. **Handwritten-looking cash receipt**, one per company: Ferrone $52.00
   (toll/parking reimbursement), Halloran & Vance $84.00 (Chelsea Hardware &
   Supply), Bright Harbor $40.00 (shop rags, petty cash).
8. **Credit card statements for the full year.** Bright Harbor only: twelve
   monthly statements for the Steinway Savings Bank Business Visa, its own
   liability account (2300), paid down from the operating account the
   following month.
9. **Loan interest/principal split.** Bright Harbor only: the older vehicle
   loan (fully retired during 2025) and the new equipment term loan drawn
   April 2025 against the press brake, each monthly payment split across
   interest expense, principal reduction and cash.
10. **CSV bank export duplicating six months already on the PDF
    statements.** Ferrone only: `operating-export-2025-01-to-06.csv`
    mirrors January–June, registered but never cited by the ledger.

## How to regenerate

Each company's `generate.py` is deterministic — same seed, same output tree,
every time. Run:

```
python3 lab/challenge-three/<slug>/generate.py
```

from within `lab/challenge-three/<slug>/`, or with `lab/challenge-three` on
`sys.path`. This rewrites that company's four `.jsonl`/`.json` data files
plus its shipped tree under
`content/21-challenges/materials/challenge-three/<slug>/`. Then verify:

```
CHALLENGE3_BASELINE_MANIFEST=<baseline-manifest> python3 lab/challenge-three/validate.py <slug>
```

The baseline manifest is a plain `path<TAB>size` listing of the whole repo
tree, excluding the two challenge-three trees
(`content/21-challenges/materials/challenge-three` and
`lab/challenge-three` themselves), that check 8 diffs the live tree against
to catch stray files leaking in anywhere else in the repo. It is a snapshot
of a point in time, not a fixture: **build it fresh against the tree you
are about to validate**, don't reuse an old one. In particular, a manifest
captured with `.git` or `.dvc` pruned out will not match a live repo tree
that still has `.git`/`.dvc` present, and check 8 will report every one of
those paths as a spurious "new file outside permitted trees" — a tooling
mismatch, not a corpus defect, but confusing enough to chase by hand if you
don't know to expect it. Regenerate the manifest for the tree you actually
have on disk right before you validate.

## What the validator checks, and why check 6 matters

`validate.py` runs nine checks per company: (1) every bank statement line
matches a ledger entry and vice versa; (2) each statement's own arithmetic
is internally consistent; (3) each account's closing balance equals the
next period's opening balance with no gaps; (4) inter-account transfers are
recognised symmetrically on both sides with no phantom income or expense;
(5) every non-cash ledger entry is evidenced by a specific shipped
document; (6) the explicit, and required-empty, list of ledger entries that
fail that evidence test; (7) the accounting identity — assets equal
liabilities plus equity plus income minus expense — as of period end, plus
every entry balancing debit to credit; (8) no forbidden derived-summary
document (a balance sheet, P&L, trial balance, tax return, etc.) shipped
into the materials tree, and no stray file outside the two permitted
challenge-three trees; (9) the opening letter's stated cash balances tie to
the first in-period statement.

Check 6 is the one worth calling out specifically: it's not a
sanity-check add-on, it is the actual pass condition for document coverage.
Check 7's "assets = liabilities + equity" identity is trivially true of
*any* double-entry ledger that balances its own debits and credits — it
proves the arithmetic is self-consistent, not that any of it is backed by a
real document a reader could go find. A ledger can be perfectly balanced
and entirely fabricated. Check 6's explicitly-empty list is what actually
says every line in the ledger traces to something a reader can open and
read. (This is also exactly the distinction that let the sign bug described
below hide for as long as it did — see "Corrections made during the
build.")

## Known deviations and limitations

- **Bright Harbor's scans render at 150 DPI / JPEG quality 60**, not the
  SPEC's nominal 200/75 (`scanify()`, unchanged by the receipt-resolution
  fix below). See "OCR verification" below: every scanned and rasterised
  class still yields date, counterparty and total under `tesseract --psm
  6`, so the lower setting remains an accepted deviation — legibility was
  the point of the DPI figure, and legibility holds.
- **`validate.py`'s `line_evidenced()` is an existence check, not a content
  check.** It confirms a ledger line's `doc_ids` resolve to a
  `documents.jsonl` row whose file exists on disk at the stated path — it
  does not open that file and confirm it actually states the claimed
  amount, date or counterparty. This is a known, accepted hole; the
  human-level determinacy review (reading the documents, not just checking
  they exist) is what covers it. It is also exactly the gap that let the
  now-fixed `scan0021.pdf` filename collision go undetected by every
  automated check for as long as it did — see "Corrections made during the
  build."
- **`Copy of payroll.xlsx` in Bright Harbor varies by a few bytes between
  regenerations.** `openpyxl` embeds a creation timestamp in the XLSX
  container; this is otherwise-deterministic generation leaking one
  non-reproducible field. The PDF and JPEG render paths embed their own
  timestamps too, so byte-for-byte identity across regenerations was never
  a goal for any of the rendered-document formats — only the `.jsonl`/
  `.json` data files and the accounting figures they produce are meant to
  be exactly reproducible from a seed.
- **Ferrone's mandated-defect-5 figures ($4,464.00 COGS/inventory reversal,
  $3,200.00 shrinkage) are now independently reachable from shipped source
  documents alone** (the credit note's own returned-goods table priced off
  either stock count's own unit-cost column; the closing stock count's own
  book-vs-counted variance column) — this was a gap in an earlier pass and
  is now closed, per Ferrone's answer key §10.1. The annual COGS total
  ($1,230,800.00) was always independently reachable via the periodic
  formula regardless.
- Bright Harbor's utilities, telephone, vehicle expense, bank fees and
  professional fees now vary month to month (see "Corrections made during
  the build") rather than repeating flat constants; this closed a realism
  gap flagged in an earlier pass.

### OCR verification

The photographed-receipt gap this section used to document (a scatter of
misread totals, a dropped counterparty line, a garbled date, on a fraction
of samples) has been diagnosed to its root cause and fixed, not just
patched around. The flat receipt renders that `photograph_receipt()`
photographs were about 660×810 px, which `tesseract` reads as roughly 109
DPI — well below the resolution at which it resolves closed digit counters
reliably. It was a pixel-size problem, not a distortion problem, which is
why the first two remediation attempts (softening the perspective warp,
then separately softening the blur and raising JPEG quality) did not
touch it: both addressed distortion, and the problem was resolution.

`lib/render.py`'s `photograph_receipt()` now, in this order: upscales any
source render narrower than 1900 px with Lanczos before any warp, rotation
or lighting is applied (a real phone photograph of a receipt is thousands
of pixels wide, so this is also the more faithful rendering, and it is
done once in the shared library so all three companies get it from one
place); applies the already-softened distortion (perspective jitter 1.5%,
rotation ±2°, blur radius 0.4); and saves at the highest JPEG quality that
still fits the 500 KB per-page raster cap, stepping down through 88 / 82 /
76 / 70 / 64 (in practice the first step, 88, is taken, at roughly 150 KB
per receipt — confirmed above, no photographed receipt in the corpus comes
close to the cap).

This was re-verified directly for this note: every photographed receipt
in all three companies (27 JPEG/JPG files total across Ferrone, Halloran &
Vance and Bright Harbor — a full sweep, not a sample) was run through
`tesseract --psm 6` unaided. **26 of 27 recover counterparty and total
cleanly.** The single exception is `chelsea_hardware_receipt.jpg`
(Halloran & Vance), one of the three deliberately handwritten cash
receipts, which are excused from a clean-OCR bar by design and were
confirmed legible by eye against their ledger figures. Both previously-named
regressions now read exactly right: Bright Harbor's `IMG_4409.jpg` gives
"Astoria Hardware De pot / Date: 08/25/2025 / Total $96.10" and Ferrone's
`receipt-molino-doro-delivery.jpg` gives "Molino d'Oro Pasta Imports LLC /
Date: 11 Feb 2025 / Amount $39,279.00" — both fields that used to misread.

The open question this section used to pose — whether the corpus needs to
survive unattended bulk OCR, or only a reader who opens and reads each
document — is now moot for the photographed-receipt class: it survives
unattended OCR. There is no remaining equivocation to report here.

The scanned-PDF classes are unaffected by this fix (`scanify()` was not
touched) and were re-checked, unchanged in behaviour from before:

- **Scanned bank statements (single-file and the two-file August split),
  scanned vendor bills, scanned multi-document bundles (`march bills.pdf`,
  `Scanned Documents.pdf`, `Scanned Documents 3.pdf`, `scan0040.pdf`), and
  the press brake invoice image** all yield date, counterparty and total
  cleanly and completely from `tesseract --psm 6` at the shipped 150 DPI /
  quality 60 setting.
- **The three annual-bill bundles** (`utility bills 2025.pdf`,
  `phone bills 2025.pdf`, `Corrado invoices 2025.pdf`) are registered
  `"scanned": false` in `documents.jsonl`, and this is correct, not a
  metadata bug: `pdfimages -list` finds no embedded raster images in any of
  them and `pdftotext` extracts a clean, complete text layer directly —
  they are ordinary text-native, twelve-page PDFs that happen to bundle a
  full year of one vendor's bills into one file, not scans at all. A
  reader doesn't need OCR for these; plain text extraction already works.

No class is illegible at `--psm 6` — nothing here makes the challenge
impossible, and, unlike the previous pass, there is no longer a
qualification to attach to the photographed-receipt class either.

## Corrections made during the build

These are worth recording because they are the non-obvious traps a future
pass could reintroduce:

- **A sign bug in `lib/ledger.py`'s `balance_sheet_totals()`** summed
  contra-equity accounts (member/partner distributions and draws) and
  accumulated depreciation into equity and assets in their raw
  debit-positive form, instead of netting them against their type's
  canonical direction. Because check 7's identity is `assets = liabilities
  + equity + income − expense`, inflating both assets and equity by the
  same contra balances let the identity pass by coincidence on a ledger
  that did not actually balance correctly — the kind of bug that a
  balance-the-books check alone cannot catch itself, which is exactly why
  check 6's document-evidence list matters independently (see above). Now
  fixed: the function sums each account by its type's canonical direction
  (assets/expenses debit-positive, liabilities/equity/income
  credit-positive), which correctly subtracts contra balances.
- **One company's expense model of perfectly recurring flat constants had
  to be rebuilt.** Bright Harbor's utilities, telephone & internet, vehicle
  expense, bank fees and professional fees each repeated one flat monthly
  figure for all twelve months of 2025 — implausible for inherently
  usage-based costs, and especially so once the press brake landed in Q2
  and should have visibly raised the shop's electricity draw. `generate.py`
  was edited to give each of the five accounts realistic month-to-month
  variation (seasonal load, occasional overage, lumpy professional-fee
  timing around real accounting events), and the whole corpus was
  regenerated from the edited generator — nothing was hand-patched into a
  rendered document or the ledger directly.
- **Unevidenced year-end closing journal entries were removed.** An earlier
  pass posted current-period net income (and/or distributions) into
  capital via a closing entry with no source document behind it. All three
  companies now leave current-period net income, and each partner's/
  member's/shareholder's distributions or draws, as open balances at
  period end — exactly as a pre-closing, ledger-derived balance sheet
  would show them — rather than manufacturing an unevidenced entry to tidy
  the presentation.
- **Four real-world entity names had leaked into the corpus and were
  replaced**: a real TriBeCa restaurant name, a real airline name, the
  real Decoration & Design Building, and a real brokerage name were all
  found and swapped for invented equivalents, plus a utility name
  ("Consolidated Utility Co") that was judged too close to Consolidated
  Edison, the real New York utility, and was renamed to Harborline Utility
  Co throughout Bright Harbor's corpus (`documents.jsonl`, the ledger, the
  rendered `utility bills 2025.pdf` bundle, and the answer key). Halloran &
  Vance's personal-flight defect (§3, mandated defect 2) now names the
  airline "Atlantic Crest Airlines" and Ferrone's names "JetAzzurro
  Airlines" — both invented.
- **The `scan0021.pdf` filename collision in Bright Harbor is fixed.**
  `documents.jsonl` used to have two rows pointing at the same path
  `scan0021.pdf` — the July bank statement and the scanned-PDF half of
  mandated defect 1 (the Gotham Fastener & Hardware $118.40 duplicate
  receipt) — because the July statement's own `generate.py` filename table
  collided with a separately hardcoded path for the duplicate-receipt
  document. Only the bank statement actually existed at that path, so
  defect 1's PDF half was never really instantiated and the trap could
  never fire. The duplicate receipt's PDF half now ships at its own,
  non-colliding path, `Scanned Documents 3.pdf`; `scan0021.pdf` is once
  again only the July bank statement. `documents.jsonl` now has zero
  duplicate paths across all three companies, and Bright Harbor's
  `register_doc()` now asserts path uniqueness on every call (`assert
  path_rel not in _doc_paths`), so this class of collision fails loudly at
  generation time instead of silently shipping a document that isn't what
  it claims to be.
- **The photographed-receipt OCR gap was diagnosed to a root cause and
  fixed, not patched around.** An earlier pass's fixes (softening the
  perspective warp, then separately softening the blur and raising JPEG
  quality) had not closed the gap because both addressed distortion, and
  the actual cause was resolution: the flat receipt renders `photograph_
  receipt()` worked from were about 660×810 px, which `tesseract` reads as
  roughly 109 DPI, well below where it reliably resolves closed digit
  counters. `lib/render.py` now upscales any source render narrower than
  1900 px with Lanczos before warp/rotation/lighting are applied. The
  lesson worth keeping: "the scans are legible" has to be measured across
  the whole class, not sampled — the fraction that failed was small enough
  that a sample could easily have missed it, which is exactly what let the
  first two, distortion-focused fixes look sufficient when they weren't.

## A note on what is deliberately not here

There is no README under
`content/21-challenges/materials/challenge-three/`, and none should be
added. Challenge one has no README either; the framing these companies
need belongs in a course article nobody has written yet, and a README
under the shipped materials tree is a second copy of this information that
someone would then have to keep in sync with it. This file, under `lab/`,
is the one corpus note, and `lab/` is stripped out before a reader ever
sees the tree.

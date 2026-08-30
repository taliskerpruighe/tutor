# Challenge Two — Build Scaffold

This folder builds the "challenge two" teaching corpus: nine fictional
noncompete agreements plus three fictional law-firm intake emails, used as
exercise material for the course. **Every person, company, address, email
domain, and document referenced anywhere in this corpus is invented for a
teaching exercise. None of it is legal advice, and none of it is a usable
contract or email template.** Do not copy any clause out of this corpus
into a real document.

This `lab/challenge-two/` folder does not ship — `install.sh` strips `lab/`
from any copy a reader downloads. It exists only to build
`content/21-challenges/materials/challenge-two/`, which does ship.

## Layout

```
lab/challenge-two/
  README.md                       -- this file
  build.sh                        -- renders sources into the shipped corpus
  render_pdf.py                   -- reportlab-pdf producer used by build.sh
  sources/
    shared-provisions.md          -- clause library authoring workers paste from
    manifest.tsv                  -- one row per contract: file names, producer,
                                      state, ancillary set, style/variant choices
    contracts/                    -- authoring workers write their .md/.txt
                                      source files here (empty until authored)
    to-do/                        -- authoring workers write intake-email
                                      .txt sources here (empty until authored)
  ANSWER-KEY.md                   -- skeleton answer key (no data yet)

content/21-challenges/materials/challenge-two/
  contracts/                      -- build output: exactly 9 rendered files
  to-do/                          -- build output: intake email .txt files
```

## How to rebuild

```
bash lab/challenge-two/build.sh
```

The script is idempotent and safe to re-run — it overwrites its own
outputs. It reads `sources/manifest.tsv`, renders each of the nine
contract sources through the producer named in that row (`pandoc-docx`,
`reportlab-pdf`, `soffice-pdf`, or `copy-txt`) into
`content/21-challenges/materials/challenge-two/contracts/`, and copies any
`.txt` files in `sources/to-do/` into
`content/21-challenges/materials/challenge-two/to-do/`.

It can be run at any point during authoring: any contract whose source
file does not yet exist under `sources/contracts/` is skipped with a clear
message, and the script still exits 0.

Two of the nine contracts (rows 4 and 7 in the manifest, producer
`soffice-pdf`) go through an intermediate docx (via `pandoc`) before
`soffice` converts that docx to PDF. That intermediate docx is written to
a private temp directory and is deleted at the end of the run — it never
lands in `contracts/`, which must contain exactly nine files once all
nine sources exist. Every `soffice` invocation in `build.sh` uses an
isolated user profile (`-env:UserInstallation=file:///tmp/lo-challenge-two`)
and `build.sh` runs its `soffice` calls one at a time, never in parallel,
because a concurrent job elsewhere in this repository also invokes
`soffice` and shares the same machine.

## `sources/shared-provisions.md`

This is the clause library the three authoring workers draft the nine
contracts from. Every recurring provision type (confidentiality,
customer non-solicitation in three styles, governing law in three
states, severability in three forms, employee no-hire, injunctive
relief, tolling, integration, at-will, return of property, assignment of
inventions, and a set of ancillary provisions) has full-length clause
text there, ready to paste verbatim. It ends with a **DO NOT WRITE**
section naming the two provision types (supplier/vendor non-solicitation,
and training-cost repayment/clawback) that must never appear anywhere in
the corpus, in any phrasing — these are deliberate gaps the exercise
depends on.

## `sources/manifest.tsv`

One row per contract (9 data rows). Columns, in order:

`n`, `source_file`, `output_filename`, `producer`, `state`,
`ancillary_provisions` — the six required columns — followed by columns
carrying the fixed facts from the build plan (`employer`, `employee_name`,
`role`, `industry`, `term`, `geography`, `posture`) so that authoring
workers have a single character-sensitive source for names like "Alina
Fenwick, M.D." and "Halvorsen Medical Systems Inc.", and finally four more
columns load-bearing for distinctness and for keeping the three blind
authoring workers from converging on the same phrasing:
`customer_nonsolicit_style`, `confidentiality_variant`,
`severability_form`, plus a free-text `special_core_flags` column, and
finally `employee_no_hire` — added after the fact to reconcile this
manifest with the as-built documents (see "Supersession note" below);
it is the sole record of employee no-hire treatment, replacing an
earlier `employee_nonsolicit` column that disagreed with it on
contracts 1 and 6 and has been removed.

`output_filename` values are reproduced character-for-character from the
fixed table in the build plan — verified programmatically (see
"How distinctness was verified" below).

### Ancillary provisions per contract, and why they don't collide

| n | state | customer non-solicit | confidentiality | severability | employee no-hire | ancillary set |
|---|---|---|---|---|---|---|
| 1 | NY | Style A | canonical | bare, no reformation | omitted | return of Company property, assignment of inventions, injunctive relief, integration |
| 2 | NY | Style B | variant 1 | bare, no reformation | canonical (5a) | return of Company property, non-disparagement, tolling, injunctive relief, attorneys' fees, integration |
| 3 | NY | none (arbitration) | variant 2 | bare, no reformation | omitted | return of Company property, at-will disclaimer, notice |
| 4 | CT | Style C (patient) | canonical | bare, no reformation | omitted | return of Company property, injunctive relief, survival |
| 5 | CT | Style B | variant 2 | CT express-reformation | variant (5b) | return of Company property, non-disparagement, injunctive relief, attorneys' fees, assignment/successors |
| 6 | CT | none (bare severability, no reform) | variant 1 | bare, no reformation | omitted | assignment of inventions, tolling, injunctive relief, forum selection |
| 7 | NJ | none (garden leave) | canonical | NJ reformation | canonical (5a) | return of Company property, non-disparagement, attorneys' fees, assignment/successors, jury waiver |
| 8 | NJ | Style B | variant 1 | NJ reformation | variant (5b) | assignment of inventions, tolling, injunctive relief, integration, forum selection |
| 9 | NJ | Style A | variant 2 | NJ reformation | omitted | return of Company property, at-will disclaimer, survival |

Confidentiality variants are spread evenly across the corpus so each
authoring worker (drafting three contracts each, split 1–3 / 4–6 / 7–9)
uses each of the three variants exactly once: canonical → {1, 4, 7},
variant 1 → {2, 6, 8}, variant 2 → {3, 5, 9}.

Employee no-hire was likewise pinned per contract rather than left open,
for the same reason as severability below: it's a library entry that
isn't fixed by the build plan and isn't in the ancillary pool, so leaving
it to each blind worker's discretion would have meant guessing both
inclusion and phrasing independently. It's assigned canonical (5a) →
{2, 7}, variant (5b) → {5, 8}, omitted → {1, 3, 4, 6, 9}.

**Supersession note:** this assignment previously read canonical (5a) →
{1, 2, 7}, variant (5b) → {5, 6, 8}, omitted → {3, 4, 9} — a clean 3/3/3
spread across the corpus. That is not what was built: contracts 1 and 6
were both authored with no employee no-hire clause at all. The record
above has been corrected to match the as-built documents (the documents
themselves were not changed), and pairwise distinctness across all nine
contracts was re-verified after the correction — see "How distinctness
was verified" below. The spread is no longer a clean 3/3/3; it is 2
canonical, 2 variant, and 5 omitted.

Severability form was not left to each authoring worker's discretion, even
though the build plan only pinned it for contracts 5 and 6. Leaving it
open would have meant three blind workers independently guessing which of
the three forms to use for the other seven contracts, risking accidental
convergence. It was assigned as: bare severability, no reformation power →
{1, 2, 3, 4, 6}; Connecticut express-reformation → {5} (as specified);
New Jersey reformation, paired with legitimate-business-interest framing
→ {7, 8, 9} (all three New Jersey contracts, consistent with New Jersey's
own reformation doctrine). Contract 6's severability clause uses the bare
severability text as-is (clause 4c in `shared-provisions.md`), which says
nothing about narrowing an unenforceable provision — per the build plan,
this must remain silent on reformation, not add an explicit statement
that reformation is unavailable.

### How distinctness was verified

Each contract's full provision-type set was built as the union of: the
core provisions every contract carries (confidentiality, governing law,
severability), the core provisions fixed by the build plan (customer
non-solicit style or its absence, arbitration, garden leave, the
termination-without-cause carve-out, the severability form), its assigned
employee no-hire treatment, and its assigned ancillary set. This was
computed three times with a short Python script (not checked in —
throwaway verification): once including a positive "no customer
non-solicit" marker for contracts 3, 6, and 7; once using only provisions
that are actually present (dropping that marker, since a later automated
check is more likely to compute the union of provisions *present* than to
track absences); and once more after the employee no-hire assignment was
added, to confirm that addition didn't accidentally collapse two
contracts onto the same set. All three computations came back pairwise
distinct across all nine contracts — no two contracts share an identical
combined provision-type set. Ancillary-set sizes range from 3 to 6
provisions per contract, satisfying the "vary the counts" requirement.

The two contracts most at risk of collision — 2 and 8, both broad,
New York/New Jersey, Style B customer non-solicit, `pandoc-docx` producer,
described as "well-drafted" — were deliberately given disjoint ancillary
sets (2 has return of Company property, non-disparagement, and attorneys'
fees, which 8 lacks; 8 has assignment of inventions and forum selection,
which 2 lacks) and different counts (6 vs. 5).

## `render_pdf.py`

The `reportlab-pdf` producer. Renders a minimal Markdown dialect (H1
title, ALL-CAPS headings, paragraphs, and a `<!-- signature-block -->`
marker for the signature block) to PDF using Helvetica at 10.5pt/15.5pt
leading with asymmetric 1.35in/0.95in margins — deliberately different
from LibreOffice's default export (a serif face at ~12pt with ~1in
margins), so that a later check can tell `reportlab-pdf` output apart
from `soffice-pdf` output by inspecting the text layer's font metadata
(confirmed in the smoke test below: reportlab output uses
`Helvetica`/`Helvetica-Bold`; LibreOffice's default export used
`NotoSerif-Regular` on this machine — the two font sets are always
disjoint). Output always contains a real, selectable text layer, never a
rasterized image.

## Smoke test result

Before this scaffold was reported done, one throwaway Markdown source was
pushed through all four producers (into `/tmp`, never into the real
`content/` output paths) and every output was verified to open and
extract non-empty text:

- `pandoc-docx` — produced a valid `.docx`; `python-docx` extracted 500
  non-empty characters.
- `reportlab-pdf` — produced a valid PDF with a real text layer;
  `PyMuPDF` (`fitz`) extracted 500 non-empty characters.
- `soffice-pdf` — markdown → docx (pandoc) → PDF (soffice, isolated
  profile at `/tmp/lo-challenge-two`, single serial call); `fitz`
  extracted 503 non-empty characters.
- `copy-txt` — plain copy; verified the copy was byte-identical to the
  source and non-empty (27 bytes in, 27 bytes out).

The reportlab/soffice font discriminator was checked directly: the two
PDFs' font-name sets were confirmed disjoint
(`{Helvetica, Helvetica-Bold}` vs. `{NotoSerif-Regular}`), and their first
text span's left margin differed as designed (~171pt / 1.35in for
reportlab vs. ~72pt / 1in for soffice's default).

All throwaway outputs, the throwaway temp directories, and the isolated
LibreOffice profile directory were deleted afterward. `content/21-challenges/materials/challenge-two/contracts/`
and `content/21-challenges/materials/challenge-two/to-do/` were confirmed
empty (`ls -la`, no entries besides `.` and `..`) as the last action of
the build step.

## Intake email filenames

The three fictional law-firm intake emails go under `sources/to-do/` as
plain `.txt` files, named `001-<short-slug>.txt`, `002-<short-slug>.txt`,
and `003-<short-slug>.txt`, in that numeric order. `build.sh` copies
whatever `.txt` files it finds there into
`content/21-challenges/materials/challenge-two/to-do/` unchanged. This
numbering is what `ANSWER-KEY.md` Table 1 means by "email 002" — it's the
email authored as `002-*.txt`, not necessarily the second email
chronologically within its own narrative.

## `ANSWER-KEY.md`

A skeleton only — three empty tables (one per email, one per contract,
one provision matrix), each with expected-vs-rendered columns for a later
step to fill in once all twelve documents exist. No data is recorded yet.

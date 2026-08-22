# SPEC-DELTA — Phase 2..6 reconciliation of the Phase-1 artefacts to STYLE-SPEC §16

Written at the head of the Phase 2–6 run. STYLE-SPEC §16 is the user's binding
ruling set and it postdates every other Phase-1 artefact on disk. The templates
and `tools/README.md` were written against §14 and therefore encoded overturned
law. A subagent handed those files would have implemented dead rules faithfully.
They are patched in place; this file is the ledger.

## A. Patched to §16

| file | was | now | authority |
|---|---|---|---|
| `templates/divider.yaml` | `size_pt: 24` | `size_pt: 12` | §16 r3 |
| `templates/divider.yaml` | `green_card: GREEN CARD` | `PERMANENT RESIDENT CARD` | §16 r4 |
| `templates/divider.yaml` | `auto_policy: JOINT AUTOMOBILE POLICY` | `JOINT AUTOMOBILE INSURANCE POLICY` | §16 r4 precedent, decision D-A below |
| `templates/cover-page.yaml` | `A: SUMMARIES, B: BIOGRAPHICAL` | `A: SUMMARY, B: BIOGRAPHICAL INFORMATION` | §16 r2 |
| `templates/cover-letter.docx.yaml` | signature block `{FIRM_NAME}` / `By: {PREPARER_NAME}` / `Petition Preparer` | `Petition Preparer` alone; both slots deleted | §16 r7 |
| `tools/README.md` | `render_n400.py` fills Parts 11 **and 13**, renders Z003 signature | Part 11 only; Part 13 blank; unsigned; Z003 unused | §16 r10, r11 |
| `tools/README.md` | `build_blocklist.py` rerun instructions | DO NOT RERUN (OCR forbidden this run) | run order |

**Explicitly NOT changed:** tab cover pages stay at **24 pt**. §16 r3 lowers the
*dividers*; its own consequences note says so ("changes divider geometry").
Harmonising the tab covers down would be an unforced error.

## B. Decisions taken without asking

**D-A — the auto-policy title gains `INSURANCE`.** §4.3 set the divider
`JOINT AUTOMOBILE POLICY` while §4.4 set the TOC line `Joint automobile
insurance policy`. §16 "Still open" item 1 asks whether the invented
spousal-cluster titles read right and records that ruling 4 set a precedent —
the user preferred the formal name (`PERMANENT RESIDENT CARD`) over the
colloquial one (`GREEN CARD`). Applying that precedent: the divider takes the
fuller, formal string, the two strings stop disagreeing, and the component file
name follows. The other four invented titles (`SPOUSE'S PASSPORT`,
`FORM I-797C, NOTICE OF ACTION`, `JOINT DEED`, `CHILD'S PASSPORT`) were already
the formal form of their document and stand unchanged.

**D-B — the signature block keeps the role line.** §16 r7 forbids any firm or
preparer identity. It does not forbid the unattributed role, and STYLE-SPEC §11
lists both `Sincerely,` and `Petition Preparer` as strings the house style
requires every packet to contain. The block therefore closes:
`Sincerely,` · blank · blank · `Petition Preparer`. No name, no firm, no `By:`.

**D-C — `document-catalog.yaml` is the single join table.** Each document's file
name (§2.1), divider title (§4.3) and TOC line (§4.4) lived in three separate
prose tables. Renderers and `verify_client.py` now read one YAML instead of
three sections, so §4.4's TOC/divider/count lock cannot drift by transcription.

**D-D — `ships_as` rule confirmed** (§15.5, open): `authored_by: firm` ships
docx + pdf; forms and exhibits ship pdf only. This is the reading the run order
directs and it is now machine-readable in the catalog.

**D-E — the Part 13 assertion needs a positive control.** §13 D1 records that
the N-400 parts were renumbered between the 04/01/24 and 01/20/25 editions. A
verifier asserting "the Part 13 fields are empty" against field names that do
not exist on the committed blank passes vacuously while a filled preparer block
ships. `verify_client.py` must first PROVE the Part 11, Part 13 and signature
field names exist in the blank's 488-name dump, then assert Part 13 and the
signature fields are empty and Part 11 is populated.

**D-F — the leakage scan matches whole tokens, and §11 hits are not a halt.**
`blocklist.txt` carries 12,454 tokens including bare digit strings (`000000`,
`01212`, `02365`, `026300`). A naive substring grep over "every synthetic
digit-string" would hit on ZIPs, AGIs and dates and trip the run's halt
condition on noise. `verify_set.py` therefore matches on whole tokens with a
minimum length, and honours STYLE-SPEC §11's own rule: a hit on a §11-listed
house-style string is an exclusion-set bug to be recorded, not a halt. The halt
is reserved for a hit on a real corpus proper noun or identifier.

**D-G — `blocklist.txt` is consumed as built.** It and `.ocr-cache/` are
committed Phase-1 artefacts. The run order forbids OCR, so the script is not
re-run; the Phase-1 token list is authoritative for this build.

**D-H — SUPERSEDED BY D-H2. Retained for traceability.** D-H claimed the
committed blank has no printed Part 13 and that §16 rulings 10/11 therefore had
to be honoured "semantically" against printed Parts 10 and 12. **That was wrong.**
It identified Parts from the AcroForm `/TU` tooltips, which on this blank are
stale and mislabelled.

**D-H2 — §16 rulings 10 and 11 apply LITERALLY; the printed numbering already
matches.** A Phase 2b masterkey writer challenged D-H from the primary source and
was right. Reading the printed page text with `pdftotext -layout` shows the
committed 01/20/25 blank prints: Part 10 Request for a Fee Reduction · **Part 11
Applicant's Contact Information, Certification, and Signature** · Part 12
Interpreter · **Part 13 Contact Information, Certification, and Signature of the
Person Preparing this Application** · Part 14 Additional Information · Part 15
Signature at Interview · Part 16 Oath of Allegiance. So the user's wording —
"Part 11 ... IS filled", "Part 13 preparer block stays entirely blank" — needs no
reinterpretation at all.

What survives from D-H unchanged, and what it is worth: **the field-name lists.**
They were derived from page position and are correct either way. The AcroForm
prefixes lag the printed Parts by no constant offset (`P10_*` on page 11 is
printed Part 10, but `P12_*`/`P13_*` on that same page are printed Part 11, and
`P15_*` on page 12 is printed Part 13), so **no tool may infer a Part from a
field-name prefix or a `/TU` tooltip.** The positive control still stands and is
still necessary: `verify_client.py` must prove each named field EXISTS in the
488-name dump before asserting it is empty, or the assertion passes vacuously.
Field lists, page mapping and the control: `lab/synthetic/tools/n400-part-map.md`
(corrected 2026-08-22). Supporting dump: `lab/synthetic/tools/n400-field-dump.tsv`.

**Process note worth keeping.** This error was caught because the masterkey
writers were told to read the blank themselves rather than trust the digest. Two
of the run's artefacts now carry a standing instruction to prefer the printed
page over any extracted label.


**D-I — the six masterkeys are normalised to one shape before Phase 3 reads
them.** The six Phase 2b agents wrote correct content in six different shapes:
`exhibits` was a bare list in two and `{list: [...]}` in four (and adeyemi
inverted the field meanings, writing `{doc: <int>, id: <catalog id>}` where
everyone else wrote `{doc: <catalog id>, seq: <int>}`); `travel` appeared as a
list, a `{list:}`, a `{trips:}` and a `{countable_trips:}`; moral-character keys
were `q1` in three and `q_1` in three; `documents.passport` was
`applicant_passport` in one; `tax_return.year` was `tax_year` in three.

`tools/normalize_masterkeys.py` writes `clients/<slug>/masterkey.norm.yaml`, and
**everything from Phase 3 onward reads only the `.norm.yaml`.** The authored file
stays as provenance. This is deliberately a normalise-to-disk step rather than an
import-time shim: with ~10 renderers, two verifiers, six Phase 4 fabricators, six
Phase 5 reviewers and three dogfood solvers still to come, a shim only works if
every one of them remembers to use it, and the failure when one does not is
silent — a missing `on_form` flag reads as `None`, C4 quietly stops firing, the
TOC comes out one line short, and the verifier recomputes from the same raw file
and agrees. Normalising once, loudly, in one place, removes that whole class.

The normaliser also emits `rule_inputs`, a flat block of the booleans STYLE-SPEC
§9's four-argument rule actually consumes (`c1_fires` … `c6_fires`, the arrest
and Part-14 item lists, trip counts, supplied-evidence types). `verify_client.py`
and `validate_masterkeys.py` read those rather than each re-deriving the rule
with their own heuristics — two independent derivations of one rule is how a
verifier ends up agreeing with a renderer's shared mistake.

One real bug this surfaced, and one of my own: `tran_daniel` carries a joint auto
policy in `documents.evidence` with `supplied: false` — a deliberate negative
control, since T1 must exercise C3a and C3c but *not* C3b. The first normaliser
read the evidence *type* alone and fired C3b, which would have shipped an
eleventh document. §9.3 rule 3 is explicit that C3a–C3c are a function of
*supplied* evidence; the flag is now honoured and `evidence_declined` is carried
so the verifier can assert the negative.

**D-J — the leakage scan matches on distinctiveness, and it is poison-tested.**
D-F set the policy; this is the implementation. Grepping every masterkey string
against `blocklist.txt` raw produced 162–535 "hits" per client and not one was
leakage: the list carries ~12,400 tokens harvested from all corpus prose,
including `Allegiance`, `Constitution`, `Company`, `Additional`, `Engineering`,
`Circuit`, `Republic` and `seal`. A scan that red-lights every client on every
run is a scan nobody reads.

Four filters, in order:
1. **Scan only invented-fact paths** — names, addresses, employers, contact
   details, document and case numbers. Not `moral_character.*.text` (that is the
   printed form's own wording), not agent commentary, not `input_surfaces` or
   `consistency_locks` (those are prose about the facts, not the facts).
2. **Excuse house-style vocabulary by construction** — every word occurring in
   the three committed blank forms, in STYLE-SPEC §11, or in
   `templates/document-catalog.yaml`.
3. **Excuse ordinary English** via `/usr/share/dict/words`, after stripping
   possessives and splitting hyphens (which is what finally cleared
   `Self-Prepared`). The discrimination was verified before being trusted: that
   list contains `engineering`, `circuit`, `pharmacy`, `republic`, `district`
   and `seal`, and does **not** contain `Oliveira`, `Izaguirre`, `Zhu` or
   `Symple`.
4. **Force-flag the corpus's own distinctive nouns** regardless of the
   dictionary, because `Malone` is an ordinary dictionary word and would
   otherwise be excused.

Whole field values are additionally matched against the blocklist entire, so a
multi-word address leaks even when each word is innocuous.

**The scan is poison-tested rather than assumed.** Injecting `Oliveira` as a
surname, `SYMPLE` as an employer and `26 Broadway Fl 8` as a street into a
masterkey turns the barrier red on all three and names the exact paths; removing
them returns it to green. A leakage gate that has never been shown to fail on
real leakage is not evidence of anything.

The §11 exclusion set this required is recorded, not hidden, in
`tools/blocklist-exclusions.txt` — `blocklist.txt` itself is not regenerated
because the run order forbids the OCR pass. Two masterkey agents independently
flagged `Self-Prepared`, and the `tran_daniel` agent flagged county and
court-type nouns, noting that T1 is the first client to carry a deed and no
worked pair has one. Both are in the file with their provenance.

**D-K — the tax-year rule in the first validator draft was inverted, and the six
agents were right.** It computed "filed before mid-April → previous year". The
correct reading of §13 D11 is that "latest tax return" means the latest return
that *exists* at the filing date, and TY N is not filed until roughly 15 April of
year N+1. So a packet filed before mid-April of year Y has **TY(Y−2)** as its
latest, and one filed on or after has TY(Y−1). All six masterkeys already had it
right; the validator was corrected to match them.

**D-L — Phase 3 integration findings, fixed at the source rather than worked
around.** Four defects surfaced only when independently-built renderers ran
against real masterkeys. Recorded because each was found by a downstream
consumer challenging an upstream artefact, which is the property worth keeping.

1. **`mklib.stamp_deterministic` crashed on pypdf 6.14.2** — `w._ID` was assigned
   a plain list where `_write_trailer` requires an `ArrayObject`, and because the
   assignment itself raised nothing the surrounding `try/except` never fired; the
   failure surfaced later at `w.write()`. Two renderers hit it independently and
   both reported rather than patched (they were scoped to one file each). The
   toolsmith fixed it; the workarounds have been unwound so every component
   carries the house `/CreationDate` and `/Producer`.
2. **`rule_inputs.trips_day_excluded` was wrong on two clients.** The first
   implementation substring-matched `"day trip"` in each trip's `why_excluded`,
   and `tran_daniel` and `adeyemi_tunde` carry overflow trips whose prose says
   explicitly "**not** a day trip" — the match fired on the negation. Replaced
   with a structural test: a day trip is one whose depart and return dates are
   equal. Found by `render_addendum.py`, which cross-checked the derived block
   against the trip rows themselves instead of trusting it. The corrected counts
   now match BUILD-PLAN §5.3 exactly: day trips exist only on `almeida_paulo`
   (W1, which demonstrates the exclusion) and `stavros_daphne` (T2, which reuses
   it).
3. **Field spellings inside document blocks were never unified.** D-I's
   normaliser unified container shapes and top-level keys, but each agent spelled
   the facts *inside* `documents.<doc>` its own way — `number`/`surname`/
   `given_names` in one client, `passport_number`/`surname_printed`/
   `given_names_printed` in another. Three renderers independently built closed
   alias resolvers that **raise on an unknown spelling rather than guess**, which
   is the right shape: a silent fallback here would render a blank passport
   number and pass every downstream text check.
4. **Docx and `soffice` output were not deterministic.** `docx.Document.save()`
   writes wall-clock zip timestamps and `soffice` embeds a wall-clock XMP packet
   that stamping the `/Info` dictionary does not touch. Normalised so that
   identical masterkey in gives byte-identical output out — without which Phase
   5 cannot diff a re-render against a manifest.

**One open data gap, recorded not closed:** `tran_daniel`'s
`documents.tax_return` carries no dependant even though `family.children` lists a
child of the marriage. It is a plausibility blemish for the Phase 5 per-client
reviewer, not a lock failure — the joint return's function as marriage evidence
(§9.3 rule 1) turns on the two spouses' names, which are present.

**D-M — `verify_coverage.py`: the differential sweep, added because the round
trip proved it could not see its own blind spot.** `render_n400.py`'s round trip
fills from the masterkey, reads back and diffs. It reported **0 diffs on all six
clients while five real defects were shipping.** Where a masterkey spelled a fact
`cob` and the fieldmap looked for `country_of_birth`, the renderer wrote nothing,
the extractor read nothing, and the diff compared an absent key against an absent
value and called it a match. Printed Part 2 items 10 and 11 were blank on two
clients; **printed Part 1's "Reason for Filing" — the single most important
control on the form — was unchecked on five of six**; Part 4 item 2 answered "No"
on five of six, promising a mailing address that was never supplied.

The lesson generalises past this build: **a check that compares intent to result
cannot see a fault that erases both.** What catches it is comparing the six
clients to each other. They are six renders of one form by one toolchain, so a
field carrying a value for five clients and empty for the sixth is a defect until
a stated rule explains it.

`verify_coverage.py` runs two sweeps:
- **A, differential** — any field filled for ≥5 clients and empty for another.
  Divergences that are legitimately basis-, family- or history-driven are excused
  by an explicit `EXPECTED_DIVERGENCE` table that records *why* (Part 5's spousal
  block is skipped for 316(a) by the blank's own printed instruction; Part 6 is
  empty for the childless; the Part 8 table depth varies with trip count). A
  blank whose masterkey value is itself empty is also excused — `stavros_daphne`
  genuinely has no middle name.
- **B, must-fill / must-be-empty** — a hand-written list keyed to *printed*
  Parts. It carries the §16 r10/r11 controls, and, as D-E requires, it fails when
  a control field does not **exist** rather than passing vacuously.

Two false positives were found and fixed before the sweep was trusted, both
worth recording because each would have taught a reader to ignore it. **Radio
groups had to be collapsed:** the form renders eye colour as nine sibling widgets
`P7_Line5_Eye[0..8]` and which index carries the value depends on the answer —
Brown lands on `[0]`, Blue on `[1]` — so treating widgets as independent fields
reported every blue-eyed client as missing a field. And an empty masterkey value
had to excuse an empty field.

**Poison-tested, like the leakage scan.** Clearing Part 1's eligibility box and
Part 11's telephone on one client — exactly the bug class the toolsmith found —
turns it red on four counts and names the client, the field and the peers that
fill it. Restoring returns it to green.

**D-N — Phase 5 found two blocking render defects that every scripted gate had
passed. Both are fixed; both are worth recording for what they say about
verification.**

**1. Every packet shipped a blank passport page, and nothing noticed.**
`PdfWriter.append` over seventeen components produced a merged file in which the
passport bio page's `/Resources` had lost its `/Font` entry to a cross-page
resource-name collision. Ghostscript then flattened the page to its two images
and no text. The result was a merged packet whose applicant passport — a *core*
exhibit, and the surface the MRZ and name locks depend on — was visually blank,
in all six clients, plus the spouse passport in the two spousal ones.

Every scripted gate stayed green throughout: the page count matched, the field
count was zero, the TOC/divider/document-count lock held, and the component file
on disk was perfect. **The defect lived entirely in the gap between "the
components are right" and "the merged artefact is right", and only a human
looking at a rendered page found it** — two Phase 5 reviewers, independently, on
different clients.

Diagnosis, by elimination: gs on the passport component alone keeps its text; gs
on page 24 of the pypdf-merged file, extracted alone, keeps its text; gs over the
whole pypdf-merged file loses it. So the fault is the merge, not the page and not
the flatten. **Concatenation moved from pypdf to gs**, which does the
concatenation and the flatten in one pass with its own resource namespacing. This
diverges from BUILD-PLAN §1's "merge with pypdf `PdfWriter.append`", and the
divergence is deliberate: §1's real constraint is *never `pdfunite`*, because
`pdfunite` corrupts the AcroForm. That hazard does not apply here — the merged
packet is required to carry zero form fields, and the N-400 component keeps its
own fields because it is never rewritten.

`merge_packet.py` now **asserts that no merged page is textless**, naming the
component each page came from. That check would have caught this on the first
render, and it is the lesson: a count-based lock cannot see a page that still
exists but has been emptied.

**2. N-400 printed Part 5 Items 7 and 8 were swapped on every spousal packet.**
The widget over printed Item 7 ("How many times has your current spouse been
married?") is named `P10_Line4g_Employer[0]`. The first field map took that name
at face value, so the spouse's employer went into the times-married box — where
it rendered as the clipped fragment `re Prot` — and the count `1` went into the
employer box.

This is the same trap as the `/TU` tooltips in D-H2, one layer deeper: **on this
blank, neither the tooltips nor the internal field names track the printed form.
Geometry is the only reliable authority.** The correction was made by comparing
widget `/Rect` positions against `pdftotext -bbox` word positions: the widget at
y=102 from the page top sits against printed Item 7 at y=103 and is 42pt wide, a
count box; the 318pt-wide box at y=162 is Item 8.

Item 8 is now **deliberately unmapped for every client.** The form's own printed
instruction beneath it reads "Only answer Item Number 8. if you are filing under
Part 1., Item Number 1.d., Spouse of U.S. Citizen in Qualified Employment
Abroad." No client in this set files under 1.d, so blank is the correct value and
the spouse's employer remains a masterkey fact that no form field consumes.

**D-O — the T2 dogfood run passed, and its two findings were both real.**
A solver given only the challenge article, the three worked pairs and T2's input
folder derived the correct eight-document set with the correct triggers, stated
the exhibit rule in its own words, excluded the day trip, resolved the superseded
address by chronology corroborated against the tax return, and — the point of the
Phase 2 blocking finding — **caught Part 9 Items 8.a and 12 from Daphne's
narrated prose.** It also picked the Elgin lockbox correctly for New Jersey by
generalising from two worked examples.

It reported one genuine data bug and one genuine ambiguity, which is exactly what
the dogfood exists to surface:
- **The data bug, now fixed.** T2's account of the 2015 notices said they went to
  "an address he'd already moved away from", while the address history showed
  continuous occupancy from 2011 to 2024. Both could not be true. Rewritten so
  the correspondence address on the 2013 filing was the *daughter's* — she filed
  the petition and gave her own address, then moved in 2014 without updating a
  still-open case. The applicant never moved. Fixed in the masterkey narrative
  and in her email 000004, in her own voice, and it now reads as the thing she
  feels worst about, which suits the register.
- **The ambiguity, left open deliberately.** Whether the military discharge paper
  should be its own exhibit cannot be settled from three worked examples: it is
  either documentary evidence for a disclosed Part 9 item (like W3's court
  record) or inert over-delivery (like W1's second-email pile). The solver chose
  inert, which matches the answer key. Recorded rather than closed, because
  closing it would mean adding a fourth worked pair.

**D-P — the N-400 printed clipped, and the fix meant generating appearance
streams instead of asking for them.** Phase 5 reviewers found Part 4 and Part 7
cells printing "Harborline Struc", "United St", "ructural Engine" — values
correct in the field data and correct under `pdftotext`, wrong on the page.

`NeedAppearances = true` asks a *viewer* to draw each field. Ghostscript, doing
the flatten, drew them at its own fixed size and clipped the overflow. Setting a
per-field `/DA` did not help: with NeedAppearances set, gs never consults it.

So `mklib` now builds the appearance streams itself — measuring each value in
Helvetica against its widget's `/Rect` and choosing the largest size from 9pt
down to a 4pt floor that fits — and then turns NeedAppearances **off**, because a
generator that regenerates appearances would undo the work. Comb fields are
skipped (the form spaces those itself) and so are the PDF417 barcode widgets,
which carry their own graphic: overwriting those printed the literal string
`N-400|01/20/25|5` where the barcode belongs, caught on the first visual check
after the change.

One self-inflicted bug worth recording: the first version seeded its Helvetica
width table with a module-level `for _c, _w in zip(...)` loop, which rebound
`mklib`'s own `_w()` XML-namespace helper to an integer and broke every docx page
with "'int' object is not callable". The table is now seeded inside a function so
its loop variables cannot leak.

**D-Q — Ghostscript renders one filled 1040 wrong, and poppler does not.**
With the clipping fixed, the ink guard immediately caught a second defect the
text guard could not see: `nowak_agata`'s 1040 page 2 flattened to 0.4% ink
against 15.6% before the flatten — the page's rules and labels simply were not
painted, while its text layer survived intact.

It is not the data: clearing the two fields unique to that client does not help,
and the byte-identical template filled for two other clients flattens correctly.
It is not a flag: `-dPreserveMarkedContent=false`, `-dNOTRANSPARENCY`,
`-dCompatibilityLevel=1.4`, `-dPDFSETTINGS=/prepress` and keeping annotations all
reproduce it exactly. It is not the concatenation: gs on that one component alone
reproduces it.

poppler renders the page correctly, so poppler now does the form flatten:
`merge_packet.py` pre-flattens every **form-bearing** component with
`pdftocairo -pdf` — which drops the AcroForm and emits a flat, still
text-extractable page — and gs is left to concatenate. Components with no form
fields are passed through untouched, so the extra pass costs two files per
packet.

**The guard that found it is the one worth keeping.** `merge_packet.py` now
rasterises every merged page and asserts a minimum ink coverage, with a much
lower floor for pages that are legitimately sparse — dividers and tab covers are
two short lines on an empty sheet, about 0.2% ink, and are identified by label
rather than by loosening the threshold for everyone. Text extraction alone
passed this page; only measuring the paint caught it.

**D-R — what was cut, and what is left open.** Recorded here so the gaps are
findable rather than implied.

**Cut, per BUILD-PLAN §10's own cut order:**
- **Dogfood runs for T1 and T3.** Cut #3 permits "dogfood T2 only"; T2 is the
  intended median and the first target, and it passed both by inspection and by
  scripted diff. T1 and T3 have answer keys rendered and held in
  `lab/synthetic/answer-keys/`, so either can be run later without rebuilding.
- **Photo-realistic finish on the green card.** `fabricate_ids.fabricate(...,
  finish="photo")` applies rotation, perspective, desk texture and JPEG noise to
  the passport but only a background tint to the card faces, which are drawn as
  vector text rather than a warpable image. Cut #1 makes clean flat scans the
  acceptable floor, and they are met. Cost: W1 demonstrates the phone-photo mess
  type on the passport only.

**Open, recorded not closed:**
- **W2 Kavanagh has holes inside the residence window** — about 15 months of
  employment and 5 months of address unfilled, in a *worked pair*. T1 closes the
  same problem with an explicit "not employed (homemaker)" row. Raised by the
  set reviewer. Not closed because naming a first employer adds a twelfth entry
  to the registry's `collision_check.employers`, which is asserted unique, and
  the change would ripple into the input thread.
- **The normaliser still does not emit one spelling for everything.**
  `immigration.derived.early_filing_date` and `.earliest_filing_date` split 3/3
  with neither set carrying the other; `height_ft`/`height` and
  `weight_lb`/`weight_lbs` coexist because the normaliser adds the canonical key
  without removing the original. Nothing currently reads the drifting names —
  `validate_masterkeys.py` recomputes the filing window from `lpr_date` directly,
  which is why it stayed green — but that is luck, not design. Two mirror lines
  in the normaliser would close it.
- **The C3 ordering cue is thin.** Because W2 supplies exactly one C3 document,
  the catalog's `C3a → C3b → C3c` precedence is never observable in a worked
  pair. T1 needs the joint deed at DOCUMENT 8 and the child's passport at 9; a
  solver grouping by kind could invert them. What carries it is one line of one
  email in T1's own thread, which happens to list the documents in precedence
  order. Whoever sets a dogfood diff's ordering tolerance should know it rests
  on that.
- **nowak: Part 14 renders empty.** Raised as a should-fix, but probably not a
  defect: the T2 dogfood solver independently *inferred* from the worked
  examples that the firm never types the narrative into Part 14 and always ships
  it as a separate written-explanation exhibit — and matched the answer key by
  doing so. Changing it now would break a rule a solver has already proven is
  learnable. Left as it is, deliberately.
- **tran: the joint 1040 lists no dependant** although a child of the marriage
  exists. A plausibility blemish, not a lock failure — the return's function as
  marriage evidence turns on the two spouses' names, which are present.

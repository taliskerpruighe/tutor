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

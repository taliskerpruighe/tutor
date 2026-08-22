# Phase 5 — Layer-2 Per-Client Review — `tran_daniel` (T1)

**Verdict: FAIL**

Two blocking defects were found, both confined to the render/merge step of
the final `N-400 Packet.pdf` — the masterkey, the input correspondence, and
the individual Tab-B component files are all correct on their own. But the
merged packet is the filing artifact, and as generated it is missing the
content of a CORE identity exhibit (the applicant's own passport bio page)
and carries garbled/misplaced data on the N-400 form itself. Neither is
cosmetic; both would need to be caught before this packet could be filed.
The narrative, the negative control, the name-change handling, and the
no-firm-identity discipline are all sound — see below — but they don't
outweigh a blank CORE exhibit.

---

## Blast radius — why the green gates didn't catch this

Pages 24 and 31 exist, are correctly counted, and sit in the correct TOC/
divider slots — so **page-count, TOC/divider/document-count-lock, and any
gate keyed on page or document counts all pass green on a packet with two
blank exhibits.** Text-coverage sweeps run against the *component* files
(`B-4. Bio Page of Passport.pdf`, `B-7. Bio Page of Spouse Passport.pdf`)
would also pass green, since those standalone files are correct — the
corruption is introduced only when they're merged into `N-400 Packet.pdf`.
This is exactly the failure mode a layer-2 human reviewer exists to catch:
every scripted gate that counts things or checks components in isolation is
satisfied; only opening the final merged artifact and rendering it shows the
defect.

Since the merge step is shared tooling, not client-specific, **this is worth
a one-line sweep across every other client's merged packet before this build
ships anything**: `for p in $(seq 1 N); do pdffonts -f $p -l $p "N-400
Packet.pdf" | tail -n +3 | wc -l; done` and flag any page reporting 0 fonts
that isn't supposed to be image-only. I did not run this on other clients —
corpus quarantine — but whoever holds the full set should.

## Findings

### Blocking

**1. Two of three passport bio pages are blank in the merged `N-400 Packet.pdf`.**
- File: `output/N-400 Packet.pdf`, page 24 (Document 4 — applicant's own
  passport bio page) and page 31 (Document 7 — spouse's passport bio page).
- Both pages have zero extractable text and zero embedded fonts
  (`pdffonts -f 24 -l 24` / `-f 31 -l 31` return empty tables; `pdftotext`
  returns nothing). Rendered to PNG at 150dpi, both pages are visually blank
  except for a faint gray footer bar.
- This is a merge-stage defect, not a data or source problem: the standalone
  component files render correctly and completely —
  `output/Tab B (Biographical Info)/B-4. Bio Page of Passport.pdf` shows
  Ha's full bio page (VU / THANH HA / C6820451, correct MRZ) and
  `.../B-7. Bio Page of Spouse Passport.pdf` shows Daniel's full bio page
  (TRAN / DANIEL QUANG / 548219307, correct MRZ). Only the copies inside the
  final merged packet lost their content.
- The child's passport (Document 9, page 35) merged correctly and is the
  control case proving this is not a systemic problem — it's isolated to
  exactly these two pages.
- Consequence: as currently generated, the filed packet is missing the
  content of two identity-anchoring exhibits, including one CORE document
  (the applicant's own passport).
- **Root cause, located precisely via `mutool show`:** in the standalone
  `B-4. Bio Page of Passport.pdf`, the page's content stream (object 4 0 R,
  812 bytes) contains the full text layer — every `BT ... Tj ... ET` block
  for "Type/Code," "Passport No.," the MRZ, etc. — plus two image `Do`
  calls. In the merged packet, page 24's page object (2247 0 R) points to a
  *different, much shorter* content stream (2252 0 R, 159 bytes) that
  contains **only** a background fill and the same two image `Do` calls —
  every `BT`/`Tj` text operator is gone. Consistent with this, page 24's
  `/Resources` dictionary in the merged file has no `/Font` key at all
  (`/ProcSet /ExtGState /XObject` only), whereas the working comparison
  pages — 26 (green card), 33 (deed), 35 (child's passport) — all carry a
  `/Font` entry and share font objects `35 0 R`/`36 0 R` correctly. Page 31
  (spouse's passport) shows the identical pattern. **What to change:** this
  points at the merge/concatenation step substituting or truncating the
  content stream specifically for these two documents rather than a data or
  font-resource problem per se — the font resource is *also* missing, but
  only because the text operators that would have used it were already gone
  before the resource dict was assembled. Worth checking whether the merge
  tool has a code path that treats these two documents differently from the
  other eight (both are adult passport bio pages generated with the same
  sub-template as the child's, which worked — so the discriminator is not
  document type but something else, e.g. processing order or a
  duplicate-resource-name collision during merge).

**2. N-400 Part 5, Items 7 and 8 show swapped/garbled values.**
- File: `output/N-400 Packet.pdf`, page 13 (Form page 5 of 14).
- Item 7 ("How many times has your current spouse been married?") — a
  single-digit answer box — shows the clipped text `re Prot`, a truncated
  fragment of "Trestle Fire Protection" (Daniel's employer, per
  `masterkey.norm.yaml: family.spouse.employer`).
- Item 8 ("Current Spouse's Current Employer or Company") shows `1` — the
  value that belongs in Item 7.
- Item 8 is explicitly instructed on the form to be answered only if filing
  under Part 1, Item 1.d (Spouse of USC in Qualified Employment Outside the
  US); this client correctly checked box B (Spouse of U.S. Citizen, verified
  by direct render of page 9), so Item 8 should be blank regardless — instead
  it's carrying a misplaced value.
- Confirmed by direct visual render (150dpi PNG), not just text extraction —
  screenshot shows the box literally overflowing with clipped text.
  **What to change:** field-mapping bug in the N-400 renderer — Item 7 and
  Item 8 values are transposed for this client, and Item 8 should be
  suppressed entirely for a Part 1.B filer.

### Should-fix

**3. Part 4/5 boundary row overlaps the page footer.**
- File: `output/N-400 Packet.pdf`, page 12 (Form page 4 of 14), Item 5.b
  ("Date Your Current Spouse Became a U.S. Citizen").
- The row is compressed against the very bottom margin; the answer box
  border overlaps and visually strikes through the "5.b." label text, and the
  table grid lines are broken/malformed at the page edge, right above the
  footer. Cosmetic, not a content error (the date `05/21/2009` itself is
  correct), but it's untidy enough that a reviewer should see it fixed.

### Note

**4. Deed "prepared by" attorney field correctly suppressed.** The brief
flagged the deed as the most likely place for a firm-identity leak, since
real recorded deeds carry a "prepared by" attorney line. The masterkey does
carry an invented preparer (`Heather M. Collins, Attorney at Law`) as
internal metadata, but it does **not** appear anywhere in the rendered deed
(`output/Tab B (Biographical Info)/B-8. Joint Deed.pdf`, verified by direct
render) or anywhere else in the packet. A whole-packet grep for
`attorney|esq\.|law office|LLP|law firm|Collins|prepared by` turns up only
standard N-400 boilerplate ("...law enforcement officer, or attorney,
told you..."), not a leak. Because the merged-packet text dump used for this
grep is missing pages 24 and 31 (Finding 1), I also ran the same check
directly against the standalone component text for those two documents
(`B-4. Bio Page of Passport.pdf`, `B-7. Bio Page of Spouse Passport.pdf`) —
clean, no firm identity in either. This is the schema-slot-is-dead rule
applied correctly — worth recording as evidence it was actually checked, not
just asserted.

**5. Deed exhibit is visually thin as a "recorded instrument."** It carries a
recording block (instrument number, date, county recorder) which is a nice
touch, but has no notary acknowledgment, no grantor signature lines, and no
legal description beyond the street address. This is minor — the recording
block does the essential work of making it look official — and may be a
deliberate simplification consistent with the rest of the corpus's document
fidelity level, so I'm not marking it should-fix, but a build note.

**6. Masterkey mislabels the printed Part for the spouse-passport lock.**
`masterkey.norm.yaml`'s `consistency_locks.spouse_passport_lock` reads
"N-400 **Part 7** (Marital History)" — but Marital History is printed
**Part 5** (confirmed by direct render of pages 12–13, and by `brief.md`
itself); Part 7 is Employment and Schools. Harmless to the render — nothing
reads this rule's prose, only its `value` — but confusing to maintain, and
ironic given this masterkey's own `_authored_notes.disagreements` section is
otherwise unusually careful about exactly this Part-numbering hazard
(it documents the printed Part 9→10→11→12→13→14→15→16 sequence in detail
elsewhere). Worth a one-line fix for whoever maintains this file next.

---

## The negative control (auto insurance)

Genuinely clear, and it's the best-constructed negative control I'd expect
to see. `input/000004_2026-05-04_deed-child-passport-auto-insurance/body.txt`
quotes the firm's original three-item request verbatim at the top of the
message (including "Any evidence of a jointly-held automobile insurance
policy, if you have one"), and Daniel's numbered reply directly under it
states: "Ours is through my employer's group plan and it's in my name only,
so I don't think it helps you." The ask and the refusal sit in the same
message, in the same numbered structure as the two exhibits that *do* fire
(deed, child's passport). A solver reading this input as intended will see
unambiguously that C3b doesn't fire for lack of supplied evidence — not
because nobody asked. This is exactly the generalization test the brief
describes, and it lands. Confirmed against the masterkey: `evidence_declined:
[auto_policy]`, `c3b_fires: false`, and the deed/child-passport equivalents
both fire (`c3a_fires: true`, `c3c_fires: true`).

## The name change

Also unambiguous in the input. `000008_2026-05-13_name-change-question` is
Ha's own message, first person, unhedged: "I'd like to take Daniel's
surname, Tran, on the N-400." `000011_2026-05-20_name-change-confirmed` has
Daniel restate it explicitly ("yes, she wants to go ahead with the name
change to Ha Thanh Tran on the application") while flagging the mismatch
with her existing documents — which is itself a tell for a solver that this
is a request, not a fact about any other document. Checked against the
output: the N-400's own Part 2 Item 1 (current legal name) reads Vu / Ha /
Thanh, and Item 3 (name change) reads Tran / Ha / Thanh — the single field of
record, exactly as specified. Every other artifact I checked — applicant
cover page, cover letter Re: block, tax return spouse line, the passport
exhibit, the deed, the signature page's printed name — carries "Vu Thanh
Ha," never "Ha Thanh Tran." I found no instance of the requested name
leaking into a document that should carry the current legal name.

I'd also flag as a positive (not a defect): Ha's resume
(`input/000002.../Ha_Vu_Resume.pdf`) headers itself "HA THANH VU" — Western
name order, plausible for a document written for a U.S. employer — while
every other surface uses Vietnamese order (family name first). Since the
resume is an input-only document used solely for the employment/Part 7 lock
(not a name-lock surface), this is authentic texture, not an inconsistency,
and it demonstrates the packet is internally consistent by function rather
than merely uniform in string, per the brief's specific caution.

## No I-751 / no I-797C

Confirmed clean. `000001_2026-04-27_engagement-intake` point 5 has Daniel do
the arithmetic himself in-thread ("two years and eight months, well past any
two-year mark, so I don't think any of that conditional-resident stuff
applies to her at all"), and the green-card scan shows only the unconditional
10-year card. Nothing else in the thread or the packet suggests a 2-year
card or a pending I-751 ever existed. The masterkey's
`immigration.conditional_resident` block reasons through both conjuncts
independently and correctly concludes `was_cr: false`; `c2_fires: false` is
reflected nowhere in the output (no I-797C exhibit, no CR language on the
N-400).

## Timeline, voice, and coherence

All dates reconcile cleanly: marriage (2020-03-14) → first entry to the US
(2020-05-27, four days after the Gahanna address start, which is fine since
that's also her entry date) → child's birth (2021-08-02) → LPR
(2022-11-30) → deed closing (2023-04-14) → move-in (2023-04-20, six days
after closing, plausible) → Scioto start (corrected to 2023-01-09 via Ha's
own follow-up, not Daniel's original "January 2022") → seven trips spanning
2023–2026. Nothing strains credulity.

Voice matches the card closely: Daniel's messages run long, numbered,
self-answering, closing on the same forward-looking sentence almost every
time ("Let me know what you need next and I'll get it turned around
tonight"), with the one "Sent from my phone, apologies for typos" that is,
as specified, typo-free. Ha's three messages are short, correct, and
slightly formal, including the one that fixes Daniel's date error. They read
as two different people.

The folder-naming mess (named for Daniel, the correspondent, not for Ha, the
applicant) is real but resolved the same way the brief says it should be —
by cross-referencing the passport and green-card scans — and never creates
genuine ambiguity in the thread, since Daniel's own messages consistently
refer to "Ha's citizenship application," "Ha's N-400," etc.

## Look and feel

Dividers (checked Tab A divider, "TAB A / SUMMARY") are clean and legible at
the rendered size. The applicant cover page and cover letter are clean,
correctly named, and carry no firm identity — the signature block is the bare
"Petition Preparer" line with nothing else. Part 11 is filled with Ha's own
phone/email and left unsigned; Part 13 (preparer block) is completely empty;
Part 1 Item B (Spouse of U.S. Citizen) is correctly checked. These three are
the load-bearing no-firm-identity/unsigned checks and all three passed on
direct visual inspection, not just by text grep.

## Is the input genuinely sufficient to build the packet?

Yes. Every fact needed for the ten-document packet is locatable in the
eleven input messages and their attachments, including the two hardest
things to get right: the negative control (present, and legible as
"asked-and-declined" rather than "never asked") and the name-change request
(present, unhedged, in Ha's own words and then confirmed by Daniel). The
employment-date correction (Daniel's "January 2022" superseded by Ha's "9
January 2023") is a fair, resolvable mess — the later, more specific,
first-person correction is the obvious one to trust, and the resume
corroborates the year. I did not find any fact the masterkey needed that
isn't recoverable from the input as a solver would read it.


---

## ADDENDUM — 2026-08-22, after the fixes

**This report's verdict above was FAIL. The two blocking findings it raised have since
been fixed and re-verified. The current state of this client is PASS.** The
original verdict is left standing rather than edited, because the finding was
correct when it was made and the record of it is the point.

### What was fixed

1. **Passport bio pages rendered blank in the merged packet** while the
   standalone components were correct. **Fixed** — and it was systemic, not
   client-specific: `PdfWriter.append` lost the page's `/Font` resource to a
   cross-page name collision, and gs then flattened the page to its images.
   Concatenation moved to gs, which does its own resource namespacing.
   `merge_packet.py` now asserts every merged page carries extractable text
   *and* a minimum ink coverage. See SPEC-DELTA D-N and D-Q.
2. **N-400 Part 5 Items 7 and 8 carried each other's values.** The widget over
   printed Item 7 is named `P10_Line4g_Employer[0]`; the first field map trusted
   the name. **Fixed** by geometry — widget `/Rect` positions compared against
   `pdftotext -bbox` word positions. Item 8 is now deliberately unmapped for
   every client, because the form restricts it to Part 1 Item 1.d filers and no
   client here is one. See SPEC-DELTA D-N.

### How the current state was verified
Re-rendered from the corrected toolchain, then: `verify_client.py` green;
`verify_coverage.py` green (a differential sweep of 325 N-400 fields across all
six clients, plus must-fill/must-be-empty controls proved to exist before being
asserted); `merge_packet.py`'s new text-layer and ink-coverage assertions pass on
every page; and the rendered pages the finding named were re-rasterised and
looked at. Determinism was re-confirmed after the toolchain changes: a full
re-render of a client is byte-identical across 26 components including the
merged packet.

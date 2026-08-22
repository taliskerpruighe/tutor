# Phase 5 — Per-Client Review — kavanagh_liam

## Verdict: FAIL

The email-to-packet story is genuinely good — better than most of what I'd expect from a
worked-pair sample — and every mess event this client exists to demonstrate resolves cleanly.
But the actual PDF that would go in the FedEx envelope has two confirmed, reproducible defects
that a human reviewer would catch on the first flip-through: three of the nine exhibits render
visually blank in the merged packet (though intact in their own component files), and two
adjacent items on the N-400 itself display swapped/wrong content. Both are blocking. I have
verified both with two independent renderers and a standalone-vs-merged comparison, so neither
is a rendering-tool artifact.

---

## Findings

### 1. [blocking] Three exhibit pages render blank in `N-400 Packet.pdf` — intact in their own component files

File: `lab/synthetic/clients/kavanagh_liam/output/N-400 Packet.pdf`, merged pages 24, 29, 31.

- **Page 24** = DOCUMENT 4, applicant's passport bio page (component: `Tab B (Biographical Info)/B-4. Bio Page of Passport.pdf`)
- **Page 29** = DOCUMENT 6, page 2 of 2, the 2024 joint tax return's Payments/Refund/Sign Here/Paid
  Preparer section (component: `Tab B (Biographical Info)/B-6. 2024 Income Tax Return.pdf`, page 2)
- **Page 31** = DOCUMENT 7, spouse's passport bio page (component: `Tab B (Biographical Info)/B-7. Bio Page of Spouse Passport.pdf`)

On all three, only a handful of overlay data survives (a few numbers, "Self-Prepared," a tiny
gray fragment) — the base template content (photo box, field labels, MRZ, "Sign Here," "Paid
Preparer Use Only," table headers) is missing. Rendered PNGs of these merged pages are 4.4–11 KB;
the same pages rendered from their own standalone component PDFs are 35–53 KB and look completely
correct — full labels, boxes, and (on the passports) the photo placeholder and MRZ lines.
Confirmed independently with `pdftoppm`, `pdftocairo`, and Ghostscript (`gs`), so this is not a
single-renderer quirk. `pdffonts` shows a font-embedding difference between the standalone B-6
page 2 (`HelveticaLTStd-Bold`, not embedded) and the merged page 29 (`XVHNFE+HelveticaLTStd-Bold`,
embedded subset) — consistent with something going wrong in the merge step for these three pages
specifically.

This hits two of the packet's nine mailed exhibits at their most load-bearing point — both
passport bio pages (the primary identity documents for applicant and spouse, one of them the
C1-triggered exhibit) — plus the signature/payments half of the tax return that the brief singles
out as the packet's marriage evidence. A reviewer or USCIS officer opening `N-400 Packet.pdf`
would see three near-blank pages where photo IDs and a return signature block should be.

Page 24 specifically is the surface the masterkey's `name_lock` and `dob_lock` name as
consistency anchors — "identical on N-400 Part 2, passport MRZ, cover letter Re: block,
applicant cover page, green card" — and where the verified MRZ check digits actually live. The
lock is true of the underlying data and true in the standalone component; in the file that ships,
that page is visually blank, so the thing the lock is supposed to guarantee is unverifiable by
looking at the deliverable.

**What to change:** re-run the merge step for this client (or re-verify the merge tool version)
and confirm pages 24, 29, and 31 of the shipped PDF match their standalone components byte-for-byte
in visible content, not just in extracted text.

### 2. [blocking] Form N-400 Part 5, Items 7 and 8 display swapped/wrong content

File: `Tab B (Biographical Info)/B-3. Form N-400, Application for Naturalization.pdf`, page 5 of 14
(merged page 13). Confirmed present in the **standalone** component file itself, not introduced by
merging — this is a form-fill defect.

- Item 7 ("How many times has your current spouse been married?") displays the clipped fragment
  **"Freight"** — the tail end of the spouse's employer name, "Halsted Freight Systems" — instead
  of the numeral it should hold. Per the masterkey (`family.spouse.times_married: 1`), Item 7
  should read "1"; that value is rendered correctly nowhere on the form.
- Item 8 ("Current Spouse's Current Employer or Company") displays **"1"** instead of being left
  blank. The form's own instruction directly under Item 8 reads: "Only answer Item Number 8. if
  you are filing under Part 1., Item Number 1.d., Spouse of U.S. Citizen in Qualified Employment
  Outside the United States." This applicant files under Item 1.b. (Spouse of U.S. Citizen), so
  Item 8 should be blank, not populated with the spouse's employer or anything else.

**What to change:** Item 7 should read "1"; Item 8 should be blank. Whatever field-fill logic is
placing the spouse-employer string is both mapping it to the wrong box and populating a box the
form instructs to leave empty for this filing basis.

### 3. [should-fix] Text overflow/clipping in Part 4 and Part 7, same root cause as Finding 2

Also confirmed in the standalone `B-3` component, not a merge artifact:

- **Part 4, current address** (page 4 of 14): the "Dates of Residence: To" box shows a bold
  "PRESENT" overlapping a second, lighter "PRESENT" directly underneath it — a doubled/ghosted
  rendering.
- **Part 4, prior address row** (Quarry Lane): the Country column shows "United" with "States"
  clipped off outside the cell.
- **Part 7, employment table**: "Riverbend Veterinary Clinic" runs directly into the City/Town
  column with no space or line break ("Riverbend VeteriBerwyn"), "United States" is clipped to
  "United St," and "Veterinary Technician" is clipped on *both* ends to "erinary Technic."

None of these change the underlying data (the correct values are recoverable from context and
from other locked-consistent surfaces, e.g. the resume-employer lock), but they are genuinely
visually broken on the form that ships, which is squarely in scope for a look-and-feel check.
Same likely root cause as Finding 2 — the field-fill overlay is not wrapping or truncating
long values safely, and in Item 7/8's case is also misrouting them.

### 4. [note] Part 9, Item 33 (disability exception to the Oath) has no basis anywhere in the eleven emails

The form correctly answers "No" to Item 33 ("Are you unable to take the Oath of Allegiance
because of a physical or developmental disability or mental impairment?"). But unlike the rest
of Part 9 — which email 000010 covers with confident, generalizing sweeps ("no association
with any military unit, police unit, self-defense unit, vigilante unit, rebel group, guerrilla
group, or militia of any kind, ever, anywhere," "none of the awful things on that part of the
list apply to her at all," "nothing like that at all") that plausibly cover their whole thematic
clusters — Item 33 sits in the middle of the affirmative oath run (31 Yes, 32 Yes, **33**, 34
Yes...37 Yes) and is never touched. Liam's summary jumps straight from "she understands the full
Oath ... yes she's willing to take it" to "yes to all three of the follow-ups" (35/36/37),
skipping past 33 without comment, and no email anywhere discusses disability. Defaulting to "No"
in the total absence of any contrary indication is standard, defensible intake practice (and
nothing else in this very forthcoming client's record hints otherwise), so I would not block on
this — but it is the one item in Part 9 that is not actually reachable from the prose, and worth
knowing about given this client's whole reason for existing is testing exactly that.

### 5. [note] Liam's opening promise that Siobhan "will chime in herself" is never paid off

Email 000001: "she'll chime in herself when she has a minute." She never does, across eleven
emails and eleven weeks — consistent with the brief and voice-card (she appears only as reported
speech throughout, by design), but Liam is otherwise apologetic out of all proportion to far
smaller lapses, and this unfulfilled promise is never acknowledged or walked back. A minor
realism blemish in the corpus, not a defect in the built packet.

---

## What I checked and found clean

- **Identity/applicant resolution.** The folder is named for Liam (the correspondent) throughout,
  but the packet correctly follows Siobhan Maire Brennan — her name, not Kavanagh, is on the cover
  page, the cover letter Re: block, N-400 Part 2, and matches the passport/green card exhibits
  exactly. "Kavanagh" appears only where it should: the spouse fields and the spouse's passport.
- **Superseded address.** Cicero (2022-01-10 to 2024-04-30) correctly demoted to the prior-address
  row; Berwyn (2024-05-01 to present) correctly the current/mailing address, zero-day gap, both
  addresses render on Part 4 as expected once you look past Finding 3's clipped "United."
- **Two email addresses, one person.** Correctly treated as a single correspondent throughout;
  the work-address email (000003) is, as the voice card predicts, the one message with no sign-off
  at all — a nice, deliberate confirmation this is the same person on shift.
- **Address-history window.** I initially flagged a possible gap between Siobhan's 2021-08-19
  arrival and the 2022-01-10 start of the Quarry Lane address, thinking Part 4 needed 5 years of
  coverage. It doesn't for this filer: Part 4's own instruction limits the "last 5 years" language
  to general-provision (1.a.) filers and defers spouse-of-citizen (1.b.) filers to the
  specific-instructions period, which per the masterkey's own `residence_window` is the 3-year
  window 2023-02-10–2026-02-10 — entirely covered by Cicero-then-Berwyn. No gap; not a finding.
- **I-751/spousal cluster.** Receipt number, received date, and notice date all reconcile across
  the masterkey, the emailed description, and the rendered I-797C exhibit (page 33, cleanly
  typeset and fully legible — the "terrible lighting" phone photo Liam describes was evidently
  regenerated as a clean exhibit rather than shipped as the actual photo, which is the right call).
  The green card's CR6 category and expired-2024-09-15 status, the pending I-751, and the joint
  auto policy all tell one consistent conditional-residence story.
- **Voice.** Liam's long, comma-spliced, apologetic, over-explaining register is consistent across
  all eleven messages and matches the voice card closely, including the effusive double-apology
  pattern on the address correction (000005) and the anxious "is that going to hold this up"
  framing of the I-751 (000004). Siobhan is reported speech only, as designed.
- **No-firm-identity rule.** Checked the full extracted text of `N-400 Packet.pdf` and the
  `docProps/core.xml` of all five `.docx` components (`dc:creator`, `cp:lastModifiedBy` both
  blank on every one) — no firm name, address, phone, or email anywhere. Part 13 (preparer) is
  entirely blank, the applicant's own phone/email correctly fill Part 11, the applicant's
  signature and date are blank, and the interpreter block (Part 12) is empty. "Petition Preparer"
  is the only, unattributed role line, on the cover letter only.
- **TOC/divider/document-count.** Rendered several dividers and the cover page at typical review
  resolution — legible, clean, no formatting breaks. Nine documents, nine dividers, nine TOC
  lines, in order.
- **Tax return exhibit (page 1 / AGI).** Page 1 of the 1040 (merged page 28) renders perfectly —
  filing status, both SSNs, address, and the $99,600 AGI all match the masterkey. Only page 2 of
  this same exhibit is affected by Finding 1.

## Is the packet genuinely buildable from prose alone?

Yes, with one caveat. This is a well-constructed worked pair: every fact in the masterkey traces
to a specific, plausible sentence in Liam's emails, the messiness (wrong person writing, wrong
address, two email addresses) is realistic and resolved the way a careful preparer would resolve
it, and Part 9's ~37-item moral-character section is genuinely covered by natural, in-character
prose sweeps rather than a checklist. The one soft spot is Item 33 (Finding 4), which isn't
reachable even generously — but it's a "no evidence, so No" default of the kind any real intake
would apply, not a hole that breaks the exercise.

The reason this client fails is not the prose-to-masterkey pipeline — it's what happened after
that, in rendering: two passport bio pages and half the tax return exhibit are blank in the file
that ships, and two adjacent items on the N-400 itself carry swapped/wrong content. Those are
concrete, reproducible, and both blocking.


---

## ADDENDUM — 2026-08-22, after the fixes

**This report's verdict above was FAIL. The blocking and should-fix findings it raised have since
been fixed and re-verified. The current state of this client is PASS.** The
original verdict is left standing rather than edited, because the finding was
correct when it was made and the record of it is the point.

### What was fixed

1. **Three exhibit pages rendered blank in the merged packet** (applicant
   passport, tax-return page 2, spouse passport) while the standalone components
   were correct. **Fixed**, and by two separate mechanisms, because there were
   two bugs wearing one symptom: the passports were a pypdf resource collision
   (concatenation moved to gs), and the 1040's second page was Ghostscript
   mis-rendering one specific filled form (form-bearing components are now
   pre-flattened with `pdftocairo`, which renders it correctly). SPEC-DELTA D-N
   and D-Q.
2. **N-400 Part 5 Items 7 and 8 carried each other's values.** Fixed by
   geometry; Item 8 is now deliberately unmapped for every client. SPEC-DELTA D-N.
3. **Field-fill overflow** — doubled "PRESENT", clipped "United", clipped
   employer and occupation text. **Fixed**: `mklib` now builds real `/AP`
   appearance streams sized to fit each widget instead of relying on
   `NeedAppearances`, which gs was honouring at a fixed size and clipping.
   SPEC-DELTA D-P.

### How the current state was verified
Re-rendered from the corrected toolchain, then: `verify_client.py` green;
`verify_coverage.py` green (a differential sweep of 325 N-400 fields across all
six clients, plus must-fill/must-be-empty controls proved to exist before being
asserted); `merge_packet.py`'s new text-layer and ink-coverage assertions pass on
every page; and the rendered pages the finding named were re-rasterised and
looked at. Determinism was re-confirmed after the toolchain changes: a full
re-render of a client is byte-identical across 26 components including the
merged packet.

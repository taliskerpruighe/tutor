# Phase 5 — Layer-2 Client Review — `almeida_paulo`

## Verdict: PASS WITH FINDINGS

One blocking finding, two should-fix findings, one pre-disclosed note. The
packet tells one coherent story, the three previously-fixed defects are
confirmed gone, and all four W1 mess types are present and correctly
resolved in substance — but a field-width/rendering bug on the N-400 clips
visible text in two tables (Part 4 and Part 7), and in one field doubles it.
None of this is visible to a text-extraction sweep, because `pdftotext`
recovers the full, correct underlying strings in every case — the defect is
in the printed *display*, not the data. That is exactly why a client with
24/24 `verify_client.py` checks green still has a look-and-feel defect: the
scripted gates read extracted text, and the text is intact. This finding and
the scripted gates are not in tension.

---

## Findings

### 1. [blocking] Part 7 employment table — employer, city, country, and occupation text clipped
**File:** `output/Tab B (Biographical Info)/B-3. Form N-400, Application for Naturalization.pdf`, page 5 of 14 (packet page 13); reproduced identically in the merged `output/N-400 Packet.pdf`, page 13.

Rendered at 250 dpi, the "Employer or School / Name" column shows
`Harborline Struc` and `Dunmore Precisio` — both clipped mid-word, not
wrapped. The "Country" column shows `United St` (Somerville row) and
`United St` (Medford row), both clipped. The "Occupation or Field of Study"
column shows `ructural Engine` and `esign Engineer`, clipped on **both**
sides, meaning the true string is centered/overflowing outside the visible
cell box in both directions. `pdftotext -layout` recovers the full correct
strings ("Harborline Structural Engineering LLC", "Dunmore Precision
Castings", "United States", "Structural Engineer", "Design Engineer") in
scrambled reading order — the data is intact; only the display clips it.

This is blocking because the brief's `resume_equals_part7` consistency lock
depends on a reader being able to see that the resume and Part 7 employer
names match, and on the printed page they cannot: "Harborline Struc" is not
independently verifiable against "Harborline Structural Engineering LLC" on
the resume without OCR or a text-layer copy-paste, which a reviewing officer
will not do.

Also visible in the same table: on the Dunmore row, `03/01/2016` and
`04/04/2019` (Employment Dates From/To) abut with no visible gutter between
them — same root cause (the field is sized to the glyph run rather than
wrapped or shrunk-to-fit). Not a separate finding; roll into this one.

**What to change:** the N-400 field-filling step (not the masterkey — the
underlying values are correct) needs auto-shrink-to-fit or a smaller fixed
point size for the Part 7 table's Name/City/Country/Occupation cells, and
for the Employment Dates From/To cells.

### 2. [should-fix] Part 4 prior-address table — Country clipped to "United"
**File:** same PDF, page 3 of 14 (packet page 11); confirmed pre-merge in the standalone `B-3` component, so not a merge artifact.

The prior-address row (118 Hollis Avenue, Medford, MA 02155) shows `United`
in the Country column where `United States` was entered. `pdftotext`
confirms the full string is present; only the rendered cell clips it.
Lower severity than finding 1 because a reader can trivially infer "United
States" from context (a Massachusetts ZIP code, an N-400 filed from a
Massachusetts address) — no fact is actually put in doubt, unlike the
employer names above.

**What to change:** same field-width/auto-size fix as finding 1, applied to
the Part 4 Country column.

### 3. [should-fix] Part 4 current-address "Dates of Residence: To" — doubled/overlapping "PRESENT"
**File:** same PDF, page 3 of 14 (packet page 11); confirmed pre-merge in the standalone component.

Zoomed render shows two overlapping instances of "PRESENT" at different
sizes in the same field, producing garbled, partly-illegible text. This
appears to be local to this one field: the same filler value renders cleanly
as a single "PRESENT" in the Part 7 employment table's "To" column two pages
later, so this is not a general "PRESENT" rendering fault — most likely two
stacked form elements at that one coordinate on Part 4. Should-fix rather
than blocking because the surrounding context (Item 1's "From 11/01/2019,"
Item 2's "current physical address") leaves no real ambiguity about the
applicant's current-residence status, only an ugly, unprofessional-looking
field on the first page a reader reaches.

**What to change:** the N-400 field-filling step, specifically whatever
places a value at the Part 4 current-address "Dates of Residence: To"
coordinate — check for two form fields or a filled-value-plus-overlay both
targeting the same location.

### 4. [note] Green-card phone-photo texture — pre-disclosed tool gap, confirmed present
**Files:** `input/000001_2025-10-16_documents-and-questionnaire/green_card_photo.pdf`; `output/Tab B (Biographical Info)/B-5. Permanent Resident Card.pdf`.

The masterkey's own `_authored_notes`/`mess_events` already discloses this:
`fabricate_ids.py`'s `_draw_card_face` accepts a `finish` argument but does
not yet apply `_apply_photo_finish` to card faces, "a tool gap outside this
client folder's scope, not hand-waved here." I confirmed it by rendering
both the input `green_card_photo.pdf` and the output card page: both are
flat, white-background, unrotated, no shadow or grain — visually
indistinguishable from a scan. By contrast, the input `passport_photo.pdf`
(and the output passport page) does carry a visible desk/shadow texture,
angled light and a dark vignette.

So: of the two documents meant to demonstrate the "phone-photo" mess type,
only one — the passport — is legible as a lesson. The green card reads as a
clean scan, not a phone photo, though every fact on it is correct and
consistent with the questionnaire regardless. Recorded as a note, not a
new defect, since the build already knows about it and has scoped it out of
this client folder; flagging so it isn't silently dropped from review.

---

## Confirmations requested by the brief

**Passport page carries real, extractable text (regression check for the
gs-merge fix).** Confirmed. `output/N-400 Packet.pdf` page 24 (`DOCUMENT 4`)
extracts cleanly via `pdftotext`, including both MRZ lines
(`P<BRAALMEIDA<<PAULO<MIGUEL<<<<<<<<<<<<<<<<<<` /
`FZ318842<6BRA8803229M3108099<<<<<<<<<<<<<<06`), identical to the standalone
`B-4. Bio Page of Passport.pdf` component. No textless pages were observed
anywhere in the 31-page merged packet during this review (I did not run
`merge_packet.py`'s own textless-page assertion directly — this is a visual
and `pdftotext` spot-check, consistent with, not a re-verification of, that
assertion).

**Part 5 Items 7 and 8 no longer swapped; Item 8 deliberately blank.**
Confirmed. Printed Item 7 ("How many times has your current spouse been
married?") and Item 8 ("Current Spouse's Current Employer or Company") both
render blank, correctly, since this applicant is single and not filing under
Part 1 Item 1.d.

**No firm identity anywhere in the output.** Confirmed. Cover letter closes
with the unattributed "Petition Preparer" line only — no name, address,
phone, or email. N-400 Part 11 (applicant's own phone/email) is filled
correctly: `(617) 555-0142` / `(617) 555-0142` / `paulo.almeida@quillmail.com`.
N-400 Part 13 (preparer block) is entirely blank — no name, business name,
phone, email, or signature. The N-400 ships unsigned (Part 11 Item 4
signature and date both blank).

**Four demonstrated mess types — legible as lessons:**
- **Day trip excluded per firm instruction.** Legible and well-taught. The
  day trip (Toronto, 2024-05-14, same-day drive) appears in
  `questionnaire.docx` (row 3, travel table) and in `email:000001`'s body,
  and is correctly absent from both the Part 8 table (6 rows, most recent
  first, correctly ending at the 7th-oldest countable trip on a row-count
  basis, not on the day trip) and the travel addendum (7 rows, the day trip
  never counted). The printed Part 8 instruction — "Do not include day
  trips (where the entire trip was completed within 24 hours) in the
  table" — sits directly above the table, which is what makes the exclusion
  teachable as a rule rather than arbitrary.
- **Over-delivery of unrequested documents.** Legible. The expired 2014
  passport, lease, and vaccination record arrive in `email:000002` and are
  cleanly absent from the output (`grep` of the merged packet's extracted
  text turns up no genuine hits for "lease," "vaccination," "EA204471," or
  "expired" — only false-positive substring matches inside unrelated words
  like "please").
- **Phone-photo documents.** Half-legible — see finding 4. Passport texture
  present and effective; green-card texture absent (known, disclosed gap).
- **Unrelated-matter noise.** Legible. The cousin's B-2 visitor-visa
  question (`email:000005`) touches no packet fact and produces no
  document; confirmed zero mentions of "cousin," "B-2," or "visitor visa"
  anywhere in the output.

---

## Other checks performed (no findings)

- **Timeline plausibility:** DOB 1988-03-22; first entered US 2015-09-02 at
  27 (Selective Service correctly answered No, "first entered ... at age
  27"); employment continuous 2016-03-01 (Dunmore) → 2019-04-08 (Harborline)
  → present, no gap; LPR since 2020-06-19; filed 2025-12-08, 262 days after
  the earliest eligible date (2025-03-21) — all internally consistent and
  matches `masterkey.norm.yaml`'s `rule_inputs`.
- **Narrative coherence, emails vs. form:** every fact volunteered across
  the five emails (Medford end date, employment dates, travel/day-trip
  note) appears correctly in the corresponding N-400 field.
- **Voice:** consistent terse-professional-engineer register across all
  five emails — short declarative sentences, numbered notes, dates
  written `mm/dd/yyyy` in forms vs. spelled out only where prose calls for
  it, minimal sign-offs, one "Thanks" near the end of two of the five
  (distinct) threads. No deviation from `voice-card.md`.
- **LPR-date triple lock:** 2020-06-19 identical across green card
  ("Resident Since"), N-400 Part 2 Item 7, and the cover letter's 316(a)
  eligibility clause. Confirmed by direct render/text comparison.
- **Tax-address lock:** 47 Larkspur Street, Apt 3, Somerville, MA 02143
  identical on the Form 1040 and N-400 Part 4 current address. Confirmed.
- **TOC/divider/document-count lock:** TOC lists exactly 7 lines, in order,
  matching the 7 `DOCUMENT n` dividers and 7 components actually present.
  Confirmed.
- **Dividers and cover pages:** rendered at 100 dpi, legible, comfortably
  above 12 pt, no visual defects.
- **Part 9 moral-character answers:** spot-checked against
  `masterkey.norm.yaml` — all No except the oath items (31, 32, 34–37 Yes),
  matching the questionnaire exactly.

No corpus-quarantine violations; only `almeida_paulo`'s own folders were
read.

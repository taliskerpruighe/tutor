# Phase 5 — Per-Client Review: nowak_agata (W3)

**Verdict: PASS WITH FINDINGS**

No blocking narrative-coherence problem. The packet's single most important
teaching job — showing C5 (court records) and C6 (written explanation) firing
as two genuinely independent Part 9 triggers — succeeds cleanly, with direct
textual evidence below. Two should-fix rendering defects were found on the
N-400 itself, plus one should-fix content gap (a missing Part 14 pointer), and
two notes. Nothing here threatens learnability of T2 Stavros or of this
worked pair.

---

## Explicit judgement: do C5 and C6 read as independent?

**Yes.** Reading only the four client emails and the delivered exhibits, a
solver has no way to connect the arrest to the removal proceedings, and no
sentence anywhere invites the connection.

Evidence:

- **Two separate emails, two separate subjects.** `000003_...-arrest-explanation-and-court-record`
  (15 Apr 2026, subject "...Item 15.b") covers only the 8 Nov 2019 Ann Arbor
  arrest. `000004_...-removal-proceedings-explanation` (4 May 2026, subject
  "...Item 20") covers only the 11 Mar 2015 removal proceedings, nineteen
  days later, under its own subject line. Neither body mentions the other
  event, the other date, the other city, or the other item number.
- **The one phrase a suspicious reader might flag, checked and dismissed.**
  Email 0004 opens: "I want to explain the removal proceedings, since Item 20
  on the form **also** asks about this." The "also" reaches back only to the
  general fact that Part 9 has several items requiring explanation (she had
  already answered 15.b by email at that point) — it supplies no shared
  subject matter, date, or place with the arrest. There is no "as I mentioned
  about my other issue" construction anywhere in the corpus for this client.
- **The output exhibits stay in their lanes.** `B-7. Court Records.pdf`
  (Tab B, Document 7) is the certified court disposition only — court name,
  docket, statute, plea, disposition, judge, clerk certification — and
  contains no reference to immigration proceedings. `B-8. Written
  Explanation.pdf` (Document 8) answers "Part 9., Item Number 20" only, and
  its closing line ("She was never removed or deported (see Item 21)")
  points to the removal-proceedings item family, never to Item 15.
- **The N-400 form itself keeps them apart.** Item 15.b's table row
  (offense date, place, disposition) carries only the arrest; Item 20/21 are
  answered Yes/No on their own line with no cross-reference; Part 14
  (Additional Information) is not used to splice the two together (see
  Finding 3 below — it isn't used for either item, which is a separate
  problem, but it does mean neither item borrows the other's space).
- **Timeline keeps them apart too.** Seven years separate the two triggering
  events (2015 removal filing vs. 2019 arrest), and the underlying causes are
  unrelated (an F-1 status lapse vs. a disorderly-conduct charge). Nothing in
  the masterkey's `bridge_narrative_1` — which stays out of the packet
  entirely per its own note — bleeds into either client-facing narrative.

**Conclusion: T2 Stavros's requirement — that C6 must be learnable as firing
without any C5 present — is satisfied by this worked pair. This is not a
blocking finding.**

---

## Findings

### 1. [should-fix] N-400 Item 15.b table: "Ann Arbor, Michigan" overflows into the adjacent column
**File:** `output/Tab B (Biographical Info)/B-3. Form N-400, Application for
Naturalization.pdf`, page 8 of 14 (merged `N-400 Packet.pdf`, page 16);
same defect in the standalone file.

Rendered at any resolution, the "Place of Crime or Offense" cell in the
Item 15 table shows `Ann Arbor, Mich` running directly into the next
column's `Charges dismissed` with no visible cell boundary between them —
the two strings visually merge into `Ann Arbor, MichCharges dismissed`. The
underlying text layer is correct (`pdftotext` recovers "Ann Arbor, Michigan"
in full), so this is a fill/render-width problem, not a data problem. It is
data-dependent, not a shared-template defect: I rendered page 6 of the blank
`lab/synthetic/blanks/n-400.pdf` and confirmed the blank cell is empty and
undamaged — the overflow only appears once this client's value is filled
in. A shorter place string would not clip.

This lands on exactly the page that demonstrates C5, which raises its
priority. Note for whoever fixes it: `masterkey.norm.yaml`'s
`consistency_locks` already carries an abbreviated form, `"Ann Arbor MI"`,
alongside the full `documents.court_records`/`moral_character.q15b.arrest_detail.place`
value `"Ann Arbor, Michigan"` — the abbreviation looks like the built-in
escape valve for this cell. Any fix must preserve the machine-verified
line-for-line lock against the court-records exhibit (offense date, place,
disposition must still agree word-for-word with `B-7`), so if the abbreviated
form is used in the N-400 table cell, confirm that lock is re-verified, not
silently broken.

### 2. [should-fix] Stray empty-field lattice overlaps printed text at the bottom of N-400 page 6
**File:** same file, page 6 of 14 (merged packet page 14).

At the foot of Part 9 Item 5.b, an extra row of empty bordered boxes is
rendered directly on top of the last two lines of printed instructional
text ("...destruction of property; or" / "Sabotage?"), striking through the
words and partially obscuring "Sabotage?". I confirmed this is not present
in the blank form: `pdftoppm` of `lab/synthetic/blanks/n-400.pdf` page 6
shows that text clean, with no box lattice. So this is introduced during
this client's fill/merge step, not inherited from the shared blank asset —
worth flagging precisely so it isn't misdiagnosed as a template-wide issue
when someone goes to fix it; it may still turn out to be common across
clients that reach this code path, but it is not present in the source
blank itself.

### 3. [should-fix] Item 20's Part 14 pointer never renders
**File:** `output/Tab B (Biographical Info)/B-3. Form N-400, Application for
Naturalization.pdf`, Part 14 (page 13 of 14) and Part 9 Item 20 (page 9 of
14).

The form's own printed instruction above Items 20–21 says: "If you answer
'Yes' to Item Numbers 20. - 21. below, provide an explanation in the space
provided in Part 14. Additional Information." Item 20 is answered Yes. Part
14 renders completely empty — no name, no Page/Part/Item Number entry, no
pointer of any kind to the written explanation. `masterkey.norm.yaml`'s own
`documents.written_explanation.text` field describes "one narrative, two
homes (Part 14 reference and the written-explanation document)," which
reads as though a Part 14 entry ("Item Number 20 — see Document 8, Written
Explanation") was intended and simply didn't make it into the render. This
is a real, packet-visible gap in "does the packet tell one story": a solver
who reads the form's own instruction and then checks Part 14 finds nothing
there, even though the explanation exists two documents later in the same
tab. It does not create any false cross-reference and does not threaten
C5/C6 independence — it's a missing pointer, not a wrong one — but it should
be added: one line in Part 14 (Page 9, Part 9, Item Number 20 → "See
Document 8, Written Explanation").

### 4. [note] voice-card.md contains a sample line that couples the two Part-9 events
**File:** `voice-card.md`, "Invented sample lines" section, final example.

The card's last invented sample has Ms. Nowak saying, in one breath: "The
arrest was November 2019... The immigration court was much earlier, 2015...
these are not connected." This line was never shipped — neither email uses
it, and the two events stay in separate messages exactly as `brief.md`
requires — so the delivered packet is unaffected. But the line directly
contradicts `brief.md`'s binding rule ("Nothing in either narrative may
reference the other") and sits in the one voice-card file whose whole
purpose is to be drawn from for regeneration. It is a hazard for any future
resynthesis pass on this client (or a careless reuse of the sample for a
similar client) rather than a defect in what shipped. Recommend deleting or
rewriting that sample line so the card cannot be misread as license to
couple the two events.

### 5. [note] ~17-month gap in the masterkey's own employment-authorization story, invisible in the packet
**File:** `masterkey.norm.yaml`, `immigration.bridge_narrative_1`.

The masterkey's background narrative asserts that continuous employment
from 2016-05 is "lawful and coherent" because of an I-485-linked EAD — but
that EAD is dated from 2017-10, roughly seventeen months after the
employment start, while removal proceedings were still open (they
terminated 2017-09-22). This is masterkey-internal world-building only; the
narrative explicitly says the I-140/I-485 mechanics are "masterkey context,
not packet prose," and neither shipped email nor the N-400 itself asserts a
work-authorization basis for that period — Part 7 employment history asks
only for employer/dates, not authorization basis. A solver reading only the
packet has no visible inconsistency to trip over. Recorded for completeness
since the task asked me to judge timeline plausibility "as a life," but this
does not affect learnability and is not a packet defect.

---

## Other checks performed (all clean, no findings)

- **Blank-field mess event** (height, weight, eye/hair color, A-number):
  questionnaire leaves these blank with a "will send" note in email 0001;
  email 0002 supplies each value in numbered prose, in the voice the
  voice-card predicts, and the values match masterkey and rendered N-400
  exactly.
- **Password-protected attachment**: `Court Disposition - Certified
  Copy.pdf` opens cleanly with password `JakubMarzec2014`, given two lines
  below the attachment in the same email, exactly as `brief.md` describes.
  Decrypted text matches the masterkey's `documents.court_records` and the
  shipped `B-7` exhibit verbatim.
- **Voice consistency**: all four emails match `voice-card.md` — comma
  splices, greeting softening from "Dear Sir or Madam," to "Hello,", full
  name signed every time, numbered-list answers, the specific texture of
  giving detail (docket number) before being asked.
- **No-firm-identity rule**: confirmed by reading (cover letter and cover
  page carry no firm name/address/phone, signature block is the
  unattributed "Petition Preparer") and by inspecting file metadata — `pdfinfo`
  across every output PDF and `docProps/core.xml` in every output DOCX show
  no author, creator, company, or "last modified by" identity of any kind
  (blank fields, or generic tool names — `python-docx`, `mklib`, `anonymous`,
  `ReportLab`, `USCIS`). N-400 Part 11 (applicant's own phone/email) renders
  filled; Part 13 (preparer block) renders entirely blank; the applicant's
  signature line (Part 11 item 4, and Parts 15/16) renders blank — the form
  ships unsigned.
- **Document count / TOC / dividers**: 8 documents, TOC lists 8 lines in
  order, 8 numbered dividers ("DOCUMENT n / TITLE") all legible, well above
  12pt, none garbled elsewhere in the packet.
- **Look and feel elsewhere**: cover page, TOC, cover letter, passport bio
  page, green card front/back, and tax return page 1 all render cleanly with
  correct data and no visual defects. The court-records exhibit itself
  (`B-7`) is a plausible certified-copy layout — court name, docket, charge,
  disposition, judge, clerk certification, seal description — consistent
  with the corpus's born-digital design (no simulated scan).
- **Cross-document consistency spot-checks**: name/DOB/A-number/LPR date
  identical across cover page, cover letter, N-400, passport, green card;
  tax-return address matches N-400 address history; resume employers/dates
  match Part 7 and the masterkey; dependent SSN on Form 1040 matches
  masterkey.

---

## Summary for reviewers upstream

- **Verdict: PASS WITH FINDINGS**
- **Blocking: none.**
- **Should-fix (3):** Item 15.b table cell overflow (finding 1); stray box
  lattice over Item 5.b text on N-400 p.6 (finding 2); missing Part 14
  pointer for Item 20 (finding 3).
- **Note (2):** voice-card.md's coupling sample line, unshipped but
  contradicts brief.md (finding 4); masterkey-internal EAD-timing gap,
  invisible in the packet (finding 5).
- **C5/C6 independence: confirmed, with evidence, not blocking.**

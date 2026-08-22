# Phase 5 Layer-2 Review — adeyemi_tunde (T3)

**Verdict: PASS WITH FINDINGS. Nothing blocks.**

The brief's own blocking test is "an unlocatable fact is a broken test, not
a blemish." Every fact this client's masterkey needs is locatable in the
input: all five phone photos were opened and rendered, and every fact the
masterkey ties to a specific photo (LPR date on the green card's *back*
face specifically, A-number/E21 on the front, full passport MRZ, and the
complete court-record fact set) is legible on it; the password-protected
1040 was opened with the password from the correct later message. The input
is sufficient for a solver to build a correct packet from this folder alone.
By that criterion, nothing here blocks.

Two HIGH-severity rendering defects were found in the *output* packet — one
a gs-flatten-induced loss of visible content on the tax-return exhibit's
second page, the other a systemic text-overflow clip on the N-400 form
itself. Both are output-side rendering defects with zero effect on
solvability: every underlying fact is correct, present, and consistent
across input and output, and I traced each defect to its likely mechanism
below. This client's timeline, narrative, both negative controls, voice,
and no-firm-identity compliance all pass cleanly. The two rendering defects
should still be fixed before this packet is relied on as a filing reference
or a grading answer key, because they touch exactly the consistency-locked
facts (Item 15.b offense/place, tax-return page 2, Part 7 employer/
occupation) the set is built to test — a solver who reproduces the full,
correct strings would not visually match this reference on those fields.

---

## Findings

### Finding 1 — HIGH — tax-return page 2 loses its visible template content when gs flattens it
**File:** `output/N-400 Packet.pdf`, page 29 (= Tab B-6, "2025 Income Tax
Return," page 2 of 2). Reference for comparison: `output/Tab B (Biographical
Info)/B-6. 2025 Income Tax Return.pdf`, page 2 (standalone, as currently
shipped, renders fine).

Rendering the merged packet page 29 with `pdftoppm` produces a page that is
almost entirely blank: the teal header bar, the full black-ink instructional
text (line labels 11b–38, "Tax and Credits," "Payments and Refundable
Credits," "Refund," "Sign Here," "Paid Preparer Use Only," etc.) and the
cyan shading are all invisible. Only the blue filled-in values (AGI
131,800; total tax 15,240; refund 2,315 twice; "Bettina Wachtel, CPA") and a
few empty field-border boxes remain visible. The currently-shipped
standalone component file renders that same page correctly, in full.

**Isolated the mechanism:** I ran `merge_packet.py`'s own gs invocation
(`gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -dPreserveAnnots=false
-sOutputFile=... "B-6. 2025 Income Tax Return.pdf"`) against that one
component file alone, with nothing else in the argument list, and rendered
the result. Page 2 breaks identically, solo, with no other document present
to collide with. Page 1 of that same solo-flattened file renders correctly,
matching the asymmetry seen in the full merged packet (page 28 = 1040 p1,
fine; page 29 = 1040 p2, broken). This rules out a cross-document
`/Resources` collision from concatenation — the merge_packet.py docstring's
passport precedent (confirmed still fixed; see Confirmation below) does not
apply here. The mechanism is narrower: `gs ... -dPreserveAnnots=false`
itself strips whatever delivers page 2's visible template content on this
specific IRS-issued, JavaScript-bearing 1040 (`pdfinfo` shows `Form:
AcroForm`, `JavaScript: yes`) — almost certainly annotation/widget-borne
content that page 1 does not depend on in the same way. The currently
shipped standalone `B-6...pdf` was evidently produced by a different step
that does not strip this, which is why it looks fine until it goes through
`merge_packet.py`'s flatten.

Independent of mechanism, one part of this finding is solid on its own:
`merge_packet.py` asserts every merged page has `pdftotext` output of at
least 8 characters; page 29's *text layer* is fully intact (`pdftotext -f 29
-l 29` returns the entire label text, hundreds of characters — "Tax and
Credits 11b Amount from line 11a..." and so on), so the assertion passes
cleanly on a visually broken page. A length-of-extracted-text check cannot
see this class of bug, regardless of its cause.

**What to change:** for this component specifically, either pre-flatten or
rasterize the 1040 (or otherwise resolve its annotation-borne content)
*before* it enters `merge_packet.py`'s gs argument list, rather than relying
on the packet-wide flatten to handle it; and separately, extend the
post-merge check beyond "page has >= 8 extractable characters" — a
raster-diff against each component's own standalone render, or a
minimum-ink-coverage check per page, would catch this class of defect where
the passport-era text-length check cannot.

### Finding 2 — HIGH — text-overflow clipping in N-400 fixed-width fields
**File:** `output/Tab B (Biographical Info)/B-3. Form N-400, Application for
Naturalization.pdf` (confirmed present in the standalone component, and
therefore also in the merged packet — not a merge artifact).

Two locations, both reproduced at 300 dpi:

- **Part 9, Item 15.b arrest table** (page 8 of 14): the offense field
  prints `Operating a Motor Ve` (full string is "Operating a Motor Vehicle
  with a Suspended License") and the place-of-crime field prints
  `Fitchburg, Wisc` (full string "Fitchburg, Wisconsin, USA"), which runs
  directly into the adjoining disposition cell's `dismissed` with no visible
  column boundary — reads as `Wiscdismissed`.
- **Part 7, employment table** (page 5 of 14): the employer field prints
  `Cardinal Polymer` (full string "Cardinal Polymer Systems") and bleeds
  into the next column's `Fitchburg`; the occupation field prints `rocess
  Enginee` — clipped on **both** the leading and trailing edge (loses the
  "P" and the "r" of "Process Engineer"). I did not test the fill tool
  directly, so the exact anchoring mechanism (center-anchored text
  overflowing a too-narrow field, a field origin offset from the visible
  cell boundary, or something else) is inferred, not confirmed — what is
  confirmed is that the string is cut on both ends and the field draws no
  wrap or shrink-to-fit.

In both cases the full, correct string is present and legible elsewhere in
the same packet (the court-records exhibit for Item 15; the resume/employer
data for Part 7), so the underlying data is right — only the N-400's own
printed field is truncated. This matters more than ordinary cosmetics here
because the packet's own consistency locks require these exact strings to
"agree ... line for line" between the N-400 table and the supporting
exhibit; as rendered, the N-400 page does not actually display the full
string to agree with.

**What to change:** `lab/synthetic/tools/render_n400.py` fills these
AcroForm text fields with no wrap, shrink-to-fit, or truncation-with-ellipsis
logic. Add one, at least for the Item 15 table and the Part 7 employer/
occupation columns, which are the narrowest fields carrying the longest
client-supplied strings in the set.

### Finding 3 — MEDIUM — garbled double-printed "PRESENT" in Part 4
**File:** `output/Tab B (Biographical Info)/B-3. Form N-400, Application for
Naturalization.pdf`, page 3 of 14 (current-address block). Reproduced in
both the standalone component and the merged packet.

The "Dates of Residence: To (mm/dd/yyyy)" field for the current Fitchburg
address prints two overlapping renderings of the word "PRESENT" at
different weight/scale, reading as a garbled `PRESPRESENT`. Legible enough
to guess the intent, but visibly broken.

**What to change:** find and remove the duplicate paint of the "present"
flag in `render_n400.py`'s current-address block (likely a placeholder
"PRESENT" being drawn and then the actual value "PRESENT" drawn again on
top without clearing).

### Finding 4 — LOW — brief.md phrasing could mislead about Part 5 content (set-level, not blocking)
**File:** `lab/synthetic/clients/adeyemi_tunde/brief.md` ("Folake is in
N-400 Part 5 as a non-citizen spouse; Ayodele is in Part 6.")

The rendered N-400 correctly leaves Part 5 Items 4.a–8 (spouse's name, DOB,
marriage date, A-number, employer) blank, because the form's own routing
instruction ("If you are not filing under one of the categories above
[Spouse of U.S. Citizen / VAWA / etc.], skip to Part 6") applies — this
applicant files under 316(a)'s general provision, not as spouse of a USC.
The marriage is plainly stated via Item 1 (`Married`, checked) and Item 3
(`times married: 1`) alone, which is correct and is exactly the negative
control the client is built around. I confirmed this is correct behavior,
not a defect — flagging only because a future reader of brief.md could take
"Folake is in Part 5" to mean her name appears there, which it does not and
should not.

---

## Report back

**Verdict:** PASS WITH FINDINGS — two HIGH findings (rendering, not data),
one MEDIUM (cosmetic), one LOW (documentation ambiguity, informational).

**Password-protected 1040:** Opened successfully. `input/000010_.../
f1040_2025.pdf` is AES-256 encrypted (`pdfinfo` confirms). The password
`Cx7-Marlow-2025` arrives in `input/000012_2026-06-17_password/body.txt`,
two emails after the attachment (`000010`), exactly as the brief specifies
("escalated from W3, where the password was in the same message"). Opened
with `pdftotext -upw 'Cx7-Marlow-2025'` and `pdftoppm -upw ...`; confirms
Married Filing Jointly, Tunde/Folake, correct SSNs, address, AGI 131,800,
total tax 15,240, refund 2,315, preparer Bettina Wachtel CPA.

**Passport page text layer (already-fixed defect #1):** Confirmed fixed.
Page 24 of the merged `N-400 Packet.pdf` carries full, correct extractable
text, including both MRZ lines verbatim
(`P<NGAADEYEMI<<TUNDE<OLUSEGUN<<<<<<<<<<<<<<<<` /
`A048715627NGA8511098M2908111<<<<<<<<<<<<<<06`), matching the masterkey's
`documents.passport.mrz` exactly. Note, however, Finding 1 above: a
different page (the tax return's page 2) shows a visually similar symptom —
visible paint lost while the text layer survives — but I traced it to a
different, narrower mechanism (the packet-wide gs flatten stripping
annotation-borne content specific to that one IRS-issued AcroForm page, not
a cross-document `/Resources` collision from concatenation). The "already
fixed" defect is fixed for the passport specifically; it just isn't the
only way this pipeline can lose visible content while text survives, and
the safeguard written for the passport failure mode doesn't catch the
tax-return one either.

**Negative control 1 — married, no spouse passport:** Holds, and is well
executed. Part 5 Item 1 shows `Married` checked; Item 3 shows `1`. Items
4.a–8 (spouse detail) are correctly blank per the form's own routing
instruction, not omitted by the packet — I verified this is the N-400's
documented skip-to-Part-6 behavior for applicants not filing under
Spouse-of-USC/VAWA categories, so 316(a) applicants correctly never reach
those items regardless of marital status. No spouse passport, no C1/C2/C3
exhibit anywhere in the 8-document set, confirmed against both the exhibits
list and the rendered packet. The marriage is plainly stated; no spousal
evidence is requested or sent. This negative control is visible and
learnable as designed.

**Negative control 2 — C6 must not fire:** Holds, on both sides of the
input/output boundary. Input: email 000005 asks explicitly "Form N-400 Part
9 asks about arrests, citations, charges, and removal or deportation
proceedings. Please answer plainly..."; email 000006 answers with "All
other Part 9 questions: No" (a blanket covering Items 20–21 among others) —
an affirmative negative, not a silent absence. Output: rendered Item 20 and
Item 21 both show the `No` box marked (confirmed at 150dpi render, page 17);
Part 14 Additional Information (page 21) is entirely blank — no explanation
text anywhere near removal/deportation. The voice card's "do not write... any
explanation he was not asked for" reinforces why no such text would ever
appear. C6 does not fire, and nothing in the packet could lead a solver to
produce a written explanation.

**Voice — genuinely distinct:** Yes. Judged independently on this client's
own terms (not against Almeida, per instruction). The five emails from Tunde
Adeyemi are uniformly short (one to six lines), numbered to match the firm's
numbered questions with no restatement, no greeting beyond none, sign-off
either `TA` or nothing, zero hedging or apology language, and the arrest
disclosed in the same flat register as his height and weight ("Arrested
2023-06-24 in Fitchburg. Driving with a suspended licence. Dismissed
2023-09-12. I have the court paper. Photo attached."). This reads as
distinctly different in texture from a warmer or more discursive
correspondent — terse without ever crossing into curt or caricatured; each
message answers exactly what was asked and stops, consistent with the voice
card's own description. No exclamation marks, no ellipses, no filler
observed anywhere in the six-message thread.

**Look and feel:** Divider pages ("DOCUMENT 8 / COURT RECORDS" etc.) are
large, centered, legible serif type, well above 12pt. Input exhibits (all
five phone photos) render with a consistent "photo on a desk" treatment —
dark vignette/texture background, slight page-corner shadow — while every
fact on every one of them stays fully legible at 150dpi (checked passport
bio, green card front, green card back, court record, resume). Output
exhibit pages (passport/green card/tax return/travel addendum/court records
as they appear in the merged packet) are clean typeset transcriptions, not
styled as photographs — that is the pipeline's standard exhibit-rendering
choice, applies packet-wide, and is not a client-specific defect. Findings
1–3 above are the visually-broken items found.

**No-firm-identity rule:** Confirmed by direct inspection — rendered, not
just text-grepped, given Finding 1 shows this pipeline can lose visible
content while the text layer survives. Rendered page 1 (applicant cover
page: name, DOB, COB/CON, classification basis only, no firm anywhere) and
page 6 (cover letter, full body) of the merged packet at 150dpi: letterhead-
free, no firm name, no firm address, no firm phone, no firm email anywhere
on either page; sign-off is the bare, unattributed "Petition Preparer" with
no name. N-400 Part 11 (page 11 of 14) is filled with the applicant's own
phone numbers and his personal email `tunde.adeyemi@quillmail.com`
(correctly not the work address he emailed from mid-thread). Part 13
preparer block (page 12) is completely blank — no name, no business name,
no phone, no email, unsigned. The N-400's own signature line (Part 11 Item
4) is blank/undated — unsigned as required. Also grepped the full
merged-packet extracted text for `brightpost`/`casework@` (the firm's
input-side email) — zero hits. No firm-identifying content found anywhere
in the output.

**Any other blocking finding in full:** None. Nothing in this review blocks,
by the brief's own test ("an unlocatable fact is a broken test"). All five
input phone photos (passport bio, green card front, green card back, court
record, resume) were opened and every fact claimed to live only on that
photo (per `input_surfaces` in the masterkey) was independently confirmed
legible: LPR date on the green card back face specifically (not the front),
A-number/E21/DOB/COB on the front, full MRZ and passport data on the
passport photo, and the complete court-record fact set (police case number,
docket, statute, offense, plea, disposition, disposition date, judge,
clerk, certification date, seal) on the single court-record photo. Nothing
here is unlocatable; this stress-test client's input is sufficient for a
solver to build a correct packet from. Findings 1–2 are HIGH severity as
rendering defects in the reference output — worth fixing before this packet
is used as a filing or grading reference — but neither withholds or
obscures a fact a solver needs; both are treated as non-blocking for that
reason.

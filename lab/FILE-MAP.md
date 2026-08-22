# FILE-MAP — the reference corpus for challenge one

Synthesised from 25 runner reports (5 lenses x 5 client matter folders).
Individual reports live in `lab/reports/`. Decisions live in `lab/NOTES.md`.

Lenses per folder: manifest · packet anatomy · form field provenance ·
intake chronology · exhibit origin.

---

## 1. WHAT IS ACTUALLY IN `lab/`

| folder | files | span | matter | packet? |
|---|---|---|---|---|
| jacobs_brent | 423 | 2015-2025 | N-400 for Lauren Rae Garth (INA 319 spousal) | yes, flat, unmerged |
| zhu_vivian | 383 | 2020-2025 | N-400 for Xuying Zhu (INA 316(a)) | yes, tabbed, merged |
| izaguirre_jesus | 103 | 2021-2022 | N-400 for Jesus Antonio Izaguirre Paz (INA 316) | yes, indexed, unmerged |
| malone_kyle | 188 | 2020-2025 | TWO N-400s: Luwilyn Malone (319, 3-yr), David Braun (316, 5-yr) | two packets |
| ossola_ylenia | 36 | 2021-2025 | N-400 for Ylenia Ossola (INA 319 spousal, 3-yr) | yes, flat 0-12, unmerged |

Every .pdf, .docx and .xlsx has a `<name>.<ext>.txt` sidecar with extracted
text (174 PDFs, 37 office files; all PDFs had a text layer).

### Traps
- **A folder name does not name the applicant.** `jacobs_brent` is the US
  citizen husband; the applicant is his wife. `malone_kyle` is the US citizen
  sponsor; the applicants are his wife and stepson. `ossola_ylenia` is the
  petitioner; the beneficiaries are her parents. Three of five.
- **`ossola_ylenia` IS an N-400 matter** — corrected on a second pass; an
  earlier truncated copy made three reports say otherwise. Its `7-sprint/`
  wrapper is prior AGENT work from 2026-06 (README/DIARY say so outright); the
  `.md` files beside each document are agent extractions, and most are stubs.
  The packet itself is genuine firm output from 2022.
- Matter folders accumulate unrelated material: a $100k promissory note with
  share collateral (izaguirre), a Minnesota power of attorney and an LLC
  formation (malone), a sibling's visa enquiry (ossola).

---

## 2. THE HOUSE STYLE IS A FAMILY, NOT A SINGLE FORM

Four generations of the same skeleton. The firm builds each packet by copying
the last one — `luwilyn_cover_letter_example.pdf` and `index_example.pdf` sit
inside David Braun's folder as templates. That copying is the transmission
mechanism, and it is why the style drifts.

| | malone/Luwilyn 2020 | malone/Braun 2021 | ossola 2022 | izaguirre 2022 | zhu 2024 | jacobs 2025 |
|---|---|---|---|---|---|---|
| heading | INDEX OF DOCUMENTS | INDEX OF DOCUMENTS | INDEX OF DOCUMENTS | INDEX OF DOCUMENTS | TABLE OF CONTENTS | TABLE OF CONTENTS |
| structure | flat 1-6 | flat 2-6 | flat 0-12 | flat 0-7 + a-g | TAB A / TAB B | flat 0-4 |
| merged PDF | YES | no | no | no | YES | no |
| lockbox | Chicago | Chicago | Chicago (Box 4380) | Lewisville TX | Dallas | Chicago |
| carrier | FedEx | FedEx | FedEx | FedEx | USPS | FedEx |
| letterhead | 26 Broadway Fl 8 | 31 Hudson Yards Fl 11 | none on letter | (SYMPLE) | — | — |
| signature | Marcel S. Oliveira, J.D. / Petition Preparer | same | Marcel S. Oliveira / Petition Preparer | SYMPLE / By: Marcel S. Oliveira / Petition Preparer / MSO / Encls. | Sincerely, SYMPLE / By: Marcel Oliveira / Petition Preparer | (not extracted) |
| cover page | no | no | no | no | YES, w/ Classification Basis | no |
| doc dividers | no | no | no | no | DOCUMENT n | DOCUMENT n |

### The invariant core — present in all four packets
1. An index or table of contents, headed by applicant name, DOB, COB/CON.
2. A cover letter to a USCIS lockbox.
3. The N-400.
4. A green card copy.
5. A passport bio page.

### The cover-letter template, recovered
```
{LETTERHEAD}

{DATE, written in full}

VIA {CARRIER}

Department of Homeland Security
United States Citizenship and Immigration Services
{LOCKBOX BLOCK}

       Re:     Form N-400, Application for Naturalization
               Applicant: {TITLE} {FULL NAME}
               COB/COC: {COUNTRY}

To Whom It May Concern:

       Enclosed please find one (1) Form N-400, Application for Naturalization,
along with the accompanying filing fee and supporting documentation, for
{TITLE} {FULL NAME}. {TITLE} {SURNAME} is eligible for naturalization pursuant
to {ELIGIBILITY CLAUSE}. See {CITATION}.

      Please note that the enclosed packet contains photocopies of certain
documents. {TITLE} {SURNAME} understands that, in the future, {PRONOUN} may
need to present original versions of any such documents to an official.

       Thank you for your time and attention.

                                                 Sincerely,

                                                 {SIGNATURE BLOCK}
```
Eligibility clause variants actually observed:
- "having three (3) years of permanent residency combined with continuous
  residence with her U.S. citizen spouse, Mr. {NAME}" — cite 8 C.F.R. § 319.1
- "having five (5) years of permanent residency" — cite 8 C.F.R. § 319.1
- "following more than five (5) calendar years of continuous permanent
  residency in the United States" — no citation
- jacobs 2025 argues INA § 319 citing 8 U.S.C. § 1430(a) and 8 CFR § 319.1(a)

---

## 3. HOW INPUT BECOMES OUTPUT — the four-category rule

Confirmed independently on five matters, and shown to hold on non-N-400 forms.

**A. ID documents supply identity.** Passport bio page and green card give:
legal name, DOB, sex, country of birth, country of citizenship, A-number, LPR
date, and the Part 3 physical descriptors.

**B. The questionnaire and resume supply history.** Address history with
dates, employment history, trips outside the US, marital and spouse details,
children, contact details, and every moral-character answer. Where a resume
exists, Part 7 employment matches it exactly.

**C. The firm derives.** Filing basis from marital status and spouse
citizenship. Continuous-residence dates from the LPR date. Prior-address date
ranges interpolated from employment history. Travel addenda compiled and
trimmed from a wider client-supplied list.

**D. The firm supplies.** Preparer block, firm address, G-28/G-1145/G-1450,
letterhead, the index, the cover letter, the cover pages.

### Cross-document consistency locks
From `ossola_ylenia/9-sprint/ds260-masterkey-*.yaml`, and corroborated
everywhere else:
- surname and given name must match the petition and the passport MRZ exactly
- DOB equal across every document that carries it
- place of birth city and country must match across petition and birth record
- receipt numbers must reconcile against the corresponding notice
- the tax return address must appear in the address history
- resume employers and dates must equal Part 7
- the travel addendum must be a superset of the form's travel part
- the green card supplies the A-number and LPR date, which drive the
  continuous-residence computation

### The exhibit set is a FUNCTION of two things
`exhibits = f(eligibility basis, moral-character answers)`
- INA 319 spousal -> add the US citizen spouse's passport bio page; drop
  nothing else.
- INA 316 five-year -> no spousal evidence at all.
- One "Yes" on removal proceedings dragged SEVEN exhibits plus a Written
  Explanation into the izaguirre packet.
- An arrest history produced a Court Records tab in zhu.
- Extensive travel produced a Travel Addendum in zhu and an .xlsx addendum in
  izaguirre.
Everything beyond the invariant core is conditional, and the condition is
always traceable to a form answer.

### TRANSCRIPTION IS LOSSY — the finding that matters most
`malone_kyle` preserves a completed questionnaire beside the filed N-400, so
the transcription can be audited directly:

| questionnaire | N-400 as filed |
|---|---|
| Malone | "Ma Lone" |
| 917 E 10th St | 917 E 16th St |
| apt #301 | apt #391 |
| 5 addresses with dates | 4, dates mostly blank |
| 5 employers with dates | 3, dates blank |
| 5 children | 4 |
| height, weight, hair, eyes | all blank |

Compare "Comerio" rendered "Commerico" on the ossola I-824. Compare the jacobs
2025 thread where middle names sat in First Name boxes and the email address
was stale. **The output is not a faithful function of the input.** Whether the
three synthetic pairs should be clean or should carry deliberate loss is the
first question the plan must answer.

---

## 4. WHAT INPUT LOOKS LIKE WHEN IT ARRIVES

### The intake questionnaire evolved
**2021, Airtable** (izaguirre — full text in `reports/izaguirre_jesus--intake-chronology.md`): ten items. Green card front and back; passport bio page;
driver's licence front and back; three years of 1040s; desired name change;
address history since the green card; job history since the green card; trips
since the green card; marriage since the green card; children since the green
card. Anchored throughout on the phrase "since you received your green card".
Contains the firm's own typo, "the approximate month/year the job stated".

**2024, Jotform/docx** (zhu — full text in `reports/zhu_vivian--intake-chronology.md`): tightened. Address plus move-in date; other citizenships;
five years of trips; marital status; spouse details. Documents reduced to
four: resume, first two pages of the 1040, passport bio page, green card.
Drops the driver's licence and the name-change question; adds other
citizenships. Preamble worth quoting: "if you do not have all answers, or all
documents, that is not a problem. Just provide what you have."

**2025, Airtable** (jacobs): shortened per matter — "we went through it and
cut the questions that we know we can already answer--and whose answers have
not changed--from the old green card paperwork."

**DS-260** (ossola): 25 pages, including social media handles and every
address since age 16. Same discipline, an order of magnitude more surface.

### The recurring failure modes
- The hardest fields come back BLANK. Izaguirre left addresses, employment and
  trips empty; the trips arrived months later as a separate 56-row Excel.
- Documents arrive as phone photos, on wooden desks. Green cards, receipt
  notices, everything.
- A tax return arrives password-protected with no password. The firm chases;
  the client answers a different question.
- Corrections come back as EMAIL PROSE WITH SCREENSHOTS, never as a corrected
  form.
- The CLIENT catches the firm's errors, not the reverse.
- Delivery friction: a file too large to email, moved to Drive; a client who
  wants a print-and-scan to avoid "PDF glitches or omissions"; an e-signature
  that will not work on a phone.
- The client over-delivers unrequested documents "just in case".
- Multiple email addresses used inconsistently by the same client.
- Long silences, then sudden urgency.
- Sometimes a relative does all the corresponding and the applicant barely
  appears at all.

### Five client voices, all quotable in the reports
1. **Australian couple** (jacobs) — warm, apologetic, chatty, catches errors,
   "Just checking in", "Have a great day!", occasional typos.
2. **Chinese professional** (zhu) — terse, returns the form fast but thin,
   impatient by December, profane by June: "This is a bitch gov."
3. **Mexican professional** (izaguirre) — fluent, slightly non-native syntax,
   comma splices, "Best regards, Jesus", leaves hard fields blank.
4. **Filipina applicant via a US relative** (malone) — deferential, short,
   technically blocked; "I tried e-signature but it won't have to my phone."
   The US relative writes for her, verbose and solution-oriented.
5. **Italian-American** (ossola) — warm, over-delivering, self-doubting,
   asks permission rather than asserting, "Thank you so much, / Ylenia".

---

## 5. INPUT/OUTPUT DISCERNMENT — the hard problem, quantified

Traceability = the fraction of packet exhibits that can be traced back to an
arrival event (an email, an intake upload).

| matter | rate | why |
|---|---|---|
| ossola_ylenia | ~100% | every document has a covering email naming it |
| zhu_vivian | high | phone photos in `Others/`, Jotform submission |
| malone_kyle | ~15% | only USCIS's own AR-11 confirmations survive |
| izaguirre_jesus | ~11% | exhibits inherited from a prior file, some by FOIA |
| jacobs_brent | 0% | green card and passport exist only inside the packet |

**There is no reliable link from an output document back to its arrival.** Any
approach that assumes one will fail on three matters out of five. Classification
must rest on the document's own character — who issued it, whose signature is
on it, whether it is a form or a scan — not on where it sits or how it arrived.

### The reliable signals
- **Folder names, where they exist.** `Deliverables/` vs `Intake/`
  (izaguirre) is the cleanest split in the corpus; `Packet/`, `Final Packet/`,
  `Tab A`/`Tab B` are strong. But two of five matters have no such split.
- **Numeric and letter prefixes** encode packet order reliably.
- **The index is the firm's INTENT; the folder is what survived.** They differ.
  Luwilyn's G-1145 is on disk but in neither the index nor the merged PDF;
  David's index lists seven items against five files; zhu's TOC promises a
  G-1450 that does not exist. Prefer the index when reconstructing what a
  packet is meant to be.
- Working `.docx`/`.jpg` beside a normalised `.pdf` of the same name means
  draft vs filed.
- `(Updated)`, `(Second Update)`, `Compressed`, `_Signed`, `_Original Copy`
  mark revision state.

---

## 6. IMPLICATIONS FOR THE SYNTHETIC BUILD

Recorded as observations, not decisions. The decisions belong to the plan.

1. The prompt promises "merged into one PDF". Only two of six packets are
   merged (zhu 2024, malone/Luwilyn 2020). If the synthetic outputs must be
   merged, they follow zhu.
2. The prompt promises consistent output. The corpus is not consistent. The
   synthetic three must be MORE uniform than anything the firm actually did —
   which is the stated reason for picking jacobs and zhu as the two sources.
3. jacobs and zhu diverge on nearly every axis. Choosing the mix is a design
   act, not an extraction.
4. Six synthetic clients need six distinct eligibility profiles, because the
   exhibit set is a function of the basis. At minimum one 319 spousal, one 316
   five-year, and one with a complicating answer that drags exhibits in.
5. Five client voices are documented with quotes; six clients need a sixth or
   a reuse.
6. The three input-only clients should follow the ossola shape: material
   received, holes documented, nothing produced.
7. Every fact must be invented, and the consistency locks in section 3 must
   hold across each client's whole document set, or the challenge is
   unsolvable by the plugin it is meant to test.

---

## 7. CORRECTION — ossola_ylenia, added after a second pass

The first pass reviewed a truncated copy and reported no packet. Wrong. Five
corrective runners re-ran the same five lenses. What changed:

### It is a fifth reference packet, and the best-documented one
Ylenia Ossola, Italian, LPR 2019-06-20 via marriage, N-400 filed 2022-03-20 on
the three-year spousal basis. Flat numbering `0. Index` through
`12. Child Passport`, izaguirre generation, Chicago lockbox, no merge.
A complete field-level provenance map now exists in
`reports/ossola_ylenia--n400-provenance.md` — every Part, every value, every
source. **Use it as the worked example when specifying the synthetic pairs.**

### Two document types nothing else in the corpus has
1. **A supplemental cover letter.** `Cover Letter with Greencard.docx`, dated
   2023-01-30, ten months after filing, enclosing the unconditional green card
   once the I-751 was approved. Its RE: block carries a CASE NUMBER rather than
   a form name. A mid-flight addition to a live application.
2. **An I-751 receipt bound in as an exhibit.** `7. I-797C` proves she held
   valid LPR status while the removal-of-conditions petition was pending. New
   rule: a conditional resident naturalising before the unconditional card
   arrives must evidence the gap.

### Bona fide marriage evidence inside a naturalization packet
Spouse's passport, joint residential deed, joint auto policy, child's passport.
None is a standard N-400 exhibit. The firm carries I-751-style proof forward.

### A new cover-letter variant
The RE: block substitutes a `Basis:` line ("Three-Year Continuous Residence")
for the DOB and COB/CON every other matter uses. No statutory citation at all.
Closing inverts izaguirre's phrasing: "favorable and speedy" vs "speedy and
favorable". Contains the firm's own malapropism, "receival".

### Soft inconsistencies to imitate
- Three dates for one filing: cover letter 2022-03-20, signature on the filed
  form 8/16/22, a replacement signature page 2022-11-14.
- Continuous residence is 2y9m against a 3-year requirement on its face.
- No intake questionnaire at all for this N-400 — the firm reused what it held
  from the earlier I-751 matter. Returning clients get no fresh intake.

### A correction to my own tooling claim
54 of 185 PDFs across the corpus are image-only scans with no text layer,
including this matter's N-400. Their `.txt` sidecars now say so explicitly.
The provenance runner recovered the full field map by reading the scan
visually — **any agent working this corpus must read scanned PDFs as images,
not rely on sidecars.**

### Proper nouns from scans are unreliable
Two runners read the deed preparer as both "Nery & Richardson LLC" and
"Griffin & Gallagher", the tax preparer as both "Coconautsand LLC" and "DLC
Tax Services and Accounting Inc". Immaterial — every such name is invented in
the synthetic set — but a caution against trusting OCR'd proper nouns.

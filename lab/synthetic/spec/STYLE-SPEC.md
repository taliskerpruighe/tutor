# STYLE-SPEC — the frozen house style for the six synthetic packets

*Phase 1 of `lab/BUILD-PLAN.md`. Written 2026-08-21 by the one corpus-exposed
agent. **This document replaces the corpus.** From here on no content-side
agent reads `lab/<client>/` again: every renderer, template and verifier works
from this file, the templates beside it, and the masterkeys.*

**Status: awaiting user sign-off (BUILD-PLAN §2 barrier).** The taste calls are
numbered in §14; the plan's own errors are in §13.

---

## 0. SOURCES OF AUTHORITY

Every claim below cites the file it was read from. Paths are relative to
`lab/`. Where two sources disagree the choice is recorded as a taste call.

| short name | file | what it settles |
|---|---|---|
| **zhu/merged** | `zhu_vivian/N-400 Naturalization/Zhu, Vivian/Others/(Second Update) N-400 Packet.pdf` (64 pp, 0 form fields) | packet structure, cover pages, dividers, page geometry |
| **zhu/TOC** | `.../Tab A (Content + Cover)/A-1. Table of Contents.docx` | TOC wording, list numbering, character formatting |
| **zhu/letter** | `.../Tab A (Content + Cover)/A-2. Cover Letter.docx` | cover-letter body, closing, signature block |
| **zhu/divider** | `.../Tab A (Content + Cover)/A-1.pdf`, `A-2.pdf` | divider page layout |
| **zhu/N-400** | `.../Tab B (Biographical Info)/B-4. N-400, Application for Naturalization_Signed.pdf` (14 pp, 414 fields, 277 filled) | which N-400 fields the firm actually fills |
| **zhu/addendum** | `.../Tab B (Biographical Info)/B-8. Travel Addendum.pdf` | travel-addendum layout and wording |
| **zhu/courts** | `.../Tab B (Biographical Info)/B-9. Court Records.pdf` (image-only; read visually) | court-records exhibit shape |
| **jacobs/TOC** | `jacobs_brent/Packet/0. Table of Contents.docx` | applicant cover-page block |
| **jacobs/letter** | `jacobs_brent/Packet/1. Cover Letter.docx` | date line, Re: block, statutory citation |
| **jacobs/dividers** | `jacobs_brent/Packet/Cover Pages.docx` | divider wording, 12 pt variant |
| **jacobs/N-400** | `jacobs_brent/Packet/2. N-400.pdf` (image-only; read visually) | edition 01/20/25, print-and-scan generation |
| **ossola/exhibits** | `reports/ossola_ylenia--exhibit-origin.md` | the situational exhibit branches |
| **ossola/provenance** | `reports/ossola_ylenia--n400-provenance.md` | the completeness benchmark for §12 |
| **live/lockbox** | uscis.gov, *Direct Filing Addresses for Form N-400*, fetched 2026-08-21 (page last reviewed 01/24/2025) | §7 lockbox table |
| **live/blanks** | `lab/synthetic/blanks/n-400.pdf`, `f1040.pdf`, `f1040--2024.pdf` | committed blank forms |

Rejected as format sources by `lab/NOTES.md`: `izaguirre_jesus`, `malone_kyle`,
`ossola_ylenia`. They are cited here only for *rules* (exhibit triggers,
provenance), never for wording or layout.

---

## 1. THE PACKET, IN ONE PARAGRAPH

One flattened PDF, letter portrait, preceded by an applicant cover page, split
into two tabs. **TAB A** carries the firm's own summary documents (table of
contents, cover letter); **TAB B** carries everything biographical, beginning
with the N-400. Each document is introduced by a one-page divider reading
`DOCUMENT n` over the document's title. Numbering runs continuously from 1
through the last document, across the tab boundary. Every firm-authored page
is Times New Roman. The same components also ship loose, numbered, as docx and
pdf. Source: zhu/merged.

---

## 2. THE OUTPUT FOLDER

```
<client_slug>/output/
  00. Applicant Cover Page.docx          <- INVENTED NAME, see §13 D9
  00. Applicant Cover Page.pdf
  Tab A (Content + Cover)/
    A-0. Tab Cover Page.docx  / .pdf     <- INVENTED NAME, see §13 D9
    A-1.pdf                              <- DIVIDER for document 1
    A-1. Table of Contents.docx / .pdf   <- CONTENT of document 1
    A-2.pdf                              <- DIVIDER for document 2
    A-2. Cover Letter.docx / .pdf        <- CONTENT of document 2
  Tab B (Biographical Info)/
    B-0. Tab Cover Page.docx  / .pdf     <- INVENTED NAME, see §13 D9
    B-3.pdf
    B-3. Form N-400, Application for Naturalization.pdf
    B-4.pdf
    B-4. Bio Page of Passport.pdf
    ...                                  <- one pair per document, §8
  N-400 Packet.pdf                       <- merged and flattened, 0 fields
```

Folder names `Tab A (Content + Cover)` and `Tab B (Biographical Info)` are
verbatim zhu (zhu/merged tree). So is the merged file's stem, `N-400 Packet`
(zhu's copies are `(Updated) N-400 Packet.pdf`, `(Second Update) …`,
`Compressed …`; the synthetic build ships one clean copy with no revision
marker — taste call 12).

**The naming collision, stated loudly because a renderer will get it wrong.**
In zhu's tree the *bare* numbered PDF is the **divider**, and the file with a
title after the number is the **content**:

```
A-1.pdf                      = the page reading "DOCUMENT 1 / TABLE OF CONTENTS"
A-1. Table of Contents.docx  = the table of contents itself
```

Confirmed by page count and text: `A-1.pdf` is 1 page reading `DOCUMENT 1` /
`TABLE OF CONTENTS`; `B-4.pdf` is 1 page reading `DOCUMENT 4` / `FORM N-400`
while `B-4. N-400, Application for Naturalization_Signed.pdf` is the 14-page
form. **Merge order is taken from the TOC, never from a directory sort** —
alphabetically `A-1. Table of Contents.docx` sorts *before* `A-1.pdf`.

The file number equals the DOCUMENT number: zhu's N-400 is document 4 and is
filed as `B-4`. With G-1450 dropped (§10) the N-400 becomes document 3, so it
is filed as `B-3`. Tab A always holds documents 1 and 2.

**Both layers ship.** Loose numbered components (docx *and* pdf for
firm-authored documents; pdf only for forms and exhibits) *and* the merged
`N-400 Packet.pdf`. BUILD-PLAN §2: "Teaches both layers."

### 2.1 Component file name per document

Frozen so that no later agent has to guess — and so that nobody inherits zhu's
own inconsistency. zhu's real exhibit components carry the client's file names
through unchanged (`B-5. Bio Page of New Passport.jpg` — a JPEG, not a PDF;
`B-7. 2023 COMPLETE Fed ITR - Xuying Zhu v2_unlocked.pdf`). **Normalised here:
every shipped component is a PDF, and its name is the document's title.**

| DOC | divider file | content file |
|---|---|---|
| — | — | `00. Applicant Cover Page.docx` + `.pdf` |
| — | — | `Tab A (Content + Cover)/A-0. Tab Cover Page.docx` + `.pdf` |
| 1 | `A-1.pdf` | `A-1. Table of Contents.docx` + `.pdf` |
| 2 | `A-2.pdf` | `A-2. Cover Letter.docx` + `.pdf` |
| — | — | `Tab B (Biographical Info)/B-0. Tab Cover Page.docx` + `.pdf` |
| 3 | `B-3.pdf` | `B-3. Form N-400, Application for Naturalization.pdf` |
| 4 | `B-4.pdf` | `B-4. Bio Page of Passport.pdf` |
| 5 | `B-5.pdf` | `B-5. Permanent Resident Card.pdf` |
| 6 | `B-6.pdf` | `B-6. {YEAR} Income Tax Return.pdf` |
| C1 | `B-n.pdf` | `B-n. Bio Page of Spouse Passport.pdf` |
| C2 | `B-n.pdf` | `B-n. Form I-797C, Notice of Action.pdf` |
| C3a | `B-n.pdf` | `B-n. Joint Deed.pdf` |
| C3b | `B-n.pdf` | `B-n. Joint Automobile Policy.pdf` |
| C3c | `B-n.pdf` | `B-n. Bio Page of Child Passport.pdf` |
| C4 | `B-n.pdf` | `B-n. Travel Addendum.docx` + `.pdf` |
| C5 | `B-n.pdf` | `B-n. Court Records.pdf` |
| C6 | `B-n.pdf` | `B-n. Written Explanation.docx` + `.pdf` |

`{YEAR}` is the tax year. `n` is the DOCUMENT number the exhibit rule (§9.2)
assigns; the C-codes are trigger ids, not file names. The travel addendum and
the written explanation are firm-authored, so they ship as docx + pdf like the
other firm pages.

---

## 3. TYPOGRAPHY

Frozen for every firm-authored page.

| property | value | source |
|---|---|---|
| page | US Letter, 12240 × 15840 twips, portrait | zhu/TOC, zhu/letter, jacobs/* `sectPr` |
| margins | 1 inch all four sides (1440 twips) | same |
| face | **Times New Roman** (`w:rFonts` ascii/hAnsi/eastAsia/cs) | zhu/TOC runs; jacobs/dividers runs |
| body size | **12 pt** (`w:sz w:val="24"`) | zhu/TOC, zhu/letter, jacobs/* |
| line spacing | **1.15** (`w:spacing w:line="276" w:lineRule="auto"`) — renders as 15.87 pt leading at 12 pt, measured 15.84 pt in zhu/merged p.4 | zhu/TOC docDefaults |
| paragraph gaps | an **empty paragraph**, never `spacing after` — the corpus separates every block with a blank paragraph | zhu/TOC, zhu/letter |
| cover-letter body | **justified** (`w:jc w:val="both"` in docDefaults) | zhu/letter, jacobs/letter |
| cover-letter first line | **no** first-line indent | zhu/letter (no `w:ind` on body paragraphs) |
| tab cover pages | 24.0 pt (measured 26.57 pt glyph box ÷ 1.107) | zhu/merged pp. 2, 7 |
| dividers | **24 pt** — taste call 3; the corpus drifts 19.9 / 22.1 / 23.0 pt across zhu's own dividers and sits at 12 pt in jacobs/dividers | measured, zhu/merged pp. 3, 5, 8, 10, 25, 27, 30, 61, 63 |

**Plain paragraphs only. No text boxes, no tables, no headers, no footers, no
page numbers, no shapes, no images in firm-authored docx.** The reason usually
given (FILE-MAP §2, BUILD-PLAN §2) is that the firm's letterheads lived in
text boxes and converters lose them. That reason is *half* right and the
correction is in §13 D3: the only text-box document in the whole corpus is
`malone_kyle/Braun, David/Cover letters/Cover Letter.docx` (24 `txbxContent`
elements). The rule stands anyway — `soffice --headless --convert-to pdf` is
the only converter in the toolchain and text-box fidelity is exactly what it
risks. Cost of the rule: none, because the frozen style has no element that
needs one.

**Alignment vocabulary.** Only three alignments occur: `center` (cover-page and
document titles), `left` (default), `both` (cover-letter body paragraphs).
Underline (`w:u val="single"`) and bold (`w:b`) are the only character
decorations. No italics anywhere in a firm-authored page.

---

## 4. LITERAL STRINGS — THE PAGES THE FIRM WRITES

Everything in `{braces}` is a slot. Everything else is literal and is quoted
from the file named.

### 4.1 Applicant cover page — `00. Applicant Cover Page`

Source: zhu/merged p. 1 (measured: 12 pt throughout, title centred and
underlined with a rule at y 706.57 spanning x 201.59–411.59, body left at
x 72.47). The block wording is also jacobs/TOC paragraphs 0–6, where it sits at
the head of the table of contents instead of on its own page.

```
                    APPLICATION FOR NATURALIZATION          <- centred, underlined
                                                            <- blank
                                                            <- blank
APPLICANT:                                                  <- left
                                                            <- blank
{HONORIFIC} {FULL LEGAL NAME}
DOB: {MM/DD/YYYY}
COB/CON: {COUNTRY}
                                                            <- blank
Classification Basis: {INA 316(a)|INA 319(a)}
```

- `APPLICATION FOR NATURALIZATION`, `APPLICANT:`, `DOB:`, `COB/CON:`,
  `Classification Basis:` are literal, exactly as spelled — note `COB/CON`
  (country of birth / country of nationality), not `COB/COC`.
- Name style: zhu/merged p. 1 uses `Ms. Xuying Zhu` (mixed case, honorific);
  jacobs/TOC uses `LAUREN RAE GARTH` (all caps, no honorific). **Taste call 1:
  zhu.** Mixed case with honorific.
- `Classification Basis:` exists only in zhu. It is the packet's one-line
  statement of the eligibility basis and it is the reason zhu is the structural
  model. Values: `INA 316(a)` or `INA 319(a)` — nothing else.

### 4.2 Tab cover page — `A-0. Tab Cover Page`, `B-0. Tab Cover Page`

Source: zhu/merged pp. 2 and 7 (24.0 pt; line 1 Times New Roman **Bold**, line
2 regular; both centred; line 1 top at y 73.41 = the 1-inch margin; line 2 top
at y 136.77, i.e. one blank line between).

```
                              TAB A                    <- bold, centred, 24 pt
                                                       <- blank
                           SUMMARIES                   <- regular, centred, 24 pt
```
```
                              TAB B                    <- bold, centred, 24 pt
                                                       <- blank
                          BIOGRAPHICAL                 <- regular, centred, 24 pt
```

`SUMMARIES` and `BIOGRAPHICAL` are exactly what the pages say — **not**
"Summary" and "Biographical Information", which is what the TOC says about the
same two tabs. Both strings are kept (taste call 2; alternative in §13 D5).

### 4.3 Document divider — `A-n.pdf` / `B-n.pdf`

Source: zhu/divider (content stream: `/F4` = TimesNewRomanPS-**Bold**MT for
line 1, `/F5` = TimesNewRomanPSMT for line 2; both lines whole-line centred at
x 306.0; line 1 top at the 1-inch margin, one blank line, line 2) and
jacobs/dividers (same two-line shape, same bold/regular split, 12 pt).

```
                          DOCUMENT {n}                 <- bold, centred, 24 pt
                                                       <- blank
                          {TITLE, ALL CAPS}            <- regular, centred, 24 pt
```

Divider titles, verbatim from the corpus where the corpus has them, and set by
the same rule (screaming caps, no `Form` prefix, no punctuation) where it does
not:

| document | divider title | attested |
|---|---|---|
| table of contents | `TABLE OF CONTENTS` | zhu/divider `A-1.pdf`; jacobs/dividers |
| cover letter | `COVER LETTER` | zhu/divider `A-2.pdf`; jacobs/dividers |
| N-400 | `FORM N-400` | zhu/merged p. 10; jacobs/dividers |
| applicant passport | `PASSPORT` | zhu/merged p. 25 |
| green card | `GREEN CARD` | zhu/merged p. 27; jacobs/dividers has `PERMANENT RESIDENT CARD` — taste call 4 chooses zhu |
| tax return | `{YEAR} INCOME TAX RETURN` | zhu/merged p. 30 (`2023 INCOME TAX RETURN`) |
| travel addendum | `TRAVEL ADDENDUM` | zhu/merged p. 61 |
| court records | `COURT RECORDS` | zhu/merged p. 63 |
| spouse's passport | `SPOUSE'S PASSPORT` | **set here** — no divider exists in a corpus spousal packet (ossola's generation had none) |
| I-751 receipt | `FORM I-797C, NOTICE OF ACTION` | **set here**, from ossola's exhibit name `7. I-797C` |
| joint deed | `JOINT DEED` | **set here**, from ossola exhibit `10. Joint Deed` |
| joint auto policy | `JOINT AUTOMOBILE POLICY` | **set here**, from ossola exhibit `11` |
| child's passport | `CHILD'S PASSPORT` | **set here**, from ossola exhibit `12. Child Passport` |
| written explanation | `WRITTEN EXPLANATION` | **set here**, from izaguirre's exhibit name |

### 4.4 Table of contents — `A-1. Table of Contents.docx`

Source: zhu/TOC (XML read directly) and zhu/merged p. 4 (geometry: title top
y 72.51; every subsequent line 31.74 pt apart, i.e. a blank paragraph between
every line; list numbers at x 90.0 = 0.25" indent; list text at x 108.0 = 0.5").

```
                        TABLE OF CONTENTS         <- centred, BOLD + UNDERLINE, 12 pt
                                                  <- blank
    Tab A (Summary)                               <- bold, indent 0.25"
                                                  <- blank
    1.  {TAB A ITEM}                              <- numbered list, number 0.25", text 0.5"
                                                  <- blank
    2.  {TAB A ITEM}
                                                  <- blank
    Tab B (Biographical Information)              <- bold, indent 0.25"
                                                  <- blank
    3.  {TAB B ITEM}
                                                  <- blank
    ...
```

- Heading is `TABLE OF CONTENTS`, bold **and** underlined, centred. `INDEX OF
  DOCUMENTS` is rejected (§10).
- Tab headings are `Tab A (Summary)` and `Tab B (Biographical Information)` —
  bold, sentence case, in parentheses, left-indented 0.25", **not numbered**.
- Items are a single Word numbered list (`numId 1`, `ilvl 0`,
  `ind left=720 hanging=360`) that **runs continuously across the Tab B
  heading** — the heading interrupts the layout, not the numbering. The list
  number is the DOCUMENT number.
- Item text is sentence case, except that form names keep their own case.
  Attested item strings, verbatim from zhu/TOC:

| # | TOC line |
|---|---|
| 1 | `Table of contents` |
| 2 | `Cover letter` |
| 3 | `Form N-400, Application for Naturalization` |
| 4 | `Bio page of latest passport of the applicant` |
| 5 | `Form I-551, Permanent Resident Card` |
| 6 | `Latest tax return` |
| 7 | `Travel addendum` |
| 8 | `Court records` |

  (zhu's own numbering ran 1–9 because `Form G-1450, Authorization for Credit
  Card Transaction` sat at 3; that line is rejected, §10, and everything below
  it shifts up one.)

  Lines set here for the conditional documents the corpus has no modern TOC
  for, built on the same pattern:

| TOC line | for |
|---|---|
| `Bio page of latest passport of the applicant's spouse` | spousal basis |
| `Form I-797C, Notice of Action` | I-751 receipt |
| `Joint deed` | marriage evidence |
| `Joint automobile insurance policy` | marriage evidence |
| `Bio page of latest passport of the applicant's child` | marriage evidence |
| `Written explanation` | moral-character narrative |

- **Lock:** the TOC list is the packet. TOC line count == DOCUMENT count ==
  divider count, TOC line *n* names the same document as divider *n*, and
  merge order is TOC order. FILE-MAP §5 records that the real firm broke this
  in four matters out of five; the synthetic build does not.

### 4.5 Travel addendum — `B-n. Travel Addendum`

Firm-authored, so its layout is frozen here rather than left to Phase 3.
Source: zhu/addendum and zhu/merged p. 62 (title centred at the top margin;
body block indented 0.25" on both sides — measured x 90.47 to x 522.46 —
justified; items 15.84 pt apart with a blank paragraph between).

```
                          TRAVEL ADDENDUM               <- centred, 12 pt

The following is a full list of the Applicant's trips to countries other than
the United States within the last {5|3} years, excluding day trips. It combines
the trips listed in Page {p}, Part 8, Question 1, with the trips listed in the
addendum thereto.

1. {MM/DD/YYYY}-{MM/DD/YYYY} – {COUNTRY}

2. {MM/DD/YYYY}-{MM/DD/YYYY} – {COUNTRY}
```

- The intro sentence is verbatim zhu/addendum, with the residence period and
  the page reference slotted (zhu says "last 5 years" and "Page 6"; a 319(a)
  applicant's Part 8 window is 3 years, and the page number comes from the
  filled form).
- Separator between dates and country is an **en dash** `–` with spaces; the
  date range itself uses a plain hyphen and no spaces.
- Order is **most recent first** (zhu/addendum runs 03/31/2024 down to
  03/30/2019).
- "excluding day trips" is the firm instruction the mess catalogue leans on
  (BUILD-PLAN §5.3, "day trip in travel list, excluded per firm instruction").

---

## 5. THE COVER LETTER

Source: zhu/letter for body, closing and signature block; jacobs/letter for the
date line, the Re: block and the statutory citation; FILE-MAP §2's recovered
template for the photocopies paragraph's slot structure. Where the three
disagree the choice is a numbered taste call. The machine-readable form of this
section is `lab/synthetic/templates/cover-letter.docx.yaml`.

```
{FILING DATE, WRITTEN IN FULL}                    <- e.g. "August 25, 2025"

VIA {CARRIER}                                     <- BOLD + UNDERLINE, all caps

{LOCKBOX BLOCK, 5 or 6 lines}                     <- §7, no blank lines within

⇥Re:⇥Form N-400, Application for Naturalization

⇥⇥Applicant:⇥{HONORIFIC} {FULL LEGAL NAME}
⇥⇥DOB:⇥⇥{MONTH D, YYYY}
⇥⇥COB/CON:⇥{COUNTRY}

To Whom It May Concern:

Enclosed please find one (1) Form N-400, Application for Naturalization, along
with the accompanying filing fee of ${FEE} and supporting documentation, for
{HONORIFIC} {FULL LEGAL NAME}, {A|AN} {NATIONALITY ADJECTIVE} national.
{HONORIFIC} {SURNAME} is eligible for naturalization {ELIGIBILITY CLAUSE}.
See {CITATION}.

All supporting documents in this packet are photocopies of originals.
{HONORIFIC} {SURNAME} understands that {PRONOUN} may have to present originals
as part of the adjudication process.

We look forward to your speedy and favorable adjudication of this application.

Sincerely,

{FIRM NAME}


By: {PREPARER NAME}
Petition Preparer
```

`⇥` is a tab character. Body paragraphs are justified, no first-line indent,
one blank paragraph between blocks. The address block lines carry
`w:spacing after=0` so they set solid (zhu/letter).

### 5.1 The eligibility clause and its citation

Two bases, and only two, per BUILD-PLAN §7.

| basis | `{ELIGIBILITY CLAUSE}` | `{CITATION}` |
|---|---|---|
| **INA 319(a)** — spouse of a U.S. citizen, 3 years | `having three (3) years of permanent residency combined with continuous residence with {PRONOUN_POSS} U.S. citizen spouse, {SPOUSE HONORIFIC} {SPOUSE FULL NAME}` | `8 U.S.C. § 1430(a); 8 C.F.R. § 319.1` |
| **INA 316(a)** — general provision, 5 years | `as it has been more than five (5) years since {PRONOUN} became a permanent resident on {LPR DATE, WRITTEN IN FULL}` | `INA § 316(a); 8 C.F.R. § 316.2` |

The 319(a) clause is FILE-MAP §2's recovered variant; the 316(a) clause is
zhu/letter verbatim ("Ms. Zhu is eligible for naturalization as it has been
more than five (5) years since she became a permanent resident on February 15,
2019."). jacobs/letter proves the firm cites in this position and in this form:
"Ms. Garth is eligible for naturalization under section 319 of the Immigration
and Naturalization Act. 8 U.S.C. § 1430(a); 8 CFR § 319.1(a)." The citation
forms are normalised to the BUILD-PLAN §2 pairs (taste call 6): section symbols
spaced, `C.F.R.` pointed, no `(a)` on the C.F.R. cite.

### 5.2 The fee

`$760.00` — the paper-filing fee, confirmed twice: uscis.gov's N-400 page
("Submit $760 if filing by paper") fetched 2026-08-21, and zhu's own G-1450 in
zhu/merged p. 9, which authorises `760.00`. It travels **only** in the cover
letter's first sentence; no G-1450, no fee page (§10).

### 5.3 What is not on the cover letter

- **No letterhead.** Neither format source has one — no header part, no logo,
  and zhu/merged p. 6 begins at the 1-inch margin with `VIA U.S. POSTAL
  SERVICE (USPS)`. The firm's identity reaches the page only through
  `{FIRM NAME}` in the signature block. See §13 D4; taste call 7.
- **No `Basis:` line** in the Re: block (that is the rejected ossola variant,
  §10).
- **No `Encls.` line, no `MSO` initials** (izaguirre generation).
- **No page number, no footer.**

---

## 6. PACKET ORDER

Fixed. Documents 1–6 are unconditional; conditional documents append in the
precedence order of §9 and take the next numbers.

| DOC | tab | file | content |
|---|---|---|---|
| — | — | `00. Applicant Cover Page` | §4.1 |
| — | A | `A-0. Tab Cover Page` | §4.2 |
| 1 | A | `A-1` | Table of contents |
| 2 | A | `A-2` | Cover letter |
| — | B | `B-0. Tab Cover Page` | §4.2 |
| 3 | B | `B-3` | Form N-400, Application for Naturalization |
| 4 | B | `B-4` | Bio page of latest passport of the applicant |
| 5 | B | `B-5` | Form I-551, Permanent Resident Card (front and back) |
| 6 | B | `B-6` | Latest tax return |
| 7+ | B | `B-7…` | conditional, §9 |

The N-400 comes first among the documents, as the challenge article promises
("The documents in a particular order — the N-400 application form first, then
a handful of others attaching the client's own documents"). Zhu's real order
put the G-1450 at 3 and the N-400 at 4; dropping the G-1450 makes the article's
sentence true.

**Merged page sequence:** applicant cover page · TAB A cover · DOC 1 divider ·
TOC · DOC 2 divider · cover letter · TAB B cover · DOC 3 divider · N-400 (14
pp) · … Every document is preceded by its divider; the tab cover precedes the
first document of its tab; the applicant cover page precedes everything.
Verified against zhu/merged pages 1, 2, 3, 4, 5, 6, 7, 8/9, 10–24, 25/26,
27–29, 30–60, 61/62, 63/64.

---

## 7. LOCKBOX — a two-argument function

`lockbox_block = f(state_of_residence, carrier)`. Source: live/lockbox, fetched
2026-08-21. Both carrier variants matter: jacobs/letter used FedEx and the
Chicago **street** address; zhu/letter used USPS and the Dallas **P.O. Box**.
The `VIA {CARRIER}` line and the address block are locked to each other.

**Line 1 and 2 of every block** (zhu/letter; jacobs/letter opens
`U.S. Department of Homeland Security` — taste call 8 takes zhu's shorter form):

```
Department of Homeland Security
United States Citizenship and Immigration Services
```

| states of residence | lockbox | `VIA U.S. POSTAL SERVICE (USPS)` | `VIA FEDERAL EXPRESS` / UPS / DHL |
|---|---|---|---|
| CT DE DC FL GA ME MD MA NH NJ NY NC PA RI SC VT VA WV | **Elgin** | `USCIS Elgin Lockbox`<br>`Attn: N-400`<br>`P.O. Box 4060`<br>`Carol Stream, IL 60197-4060` | `USCIS Elgin Lockbox`<br>`Attn: N-400 (Box 4060)`<br>`2500 Westfield Drive`<br>`Elgin, IL 60124-7836` |
| AL AK AZ CA CO HI ID KS KY MN MS MT NE NV NM ND OR SD TN UT WA WY (+ territories, Armed Forces) | **Phoenix** | `USCIS Phoenix Lockbox`<br>`Attn: N-400`<br>`P.O. Box 21251`<br>`Phoenix, AZ 85036-1251` | `USCIS Phoenix Lockbox`<br>`Attn: N-400 (Box 21251)`<br>`2108 E. Elliot Rd.`<br>`Tempe, AZ 85284-1806` |
| AR LA OK TX | **Dallas** | `USCIS Dallas Lockbox`<br>`Attn: N-400`<br>`P.O. Box 660060`<br>`Dallas, TX 75266-0060` | `USCIS Dallas Lockbox`<br>`Attn: N-400 (Box 660060)`<br>`2501 S State Hwy 121 Business`<br>`Suite 400`<br>`Lewisville, TX 75067-8003` |
| IL IN IA MI MO OH WI | **Chicago** | `USCIS Chicago Lockbox`<br>`Attn: N-400`<br>`P.O. Box 4380`<br>`Chicago, IL 60680-4380` | `USCIS Chicago Lockbox`<br>`Attn: N-400 (Box 4380)`<br>`131 S. Dearborn, 3rd Floor`<br>`Chicago, IL 60603-5517` |

Carrier strings on the `VIA` line: `U.S. POSTAL SERVICE (USPS)` (zhu/letter),
`FEDERAL EXPRESS` (jacobs/letter). Those two only — the corpus uses no other.

Two notes for Phase 2 casting. BUILD-PLAN §2's preference — one lockbox serving
all six clients — **is** achievable: IL, IN, IA, MI, MO, OH and WI all route to
Chicago. Recommendation (taste call 9): don't. Spread the worked three across
at least two lockboxes *and* both carriers so the dependence is demonstrated
before a test client is asked to derive it, which is the plan's own fallback
and its own "learnability rule" (§0.1).

---

## 8. THE N-400 ITSELF

- **Edition `01/20/25`, 14 pages, 488 AcroForm fields.** Committed at
  `lab/synthetic/blanks/n-400.pdf` (776,244 bytes, sha256
  `8b33868b…a82d909`), fetched 2026-08-21 from
  `https://www.uscis.gov/sites/default/files/document/forms/n-400.pdf`.
  BUILD-PLAN §1 calls this edition `04/01/24`; it is wrong (§13 D1). The
  01/20/25 edition is also what jacobs filed in 2025 (jacobs/N-400 p. 1, read
  visually), which suits the Nov 2025 – Jul 2026 in-world timeline.
- **`fieldmap_n400.yaml` is built from the committed blank, never from zhu's
  filed copy.** zhu's form is the older 04/01/24 edition (414 fields in the
  signed copy, 489 in the unflattened original) and the parts were renumbered
  between editions.
- **Born-digital.** Fill with pypdf, delete `/XFA`, set `NeedAppearances`;
  never print-and-scan (BUILD-PLAN §0.1).
- **Fill Part 11 (applicant's contact information) and Part 13 (preparer).**
  zhu's filed form leaves both empty — 277 of 414 fields carry values and none
  of them is a phone, an email or a preparer name. That is the real firm being
  careless; a firm-prepared form with an empty preparer block is not a style to
  copy. Taste call 10.
- **Signature.** Rendered in Z003 (Zapf Chancery clone, confirmed installed by
  BUILD-PLAN §1) over the signature widget, plus the signature date. zhu's ink
  is present only in the flattened image, so the corpus neither confirms nor
  contradicts; this is taste call 11.
- **What the firm fills, from zhu/N-400's 277 non-empty fields:** Part 1
  eligibility box; A-number on every page header; Part 2 name, other names,
  name-change request, DOB, sex, LPR date, country of birth, country of
  citizenship, disability claims (No); Part 3 ethnicity, race, height, weight,
  eye colour, hair colour; Part 4 current address + three prior addresses with
  from/to; Part 5 marital status, times married, spouse country; Part 7
  employment (three employers with city, state, ZIP, country, occupation,
  from/to); Part 8 travel table (6 rows on that edition); Part 9 every
  moral-character question; Part 11/12 oath answers. That is the fact set §12
  formalises.

---

## 9. THE EXHIBIT RULE — a four-argument decision table

`exhibits = f(basis, moral-character answers, immigration history, supplied
evidence)`

FILE-MAP §3 had two arguments; ossola/exhibits and ossola/provenance add the
third and fourth. The Phase 5 verifier recomputes this table per client and
diffs it against the rendered packet.

### 9.1 Unconditional core — every packet, every client

| DOC | document | why |
|---|---|---|
| 1 | Table of contents | firm-authored |
| 2 | Cover letter | firm-authored |
| 3 | Form N-400 | the application |
| 4 | Applicant's passport bio page | identity; supplies name, DOB, COB, MRZ |
| 5 | Form I-551, Permanent Resident Card (front and back) | supplies A-number and LPR date |
| 6 | Latest tax return | continuous-residence and good-moral-character evidence |

Attested as the invariant core across all five corpus matters (FILE-MAP §2
"The invariant core"; ossola/exhibits "ALWAYS"). The tax return is core in
zhu and ossola and is kept core here (taste call 5) even though jacobs' 2025
packet has only four documents — jacobs is a returning client whose packet is
the thinnest in the corpus.

### 9.2 Conditional documents, in append precedence order

| order | document | argument | trigger — exact condition |
|---|---|---|---|
| C1 | Spouse's passport bio page | **basis** | `basis == 319(a)` |
| C2 | Form I-797C, Notice of Action | **immigration history** | `conditional_resident.was_cr == true` **and** the unconditional I-551 was not in hand at the filing date (I-751 pending, or approved so late that the card post-dates filing) |
| C3a | Joint deed | **supplied evidence** | `basis == 319(a)` **and** a joint deed is among the documents the client supplied |
| C3b | Joint automobile insurance policy | **supplied evidence** | `basis == 319(a)` **and** supplied |
| C3c | Child's passport bio page | **supplied evidence** | `basis == 319(a)` **and** a child of the marriage exists **and** the child's passport was supplied |
| C4 | Travel addendum | **derived** | trips within the residence window exceed the Part 8 table's row count, **or** any supplied trip was trimmed from the form (day trips) |
| C5 | Court records | **moral-character answers** | any Part 9 arrest / citation / detention / charge answer is `Yes` |
| C6 | Written explanation | **moral-character answers** | any Part 9 `Yes` that the form's own table cannot carry (removal proceedings, deportation, benefit denial) |

### 9.3 Rules that fall out of the table

1. **A joint tax return is not a separate document.** If the applicant files
   jointly, DOCUMENT 6 (the core tax return) *is* the marriage evidence.
   Ossola's packet listed `9. Tax Returns` inside the marriage cluster; here
   the core slot absorbs it. Taste call 13.
2. **316(a) admits no spousal evidence at all** — no C1, no C2, no C3. FILE-MAP
   §3: "INA 316 five-year → no spousal evidence at all."
3. **The firm over-documents, but only what arrived.** C3a–C3c are a function
   of *supplied* evidence, not of the basis alone. This is the classification
   behaviour the plugin must exercise (BUILD-PLAN §2).
4. **Every conditional document is traceable to a fact on the form.** If a
   packet contains a document that no row above triggers, the packet is wrong.
   FILE-MAP §3: "Everything beyond the invariant core is conditional, and the
   condition is always traceable to a form answer."
5. **The travel addendum is a superset of the form's travel table** — the
   addendum lists every countable trip; the form lists as many as fit.
6. **G-1450 and G-1145 are never triggered** (§10).

### 9.4 Cross-document consistency locks (carried from FILE-MAP §3)

Surname and given name identical on N-400, passport MRZ and cover letter · DOB
identical everywhere it appears (cover page, cover letter, N-400, passport,
green card) · place of birth identical on N-400 and passport · A-number
identical on green card, every N-400 page header and any I-797C · green card
`Resident Since` == N-400 Part 2 LPR date == the cover letter's 316(a) date ·
tax-return address appears in the N-400 address history · resume employers and
dates equal Part 7 · travel addendum ⊇ Part 8 table · I-797C receipt number
reconciles with the masterkey · TOC line count == divider count == DOCUMENT
count · merged page count == sum of component page counts.

---

## 10. CONSCIOUSLY REJECTED

| rejected | seen in | why |
|---|---|---|
| **Form G-1450, Authorization for Credit Card Transaction** | zhu/TOC line 3; zhu/merged pp. 8–9 (a filled, redacted G-1450 authorising $760); ossola `4. G-1450` | Three reasons. The challenge article promises the N-400 first among the documents; a G-1450 sits on top of it. It carries a live credit-card number, an expiry and a signature — a document class the synthetic build has no business fabricating even from invented digits. And the fee is fully expressible in one cover-letter clause (§5.2). *Correction to FILE-MAP §5, which says zhu's TOC "promised a G-1450 that does not exist": it exists in the merged packet; what is missing is a loose `B-3` component. See §13 D2.* |
| **Form G-1145, E-Notification of Application Acceptance** | ossola `1. G-1145`; malone/Luwilyn (on disk, absent from index and merge) | Same first-position problem, and its only effect is a text message to the client — invisible in the packet and unlearnable from it. |
| **The ossola cover-letter variant** | ossola/exhibits; FILE-MAP §7 | Replaces the DOB and COB/CON lines with a `Basis:` line, carries no statutory citation at all, and inverts the closing to "favorable and speedy". Pre-zhu generation, excluded as a format source by `lab/NOTES.md`, and dropping the citation loses the one part of the letter that teaches the basis rule. |
| **The `Permanent Resident Since:` index header** | malone, izaguirre index headers | 2020–2022 generation. Its fact is already on the cover page as `Classification Basis` and in the cover letter's eligibility clause. |
| **The `INDEX OF DOCUMENTS` heading** | malone/Luwilyn 2020, malone/Braun 2021, ossola 2022, izaguirre 2022 | Died with the 2022 generation. Both modern packets say `TABLE OF CONTENTS` (FILE-MAP §2). |
| **The supplemental cover letter** | ossola `Cover Letter with Greencard.docx`, 2023-01-30, RE: block carrying a case number | Real and interesting, but it is not a function of the input folder — it answers a later USCIS event. `naturalize <input-folder>` produces one packet. It cannot be taught by input/output pairs and would blur what an output folder is (BUILD-PLAN §2). |
| **Simulated print-and-scan output** | jacobs/N-400, ossola's filed N-400 (both image-only) | Every synthetic output is born-digital (BUILD-PLAN §0.1): the taker's plugin can only produce born-digital output, so a scanned target is unmatchable; and a text layer keeps the challenge tractable. Scans still appear — on the **input** side, which is where phone photos of cards and notices belong. |
| **Letterhead** | malone (`26 Broadway Fl 8`, `31 Hudson Yards Fl 11`), izaguirre (`SYMPLE`) | Neither format source has one (§5.3). §13 D4. |
| **Text boxes, tables, headers, footers, page numbers** | malone/Braun cover letter (24 `txbxContent`) | §3. |
| **Revision markers in file names** (`(Updated)`, `(Second Update)`, `Compressed`, `_Signed`, `_Original Copy`) | zhu's `Others/` | The output folder is what was filed, once. Revision archaeology is a corpus artefact, not a house style. |
| **Transcription loss and output-side inconsistency** | malone ("Ma Lone", 10th→16th St), ossola (three filing dates; 2y9m continuous residence) | BUILD-PLAN §0.1: the pairs are internally perfect at the fact level; all mess lives on the input side with a deterministic resolution. |

---

## 11. SHARED STRINGS — NOT LEAKAGE

Phase 5 layer 3 greps `lab/synthetic/blocklist.txt` against the synthetic tree
in both directions and allows zero hits. This section exists so that whoever
writes that scan knows the difference between a real hit and a string the house
style **requires** every packet to contain. All of the following appear in the
corpus *and* must appear in synthetic output; `build_blocklist.py` excludes
them by construction and they must never be re-added:

- The four lockbox blocks of §7 in both carrier variants — `USCIS`,
  `Chicago`, `Dallas`, `Elgin`, `Phoenix`, `Carol Stream`, `Tempe`,
  `Lewisville`, `P.O. Box 4380`, `P.O. Box 660060`, `P.O. Box 4060`,
  `P.O. Box 21251`, `131 S. Dearborn`, `2500 Westfield Drive`,
  `2108 E. Elliot Rd.`, `2501 S State Hwy 121 Business`, and their ZIPs.
- Agency and form vocabulary — `Department of Homeland Security`,
  `United States Citizenship and Immigration Services`, `N-400`, `I-551`,
  `I-751`, `I-797C`, `G-1450`, `1040`, `Form`, `Application for
  Naturalization`, `Permanent Resident Card`.
- Statutory citations and the fee — `INA`, `8 U.S.C. § 1430(a)`,
  `8 C.F.R. § 319.1`, `INA § 316(a)`, `8 C.F.R. § 316.2`, `316`, `319`, `760`.
- Every literal string frozen in §4 and §5 — `APPLICATION FOR NATURALIZATION`,
  `APPLICANT:`, `DOB:`, `COB/CON:`, `Classification Basis:`, `TAB A`,
  `SUMMARIES`, `TAB B`, `BIOGRAPHICAL`, `DOCUMENT`, `TABLE OF CONTENTS`,
  `Tab A (Summary)`, `Tab B (Biographical Information)`, `COVER LETTER`,
  `FORM N-400`, `PASSPORT`, `GREEN CARD`, `INCOME TAX RETURN`,
  `TRAVEL ADDENDUM`, `COURT RECORDS`, `VIA`, `Attn:`, `Re:`,
  `To Whom It May Concern:`, `Enclosed please find`, `Sincerely,`,
  `Petition Preparer`, and the two eligibility clauses.
- US state names and abbreviations, month names, country names, generic
  address nouns (`Street`, `Avenue`, `Apt`, `Suite`, `Floor`, `Box`).
- The vocabulary of the exhibits the build itself renders — 1040 line labels,
  deed and recorder terms, insurance-policy terms, I-797C notice terms, court
  disposition terms.

### 11.1 What the blocklist can and cannot see

`build_blocklist.py` harvests every `.txt` sidecar, every email body, every
`.md` report and every path name under `lab/`. **54 of the 185 corpus PDFs are
image-only scans whose sidecars are the stub `[NO TEXT LAYER — …]`** (FILE-MAP
§7), and every identifier that lives *only* on a scan — jacobs' A-number, zhu's
police case number, the deed and tax preparers — is invisible to that pass.

The script therefore runs a **second pass: `pdftoppm -r 200 -gray` plus
`tesseract` over each of the 54, cached by file hash in `tools/.ocr-cache/`**
so that reruns are offline and deterministic. OCR noise is *wanted* here: the
variant readings it produces are exactly the OCR variants FILE-MAP §7 says must
all go on the list ("Ma Lone" as well as "Malone"). Tokens read visually during
Phase 1 are additionally hardcoded in the script's `KEEP_ALWAYS`.

Two limits to carry forward. Tesseract's output is not pinned across versions,
so the *cache* — not the OCR — is what makes the build reproducible; delete it
and the token list may shift slightly. And OCR on a photographed card or a
hand-annotated court form is imperfect, so **the leakage scan is necessary but
not sufficient**. BUILD-PLAN §10 ranks leakage as risk 2 and puts the scan on
the never-cut list; this is a recorded hole in it, not a closed one. Phase 6's
final scan on the shipped tree inherits the same limit.

**Applicant-nationality exclusions are a casting constraint, not a blocklist
entry.** BUILD-PLAN §7 rules Australia, China, Mexico, the Philippines and
Italy out as *applicant* nationalities. Those country names still appear
legitimately in travel history, so they stay off `blocklist.txt`; Phase 2's
registry enforces the constraint instead.

---

## 12. FACTS THE OUTPUT CONSUMES

Every distinct fact some output artefact needs. Phase 2's masterkey schema is
validated against this list; a fact here with no masterkey home is a schema
bug, and a fact here with no input surface is a broken test client
(BUILD-PLAN §3). Benchmarked against ossola/provenance, which maps one real
packet field by field.

### 12.1 Identity
family name · given name · middle name · other names used since birth (0–2,
family/given/middle each) · name-change requested? and if so the new
family/given/middle name · honorific (`Mr.`/`Ms.`) · pronouns (subject,
possessive) · date of birth · sex · country of birth · country of citizenship
or nationality · nationality adjective (for the cover letter's "an Australian
national") · SSN · USCIS online account number (or none) · height (feet,
inches) · weight (pounds, 3 digits) · eye colour · hair colour · ethnicity
(Hispanic/Not Hispanic) · race (one or more)

### 12.2 Contact
daytime telephone · mobile telephone · email address

### 12.3 Immigration status
A-number (9 digits) · date became a permanent resident (LPR date) · class of
admission · eligibility basis (`316(a)` / `319(a)`) · classification-basis
string for the cover page · was a conditional resident? · I-751 receipt
number · I-751 received date · I-751 notice dates · I-751 status at filing ·
unconditional card in hand at filing? · **derived:** earliest filing date
(LPR + 3y − 90d, or LPR + 5y − 90d) · continuous-residence years at filing

### 12.4 Residence
current physical address (street number and name, unit type + number, city,
state, ZIP, country, from-date) · mailing address if different · prior
addresses, gap-free, covering the residence window (street, unit, city, state,
ZIP, country, from, to) · state of residence → lockbox (§7)

### 12.5 Marital and family
marital status · number of times married · date of current marriage · spouse
family/given/middle name · spouse DOB · spouse A-number (if any) · spouse is a
U.S. citizen? · citizen at birth or naturalised (+ date and place if
naturalised) · spouse's address (same as applicant?) · spouse's employer ·
spouse's number of prior marriages · prior marriages of the applicant (name,
dates, how ended) · each child: family/given/middle name, DOB, country of
birth, relationship type, address, lives with applicant? · each parent: name,
U.S. citizen?, married before the applicant turned 18?

### 12.6 Employment and education
per entry, covering the residence window: employer or school name · city ·
state · ZIP · country · occupation or field of study · from date · to date ·
"present" flag

### 12.7 Travel
per trip: departure date · return date · country or countries · day count ·
`on_form` flag · `why_excluded` (day trip / outside window) · **derived:**
total days outside the U.S. · whether an addendum is triggered (§9.2 C4)

### 12.8 Moral character
every Part 9 item: answer (`Yes`/`No`) and, where `Yes`, the explanation text,
the arrest/charge detail row (date, place, offence, outcome), and whether it
triggers court records (C5) or a written explanation (C6) · Part 10 fee
reduction (`No`) · Part 12 oath answers (bear arms / noncombatant service /
work of national importance / support the Constitution / no mental
reservation)

### 12.9 Matter and firm
firm name · preparer name · preparer title (`Petition Preparer`) · preparer
daytime telephone · preparer email · preparer business address (street, city,
state, ZIP) · engagement date · **filing date** (drives the cover-letter date
and the signature date) · carrier (`U.S. POSTAL SERVICE (USPS)` /
`FEDERAL EXPRESS`) · lockbox block (derived, §7) · fee (`760.00`) · form
edition string (`01/20/25`)

### 12.10 Exhibit facts
- **applicant passport:** issuing country · passport number · surname and given
  names as printed · nationality · DOB · sex · place of birth · issue date ·
  expiry date · issuing authority · MRZ line 1 and line 2 (check digits
  computed)
- **green card (I-551):** surname · given name · A-number (`USCIS#`) ·
  category / class of admission · country of birth · DOB · sex · card expiry ·
  `Resident Since` date · front and back
- **spouse's passport / child's passport:** the same field set
- **tax return:** tax year · filing status · taxpayer and spouse names and
  SSNs · address as printed · wages · adjusted gross income · total tax ·
  refund or amount owed · preparer name · which blank (`f1040.pdf` = TY2025,
  `f1040--2024.pdf` = TY2024; §13 D11)
- **Form I-797C:** receipt number · case type (`I751`) · received date ·
  notice date · notice type · applicant name · A-number · fee paid
- **joint deed:** grantor(s) · grantee(s) · property address · county ·
  recording date · instrument number · consideration · preparer
- **joint automobile policy:** insurer · policy number · named insureds ·
  policy period (effective, expiry) · garaging address · vehicle(s) · coverages
- **court records:** court name and location · police case number · docket
  number · charge(s) with statute number and offence date · plea · disposition
  and disposition date · judge · clerk certification date and seal
- **travel addendum:** the full trip list (§4.5) · residence window (3 or 5
  years) · the Part 8 page number on the filled form
- **resume** (input-side, but locked to Part 7): employer, title, city, dates

### 12.11 Facts that exist only in the output
TOC line list (derived from §9) · DOCUMENT count · each DOCUMENT's divider
title (§4.3) and TOC line (§4.4) · per-component page count · merged page count
· eligibility clause and citation (§5.1) · nationality adjective (§12.1)

---

## 13. DIVERGENCES FROM THE PLAN

Recorded where the raw files contradict BUILD-PLAN §2 or FILE-MAP. Nothing here
is silently followed.

**D1 — the N-400 edition. BUILD-PLAN §1 is wrong.** It records the fetched
blank as "edition 04/01/24, 14 pp", "same edition as zhu's filed form". Fetched
again 2026-08-21: same URL, same 776,244 bytes, same 14 pages, same 488 fields
— **edition `01/20/25`**, expires 02/28/2027. uscis.gov's N-400 page states
`Edition Date 01/20/25`. zhu's filed form is the *older* 04/01/24 edition;
jacobs' 2025 filing is 01/20/25. Consequence: `fieldmap_n400.yaml` must be
built from the committed blank, not from zhu's field dump (§8).

**D2 — zhu's G-1450 exists.** FILE-MAP §5 says "zhu's TOC promises a G-1450
that does not exist". Read visually: zhu/merged p. 9 is a completed G-1450
(applicant Xuying Zhu, card holder Marcel Oliveira, `760.00` authorised, card
number redacted by hand). What is missing is the *loose* `B-3` component in the
Tab B folder — the index/disk mismatch is on the component tree, not the
packet. The decision to drop the G-1450 stands, on the grounds in §10.

**D3 — the text-box rule's stated reason is misattributed.** BUILD-PLAN §2 says
"the corpus letterheads lived in docx text boxes and that is exactly what
converters lose (jacobs' own signature block never extracted)". jacobs/letter
contains **zero** `txbxContent` elements, no header part and no drawing; its
XML simply ends after the eligibility sentence — it is a truncated draft, not a
text-box casualty. A scan of every `.docx` in `lab/` finds exactly one file
with text boxes: `malone_kyle/Braun, David/Cover letters/Cover Letter.docx`
(24). The no-text-boxes rule is kept (§3); its justification is corrected.

**D4 — no letterhead in either format source.** FILE-MAP §2's recovered
template opens with `{LETTERHEAD}` and BUILD-PLAN §2 says the Phase 2 registry
invents a "letterhead address". Neither jacobs/letter nor zhu/letter has one:
no header part, and zhu/merged p. 6 starts at the top margin with the `VIA`
line. Letterhead belongs to the 2020–2022 generation (`26 Broadway Fl 8`,
`31 Hudson Yards Fl 11`). **Decision: no letterhead** (taste call 7). The
registry still invents a firm address — Phase 3 needs it for the N-400's Part
13 preparer block — it just never reaches the cover letter.

**D5 — two names for each tab.** BUILD-PLAN §2 names the tabs "TAB A (Summary)
/ TAB B (Biographical Information)". The packet uses **two different strings**:
the tab cover pages say `TAB A` / `SUMMARIES` and `TAB B` / `BIOGRAPHICAL`
(zhu/merged pp. 2, 7), while the TOC says `Tab A (Summary)` and `Tab B
(Biographical Information)` (zhu/TOC). Both are preserved (taste call 2). The
alternative — harmonising on the TOC's wording and rewriting the cover pages
`TAB A` / `SUMMARY` — is available if the user prefers one string per tab.

**D6 — the cover-letter date.** jacobs/letter opens with a written-out date
(`August 25, 2025`); zhu/letter has **no date at all**. The template takes
jacobs' date line (taste call 6), because a filed letter without a date is an
omission, not a style.

**D7 — the "recovered template" is a synthesis, not a document.** FILE-MAP §2's
template matches no single file. Its indented first lines, its `{LETTERHEAD}`
slot and its closing "Thank you for your time and attention." all come from the
2020–2022 generation; the modern closing is zhu's "We look forward to your
speedy and favorable adjudication of this application." §5 reconciles it
against jacobs and zhu line by line and states which line came from where.

**D8 — lockbox is two arguments, not one.** BUILD-PLAN §2 asks for "current
N-400 paper-filing addresses by state". Each lockbox has two addresses, USPS
and courier, and the corpus uses both (jacobs: FedEx + street; zhu: USPS + P.O.
Box). §7 states it as `f(state, carrier)`. The plan's "one lockbox serves all
six" preference is achievable but is recommended against (taste call 9).

**D9 — three pages have no loose component.** The applicant cover page and both
tab cover pages exist *only* inside zhu's merged PDF; there is no docx or pdf
for them anywhere in the tree. Since the deliverable is loose components **and**
a merged PDF, names are invented here: `00. Applicant Cover Page`,
`A-0. Tab Cover Page`, `B-0. Tab Cover Page` (§2). Invented, and marked as
invented.

**D10 — zhu's Part 11 and Part 13 are empty.** 277 filled fields and not one of
them a phone number, an email address or a preparer name. We fill them (§8,
taste call 10).

**D11 — which tax year is "latest".** The matters run Nov 2025 – Jul 2026. A
packet filed before roughly mid-April 2026 has TY2024 as its latest return;
after, TY2025. Both blanks are committed (`f1040--2024.pdf`, 2 pp / 155 fields;
`f1040.pdf` TY2025, 2 pp / 229 fields). Phase 2 must set each client's tax year
consistently with its filing date; Phase 5 should lock it.

**D12 — jacobs is thinner than the core.** jacobs' 2025 packet has four
documents (cover letter, N-400, green card, passport) and no tax return, no
travel addendum and no cover page. It is a returning client's packet and it is
the weakest structural source in the corpus. Structure is taken wholly from
zhu; jacobs contributes wording only (date line, Re: block, citation, divider
shape). Stated so that a later agent does not "restore" jacobs' four-document
shape.

**D13 — BUILD-PLAN §7's profile table breaks its own no-duplicate rule.**
§7 promises "no test client's exhibit set equals any worked example's, so
copying fails and rule-learning succeeds". Run the §9 table over the six
profiles as written:

| client | basis | conditional documents | DOC count |
|---|---|---|---|
| W1 Almeida | 316(a) | C4 travel addendum | 7 |
| W2 Kavanagh | 319(a) | C1, C2, C3b | 9 |
| W3 Nowak | 316(a) | C5, C6 | 8 |
| T1 Tran | 319(a) | C1, C3a, C3c, C4 | 10 |
| **T2 Stavros** | **316(a)** | **C4 travel addendum** | **7** |
| T3 Adeyemi | 316(a) | C4, C5 | 8 |

**T2's exhibit set is identical to W1's** — same basis, same single
conditional, same seven documents. Under the frozen rule T2 is copyable from
W1, which is precisely what §7 says must not happen. Phase 1 does not fix this
(casting owns the profiles) but it does not let it pass silently: it is a
Phase 2 decision, listed in §15.

---

## 14. TASTE CALLS — the user's sign-off list

Each is a place where the sources disagreed or were silent and this document
decided. Numbered so they can be accepted or overturned individually.

1. **Applicant cover page follows zhu**, mixed case with honorific
   (`Ms. Xuying Zhu`), not jacobs' all-caps `LAUREN RAE GARTH`; and it is its
   own page, not the head of the TOC as in jacobs.
2. **Both tab-name strings are kept** — `SUMMARIES` / `BIOGRAPHICAL` on the
   cover pages, `(Summary)` / `(Biographical Information)` in the TOC. See D5
   for the harmonised alternative.
3. **Dividers are set at 24 pt**, matching the tab cover pages. The corpus
   drifts 12 / 19.9 / 22.1 / 23.0 pt; the two-line bold/regular shape is the
   real invariant and the point size is arbitrary.
4. **Green-card divider says `GREEN CARD`** (zhu), not `PERMANENT RESIDENT
   CARD` (jacobs) — while the TOC line stays `Form I-551, Permanent Resident
   Card` (zhu). The divider shouts, the TOC is formal.
5. **The latest tax return is core, not conditional** (zhu, ossola). jacobs has
   none.
6. **Cover letter is a reconciliation:** date line, `Re:` block with tab
   alignment and `DOB:` / `COB/CON:` abbreviations, `To Whom It May Concern:`
   and the statutory citation from jacobs; opening sentence, photocopies
   paragraph, closing sentence and signature block from zhu; the fee clause
   from FILE-MAP's recovered template with the amount added. Citations
   normalised to the BUILD-PLAN §2 pairs.
7. **No letterhead.** See D4.
8. **Address block opens `Department of Homeland Security`** (zhu), not
   `U.S. Department of Homeland Security` (jacobs).
9. **Spread the six clients across at least two lockboxes and both carriers**,
   demonstrating each in a worked pair before any test client needs it —
   against BUILD-PLAN §2's stated preference for one lockbox. See D8.
10. **Fill the N-400's Part 11 contact block and Part 13 preparer block**,
    which zhu left empty. See D10.
11. **Render a cursive signature** (Z003) on the N-400 signature line and the
    signature date, rather than shipping an unsigned form.
12. **The merged file is `N-400 Packet.pdf`** with no revision marker.
13. **A joint tax return does not appear twice** — the core DOCUMENT 6 absorbs
    it when it is also marriage evidence. See §9.3.1.
14. **`Classification Basis:` values are `INA 316(a)` and `INA 319(a)`** and
    nothing else, on every packet, matching zhu's `INA 316(a)`.

---

## 15. UNRESOLVED — NEEDS USER

The lockbox question BUILD-PLAN §2 flagged is **resolved**: uscis.gov was
reachable and §7 carries the live table for all four lockboxes and both
carriers. What remains:

1. **The invented firm identity** — name, preparer name, business address,
   phone, email. Phase 2's registry proposes; this is a taste call the user
   owns. Constraint from §11: it must not collide with `SYMPLE`,
   `Marcel Oliveira`, `26 Broadway`, `31 Hudson Yards`, `66 Hudson Blvd E` or
   `trysymple.com`, all of which are on `blocklist.txt`.
2. **Sign-off on the fourteen taste calls in §14**, chiefly 2, 6, 7, 9 and 10.
3. **Whether the divider titles set in §4.3 for the spousal cluster** —
   `SPOUSE'S PASSPORT`, `FORM I-797C, NOTICE OF ACTION`, `JOINT DEED`,
   `JOINT AUTOMOBILE POLICY`, `CHILD'S PASSPORT` — read right. They are
   invented: no modern-generation packet in the corpus has a spousal divider.
4. **T2 Stavros duplicates W1 Almeida's exhibit set** (§13 D13). Phase 2
   either gives T2 a differentiator — an arrest (C5), a conditional-resident
   history (C2), or a spousal basis — or BUILD-PLAN §7's no-duplicate claim is
   weakened to allow the one intentional overlap. The plan's own difficulty
   ramp (T2 is the median and the first dogfood target) argues for giving T2
   something W1 does not have.
5. **The `.docx` for a form or an exhibit does not exist.** Only the four
   firm-authored documents (applicant cover page, tab cover pages, TOC, cover
   letter, travel addendum) ship as docx + pdf; forms and exhibits ship as pdf
   only. Confirm that is the intended reading of "loose numbered components
   (docx + pdf)".

---

## 16. USER DECISIONS — 2026-08-21 — BINDING

The §14 taste calls were put to the user one at a time and answered. **These
rulings override §14 and every section they touch.** Where a ruling overturns
the spec, the overturned text stays in place above for traceability but is
DEAD — this section governs.

| # | ruling | status |
|---|---|---|
| 1 | Applicant cover page follows zhu: standalone page, mixed case with honorific | UPHELD |
| 2 | **One string per tab.** Harmonise on the TOC wording per D5: cover pages become `TAB A` / `SUMMARY` and `TAB B` / `BIOGRAPHICAL INFORMATION`; the TOC keeps `Tab A (Summary)` / `Tab B (Biographical Information)`. The plural `SUMMARIES` and the bare `BIOGRAPHICAL` are DEAD | **OVERTURNED** |
| 3 | **Dividers set at 12 pt**, matching body text and jacobs/dividers. The 24 pt in §3 is DEAD. The two-line bold/regular shape is unchanged | **OVERTURNED** |
| 4 | **The green-card divider reads `PERMANENT RESIDENT CARD`**, not `GREEN CARD`. The TOC line stays `Form I-551, Permanent Resident Card`. §4.3 must be updated | **OVERTURNED** |
| 5 | Latest tax return is core, always present as DOCUMENT 6 | UPHELD |
| 6 | Cover letter is the jacobs/zhu stitch described in §5 | UPHELD |
| 7 | **No letterhead — and no firm name anywhere in any artefact.** This goes beyond §14.7: the firm is never named on the cover letter, the signature block, the N-400, or any other page. See ruling 10 | **UPHELD AND EXTENDED** |
| 8 | **Address block opens `U.S. Department of Homeland Security`** (jacobs), not zhu's shorter form | **OVERTURNED** |
| 9 | Spread the six clients across at least two lockboxes and both carriers, each demonstrated in a worked pair first | UPHELD |
| 10 | **N-400 Part 13 preparer block stays entirely blank** — no preparer name, no business name, no preparer address, no preparer signature. Part 11 (the applicant's own phone and email) IS filled | **PARTLY OVERTURNED** |
| 11 | **The N-400 ships UNSIGNED.** No cursive rendering, no signature date. The Z003 font is not used | **OVERTURNED** |
| 12 | Merged file is `N-400 Packet.pdf`, no revision marker | UPHELD |
| 13 | A joint tax return appears once; DOCUMENT 6 absorbs it | UPHELD |
| 14 | `Classification Basis:` takes exactly `INA 316(a)` or `INA 319(a)` | UPHELD |

### Consequences later phases must honour

- **Ruling 7 kills the firm identity question in §15.1.** Phase 2's registry
  invents no firm name, no preparer name, no business address, no firm phone
  or email. Nothing downstream may reintroduce one.
- **Rulings 10 and 11 shrink the render surface.** `render_n400.py` drops the
  signature path entirely and writes no Part 13 field. Phase 5's verifier
  should assert Part 13 and the signature fields are EMPTY, not merely
  consistent — a filled preparer block is a build bug.
- **Ruling 3** changes divider geometry: at 12 pt the two-line block no longer
  reads as a title page. Phase 3's QA pass should confirm dividers still
  register as dividers at that size before all six clients render.
- **Ruling 2** changes the tab cover pages, which are among the three pages
  §13 D9 notes have no loose component in the corpus at all. They are
  invented regardless, so the new strings cost nothing.

### Still open after this pass

1. The spousal-cluster divider titles in §4.3 (`SPOUSE'S PASSPORT`,
   `FORM I-797C, NOTICE OF ACTION`, `JOINT DEED`, `JOINT AUTOMOBILE POLICY`,
   `CHILD'S PASSPORT`) — invented, never shown to the user. Note that
   ruling 4 sets a precedent: the user preferred the formal name over the
   colloquial one, so these read consistently with that.
2. **T2 Stavros duplicates W1 Almeida's exhibit set** (§13 D13). A Phase 2
   casting decision, still unmade.
3. Confirmation that only firm-authored documents ship as docx + pdf, and
   forms and exhibits ship as pdf only (§15.5).

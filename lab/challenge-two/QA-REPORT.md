# Challenge Two — Independent QA Report

## Verdict: FAIL (1 of 26 checks fails, low severity)

25 of 26 checks pass with mechanically-verified evidence. Check 18 fails: the
Subject line of `to-do/002_2026-02-04_pell-ottway.txt` places the complete
employee-name value ("Colin Mazur") on a labelled header line, which the
task's own check 18 explicitly prohibits for all six variables. This is a
real, narrow, easily-fixed defect, not a structural problem with the corpus —
see the defect list for full detail and mitigation. Every other check,
including the harder cross-cutting ones (provision matrix, the two
deliberate gaps, citation-freedom, the answer key's own zero-mismatch claim),
holds up under independent, mechanical re-verification against the rendered
files, not the manifest or the answer key's prose.

All extraction was done directly from the rendered files: `python-docx` for
the four `.docx` contracts, `fitz`/PyMuPDF for the four `.pdf` contracts
(plus raw `strings` and internal-XML passes for a second look), and `cat`/
`grep` for the one `.txt` contract and all three `.txt` emails. Extracted
text lives in `.scratch/extracted/*.extracted.txt` (worktree-local, not part
of the deliverable).

---

## Checks 1–26

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File counts, no subfolders, nothing extra | PASS | `find` shows exactly 9 files in `contracts/`, 3 in `to-do/`, no subdirectories, no other files anywhere under `challenge-two/`. |
| 2 | Format tally: 4 docx / 4 pdf / 1 txt | PASS | `ls contracts \| sed 's/.*\.//' \| sort \| uniq -c` → `4 docx, 4 pdf, 1 txt`. Producer confirmed independently: all 4 `.docx` files carry `<Application>Microsoft Word 12.0.0</Application>` in `docProps/app.xml`, pandoc's fixed signature string. The `.txt` contract is byte-identical (`cmp`) to `lab/challenge-two/sources/contracts/06-vantage-ct.txt` — confirms `copy-txt`. |
| 3 | Two PDF producers distinguishable | PASS | PyMuPDF metadata: contracts 3 & 9 → `producer: ReportLab PDF Library - (opensource)`, fonts `{Helvetica, Helvetica-Bold}`. Contracts 4 & 7 → `producer: LibreOffice 26.2.3.2 (AARCH64)`, `creator: Writer`, fonts `{NotoSerif-Regular, NotoSerif-Bold}` (subset-embedded). Producer metadata and font sets both cleanly separate the two groups, and both match the manifest's assignment (reportlab → 3, 9; soffice → 4, 7). |
| 4 | Filenames match manifest `output_filename` exactly | PASS | Programmatic set comparison (Python, `csv.DictReader` on the manifest vs `os.listdir`): `expected_set == actual` → `True`. Zero differences either direction. |
| 5 | No README/NOTICE/index/manifest/.gitkeep anywhere under `challenge-two/` | PASS | `find ... -iname "*readme*" -o -iname "*notice*" -o -iname "*index*" -o -iname "*manifest*" -o -iname ".gitkeep"` → no output. |
| 6 | Nothing added to `content/index.json` | PASS | `grep -o '"[^"]*materials[^"]*"' content/index.json` → no match; confirmed `index.json` parses as valid JSON and contains no `materials/` path. |
| 7 | 3 NY / 3 CT / 3 NJ, governing-law clause matches manifest state per contract | PASS | Extracted each contract's "Governing Law" clause directly: 1 Halvorsen→NY, 2 Ostrander→NY, 3 Kestrel→NY, 4 Merrow→CT, 5 Stonefield→CT, 6 Vantage→CT, 7 Ardsleigh→NJ, 8 Bramwell→NJ, 9 Larkspur→NJ. All nine match the manifest's `state` column exactly. |
| 8 | No term > 24 months, no geography beyond national, anywhere in the corpus | PASS (with one flagged design tension, not a defect) | Regex sweep for month/year terms across all 9 rendered contracts found only 6/9/12/18/24-month terms, nothing higher, and no bare "N years" language in any contract. Geography sweep found no "worldwide/international/globally" restriction; the one hit ("internationally") in contract 2 is in a WHEREAS recital describing the *company's* business, not the restrictive covenant — the covenant's own `"Territory" means the United States` definition is unaffected. Emails: 001's "a year and a half" = 18mo (fine); 003's "two years" = 24mo (fine); 002 contains "three years" **three times** (lines 13, 14, 49) — this is the deliberately-included stale client quote required by check 20, superseded in the same email by the operative 24-month correction at line 12. Flagging this explicitly so it isn't mistaken for an unnoticed 36-month term: check 8 is being read as applying to *operative* values, and check 20 mandates the stale value's presence, so there is no actual conflict — just worth stating rather than resolving silently. |
| 9 | Every contract has signature block (both parties), execution date, consideration recital | PASS | All 9 confirmed individually: each has a "Consideration" recital or section, "IN WITNESS WHEREOF" execution language, a named signatory for each party, and a date for each signature. Contract 6 (Vantage/Okonkwo, `.txt`) was checked in full to the "END OF DOCUMENT" marker specifically because the employer signatory (Rosalind Ferraro) and employee (Daniel Okonkwo) sit on different lines than the dates — both names confirmed present. |
| 10 | Contract 5 has express reformation; contract 6 does not; NY partial-enforcement (1,2,3) is not reformation | PASS | Whole-corpus search for "reform" (newline-tolerant): present only in contracts 5, 7, 8, 9 (5 = CT express reformation; 7/8/9 = NJ reformation, expected separately per manifest). Absent from 1, 2, 3, 4, 6. Contract 6's severability section was read in full — bare 4c text, no reformation, no partial-enforcement sentence, matching the manifest's explicit "omit any reformation language entirely" instruction. Contracts 1/2/3's "Partial Enforcement" sections were read verbatim — all use "enforced ... to the extent the court deems reasonable" / "partial enforcement," never "reform" or "modify" — genuinely a different mechanism (blue-pencil/partial-enforcement vs. affirmative judicial reformation). |
| 11 | No two contracts share an identical provision set | PASS | Computed each contract's tuple of (state, ancillary_provisions, customer_nonsolicit_style, confidentiality_variant, severability_form, special_core_flags, employee_no_hire) from the manifest — all 9 tuples distinct (verified programmatically, zero duplicate keys). Then independently verified against the **rendered documents** (not just the manifest) that each contract's ancillary-provision set matches what's actually in the text: checked presence/absence of return-of-property, assignment-of-inventions, injunctive relief, integration, non-disparagement, tolling, attorneys' fees, at-will disclaimer, notice, survival, assignment/successors, forum selection, and jury-waiver clauses across all 9 files — every contract's rendered set matches its manifest row exactly. |
| 12 | Confidentiality/Trade Secrets in contracts from all 3 states | PASS | "Confidential" found in all 9 rendered contracts (grep, case-insensitive) — trivially covers all 3 states since all 9 contracts have it. |
| 13 | Customer Non-Solicitation in contracts from all 3 states (1,9=NY+NJ; 2=NY; 5,4=CT; 8=NJ) | PASS | Rendered customer/patient non-solicit clauses found in exactly 1, 2, 4 (as patient non-solicit), 5, 8, 9 — matching manifest states NY(1,2), CT(4,5), NJ(8,9). Absent from 3, 6, 7 as expected. |
| 14 | Single-state types: garden leave (NJ/7 only), mandatory arbitration (NY/3 only), termination-without-cause carve-out (CT/4 only) | PASS | Corpus-wide grep for each phrase against all 9 rendered contracts: each hits exactly one contract and zero others — garden leave only in 7, arbitration only in 3, termination-without-cause carve-out only in 4. |
| 15 | Three customer non-solicit stylings are materially distinct, not reworded synonyms | PASS (judged directly) | Read all three stylings verbatim. Style A (1, 9): numbered "Schedule A — [Scheduled/Restricted] Customers" exhibit with an enumerated named-customer list (8 names each), formal third-person "Employee shall not... solicit, call upon, or accept business from any customer identified on Schedule A." Style B (2, 5, 8): abstract two-part defined-term test — "Restricted Customer" (met by a 24-month "Lookback Period") AND "Material Contact" (a four-part definition: dealt with, supervised, learned Confidential Information about, or was compensated on) — no named list at all, a functional test instead. Style C (4): second-person, plain-English, patient-framed prose ("When you leave the Company... you agree that... you will not try to take the Company's patients with you") with zero defined terms and zero occurrences of "client" (checked: 0 hits) against 26 occurrences of "patient." These are three genuinely different drafting architectures (exhibit-based, definitional-test-based, plain-English-narrative), not three phrasings of one clause — my own judgment concurs with the design intent. |
| 16 | Supplier/vendor non-solicitation and training-cost repayment: zero in `contracts/`, present in `to-do/` | PASS | Corpus-wide search for "supplier"/"vendor": hits in contracts 1, 2, 4, 6, 7, 8, every one of them inside a confidentiality-information enumeration (e.g., "research and development materials, supplier and vendor information, personnel information..."). A targeted regex requiring a restriction verb (solicit/contact/induce/divert/do business with) within ~30 characters of "supplier"/"vendor" returned **zero hits anywhere in the corpus** — no restriction is attached to any mention. Training/tuition/certification-cost/repay/clawback search returned zero hits in any contract; the one "certif-" hit in contract 4 ("shall maintain hospital privileges, credentialing, and any facility-specific certifications... board certification in cardiovascular disease") is a physician-qualifications representation, not a clawback, confirmed by reading the surrounding sentence. Both gap provisions are present in `to-do/`: supplier non-solicitation requested in email 001 line 34 ("something that stops her going after their reagent suppliers... poaching them, redirecting orders"), training-cost repayment requested in email 002 lines 22–28 ("repay the firm for the certification costs... tied to that same two-year window") and referenced again in email 003 line 21. |
| 17 | All six variables + governing state recoverable from each email | PASS | Extracted independently by reading each email cold, then compared to the answer key's expected column: 001 (Merrivale Diagnostics Inc. / Serena Adeoye / Director of Assay Development / a year and a half / five boroughs+Long Island+Westchester / in-vitro diagnostics-assay/reagent / NY), 002 (Pell & Ottway Wealth Partners LLC / Colin Mazur / Senior Portfolio Manager / 24 months / Fairfield County+Manhattan office / wealth management, not institutional / CT), 003 (Quarrymount Beverage Co., Newark / Tanya Brissett / VP of National Accounts / two years / national / non-alcoholic craft beverage + energy drinks / NJ). All matched the answer key on independent re-extraction — no self-agreement, values were pulled from the raw email text first. |
| 18 | None of the six sits on a labelled line/form field/list | **FAIL** (one instance) | See defect list — email 002's Subject line contains the full employee name. The same completeness test was applied to every labelled header line in all three emails, not just Subject lines: `From:`/`To:` lines in all three emails name only the drafting lawyers (Calloway, Ilo, Okafor, Lindqvist) and each other — none of the six variables — so those don't trip the check. Email 002's `From:` (forwarded block, line 37) is `hpell@pellottway.com`; that domain, and the filename `002_2026-02-04_pell-ottway.txt`, yield only a short/informal form of the company, not the complete required value "Pell & Ottway Wealth Partners LLC" — the same standard already applied to 001's Subject line ("Merrivale") and 003's Subject line ("Quarrymount"), both of which are informal short forms, not complete values, and so don't trip the check either. Only 002's Subject line carries a *complete* value on a labelled line. No tables, form fields, or bulleted lists exist in any of the three emails. |
| 19 | Email 001: duration "a year and a half," no numeral form; geography has all 3 legs | PASS | `grep -n "18"` on the full email → no match; `grep -n "[0-9]"` → only the 2026-01-22 date line. Each geography leg checked separately: "five boroughs" (line 18), "Long Island" (line 18), "Westchester" (line 19) — all three present, all three in one prose sentence, none itemized as a list. |
| 20 | Email 002: stale (3yr/everywhere) + correction (24mo/Fairfield+Manhattan) present, correction above quote | PASS | Stale value at forwarded-block lines 49–50 ("I'd like three years... cover everywhere we do business"). Correction at lines 12–15 ("Cap the term at twenty-four months... Fairfield County plus the Manhattan office"). Correction (lines 12–15) sits above the quoted/forwarded block (starts line 36) — confirmed by direct line-number comparison, not estimation. |
| 21 | Email 003: decoy (Desmond Okafor, different role) differs from real hire; real role stated once, late | PASS | Decoy confirmed: "Desmond Okafor... was up for... a Director of Trade Marketing job... pulled out of the process" (lines 27–29), explicitly different from Tanya Brissett / VP of National Accounts. Exact-string count of "VP of National Accounts" in the file: **1 occurrence**, at line 63 of 74 (85% through the email). Near-miss phrases checked and confirmed non-matching: "accounts leadership role" (line 26, refers to the decoy's opening), "national accounts desk" (line 36, describes her *prior* job, not her new title), "accounts person" (line 61, informal aside, immediately followed by the correction to the real title). |
| 22 | No case name/reporter citation/statute section anywhere in `contracts/` or `to-do/` | PASS | Regex sweep for `§, Sec\., N.J.S.A, Conn. Gen, Stat., Public Act, U.S.C., C.F.R., F.3d, A.2d, N.Y.2d` and the `Name v. Name` pattern across all extracted contract/email text: zero hits. Extended the check beyond `python-docx`'s paragraph/table model: unzipped all 4 `.docx` files and grepped the raw `word/document.xml`, `comments.xml`, and `footnotes.xml` directly (no header/footer parts exist in these files at all) — still zero hits, closing the risk that citation text could live somewhere `python-docx`'s object model doesn't walk. Also ran `strings` against the 4 raw PDF files directly as a second, extraction-independent pass — zero hits. |
| 23 | Contract 4's physician-statute reference is conditional on CITATION-DECISION.md saying "verified" | PASS | `CITATION-DECISION.md` records the decision as **"Omitted,"** not "verified" — meaning any statute number in contract 4 would be a defect. Independently confirmed (check 22's sweep plus a targeted read of contract 4 in full) that contract 4 contains no statute number, section citation, or named authority anywhere; the physician-specific narrowing is expressed entirely as plain contract terms (12-month/15-mile restriction, reasonableness acknowledgment, termination-without-cause carve-out, continuity-of-care provision) exactly as the decision record describes. No inconsistency. |
| 24 | Contract 3's federal savings clause names no agency/rule/citation/date | PASS | Full clause read: "FEDERAL LAW SAVINGS CLAUSE — If any federal rule or regulation restricting non-competition covenants applies to you and makes any restriction in this Agreement unenforceable, that restriction shall not apply to you to the extent required by that rule or regulation..." No agency name, rule name, citation, or effective date anywhere in it. |
| 25 | No party/company/person name reads as a real entity; email domains invented | PASS | Enumerated and reviewed: 9 manifest employers, 9 employee names, all 9 contract signatories (Frances Odom, Colm Feeney, Marcus Delvecchio, Howard Merrow M.D., Patrick Donnelly, Rosalind Ferraro, Priya Nakamura, Harold Bramwell III, Denise Okafor), all 16 Schedule A customer entities (contracts 1 and 9), the 3 to-do companies (Merrivale Diagnostics Inc., Pell & Ottway Wealth Partners LLC, Quarrymount Beverage Co.), and both email domains actually used in the to-do files (`halloranvance.net`, `pellottway.com`, extracted programmatically from every `To:`/`From:` line — only two domains appear across all three emails). None reads as a real, identifiable company or a real public figure to me. Domains are plausible-but-invented law-firm/client domains. One naming-collision observation, not a check failure: three unrelated "Okafor"s appear across the corpus (Diane Okafor, the CT lawyer; Desmond Okafor, the decoy candidate; Denise Okafor, the Larkspur HVAC signatory), two "Priya"s (Raghunathan, Nakamura), and contract 1's Schedule A lists a customer "Fenwick Medical Center" while contract 4's employee is "Alina Fenwick, M.D." Email 003 explicitly lampshades the Diane/Desmond collision ("no relation to Diane, different Okafor, funny coincidence"); the Denise Okafor and Fenwick instances are unlampshaded coincidences sitting in the contracts. None of these reads as a real entity, so it doesn't fail check 25, but it slightly muddies the "decoy" teaching device if a reader notices it — worth a light mention. |
| 26 | Answer key claims zero mismatches — spot-checked independently | PASS | Independently re-verified **six** rows (more than the required five) directly against rendered files, not the key's prose: (1) contract 4 geography — rendered text reads "within a fifteen (15) mile radius of the Practice Site," confirms the key's spec-vs-manifest resolution. (2) contract 1 Schedule A — counted 8 named customers directly, matches. (3) contract 9 Schedule A — counted 8 named customers directly, matches. (4) email 002 correction-above-quote — confirmed by raw line numbers (12–15 vs. 36+), not by re-reading the key's claim. (5) contract 3's arbitration clause wording — rendered text reads verbatim "Except for claims seeking injunctive or other equitable relief," exactly as the key states, with no dangling section cross-reference. (6) contract 6 signature block — confirmed both Rosalind Ferraro and Daniel Okonkwo present by name, matching the key. All six held up. One very minor imprecision noted, not counted as a mismatch: the key describes contract 2's "unique and extraordinary" phrase as appearing "twice" (WHEREAS recital + body reinforcement); a literal case-insensitive string count returns 3 raw hits because the phrase also appears once, verbatim, as the heading of Section 3 ("Unique and Extraordinary Services") — the key's substantive claim (present in contract 2, and separately once in contract 1 despite its `special_core_flags` reading "none") is still correct, it just didn't count the section heading as a separate "appearance." Given six independent, un-agreed-with-in-advance spot checks all held, the key's zero-mismatch claim is genuine, not self-agreement. |

---

## Defect list

### 1. (Low severity) Email 002's Subject line exposes the employee name on a labelled line

**File:** `content/21-challenges/materials/challenge-two/to-do/002_2026-02-04_pell-ottway.txt`, line 4.

**What's wrong:** The header reads `Subject: Fwd: Colin Mazur -- noncompete terms`. Check 18 requires that none of the six recoverable variables — company, employee name, employee role, duration, geographic scope, industry — sit on "a labelled line, a form field, or in a list." `Subject:` is a labelled header field, and it carries the complete, exact employee-name value ("Colin Mazur") with no need to read any prose to recover it. This is a mechanical, literal violation of the check as written, on one of the six variables, in one of the three emails.

**Mitigation already present:** The same name also appears independently in prose at line 20 ("Colin Mazur is coming in as Senior Portfolio Manager there..."), so the exercise this corpus supports (searching by meaning rather than scanning labelled fields) is not fully defeated for this email — a reader could still find the name the intended way. This is why the defect is rated low severity rather than a corpus-breaking flaw, but it is a real, checkable miss against the letter of check 18, not a matter of interpretation.

**Counter-argument considered and rejected:** One could argue `Subject:` is envelope metadata, categorically outside "the email" a reader parses as prose, and so outside the check's intent. I rejected that reading: the Subject line is rendered text sitting in the same `.txt` file as the body, a mechanical extraction pass sees it exactly as it sees the body, and check 18 states its rule ("None of the six sits on a labelled line...") with no stated exception for headers. Adopting the metadata-exception reading is the more sophisticated, tidier-report interpretation, which is exactly the kind of self-serving reading an adversarial QA pass should distrust rather than reach for.

**What would fix it:** Reword the Subject line to remove the full name, e.g. `Subject: Fwd: noncompete terms — new PM hire` or reference a matter/file number instead, consistent with how emails 001 and 003 keep their Subject lines to informal, incomplete company references only ("Merrivale — draft this one fast," "Quarrymount — long one, sorry, read the whole thing") rather than a complete recoverable value.

### No other defects found

Checks 1–17 and 19–26 all passed independent, mechanical re-verification against
the rendered files (not the manifest's or the answer key's claims). The
provision matrix, the two deliberate gaps, the reformation/partial-enforcement
distinction, the citation-freedom checks (including a docx-internal-XML and
raw-PDF-bytes pass beyond what `python-docx`/`fitz`'s normal object models
expose), and the answer key's own zero-mismatch claim (spot-checked on six
independently-selected rows, not five) all held up.

---

## Remediation (2026-08-29)

All four fixes below were applied to the source files under
`lab/challenge-two/sources/` and the corpus was re-rendered with
`bash lab/challenge-two/build.sh`. The original verdict and check table
above are left unmodified as the historical record of the QA pass that
found these issues.

### 1. Check 18 — email 002 Subject line named the employee on a header line

**File:** `lab/challenge-two/sources/to-do/002_2026-02-04_pell-ottway.txt`

- Line 4: `Subject: Fwd: Colin Mazur -- noncompete terms` → `Subject: Fwd: noncompete terms -- new PM hire`
- Line 39 (quoted original): `> Subject: Colin Mazur - need paper before he starts` → `> Subject: new hire - need paper before he starts`

Nothing else in the file changed (line count unchanged, 56 lines before and
after; both edits confirmed by `diff` against a pre-edit snapshot). The
full name remains in body prose at "Colin Mazur is coming in as Senior
Portfolio Manager there..." (line 20), so the check-18 requirement — no
complete value of any of the six variables on a labelled line — is now met
without weakening the exercise. The other two emails' header lines were
re-checked against the same standard: 001's "Merrivale" (Subject line) and
003's "Quarrymount" (Subject line) remain informal short forms of the
company names, not complete legal-name values, so per the standard already
applied to them they were left unchanged.

### 2. "Okafor" collision — contract 9 signatory renamed

**File:** `lab/challenge-two/sources/contracts/09-larkspur-nj.md`, line 64.

`Name: Denise Okafor` → `Name: Yolanda Prescott`

Diane Okafor (email 002/003) and Desmond Okafor (email 003's decoy
candidate) are untouched. Grep of `lab/challenge-two/sources/` for
"Denise Okafor" and for "Yolanda"/"Prescott" individually confirms zero
remaining hits of the old name and zero pre-existing hits of the new one
before the edit.

### 3. "Fenwick" collision — contract 1 Schedule A customer renamed

**File:** `lab/challenge-two/sources/contracts/01-halvorsen-ny.md`, line 117.

`6. Fenwick Medical Center` → `6. Thistlewood Medical Center`

Contract 4's employee, Alina Fenwick, M.D., is untouched. Grep confirms
zero remaining "Fenwick Medical Center" hits and zero pre-existing
"Thistlewood" hits in `lab/challenge-two/sources/`.

### 4. "Priya" collision — contract signatory renamed

**Correction to the task's file pointer:** the task specified contract 8
(`08-bramwell-nj.md`) as the location of the second "Priya," but that file's
signatory is "Harold Bramwell III" (the company's eponym — `Bramwell
Specialty Foods Inc.`) and contains no "Priya" anywhere. The actual second
"Priya" is contract 7's signatory, in
`lab/challenge-two/sources/contracts/07-ardsleigh-nj.md`, line 112.

`Name: Priya Nakamura` → `Name: Renata Sloane`

Contract 2's employee, Priya Raghunathan, and contract 8's signatory,
Harold Bramwell III, are both untouched. Grep confirms zero remaining
"Priya Nakamura" hits and zero pre-existing "Renata"/"Sloane" hits in
`lab/challenge-two/sources/`.

**Also observed, not fixed:** "Harold" appears twice in the corpus —
Harold Pell (client contact, email 002) and Harold Bramwell III (contract 8
signatory, the company's own eponym). This is the same class of coincidence
as the three fixed above, but the task specified exactly four fixes and
renaming contract 8's signatory would break the founder-name/company-name
consistency that nothing asked to be broken. Flagging it for a future pass
rather than acting on it unilaterally.

### Re-render verification

- `content/21-challenges/materials/challenge-two/contracts/` has exactly 9
  files, `to-do/` has exactly 3, no subfolders, no leftover intermediate
  `.docx`.
- Format tally unchanged: 4 `.docx`, 4 `.pdf`, 1 `.txt`.
- Contract 1's rendered `.docx` (`python-docx` extraction) contains
  "Thistlewood" and no longer contains "Fenwick".
- Contract 7's rendered `.pdf` (`fitz`/PyMuPDF extraction) contains "Renata
  Sloane" and no longer contains "Priya" or "Nakamura".
- Contract 9's rendered `.pdf` (`fitz`/PyMuPDF extraction) contains "Yolanda
  Prescott" and no longer contains "Denise" or "Okafor".
- Contract 8's rendered `.docx` still contains "Harold Bramwell III" and no
  "Priya" — confirming it was correctly left untouched.
- Email 002's rendered copy is byte-identical (`cmp`) to its edited source;
  its rendered Subject lines no longer contain "Colin Mazur", which still
  appears once in the body.
- Contract 6's rendered `.txt` remains byte-identical (`cmp`) to
  `lab/challenge-two/sources/contracts/06-vantage-ct.txt`, unaffected by
  this remediation.

Nothing in `lab/challenge-three/`, `content/pipeline.md`, or
`content/index.json` was touched.

---

## Post-Remediation Verification

### Verdict: PASS (14 of 14 checks pass, 0 defects)

This is an independent re-verification pass, performed fresh against the
**rendered files only** (`content/21-challenges/materials/challenge-two/`),
not against the QA-REPORT's or the Remediation section's prose claims. All
12 rendered files (9 contracts, 3 to-do emails) were re-extracted from
scratch with `python-docx` (4 `.docx`), `fitz`/PyMuPDF (4 `.pdf`), and
`cat`/direct read (1 `.txt` contract + 3 `.txt` emails) into
`.scratch/verify_extracted/` (worktree-local, not part of the deliverable).
Nothing in `lab/challenge-three/`, `content/pipeline.md`, or
`content/index.json` was read for evidentiary purposes beyond a
non-modifying existence/JSON-validity check, and nothing outside this
report section was edited.

#### Part 1 — did the remediation land?

1. **Check 18 (original failure) — PASS.** Every labelled header line
   (`From:`/`To:`/`Date:`/`Subject:`) in all three rendered emails was read
   directly, including email 002's quoted forwarded-block headers. Email
   001: Subject is `Merrivale -- draft this one fast` (informal short form,
   not "Merrivale Diagnostics Inc."). Email 002: Subject is now `Fwd:
   noncompete terms -- new PM hire` (no name at all — the fix landed); the
   quoted `> Subject: new hire - need paper before he starts` (line 39) also
   no longer names Colin Mazur; the quoted `> From: Harold Pell
   <hpell@pellottway.com>` (line 37) yields only an informal domain
   fragment, not the complete legal name "Pell & Ottway Wealth Partners
   LLC." Email 003: Subject is `Quarrymount -- long one, sorry, read the
   whole thing` (informal short form only). No `From:`/`To:` line in any of
   the three emails names anyone but the drafting lawyers. No complete
   value of any of the six variables sits on any labelled header line in
   any of the three files.

2. **Email 002 integrity — PASS.** Confirmed by direct line read of
   `to-do/002_2026-02-04_pell-ottway.txt`: Diane's correction (lines 6–34)
   sits above the `---------- Forwarded message ----------` marker (line
   36) and the quoted block (lines 37–56, every line prefixed with `>`,
   markers intact). Stale values present: "three years" (lines 13 and 49)
   and "everywhere we do business" (line 50). Corrected values present:
   "twenty-four months" (line 12–13) and "Fairfield County plus the
   Manhattan office" (line 15). Training-cost-repayment request present at
   lines 22–28 ("if he leaves within two years, he has to repay the firm
   for the certification costs..."). "Colin Mazur" appears in body prose at
   line 20 ("Colin Mazur is coming in as Senior Portfolio Manager there...")
   and nowhere on a header line.

3. **The three renames — PASS.** Grepped the rendered (extracted) text of
   each file directly:
   - Contract 1 (`Halvorsen Medical Systems - Executed NC (Rourke).docx`):
     contains "Thistlewood Medical Center" (Schedule A, item 6); zero hits
     for "Fenwick."
   - Contract 7 (`Ardsleigh Capital - Noncompetition Agreement - Voss
     (EXECUTED).pdf`): signature block reads "Name: Renata Sloane"; zero
     hits for "Priya" or "Nakamura."
   - Contract 9 (`Copy of Noncompete - Larkspur HVAC (M. Duarte) FINAL.pdf`):
     signature block reads "Name: Yolanda Prescott"; zero hits for "Denise"
     or "Okafor."
   - Contract 4 (`Merrow Cardiology Associates...pdf`) still names "Alina
     Fenwick, M.D." (twice — recital and signature block), confirming this
     Fenwick was correctly left untouched.
   - Contract 2 (`NONCOMPETE_FINAL_v3.docx`) still names "Priya
     Raghunathan" (recital and signature block), confirming this Priya was
     correctly left untouched.

4. **"Okafor" scope — PASS.** `grep -l "Okafor"` across all 12 rendered
   extractions returns exactly two files: `002_2026-02-04_pell-ottway.txt`
   (Diane Okafor) and `003_2026-02-17_quarrymount-beverage.txt` (Desmond
   Okafor, the decoy, explicitly lampshaded as "no relation to Diane,
   different Okafor"). Zero hits in any of the 9 rendered contracts.

#### Part 2 — did the rebuild regress anything?

5. **File counts / structure — PASS.** `find` shows exactly 9 files
   directly under `contracts/` and 3 directly under `to-do/`; `find -type
   d` shows only the two expected subdirectories (no nested subfolders); a
   case-insensitive search for `*readme*`, `*notice*`, `*index*`,
   `*manifest*`, `.gitkeep` anywhere under `challenge-two/` returns no
   hits; no leftover intermediate `.docx` beyond the 4 that belong in
   `contracts/` (verified by `find -iname "*.docx"` returning exactly those
   4, and no hidden files anywhere in the tree).

6. **Format tally / filenames — PASS.** `ls contracts | sed 's/.*\.//' |
   sort | uniq -c` → 4 docx, 4 pdf, 1 txt. Programmatic set comparison
   (Python `csv.DictReader` on `manifest.tsv`'s `output_filename` column vs
   `os.listdir` on the rendered `contracts/` directory) → `expected ==
   actual` is `True`, zero differences either direction.

7. **Extraction clean/non-empty, producers distinguishable — PASS.** All 12
   rendered files extracted non-empty (1,846–17,859 characters, no
   failures, no exceptions). PDF producer metadata: contracts 3 and 9 →
   `producer: ReportLab PDF Library - (opensource)`; contracts 4 and 7 →
   `producer: LibreOffice 26.2.3.2 (AARCH64)`, `creator: Writer` — matches
   the manifest's reportlab→{3,9}, soffice→{4,7} assignment and remains
   cleanly separable. All 4 `.docx` files carry `<Application>Microsoft
   Word 12.0.0</Application>` in `docProps/app.xml` (pandoc's fixed
   signature).

8. **Contract 5 bold run-in lead-ins — PASS.** `python-docx` run-level
   inspection of `stonefield_noncompete_kilbride.docx` finds 13 distinct
   bold runs, each a clause lead-in ("Background and Consideration.",
   "Non-Competition.", "Non-Solicitation of Customers.", ...,
   "Severability; Reformation.", "Governing Law.", "Acknowledgment.") — the
   bolding survived pandoc as genuine run-level formatting, not flattened
   into plain prose.

9. **Contract 6 byte-identical — PASS.** `cmp` between the rendered
   `Employment Agreement - Vantage Aerostructures - D Okonkwo.txt` and
   `lab/challenge-two/sources/contracts/06-vantage-ct.txt` reports no
   differences.

10. **Single-state provisions — PASS.** Corpus-wide regex sweep: "garden
    leave" hits only contract 7 (8 occurrences, zero elsewhere);
    "arbitrat[e/ion]" hits only contract 3 (6 occurrences, zero elsewhere).
    "without cause" appears in 5 contracts (1, 3, 4, 7, 9), but reading each
    in context shows only contract 4 has the actual carve-out — "if the
    Company terminates Employee's employment without Cause..., the
    post-employment restriction on treating patients... shall not apply."
    Contracts 1, 3, 7, and 9 all use it as ordinary at-will/termination
    boilerplate ("with or without cause," describing how employment may
    end, not exempting the restriction). Because the check is semantic, not
    literal, both provisions were re-tested with wording-independent nets
    rather than trusting the label alone: a sweep for "shall/does/will not
    apply" across all 9 contracts returns only contract 3's unrelated
    federal-savings clause and contract 4's carve-out — nothing else in the
    corpus states that a restriction stops applying on any triggering
    condition. A sweep for "notice period / salary continuation / continue
    to pay / paid leave" across all 9 contracts returns hits only inside
    contract 7's Article VI ("place Employee on garden leave for up to
    ninety (90) days... shall continue to receive base [salary]... the
    Company shall continue to pay Employee for the remainder of..."),
    confirming the paid-notice mechanism itself, not just the label "garden
    leave," is single-state. Both provisions are confirmed single-state (CT
    carve-out/4, NJ garden leave/7; arbitration NY/3) under both a literal
    and a wording-independent search.

11. **The two deliberate gaps — PASS.** Every supplier/vendor mention in
    the corpus (contracts 1, 2, 4, 6, 7, 8) sits inside a confidentiality-
    information enumeration ("...research and development materials,
    supplier and vendor information, personnel information..." /
    "...pricing, margins, supplier terms..."); a regex requiring a
    restriction verb (solicit/contact/induce/divert/do business with)
    within ~40 characters of "supplier"/"vendor" returns zero matches
    anywhere in the corpus. Training/tuition/certification/repay/clawback
    sweep returns only false positives on inspection: "restraining"
    (substring of "train"), "certified mail" (contract 3), physician
    qualifications language (contract 4's "facility-specific
    certifications... board certification"), and "retrain a successor"
    (contract 8, an operational transition detail, not a repayment
    obligation) — no actual repayment/clawback provision anywhere in
    `contracts/`. Both gaps are requested in `to-do/`: supplier
    non-solicitation in email 001 ("he wants something that stops her going
    after their reagent suppliers... poaching them, redirecting orders");
    training-cost repayment in email 002 ("if he leaves within two years,
    he has to repay the firm for the certification costs..."), referenced
    again in email 003.

12. **Reformation — PASS.** "reform" hits contracts 5, 7, 8, 9 only,
    absent from 1, 2, 3, 6. Contract 5's clause ("Severability;
    Reformation... the parties intend for the court to modify and reform
    that restriction, rather than to void it entirely") is genuine express
    reformation. Contracts 7, 8, 9 (NJ) also reform, as the manifest
    specifies separately for that state. Contract 6's severability section
    was located by string search and its full text read (`SEVERABILITY.
    ... If any provision of this Agreement is held by a court of competent
    jurisdiction to be invalid, illegal, or unenforceable, that provision
    shall be struck from this Agreement...` immediately followed by the
    `GOVERNING LAW` section) — bare severability only, no reformation
    language, no partial-enforcement sentence, nothing truncated. Contracts
    1, 2, 3 (NY) were read in full: all three use "Partial Enforcement...
    enforced... to the extent the court deems reasonable, rather than
    [voided/thrown out] entirely" — genuinely distinct blue-pencil
    language, never "reform" or "modify." Since contract 5's own clause
    pairs "modify **and** reform," a reformation clause drafted with only
    the "modify" stem and not "reform" would be invisible to the `reform`
    grep alone, so a separate corpus-wide sweep for "modif" was run: it
    hits contracts 1, 2, and 8, but in 1 and 2 it is only the standard
    integration-clause boilerplate ("This Agreement may not be amended or
    modified except by a written instrument..."), not judicial reformation
    — contract 8's hit is its already-counted NJ reformation clause.
    Contracts 3 and 6 have zero "modif" hits. No modify-only reformation
    clause is hiding in 1, 2, 3, or 6.

13. **Term/geography caps — PASS.** Regex sweep of every `N (##) month`/
    `N (##) year` pattern across all 9 contracts found a maximum of 24
    months (contracts 5 and 8), nothing higher. A follow-up sweep for bare
    "year(s)" mentions not already covered by a parenthetical-months form
    found only non-duration boilerplate ("over many years," "a period of
    years," "in your last year there") — no disguised multi-year term. A
    third, broader sweep of every bare `months?` occurrence not already
    captured by a `(##) month` form (to catch spelled-out durations with no
    digit at all, e.g. "thirty-six months") found only "six-month"
    (contract 3) and "twenty-four-month" (contract 8, twice) — both already
    within the 24-month ceiling, nothing higher hiding in spelled-out form.
    The lone "internationally" hit (contract 2) sits in a WHEREAS recital
    describing the company's business generally, not the restrictive
    covenant's own "Territory" definition (which is the United States).

14. **No citations — PASS.** A regex sweep for `§`, `Sec.` + digit,
    `N.J.S.A`, `Conn. Gen`, `Stat.` + digit, `Public Act`, `U.S.C`, `C.F.R`,
    `F.3d`, `A.2d`, `N.Y.2d`, and the `Name v. Name` pattern across all 12
    rendered extractions returned zero hits. `CITATION-DECISION.md` records
    contract 4's decision as "Omitted," and contract 4's rendered text was
    checked specifically — no statute number, section number, or named
    authority anywhere in it; the physician-specific narrowing (12-month/
    15-mile radius, reasonableness acknowledgment, termination-without-
    cause carve-out) is expressed entirely in plain contract terms.

#### Defect list

None found. All 14 checks pass against the rendered files.

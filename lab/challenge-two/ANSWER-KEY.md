# Challenge Two — Answer Key

Expected values below are taken **only** from the task specification and
from `lab/challenge-two/sources/manifest.tsv` (plus, for section 4 of
Table 2, the clause text in `lab/challenge-two/sources/shared-provisions.md`,
which the manifest points to). None of the "expected" cells were written by
reading the rendered documents. Rendered values were then read back from
the built files in `content/21-challenges/materials/challenge-two/` and
compared. Text comparison was done on whitespace-and-quote-normalized
extracted text (curly quotes/dashes folded to ASCII, runs of whitespace
collapsed) so that PDF hard-wrapping and typography did not produce false
mismatches; matches below are semantic/substantive, not brittle exact-string
matches, and any place a match required interpreting paraphrase-vs-verbatim
is noted.

**Post-QA remediation (2026-08-29):** independent QA (see `QA-REPORT.md`)
found one real defect (check 18) and three cosmetic naming collisions; all
four were fixed in the source files and the corpus was re-rendered. Check
18's fix changed email 002's Subject line wording only — see the note on
the `002 | employee` row below. Corpus mismatches remained **0** throughout,
since each rename's source and rendered value were changed together;
nothing below needed a value change as a result. Details in the
"Remediation" section appended to `QA-REPORT.md`.

## Table 1 — Intake Emails

| email | field | expected | rendered | match? | notes |
|---|---|---|---|---|---|
| 001 (Merrivale) | company | Merrivale Diagnostics Inc. | Merrivale Diagnostics Inc. | match | |
| 001 | employee | Serena Adeoye | Serena Adeoye | match | |
| 001 | role | Director of Assay Development | Director of Assay Development | match | |
| 001 | duration | "a year and a half" (=18 months), **no numeral form** | "a year and a half" is the only duration phrase in the file; the file's only digits are the 2026-01-22 date | match | confirmed programmatically — no numeral duration (e.g. "18") appears anywhere in the email |
| 001 | geography | all three legs required: "the five boroughs", "Long Island", "up through Westchester" | all three legs present, each independently confirmed | match | checked each leg separately per instruction |
| 001 | industry | in-vitro diagnostics, assay development and reagent work | "in-vitro diagnostics" scope, narrowed to "assay development and reagent work" ("reagent chemistry side") | match | |
| 001 | governing state | New York | "Governing law is New York" (explicitly kept separate from territory) | match | |
| 001 | gap provision requested | supplier non-solicitation (reagent suppliers) | CEO asks for something to stop her "going after their reagent suppliers" — poaching/redirecting orders | match | this is a client request in the email, not a request that it appear in a rendered contract; confirmed absent from `contracts/` in Table 3 |
| 002 (Pell & Ottway) | company | Pell & Ottway Wealth Partners LLC | Pell & Ottway Wealth Partners LLC | match | |
| 002 | employee | Colin Mazur | Colin Mazur | match | check-18 remediation: the name was removed from the Subject line (both the live header and the quoted original's header) and now appears only in body prose, at the same location cited above; this does not change the match |
| 002 | role | Senior Portfolio Manager | Senior Portfolio Manager | match | |
| 002 | industry | wealth management, high-net-worth advisory, not institutional | "wealth management and high-net-worth advisory work," explicitly "not the institutional side" | match | |
| 002 | governing state | Connecticut | "Connecticut governs, obviously, this whole file is Connecticut" | match | |
| 002 | gap provision requested | training-cost repayment (sponsored certification costs if leaves within 2 years) | Diane: repay "certification costs" (exam sequence + study materials) if he leaves within two years | match | |
| 002 | stale value (quoted client original) | term: three years; geography: "everywhere we do business" | Harold's forwarded email: "I'd like three years... cover everywhere we do business" | match | |
| 002 | corrected value (operative) | term: 24 months; geography: Fairfield County + Manhattan office | Diane: "Cap the term at twenty-four months"; "narrow the territory way down: Fairfield County plus the Manhattan office" | match | |
| 002 | correction position | correction must appear above the quoted block | Diane's correction is at lines 12–15 of the email body; the forwarded/quoted block starts at line 36 | match | confirmed by line position |
| 003 (Quarrymount) | company | Quarrymount Beverage Co. (Newark) | Quarrymount Beverage Co., based in Newark | match | |
| 003 | employee | Tanya Brissett | Tanya Brissett | match | |
| 003 | role | VP of National Accounts (stated once, late) | stated once, near the end of the email ("the title on the offer letter is VP of National Accounts") | match | |
| 003 | duration | two years (24 months) | "running two years... just use it" | match | |
| 003 | geography | national | "whatever we draft on territory needs to be national" | match | |
| 003 | industry | non-alcoholic craft beverage plus energy drinks | "non-alcoholic craft beverage side"... "energy drinks folded into the restricted subject matter" | match | |
| 003 | governing state | New Jersey | "they want New Jersey to govern" | match | |
| 003 | decoy | Desmond Okafor, a withdrawn candidate for a **different** role (Director of Trade Marketing) | Desmond Okafor — "no relation to Diane" — was up for "a Director of Trade Marketing job" and "pulled out of the process" | match | name and role both confirmed to differ from the real hire (Tanya Brissett / VP of National Accounts) |

**Table 1 mismatches: 0.**

All three to-do files in `content/21-challenges/materials/challenge-two/to-do/`
were also confirmed byte-identical (via `cmp`) to their sources in
`lab/challenge-two/sources/to-do/`, so every fact above that is true of the
source email is necessarily true of the rendered copy.

## Table 2 — Contracts

Expected values below are transcribed from the spec table in the task and
from `manifest.tsv`; where the spec table and the manifest diverge in
specificity (contract 4's geography: manifest only says "fixed short radius
of primary practice site," the spec pins it at "15-mile radius"), the spec
value is used as expected, and that is flagged.

| n | field | expected | rendered | match? | notes |
|---|---|---|---|---|---|
| 1 | state / employer / employee / role | NY / Halvorsen Medical Systems Inc. / Dana Rourke / Regional Sales Director | all four found verbatim | match | |
| 1 | industry | surgical navigation devices | doc describes "surgical navigation systems and related image-guided surgical technology" | match | same industry, non-verbatim paraphrase in the drafted recitals — not a defect |
| 1 | term | 12 months | "twelve (12) months" | match | |
| 1 | geography | counties where the Company had an office or the employee had customer responsibility in the final 24 months | "Restricted Area" defined exactly this way: counties with a Company office, or where Employee had customer responsibility, in each case during the final twenty-four (24) months | match | |
| 1 | producer / format | pandoc-docx / .docx | pandoc-docx / .docx | match | |
| 1 | provisions | Confidentiality (canonical); Customer Non-Solicit Style A + attached Schedule A (8 named customers); no employee no-hire; severability bare + NY partial-enforcement sentence (not reformation); ancillary: return of property, assignment of inventions, injunctive relief, integration/entire agreement; NY governing law | all present as expected; Schedule A is attached and populated (8 customer names) | match | |
| 2 | state / employer / employee / role | NY / Ostrander Brand Group LLC / Priya Raghunathan / VP, Brand Strategy | all found; role rendered as "Vice President, Brand Strategy" | match | "VP" spelled out as "Vice President" — same role, not a defect |
| 2 | industry | cosmetics and personal care | matches | match | |
| 2 | term | 18 months | "eighteen (18) months" | match | |
| 2 | geography | the United States | "the United States" | match | |
| 2 | producer / format | pandoc-docx / .docx | pandoc-docx / .docx | match | |
| 2 | provisions | Confidentiality (variant 1); Customer Non-Solicit Style B; employee no-hire canonical (5a); severability bare + NY partial-enforcement sentence; ancillary: return of property, non-disparagement, tolling, injunctive relief, attorneys' fees, integration; special flag "unique and extraordinary services" recital; NY governing law | all present as expected; "unique and extraordinary" confirmed present twice (once in a WHEREAS recital, once reinforced later in the body) | match | contract 1 also contains the phrase once ("Employee will render unique and extraordinary services to the Company") despite its `special_core_flags` column reading `none` — that column carries posture labels (`aggressive`, `tight, appropriately narrow`, `broad geography`, etc.), not an exclusive per-phrase assignment, so this is not treated as a defect. No other contract contains the phrase. |
| 3 | state / employer / employee / role | NY / Kestrel Freight Partners Inc. / Anand Bhatt / Operations Manager | all found verbatim | match | |
| 3 | industry | freight brokerage and logistics | matches | match | |
| 3 | term | 6 months | "six-month duration" / "six (6) months" | match | |
| 3 | geography | 50 miles of the Maspeth terminal | "fifty-mile area," "office and terminal located at 47 Rust Street, Maspeth, New York" | match | numeral spelled as "fifty-mile," semantically identical |
| 3 | producer / format | reportlab-pdf / .pdf | reportlab-pdf / .pdf | match | |
| 3 | provisions | Confidentiality (variant 2); no customer non-solicit; no employee no-hire; severability bare + NY partial-enforcement sentence; ancillary: return of property, at-will disclaimer, notice; special flag mandatory arbitration; NY governing law | all present as expected | match | The library text for the arbitration clause (shared-provisions.md §12h) reads "Except for claims seeking injunctive relief under the Injunctive Relief Section above" — but contract 3's ancillary list has no separate Injunctive Relief section. Checked directly: the rendered clause reads "Except for claims seeking injunctive **or other equitable relief**," with no cross-reference to a named section. The clause was correctly adapted for a contract lacking a standalone Injunctive Relief section — not a dangling cross-reference, and not a defect. |
| 4 | state / employer / employee / role | CT / Merrow Cardiology Associates PC / Alina Fenwick, M.D. / Interventional Cardiologist | all found verbatim | match | |
| 4 | industry | cardiology practice | matches | match | |
| 4 | term | 12 months | "twelve (12) months" | match | |
| 4 | geography | 15-mile radius of the primary practice site (spec value; manifest only says "fixed short radius") | "within a fifteen (15) mile radius of the Practice Site" | match | spec and manifest diverge in specificity here; spec's 15-mile figure is confirmed correct against the rendered document |
| 4 | producer / format | soffice-pdf / .pdf | soffice-pdf / .pdf | match | |
| 4 | provisions | Confidentiality (canonical); Customer Non-Solicit Style C reframed as patient non-solicitation; no employee no-hire; severability bare, **no partial-enforcement sentence** (CT, not NY); ancillary: return of property, injunctive relief, survival; special flag termination-without-cause carve-out (releases both the geographic noncompete and the patient non-solicitation); CT governing law | all present as expected; severability is the bare 4c text with no reformation and, correctly, no NY-style partial-enforcement addendum (that addendum is NY-only per the spec) | match | initial automated pass flagged "missing partial-enforcement sentence" here — that was a script error (grouping contract 4 with the NY bare-severability contracts); on manual reread it is correctly bare with no such sentence, since contract 4 is CT. The Style C reframe was verified directly: the section is headed "Non-Solicitation of Patients / Not Taking Patients With You," uses "patient" 26 times, and the word "client" does not appear anywhere in the document (0 occurrences) — confirming a complete replacement of clients→patients and business→care, not a partial or leftover reframe. |
| 5 | state / employer / employee / role | CT / Stonefield Insurance Brokers LLC / Margaret Kilbride / Commercial Lines Producer | all found verbatim | match | |
| 5 | industry | commercial insurance brokerage | matches | match | |
| 5 | term | 24 months | "twenty-four (24) months" | match | |
| 5 | geography | Fairfield, New Haven and Hartford Counties | "Fairfield County, New Haven County, or Hartford County, Connecticut" | match | |
| 5 | producer / format | pandoc-docx / .docx | pandoc-docx / .docx | match | |
| 5 | provisions | Confidentiality (variant 2); Customer Non-Solicit Style B; employee no-hire variant (5b); severability **CT express reformation** ("Severability; Reformation"); ancillary: return of property, non-disparagement, injunctive relief, attorneys' fees, assignment and successors; CT governing law | all present as expected | match | see also the dedicated bold-run-in check below |
| 6 | state / employer / employee / role | CT / Vantage Aerostructures Corp. / Daniel Okonkwo / Manufacturing Process Engineer | all found verbatim | match | |
| 6 | industry | aerospace components | matches | match | |
| 6 | term | 18 months | "eighteen (18) months" | match | |
| 6 | geography | any US facility designing or making Competing Products | "Facility" defined as any plant/factory/laboratory "wherever situated within the United States" at which work on "Competing Products" is carried out | match | |
| 6 | producer / format | copy-txt / .txt | copy-txt / .txt | match | see byte-identity check below |
| 6 | provisions | Confidentiality (variant 1); no customer non-solicit; no employee no-hire; severability **bare, explicitly no reformation power and no partial-enforcement sentence**; ancillary: assignment of inventions, tolling, injunctive relief, forum selection; CT governing law | all present as expected; confirmed no "reform" language and no partial-enforcement sentence anywhere in the document | match | |
| 7 | state / employer / employee / role | NJ / Ardsleigh Capital Management LLC / Theo Voss / Head of Quantitative Research | all found verbatim | match | |
| 7 | industry | asset management | matches | match | |
| 7 | term | 12 months | "twelve (12) months" | match | |
| 7 | geography | the United States | "the United States" | match | |
| 7 | producer / format | soffice-pdf / .pdf | soffice-pdf / .pdf | match | |
| 7 | provisions | Confidentiality (canonical); no customer non-solicit; employee no-hire canonical (5a); severability **NJ reformation**; ancillary: return of property, non-disparagement, attorneys' fees, assignment and successors, jury waiver; special flag garden leave / paid notice period; NJ governing law | all present as expected | match | |
| 8 | state / employer / employee / role | NJ / Bramwell Specialty Foods Inc. / Gina Esposito / National Accounts Manager | all found verbatim | match | |
| 8 | industry | specialty food distribution | "sourcing, marketing, and distributing specialty and gourmet food products" | match | |
| 8 | term | 24 months | "twenty-four (24) months" | match | |
| 8 | geography | any state where the Company sold Products during employment | "Territory" defined as "each state of the United States in which the Company sold Products at any time during Employee's employment" | match | |
| 8 | producer / format | pandoc-docx / .docx | pandoc-docx / .docx | match | |
| 8 | provisions | Confidentiality (variant 1); Customer Non-Solicit Style B; employee no-hire variant (5b); severability **NJ reformation**; ancillary: assignment of inventions, tolling, injunctive relief, integration, forum selection; NJ governing law | all present as expected | match | |
| 9 | state / employer / employee / role | NJ / Larkspur Mechanical Services LLC / Miguel Duarte / Service Technician Supervisor | all found verbatim | match | |
| 9 | industry | commercial HVAC contracting | "installs, services, and maintains commercial heating, ventilation, and air conditioning systems for commercial building owners" | match | |
| 9 | term | 9 months | "nine (9) months" | match | |
| 9 | geography | 30 miles of any Company branch where the employee worked | "within thirty (30) miles of any Company branch location at which Employee worked" | match | |
| 9 | producer / format | reportlab-pdf / .pdf | reportlab-pdf / .pdf | match | |
| 9 | provisions | Confidentiality (variant 2); Customer Non-Solicit Style A + attached Schedule A (8 named customers); no employee no-hire; severability **NJ reformation**; ancillary: return of property, at-will disclaimer, survival; NJ governing law | all present as expected; Schedule A attached and populated (8 customer names); "SURVIVAL" heading present | match | initial automated pass flagged "missing survival clause" — script bug (marker required a trailing period that the PDF-extracted, all-caps heading doesn't have); manual reread confirms the survival clause text is present in full |

**Table 2 mismatches: 0.**

Producer/format tally confirmed independently in Part A: 4 `.docx`
(contracts 1, 2, 5, 8) via pandoc-docx, 4 `.pdf` split 2 reportlab (3, 9) /
2 soffice (4, 7), 1 `.txt` (6) via copy-txt — matches the manifest and the
spec table exactly.

## Table 3 — Provision Matrix

| provision type | expected scope / location | rendered scope / location | match? | notes |
|---|---|---|---|---|
| Confidentiality / Trade Secrets | all 9 contracts; appears in contracts from all three states (NY 1–3, CT 4–6, NJ 7–9) | present in all 9, correct variant per contract (canonical: 1,4,7; variant 1: 2,6,8; variant 2: 3,5,9) | match | cross-state, trivially and by construction |
| Customer Non-Solicitation | present in contracts from all three states; absent from contracts 3, 6, 7 | present in 1,2,4,5,8,9 (NY: 1,2; CT: 4,5; NJ: 8,9); absent from 3,6,7 (one per state) | match | cross-state confirmed |
| Governing Law | all 9 contracts, trivially cross-state | present in all 9, correct state each time | match | |
| Garden leave / paid notice period | NJ only — contract 7 | found only in contract 7; absent from all other 8 | match | |
| Mandatory arbitration | NY only — contract 3 | found only in contract 3; absent from all other 8 | match | |
| Termination-without-cause carve-out | CT only — contract 4 | found only in contract 4; absent from all other 8 | match | |
| Customer non-solicit Style A (schedule/enumerated) | contracts 1, 9 | contracts 1, 9, each with an attached, populated Schedule A | match | |
| Customer non-solicit Style B (lookback/material contact) | contracts 2, 5, 8 | contracts 2, 5, 8 | match | |
| Customer non-solicit Style C (plain English, patient non-solicitation) | contract 4 only | contract 4 only, reframed to "patients"/"care" per the shared-provisions instruction | match | |
| Gap: supplier/vendor non-solicitation | absent from all 9 contracts | absent from all 9 — "supplier"/"vendor" appear only inside confidentiality-information enumerations (e.g. "supplier and vendor information," "supplier terms") in contracts 1, 2, 4, 6, 7, 8; no restriction (solicit/contact/induce/divert/do-business-with/poach) is attached to any of those mentions in any contract | match | judged by presence of a restriction, not the bare word, per instruction |
| Gap: training-cost repayment / clawback | absent from all 9 contracts | no occurrence of repayment/clawback/tuition/certification-cost/licensing-cost/training-cost language anywhere in `contracts/`; the one "certif-" hit outside contract 3's boilerplate "certified mail" is in contract 4, and is a physician credentialing representation ("shall maintain hospital privileges, credentialing, and any facility-specific certifications..."), not a clawback | match | |
| "restraining" false-positive check | injunctive-relief language, not training-related | every "restraining" hit (contracts 1, 2, 4, 5, 6, 8) is inside the standard Injunctive Relief clause ("...injunctive relief restraining Employee from committing...") | n/a — confirms non-issue | flagged explicitly per instruction, not counted as a mismatch |
| Reformation clause | contract 5 has an express reformation clause (CT); contract 6 does not | confirmed: contract 5's "Severability; Reformation" section instructs a reviewing court to modify/reform restrictions; contract 6's severability section is the bare 4c text only, with no reformation language and no NY-style partial-enforcement sentence | match | |
| NY partial-enforcement sentence | contracts 1, 2, 3 (NY) carry a "Partial Enforcement" sentence — deliberate NY drafting, **not** reformation | present in all three, worded as enforcement "to the extent the court deems reasonable"; none of the three contains reformation language ("modify," "reform") | match | explicitly distinguished from reformation per instruction; confirmed absent from all non-NY contracts |

**Table 3 mismatches: 0.**

## Summary

**Total mismatches found across Tables 1–3: 0.**

No discrepancy was found between the specification/manifest-derived
expected values and the rendered documents, across all 9 contracts, all 3
intake emails, and the full provision matrix (cross-state types,
single-state types, the three customer non-solicit stylings, the two
deliberate gap types, and the reformation/partial-enforcement distinction).

Two apparent mismatches surfaced during automated first-pass checking and
were traced to bugs in the verification script itself, not defects in the
corpus, and are recorded above as such:
1. Contract 4 was transiently flagged for "missing" the NY partial-enforcement
   sentence — the check script had grouped it with the NY bare-severability
   contracts (1, 2, 3) by mistake; contract 4 is CT, and the spec is explicit
   that the partial-enforcement sentence is NY-only. On correction, contract
   4's severability section is exactly the expected bare 4c text.
2. Contract 9 was transiently flagged for a "missing" survival clause — the
   check's text marker required a trailing period after "Survival" that the
   PDF-extracted, all-caps heading ("SURVIVAL") doesn't carry. The clause
   text is present in full.

Everything specified could be verified against the rendered files; nothing
was left unverifiable.

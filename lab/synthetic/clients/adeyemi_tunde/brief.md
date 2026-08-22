# T3 — `adeyemi_tunde` — BRIEF

*Ships as a **test input only** (`to-do/adeyemi_tunde/`). **The hardest client
in the set** — the end of the T1 → T3 difficulty ramp.*

## Who

**Mr. Tunde Olusegun Adeyemi**, a Nigerian process engineer, 40. Born
9 November 1985 in Nigeria; first entered the United States 11 January 2016 at
30 (so Part 9 Item 22.a, Selective Service, is **No**). He is his own
correspondent — the folder is named for the applicant.

Married **Folake Adeyemi** on 16 December 2017. **She is a Nigerian national
and a lawful permanent resident, NOT a U.S. citizen** — which is why the basis
is 316(a) and why there is **no spouse's passport in this packet**. Daughter
**Ayodele Adeyemi**, born 19 July 2022 in Fitchburg, Wisconsin, a U.S. citizen.
Process engineer at Cardinal Polymer Systems, Fitchburg, since 30 September
2019; Folake is a pharmacy technician at Silverwood Pharmacy.

Three addresses inside the five-year window, all in Wisconsin: 5127 Copperleaf
Lane, Fitchburg, WI 53711 (from 1 February 2023); 908 Foundry Street, Apt 12,
Middleton, WI 53562 (15 June 2021 – 31 January 2023); 412 Wren Street, Verona,
WI 53593 (20 September 2019 – 14 June 2021).

A-216540923 · SSN 396-70-2841 · (608) 555-0171 · tunde.adeyemi@quillmail.com
Second address: t.adeyemi@cardinalpolymer.com

## The matter

Engaged 11 May 2026, filed **7 July 2026** — Wisconsin → **Chicago lockbox, VIA
U.S. POSTAL SERVICE (USPS)**, exactly W3's pair. Latest return **TY2025**,
`f1040.pdf`, **Married Filing Jointly** with Folake.

## Basis, and why

**INA 316(a)** — five years. Permanent resident **4 March 2021**, class E21,
never a conditional resident. Earliest filing = 4 March 2026 − 90 days =
**4 December 2025**; filed 215 days later.

**He is married and he has a child, and neither produces a document.** His wife
is not a U.S. citizen, so 319(a) is unavailable and §9.3 r2 bars the whole
spousal cluster; C3c needs a 319(a) basis. This is the deliberate negative
control that stops "spouse → spouse's passport" being learned as a rule
(registry decision D11).

## Exhibits — **{C4, C5}**, eight documents

1 TOC · 2 Cover letter · 3 N-400 · 4 Passport · 5 Permanent Resident Card ·
6 2025 Income Tax Return (joint) · **7 Travel addendum** · **8 Court records**

- **C4** — seven countable trips exceed the Part 8 table's six rows.
  Demonstrated by W1.
- **C5** — Part 9 **Item 15.b** is **Yes**: arrested 24 June 2023 in Fitchburg,
  Wisconsin for **operating a motor vehicle with a suspended license**; the
  charge was **dismissed** on 12 September 2023. **Spelling: the charge as it
  appears on the court record and in the Part 9 Item 15 table is the American
  `license`.** Tunde's own prose may spell it `licence` — a Nigerian-education
  tell, and it is on his voice card — but the two locked artefacts use one
  spelling, or the "court records agree with Item 15 line for line" lock is
  being checked against two strings. The event fits the form's own Item 15
  table and the court records back it. Demonstrated by W3.
- **NO C6.** Item 20 and Item 21 are both **No** — nothing non-tabulable.
  **This is the mirror of T2:** C5 does not drag C6 along either. W3 has both,
  T2 has C6 alone, T3 has C5 alone; all four cells of the 2×2 are populated.

## Input modality — the stress test

**Phone photographs only. There is no questionnaire of any kind in this
folder.** Every document arrives as a photograph taken on a desk or a car seat.
The 2025 return arrives as a **password-protected PDF, and the password is not
in that e-mail** — it turns up two messages later, after the firm asks. Facts
that a questionnaire would have collected are scattered through prose.

## Mess events — four, all demonstrated in worked pairs, all escalated

| mess | deterministic resolution |
|---|---|
| **Blanks supplied by prose** (W3, escalated: there is no form at all here). | Every consumed fact is stated exactly once, unambiguously, somewhere in the thread. Height, weight, eye and hair colour, ethnicity and race arrive in one dense reply to the firm's numbered questions. |
| **Password chase** (W3, escalated). W3's password is in the same message; **his is two e-mails later.** | The password opens the file. There is exactly one password and exactly one protected attachment. |
| **Phone-photo documents** (W1). | Every fact on every photograph is legible. Difficulty is in the count and the format, never in the pixels. |
| **Multiple e-mail addresses** (W2, escalated: **the applicant himself**, not a correspondent). He replies from work when he is on shift. | One person, one thread. Part 11 takes his **personal** address, `tunde.adeyemi@quillmail.com`, because that is the address he gives when asked for his contact details. |

**Address history is spread across the thread**, not given in one block — three
addresses arrive in three different messages and must be assembled gap-free.

## Facts the masterkey must nail

- Item 15.b **Yes** and Item 20 **No**. The court records exhibit exists; the
  written explanation does **not**.
- The Item 15 table row must agree with the court records line for line: date
  of offence 2023-06-24, place Fitchburg, Wisconsin, disposition `dismissed`,
  disposition date 2023-09-12, no conviction date, no sentence.
- Seven countable trips, no day trips. Part 8 carries six; the addendum carries
  all seven, "last **5** years", "Page **6**".
- Three addresses, gap-free, 2019-09-20 to the filing date, all in Wisconsin, so
  the lockbox is Chicago throughout.
- Folake is in N-400 Part 5 as a **non-citizen** spouse; Ayodele is in Part 6.
  Neither produces an exhibit.
- The joint 2025 return prints both names and both SSNs and the Fitchburg
  address; that address must appear in the N-400 history.
- Part 11 filled; Part 13 empty; form unsigned.

---

## INVENTION RULES — BINDING ON THE MASTERKEY

*You will invent facts this brief does not fix: passport numbers and MRZs,
green-card expiry dates, an insurer and a policy number, a court, a judge, a
clerk, docket and police case numbers, deed parties and instrument numbers,
a tax preparer, AGI figures, travel destination countries, a spouse's employer.
These rules govern all of it.*

1. **Leakage.** Whole-token grep every new proper noun and every digit-string of
   six characters or more against `lab/synthetic/blocklist.txt` before you use
   it — `grep -ixF "<token>" lab/synthetic/blocklist.txt` must return nothing.
   Zero hits. This applies to court names, judges, clerks, insurers, deed
   parties, tax preparers, employers and travel countries as much as to people.
   A single hit halts the whole run (RUN-PHASE-2-6.md).
2. **Telephones.** A real area code plus the reserved fiction block
   `555-0100`–`555-0199`. Nothing else.
3. **E-mail.** Only `quillmail.com`, `brightpost.net`, or an employer domain
   already named in this brief. **Never a real consumer mail domain** — the
   three commonest are all on the blocklist.
4. **ASCII only**, in every name, everywhere. The names travel through a
   passport MRZ and a `soffice --headless` conversion.
5. **No firm identity of any kind.** No firm name, no preparer name, no
   preparer address, no firm telephone, no firm e-mail — not on the cover
   letter, not in the signature block, not on the N-400, nowhere (STYLE-SPEC
   §16 ruling 7). If a schema slot appears to want one, **the slot is dead:
   leave it out.** The only survivor is the unattributed role line
   `Petition Preparer`. N-400 Part 11 is filled with the applicant's own
   telephone and e-mail; **Part 13 stays empty and the form ships unsigned**
   (§16 rulings 10 and 11).
6. **Corpus quarantine.** Do not read `lab/jacobs_brent`, `lab/zhu_vivian`,
   `lab/izaguirre_jesus`, `lab/malone_kyle` or `lab/ossola_ylenia` — not one
   file, not one directory listing. `lab/reports/*.md` is permitted.
7. **Nationality.** The applicant's nationality is fixed by this brief.
   Australia, China, Mexico, the Philippines and Italy are barred as *applicant*
   nationalities (BUILD-PLAN §7); they may appear as travel destinations.
8. **Document strings.** The document lists in this brief are **shorthand**.
   The authoritative component file name, divider title and TOC line for every
   document is `lab/synthetic/templates/document-catalog.yaml` (SPEC-DELTA
   D-C). Do not re-derive any of the three from prose; STYLE-SPEC §4.4's lock —
   TOC line count == divider count == DOCUMENT count, and TOC line *n* names
   document *n* — is what breaks if you do.
9. **Fee, edition, fixed values.** Fee `760.00`; N-400 edition `01/20/25`; the
   Part 8 travel table has exactly **six rows** and sits on **page 6** of 14.

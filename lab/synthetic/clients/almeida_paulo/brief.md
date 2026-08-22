# W1 — `almeida_paulo` — BRIEF

*Ships as a **worked pair** (`examples/almeida_paulo/{input,output}`). Read this
with the BUILD-PLAN §3 masterkey schema and STYLE-SPEC §12; you need nothing
else, and you may not read `lab/<client>/`.*

## Who

**Mr. Paulo Miguel Almeida**, a Brazilian structural engineer, 38, single, no
children. Born 22 March 1988 in Brazil; first entered the United States on
2 September 2015 at 27 (so Part 9 Item 22.a — Selective Service — is **No**).
Lives at 47 Larkspur Street, Apt 3, Somerville, Massachusetts 02143, since
1 November 2019; before that 118 Hollis Avenue, Medford, MA 02155. He is his
own correspondent: the folder is named for the applicant.

A-208451772 · SSN 037-84-2196 · (617) 555-0142 · paulo.almeida@quillmail.com

## The matter

The simplest packet in the set, and the one every other client is measured
against. Engaged 14 October 2025, filed 8 December 2025 — **Massachusetts →
Elgin lockbox, VIA U.S. POSTAL SERVICE (USPS)**, the P.O. Box variant of
STYLE-SPEC §7. Filed before mid-April 2026, so the latest return is **TY2024**
on the `f1040--2024.pdf` blank, filing status Single.

## Basis, and why

**INA 316(a)** — the general five-year provision. He is not married, so no
spousal route exists. Permanent resident since **19 June 2020** (class E21),
never a conditional resident. Earliest filing date = 19 June 2025 − 90 days =
**21 March 2025**; he filed 262 days later. The cover letter's eligibility
clause is the 316(a) one and must read "…since **he** became a permanent
resident on **June 19, 2020**", with the citation `INA § 316(a); 8 C.F.R.
§ 316.2`.

## Exhibits — **{C4}**, seven documents

1 Table of contents · 2 Cover letter · 3 Form N-400 · 4 Passport bio page ·
5 Permanent Resident Card · 6 2024 Income Tax Return · **7 Travel addendum**

**C4 trigger:** seven countable trips in the five-year window exceed the Part 8
table's **six rows** (verified against the committed 01/20/25 blank). Nothing
else fires: 316(a) bars C1/C2/C3 outright (STYLE-SPEC §9.3 r2), and every Part
9 moral-character answer is **No**, so no C5 and no C6.

## Input modality

A questionnaire **docx** returned filled, phone photographs of the green card
(front and back) and the passport bio page, a PDF of the 2024 return, and a
resume docx whose employers and dates must equal Part 7 exactly.

## Mess events — W1 **demonstrates** four of the nine (BUILD-PLAN §5.3)

| mess | deterministic resolution |
|---|---|
| **Day trip in the travel list.** He lists eight trips; one is a same-day drive into Canada. | The day trip appears on the input side and on **neither** the Part 8 table **nor** the travel addendum. C4 fires on the row count, not on the trim. (registry decision D7.) |
| **Phone-photo documents.** Card and passport arrive as desk photographs, slightly rotated, with shadow. | Every fact on them is legible and agrees with the questionnaire; the photograph is a texture, never an ambiguity. |
| **Over-delivery.** He also sends an expired 2014 Brazilian passport, a lease, and a vaccination record. | None is triggered by any §9.2 rule, so none enters the packet. The extras still agree with the masterkey. |
| **Unrelated-matter noise.** One e-mail asks, in passing, about a cousin's B-2 visitor visa. | Not this matter. It affects no packet fact and produces no document. |

## Facts the masterkey must nail

- LPR date **2020-06-19** appears three times and must be identical: green card
  `Resident Since`, N-400 Part 2, and the cover letter's eligibility clause.
- Seven countable trips **plus** one day trip = eight supplied. Part 8 carries
  six, most recent first; the addendum carries all **seven** countable trips,
  most recent first, and says "last **5** years" and "Page **6**".
- Employment gap-free from 2016-03-01 (Dunmore Precision Castings, Medford) to
  Harborline Structural Engineering LLC, Somerville, 2019-04-08 to present.
- Address history gap-free across the five-year window; the tax return's
  printed address is the Somerville one and must appear in the N-400 history.
- Part 11 (his own telephone and e-mail) is **filled**; Part 13 is **empty**;
  the form ships **unsigned**.

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

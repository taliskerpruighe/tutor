# T1 — `tran_daniel` — BRIEF

*Ships as a **test input only** (`to-do/tran_daniel/`, input files, no output).
The answer key is rendered but unshipped. **BUILD-PLAN §8 gave T1's folder a
different given name; it is `tran_daniel` here, because that given name is a
blocklisted corpus token and a folder name ships. See registry decision D2.***

## Who — READ THIS FIRST

**The folder is named for the correspondent.** `Daniel Quang Tran`, a U.S.
citizen by naturalization (21 May 2009, Cleveland, Ohio), writes almost every
message. **The applicant is his wife, Ms. Vu Thanh Ha**, a Vietnamese national.
Vietnamese name order: family name **Vu**, given name **Ha**, middle name
**Thanh**. Her passport prints `VU THANH HA`.

Born 18 June 1991 in Vietnam; first entered the U.S. 27 May 2020; married
Daniel **14 March 2020**. Medical laboratory technician at Scioto Clinical
Laboratories, Westerville, Ohio, since 9 January 2023; at home with the child
before that. They live at 3155 Sandpiper Drive, Westerville, OH 43081 since
20 April 2023 — the house they bought on 14 April 2023 — and before that at
690 Bellhaven Court, Gahanna, OH 43230.

Daughter **Mai Linh Tran**, born 2 August 2021 in Westerville, Ohio, a U.S.
citizen with a U.S. passport.

A-214902186 · SSN 289-63-4157 · (614) 555-0129 · ha.vu@quillmail.com
Daniel: (614) 555-0176 · dtran@trestlefp.com

## THE SINGLE MOST LIKELY ERROR IN THIS CLIENT

She **requests a name change** on the N-400 to `Ha Thanh Tran`. That string
belongs in **exactly one place**: the Part 2 name-change item. The applicant
cover page, the cover letter Re: block, the passport and its MRZ, the green
card, the tax return and every divider carry her **current legal name, Vu Thanh
Ha**. A requested name is a request, not a fact about a document that exists at
filing (registry decision D13).

## The matter

Engaged 27 April 2026, filed **15 June 2026** — Ohio → **Chicago lockbox, VIA
FEDERAL EXPRESS**, the courier street address. Latest return **TY2025**,
`f1040.pdf`, **Married Filing Jointly**.

## Basis, and why

**INA 319(a)**. Permanent resident **30 November 2022**, class **IR6**.
Earliest filing = 30 November 2025 − 90 days = **1 September 2025**; filed 287
days later. She married in March 2020 and became a resident in November 2022 —
**two years and eight months later, so she was NOT a conditional resident.**
`was_cr` is **false**, there is no I-751, and **C2 must not appear**. Getting
this wrong would give her W2's story and break the no-duplicate rule.

## Exhibits — **{C1, C3a, C3c, C4}**, ten documents — the largest packet

1 TOC · 2 Cover letter · 3 N-400 · 4 Passport · 5 Permanent Resident Card ·
6 2025 Income Tax Return (joint) · **7 Spouse's passport** · **8 Joint deed** ·
**9 Child's passport** · **10 Travel addendum**

- **C1** — basis is 319(a). Demonstrated by W2.
- **C3a** — 319(a) **and** the joint deed to the Westerville house was
  supplied. **C3c** — 319(a) **and** a child of the marriage exists **and** her
  passport was supplied. Both are the *same rule* W2 demonstrates with a single
  document (the automobile policy); this client is the generalisation test
  (BUILD-PLAN §7).
- **Not C3b** — no automobile policy was supplied. They were asked; they did
  not send one. Supplied evidence, not basis, is the argument.
- **C4** — seven countable trips exceed the Part 8 table's six rows.
- Not C5, not C6: every Part 9 answer is No.
- The joint 2025 return is DOCUMENT 6 and is not duplicated.

## Input modality

**Delegated correspondence.** Daniel writes; Ha appears two or three times, very
briefly, usually to confirm a date he got slightly wrong. Documents arrive as
his scans and photographs, named the way he names things.

## Mess events

| mess | deterministic resolution |
|---|---|
| **Folder named for the correspondent** (reuses W2). | The applicant is the person on the passport and the green card. |
| **E-signature friction** (T1 only, and inert). An e-signature attempt fails; he prints, signs, scans and returns the page instead. | No packet fact depends on which route the page took. The N-400 ships **unsigned** in any case (§16 r11). Texture, not a mess with consequences. |

## Facts the masterkey must nail

- `Vu Thanh Ha` everywhere; `Ha Thanh Tran` in the Part 2 name-change item only.
- Marriage 2020-03-14, LPR 2022-11-30, class IR6, `was_cr: false`.
- Deed facts must reconcile with the address history: grantees are both
  spouses, property is 3155 Sandpiper Drive, recording date on or about
  2023-04-14, and her Westerville from-date is 2023-04-20.
- Child's passport is a **U.S.** passport (she was born in Ohio); her name and
  DOB must match the N-400 Part 6 child entry.
- Spouse's passport is Daniel's U.S. passport; his naturalization date and place
  appear in N-400 Part 5.
- Seven trips: Part 8 carries six, the addendum carries all seven, most recent
  first, "last **3** years" (319(a) window) and "Page **6**".
- Part 11 filled with **her** telephone and e-mail, not Daniel's. Part 13 empty.

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

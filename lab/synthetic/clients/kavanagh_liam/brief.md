# W2 — `kavanagh_liam` — BRIEF

*Ships as a **worked pair** (`examples/kavanagh_liam/{input,output}`).*

## Who — READ THIS FIRST

**The folder is named for the correspondent, not the applicant.** `Liam
Patrick Kavanagh` is a U.S. citizen by birth and he writes every message in the
thread. **The applicant is his wife, Ms. Siobhan Maire Brennan**, an Irish
national who kept her own surname on marriage. Nothing in the packet says
"Kavanagh" except the spouse fields and the spouse's passport exhibit.

Siobhan: born 27 November 1990 in Ireland, first entered the U.S. 19 August
2021, married Liam on 19 February 2022 in Illinois. Veterinary technician at
Riverbend Veterinary Clinic, Berwyn, Illinois, since 14 November 2022. No
children. A-213668041 · SSN 341-27-8065 · (773) 555-0118 ·
s.brennan@quillmail.com. Liam: born 8 May 1987, dispatcher at Halsted Freight
Systems, Chicago; (312) 555-0187; he writes from **two** addresses,
liam.kavanagh@brightpost.net and l.kavanagh@halstedfreight.com.

## The matter

Engaged 2 December 2025, filed **10 February 2026** — Illinois → **Chicago
lockbox, VIA FEDERAL EXPRESS**, so the courier street address of STYLE-SPEC §7,
not the P.O. Box. Latest return is **TY2024**, `f1040--2024.pdf`, **Married
Filing Jointly** with Liam.

## Basis, and why

**INA 319(a)** — spouse of a U.S. citizen, three years. She became a permanent
resident on **15 September 2022**, seven months after the marriage, so she was
admitted as a **conditional** resident, class **CR6**. Earliest filing =
15 September 2025 − 90 days = **17 June 2025**; she filed 238 days later. The
eligibility clause is the 319(a) one, naming **Mr. Liam Patrick Kavanagh**,
with `8 U.S.C. § 1430(a); 8 C.F.R. § 319.1`.

**The I-751 is the point of this client.** Petition to remove conditions filed
2 July 2024, receipt **MSC0918452207**, notice dated 11 July 2024, still
**pending** on the filing date, approved only on 30 April 2026 — after filing.
So at filing she holds an expired two-year card plus a receipt notice.

## Exhibits — **{C1, C2, C3b}**, nine documents

1 TOC · 2 Cover letter · 3 N-400 · 4 Passport · 5 Permanent Resident Card ·
6 2024 Income Tax Return (joint) · **7 Spouse's passport** ·
**8 Form I-797C, Notice of Action** · **9 Joint automobile insurance policy**

- **C1** — basis is 319(a); unconditional on the basis.
- **C2** — she *was* a conditional resident **and** no unconditional I-551 was
  in hand at the filing date. Both halves of the condition are needed and both
  are true; this is the only C2 in the six.
- **C3b** — 319(a) **and** a joint automobile insurance policy was supplied.
  This one document is where the whole supplied-evidence rule is taught, and
  T1 must generalise it to a deed and a child's passport.
- **Not C3a** (they rent), **not C3c** (no children), **not C4** (four
  countable trips, under the six Part 8 rows, nothing trimmed), **not C5/C6**
  (every Part 9 answer is No).
- **The joint 2024 return is marriage evidence and it stays DOCUMENT 6.** It is
  never listed twice (STYLE-SPEC §9.3 r1, §16 r13).

## Input modality

**E-mail prose only. There is no questionnaire in this folder at all.** Every
fact reaches the firm inside a sentence Liam wrote. Attachments are scans and
one phone photograph of the I-797C.

## Mess events — W2 **demonstrates** three of the nine

| mess | deterministic resolution |
|---|---|
| **Folder named for the correspondent.** | The applicant is the person whose name is on the passport and the green card. The correspondent is the person whose name is on the e-mail. They are different people, and the packet follows the applicant. |
| **Superseded address.** An early message gives 5417 Quarry Lane, Cicero as their address; a later message corrects it — they moved to 2214 Wexford Road, Berwyn on 1 May 2024 and he forgot. | **Chronological: the later e-mail wins.** Berwyn is the current address; Cicero becomes the prior address, 2022-01-10 to 2024-04-30. Both are in Illinois, so the lockbox is Chicago either way. |
| **Two e-mail addresses.** He starts on his personal address and replies from work when he is on shift. | One person, one thread. Both addresses belong to Liam and neither belongs to the applicant. |

## Facts the masterkey must nail

- Applicant surname **Brennan** everywhere: cover page, cover letter Re: block,
  N-400 Part 2, passport MRZ, green card. **Kavanagh** appears only as the
  spouse.
- The I-797C receipt number, the received date and the notice date must
  reconcile with the I-751 block, and the A-number on the notice must equal the
  A-number in every N-400 page header and on the green card.
- Green card is **CR6**, `Resident Since` **09/15/2022**, expiring 15 September
  2024 — expired at filing, which is exactly why C2 exists.
- Four trips only; **no travel addendum**, and Part 8 has spare rows.
- Marriage date 2022-02-19; she has been married once, he has been married once.

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

# W3 — `nowak_agata` — BRIEF

*Ships as a **worked pair** (`examples/nowak_agata/{input,output}`). This is the
client that teaches the moral-character half of the exhibit rule. Two test
clients depend on it.*

## Who

**Ms. Agata Zofia Nowak**, a Polish graphic designer, 39, divorced, one child.
Born 30 September 1986 in Poland; first entered the United States 24 August
2011 on a student visa. Senior graphic designer at Kestrel Field Design, Ann
Arbor, Michigan, since 17 August 2020; before that Ferndale Type Works,
Ypsilanti. Lives at 806 Brightwood Terrace, Ann Arbor, MI 48104 since 1 June
2019; before that 1120 Tanager Way, Ypsilanti, MI 48197. She is her own
correspondent.

Son **Jakub Nowak**, born 5 March 2014 in Poland, lives with her. Divorced from
Marek Wisniewski, a Polish national — married 16 June 2012, divorced 12 April
2018.

A-212337509 · SSN 372-51-9430 · (734) 555-0163 · a.nowak@quillmail.com

## The matter

Engaged 30 March 2026, filed **26 May 2026** — Michigan → **Chicago lockbox,
VIA U.S. POSTAL SERVICE (USPS)**. Filed after mid-April 2026, so the latest
return is **TY2025** on the `f1040.pdf` blank, filing status Head of Household.
**She is the only worked pair on the TY2025 blank**, and she exists in that
position on purpose: without her, two test clients would be asked to produce a
tax year no worked example had ever shown (registry decision D6).

## Basis, and why

**INA 316(a)** — five years. Permanent resident **11 February 2021**, class
E31, never a conditional resident. Earliest filing = 11 February 2026 − 90 days
= **13 November 2025**; she filed 194 days later.

**The bridge across the 2011–2021 decade, stated so nobody invents six versions
of it.** She entered on an F-1 in August 2011, violated her status in 2014 when
she stopped attending, and was placed in removal proceedings in March 2015. Her
employer at the time filed an employment-based petition for her, and the
proceedings were **terminated** in September 2017 so that she could pursue
adjustment of status before USCIS on the approved petition. Her I-485 was
pending from October 2017 with an employment authorisation document — which is
what makes her continuous employment from May 2016 lawful and coherent — and was
approved on 11 February 2021, giving her the E31 card. Her son was born in
Poland in 2014 during a visit and entered the United States with her.

She is divorced and she has a child, and **neither fact produces a single
document** — a deliberate negative control (registry decision D11). A solver
who has learnt "child → child's passport" from T1 must fail here, and must
notice that the rule's antecedent was the *basis*, not the child.

## Exhibits — **{C5, C6}**, eight documents

1 TOC · 2 Cover letter · 3 N-400 · 4 Passport · 5 Permanent Resident Card ·
6 2025 Income Tax Return · **7 Court records** · **8 Written explanation**

**Two separate events, seven years apart, on two different Part 9 items. This
separation is the entire teaching point.**

- **C5 ← Part 9 Item 15.b = Yes.** Arrested 8 November 2019 in Ann Arbor,
  Michigan; **disorderly conduct**; charge **dismissed** 14 February 2020; no
  conviction, no sentence. The event fits the form's own Item 15 table, and the
  court records exhibit backs it.
- **C6 ← Part 9 Item 20 = Yes.** Placed in removal proceedings 11 March 2015
  after a violation of her F-1 status; proceedings **terminated** 22 September
  2017; she later adjusted status and became a permanent resident in 2021.
  Item 21 (removed or deported) is **No**. Item 20 has no table anywhere on the
  form — it routes to Part 14, Additional Information — so the firm authors a
  written explanation.
- Not C1/C2/C3 (316(a) bars spousal evidence outright); not C4 (three countable
  trips, no trims).

**Why both, in one client:** T2 Stavros ships with C6 and *no* C5. Unless a
worked pair shows C6 arriving from its own trigger, independent of any arrest,
T2's packet is unlearnable and the challenge is broken (registry decision D1).

## Input modality

An **xlsx questionnaire** returned with several hard fields left blank, plus
flatbed scans — one of them password-protected.

## Mess events — W3 **demonstrates** two of the nine

| mess | deterministic resolution |
|---|---|
| **Blank questionnaire fields.** Height, weight, eye colour, hair colour and the A-number come back empty; she did not know them or could not find the card. | She supplies each one later, **in e-mail prose**, in a message that answers the firm's follow-up. The prose value is the value. Nothing is guessed and nothing is left blank on the form. |
| **Password-protected attachment — benign.** The scan of her court disposition is a password-protected PDF. | **The password is in the same e-mail, two lines below the attachment.** No chase. T3 escalates this to a real two-message chase; W3 exists so that the shape is familiar before it becomes difficult. |

## Facts the masterkey must nail

- The arrest and the removal proceedings are **unrelated**. Nothing in either
  narrative may reference the other. Different years, different cities,
  different causes.
- The written explanation covers the **proceedings only**; the court records
  cover the **arrest only**.
- Court records must carry: court name and location, police case number, docket
  number, the charge with its statute number, the offence date, the plea, the
  disposition (`dismissed`) and its date, the judge, and a clerk certification.
- Part 9 Item 15's table row must agree with the court records line for line —
  offence date, place, disposition — and the "no conviction" case means the
  conviction-date cell stays empty.
- Three trips only; **no travel addendum**; Part 8 has spare rows.
- Address and employment history gap-free across the full five-year window.

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

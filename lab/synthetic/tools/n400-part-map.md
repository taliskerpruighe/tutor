# `n400-part-map.md` — the empirical Part map of the committed 01/20/25 blank

Built in Phase 2 by dumping all 488 AcroForm fields of `../blanks/n-400.pdf`
with their page numbers and `/TU` tooltips. Full dump: `n400-field-dump.tsv`.
**`fieldmap_n400.yaml`, `render_n400.py` and `verify_client.py` all read THIS
file for the Part 10/11/12 question. Nobody re-derives it from prose.**

## CORRECTED 2026-08-22 — read this before anything else

**An earlier draft of this file identified Parts from the AcroForm `/TU`
tooltips. That was wrong and the correction was raised by a Phase 2b masterkey
writer working from the primary source.** The tooltips on this blank are stale
and internally inconsistent: they carry a previous edition's numbering, they
disagree with each other, and several are simply mislabelled (a page-11 contact
field is tooltipped "Part 7. Marital History"). **The tooltips are not evidence
of anything. Identify a Part by the printed page text, read with
`pdftotext -layout`, and by which PDF page the field sits on.**

**The consequence is good news: STYLE-SPEC §16's numbering is exactly right for
this edition, and needs no reinterpretation.** The applicant's contact block IS
printed Part 11 and the preparer block IS printed Part 13, precisely as the user
worded rulings 10 and 11.

### The printed Parts of the committed 01/20/25 blank, by page

Verified with `pdftotext -f n -l n -layout ../blanks/n-400.pdf -`:

| PDF page | printed Part | title |
|---|---|---|
| 6–10 | 9 | Additional Information About You (the moral-character block) |
| 11 | **10** | **Request for a Fee Reduction** |
| 11 | **11** | **Applicant's Contact Information, Certification, and Signature** |
| 12 | **12** | **Interpreter's Contact Information, Certification, and Signature** |
| 12 | **13** | **Contact Information, Certification, and Signature of the Person Preparing this Application** |
| 13 | 14 | Additional Information |
| 14 | 15 | Signature at Interview |
| 14 | 16 | Oath of Allegiance |

### The field-name prefixes lag, and they lag inconsistently

`P10_*` on page 11 really is printed Part 10 (household income, household size —
the fee-reduction items). But `P12_*` and `P13_*` on the *same page* are printed
Part 11, and `P15_*` on page 12 is printed Part 13. **There is no constant
offset. Never infer a Part from a field-name prefix.** The field lists below were
derived from page position plus printed text and are authoritative; only the
earlier draft's *labels* were wrong, never its field names.

## What §16 rulings 10 and 11 require, in field names

| §16 says | printed Part | action |
|---|---|---|
| "Part 11 — the applicant's own phone and email — IS filled" (r10) | 11, items 3, 4, 5 | **FILL** |
| "Part 13 preparer block stays entirely blank" (r10) | 13 | **LEAVE EMPTY** |
| "The N-400 ships UNSIGNED, no signature date" (r11) | 11 signature + date | **LEAVE EMPTY** |

Also empty: printed Part 12 (interpreter — none is engaged on any of the six
matters) and printed Parts 15 and 16 (executed at the USCIS interview, never by
the firm). Printed Part 10 (fee reduction) is **No** for all six clients
(STYLE-SPEC §12.8), so its household-income and household-size fields stay empty.

### FILL — exactly three fields (§16 r10, first half)
```
form1[0].#subform[10].P12_Line3_Telephone[0]   printed Part 11 item 3  daytime telephone
form1[0].#subform[10].P12_Line3_Mobile[0]      printed Part 11 item 4  mobile telephone
form1[0].#subform[10].P12_Line5_Email[0]       printed Part 11 item 5  email address
```

### LEAVE EMPTY — assert, do not merely omit
```
# printed Part 11 applicant signature + date  -- §16 r11, form ships unsigned
form1[0].#subform[10].P12_SignatureApplicant[0]
form1[0].#subform[10].P13_DateofSignature[0]

# printed Part 13 PREPARER BLOCK -- §16 r10 + r7 (no firm identity anywhere)
form1[0].#subform[11].P15_Line1_PreparerFamilyName[0]
form1[0].#subform[11].P15_Line1_PreparerGivenName[0]
form1[0].#subform[11].P15_Line2_NameofBusinessorOrgName[0]
form1[0].#subform[11].P15_Line4_Telephone[0]
form1[0].#subform[11].P15_Line5_Mobile[0]
form1[0].#subform[11].P15_Line6_Email[0]
form1[0].#subform[11].P15_DateofSignature[0]
form1[0].#subform[11].P12_SignatureApplicant[2]    # preparer's signature

# printed Part 12 INTERPRETER BLOCK -- no interpreter on any of the six matters
form1[0].#subform[11].P14_Line1_nterpreterFamilyName[0]   # sic, the blank misspells it
form1[0].#subform[11].P14_Line1_nterpreterGivenName[0]
form1[0].#subform[11].P14_Line2_NameofBusinessorOrgName[0]
form1[0].#subform[11].P14_Line4_Telephone[0]
form1[0].#subform[11].P14_Line5_Mobile[0]
form1[0].#subform[11].P14_Line5_EmailAddress[0]
form1[0].#subform[11].P14_NameOfLanguage[0]
form1[0].#subform[11].P14_DateofSignature[0]
form1[0].#subform[11].P12_SignatureApplicant[1]    # interpreter's signature

# Parts 15 and 16 -- executed at the USCIS interview, never by the firm
form1[0].#subform[13].Part15ApplicantsSignature[0]
form1[0].#subform[13].Part15DateofSignature[0]
form1[0].#subform[13].Part15USCISSignature[0]
form1[0].#subform[13].Part15USCISName[0]
form1[0].#subform[13].ApplicantsSignature[0]
form1[0].#subform[13].Part15DateofSignature[1]
```

## The positive control `verify_client.py` MUST run

Asserting "these fields are empty" against names that do not exist on the blank
passes vacuously while a filled preparer block ships. So, in order:

1. Load the 488-name set from `../blanks/n-400.pdf`.
2. **Assert every name in both lists above EXISTS in that set.** A missing name
   is a build bug (edition drift), not a pass. **Do NOT identify these fields by
   `/TU` tooltip — the tooltips on this blank are stale and mislabelled.**
3. Assert the three FILL fields are non-empty in the rendered component and
   equal the masterkey's `contact.*` values.
4. Assert every LEAVE-EMPTY field is empty or absent-of-value in the rendered
   component.

## Other notes for the toolsmith
- `#pageSet[0].Page1[n].PDF417BarCode1[0]` (14 of them, one per page) are the
  2D barcode fields. Leave them empty.
- `#area[n].Line1_AlienNumber[n]` is the per-page A-number header, one per page.
  Tooltips say "No Entry" on some pages; fill every one that accepts a value —
  STYLE-SPEC §8 records that the firm puts the A-number on every page header,
  and §9.4 locks it to the green card.
- Comb fields (the A-number) extract space-separated under `pdftotext`; the
  verifier must strip whitespace before comparing.
- 95 fields carry no `Part n.` tooltip (`#subform`, `#area`, `#pageSet`
  containers and a few strays). They are structural, not data.

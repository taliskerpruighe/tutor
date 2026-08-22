# zhu_vivian — packet anatomy (runner report)

Applicant: Ms. Xuying Zhu. Basis INA 316(a) (five-year, NOT the spousal 319
used in jacobs_brent).

## Structure — TABBED, and MERGED
Cover page:
```
                    APPLICATION FOR NATURALIZATION

APPLICANT:

Ms. Xuying Zhu
DOB: 09/04/1992
COB/CON: China

Classification Basis: INA 316(a)
```

TAB A / SUMMARIES
  DOCUMENT 1 Table of Contents
  DOCUMENT 2 Cover Letter
TAB B / BIOGRAPHICAL
  DOCUMENT 3 Form G-1450, Authorization for Credit Card Transaction
  DOCUMENT 4 Form N-400
  DOCUMENT 5 Bio page of latest passport
  DOCUMENT 6 Form I-551, Permanent Resident Card
  DOCUMENT 7 Latest tax return
  DOCUMENT 8 Travel Addendum
  DOCUMENT 9 Court Records

Tab header format:
```
  TAB A

SUMMARIES
```

## Table of contents (verbatim)
```
                               TABLE OF CONTENTS

Tab A (Summary)

1. Table of contents

2. Cover letter

Tab B (Biographical Information)

3. Form G-1450, Authorization for Credit Card Transaction

4. Form N-400, Application for Naturalization

5. Bio page of latest passport of the applicant

6. Form I-551, Permanent Resident Card

7. Latest tax return

8. Travel addendum

9. Court records
```

## Cover letter
```
VIA U.S. POSTAL SERVICE (USPS)
Department of Homeland Security
United States Citizenship and Immigration Services
USCIS Dallas Lockbox
Attn: N-400
P.O. Box 660060
Dallas, TX 75266-0060

       Re:    N-400 Application for Naturalization

              Applicant: Ms. Xuying Zhu
              Date of Birth: September 4, 1992
              Country of Birth/Country of Citizenship: China
```
"To whom it may concern:", two substantive paragraphs plus a boilerplate
paragraph on supporting documents. Signature block:
```
Sincerely,

SYMPLE


By: Marcel Oliveira
Petition Preparer
```

## Merge
Single monolithic PDF. Names seen: `(Second Update) N-400 Packet.pdf`,
`(Updated) N-400 Packet.pdf`, `Compressed N-400 Packet.pdf`. Components also
kept loose, named with letter-number prefixes A-1, A-2, B-4 ... B-9, under
`Tab A (Content + Cover)/` and `Tab B (Biographical Info)/`.

## Typography
Centred uppercase section headers. "DOCUMENT n" centred. N-400 footer
"Form N-400 Edition 04/01/24 | Page X of 14". No Bates numbering.

## DIVERGENCE FROM jacobs_brent — the thing to resolve
| | jacobs_brent (2025) | zhu_vivian |
|---|---|---|
| merged PDF | none, discrete numbered files | yes, monolithic |
| tabs | none; flat DOCUMENT 1-4 | TAB A / TAB B with named sections |
| basis | INA 319 spousal | INA 316(a) five-year |
| lockbox | Chicago | Dallas |
| delivery | FedEx | USPS |
| exhibits | I-551, passport only | + G-1450, tax return, travel addendum, court records |
| cover page | none over TOC | yes, applicant header + classification basis |
| signature | (not extracted) | SYMPLE / By: Marcel Oliveira, Petition Preparer |

The challenge prompt promises a merged PDF and cover pages, which matches
zhu_vivian. jacobs_brent contributes the flat numeric-prefix file naming and
the s.319 spousal cover-letter argument.

# izaguirre_jesus — N-400 field provenance (runner report)

Applicant Jesus Antonio Izaguirre Paz. A-072570588. LPR 2012-05-24.
N-400 edition 09/17/19, filed 2022-02-09. Basis: Part 1 Box A, 5+ years LPR.

## RULE SET CONFIRMED on a third matter
- ID documents supply: name, DOB, sex, COB/COC, A-number, LPR date, height,
  weight.
- Questionnaire supplies: address history with date ranges, employment, trips,
  marital status, children, contact details, moral-character answers.
- Firm derives: filing basis from the LPR date; continuous residence from it.
- Firm supplies: preparer block, firm address, phone, email.

## Cross-document consistency VERIFIED here
- Name identical across N-400, G-1145, G-1450, Index and cover letter. Green
  card shows "Jesus A" — middle name abbreviated to an initial, which is
  normal card formatting, not a conflict.
- A-number identical on N-400 and green card.
- LPR date 2012-05-24 on the card vs approval notice 2012-05-29 (Exhibit G) —
  a five-day lag, which is the expected notice-processing gap.
- Email identical on N-400, G-1145 and intake form.
- Current address on N-400 matches the intake questionnaire.
- Every Part 9 trip appears in the trips spreadsheet.
- Destinations consistent with country of citizenship.

## Gaps and conflicts — TEXTURE FOR SYNTHETIC DATA
- Mobile phone blank on the N-400 while G-1145 carries a different number.
- Employment "Date From" blank — the client never supplied a start date.
- The third address (South Bend) has NO date range at all, because the
  questionnaire answer had none.
- The addendum reaches back to 2012, well beyond the five-year window.

These are not errors to avoid in the synthetic build — they are exactly the
kind of hole a real intake leaves, and a good synthetic input should leave
some too.

## The .xlsx addendum
Columns: `Day Left | Day Returned | 6+ Months? | Countries | Days Abroad`.
Filed version ~23 rows (2017-2022); intake source 56 rows (2012-2022). The
firm trims the source to the filing window plus margin. Main form holds six
trips; everything beyond overflows to the spreadsheet.

## Exhibits — driven by a contested immigration history
A: I-485 (2010-03-07) · B: I-797A (2002-01-17, Notre Dame sponsorship) ·
C: AOS decision (2011-03-23, denied on removal grounds) · D: Notice to Appear
(2009-10-09, alleged H-1B overstay) · E: I-797A (2009-04-08, H-1B extension
proving no unlawful presence) · F: Immigration Judge order (2011-04-01,
proceedings terminated on joint motion) · G: approval notice (2012-05-29).

ALL SEVEN exist to support ONE answer: Part 12 Q35, removal proceedings = Yes.
The Written Explanation narrates it. This is the rule: a single "Yes" on a
moral-character or history question drags a whole exhibit set behind it.

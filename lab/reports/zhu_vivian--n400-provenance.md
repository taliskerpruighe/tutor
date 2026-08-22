# zhu_vivian — N-400 field provenance (runner report)

Final: `Tab B (Biographical Info)/B-4. N-400, Application for Naturalization_Signed.pdf`
14 pages, signed 2024-12-16. Basis: general provision (5-year residence).

## Provenance categories — CORE RULE SET (confirms jacobs_brent pattern)

**Transcribed from ID documents (passport bio page, green card)**
Legal name, DOB, sex, country of birth, country of citizenship, and the
Part 3 physical descriptors (race, height, weight, eye colour, hair colour).

**From the questionnaire / resume**
Name-change request, current address and move-in date, marital status and
prior-spouse details, contact phone and email, all Part 9 answers, and the
entire Part 7 employment history — employer, city, title and date ranges
match the client's resume EXACTLY. The resume is the employment source.

**Derived/computed by the firm**
- Prior address history and its date ranges, interpolated from employment
  start/end dates cross-checked against the address on the tax return.
- The Travel Addendum (B-8), which compiles 10 trips 2019-2024, wider than
  the 6 trips carried into Part 8.
- Continuous-residence calculation from the LPR date.

**From firm records**
Preparer block, firm contact, fee terms.

## Cross-document consistency rules the synthetic data must honour
- Tax return address must match one of the address-history entries.
- Resume employers/dates must match Part 7 exactly.
- Travel addendum must be a superset of Part 8.
- Green card supplies the A-number and LPR date, which in turn drive the
  continuous-residence dates.
- Passport supplies name/DOB/COB, which must agree with the green card.

## Loose ends the runner noted (UNVERIFIED — haiku reading scans)
- Court Records tab (B-9) holds dismissed Connecticut charges from 2019 while
  Part 9 arrest questions read "No". Runner calls this a material omission;
  treat as an unconfirmed inference, not a finding. Structurally the useful
  point is that the Court Records tab exists and is populated from a
  third-party court source the client did not necessarily volunteer.
- Marital status "Divorced" with a 2023 marriage date and no divorce decree
  in the packet.
- Travel addendum reaches back beyond the Part 8 window.

For the synthetic build these are irrelevant as facts but instructive as
SHAPES: a packet can contain an internally inconsistent answer, a tab with no
supporting document, and an addendum broader than the form.

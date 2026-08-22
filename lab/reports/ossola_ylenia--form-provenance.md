# ossola_ylenia — form provenance (runner report)

Not an N-400. Completed forms are two I-824s (Ezio Ossola, Lorena Bertagna),
notifying a new consulate of I-130s approved 2025-07-30, receipt IOE0923041286.
DS-260s are drafted but unfillable — blocked on the NVC welcome letter.

## THE FOUR-CATEGORY RULE SET TRANSFERS TO OTHER FORM TYPES
1. ID documents -> identity fields. Transfers exactly.
2. Questionnaire/resume -> addresses, contact, employment. Transfers, with
   scope reduced (I-824 needs current address only, no history).
3. Firm derives -> does NOT transfer to a notification form; there is nothing
   to compute, the dates come off the approval notice.
4. Firm supplies -> preparer block, institutional data. Transfers exactly.

**Conclusion: the provenance discipline is form-agnostic. The plugin's logic
generalises beyond the N-400.**

## Explicit consistency locks, quoted from the masterkey schema
- Surname must match the I-130 and the passport MRZ byte-for-byte.
- Given name likewise.
- DOB must be equal across I-130, passport and birth certificate.
- Place of birth city/country must match across I-130 and birth certificate.
- The I-130 receipt number on the I-824 must reconcile against the I-797
  notice — OCR uncertainty on trailing digits flagged for verification.

This is a MACHINE-READABLE version of the cross-document consistency rules the
other four matters only implied. Worth copying wholesale.

## A transcription error caught in the wild
The I-824 renders the city as "Commerico"; the resume and masterkey say
"Comerio". Same class of error as the malone "Ma Lone".

## What the corpus can and cannot supply
Available: names, DOBs, sex, places of birth, citizenship, current address,
phone, email, marital details, one child, Ezio's full work history
(Cagiva 1982-86, import-export 1984-90, real estate 1990-present), his
education, his military service (Italy, Aviation, Jul 1982 - Jul 1983),
passport numbers (Ezio YA8091797; Lorena YA6524423, expired 2024-06-26).

Absent: Lorena's parents entirely, Ezio's parents' birthplaces and
nationalities, complete address history since age 16 for both, Lorena's
pre-2021 employment and education, and the NVC case number.

That asymmetry — one applicant well documented, the other barely — is itself
worth reproducing in the synthetic data.

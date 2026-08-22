# Dogfood run — T2 `stavros_daphne` — the acceptance gate

BUILD-PLAN §6 layer 4. A solver was given a clean context and **only** what a
challenge-taker gets: the challenge article, the three worked pairs (input and
output), the Stavros input folder, and the blank forms. Masterkeys, the spec,
the templates, the registry, the briefs, the voice cards and the whole of
`tools/` were forbidden, as was the answer key. The solver's own honesty
statement records that it ran one `find` listing that showed the *names* of
forbidden files without opening any — declared rather than hidden, which is the
behaviour the gate wants.

## Verdict: PASS

The solver produced the correct packet into `lab/synthetic/dogfood/stavros_daphne/`.

**Document set — correct, 8 documents, both triggers right.**
1 Table of contents · 2 Cover letter · 3 Form N-400 · 4 Passport · 5 Permanent
Resident Card · 6 Tax return · **7 Travel addendum (C4)** · **8 Written
explanation (C6)**.

It derived C4 from the Part 8 table holding six rows against eight countable
trips, and C6 from the non-tabulable Part 9 answers. **It correctly excluded the
day trip**, generalising from W1. **It correctly fired C6 without any C5**, which
is the property W3 exists to teach and the reason T2's exhibit set was
redesigned in Phase 2.

**It caught Part 9 Items 8.a and 12** — the Phase 2 blocking finding. Those items
had been reachable only through a scan in the "extra things, probably not
necessary" pile, which W1 teaches solvers to treat as inert; Phase 4 gave them a
narrated surface in Daphne's own words. The solver found them there. That is the
fix working end to end.

**It inferred the exhibit rule in its own words**, unprompted: a fixed
identity/status/tax core, plus a document only where USCIS instructions point to
one for a specific form item, plus a written explanation where an item requires
disclosure but no official document exists. It also noted that the narrative
never goes into the form's own Part 14 — a house behaviour nobody stated
anywhere, inferred from two worked examples.

**It resolved the superseded address correctly**, by chronology, and
independently corroborated it against the address printed on the tax return.

**It picked the Elgin lockbox for New Jersey correctly**, generalising from two
worked examples (MA→Elgin, MI→Chicago).

## The two findings, both real, both acted on

**1. A data bug — fixed.** The 2015 account said the notices went to "an address
he'd already moved away from" while the address history showed continuous
occupancy from 2011 to 2024. Both could not be true, and the solver said so
rather than papering over it. Rewritten so the correspondence address on the
2013 filing was the *daughter's* — she filed the petition, gave her own address,
and moved in 2014 without updating a still-open case. The applicant never moved.
Corrected in the masterkey narrative and in her email 000004, in her own voice.
Recorded as SPEC-DELTA D-O.

**2. An ambiguity — left open deliberately.** Whether the military discharge
paper should be its own exhibit cannot be settled from three worked examples: it
is either documentary evidence for a disclosed Part 9 item (like W3's court
record) or inert over-delivery (like W1's second-email pile). The solver chose
inert, which matches the answer key, and named the discriminating rule it could
not find. Closing this would mean adding a fourth worked pair; the cost is not
worth it, and the ambiguity is recorded rather than hidden.

## Lower-confidence assumptions the solver declared
The city for the "Retired" employment row, and the exact filing date, are not
fixed by anything in the input. Neither changes the document set or any locked
fact. Recorded here so a future tightening pass knows where the slack is.

# PHASE 4 — INPUT FABRICATION. Carried requirements.

Six agents in parallel, one per client, corpus-quarantined. Each reads its own
`masterkey.norm.yaml`, `voice-card.md`, `brief.md` and nothing else about any
other client.

## THE BLOCKING FINDING FROM THE PHASE 2 REVIEW — must be fixed here

**`stavros_daphne` (T2) — Part 9 Items 8.a and 12 have no narrated input
surface.** T2's applicant did routine Greek compulsory military service
(1976–78), so Items 8.a and 12 are correctly `Yes` and route to Part 14. But the
masterkey's only input surface for those facts is a scan filed under
`over_delivered_not_used`, sitting beside two expired passports, a death
certificate and a utility bill — and T2's own voice card has the correspondent
say "Ignore whatever isn't useful" in the same breath.

Why that breaks the run: the worked pair W1 Almeida **demonstrates** that items
in the over-delivery bucket produce no document and no form change. A solver
generalising that demonstrated rule correctly will conclude the discharge paper
is equally inert and answer 8.a/12 `No` — failing the fact-level diff on **T2,
the first and never-cut dogfood target**.

**Required fix:** give Items 8.a/12 a **second, narrated surface, clearly
distinct from the inert over-delivery pile** — e.g. Daphne mentions her father's
army service in the body of an email in her own words, or the tidy table export
carries a "military service" row. The discharge scan may stay in the
over-delivery pile; what must change is that the *fact* is also stated somewhere
a solver reads as substantive. Update `input_surfaces` to record the new surface.

## The other Phase 2 review findings, already closed
- Finding 2 (T2's written explanation had no pinned narrative order) — closed in
  Phase 2: `stavros_daphne/masterkey.yaml` now carries
  `immigration.written_explanation_structure` with `order: [q20, q8a, q12]` and
  `lead_paragraph_is: q20`.
- Finding 3 (`rule_inputs.trips_trimmed` conflated the two C4 disjuncts) — closed
  in Phase 2: the normaliser now emits `trips_overflow_from_part8`,
  `trips_day_excluded` and `c4_reason` separately.

## Input shape
Email-directory convention `NNNNNN_YYYY-MM-DD_slug/` with a body `.txt` plus
attachments, per the corpus export shape (BUILD-PLAN §5).

## The bounded mess catalogue (BUILD-PLAN §5.3) — demonstrated before tested
| mess type | demonstrated in | reused in |
|---|---|---|
| folder named for the correspondent, not the applicant | W2 | T1 |
| blank questionnaire field, supplied later by email prose | W3 | T3 |
| superseded fact (later email wins) | W2 | T2 |
| day trip in travel list, excluded per firm instruction | W1 | T2 |
| phone-photo documents | W1 | T3 |
| password-protected attachment, password in a later email | W3 (benign, same thread) | T3 |
| over-delivery of unrequested documents | W1 | T2 |
| same client, multiple email addresses | W2 | T3 |
| unrelated-matter noise in the mailbox | W1 | T2 |

## Rules
- Every fact any output artefact consumes must be locatable on at least one
  input surface. The three `to-do` clients' packets must be **buildable** by a
  challenge-taker or the challenge is broken.
- Every mess event resolves deterministically; chronological precedence (latest
  client statement wins) is the standing rule.
- Document images come from `tools/fabricate_ids.py`. `finish="photo"` is for the
  phone-photo clients (`almeida_paulo`, `adeyemi_tunde`); everyone else uses
  `finish="scan"`.
- `input_surfaces` and `mess_events` in the masterkey must be updated to match
  what was **actually written**, not what was planned. The Phase 4 barrier checks
  the extracted text of the produced inputs, not the agents' claims.

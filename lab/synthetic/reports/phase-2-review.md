# Phase 2 barrier (b) — set review

**Reviewed:** 2026-08-22
**Scope:** all six `clients/*/masterkey.norm.yaml`, `registry.yaml`, all six `brief.md`, all six `voice-card.md`, `spec/SPEC-DELTA.md`, `spec/STYLE-SPEC.md` §9/§12/§16. No corpus files opened (`lab/jacobs_brent/`, `lab/zhu_vivian/`, `lab/izaguirre_jesus/`, `lab/malone_kyle/`, `lab/ossola_ylenia/` were not read).
**Barrier (a):** green, 79 checks, 0 warnings (`tools/validate_masterkeys.py`).

## Verdict: PASS WITH FINDINGS

The set reads as six different people. Six distinct professions (structural
engineer, veterinary technician, senior graphic designer, medical laboratory
technician, retired baker, process engineer), six distinct family shapes
(single / married-childless / divorced-with-child / married-with-child /
widowed-with-adult-child / married-with-child), six distinct income levels,
ages spanning 1957–1991, six states, six non-overlapping nationalities, and
six voice registers with no bleed between them (confirmed by reading all six
voice cards — the sample lines do not repeat a rhythm, a hedge pattern, or a
sign-off across clients). Every date derivation, MRZ check digit and
filing-window computation I re-checked matched the masterkeys' own
recomputation notes. The four negative controls (T3 spouse+child/no C1,
W3 child/no C3c, T1 319(a)+no C3b, T1 319(a)+no C2, T2 Part-9-Yes/no-C5,
T3 arrest/no-C6) are each genuinely present-as-data-but-absent-from-exhibits,
not merely asserted. The mess catalogue is demonstrated-before-tested in
every case bar one (T1's e-signature friction, correctly flagged in the
registry as extra, inert, consequence-free texture). Coverage of both bases,
all conditional-exhibit rules, and the lockbox/carrier/tax-year matrix is
real, not asserted — I re-derived several by hand against the underlying
masterkey fields rather than trusting `registry.yaml`'s own coverage-matrix
block, and they held.

One finding is blocking. It concerns T2 Stavros specifically — the client
BUILD-PLAN names as the first, never-cut dogfood target — and it is a defect
in the input-side data, not in judgment about whether the six read as a
believable set.

---

## Findings

### 1. [blocking] T2 Stavros: Part 9 Items 8.a and 12 have exactly one input
surface, and that surface is filed in the bucket whose worked-pair-demonstrated
resolution is "produces no document and no form change."

Path: `lab/synthetic/clients/stavros_daphne/masterkey.norm.yaml`,
`input_surfaces.moral_character.q8a` / `.q12`, and
`input_surfaces.over_delivered_not_used`.

The masterkey correctly sets `q8a: Yes` and `q12: Yes` (routine 1976–78
compulsory Hellenic Army conscription, honourably discharged) — this
resolution is right, and the masterkey's own `_authored_notes.item_8a_finding`
correctly catches and repairs a brief/registry disagreement to reach it. The
problem is upstream of that repair, in what the client's input thread actually
contains:

```yaml
moral_character.q8a:
- military_discharge_scan
moral_character.q12:
- military_discharge_scan
...
over_delivered_not_used:
- greek_military_discharge_scan
- greek_passport_expired_1_scan
- greek_passport_expired_2_scan
- death_certificate_scan
- utility_bill_scan
```

The discharge scan is the *only* surface for two `Yes` answers, and it sits
inside a list literally named `over_delivered_not_used`, alongside two expired
passports, a death certificate and a utility bill — none of which carries a
fact any output consumes. The voice card sharpens this: Daphne's sample line
introducing the discharge paper is "I'm also attaching a few things you didn't
ask for — his old Greek passports (two), the discharge paper from his
military service in Greece, my mother's death certificate, and a utility bill
with his name on it. **Ignore whatever isn't useful.**" No sample line on the
card narrates his army service as a fact; it is presented purely as clutter.

This is exactly the class of bug BUILD-PLAN §6 layer 4 calls a data bug, not
a solver bug — and it is squarely inside the acceptance gate the whole spike
exists to pass. W1 Almeida is the worked pair that teaches the
over-delivery rule (expired passport, lease, vaccination record — three items
that change nothing). A solver correctly generalising from W1 will conclude
that a scan sitting in the same rhetorical position ("here's some extra stuff,
ignore whatever isn't useful") is equally inert, answer 8.a and 12 as `No`,
and fail the fact-level diff against the answer key — on T2, the first and
(per BUILD-PLAN §10's cut order) never-cut dogfood run.

**What to change:** give 8.a/12 a second, narrative surface. Daphne should
say, in prose, something like "he also did his national service in Greece
years ago, standard two years, nothing remarkable — I'm attaching the
discharge paper in case it's relevant" — distinguishing it in tone and
placement from the genuinely-inert items (the expired passports, the death
certificate, the utility bill), which can keep the "ignore whatever isn't
useful" framing. The fix is Phase 4 input-fabrication work; this masterkey
only needs a note recording that `q8a`/`q12` require a narrated surface, not
merely a scanned one.

### 2. [should-fix] T2 Stavros: the written-explanation document (DOCUMENT 8)
has no content-structure block, and nothing downstream pins its narrative
order.

Path: `lab/synthetic/clients/stavros_daphne/masterkey.norm.yaml` (absent —
compare `lab/synthetic/clients/nowak_agata/masterkey.norm.yaml`,
`documents.written_explanation`, which has `covers: "Part 9 Item 20
(removal proceedings) ONLY — never the arrest"` plus a full ordered
narrative). T2's `documents:` block has no `written_explanation` key at all;
the only content lives in `immigration.history_for_the_written_explanation`
(a plain event list) and scattered `moral_character.q*.explanation` prose.

I checked whether this is enforced elsewhere: `templates/document-catalog.yaml`
fixes only `trigger`/`tab`/`file_stem`/`divider_title`/`toc_line`/`renderer`
for `written_explanation`, nothing about content or order.
`tools/validate_masterkeys.py` only asserts the document's *presence* when
`c6_fires` is true (`if r.get("c6_fires"): out.append("written_explanation")`)
— it does not check what the document says. So T2's answer-key content for
DOCUMENT 8 is currently undetermined, and T2's answer-key rendering is the one
BUILD-PLAN §10 explicitly keeps for the dogfood diff even under the cut order.

On the substance of the task's question ("could a solver fire C6 off the
military service and never engage Item 20?"): **no, not at the rule level.**
`rule_inputs.part14_items_yes: ['12', '20', '8a']` — all three share
`classification: part14`, and C6 fires from *any* non-tabulable `Yes`, so
narrative order cannot change *whether* C6 fires. The real risk this pairing
creates is finding 1 above (whether 8.a/12 are visible as `Yes` at all), not
signal confusion about C6 itself.

**What to change:** add a `documents.written_explanation` block to this
masterkey, shaped like W3's, that states explicitly that the narrative leads
with Item 20 (the 2013–2020 I-130/I-485/NTA/termination/LPR history — the
actual differentiator per registry D1) and covers 8.a/12 as a short,
clearly secondary paragraph. This is about the clarity of the shipped answer
key, not the correctness of the exhibit rule.

### 3. [should-fix] `rule_inputs.trips_trimmed` conflates two distinct C4/D7
disjuncts across all six clients.

Path: `tools/normalize_masterkeys.py` (the field it emits) and all six
`clients/*/masterkey.norm.yaml`, `rule_inputs.trips_trimmed`.

Registry decision D7 and STYLE-SPEC §9.2 draw a real distinction: a trip can
be missing from the Part 8 table because it's the row-count overflow (stays
on the addendum) or because it's a day trip (excluded from *both* the table
and the addendum). `trips_trimmed` currently counts both together with no way
to tell them apart:

| client | trips_trimmed | day trips (excluded from both) | row-count-only (addendum-only) |
|---|---|---|---|
| W1 | 2 | 1 | 1 |
| T2 | 3 | 1 | 2 |
| T1 | 1 | 0 | 1 |
| T3 | 1 | 0 | 1 |

This is currently harmless — I checked `validate_masterkeys.py` and it never
reads `trips_trimmed`, only the precomputed `c4_fires` boolean. But
SPEC-DELTA D-I's entire stated reason for `rule_inputs` existing is to give
Phase 5's `verify_client.py` one designated place to read from "rather than
each re-deriving the rule with their own heuristics," specifically to avoid
silent disagreement. A future verifier that wants to assert D7's resolution
("the day trip appears on neither the form nor the addendum") per mess event
cannot do it from this field alone.

**What to change:** before Phase 5 is built, split this into two fields (e.g.
`trips_addendum_only` and `trips_excluded_entirely`) in the normaliser and
regenerate all six `.norm.yaml`.

### 4. [note] `stavros_daphne/brief.md`'s over-delivery row is slightly
overbroad given the masterkey's own later correction.

Path: `lab/synthetic/clients/stavros_daphne/brief.md`, the mess-events table
("Over-delivery... No §9.2 rule triggers on any of them; none enters the
packet"). True for the packet (none of the five items becomes its own
exhibit), but read in isolation it doesn't flag that one of the five
corroborates a required `Yes` answer, which the masterkey's own
`_authored_notes.item_8a_finding` had to catch and repair. Phase 4 reads the
masterkey, not the brief, so this doesn't currently block anything — but the
brief is the more human-readable artefact and is worth tightening to match
the masterkey's own resolution, for whoever reads it next.

### 5. [note] Konstantinos Stavros (T2) has an unexplained ~5-year gap between
first U.S. entry (2011, age 54) and his first recorded U.S. employment (2016,
baker), outside the N-400's required 5-year employment window and so not a
build defect, but worth a name-check.

Path: `lab/synthetic/clients/stavros_daphne/masterkey.norm.yaml`,
`identity.first_entered_us` vs. `employment[0].from`. The gap is not required
to be closed (Part 7 typically covers the residence window, 2021–2026, which
this masterkey covers gap-free), and the removal-proceedings narrative
(2015–2018) offers a plausible real-world account of why formal employment
might have been slow to start. No action needed; recorded so it isn't
mistaken for something this review missed.

### 6. [note] Wisconsin court-venue naming on T3's court records is
organisationally imprecise but deliberately so, for leakage-safety reasons
already documented in the masterkey.

Path: `lab/synthetic/clients/adeyemi_tunde/masterkey.norm.yaml`,
`documents.evidence[0].court_name_and_location: "Circuit Court, Fitchburg,
Wisconsin"`. Wisconsin circuit courts are organised by county, not
municipality, so a fully realistic label would read "[County] County Circuit
Court." The masterkey's own leakage note explains the real county name and
county-seat city were blocklist hits and were deliberately avoided. Cosmetic;
no action needed.

---

## Item 8.a/12 judgement, in one sentence (per the task's REPORT BACK)

The C6 rule itself is not muddied — all three non-tabulable Part 9 `Yes`
answers (8.a, 12, 20) independently satisfy C6 regardless of narrative order —
but the input side currently gives 8.a/12 no narrated surface at all, only a
scan filed in a bucket whose demonstrated resolution is "ignore," which is a
real risk that a solver answers those two items `No` and fails the first
dogfood diff; that is finding 1, and it needs the narrative reordered *and*
the input surfaced, not just reordered.

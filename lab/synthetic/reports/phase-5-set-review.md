# Phase 5 barrier — layer 3, SET REVIEW

**Reviewed:** 2026-08-22
**Scope:** all six `clients/*/masterkey.norm.yaml`; `registry.yaml` including its
`phase_2_review` block; all six `clients/*/voice-card.md`;
`reports/phase-2-review.md`; `reports/phase-5-scripted.md`; `spec/SPEC-DELTA.md`;
`templates/document-catalog.yaml`; `PHASE-4-BRIEF.md`; `PHASE-6-BRIEF.md`;
`content/21-challenges/01-challenge-one.md` (to establish what the solver is
actually handed); and **every `body.txt` in all six `clients/*/input/`** — 46
e-mail bodies, 882 lines.
**Not read:** `lab/jacobs_brent/`, `lab/zhu_vivian/`, `lab/izaguirre_jesus/`,
`lab/malone_kyle/`, `lab/ossola_ylenia/` (corpus quarantine honoured); and no
`clients/*/output/` packet was opened.
**Scripted gates:** all five green, taken as proven (`reports/phase-5-scripted.md`).
No arithmetic, field coverage, collision or leakage result was re-derived.

## Verdict: PASS WITH FINDINGS

**0 blocking · 4 should-fix · 3 notes.**

The set is good, and the honest headline is that the hard parts landed. The six
threads read as six different people writing e-mail, not as one register wearing
six names — the distinctions survive stripping the salutations, which is the
only test that means anything. Each packet reads as a life rather than a fact
table: the dates, the professions, the immigration routes and the family shapes
support each other, and in several places the input volunteers the *reason* a
date looks odd before a reader can wonder about it. The Phase 2 blocking finding
is closed properly — not with a bolted-on sentence but with a paragraph that a
worried daughter would plausibly write, in a different message, on a different
date, from the "ignore whatever isn't useful" pile. Both generalisation gaps are
bridgeable, and the C5/C6 one is bridged well enough that it is hard to fail.

Nothing here is blocking. I considered calling finding 1 blocking — one Phase 4
fabricator invented a firm e-mail address and shipped it in twelve files — and
decided against it deliberately, because this run already has a working
definition of the word and that defect does not meet it. Phase 2's single
blocking finding was blocking because it sat "squarely inside the acceptance
gate the whole spike exists to pass": it would have failed the dogfood diff.
Finding 1 does not touch the dogfood; it is a plausibility and house-rule defect
in shipped material, which is what `should-fix` is for. Two different meanings of
`blocking` in one `registry.yaml` would be worse than a slightly generous
severity, so the vocabulary stays consistent with Phase 2's. Finding 1 is
nonetheless the first thing to fix: it is cheap, its remedy already exists
elsewhere in the set, and it is the one detail that punctures the one-firm
illusion on sight.

---

## Findings

### 1. [should-fix] The firm runs its casework queue on its own clients' consumer webmail domain, on an address invented in Phase 4 that is in the registry's namespace nowhere

**Artefact:** all twelve `lab/synthetic/clients/adeyemi_tunde/input/*/body.txt`.

Every message in T3's thread carries `casework@brightpost.net` — six as `From:`,
six as `To:`. Three things are wrong with it, in descending order of how much
interpretation each requires.

**The domain is wrong on its face, and this argument needs no reading of any
ruling.** `registry.yaml` line 212 declares `quillmail.com` and `brightpost.net`
to be the two *invented consumer mail domains*. `brightpost.net` is already Liam
Kavanagh's personal address (`liam.kavanagh@brightpost.net`) and Daphne
Stavros's personal address (`daphne.stavros@brightpost.net`). A law firm doing
naturalisation work does not run its casework queue on the same consumer webmail
provider two of its clients use for their private mail. A reader who opens two
input folders sees it immediately, and it is the single detail in the whole set
that breaks the "one firm, six clients" illusion on sight.

**The address never entered the set-level namespace.**
`collision_check.emails` records `count: 11` and lists eleven addresses;
`casework@brightpost.net` is not among them. It was therefore never
collision-checked and never whole-token scanned against `blocklist.txt`. The
actual leakage risk is near zero — `brightpost` is already a cleared invented
token and `casework` is an ordinary English compound — so this is a process gap
rather than a live hazard. It exists because `PHASE-4-BRIEF.md` says nothing
about headers at all (finding 3), so the fabricator improvised outside the
registry that exists to prevent exactly this.

**And it sits at least in tension with §16 ruling 7.** The ruling is **UPHELD AND
EXTENDED**, and its "Consequences later phases must honour" reads: *"Phase 2's
registry invents no firm name, no preparer name, no business address, no firm
phone or email. Nothing downstream may reintroduce one."* `registry.yaml`'s
`firm:` block repeats it and adds "or any other page." I do not lean on this as
the primary argument, and it is why the finding is not blocking: every instance
r7 names — cover letter, signature block, N-400 — is a *packet* component
authored by the firm, and the sentence was written in Phase 2, before input
fabrication existed. That the T2 fabricator independently read it broadly enough
to write `To: Petition Preparer` is evidence about the missing convention
(finding 3), not proof of the ruling's scope. The domain collision decides this
finding on its own; r7 makes the fix obvious rather than optional.

**No script can see any of it.** `verify_set.py` scans for *corpus* leakage;
nothing anywhere asserts the absence of a *firm* identity, or that every address
in a shipped body is one of `collision_check`'s eleven. This is the class of
defect the layer-3 reviewer exists for.

**What to change.** The set already contains a clean solution, invented
independently by the T2 fabricator: Daphne's five bodies address the firm as
`To: Petition Preparer` — the unattributed role line that SPEC-DELTA D-B
establishes as the compliant form. Rewrite T3's twelve headers to match:
`From: Petition Preparer` on the six firm-side messages,
`To: Petition Preparer` on the six client-side ones, and delete
`casework@brightpost.net` from the build. Then add the assertion to
`verify_set.py` — a whole-token scan of every shipped `body.txt`, cover letter
and form field for any address, telephone or proper noun that is not in
`collision_check`'s eleven-address list — so ruling 7 acquires a gate instead of
relying on a reviewer noticing.

---

### 2. [should-fix] W2 Kavanagh has a fifteen-month employment hole and a five-month address hole inside the five-year window — and it is a *worked pair*, so it teaches the hole

**Artefact:** `lab/synthetic/clients/kavanagh_liam/masterkey.norm.yaml`
(`employment`, `addresses`) and
`clients/kavanagh_liam/input/000007_2025-12-18_arrival-and-travel/body.txt`;
knock-on in `registry.yaml` `collision_check.employers`.

Siobhan Brennan first entered the U.S. **2021-08-19**. W2 files **2026-02-10**,
so the Part 6/Part 7 five-year window opens **2021-02-10** and her entry falls
inside it. Her records begin:

| | first row | hole inside the window |
|---|---|---|
| employment | Riverbend Veterinary Clinic, from `2022-11-14` | 2021-08-19 → 2022-11-13, ~15 months |
| addresses | Cicero IL, from `2022-01-10` | 2021-08-19 → 2022-01-09, ~5 months |

She is the only one of the six with an unfilled stretch in-window. I checked all
six against their own filing dates: W1, W3, T2 and T3 are continuously employed
and continuously addressed across the whole window, and **T1 closes the identical
problem explicitly** with a masterkey row reading
`Not employed (homemaker, at home with the child)` spanning `2020-05-27 →
2023-01-08`.

Two things make this more than a blank cell.

**The input contradicts the answer key.** Liam's own words in `000007` are: *"Siobhan
first came out here on the 19th of August, 2021 … she came for work originally
and we met after."* The packet then records no work for the following fifteen
months. A reader who notices is reading a packet that disagrees with the file it
was built from.

**The firm is demonstrably inconsistent with itself.** It chases gaps hard
elsewhere. T3's `000007` opens: *"Your address history has a gap. You gave us
Middleton from June 2021. Where were you immediately before that, and for what
dates?"* — and T3's `000008` supplies the missing Verona row. T1 volunteers the
rule outright (*"that's also when our address history starts, since obviously she
didn't have a U.S. address before she arrived"*). For W2 the firm asked when
Siobhan moved *into* Quarry Lane (answered in `000011`: 10 January 2022) and then
never asked where she was before that. Same firm, same window, opposite
diligence — and the client it skipped is one of the three the reader is told to
imitate.

**What to change.** Add to `kavanagh_liam`'s masterkey an employment row and an
address row covering `2021-08-19 → 2022-01-09` / `2021-08-19 → 2022-11-13`, and
surface them in a Liam message in his register — naming the job she "came for
work" to do is the natural fix and closes both holes at once, since a first
employer implies a first address. This is safe on the exhibit side: W2's conditional set is
`{C1, C2, C3b}` and none of those triggers on employment or address rows; her
four trips stay under the six Part 8 rows, so C4 still does not fire and the
exhibit set stays pairwise distinct. It is not a one-file edit, though. Naming a
first employer adds a twelfth entry to `collision_check.employers`, which the
registry asserts unique — so the change needs a whole-token `blocklist.txt` check
on the new name, a registry edit, a re-render of W2's example output, and a
re-run of `verify_coverage.py` and `verify_set.py`.

---

### 3. [should-fix] The six threads use four different conventions for representing the firm, and T3 uses a different header format from the other five

**Artefacts:** all six `clients/*/input/*/body.txt`; root cause in
`lab/synthetic/PHASE-4-BRIEF.md`.

Six Phase 4 fabricators each owned one client's distinctiveness. Nobody owned the
firm, and it shows in the envelope rather than the prose:

| client | how the firm appears | `To:` header | `Date:` format | `From:` format |
|---|---|---|---|---|
| W1 Almeida | not at all — replies to unseen asks | absent | `October 16, 2025` | `Name <addr>` |
| W2 Kavanagh | not at all | absent | `December 2, 2025` | `Name <addr>` |
| W3 Nowak | not at all | absent | `March 30, 2026` | `Name <addr>` |
| T1 Tran | a quoted request block, no address | absent | `April 27, 2026` | `Name <addr>` |
| T2 Stavros | `Petition Preparer` | present | `January 26, 2026` | `Name <addr>` |
| T3 Adeyemi | six full firm-side messages at a firm address | present | `2026-05-11` | bare address |

Two separate problems live in that table.

**The firm's half of the correspondence exists in exactly one of six threads.**
Five clients answer numbered questions that are nowhere on disk; T3's firm writes
six messages. This is defensible — T3's voice card requires the firm's numbered
questions to exist (*"Numbered answers matching the firm's numbered questions,
with no restatement of the question"*), and his registry modality is "password
chase," which needs an asker. T1's quoted-request block is a third, lighter
solution to the same need. But three solutions to one problem, distributed at
random across six folders, is not a house convention; it is six people improvising.
The consequence for the reader is that the firm has one voice sample in the whole
corpus, so nothing in the set can contradict it and nothing can confirm it either.

**T3's envelope is the odd one out on three axes at once** — ISO dates, bare
addresses, `To:` present. Headers are written by a mail client, not by a
correspondent, so T3's ISO `Date:` cannot be motivated by his register the way
his prose can. Six threads exported from one firm's mailbox should have one
header format.

**What to change.** Pick one convention and state it in the brief that Phase 4
should have had: `From:`/`To:`/`Date:`/`Subject:` on every message, `Name <addr>`
for clients, `Petition Preparer` for the firm (finding 1's remedy), and one date
format — `Month D, YYYY`, which five of six already use. Then decide the
firm-half question deliberately rather than per-fabricator: either every thread
carries the firm's asks, or none does and T1's quoted-block idiom is adopted
wherever an ask must be visible. T3's twelve messages are being edited for
finding 1 regardless, so the header normalisation costs almost nothing extra.

---

### 4. [should-fix] `normalize_masterkeys.py` did not finish the job D-I set it: one derived fact carries two names split 3/3, and three clients carry two live copies of height and weight

**Artefacts:** `lab/synthetic/tools/normalize_masterkeys.py` and all six
`clients/*/masterkey.norm.yaml`.

SPEC-DELTA D-I's stated purpose is that "everything from Phase 3 onward reads
only the `.norm.yaml`," so that a consumer cannot silently read `None` off a
spelling nobody unified. A path-by-path diff of the six normalised files against
each other shows the promise is not kept. Ignoring divergences that are genuinely
fact-driven (no `family.spouse` block for the unmarried, and so on), three
residues remain:

1. **`immigration.derived.early_filing_date` vs `.earliest_filing_date`** — the
   same computed fact under two names, split exactly three and three:
   `early_filing_date` on almeida, kavanagh, adeyemi; `earliest_filing_date` on
   nowak, tran, stavros. Neither client set carries the other spelling. Any
   consumer that picks one name reads `None` for half the set — and `None` on a
   filing-window date is the silent-failure shape D-I was written to eliminate.
2. **The normaliser adds the canonical key without removing the original.**
   `kavanagh_liam` carries `identity.height_ft: 5` / `height_in: 6` at lines 25–26
   **and** a nested `identity.height:` block at line 37. `tran_daniel` carries
   `height_feet`/`height_inches` at lines 46–47 **and** `height:` at line 54.
   `adeyemi_tunde` carries `weight_lb: 185` at line 33 **and** `weight_lbs: 185`
   at line 39. The values agree today. Nothing asserts they will after the next
   edit, and a hand-fix to one copy is invisible to the other.
3. **`first_entered_us` sits under `immigration:` for `nowak_agata` and under
   `identity:` for the other five** — the container-level version of the same
   miss.

This is not currently doing damage: D-L note 3 records that three renderers built
closed alias resolvers that **raise on an unknown spelling rather than guess**,
which is the correct failure mode, and every scripted gate is green. But that is
mitigation distributed across N consumers, which is precisely the arrangement
D-I's own reasoning rejects — *"a shim only works if every one of them remembers
to use it."* Phase 6 and any future answer-key re-render add consumers.

**What to change.** Extend the normaliser to (a) canonicalise
`early_filing_date` → `earliest_filing_date` across all six, (b) *delete* the
source spelling once the canonical key is written rather than leaving both, and
(c) move `nowak_agata`'s `first_entered_us` under `identity:`. Then add a
`validate_masterkeys.py` check that the six normalised files have identical key
sets modulo an explicit fact-driven allow-list — the same differential idea as
D-M's sweep A, applied to the masterkeys instead of the form.

---

### 5. [note] The closest voice pair is W1 Almeida / T3 Adeyemi — they are distinguishable, and they are also the closest pair biographically, which is worth knowing but not worth changing

**Artefacts:** `clients/almeida_paulo/` and `clients/adeyemi_tunde/`.

The task names this pair, and it is the right pair to worry about. They are the
two low-affect, list-making, unbothered registers, and stripping the salutations
(`Hello,` / `Paulo` versus nothing / `TA`) is the test that matters. They pass it,
on at least five independent tells:

- **Bare numbered answers.** Adeyemi's signature move is a numbered answer with no
  framing sentence at all — `1. 396-70-2841.` / `2. 2016-01-11.` Almeida never
  once writes one; his lists are always inline prose behind a colon (*"Attached:
  questionnaire, photos of the green card front and back, …"*).
- **Sentence length.** Adeyemi's longest sentence in twelve messages is about
  twelve words. Almeida routinely runs to thirty — *"that one was a same-day
  drive, I left in the morning and was back the same night, no hotel."*
- **Unasked context.** Almeida volunteers it constantly: why the Toronto trip is
  flagged, that there is "no gap" in the employment, his cousin's visa. Adeyemi
  volunteers nothing — he states an arrest in nine words and offers no account of
  it, exactly as his card forbids.
- **Punctuation.** Almeida's spaced hyphen-as-dash appears in four of five
  messages; Adeyemi uses full stops only.
- **Dates and thanks.** Adeyemi writes ISO in prose (`2023-06-24`, `2016-01-11`)
  and never thanks. Almeida writes `31 October 2019` and signs off `Thanks.`
  twice. (One wobble: Almeida's `000004` writes `03/01/2016 to 04/04/2019` in
  prose, against his own card's rule that prose gets `22 March`. It is
  defensible — he is dictating form data — and it is one line.)

What is worth recording is that the closest **voices** are also the closest
**lives**: two engineers, both employment-based `E21`, both filing 316(a),
in a set where the other four biographies share nothing. The similarity therefore
compounds rather than cancelling. It still does not collapse them — single vs
married-with-a-daughter, Brazil vs Nigeria, MA vs WI, no Part 9 history vs an
arrest and court records, a five-message client-only thread vs a twelve-message
firm-driven one — and every scripted distinctness gate is green. **No change
recommended.** Recorded so a later reader does not mistake it for something this
review failed to look at. If a future revision needs slack, changing one of the
two class-of-admission codes is the cheapest lever.

---

### 6. [note] The ordering *within* the C3 cluster is never demonstrated; T1 gets it right only because its input happens to list the two documents in catalog precedence order

**Artefacts:** `templates/document-catalog.yaml`;
`clients/tran_daniel/input/000004_2026-05-04_deed-child-passport-auto-insurance/body.txt`.

The registry is explicit that the C3b → C3a/C3c **rule** gap is intended
("the rule is shown once, on one document, and must be applied to two it was
never shown on"), and I agree it is bridgeable — see the generalisation judgement
below. But one consequence of the design is not written down anywhere: because W2
supplies exactly one C3 document, no worked pair ever shows two C3 documents in
sequence, so the catalog's `C3a → C3b → C3c` precedence is unobservable. T1 needs
`JOINT DEED` at DOCUMENT 8 and `CHILD'S PASSPORT` at DOCUMENT 9. A solver
grouping by kind — putting the child's passport next to DOCUMENT 4 `PASSPORT` and
DOCUMENT 7 `SPOUSE'S PASSPORT` — would invert them, and the fact-level diff would
catch it as a defect of the materials rather than of the solver.

What saves it is luck that should be recorded as a design property: the quoted
firm request in T1's `000004` lists the items **deed · child's passport · auto
policy**, which is `C3a · C3c · C3b` — precedence order for the two that are
supplied. That is the only ordering cue in the shipped materials.

**No change recommended** — closing the gap by giving W2 a second C3 document
would cost the pairwise-distinct exhibit-set property, which is worth more.
Recorded so that whoever sets the dogfood diff's tolerance knows that
within-cluster C3 ordering is a coin flip resting on one line of one e-mail.

---

### 7. [note] Two known plausibility blemishes are inherited and confirmed; the entry-to-first-record gap is structural, not per-client sloppiness

Neither was silently dropped, and neither rises to set level.

- **Phase 2 note 5** — `stavros_daphne`: first entry 2011-05-14, first recorded
  employment 2016-03-07. Still present, still outside the five-year window, still
  explained in-world by the 2015–2018 removal proceedings. Confirmed as a note.
- **SPEC-DELTA D-L, "one open data gap"** — `tran_daniel`'s
  `documents.tax_return` carries no dependant despite `family.children` listing
  Mai Linh, born 2021, a child of the marriage. D-L hands this to the *per-client*
  reviewer, and I leave it there; it does not affect the return's §9.3 rule 1
  function as marriage evidence, which turns on the two spouses' names.
- **Worth adding, because it reframes both:** the same shape appears on
  `almeida_paulo` (entry 2015-09-02, first record 2016-02-15) and
  `adeyemi_tunde` (entry 2016-01-11, first record 2019-09-20). Three of six show
  an entry-to-first-record gap, all three entirely outside their five-year
  windows. That is the masterkey schema behaving as designed — it carries the
  window, not the life — not three fabricators being careless. Finding 2 is a
  different animal precisely because W2's gap falls *inside* the window.

---

## The task's four judgements, answered directly

**Six people, or one person six times? Six people.** No two of the six could be
confused from prose alone, and I could not name a pair I failed to tell apart.
The registers separate on mechanics that survive removing every name and
salutation: Kavanagh's comma-spliced `and/so/but` chains and genuine exclamation
marks; Stavros's parenthetical hedges, statements ending in question marks, and
single ALL-CAPS words (`DENIED`, `TERMINATED`, `OLD`) — she never uses an
exclamation mark and he never uses caps, which alone separates the two warm
registers the task asked about; Nowak's article-dropping before institutional
nouns (*"I attach scan of both sides"*) and her full-name sign-off every time;
Tran's restate-then-answer numbering and his invariable closing *"Let me know
what you need next and I'll get it turned around tonight"*, against Ha's six-word
corrections; and the Almeida/Adeyemi separation set out in finding 5. The
two-speaker threads hold their asymmetry — Ha writes twice and is right both
times; Siobhan appears only as reported speech, as her card requires.

**Does each packet tell one coherent story?** Yes, and in more than a
constraint-satisfying way. The immigration routes carry their own logic and the
input often anticipates the reader's objection: Tran does the conditional-resident
arithmetic out loud in `000001` item 5 and concludes `IR6`, not `CR6`, which is
also T1's C2 negative control stated in the client's own voice; Kavanagh's `CR6`,
seven-month marriage, expired card and pending I-751 form a single causal chain
he narrates in the order he learned it; Stavros's `IR5` requires a U.S.-citizen
petitioning child over 21, and Daphne is 25 at her 2009 naturalisation and files
the I-130 in 2013; Konstantinos, born 1957, serves March 1976 – February 1978,
which is the right age for the right conscription in the right country. Adeyemi
states the C1 negative control himself — *"My wife is a permanent resident. She
is not a citizen."* The one place where the story and the file disagree is
finding 2.

**Is the firm's behaviour consistent across the six?** Mostly, and the exceptions
are findings 1, 2 and 3 — none of them blocking, all of them worth fixing before
the materials ship. What *is* consistent is the substance: the same
conditional-exhibit rules applied the same way, the same lockbox/carrier
derivation, the same tax-year rule, the same six core documents in the same
order, and — this is the good part — the firm sensibly using a different
instrument per client (docx questionnaire, xlsx, prose, phone call, delegated
spreadsheet, numbered e-mail) while extracting the same Part 9 battery from all
six. What is inconsistent is the firm's *presence*: it chases an address gap on
T3 and leaves a larger one on W2, and it appears in four different guises across
six mailboxes.

**Are the two generalisation gaps bridgeable?** Yes, both — with the caveat in
finding 6. This matters more than it might, because
`content/21-challenges/01-challenge-one.md` hands the solver only the three
worked pairs and the three test inputs. No STYLE-SPEC, no `document-catalog.yaml`,
no rule statement. Every rule must be induced from three examples.

- **W2's C3b → T1's C3a and C3c.** Bridgeable, and better supported than the
  registry claims. Three cues stack. (i) W2's `000009` paraphrases the firm's ask
  as a *category*, not a document: *"you asked if we had anything else showing we
  share our finances or our life together … so I dug out our auto policy."* A deed
  and a child's passport sit inside that category on any reading. (ii) T1's
  `000004` quotes the firm's request naming all three candidates as evidence, and
  Daniel declines the auto policy in his own words — *"it's in my name only, so I
  don't think it helps you"* — which signposts the negative control rather than
  hiding it. (iii) The child's passport is a near-mechanical extension of a
  pattern the solver sees **twice**: core DOCUMENT 4 `Bio page of latest passport
  of the applicant` and W2's `Bio page of latest passport of the applicant's
  spouse` make `…of the applicant's child` almost forced. `Joint deed` sits the
  same way against `Joint automobile insurance policy`. The residual risk is
  ordering, not inclusion — finding 6.
- **W3's C5 and C6 → T2's C6 without C5.** Bridgeable, and this one is bridged
  well. W3 does not merely carry the two triggers from unrelated events; it puts
  them in **separate messages, on separate dates, under separate subject lines
  that name the form item** — `…- Item 15.b` (arrest → court records) and
  `…- Item 20` (removal proceedings → written explanation). A solver cannot
  easily read those as one coupled rule. T2 then closes the loop from the other
  side: in `000004` Daphne asserts Item 20 and pre-emptively negates Item 15 in
  the same breath — *"he was never arrested, never detained, never charged with
  anything — this was entirely about the missed mail."* T3 is the mirror image,
  equally explicit (*"All other Part 9 questions: No."*). The 2×2 truth table in
  `coverage_matrix.moral_character_truth_table` is not just populated on paper;
  each cell is stated in a client's own words.

## The Phase 2 blocking finding: verified closed, on the input side and in the masterkey

**It landed, and it reads naturally.** I checked placement before presence, which
is the test that distinguishes a fix from a gesture.

- **It is not in the over-delivery pile.** The inert pile is `000002`
  (2026-01-29, *"A Few Extra Things (Probably Not All Necessary)"*), which still
  ends *"Ignore whatever isn't useful"* and still lists the discharge paper
  alongside two expired passports, a death certificate and a utility bill — all
  correctly left inert. The narration is in **`000004`, 2026-02-24**, a different
  message, twenty-six days later, on the subject *"About 2015 (This Is the Part
  That Worries Me)."*
- **It narrates both items, as facts, not as an attachment.** Item 8.a: *"He
  served in the Hellenic Army, Infantry, as a Private, from March 1976 to
  February 1978 — two years, routine national conscription."* Item 12, which is
  the one that could easily have been forgotten: *"As part of it they did give
  him ordinary weapons and basic infantry training, standard for every conscript."*
  Branch, rank, dates and training are all in prose.
- **It re-classifies the scan rather than ignoring it.** *"I have the actual
  discharge paper from that — it's in the pile of extra things I sent a couple of
  weeks ago — but I wanted to say it here in my own words too, in case that scan
  isn't what you need for the form."* That single sentence lifts the document out
  of the inert bucket without contradicting `000002`, and it is the mechanism by
  which a solver correctly generalising W1's over-delivery rule still lands on
  `Yes`.
- **It is in her register.** *"One more thing while I'm thinking about it, and I
  don't want to bury it under everything above — I know the form also asks about
  any military or police service, and I don't want to leave that blank either."*
  Second person, anticipating the reader, hedged, apologetic about ordering,
  volunteering more than asked. Nothing about it reads as inserted. It is
  appended after the Item 20 narrative rather than leading — which she flags
  herself — and that placement deliberately mirrors
  `immigration.written_explanation_structure.order: [q20, q8a, q12]`.
- **The masterkey was updated too, not just the e-mail.**
  `input_surfaces.moral_character.q8a` and `.q12` now read
  `[email:0004, greek_military_discharge_scan]` — narrated surface first, scan as
  corroboration — where Phase 2 quoted `[military_discharge_scan]` alone. The
  mess catalogue gained an explicit entry recording the wrong and right surfaces.

**Phase 2's other two findings also closed**, which I checked because a fix that
lands alone often means the others were forgotten. Finding 2:
`immigration.written_explanation_structure` now exists on `stavros_daphne` with
`covers`, `order: [q20, q8a, q12]`, `lead_paragraph_is: q20` and a `render_note`.
Finding 3: `rule_inputs` now carries `trips_overflow_from_part8` and
`trips_day_excluded` alongside `trips_trimmed` on all six, and the counts match
the Phase 2 table exactly — day trips on W1 and T2 only.

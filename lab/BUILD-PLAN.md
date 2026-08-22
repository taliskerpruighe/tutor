# BUILD-PLAN — six synthetic clients for challenge one

Written 2026-08-21, second half of spike challenges/spike-002. Inputs: the
challenge text (`content/21-challenges/01-challenge-one.md`), the decisions in
`lab/NOTES.md`, the corpus map in `lab/FILE-MAP.md` **including the §7
correction pass** (ossola_ylenia re-synced; five reports rewritten; it is a
fifth N-400 packet, not a non-matter), the 25 runner reports in
`lab/reports/`, and the 9-sprint DS-260 masterkey prior art. Note on that
prior art: it was read in full before the ossola re-sync; the re-synced folder
(`7-sprint/` + `emails/`) no longer carries it on disk. Its schema is
summarised in FILE-MAP §3 and its adopt/reject rationale is §3 of this plan —
nothing in this plan depends on the deleted files.

Everything in section 1 was **tested by execution during planning**, not
assumed. The riskiest unknown — whether the packet can be rendered at all with
the local toolchain — is already resolved.

---

## 0. THE TWO DECISIONS THAT SHAPE EVERYTHING ELSE

### 0.1 The fork: perfect pairs or deliberate loss

FILE-MAP's central finding is that the firm's real transcription is lossy
(malone: "Ma Lone", 10th St -> 16th St, vanished employers, vanished child).
Should the synthetic pairs reproduce that?

**Decision: the pairs are internally perfect at the fact level. All mess lives
on the input side, and every piece of it has a deterministic resolution. No
transcription loss is seeded into any output.**

Justification:

1. *What the challenge tests.* The taker's plugin is judged by producing
   output "as close as possible" to the examples. If the examples carry
   errors, a diligent solver either reproduces errors as house style (teaching
   garbage-emulation) or notices input/output disagreement and cannot tell
   which side is authoritative. Either way the challenge stops being solvable
   by reasoning and starts being solvable only by luck. This is a Level 2
   course, not a forensics exam.
2. *What the firm's lossiness actually is.* It is a fact about a manual
   process. The plugin is supposed to beat the manual process — that is the
   course's point. An output that is the *correct* resolution of a messy input
   is the right target.
3. *Verification collapses without a clean invariant.* With perfect pairs the
   verifier asserts `output == f(resolved input)` with no carve-outs. With
   seeded errors, every future regeneration diff is ambiguous — "is this
   drift or a deliberate error?" — and the verifier needs a second ledger of
   intended wrongness. That doubles the machinery for negative teaching value.
4. *The instructive half of lossiness survives.* What made the malone finding
   valuable is cross-document disagreement. That is preserved — on the input
   side, where it belongs: a questionnaire answer superseded by a later email,
   a blank field filled by prose months later, a day trip that the firm's own
   instructions say to exclude. The output is the packet a careful firm would
   have filed. Chronological precedence (latest client statement wins) makes
   every disagreement resolvable, and the resolution is recorded in the
   masterkey.

What we knowingly give up: a malone-style "audit the firm's transcription"
exercise. That is not what challenge one asks for. The same decision covers
the ossola correction's "soft inconsistencies to imitate" — three dates for
one filing, a continuous-residence computation short on its face. Those are
output-side inconsistencies, and they stay out for the same reasons the
transcription loss does: an output-side wrinkle either gets copied as house
style or poisons the `output == f(input)` invariant. Their input-side cousins
(a re-signature request months later, unexplained silence) remain available
as email texture in the input threads, where they cost nothing.

**A second fork the correction pass surfaced: born-digital outputs or
simulated scans.** 54 of 185 corpus PDFs are image-only, including two of the
five filed N-400s (jacobs, ossola — printed, signed, scanned). **Decision:
every synthetic output is born-digital**, on the zhu model (the newest
generation, an AcroForm N-400 with a digital signature). Three reasons: the
challenge-taker's plugin can only ever produce born-digital output, so a
scanned worked example would set a target the plugin cannot match — "as close
as possible to the examples" must be achievable; a text-layered example keeps
a Level 2 challenge tractable (the taker's agents can pdftotext the worked
packets instead of reading 60 pages visually); and zhu is precedent that the
firm itself files born-digital. The scan-reading problem is still exercised —
on the *input* side, where phone photos of cards and notices belong to the
real problem being simulated.

**The learnability rule that keeps the mess fair:** no mess type appears in a
test-client input unless the same mess type appears, with its resolution
demonstrated, in at least one worked pair. The bounded mess catalogue is in
section 5.3.

### 0.2 The context problem: how one agent reviews cross-cutting artefacts

A packet is cross-cutting — cover letter, TOC, N-400 and exhibits must agree
with each other and with the input — and six clients' documents do not fit in
one context. The answer here is architectural, in three parts, not a bigger
context window:

1. **Facts flow forward through one small artefact.** Each client is fully
   described by a masterkey YAML (~300 lines, ~8 KB). Every generator — input
   fabricator, N-400 filler, cover-letter renderer — reads the masterkey, never
   another document. Consistency inside a client is therefore achieved **by
   construction**: two documents agree because they were rendered from the same
   key, not because someone checked them against each other afterwards.
2. **Mechanical work is scripts, not agents.** The N-400 fill, the cover
   letter, TOC, cover pages, the merge, the flatten — all deterministic
   renderers driven by the masterkey (toolchain proven, section 1). Agents do
   only the judgment work: casting, voice, email prose, review. What a script
   rendered from the key does not need an agent to re-derive.
3. **Verification flows backward, against extractions, never raw corpora.**
   Scripted verifiers re-extract facts from the *rendered* artefacts
   (pdftotext, pypdf field reads, docx reads) and diff them against the
   masterkey — cheap, exact, no context cost. Agent reviewers are reserved for
   what scripts cannot judge (plausibility, voice, look-and-feel), and the one
   *set-level* reviewer reads only compressed representations: six masterkeys
   + the registry + the per-client verifier reports (~60 KB total). No agent
   ever holds two clients' documents. The largest context anywhere in the plan
   is one client's full set (~50–150 KB of text), held by that client's own
   reviewer.

A fourth rule serves both context and safety: **corpus quarantine.** Only the
Phase 1 style agent (and the scripted blocklist builder) touch `lab/` raw.
Every agent that writes synthetic content works from distilled artefacts
(STYLE-SPEC, templates, masterkeys, voice cards). This keeps generation
contexts small *and* makes leakage of real client facts structurally unlikely
rather than merely checked-for.

---

## 1. PHASE 0 — TOOLCHAIN SPIKE (already executed, 2026-08-21)

Riskiest unknown first: can we produce a firm-grade packet locally? Yes.
Everything below was run and verified in this session.

| step | tool | result |
|---|---|---|
| fetch blank N-400 | `curl https://www.uscis.gov/sites/default/files/document/forms/n-400.pdf` | 200, 776 KB, edition 04/01/24, 14 pp — same edition as zhu's filed form |
| form anatomy | pypdf | 488 AcroForm fields under `form1[0]` (XFA hybrid). zhu's filed copy has XFA already stripped — precedent for our exact approach |
| fill | pypdf `update_page_form_field_values` + delete `/XFA` + `NeedAppearances` | text fields, comb fields (A-number) and checkboxes all persist; values read back correctly |
| extract | pdftotext on filled form | filled values extract (comb digits extract space-separated) |
| firm docs | python-docx + `soffice --headless --convert-to pdf` | real **Times New Roman** is installed (`~/.local/share/fonts/msttcore/`) and embeds as TimesNewRomanPSMT |
| merge | pypdf `PdfWriter.append` | clean 15-pp merge, fields intact, no errors. **`pdfunite` corrupts the AcroForm ("Can't get Fields array") — do not use it** |
| flatten | `gs -o out.pdf -sDEVICE=pdfwrite -dPreserveAnnots=false` | 0 fields remain, text still extractable, checkbox ink verified present by pixel-check of the widget /Rect. Matches the firm's real merged packet (zhu: 64 pp, 0 fields) |
| tax return | `curl https://www.irs.gov/pub/irs-pdf/f1040.pdf` | 200, fillable — same fill pipeline |
| signatures | fc-list | Z003 (Zapf Chancery clone) installed for cursive signature rendering |
| photo fabrication | PIL installed | perspective/noise/wood-texture compositing is standard PIL; prototyped in Phase 3 |

Not installed, and not needed: pdftk, qpdf, PyMuPDF, fillpdf, weasyprint.
Available and used: python3, pypdf, reportlab, PIL, fpdf, openpyxl,
python-docx, soffice, pdftotext, pdftoppm, gs, mutool, ImageMagick.

**Network fetches required (both verified live): the blank N-400 from
uscis.gov and the blank 1040 from irs.gov.** Fetch once in Phase 1, commit the
blanks into the tools tree so the build is reproducible offline.

Two small leftovers, both non-blocking, both land in Phase 3: (a) the 04/01/24
edition renumbered its parts — the complete field dump (488 names) drives the
field map, including the travel-table row count that sets the addendum
threshold; (b) one visual pass over every filled page at pdftoppm resolution.

---

## 2. PHASE 1 — STYLE FREEZE

*Consumes:* FILE-MAP §2 and §7, the actual packet files in
`jacobs_brent/Packet/` and `zhu_vivian/.../Tab A|Tab B/`, the exhibit-rule
corrections in `reports/ossola_ylenia--exhibit-origin.md`, the challenge
article's own promises.
*Produces:* `lab/synthetic/spec/STYLE-SPEC.md`, docx/YAML templates,
`lab/synthetic/tools/` skeleton, the corpus blocklist.

*Topology:* **one agent**, corpus-exposed (the only content-side agent that
ever reads `lab/` raw). Style is a design act — FILE-MAP says so explicitly —
and parallelizing a design act produces incoherence. Standing instruction for
this agent, per the FILE-MAP §7 tooling correction: 54 of 185 corpus PDFs are
image-only (jacobs' filed N-400 among them) and their sidecars are stubs —
read scanned pages visually, and treat proper nouns lifted from scans as
unreliable. Plus one scripted job: build `blocklist.txt` (every proper noun,
number-string, address token from all corpus sidecars, with the §7 caveat
that scan-derived nouns get added in every OCR variant the reports recorded)
for Phase 6's leakage scan.

The proposed resolution of the jacobs/zhu mix (the agent confirms details
against the raw files; the user signs off on taste):

- **Structure: zhu.** TAB A (Summary) / TAB B (Biographical Information),
  applicant cover page with Classification Basis, DOCUMENT n dividers,
  everything merged into one flattened PDF. The challenge prompt promises
  cover pages, tabs and a merged PDF — that is zhu, and only zhu.
- **Wording: the shared modern core.** "TABLE OF CONTENTS" (both 2024 and
  2025 use it; "INDEX OF DOCUMENTS" died with the 2022 generation).
- **Cover letter: the recovered template** in FILE-MAP §2, jacobs-style Re:
  block with DOB line, eligibility clause + citation per basis
  (319 spousal: 8 U.S.C. § 1430(a), 8 C.F.R. § 319.1; 316: INA § 316(a),
  8 C.F.R. § 316.2), the fixed photocopies paragraph.
- **No G-1450, no G-1145.** The challenge article says the N-400 comes first
  among the documents; the izaguirre/ossola-generation openers (G-1145,
  G-1450 before the N-400) contradict that, and zhu's own TOC promised a
  G-1450 the packet did not contain. Fee travels as "the accompanying filing
  fee" in the cover letter ($760, current).
- **Packet order (fixed):** TAB A: 1 TOC, 2 Cover letter. TAB B: 3 N-400,
  4 passport bio page, 5 green card, 6 latest tax return, then conditional:
  7+ spousal passport bio / I-751 receipt / marriage evidence / travel
  addendum / court records. Continuous DOCUMENT numbering across tabs.
- **The exhibit rule, extended by the ossola correction.** FILE-MAP's
  `exhibits = f(basis, moral answers)` gains two arguments:
  `f(basis, moral answers, immigration history, supplied evidence)`.
  Conditional-resident history with the unconditional card not yet in hand
  drags in the I-751 receipt notice (I-797C) — ossola's new rule. A spousal
  basis binds in whatever bona fide marriage evidence the client actually
  supplied (joint deed, joint auto policy, child's passport, joint return) —
  the firm over-documents, and *which* documents appear is a function of what
  arrived, which is exactly the classification behaviour the plugin should be
  forced to exercise. STYLE-SPEC states the rule table; the Phase 5 verifier
  recomputes it per client.
- **Consciously rejected, with reasons recorded in STYLE-SPEC:** the ossola
  cover-letter variant (`Basis:` line replacing DOB/COB, no citation), the
  "Permanent Resident Since:" index header, the izaguirre "INDEX OF
  DOCUMENTS" heading — all pre-zhu generations the NOTES decision already
  excludes as format sources. Also rejected: the **supplemental cover letter**
  (ossola's mid-flight filing against a live case number). It is a real and
  interesting document type, but it is not a function of the input folder —
  it answers a later USCIS event — and the challenge command is
  `naturalize <input-folder>` producing one packet. It cannot be taught by
  input/output pairs and would only blur what an output folder is. If a
  future challenge level wants case-lifecycle work, it starts there.
- **Born-digital outputs only** (decision and reasons in §0.1): no simulated
  print-and-scan artefacts anywhere in an output folder.
- **Typography:** Times New Roman 12 throughout the firm-authored pages.
  Templates use plain paragraphs only — the corpus letterheads lived in docx
  text boxes and that is exactly what converters lose (jacobs' own signature
  block never extracted). Self-inflicted lesson: no text boxes.
- **Deliverable per output folder:** loose numbered components (docx + pdf,
  zhu's `A-1`, `B-4` prefix convention) *and* the flattened merged
  `N-400 Packet.pdf`. Teaches both layers.
- **The firm itself is invented.** SYMPLE, Marcel Oliveira, 26 Broadway and
  31 Hudson Yards are real reference facts and go on the blocklist. The
  registry (Phase 2) invents firm name, preparer name, letterhead address.
- **Lockbox:** needs a fact check the corpus cannot supply — current N-400
  paper-filing addresses by state (web lookup in this phase). Preference:
  choose the six states of residence so one lockbox serves all six clients.
  Fallback if the real mapping will not allow it: vary the lockbox *within
  the worked examples* so fact-dependence is learnable, never sprung on a
  test client first.
- **Timeline:** all six matters run Nov 2025 – Jul 2026 (in-world today is
  Aug 2026), so one form edition, one fee, one style generation — supporting
  the challenge's "the output does not look different" claim, which the real
  decade-spanning corpus cannot.

Barrier: user reviews STYLE-SPEC.md (taste sign-off) before anything renders.

---

## 3. PHASE 2 — CASTING: REGISTRY AND SIX MASTERKEYS

*Consumes:* this plan §7 (the profiles), STYLE-SPEC, the masterkey schema.
*Produces:* `lab/synthetic/registry.yaml`, six
`lab/synthetic/clients/<name>/masterkey.yaml`, six voice cards.

*Topology:*
1. **One casting agent** writes `registry.yaml` — the set-level namespace:
   firm identity; six names, A-numbers, DOBs, addresses, employers, phone
   numbers, emails; the coverage matrix (basis x mess x modality x voice);
   and six half-page briefs. Set-level design is single-brain work — coverage
   and collision-avoidance cannot be sharded. It also distils the six voice
   cards (verbatim register descriptions and *rewritten* sample lines — no
   corpus quotes cross the quarantine; the five documented registers in the
   reports are described, then re-voiced with invented content).
2. **Fan-out: six masterkey agents in parallel**, one per client. Context:
   its brief + the schema + STYLE-SPEC's "facts the output consumes" list.
   Output: one complete masterkey. No masterkey agent sees another client or
   the corpus.
3. **Barrier:** (a) scripted validation — schema check, registry collision
   check, derivation check (continuous-residence dates recompute from LPR
   date; **filing date falls inside the statutory window**, LPR + 3y − 90d
   for 319(a) and LPR + 5y − 90d for 316(a) — the real corpus cut this to
   2y9m on its face (ossola) and the synthetic set must not inherit that
   tension; MRZ check digits recompute; every output-consumed fact has at
   least one input surface; every mess event resolves); (b) **one reviewer
   agent reads all six masterkeys together** (~50 KB — this is the
   cross-client review, done on the compressed representation, never on
   documents) for coverage, accidental sameness, and plausibility.

### The masterkey schema — 9-sprint lineage, ossola-benchmarked

Kept from the 9-sprint prior art (read pre-resync; see header note): the
one-file-per-client single source of truth; explicit `consistency_locks` with
named verification modes; per-fact provenance; the grep-able checklist
discipline. Rejected: the sentinel tokens
(`UNKNOWN`/`DNK`/`LIVE_VERIFY`/`CONDITIONAL_OMIT`) — they encode ignorance
about a live client, and we are the ground truth; a synthetic masterkey with
an UNKNOWN in it is simply unfinished. Also rejected: page-group organisation
mirroring the form — the masterkey is organised by *fact domain*, and the
N-400 field map (Phase 3) owns the projection onto the form.

**The completeness benchmark is `reports/ossola_ylenia--n400-provenance.md`**
— the correction pass produced a full field-level worked example of one
packet (every Part, every value, every source, locks verified). The schema
below must be able to express that entire fact set; the schema review in the
Phase 2 barrier includes a dry-run check that it can. It is also the reason
the schema carries fields the first draft of this plan lacked: SSN,
ethnicity/race, parents' citizenship and marriage-before-18, child
relationship type, spouse's employer, and the conditional-resident block.

```yaml
client: <slug>            # also names the shipped folder
ships_as: examples|to-do  # worked pair or test input
identity: {family_name, given_name, middle_name, dob, sex, cob, coc,
           height, weight, eye_color, hair_color, ethnicity, race, ssn,
           name_change: ...}
immigration: {a_number, lpr_date, class_of_admission, basis: 316a|319a,
              conditional_resident: {was_cr: bool,                 # ossola rule
                i751: {receipt_number, received, approved|pending}},
              derived: {early_filing_date, residence_years}}   # recomputed by script
family: {marital_status,
         spouse: {name, dob, usc: bool, usc_since: birth|naturalized, employer},
         children: [{name, dob, pob, relationship, address}],
         parents: [{name, usc: bool, married_before_applicant_18: bool}]}
addresses: [{street, city, state, zip, from, to}]              # gap-free
employment: [{employer, city, state, title, from, to}]
travel: [{depart, return, countries, days, on_form: true/false, why_excluded}]
moral_character: {q_<n>: {answer, explanation}}                # full Part 9+ set
documents: {passport: {number, issue, expiry, mrz: [l1, l2]}, green_card: {...},
            tax_return: {year, agi, filing_status},
            evidence: [{type: deed|auto_policy|child_passport|..., facts...}],
            resume: {...}}
matter: {engagement_date, filed_date, lockbox, carrier, fee}
exhibits: [{doc, trigger}]  # derived; script recomputes from the four-argument
                            # rule: basis, moral answers, immigration history,
                            # supplied evidence
input_surfaces:                           # THE input-coverage ledger
  identity.dob: [passport_scan, questionnaire]
  addresses.1:  [email:0004]              # supplied late, by prose
  ...
mess_events:
  - {type: superseded, fact: addresses.0, wrong_surface: questionnaire,
     right_surface: email:0006, resolution: chronological}
consistency_locks: [...standard set from FILE-MAP §3, inherited...]
```

The build rule the schema enforces: **every fact any output artefact consumes
must have at least one unambiguous input surface** — and this bites hardest
for the three input-only clients, whose packets must be *buildable* by the
challenge-taker or the challenge is broken.

---

## 4. PHASE 3 — OUTPUT RENDERING (scripted; outputs before inputs)

*Consumes:* six masterkeys, STYLE-SPEC, templates, the committed blank forms.
*Produces:* rendered output folders for **all six** clients (three ship as
worked examples; three are kept back as answer keys), plus
`render-manifest.json` per client (file list, hashes, field-fill dump).

Outputs render before inputs because rendering is the cheap, deterministic
validator of masterkey completeness: a renderer that hits a missing fact fails
loudly, and the masterkey is fixed before any expensive creative work happens.

*Topology:*
1. **One toolsmith agent** builds the renderers in `lab/synthetic/tools/`:
   - `fieldmap_n400.yaml` — masterkey path -> PDF field name, built from the
     488-field dump; the one genuinely fiddly artefact. Verified by
     round-trip: fill from a masterkey, extract, diff (scripted), plus a
     page-by-page pdftoppm visual pass (agent eyeballs images once).
   - `render_n400.py` (fill, strip XFA, signature via Z003 where wanted),
     `render_docs.py` (TOC/cover letter/cover pages/resume via python-docx ->
     soffice), `render_1040.py`, `render_court_records.py` (reportlab),
     `render_evidence.py` (reportlab: joint deed with recorder stamp, auto
     policy declarations page, I-797C receipt notice — the ossola-corrected
     exhibit types), `render_addendum.py` (openpyxl, izaguirre-shape),
     `merge_packet.py` (pypdf append in TOC order, gs flatten),
     `verify_client.py` and `verify_set.py` (Phase 5's engines, written now,
     run always). The card/passport fabricator covers spouse and child
     passports as well as the applicant's.
2. **One render-runner agent** drives all six renders. One agent suffices —
   its context is scripts and logs, not documents; the complexity lives in
   the tools.
3. **Barrier:** `verify_client.py` green on all six, then **three QA agents
   in parallel** (one per *worked* client) review the rendered pages as
   images against STYLE-SPEC. Answer-key packets for the test three get the
   scripted check only.

---

## 5. PHASE 4 — INPUT FABRICATION (the creative pass)

*Consumes:* per client: masterkey, voice card, modality brief, the input-shape
spec (email-dir convention `NNNNNN_YYYY-MM-DD_slug/` with body .txt +
attachments, per the corpus export shape).
*Produces:* six input folders; `input_surfaces` and `mess_events` ledgers
updated to match what was actually written.

*Topology:* **six agents in parallel**, one per client, corpus-quarantined.
Each writes the email threads (voice card governs register), the filled
questionnaire (docx or xlsx per the client's modality), and drives the shared
fabricators for document images: green card and passport composites (PIL:
card layout -> wood-grain/desk background, slight rotation, shadow, JPEG
noise; MRZ generated with correct check digits — a scripted consistency lock
in its own right), tax return (filled 1040 pp.1-2), resume.

**5.3 The bounded mess catalogue.** Only these mess types exist, each renders
from the masterkey (decoys included — an over-delivered spouse tax return
still agrees with the masterkey), and each appears in a worked pair before any
test input:

| mess type | demonstrated in | reused in |
|---|---|---|
| folder named for the correspondent, not the applicant | W2 | T1 |
| blank questionnaire field, supplied later by email prose | W3 | T3 |
| superseded fact (later email wins) | W2 | T2 |
| day trip in travel list, excluded per firm instruction | W1 | T2 |
| phone-photo documents | W1 | T3 |
| password-protected attachment, password in a later email | — worked-pair W3 carries it benignly (password in same thread) | T3 |
| over-delivery of unrequested documents | W1 | T2 |
| same client, multiple email addresses | W2 | T3 |
| unrelated-matter noise in the mailbox (a relative's visa question, an LLC aside — the corpus's "matter folders accumulate unrelated material", ossola/malone/izaguirre all show it) | W1 | T2 |

*Barrier:* scripted input-coverage check runs on the **extracted text of the
actually-produced inputs** (not on the agents' claims): every consumed fact
found on at least one surface; every superseded pair present with the right
chronology; questionnaire text matches the masterkey where it is meant to and
mismatches exactly where a mess event says so.

---

## 6. PHASE 5 — VERIFICATION (four layers, cheapest first)

1. **Scripted intra-client locks** (`verify_client.py`, all six): re-extract
   from rendered artefacts and diff against the masterkey. N-400 field values
   (pypdf read of the unflattened component), TOC lines vs actual packet
   contents vs cover-page numbers, cover-letter facts, dates, A-numbers, MRZ
   checksums, exhibit set recomputed from the four-argument rule (basis,
   moral answers, immigration history, supplied evidence), filing-window
   arithmetic, merged-PDF page count == sum of components, merged text
   contains each component's fingerprint lines. Zero tolerance: any diff is a
   build bug.
2. **Per-client agent review, six in parallel.** Each holds ONE client's full
   set — extracted text of inputs and outputs plus the page images it asks
   for (~50–150 KB; comfortably one context). Hunts what locks cannot encode:
   timeline plausibility, narrative coherence between the emails and the
   form, voice consistency, whether the packet tells one story. Output: a
   discrepancy list referencing masterkey paths.
3. **Scripted set-level scans** (`verify_set.py`): leakage — every synthetic
   proper noun and digit-string grepped against the Phase 1 corpus blocklist,
   both directions, zero hits allowed; registry collisions; coverage matrix
   (both bases present, all three conditional exhibits exercised, six
   distinct voices, mess catalogue fully demonstrated-before-tested). Then
   **one set-reviewer agent** reads six masterkeys + registry + the six
   layer-2 reports — never a document — for the judgment call: does the set
   feel like six different clients of one firm.
4. **The dogfood test — the acceptance gate for the whole spike.** A clean
   solver context per test client: given only what a challenge-taker gets
   (the challenge article + three shipped worked pairs + that one test
   input), build the packet. Scripted fact-level diff of the solver's packet
   against the answer key. Pass bar: facts correct, structure correct,
   conditional exhibits correctly chosen; formatting is graded by eye, not
   byte. A solver failure caused by ambiguity is a **data bug** — fix the
   input surfaces, not the solver. Run for all three test clients; T2 first
   (the intended-median difficulty).

---

## 7. THE SIX CLIENT PROFILES

Chosen so that the four-argument exhibit rule —
`exhibits = f(basis, moral answers, immigration history, supplied evidence)` —
is learnable from the worked three and properly exercised by the test three;
no test client's exhibit set equals any worked example's, so copying fails
and rule-learning succeeds. All facts below are placeholders for the registry
to finalise — applicant nationalities deliberately disjoint from the corpus
five (Australia, China, Mexico, Philippines, Italy are blocklisted for
*applicants*).

| | ships | basis | conditional exhibits | input modality | voice register | mess carried |
|---|---|---|---|---|---|---|
| **W1** "Almeida" | pair | 316(a) five-year | travel addendum | questionnaire docx returned filled + phone photos of GC/passport + 1040 + resume | terse professional (zhu-register), Brazilian engineer | day-trip exclusion; over-delivery; phone photos; unrelated-matter aside |
| **W2** "Kavanagh" | pair | 319(a) spousal, **conditional-resident history, I-751 approved late** | spouse passport bio + **I-751 receipt (I-797C)** + joint auto policy (supplied evidence) | **email prose only** — facts narrated across a thread, no questionnaire; photo of the I-797C among the attachments | warm, chatty, apologetic couple (jacobs-register), Irish applicant, USC husband corresponds | folder named for husband; superseded address; two email addresses |
| **W3** "Nowak" | pair | 316(a) | court records + written explanation | xlsx questionnaire + scans | fluent non-native, comma-splices (izaguirre-register), Polish designer | blank hard fields supplied later by email; benign password handoff |
| **T1** "Tran" | input only | 319(a) spousal + name change | spouse passport bio + travel addendum + **joint deed + child's passport** (supplied evidence) | delegated correspondence — USC husband writes, applicant surfaces rarely | deferential, technically blocked applicant + verbose solution-oriented relative (malone-register), Vietnamese applicant | correspondent-named folder; e-signature friction |
| **T2** "Stavros" | input only | 316(a) | travel addendum | tidy table export + full document set | warm over-deliverer, self-doubting (ossola-register), Greek-American | superseded fact; day trip to exclude; unrequested extras; unrelated-matter noise |
| **T3** "Adeyemi" | input only | 316(a) + dismissed arrest | court records + travel addendum | the stress test: phone photos only, password-protected 1040 (password two emails later), blanks filled by prose | **sixth register, new**: blunt, precise, minimal courtesy, Nigerian engineer | password chase; blanks-then-prose; multiple addresses; phone photos |

Difficulty ramps T1 -> T3. T2 is the median and the first dogfood target.
Every conditional-exhibit *rule* a test client needs is demonstrated by a
worked pair: W2 demonstrates the spousal cluster (spouse passport, I-797C,
supplied marriage evidence), so T1's deed and child's passport are a novel
*combination* of the demonstrated supplied-evidence rule, not a new rule;
likewise T3's arrest+addendum. That generalisation gap is exactly what is
worth testing. One divergence from corpus reality is deliberate and stated:
real matters show identity documents "appearing from nowhere" (jacobs 0%
traceability, ossola 8%), but every synthetic input folder fully accounts for
its packet — the challenge defines the input folder as everything the client
gave, and a packet that cannot be built from its input is a broken test, not
a realistic one.

---

## 8. LAYOUT AND LANDING

### Working tree (never ships)
```
lab/synthetic/
  spec/STYLE-SPEC.md          templates/ blanks/ (n-400.pdf, f1040.pdf)
  tools/                      registry.yaml  blocklist.txt
  clients/<slug>/masterkey.yaml  render-manifest.json  voice-card.md
  answer-keys/tran/ stavros/ adeyemi/        # rendered, unshipped
  reports/                    # verifier + dogfood output
```

### Shipped (Phase 6 copies it into the course)
```
content/21-challenges/materials/challenge-one/
  examples/
    almeida_paulo/   {input/, output/}
    kavanagh_liam/   {input/, output/}      # correspondent-named: applicant is his wife
    nowak_agata/     {input/, output/}
  to-do/
    tran_michael/    {input files}          # correspondent-named: applicant is his wife
    stavros_daphne/  {input files}
    adeyemi_tunde/   {input files}
```
`content/images/` establishes the precedent for non-article assets under
`content/`; the article gains one line pointing at `materials/challenge-one/`.
Size budget: **under 25 MB total** (merged packets ~1–2 MB, photos ~300 KB at
modest resolution) so it ships inside the GitHub ZIP with no DVC involvement.

### Shipping safety — flagged, must be closed in Phase 6
- `install.sh` strips `go/ bin/ devlog/ jobs/ packaging/ .github/` — **it has
  no rule for `lab/`**, which holds real client data. Phase 6 adds
  `rm -rf "$TUTOR_HOME/lab"` as defence in depth, and the user confirms
  `lab/` is excluded from what a reader can receive in the first place.
- Rebuild `content/index.json` (`tutor index`) and confirm the materials tree
  does not surface as articles (the index is an explicit list, so the risk is
  the rebuild glob, not the reader).
- Final leakage scan (Phase 5 layer 3) runs once more on the shipped tree
  as-landed.

---

## 9. TOPOLOGY SUMMARY

| phase | agents | corpus? | each holds | emits | barrier to next |
|---|---|---|---|---|---|
| 1 style freeze | 1 | YES (only content-side exposure) | FILE-MAP + jacobs/zhu packet files | STYLE-SPEC, templates, blocklist | user signs off style |
| 2a casting | 1 | no | plan §7 + STYLE-SPEC | registry, 6 briefs, 6 voice cards | registry validates |
| 2b masterkeys | 6 parallel | no | own brief + schema + fact-requirements | masterkey.yaml | scripted checks + 1 reviewer over all six keys |
| 3 tooling+render | 1 toolsmith, then 1 runner, then 3 QA parallel | no | scripts, logs, page images | tools, 6 output folders, manifests | verify_client green x6, QA pass x3 |
| 4 inputs | 6 parallel | no | own masterkey + voice card + modality brief | input folders, updated ledgers | scripted input-coverage on extracted text |
| 5 verify | scripts; 6 parallel reviewers; scripts; 1 set-reviewer; 3 solvers | no | one client's set / compressed set / taker's view | discrepancy lists, dogfood diffs | all green; ambiguities fixed and re-dogfooded |
| 6 landing | 1 | no | shipped tree + install.sh + index | landed materials | final leakage scan green |

Peak parallel width: 6. No context anywhere exceeds one client's document set.
Cross-client work happens only on masterkeys, the registry, and reports.

---

## 10. RISKS, UNCERTAINTIES, CUT ORDER

**Risks, ranked:**
1. *Unsolvable ambiguity from seeded mess.* Mitigated by the bounded
   catalogue, the demonstrated-before-tested rule, chronological precedence
   throughout, and the dogfood gate — the one test that measures the actual
   property the spike exists to deliver.
2. *Leakage of real client material.* Mitigated structurally (corpus
   quarantine: one exposed agent) and by the two-direction scripted blocklist
   scan; `lab/` added to install.sh strips.
3. *Field-map errors across 488 N-400 fields.* Mitigated by scripted
   round-trip (fill -> extract -> diff) and a one-time visual page pass. The
   04/01/24 edition's renumbered parts are an open detail — resolved by the
   field dump, Phase 3, before anything depends on it.
4. *Docx render fidelity.* Mitigated by the no-text-boxes template rule
   (the corpus's own converters proved the failure mode) and QA-on-images.
5. *Lockbox fact-check.* Real current N-400 paper-filing addresses need a
   web lookup (Phase 1). Fallback defined (§2).
6. *Document-image plausibility.* Phone-photo compositing might look toy.
   Acceptable floor: clean flat scans — the corpus contains both.

**Cut order if the spike runs short** (cut top-down):
1. Photo-realistic styling -> clean flat scans (keeps facts and modality).
2. The marriage-evidence cluster -> spousal clients carry spouse passport +
   I-797C only (drops the deed and policy renderers and two fabricated
   document types; the basis-driven exhibit rule stays learnable).
3. Dogfood three test clients -> dogfood T2 only.
4. The sixth voice register -> reuse a documented register, new nationality.
5. Email-thread depth (8–10 messages -> minimum 3 that carry the surfaces).
6. Answer-key rendering for T1/T3 (keep T2's for the dogfood diff).

**Never cut:** the masterkeys, the scripted lock verification, the leakage
scan, one dogfood run, the install.sh strip rule. Without any of those the
deliverable is either untrusted or unsafe to ship.

**Open questions for the user:**
- Sign-off on the §2 style resolutions, chiefly: no G-1450, zhu structure,
  loose components + merged PDF both shipped.
- The invented firm identity (name, preparer, letterhead city) — registry
  will propose; taste call.
- Confirmation that `lab/` cannot reach a reader through any channel other
  than the ones install.sh touches.
- Whether the challenge article should gain the one-line pointer to
  `materials/challenge-one/` in this spike or a follow-up.

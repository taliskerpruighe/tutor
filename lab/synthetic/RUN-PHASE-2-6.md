Execute `lab/BUILD-PLAN.md` phases 2 through 6, in order, without stopping for user input.

AUTHORITY, in this order of precedence:
1. `lab/synthetic/spec/STYLE-SPEC.md` **section 16** — the user's binding rulings. These override everything, including §14 of the same file and BUILD-PLAN §2. Read §16 FIRST and treat every "OVERTURNED" row as law.
2. The rest of STYLE-SPEC.md — the frozen house style.
3. `lab/BUILD-PLAN.md` — phase topology, masterkey schema, client profiles, verification layers.
4. `lab/FILE-MAP.md` and `lab/reports/` — rules and provenance only.

HARD CONSTRAINTS
- **Corpus quarantine.** No agent you spawn may read `lab/<client>/` — that means jacobs_brent, zhu_vivian, izaguirre_jesus, malone_kyle, ossola_ylenia. Phase 1 already consumed the corpus; STYLE-SPEC replaces it. Reading `lab/reports/*.md` is permitted.
- **No firm identity anywhere** (§16 ruling 7). No firm name, preparer name, business address, firm phone or email — not on the cover letter, not in the signature block, not on the N-400, nowhere.
- **N-400 Part 13 stays empty and the form ships unsigned** (§16 rulings 10, 11). Part 11 — the applicant's own phone and email — IS filled. Phase 5 must assert Part 13 and the signature fields are empty; a filled one is a build bug.
- **Do not run `pdfunite`** — it corrupts the AcroForm. Merge with pypdf, flatten with gs.
- **Do not run OCR.** Do not invoke tesseract or ocrmypdf. If `build_blocklist.py` has an OCR path, disable it before running.
- **No git commands, ever.** Do not mention version control state.
- Do not modify anything under `lab/` outside `lab/synthetic/` and `lab/reports/`.

DECISIONS YOU MUST MAKE WITHOUT ASKING
- Phase 2 casting must break the T2 Stavros / W1 Almeida exhibit duplicate recorded in STYLE-SPEC §13 D13 and §16. Give T2 a differentiator. Record what you chose and why in `registry.yaml`.
- The spousal-cluster divider titles (§4.3) are invented and unreviewed. §16 ruling 4 set the precedent: the user preferred the formal name over the colloquial one. Follow it.
- Firm-authored documents ship as docx + pdf; forms and exhibits ship as pdf only.
- Any other ambiguity: choose, and record the choice in the phase's output.

MODEL TIERS — pin these, do not inherit defaults
- Phase 2 casting agent, Phase 3 toolsmith, Phase 5 set-reviewer: opus.
- Phase 2 masterkey writers, Phase 4 input fabricators, Phase 5 per-client reviewers, Phase 5 solvers: sonnet.
- Phase 3 render-runner, Phase 3 QA, Phase 6 landing: sonnet.

STOP CONDITIONS — halt and report rather than push through
- The dogfood gate (BUILD-PLAN §6 layer 4) fails twice on the same client after a data fix.
- The leakage scan returns any hit.
- A phase barrier cannot be made green.

Work the cut order in BUILD-PLAN §10 if you run long. Never cut the masterkeys, the scripted lock verification, the leakage scan, one dogfood run, or the install.sh strip rule.

Report at the end: what landed where, which barriers went green, every decision you made unasked, and anything you cut.

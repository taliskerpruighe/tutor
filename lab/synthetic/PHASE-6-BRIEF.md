# PHASE 6 — LANDING. Requirements gathered in advance.

## Verified state of `install.sh` (read 2026-08-22)

It strips, at lines 205–243:
`packaging/` (after copying three files out) · `go/` · `bin/` · `devlog/` ·
`.github/` · `jobs/` · and individually `content/pipeline.md`, `content/plan.md`,
`content/outline.md`, `content/voice-guide.md`, `content/visual-guide.md`.

**There is no rule for `lab/`.** BUILD-PLAN §8 predicted this and it is
confirmed. `lab/` holds five real client matters. This is the run's single
highest-consequence shipping defect and BUILD-PLAN §10 puts the fix on the
never-cut list.

### What Phase 6 must add
`rm -rf "$TUTOR_HOME/lab"` in the same strip block, defence in depth. Place it
with the other `rm -rf` lines (the block's own comment notes it is written with
`rm -rf`/`-f` throughout and that no step depends on a previous one, so ordering
is free).

## The shipped tree (BUILD-PLAN §8)

```
content/21-challenges/materials/challenge-one/
  examples/
    almeida_paulo/   {input/, output/}
    kavanagh_liam/   {input/, output/}      # correspondent-named: applicant is his wife
    nowak_agata/     {input/, output/}
  to-do/
    tran_daniel/     {input files}          # NOTE: renamed from tran_michael, registry D2
    stavros_daphne/  {input files}          # correspondent-named: applicant is her father
    adeyemi_tunde/   {input files}
```

**`tran_daniel`, not `tran_michael`.** BUILD-PLAN §8 says `tran_michael`;
Phase 2a renamed it because `Michael` is a whole-token hit on `blocklist.txt`
and a folder name ships. Recorded as registry decision D2.

Answer-key packets for the three `to-do` clients stay in
`lab/synthetic/answer-keys/` and **must not ship**.

## The rest of the Phase 6 checklist
- Size budget: **under 25 MB total** for the shipped materials tree.
- Rebuild `content/index.json` (`tutor index`) and confirm the materials tree
  does **not** surface as articles. The index is an explicit list, so the risk
  is the rebuild glob, not the reader.
- Add one line to `content/21-challenges/01-challenge-one.md` pointing at
  `materials/challenge-one/`.
- Run the final leakage scan (`tools/verify_set.py`) once more **on the shipped
  tree as landed**, not only on `lab/synthetic/`.
- Confirm `lab/` cannot reach a reader by any channel other than the ones
  `install.sh` touches.

## Constraint that survives into Phase 6
Writing outside `lab/` is sanctioned for this phase and only this phase: the
materials tree, `install.sh`, `content/index.json` and the article pointer line
are all outside `lab/` by design. The no-modify rule covers `lab/` only.

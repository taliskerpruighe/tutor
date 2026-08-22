Continue. Everything already established in this session still holds: the
authority order, the hard constraints, the model tiers, the stop conditions and
the decisions-without-asking from the original prompt are unchanged and are NOT
restated here. Do not re-derive them and do not re-do completed work — the six
masterkeys and their normalised copies are done and Phase 2 barrier (a) is green.

Resume at the Phase 2 reviewer and run through Phase 6.

## You are not finished until every one of these is true

1. `lab/synthetic/registry.yaml` records the Phase 2 reviewer's verdict.
2. `lab/synthetic/tools/` holds the working renderers and `verify_client.py` /
   `verify_set.py`.
3. Each of the six clients under `lab/synthetic/clients/<slug>/` has an
   **output** folder containing the merged `N-400 Packet.pdf` plus its
   components, and an **input** folder of fabricated client material.
4. Every scripted lock, the leakage scan and at least one dogfood run have been
   executed and their results written to disk.
5. The Phase 6 landing has been done.

Check that list before you end your turn. If an item is unmet and no stop
condition has fired, you are not done: spawn the next agent.

## The failure that ended the last run

The last invocation reached a green barrier, wrote a progress summary, and
ended its turn. In headless mode ending a turn ends the run — there is no user
here to say "keep going". That cost the run five of its six phases.

So:

- **A green barrier is a checkpoint, not a stopping point.** Passing one means
  proceed immediately to the next agent in the same turn.
- **Write no progress summaries, no status reports, no "next: ..." notes.**
  Narrating what you are about to do next instead of doing it is the exact
  failure above. Put progress in files, not in prose.
- **You write exactly one summary, at the very end**, and only once the list
  above is satisfied or a stop condition has genuinely fired. If you find
  yourself composing a summary before then, stop composing it and spawn the
  next agent instead.
- Every turn you take must end in a tool call unless the work is finished.

Long runs are expected. Do not optimise for finishing your turn.

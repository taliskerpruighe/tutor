---
id: skills/start-with-never
title: Start with never
part: Skills
section: When To Build One
order: 1
summary: Most jobs do not need a skill — try the agents first, and build one only when the same instructions keep coming out of your mouth.
keywords: [skill, when, context rot, default agent, custom agent, subagents, repeating, correcting, proofread]
---

# Start with never

*v0.1.0*

The instinct, when something needs doing, is to build the thing that
does it. Hold that off for one round.

Agents are capable. A great deal of what you will want done, they will
do with no help from you at all, and do it well enough that a skill
would have been ceremony.

A skill is also not free. Every skill on the machine is one more thing
every session has to notice, weigh and carry before it answers
anything at all. You know from *Context rot* where that road goes. A
skill that earns its place pays for the room it takes up. A skill that
does not makes every other answer slightly worse, and never mentions
it.

So the question is not *should I write a skill for this*. It is *have
I tried it without one*.

## The ladder

Take the job — or one piece of the job, which is quicker to test — and
walk up.

**1. Ask the default agent.** Open a session in the matter folder,
describe what you want, point it at the documents. *"Read the bundle
in `disclosure/` and give me a chronology of every dated event."* A
surprising amount of work stops here.

**2. Ask a custom agent.** If the default one wandered, or drafted
when you wanted it to read, hand the job to something built for it — a
`chronologer` on the right model with the right tools, as in *Custom
agents*. Half of what looks like a missing skill is a missing agent.

**3. Send several custom agents at it.** If the job is really three
jobs, say so, and let one agent pass pieces to others: one reads the
bundle, one drafts the chronology, one checks every date against the
pleadings. Splitting the work fixes a great deal that more instruction
would not.

If a rung works, stop there. You do not need a skill, and you have
saved yourself the cost of keeping one.

## When you do need one

You have walked up the ladder and something is still wrong. It will
be one of these five shapes.

- **It does not work.** Not slowly, not roughly — it does not do the
  thing. The job needs knowledge you have not given it and cannot
  reasonably give it again every morning.
- **It does not work consistently.** Monday's chronology is exactly
  right and Thursday's is a mess, and nothing changed but the day.
  Inconsistency is the clearest sign of all, because a skill is
  precisely the machinery for making the same thing happen twice.
- **You keep repeating instructions.** Before it will do the job
  properly you find yourself explaining the same four things — the
  columns, the date format, that undated documents go at the end, that
  you want the source in brackets. Every session. From scratch.
- **You keep correcting it.** It produces something, you send it back,
  it fixes it, and you are pleased. Then you do the identical exchange
  tomorrow. A correction you have made twice is an instruction you
  have not written down.
- **The prompt never changes.** *"Proofread this."* *"Check my
  email."* Word for word, most days, on different documents. A prompt
  you have typed forty times is a skill you wrote forty times and
  saved none of them.

That last one deserves a moment. It is the easiest to spot and the
easiest to ignore, because each individual time it costs you four
seconds. It is also the case where a skill pays best: identical
prompt, identical job, and everything you would have had to add
sitting in the folder already.

---

None of this is a rule about how many skills you should own. It is a
rule about the order you find out. Try, then build — never build,
then try.

Next, what one actually is.

Press `n`.

---
id: subagents/step-two
title: Step two — the workers
part: Subagents
section: Build a Chain
order: 7
summary: Four builds — two agents and two skills — each one a short interview you have already been walked through.
keywords: [exercise, custom-agents, custom-skills, haiku, sonnet, effort, medium, high, bundle-reader, bundle-consolidator]
---

# Step two — the workers

*v0.1.0*

Four builds, in the same session in `~/tutor/bundle`. Two agents and two
skills. Each is an interview you have already been walked through — in
*Building one* for agents, and in *Building your first skill* for skills
— so what follows is a checklist rather than a lesson.

Do them in order. Answer the way it is written here the first time; you
can build your own version of any of it afterwards.

## 1. The reader agent

```
/custom-agents build me an agent
```

- **Name** — `bundle-reader`
- **What it is for** — reads one document and reports every dated event
  in it, quoting the wording it found. **It runs a skill.** It must not
  write anything.
- **Model** — **Haiku**. Search and check.
- **Where** — this project.

Two halves of that answer do real work. "Must not write anything" keeps
`Write` and `Edit` out of the file. "It runs a skill" puts `Skill` in —
and without that this agent cannot load `bundle-read` when the door
fires it, so say it in both interviews.

## 2. The consolidator agent

```
/custom-agents build me another agent
```

- **Name** — `bundle-consolidator`
- **What it is for** — takes lists of dated events and merges them into
  one chronology. **It runs a skill.** It must not go and read the
  documents itself.
- **Model** — **Sonnet**. It does the work.
- **Where** — this project.

## 3. The reading skill

```
/custom-skills build me a skill
```

- **What the job is** — pull every dated event out of one document.
  Every date, exactly as the document words it, with a line saying which
  document and where in it. Nothing summarised, nothing tidied up.
- **What you have in writing** — nothing. Say so.
- **Name** — `bundle-read`
- **Effort** — **medium**. Reading, finding, pulling things out.
- **Where** — this project.

## 4. The consolidating skill

```
/custom-skills build me one more skill
```

- **What the job is** — take several lists of dated events, merge them
  into one chronology in date order, and keep the source line against
  each entry. Anything without a date goes at the end, under a heading
  of its own. Where two lists describe the same event, one entry, both
  sources.
- **What you have in writing** — nothing.
- **Name** — `bundle-consolidate`
- **Effort** — **high**. Everything else.
- **Where** — this project.

## Where the settings landed

Look back at the four and notice how the two decisions divided.

**Model went on the agents. Effort went on the skills.** That is the
rule, and the reason is that an agent may run different skills across
different jobs — so the depth of thinking cannot be pinned in the agent
file, which cannot know which skill it will be handed.

And both varied. Haiku reads, Sonnet merges; `medium` for the finding,
`high` for the judgement. Four workers, four settings, none of them the
default. That is the point of the exercise.

Four files exist now and none of them know about each other. Next, the
one that puts them in order.

Press `n`.

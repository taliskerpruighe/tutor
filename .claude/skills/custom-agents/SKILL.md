---
name: custom-agents
description: Build a custom agent for her — interviewing her for the name, purpose, model and location, then writing the agent definition file and telling her how to launch it. Use whenever she asks to make, build, set up or create an agent, or asks for an agent that does a particular job. Do NOT use it to explain what an agent is, what a field means, or how agents work in general — those are questions the `tutor` skill answers from the course — and do NOT use it to build a skill, which is the `custom-skills` skill.
user-invocable: true
---

# Building a custom agent

She has read *Agents → Custom Agents*, so she knows an agent is one file
with frontmatter and a body. She has not written one. You do the writing;
she makes the four decisions that are hers.

Interview her first, write the file second. Never write a partial
definition and fill it in as you go — a half-written agent in
`agents/` is a real agent, and it will show up in her next session.

## The interview

Ask these in order. One at a time, in plain language, and let her answer
before moving on. Use `AskUserQuestion` where the answer is a choice
between options; ask in prose where the answer is hers to invent.

### 1. Name

Hers to pick. Take what she says and normalise it: lowercase, hyphens for
spaces, no extension. Tell her what you normalised it to. This becomes
both `name:` and the filename.

If a file of that name already exists where it is going, say so and ask
before overwriting.

### 2. What it is for

Ask what the agent should do, and when she would reach for it. Push gently
for what it should **not** do — that answer is what sizes the tool set,
and she has been told to give it.

Turn her answer into a `description` written as a trigger sentence: what
the agent does, when to use it, and an explicit "Do NOT use it to…" clause
where she gave you one. Other agents read this field to decide whether to
call this one, so it is written for them, not for her.

Show her the sentence you wrote and let her correct it.

### 3. Model

Offer the three, framed by the kind of work — this is the rubric from
*Building one*, and she should recognise it:

- **Opus** — analyse and decide. Working out what the argument is,
  reading law and facts, planning a piece of writing.
- **Sonnet** — do the work. Drafting the sections, producing the output.
- **Haiku** — search and check. Citation formats, references to the
  record, quick match-and-report.

If her description makes the answer obvious, recommend one and say why in
a single line. She still chooses.

### 4. Where it lives

Ask whether this agent should be global or belong to one folder:

- **Global** — `~/.claude/agents/<name>.md`. Every session on the machine
  can see it, including sessions where it is irrelevant.
- **This project** — `<folder>/.claude/agents/<name>.md`. Only sessions
  launched from that folder, or below it, can see it.

Name the actual folder she is in when you offer the second option. Say the
consequence in one line — every agent a session can see makes that session
slightly worse at everything, so the right home is the narrowest folder
that still covers every session needing it. Recommend the project unless
the job really is machine-wide.

Create the `.claude/agents/` directory if it does not exist.

## What you set without asking

Three fields are the same on every agent. Set them, mention them in one
line afterwards, do not turn them into questions.

- **`background: true`** — so the agent can be handed a job by another
  agent and work while she carries on.
- **`memory: user`** — so it keeps notes across its own sessions.
- **`Agent` in `tools`** — on every agent, without exception, so it can
  call other agents rather than being able only to do its own work.

## Choosing the tools

Never read her a list of tool names. Pick the smallest set that covers
what she described, starting from the floor:

| Kind of agent | `tools` |
|---|---|
| reads and reports | `Read, Glob, Grep, Agent` |
| also writes | `Read, Glob, Grep, Agent, Write, Edit` |
| also runs commands | add `Bash` |
| runs a skill | add `Skill` |
| searches the web | add `WebSearch, WebFetch` |

If she said the agent must not write, `Write` and `Edit` stay out — that
restriction is the point, and it is not yours to soften.

Tell her the set in prose afterwards: *"It can read and search files, and
call other agents. It cannot write to anything."*

## Writing the file

```markdown
---
name: bundler
description: Reads a disclosure bundle and reports which documents are
  relevant. Use for review and triage of a document set. Do NOT use it to
  draft anything.
model: haiku
tools: Read, Glob, Grep, Agent
background: true
memory: user
---

# Role

You read disclosure bundles and report what is relevant…
```

The body is prose, written from her answer to question 2. Cover the role,
what it must not do, the context it works in, and any skill it should
reach for. Write it in the second person, addressed to the agent.

The body must stand alone. When this agent is called by another agent the
body **replaces** its instructions rather than being added to them, so
anything that only makes sense as a footnote to a normal session will not
survive. Write it as a complete briefing.

## Afterwards

Tell her three things, and stop:

1. Where the file is.
2. The line to run, on its own, ready to copy:

   ```bash
   claude --agent bundler
   ```

3. That it needs a new tab, since this session is already running.

## Hard rules

- **Never invent a frontmatter field.** An unrecognised key is ignored in
  silence — the file loads clean and the setting never applies. Use only
  the six fields above.
- **Never write the file before every question is answered.**
- **Never leave `model` or `tools` out.** Omitted, they inherit
  everything, which is the default agent with extra steps.
- **Never widen a restriction she asked for.**
- Never run `git`, `jj`, `dvc`, or `git-ops`.

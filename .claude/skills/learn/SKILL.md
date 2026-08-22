---
name: learn
description: Teach the course, one section at a time — establishing where the reader has got to, sending them to the reader to read that section, checking it landed, and setting one thing to do with it. Use whenever the user asks to be taught, asks where to start or where to begin, asks what to read next, says they are new or lost or do not know where to begin, or asks for a lesson. Also use when they have just finished a section and want the next one. Do NOT use it to answer a one-off question about how something works or what a term means — that is the `tutor` skill.
effort: high
user-invocable: true
---

# Teaching the course

The reader has a wiki in one terminal tab and you in another. The wiki holds
the words; you do everything else — working out where they are, saying what
to read, finding out whether it landed, and giving them something to do with
it.

**One lesson per invocation.** A lesson is one section of one part. Run it,
finish it, stop. They will type `/learn` again for the next.

Never paste an article at them. They are about to read it, or have just read
it, in a better format than you can produce. You read the articles so you
know what to ask.

## The shape of the course

**Derive it from `content/index.json` every time.** Parts run in the order
they appear in the file. A level is a run of consecutive parts sharing a
`level`; a section is a run of consecutive articles sharing a `section`.

Two rules follow, and they hold whatever the file says:

- **A part with no sections is one lesson** — all of its articles together.
- **The course ends at the last part in the index**, and a level ends where
  the next `level` value begins.

Never write a count, a part list, or "the only part that…" into your answer
or into this file. Which parts exist, how many there are, and which have no
sections all change between releases; the index is the only thing that knows.
Section names repeat across parts — *Building One* is in both
Skills and Workflows, *What They Are* is in Workflows, Hooks and Plugins,
*Using Them* is in Hooks and Plugins. A few new names sit close enough to an
older one to be said the same way by mistake: *Prompts* (Agents) next to
*Command Lines and Prompts* (The CLI), *Plans and Permissions* (Agents) next
to *The plans* (Claude → Claude subscriptions), and *Worktrees* (Version
Control) — both a section and the article that opens it — next to Hooks'
*WorktreeCreate and WorktreeRemove*. **Always carry the part with the
section.** A section name on its own does not identify a lesson.

`content/index.json` is the authority on order, not this table and not the
status line. It is a flat list of parts, each holding a flat list of
articles; a level and a section are both derived, not stored — each is a run
of consecutive entries sharing the same `level` or `section` string. Sections
run in the order their articles appear in it; a part's last section is
followed by the first section of the next part; a level's last part is
followed by the first part of the next level. An article's `id` is stable
across releases even when its `path` is renumbered — quote the `id`, not the
path, when you need to name one precisely.

## 1. Find out where they are

Ask for the bottom line of the reader tab. The part you want looks like this:

```
 Agents 3/11 · Context · Context rot 4/6 · 40%
```

Part, section, article, and how far they have **scrolled down the article
they are on**. The part counts within the level rather than the whole course,
so `3/11` is the third part of its level, of however many that level holds
in the index you just read. That last number says
nothing about whether anything was read — a short article reads `100%` the
moment it opens, because it all fits.

**Reading the line.** They may paste the whole row, which carries key hints
on the right (`←→ levels · [] parts · ⇥ sections` and so on), and how many of
those survive depends on the window width. So do not count separators. Take
the **section** as the piece sitting between `<Part> n/N` and
`<Article title> n/N`, and ignore everything from the percentage rightwards.
In This Wiki there is no section piece at all, because that part has none.

Four cases:

- **A line, partway through a section.** That section is the lesson. Send
  them to finish it from where they are rather than restarting, and say `1`
  goes back to the top of the section if they would rather.
- **A line, on the last article of a section.** The percentage cannot tell
  you whether it was read, so ask — one short question, *"did you finish that
  one?"* If yes, the lesson is the next section. If no, that section is the
  lesson.
- **The reader is closed.** Say to open a new Ghostty tab and type `tutor`,
  then read you the bottom line. If it will not start, `bash
  ~/tutor/install.sh` and then `tutor doctor` are the fix, in that order. If
  they would rather not open it at all, ask which tab is highlighted along
  the **top** — that is the level — which heading is flush left down the
  **left** margin — the part — and which is indented under it — the section.
- **New, or does not know.** The lesson is **This Wiki**, the whole part, and
  the first thing you teach is how to drive the reader.

`~/.local/share/tutor/read.json` lists the ids of every article ticked with
`m`. It is corroboration only, not the primary signal — marking is by hand,
so an article missing from that list is not proof it went unread. The status
line stays what you ask for.

Ask once, in one line. Do not interview them.

## 2. Read the section yourself

Before you say anything about it, read it.

1. `content/index.json` lists every article with its `part`, `section`,
   `title`, `summary`, `keywords` and `path`.
2. Take every article whose `part` **and** `section` both match, in order.
   Matching on `section` alone will pull articles from the wrong part.
3. Read them at their `path`.

They are short. Read them whole — you need the detail to ask a question worth
asking, and a summary will not give you one.

If the index looks stale or an article is missing, run `tutor index` — a
subcommand, which is fine — and look again.

## 3. Frame it

Two or three sentences. What this section is for, and why it sits where it
does. Draw it from what you just read, not from what you already know about
Claude Code — they will read the articles next, and if your framing and the
course disagree they have no way to tell which is right.

Then name the Party Trick if the section carries one. There are six across
the course and they are the reason it exists:

| # | Where it lives |
|---|---|
| 1 | Claude Code Setup — content isolation |
| 2 | Agents → Context — the three resets |
| 3 | Agents → Custom Agents — agent engineering |
| 4 | Skills → Building One — skill engineering |
| 5 | Skills → Making Them Fire — always invoke manually |
| 6 | Subagents → Chains — chain engineering |

## 4. Send them to read

Name the part and the section, and give the keys to get there:

- `←` `→` — move between levels
- `[` `]` — move between parts
- `⇥` — move between sections
- `1`–`9` — jump to a numbered article in the section on show
- `n` — the next article, over and over, to read straight through
- `m` — mark the current article as read, again to clear it

Then **stop and wait.** Do not summarise what they are about to read. Do not
carry on to the questions in the same message. They have to go and read it.

## 5. Check it landed

When they come back, ask **two or three questions**. Not more.

Ask about what they would **do**, never for a definition:

- *"You've got forty documents to work through. Which of the three models
  would you put on the reading, and why that one?"*
- *"Where would you put a skill you only ever want when you're working on one
  particular project?"*
- *"You've explained the same four things about how you want a document laid
  out, three mornings running. What does that tell you?"*

If they get one wrong: give the right answer in a line or two, then ask one
more question on the same point. No lecture. If that one goes wrong too, name
the article that covers it, send them back to it, and stop the lesson there —
it can be picked up again with `/learn`.

**Do not move on from a section they could not answer for.** That is the
whole reason this skill exists rather than a list of what to read.

## 6. Set one thing to do

One task. Small enough to finish now. Then stop.

| Part → Section | The task |
|---|---|
| This Wiki *(no sections)* | Drive the reader: `/` and search for a word, jump to an article by number, `⇥` between sections, `m` to tick one off. |
| TUIs → Terminals | Open Ghostty beside the Mac's own Terminal app and name one difference. |
| TUIs → Ghostty | Open a second Ghostty tab and move between them. |
| TUIs → TMUX | Nothing to install — say aloud which of the three uses would apply to a job they already have. |
| The CLI → Command Lines and Prompts | Read their own prompt back to you and say what each piece of it is reporting. |
| The CLI → Shells | Run `echo $SHELL` and say what it answered and why. |
| The CLI → Zsh | `cd` somewhere, `ls` it, and get back home again. |
| Software → Packages | Name one app they use daily and say what it is a wrapper around. |
| Software → Homebrew | Run `brew outdated` and read what it says — no installing. |
| Files → Languages and Scripts | Open one plain-text file on their own machine and say what format it is in. |
| Files → Editors | Open a file in a terminal editor, change one word, save, quit. |
| Linux → The world runs on linux | Name three machines in their own day that are running Linux. |
| Linux → Why its better | Nothing to run — say which of the four claims they would want to test first. |
| Agentic AI → LLMs | Take one job they do weekly and say which of the three axes decides the model for it. |
| Agentic AI → Harnesses | Say what a harness gives a model that the model does not have, in one sentence. |
| Agentic AI → Cloud Computing | Say what would have to be true of a job before renting a machine beat using their own. |
| Claude → Claude | Say which of the four models they would reach for by default, and why not one of the others. |
| Claude → Claude subscriptions | Check which plan they are on. |
| Claude → Claude Code | Name one thing on the list they could not do from the website. |
| Other Models → Running Other Models | Say which of the eight things they would miss most if they pointed the harness away from Claude. |
| Other Models → Ollama | Say what would have to be true of a job before running it on a local model beat sending it to Claude. |
| Other Models → Kimi | Say which of the three effort levels a job of theirs needs, and what it would cost to be wrong. |
| Claude Code Setup *(no sections)* | Look inside `~/tutor/.claude/`, then `~/.claude/`. Say what is in each and why a session in one folder sees both. Party Trick #1. |
| Instructions → The CLAUDE.md File | Write one line for their own `CLAUDE.md` that would have saved them repeating an instruction this week. |
| Agents → Context | Watch the number on screen while working, then `/clear` and watch it drop. Party Trick #2. |
| Agents → Plans and Permissions | Press Shift-Tab in a running session and read which mode it lands on. |
| Agents → Prompts | Write one prompt for something they need done today in the three-part shape: context, objectives, traps. |
| Agents → Custom Agents | Write an agent definition for a job they actually have, save it, then launch it in a new tab. Party Trick #3. |
| Skills → When To Build One | Take a job they repeat and walk the ladder on it, out loud. |
| Skills → Building One | Find two matched sets of their own files — the input and the output — then write the skill that turns one into the other. Party Trick #4. |
| Skills → Making Them Fire | Type `/` and read the list. What can this session see, and why. Party Trick #5. |
| Subagents → Chains | Give the default agent a job with three parts and tell it to split it. Party Trick #6. |
| Subagents → Build a Chain | *One step per lesson* — see below. |
| Workflows → What They Are | Take the chain they built and say what it would gain, and lose, as a workflow. |
| Workflows → Building One | Ask the main agent for a workflow, then push back once on the agent count. |
| Version Control → Git, Github, and Jujutsu | Run `git log --oneline -5` in a folder they already have version-controlled and read back what it says. |
| Version Control → Worktrees | Run `git worktree list` in a repo they already have and say what it shows. |
| Hooks → What They Are | Read the trigger tables and pick the one that fits something they already want. |
| Hooks → Using Them | Pick one worked example and say what it would change about their own setup. |
| Plugins → What They Are | Say which of the four cases matches something they have already built. |
| Plugins → Using Them | Turn something they built into a plugin and install it somewhere else. |
| Headless Sessions → Running Without a Chat | Run one `claude -p` line and pipe a file into it. |
| Counter-Recommendations *(no sections)* | Open your global settings file at `~/.claude/settings.json` and add one of the three `env` switches this part recommends. |
| Challenges *(no sections)* | *Not a lesson* — see below. |

Where the task is to build an agent or a skill, interview them for the
decisions that are theirs — the name, the job, the model or effort level,
and whether it lives globally or in one folder — then write the file
yourself. Never write a partial definition and fill it in later: a
half-written file in `agents/` or `skills/` is a live one. Pick up the
lesson afterwards.

**Build a Chain is five lessons, not one.** Its five articles are five build
steps, each with work at the end of it. Take one per invocation: read the
step, do it, stop. They type `/learn` for the next.

Then say what the next section is, and that `/learn` will start it.

**Challenges are not lessons.** A challenge article is a brief, not
something to read and be questioned on. When the lesson lands on one, read
the article yourself, then walk them through it: what the client wants, what
they have been given, and what "done" looks like. Send them to read the
article, and stop there — the work itself is theirs, across as many sessions
as it takes, and they come back to you with it rather than to `/learn`. Do
not set a task of your own on top of it, and do not question them afterwards.

**When the index has no part left after the one they finished, they are at
the end of the course.** Say so. Point them at *This Wiki → This version*
for what a later version adds, and say that `/tutor` answers anything from
the course in a session rather than on a page.

## How to talk to them

They are new to this. Everything else follows from that.

- Short sentences. No jargon without the plain-English version first.
- Any command they should type goes on its own line, ready to copy.
- Say what will happen before they run something, and what they should see
  afterwards, so they can tell success from failure without asking you.
- Never say a thing is "simple", "easy", or "just" anything.
- When they get something wrong, fix the thing. Do not dwell on the mistake.

## If they ask a question mid-lesson

Answer it, briefly, from the course — then carry on with the lesson where you
left off. A question is not the end of the lesson, and it does not hand over
to another skill.

Find the answer the same way `tutor` does: `content/index.json`, match on
`summary` and `keywords`, read the article at its `path`, answer from it.

If the answer is in an article they have not reached yet — often the very
next one — give the one-line version and say the long one is coming, and
where. Do not pre-empt the article.

## Hard rules

- **Never launch the reader.** `tutor` on its own opens the wiki, and Claude
  Code owns this terminal — it needs a tab of theirs. Say to open one; do not
  try it from a tool call. Subcommands are a different thing and are fine:
  `tutor index` and `tutor doctor` both run happily here.
- **Never run `tutor update`.** It needs no terminal, so nothing will stop
  you, and it replaces the whole of `~/tutor` mid-lesson.
- **Never paste an article at them.** Name it and send them to it.
- **Never run more than one lesson per invocation.**
- **Never move on from a section they could not answer for.**
- **Never match a section by name alone.** Names repeat across parts.
- **Never answer from memory where the course covers it.** The course is the
  agreed version of the truth. If you contradict what they just read, they
  have no way to tell which of you is right.
- **Never edit `content/`.** It is the course, not scratch space.
- Never run `git`, `jj`, `dvc`, or `git-ops`.

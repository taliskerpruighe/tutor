---
name: learn
description: Teach her the course, one section at a time — establishing where she has got to, sending her to the reader to read that section, checking it landed, and setting her one thing to do with it. Use whenever she asks to be taught, asks where to start or where to begin, asks what to read next, says she is new or lost or does not know where to begin, or asks for a lesson. Also use when she has just finished a section and wants the next one. Do NOT use it to answer a one-off question about how something works or what a term means — that is the `tutor` skill — and do NOT use it to build an agent or a skill, which are `custom-agents` and `custom-skills`.
effort: high
user-invocable: true
---

# Teaching the course

She has a wiki in one terminal tab and you in another. The wiki holds the
words; you do everything else — working out where she is, telling her what to
read, finding out whether it landed, and giving her something to do with it.

**One lesson per invocation.** A lesson is one section of one part. Run it,
finish it, stop. She will type `/learn` again when she wants the next.

Never paste an article at her. She is about to read it, or has just read it,
in a better format than you can produce. You read the articles so you know
what to ask.

## 1. Find out where she is

Ask her for the bottom line of her reader tab. The part you want looks like
this:

```
 Agents 1/7 · Context · Context rot 3/4 · 40%
```

Part, section, article, and how far she has **scrolled down the article she
is on**. The part counts within the level she is on rather than the whole
course, so `1/7` means the first of Level 2's seven parts. That last number says nothing about whether she read anything — a
short article reads `100%` the moment it opens, because it all fits.

**Reading the line.** She may paste the whole row, which carries a list of
key hints on the right (`←→ levels · [] parts · ⇥ sections · q quit` and so
on), and how
many of those survive depends on how wide her window is. So do not count
separators. Take the **section** as the piece sitting between `<Part> n/N`
and `<Article title> n/N`, and ignore everything from the percentage
rightwards.

Four cases:

- **She gives you a line, partway through a section.** That section is the
  lesson. Send her to finish it from where she is rather than restarting it,
  and say she can press `1` to go back to the top if she would rather.
- **She gives you a line, on the last article of a section.** The percentage
  cannot tell you whether she read it, so ask — one short question, *"did you
  finish that one?"* If yes, the lesson is the next section. If no, that
  section is the lesson.
- **Her reader is closed.** Tell her to open a new Ghostty tab and type
  `tutor`, then read you the bottom line. If it will not start, `bash
  ~/tutor/install.sh` and then `tutor doctor` are the fix, in that order. If
  she would rather not open it at all, ask which tab is highlighted along the
  **top** — that is the part — and which heading is highlighted down the
  **left**, which is the section.
- **She is new, or says she does not know.** The lesson is
  **Interface → This Wiki**, and the first thing you teach is how to drive
  the reader.

`~/.local/share/tutor/read.json` lists the ids of every article she has
ticked with `m`. It is corroboration only, not the primary signal — she
marks by hand, so an article missing from that list is not proof she has
not read it. The status line stays what you ask for.

**Which section is next.** `content/index.json` is the authority on order,
not the status line. Sections run in the order the articles appear in it, and
a part's last section is followed by the **first section of the next part**.
The parts run Interface, Setup, Agents, Skills, Subagents.

Ask once, in one line. Do not interview her.

## 2. Read the section yourself

Before you say anything about it, read it.

1. `content/index.json` lists every article with its `part`, `section`,
   `title`, `summary`, `keywords` and `path`.
2. Take every article whose `section` matches, in order.
3. Read them at their `path`.

They are short. Read them whole — you need the detail to ask a real question,
and a summary will not give you one.

If the index looks stale or an article is missing, run `tutor index` — a
subcommand, which is fine — and look again.

## 3. Frame it

Two or three sentences. What this section is for, and why it sits where it
does in the course. Draw it from what you just read, not from what you
already know about Claude Code — she will read the articles next, and if your
framing and the course disagree she has no way to tell which is right.

Then name the Party Trick if the section carries one. There are six across
the course and they are the reason it exists.

## 4. Send her to read

Name the part and the section, and give her the keys to get there:

- `←` `→` — move between levels
- `[` `]` — move between parts
- `⇥` — move between sections
- `1`–`9` — jump to a numbered article in the section on show
- `n` — the next article, over and over, to read straight through
- `m` — mark the article she's on as read, again to clear it

Then **stop and wait.** Do not summarise what she is about to read. Do not
carry on to the questions in the same message. She has to go and read it.

## 5. Check it landed

When she comes back, ask **two or three questions**. Not more.

Ask about what she would **do**, never for a definition:

- *"You've got a chronology to build from forty documents. Which of the three
  models would you put on the reading, and why that one?"*
- *"Where would you put a skill you only ever want when you're working on the
  Hartley matter?"*
- *"You've explained the same four things about your chronology format three
  mornings running. What does that tell you?"*

If she gets one wrong: give her the right answer in a line or two, then ask
one more question on the same point. No lecture. If she gets that one wrong
too, name the article that covers it, send her back to it, and stop the
lesson there — she can pick it up again with `/learn`.

**Do not move her on from a section she could not answer for.** That is the
whole reason this skill exists rather than a list of what to read.

## 6. Set her one thing to do

One task. Small enough to finish now. Then stop.

| Section | The task |
|---|---|
| This Wiki | Drive the reader: `/` and search for a word, jump to an article by number, `⇥` between sections. |
| The Terminal | Open a second Ghostty tab and move between them. |
| The Shell | `cd` somewhere, `ls` it, and get back home again. |
| Linux | Look at something real under her own home folder. |
| How It Works | Start a session from a different folder, and see what changes. |
| What It Reads | Look inside `~/tutor/.claude/`, then `~/.claude/`. Say what is in each. |
| Context | Watch the number on screen while she works, then `/clear` and watch it drop. |
| Custom Agents | `/custom-agents` — build one, then launch it in a new tab. |
| When To Build One | Take a job she repeats and walk the ladder on it, out loud. |
| Building One | Find two matched sets of her own files — the input and the output. |
| Making Them Fire | Type `/` and read the list. What can this session see, and why. |
| Chains | Give the default agent a job with three parts and tell it to split it. |
| Build a Chain | *Step one* only — make the folder and get three documents into it. The other four steps are the next four lessons. |

Where the task is `/custom-agents` or `/custom-skills`, say so and let that
skill run its own interview. It knows what to ask. Pick up afterwards.

**Build a Chain is five lessons, not one.** Its five articles are five build
steps, each with real work at the end of it. Take one per invocation: read
the step, do it, stop. She types `/learn` for the next.

Then tell her what the next section is, and that `/learn` will start it.

**When she finishes Build a Chain, the course is done.** Say so. She has all
six Party Tricks and has built an agent, a skill and a chain. Point her at
*About this wiki* for what later versions add, and tell her `/tutor` answers
anything from the course in a session rather than on a page.

## How to talk to her

She is a lawyer, not a developer. Everything else follows from that.

- Short sentences. No jargon without the plain-English version first.
- Any command she should type goes on its own line, ready to copy.
- Say what will happen before she runs something, and what she should see
  afterwards, so she can tell success from failure without asking you.
- Never say a thing is "simple", "easy", or "just" anything.
- When she gets something wrong, fix the thing. Do not dwell on the mistake.

## If she asks a question mid-lesson

Answer it, briefly, from the course — then carry on with the lesson where you
left off. A question is not the end of the lesson, and it does not hand over
to another skill.

Find the answer the same way `tutor` does: `content/index.json`, match on
`summary` and `keywords`, read the article at its `path`, answer from it.

If the answer is in an article she has not reached yet — often the very next
one — give her the one-line version and tell her the long one is coming, and
where. Do not pre-empt the article.

## Hard rules

- **Never launch the reader.** `tutor` on its own opens the wiki, and Claude
  Code owns this terminal — it needs a tab of hers. Tell her to open one; do
  not try it from a tool call. Subcommands are a different thing and are
  fine: `tutor index` and `tutor doctor` both run happily here.
- **Never paste an article at her.** Name it and send her to it.
- **Never run more than one lesson per invocation.**
- **Never move on from a section she could not answer for.**
- **Never answer from memory where the course covers it.** The course is the
  agreed version of the truth. If you contradict what she just read, she has
  no way to tell which of you is right.
- **Never edit `content/`.** It is the course, not scratch space.
- Never run `git`, `jj`, `dvc`, or `git-ops`.

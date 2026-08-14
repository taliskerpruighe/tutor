---
id: prompt/long-prompts
title: Long prompts
level: Level 2
part: Agents
section: Prompts
order: 12
summary: Context, objectives and traps written out in full outgrow the chat box, so there is a keystroke for stepping outside it.
keywords: [long prompt, ctrl-g, editor, settings.json, headings, structure, chat box]
---

# Long prompts

*v0.2.9*

Context, objectives and traps, written out properly, do not always fit
comfortably in a single typed line. A settlement letter with three
prior drafts behind it, a dozen objectives and a longer list of traps
is not a sentence — it is a document, and typing a document into a
one-line box is where prompts start going wrong before the agent has
even read them.

There is a keystroke for that, and a convention for what to do once
you have it.

## Step outside the box

`Ctrl-G` takes whatever you have typed so far and opens it in your
default text editor — a proper window, full height, no wrapping inside
a narrow pane. Shape it there: paragraphs, blank lines, however much
room the prompt actually needs. Save and close, and it lands back in
Claude Code as a single ordinary line, ready to send.

Which editor opens is a setting rather than a fixed choice, and it
lives in your global `settings.json`. *Inside .claude* already
established the habit that applies here too: ask Claude Code to change
the setting for you rather than open the file by hand.

Nothing stops you drafting the whole prompt in the editor first and
sending nothing until you are satisfied with it — reading a long
prompt back before it goes anywhere is exactly the discipline you
would apply to a letter, and a prompt this size deserves the same
pass.

## Give it headings

A long prompt earns the same structure a long document would. Use
`#`, `##` and `###` to separate context from objectives from traps,
the shape *Prompt engineering* laid out:

```
# Context
Third revision of the settlement letter,
client wants firmer tone than draft two.

## Objectives
1. Tighten the without-prejudice heading.
2. Strengthen paragraph 3.

## Traps
Do not alter the figures in paragraph 5.
```

None of this is markdown for its own sake. A heading tells the agent
where one section of the prompt ends and the next begins, which
matters once there is enough text that the boundary would otherwise be
a guess. `###` earns its keep here in a way it never does inside an
article of this course — a prompt is read once and acted on, not
revisited, so a third level of nesting costs nothing.

## Why bother

A three-sentence prompt in the chat box is fine as it is — `Ctrl-G` is
for the other case, the one where context alone runs to a paragraph
and the objectives need their own numbered list. Reach for it the
moment you notice you are scrolling sideways to see what you typed, or
losing track of which trap you already wrote down.

The shape stays the same either way.

Press `n`.

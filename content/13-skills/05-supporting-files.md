---
id: skills/supporting-files
title: Supporting files
level: Level 2
part: Skills
section: When To Build One
order: 5
summary: A skill is a folder, so it can carry templates, checklists and scripts — read only when the instructions point at them.
keywords: [supporting files, assets, references, scripts, templates, checklists, folders, pointer]
---

# Supporting files

*v0.1.0*

An agent definition is one file. A skill is a folder, and that is the
whole difference between them.

Which means a skill can carry things. Your precedent letter. The house
style note. The checklist you run down before anything goes out. They
go in the folder beside the `SKILL.md`, in your own words, rather than
being paraphrased into the instructions and slowly going out of date.

Ask for a skill and you may get up to three of these folders:

```
.claude/skills/letter-before-action/
├── SKILL.md
├── assets/
│   └── lba-template.md
├── references/
│   └── house-style.md
└── scripts/
    └── check-dates.py
```

| Folder | What goes in it | For instance |
|---|---|---|
| `assets/` | things to follow | a letter skeleton |
| `references/` | things to check | your house style |
| `scripts/` | code it runs | text out of a PDF |

**`assets/`** holds templates and examples — the thing the skill fills
in or copies. Your LBA skeleton with the paragraphs in your order. Two
finished letters you were happy with.

**`references/`** holds the double-check material: guidelines,
checklists, definitions, glossaries. The phrases the firm uses and the
ones it does not. The eleven things that must appear in a letter
before action.

**`scripts/`** holds actual code the skill runs, where a step has to
come out identical every time — pulling the text out of a PDF bundle,
formatting a Word document, working a limitation date. Useful, but
narrow: only where sameness is genuinely the requirement.

## Why this beats putting it in the body

The instructions are read every time the skill fires. **These files
are read only when something reaches for them** — and the instructions
say when to reach:

> Before drafting, read `references/house-style.md`.

> If the claim involves a limitation date, run
> `scripts/check-dates.py`.

So the sixty-page style guide costs nothing on the days it is not
wanted. That is the whole reason the folders exist, and it is why
heavy material belongs in one rather than in the body. A pointer with
no condition on it gets read every time, which spends exactly what you
were saving.

## Once again, not by hand

Working out what belongs in which folder is its own course, and the
Boss has packaged that into `custom-skills` too. Ask for a skill, tell
it what you already have in writing and where those documents are, and
it sorts them — the template into `assets/`, the checklist into
`references/`, the pointers into the body with their conditions
attached.

One thing to know now, so it does not surprise you later: **the copy
inside the skill folder becomes the one that counts.** Edit that, not
the original, or the two drift apart and the skill quietly follows the
old version while looking like it is working.

Press `n`.

---
id: subagents/step-one
title: Step one — the project
part: Subagents
section: Build a Chain
order: 6
summary: Make a folder of its own, and ask Claude for three documents to point the chain at.
keywords: [exercise, project, folder, mkdir, location matters, sample documents, bundle]
---

# Step one — the project

*v0.1.0*

Five exercises. By the end of them you will have built a working chain —
two agents, three skills — and run it on documents in front of you. It
produces a chronology: a folder of papers in, a dated list of what
happened out.

You build every part of it by talking to Claude. You will not type a
definition file by hand at any point in this, which is the whole idea.
Everything you need you have already read.

## A folder of its own

Open a terminal and run this:

```bash
mkdir ~/tutor/bundle && cd ~/tutor/bundle && claude
```

Three things on one line: make the folder, move into it, start a session
there.

Where the folder sits is not an accident, and *Location matters* is the
reason. It goes **inside** `~/tutor`, so this session walks up through
the course's own folder on its way to your home directory and can
therefore see the two skills that build things — the ones you are about
to spend the next two articles using.

What you build lands the other way round. It goes in
`~/tutor/bundle/.claude/`, which is below `~/tutor`, so it is visible
here and nowhere else. This folder reaches up to the course. The course
does not reach down into this folder. Nothing you build in the next hour
will ever turn up in a session about something else.

There is no version control here and nothing to install. A folder and
three files is the entire project.

One thing you may see first: because this session sits under `~/tutor`,
it reads the course's instructions on the way in and may run the
course's installer before it does anything else. That is expected. Let
it finish.

## Something to chew on

The chain needs documents. Ask for them:

> *"Write three short sample documents into this folder: a letter, an
> email, and an attendance note. Invent the matter — fictional names,
> fictional facts. Scatter a few dates through each one, and let some of
> them refer to the same events."*

What you should see: Claude writing three files, telling you what it
called them, and stopping. Something like a letter, an email and a note
sitting in `~/tutor/bundle` beside each other.

Open one and read it. You want to know roughly what dates are in there,
because in step four you will be checking a chronology against them, and
you cannot check an answer you never looked at.

That is the project. Now the parts that work on it.

Press `n`.

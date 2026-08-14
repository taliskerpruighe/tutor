---
id: other-models/what-you-give-up
title: What you give up
level: Level 2
part: Other Models
section: Running Other Models
order: 2
summary: Eight things a non-Claude endpoint cannot do, and everything else it still does
keywords: [tool_choice, prompt caching, token count, pdf, thinking budget, citations, batches, vision, compatibility]
---

# What you give up

*v0.2.10*

The compatibility is real. It is also partial. Point the harness at a
different address and it keeps speaking the same protocol, but the far
end does not implement every corner of that protocol.

What follows is the whole of that gap — every endpoint that is not
Anthropic's own, not one provider in particular. Whatever a given
provider adds on top of it is that provider's own business, covered
where that provider is.

This one is short.

## What stops working

- **Prompt caching** is ignored. Every turn is billed and processed
  cold, with nothing carried over from the last one.
- **`tool_choice`** is gone. The harness cannot force a particular tool
  or forbid one; it can only offer the set and hope.
- **Token counts** stop being exact and become an approximation, read
  off the underlying model's own tokeniser rather than the real count.
- **PDFs** do not work. A document handed over as a PDF is refused.
- **Image URLs** do not work either, though an image sent as raw data
  still does.
- **Batches** are gone — no submitting a pile of requests to be worked
  through later, unattended.
- **Citations** are gone. Nothing comes back with a structured pointer
  into a source document.
- **Thinking budgets** are accepted and then ignored. Setting one does
  not fail; it just does nothing.

That is the whole list.

## What keeps working

Everything else does. Messages, streaming, system prompts, multi-turn
conversations, tools and the results that come back from them, vision,
and thinking itself all carry over unchanged. So do two things you have
not been shown yet and will be: the permission flow that stops the
harness before it edits anything without asking, and the editing of
files itself.

## Why none of this touches the course

Almost everything left to teach you here sits on the harness side, not
the model's — instructions, agents, prompting, skills, subagents,
hooks, plugins. None of it appears on the list above, which means none
of it cares which model is answering. Learn any of it against a
different endpoint and it is not a simplified version of the lesson; it
is the same lesson, run somewhere else.

## The one with teeth

Set that against the one entry on the first list that does bite: token
counts stop being a fact and become a guess. What that number is for,
and why it matters, is covered properly once context itself is taught —
what it costs you here, before any of that, is that anything reading
how full a conversation is, or how much of it is left to spend, is
reading an estimate rather than a real number.

Press `n`.

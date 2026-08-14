---
id: other-models/pointing-elsewhere
title: Pointing the harness elsewhere
level: Level 2
part: Other Models
section: Running Other Models
order: 1
summary: The harness and the model are separate, and the address between them is a setting you can change
keywords: [base url, auth token, redirect, endpoint, provider, credential, api]
---

# Pointing the harness elsewhere

*v0.2.10*

You already know the harness and the model are not the same thing —
one is the body, the other is the brain it is attached to, and the
brain lives somewhere else entirely. They meet over a connection, and
a connection has an address. That address is a setting, and a setting
can be changed.

This article is the whole of what changing it takes.

## The address and the credential

Two environment variables decide where a request goes and what
credential rides along with it:

```
ANTHROPIC_BASE_URL    the address requests are sent to
ANTHROPIC_AUTH_TOKEN  the credential sent with them
```

Set the first to somewhere other than Anthropic's own servers, and
every request goes there instead. There is no plugin to install and
no fork to run — the redirect is a documented, first-party feature of
the harness itself. Anything sitting at that address, speaking the
same API, answers. It does not have to be Anthropic on the other end.
It has to speak the same language.

The address is the **root** a provider gives you, nothing appended.
Adding or dropping a trailing `/v1` on a guess is the single likeliest
way to get it wrong, and the two spellings look similar enough that a
typo here fails quietly rather than loudly. The provider's own setup
page is what settles the spelling — never assume it from another
tool's habit.

## Trying it for one run

The safe way to try a redirect the first time is inline, in front of
the command, so it lasts for exactly one run and nothing longer:

```
ANTHROPIC_BASE_URL=https://example-provider/api \
  ANTHROPIC_AUTH_TOKEN=your-token claude
```

Nothing here needs anything you have not already been taught. The
variables exist for the one command they sit in front of; close the
terminal, or run `claude` again on its own, and the redirect is gone.

There is a permanent home for these two variables, a file this course
has not shown you yet — that comes later, once you know what `.claude`
is.

## Why you would bother

A subscription buys access and headroom, not a fixed quality. The
same work, run with the same prompts and the same setup, can go well
one week and badly the next, with nobody to ask and nothing to
appeal to. Being able to point the harness at a different model is
what turns that from a thing endured into a thing decided.

That is worth having in reserve even if you never use it: the harness
is yours, and the model behind it is a part you can swap.

Press `n`.

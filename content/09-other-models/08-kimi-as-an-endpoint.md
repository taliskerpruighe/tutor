---
id: other-models/kimi-endpoint
title: Kimi as an endpoint
level: Level 2
part: Other Models
section: Kimi
order: 8
summary: The second worked example is the opposite shape to Ollama — a paid cloud service reached at one address, with nothing running on your machine
keywords: [kimi, moonshot, endpoint, base url, anthropic api, chat completions, coding, cloud, protocol]
---

# Kimi as an endpoint

*v0.2.10*

Ollama was a service on your own machine: a daemon on a local port,
answering before you had typed anything. Kimi answers from nowhere
near your machine at all — a paid cloud service, run by a company
called Moonshot, reached over the internet at one address. That is
chosen on purpose. The second worked example sits at the far end of
the range from the first.

What survives the trip between them is not the daemon. It is the
mechanism *Pointing the harness elsewhere* already taught: change one
address and whatever speaks the right protocol there answers instead.
The redirect is one address, and what sits at that address is
somebody else's problem — a process on your laptop for Ollama, a
company's infrastructure for Kimi, and the harness cannot tell the
difference from where it sits.

This one is short: an address, and the two wires behind it.

## Two wires, one of them right

Moonshot does not serve one protocol from its coding endpoint. It
serves two: a wire shaped like Anthropic's own Messages API, and a
second shaped like OpenAI's Chat Completions API — the shape most
other tools expect. Claude Code was built against the Anthropic SDK,
so the Anthropic wire is the one it wants. Point it at the other and
it is speaking the wrong language to something that never claimed to
understand it.

## The address itself

The Anthropic wire lives at `https://api.kimi.com/coding/`, and the
address stops there — no `/v1` on the end. Claude Code's own SDK
appends the rest of the path itself, so a base URL that already
carries `/v1` would end up asking for it twice.

*Pointing the harness elsewhere* already warned that a stray `/v1` is
the likeliest typo, and that it fails quietly rather than loudly.
Kimi is where that warning gets teeth. A sister tool, wired into the
other wire on the very same host, is configured against
`https://api.kimi.com/coding/v1` — one path segment longer, and a
different protocol surface entirely. Copy one address into the other
tool's setting and nothing announces the swap. The request still goes
somewhere that exists — a working address, a live server, an answer
that comes back — and none of it is where you meant it to go.

## Not Kimi Code

Moonshot also ships a harness of its own, called Kimi Code — its own
interface, its own way of reading a repository, a full alternative to
the one you already run. That is not what any of this is about. What
changes here is which model answers when Claude Code asks a question,
not which program you are typing into. You keep the harness. You
change the model.

Press `n`.

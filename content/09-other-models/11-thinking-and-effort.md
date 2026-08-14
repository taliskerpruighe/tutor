---
id: other-models/thinking-and-effort
title: Thinking and effort
level: Level 2
part: Other Models
section: Kimi
order: 11
summary: Five Claude Code effort levels collapse to three on Kimi's side, and one more setting is not a level at all — it is a different, cheaper model
keywords: [effort, thinking, kimi, k3, k2.6, k2.7 code, reasoning, low, medium, high, xhigh, max]
---

# Thinking and effort

*v0.2.10*

Claude Code lets you ask for an effort level — `low`, `medium`,
`high`, `xhigh`, `max`. Kimi's endpoint understands three of those
five words: `low`, `high`, `max`.

This one is short, and the whole of it is a single trap.

## Five requests, three answers

Type `/effort` in a session to set the level. On this endpoint it
is translated, not refused:

| Claude Code | Kimi |
|---|---|
| `low` | `low` |
| `medium`, `high` | `high` |
| `xhigh`, `max` | `max` |

That reads like a rounding error. It is closer to the opposite:
`medium` and `high` are not two settings that happen to behave
alike on Kimi. They are one setting with two names in Claude Code,
and choosing between them buys nothing at all — the model thinks
exactly as hard either way, because the request that reaches it is
identical either way. The same is true of `xhigh` and `max`: two
words in your vocabulary, one word in Kimi's. Leave the level unset
entirely and the default is `high`, exactly as if you had asked for
`medium` on purpose.

None of that costs you anything you can point to. That is the same
rule as *The plans*: effort is a request, not a guarantee. Kimi's
endpoint keeps the arrangement; it just has fewer distinct answers
to give.

## Off is not off

There is a sixth choice, and it does not belong on that table,
because it is not an effort level at all. It is a way of asking for
no thinking — `none`, or for K2.7 Code the keystroke `Option-T` on a
Mac — and the request does not reach K3 or K2.7 Code with their
thinking switched off. It reaches a different, older model instead:
K2.6, standing in for whichever of the two you had configured.
Nothing about the exchange announces the substitution. No error, no
warning, nothing in red — the reply arrives, it reads like an
answer, it settles the question you asked, and it is an answer from
a model you did not ask for, and you are billed for it.

That is the whole of the trap, and it costs nothing to avoid: on
this endpoint, thinking stays on.

Press `n`.

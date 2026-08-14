---
id: other-models/when-ollama-breaks
title: When Ollama breaks
level: Level 2
part: Other Models
section: Ollama
order: 7
summary: Seven ways the redirect looks broken when it is not, in the order you will actually meet them
keywords: [ollama, troubleshooting, tool calling, context length, connection refused, ollama signin, web search, base url, model swap]
---

# When Ollama breaks

*v0.2.10*

Point Claude Code at Ollama and the redirect itself will work. Something
downstream of it will not, and the two programs will not tell you why —
Claude Code only knows that it sent a request and got back silence, a
refusal, or a reply that never touches a file. None of it is a fault in
the three variables from *Running it*.

None of what follows raises an error Claude Code recognises as its own.
What comes next is ordered by how often you will meet each one, not by
how much it costs you when you do.

## Silence, not an error

The model answers pleasantly and edits nothing. Not a broken redirect
— the model itself does not do tool calling, and a model that cannot
emit a tool call reads a request to change a file and writes a
paragraph about it instead. No error, nothing in red. Change the
model.

The session goes quiet after a handful of exchanges, or refuses one
before it starts. That is the 4k default *Context length* already
named — a room the system prompt and the tool definitions have filled
before you have typed a word of your own. `ollama ps` shows the number
that was actually allocated.

Nothing answers at all, and the terminal reports connection refused.
The daemon is not running. `ollama ps` says so too, either with an
empty list or by failing outright.

## Refused, specifically

A cloud model comes back refused rather than silent. `ollama signin`
was never run, so the daemon holds no ollama.com account to
authenticate the forwarded request with. Claude Code's own token is
still the meaningless string *Signing in* already named — the refusal
happens a step further in, at the daemon, over an account it does not
have.

Web search does nothing, even on a model running entirely on your own
machine. Ollama's web search wants an account too — account required,
the same `ollama signin` — and if you signed up for nothing because
you never left the machine, this one tool is dead while every other
one works.

## The address itself

The base URL has a `/v1` on the end — the typo *Pointing the harness
elsewhere* already warned about. Most of what Ollama serves speaks the
OpenAI wire, and `/v1` is where that lives. The wire Claude Code is
actually sending to — the Anthropic one — is served from the root.
Drop it.

## Not broken, outmatched

The last one is not a failure of the setup at all. The model answers,
calls its tools, edits the right files, and the work is worse than
what you left behind. There is nothing here to fix. `--model` takes
one argument, and changing it is changing one word.

Press `n`.

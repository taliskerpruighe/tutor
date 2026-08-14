---
id: other-models/signing-in
title: Signing in
level: Level 2
part: Other Models
section: Ollama
order: 3
summary: A local model asks nothing of you; a cloud one wants an account, and the account lives with the daemon, not with Claude Code
keywords: [ollama, signin, cloud, account, token, api key, cloud suffix, ollama.com, authentication]
---

# Signing in

*v0.2.10*

*Running one yourself*, back in Level 1, installed Ollama and covered
what its daemon does: a background service on your own machine,
listening on a local address and answering an API there. What it did
not cover is an account, because a local model needs none — pull it,
run it, and nothing asks who you are.

A cloud model does.

One command settles it, and one habit is worth avoiding along the
way.

## Getting an account

Cloud models run on Ollama's own hardware rather than yours, and
reaching them needs an account at ollama.com. The command for it:

```
ollama signin
```

That opens a browser, the same shape as signing in anywhere else. Do
it once, from the machine running the daemon, and it is done.

## Where the account actually lives

The account does not live in Claude Code. It lives with the daemon,
and the daemon is what does the work: when a request needs cloud
access, Ollama authenticates it on your behalf before sending it on.
Claude Code's own side of the connection never changes — its
`ANTHROPIC_AUTH_TOKEN` is still the meaningless string `ollama`, sent
and ignored, exactly as it was for a local model.

## Naming a cloud model

Nothing else about the setup changes. Add `:cloud` to the model name,
and the same daemon, the same address, the same variables reach a
model running on Ollama's own hardware instead of yours —
`glm-4.7:cloud` rather than `glm-4.7`.

## One to ignore

The Ollama documentation also mentions `OLLAMA_API_KEY`. That is a
different route entirely — a key for a script talking to
`https://ollama.com/api` directly, over the internet, with nothing to
do with the local daemon. Do not set it here, and do not confuse it
with `ANTHROPIC_AUTH_TOKEN`.

## What does not change

An account is what cloud access needs. Nothing sourced here says
anything more specific than that — not what it costs, not what it is
called, not whether there is more than one kind of it.

What is certain is what it is not. Your Anthropic subscription plays
no part in this: it is not being spent, and it is not helping you.
Whatever the Ollama side asks for is a separate arrangement, with a
separate company.

| | Account | Hardware |
|---|---|---|
| Local model | none | yours |
| Cloud model | ollama.com | Ollama's |

Press `n`.

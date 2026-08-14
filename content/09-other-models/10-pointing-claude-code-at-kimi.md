---
id: other-models/pointing-at-kimi
title: Pointing Claude Code at Kimi
level: Level 2
part: Other Models
section: Kimi
order: 10
summary: The same two variables Ollama used, then a model named five times over and a context ceiling matched by hand
keywords: [anthropic_model, anthropic_base_url, anthropic_api_key, subagent, k3, k3-256k, kimi-for-coding, context window, environment variables, model slot]
---

# Pointing Claude Code at Kimi

*v0.2.10*

The redirect opens exactly as *Pointing the harness elsewhere*
described it: a base URL, and beside it a credential.

```
export ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
export ANTHROPIC_API_KEY=sk-your-key-here
```

What goes in that second line is the key from *Keys and
membership* — a genuine secret, not the meaningless token
Ollama was happy to take. Ollama never asked for anything past
these two lines: the model went on the end of the `claude`
command itself, picked fresh each run. Kimi wants the model
named up front, in the environment, and it wants it named more
than once.

This one has more moving parts than a base URL and a key.

## Naming the model, five times over

Set `ANTHROPIC_MODEL` to whichever one you are running —
`k3-256k`, say, or `kimi-for-coding`. Claude Code does not
read that value once and move on. It keeps a separate slot for
every tier of model it might reach for, and each slot has to
be pointed at the same name by hand:

```
export ANTHROPIC_MODEL=k3-256k
export ANTHROPIC_DEFAULT_OPUS_MODEL=$ANTHROPIC_MODEL
export ANTHROPIC_DEFAULT_SONNET_MODEL=$ANTHROPIC_MODEL
export ANTHROPIC_DEFAULT_HAIKU_MODEL=$ANTHROPIC_MODEL
export ANTHROPIC_DEFAULT_FABLE_MODEL=$ANTHROPIC_MODEL
export CLAUDE_CODE_SUBAGENT_MODEL=$ANTHROPIC_MODEL
```

Those names, bar one, are the Claude models from *The Claude
models*. Point all of them at the same value and the
consequence needs no more explaining than that: every slot
ends up on one model, so the models you met there stop being
separate. Kimi answers Opus, Sonnet, Haiku and Fable alike,
because as far as this endpoint is concerned they are the same
request.

The one that is not from that article is the last line, which
names something not yet covered in this course — a subagent.
What it is waits for a later part. Here it is one more slot,
set the same way as the rest.

## Matching the ceiling to the tier

*Keys and membership* already named the context ceiling your
plan allows. Two more variables are where that number actually
gets set, and they have to agree with each other and with the
plan:

```
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=262144
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=262144
```

Those figures are for the 256K models. A plan that allows the
1M window changes three lines at once — the model name and
both ceilings together:

```
export ANTHROPIC_MODEL="k3[1m]"
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=1048576
export CLAUDE_CODE_MAX_CONTEXT_TOKENS=1048576
```

`k3[1m]`, brackets and quotes included, is not the model's
name anywhere else. It is understood only by this one
variable, in this one setting. Carry it into an API call, or
into another tool's model field, and it breaks — the plain
name there is `k3`.

## Before the first launch

Kimi's own documentation prints one more step ahead of all
this: a script, run once before the very first launch, that
edits files inside a folder named `.claude`. That folder has
not been covered yet — it gets a part of its own, later in the
course, and what the script is editing belongs there rather
than here. Read it before running it, once you have reached
that part and know what the files it touches actually do.

Press `n`.

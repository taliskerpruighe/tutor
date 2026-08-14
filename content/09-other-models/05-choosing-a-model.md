---
id: other-models/choosing-a-model
title: Choosing a model
level: Level 2
part: Other Models
section: Ollama
order: 5
summary: Tool calling first, memory second, and today's best names are examples rather than a list worth memorising
keywords: [tool calling, model choice, ollama, qwen3-coder, gpt-oss, glm-4.7, minimax-m2.1, vram, cloud model, alias]
---

# Choosing a model

*v0.2.10*

A model that cannot call tools does not qualify, whatever else it
does well. Ollama's own library can be filtered on exactly this one
property, which is the fastest way to rule a name out before pulling
it.

That is the harness loop from *What a harness is*, and it has one
hinge. The model never reads a file or runs a command itself — it
asks, and the harness carries the request out and reports back. A
model that cannot phrase that request will still answer you, at
length and pleasantly, and never touch a single file.

Two more questions follow the first, and both are smaller than they
look.

## Whether it fits

*What a model consumes* already sized this: a serious desktop card
holds 24 gigabytes, and a Mac's shared memory runs a small model
only. That arithmetic has not moved — a coding-sized local model
wants at least 24 gigabytes of VRAM to run smoothly, more again for a
long conversation, and a laptop without it will either refuse the
model outright or crawl through it.

That ceiling applies to the local names below only. A cloud name pays
no VRAM cost at all, which is the entire reason it exists.

## Today's names

| Model | Runs | Good at |
|---|---|---|
| qwen3-coder | local | coding |
| gpt-oss:20b | local | general work |
| glm-4.7:cloud | cloud | high-performance |
| minimax-m2.1:cloud | cloud | speed |

**`qwen3-coder`** is Ollama's own pick for coding work, named without
qualification for exactly this use — and it is the specific model
behind the 24-gigabyte figure above, not a stand-in for it.

**`gpt-oss:20b`** also runs locally, built for general use rather
than code specifically, and lighter to carry than the coder model
above.

**`glm-4.7:cloud`** and **`minimax-m2.1:cloud`** run on Ollama's own
servers rather than the machine in front of you, which is what buys
them out of the size question above entirely.

None of the four names in that table will still be the right answer
in a year. Model names date faster than anything else in this
course — the two questions above are what carries, and every entry
in that table is an example of the day, not a list worth memorising.

## A name it does not need

Some tools outside Claude Code insist on seeing a real Anthropic
model name before they will start, and Ollama has a fix for exactly
that:

```
ollama cp qwen3-coder claude-3-5-sonnet
```

That copies the model under a name that satisfies the check. Claude
Code does no such checking, so it has no use for the alias — the
`--model` flag takes whatever name you actually pulled.

Press `n`.

---
id: ai/running-one-yourself
title: Running one yourself
level: Level 1
part: Agentic AI
section: LLMs
order: 5
summary: A program that runs models on your own machine, and the trick that gets past the card it does not have
keywords: [ollama, daemon, local model, cloud model, api, localhost, background service, vram, pull, run]
---

# Running one yourself

*v0.2.10*

A model can run on the machine in front of you. The program that does
it is called **Ollama**, and running models is the whole of its job:
installed once, then left running as a background service, with
nothing on screen and no window to keep open.

Once it is running it listens, on `http://localhost:11434`, an
address that never leaves the machine, and it serves an API there for
anything that wants to send it a request. Nothing about it is clicked
on afterwards. It is addressed, not opened.

Installing it means downloading it from ollama.com. Afterwards, two
commands confirm it took: `ollama --version` to check the command is
reachable, `ollama ps` to see what, if anything, is currently loaded.

## Pulling and running

A model is fetched by name and put to work by name, and those are two
separate steps:

```
ollama pull qwen3-coder
ollama run qwen3-coder
```

The first copies the files down — the same billions of numbers the
last article weighed in gigabytes. The second loads them and starts
answering. Nothing else is configured. The name is the whole
instruction, both times.

Reaching it at that address asks nothing of anyone: no account, no
sign-in, no authentication of any kind.

## The card you do not have

Pull a model of any size worth having and the ceiling from the last
article arrives immediately: it wants more VRAM than a laptop
carries, and no amount of patience fixes that.

Ollama's answer is not a smaller model. It is the same name, run
somewhere else. **Cloud models** run on Ollama's own hardware rather
than yours, and are reached through the identical local address —
Ollama takes the request at `localhost:11434` and forwards it
outward, so nothing about the connection changes on your end. Only
the model's name changes: a cloud model carries a `:cloud` suffix
(`glm-4.7:cloud`, `minimax-m2.1:cloud`) or a `-cloud` tag
(`gpt-oss:120b-cloud`). The billions of numbers never reach your
machine at all this time — only the answer does.

A cloud model needs an account at ollama.com — `ollama signin`, once.
A local one needs none.

So the open-weight models named two articles back — Llama, Mistral,
Qwen, DeepSeek — turn out to be reachable after all, from a laptop
with no 24 gigabyte card anywhere near it. What changes is a few
characters on the end of the model's name.

Press `n`.

---
id: other-models/running-it
title: Running it
level: Level 2
part: Other Models
section: Ollama
order: 4
summary: Three environment variables and a model name, then the one command that sets all three for you
keywords: [ollama launch claude, ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_API_KEY, model, cloud, config, yes, passthrough]
---

# Running it

*v0.2.10*

Three environment variables and a model name are the whole of the
redirect. This is the shortest article in the part, because that is
genuinely all of it.

Two ways to arrive there: set the three by hand, in front of the
command, or let one Ollama command set them for you. Both end at the
same session.

## The variables, then the model

Ollama's own setup asks for three variables, not the two you have
already met:

```
ANTHROPIC_AUTH_TOKEN=ollama \
  ANTHROPIC_API_KEY="" \
  ANTHROPIC_BASE_URL=http://localhost:11434 \
  claude --model qwen3-coder
```

Ollama's documentation is not settled on whether the empty API key is
actually required — one page sets it, another does not, and neither
explains the gap. Setting it costs nothing, so set it and stop
wondering. The model name at the end, `qwen3-coder`, is the only part
you change to try a different local model.

The same command again, model name swapped for a cloud one:

```
ANTHROPIC_AUTH_TOKEN=ollama \
  ANTHROPIC_API_KEY="" \
  ANTHROPIC_BASE_URL=http://localhost:11434 \
  claude --model glm-4.7:cloud
```

The address is the daemon's own root, with no `/v1` on the end — most
Ollama guides show a `/v1` because they speak a different wire, and
getting this one wrong is the likeliest typo, as already noted in
*Pointing the harness elsewhere*.

## The shortcut

Ollama ships a subcommand that does this for you, and the command it
launches is named `claude` — not a binary-name guess, the literal
target:

```
ollama launch claude
```

It prompts for a model, configures Claude Code, and starts it. To do
the configuring without the starting:

```
ollama launch claude --config
```

Two flags skip the prompt. `--model` names the model directly,
bypassing the selector; `--yes` skips asking anything at all and
pulls the model down first if it is not already local, but it
**requires** `--model` — an unattended run has to say what it is
running. A bare `--` at the end passes everything after it straight
through to Claude Code itself, which matters once you have met the
flags that start a session with no screen at all, taught later in the
course.

## Why the order

The shortcut looks like the place to start, and is not. `ollama
launch claude` is a command that happens to exist, on this one
machine, for this one provider. The three variables above are the
mechanism it is built on, and a mechanism carries to the next
provider, or the next machine, when no subcommand is there to help.
Learn the variables first and the subcommand is a shortcut. Learn the
subcommand first and it is all you have.

Press `n`.

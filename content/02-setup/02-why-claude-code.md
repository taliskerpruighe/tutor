---
id: claude-code/why-claude-code
title: Why Claude Code
part: Setup
section: How It Works
order: 2
summary: Why the model lives in a data centre, the harness lives on your Mac, and what the alternatives are.
keywords: [vram, gpu, ram, cpu, openai, gemini, llama, mistral, qwen, local]
---

# Why Claude Code

Claude is one model among many. It is worth a page on what else is out
there, because it explains the shape of what is on your machine.

## The other models

**Cloud models**, run by the company that built them, reached over the
internet. Anthropic's Claude. OpenAI's GPT models. Google's Gemini. You
never hold the model itself; you send it text and get text back.

**Open-weight models**, published for anyone to download and run
themselves. Meta's Llama, Mistral's models from France, Alibaba's Qwen.
The files are yours. What you do with them is your business.

The open ones sound obviously better until you try to run one, at which
point the constraint appears.

## Two very different appetites

The harness and the model want completely different machines.

**A harness is an ordinary program.** It reads files, runs commands, keeps
track of a conversation, talks over the network. That needs a processor and
some memory — **CPU** and **RAM** — and not much of either. Your Mac has
plenty. So does a ten-year-old laptop.

**A model is not an ordinary program.** Running one means holding billions
of numbers where they can be multiplied together, very fast, all at once.
The hardware for that is a graphics chip, and the memory it needs is its
own: **VRAM**, video memory, sitting on the card.

The quantities are the whole story. A capable model needs tens to hundreds
of gigabytes of it. A serious desktop graphics card has 24. The machines
that run frontier models are racks of specialist hardware, wired together,
in buildings with their own power supply.

> Your Mac is a slightly special case, and it does not change the answer.
> Apple Silicon shares one pool of memory between the processor and the
> graphics chip, which means a MacBook can run a small open model where a
> typical laptop cannot. Small is doing real work in that sentence. It will
> hold a conversation. It will not do what you are about to see.

## So the work is split

Which gives the arrangement you have:

| | Runs where | Because |
|---|---|---|
| Claude Code | your Mac | it needs a CPU and your files |
| Claude | a data centre | it needs hardware you cannot own |

Everything touching your machine is local. Your files are read locally.
Commands run locally. Permission is asked locally. What crosses the network
is text: what the model needs to see, and what it says back.

And it means the heavy part is somebody else's problem. You are not buying
graphics cards, or leaving a laptop running hot overnight. The largest
models Anthropic has answer you from a terminal window on a machine that
could not begin to hold them.

## Why this one

Beyond the model itself, which you can judge for yourself over the next few
days:

**It is a terminal program.** No separate app, no editor to adopt, no
window to alt-tab to. It sits in the same place your work already happens
and reaches the same files.

**You watch it work.** Every file it reads, every command it runs, is
printed as it happens. When it goes wrong you can see exactly where.

**It asks first.** Anything consequential stops and waits for you.

**It can be taught.** The rest of this course is that: agents, skills, and
chains of them are all ways of writing down how you want things done, once,
so you stop explaining it every time.

Press `n`.

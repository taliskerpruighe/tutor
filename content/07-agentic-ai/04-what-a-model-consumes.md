---
id: ai/what-a-model-consumes
title: What a model consumes
level: Level 1
part: Agentic AI
section: LLMs
order: 4
summary: Billions of numbers held where they can be multiplied at once, and free is not the same as available to you
keywords: [vram, gpu, graphics card, ram, apple silicon, memory, open weight, hardware]
---

# What a model consumes

*v0.2.0*

A model is not an ordinary program. Running one means holding billions
of numbers where they can be multiplied together, very fast, all at
once, for every single word it produces. The hardware for that is a
graphics chip, and the memory it needs is its own: **VRAM**, video
memory, sitting on the card rather than in the computer's ordinary
memory.

The quantities are the whole story. A capable model needs tens to
hundreds of gigabytes of it. A serious desktop graphics card, the kind
bought for gaming, has 24. The machines that run frontier models are
racks of specialist hardware, wired together, in buildings with their
own power supply and their own cooling, built for nothing else.

Nothing about this is a software limitation someone could code around.
The numbers have to sit somewhere fast enough to reach, and the chip
that reaches memory that fast is bought by the rack, not the unit.

> Your Mac is a slightly special case, and it does not change the
> answer. Apple Silicon shares one pool of memory between the
> processor and the graphics chip, which means a MacBook can run a
> small open model where a typical laptop cannot. Small is doing real
> work in that sentence. It will hold a conversation. It will not do
> what you are about to see.

## Free is not the same as available

That is the catch behind the open-weight models from the last article.
The files being free to download says nothing about whether you can
run them. Llama, Mistral, Qwen, DeepSeek — every one of them is yours
to have, and none of them fits on a laptop at the size that competes
with a frontier cloud model. Downloading one and finding out it
answers slower and worse than the cloud model you already had is the
usual way this lesson gets learned.

What is genuinely available to you, on the machine in front of you, is
whichever cloud model you can reach over the internet — or a small
open one doing noticeably less. That is the whole reason Claude
arrives as a connection rather than a download: the alternative is not
on offer.

That is what the model needs to run at all.

Press `n`.

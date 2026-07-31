---
id: ai/the-models-there-are
title: The models there are
part: Agentic AI
section: LLMs
order: 3
summary: Cloud models you reach over the internet, open-weight models you can download, and why the second kind is harder than it sounds
keywords: [claude, gpt, gemini, llama, mistral, qwen, deepseek, kimi, cloud model, open weight]
---

# The models there are

*v0.2.0*

Claude is one model among many, and it helps to see the shape of the
whole field before going any further. Every entry on it is the same
mathematical function from the last two articles, at some size, built
some way, tuned for something. What separates them is who holds the
copy.

## The other models

**Cloud models**, run by the company that built them, reached over the
internet. Anthropic's Claude. OpenAI's GPT models. Google's Gemini. You
never hold the model itself; you send it text over a connection and get
text back. The company decides what version is running, when it
changes, and what it costs.

**Open-weight models**, published for anyone to download and run
themselves. Meta's Llama, Mistral's models from France, Alibaba's Qwen,
DeepSeek and Moonshot's Kimi out of China. The billions of numbers that
make up the model are ordinary files, and the files are yours once you
have them. What you do with them — run them, inspect them, change them
— is your business, not the publisher's.

## Why open sounds like the obvious choice

Nothing is sent anywhere. Nothing is logged by a company you have never
met. No pricing page can change under you, because there is no bill.
Read only that far and open-weight looks like the version of this
technology a solicitor ought to prefer, on privilege grounds alone.

The two categories are not as separate in practice as they sound.
Plenty of companies that built nothing themselves rent out somebody
else's open-weight model as a cloud service of their own — you reach
Llama or DeepSeek over the internet, exactly like Claude, from a
company that only ever hosted it. What decides which category a
session sits in is not who trained the model. It is whether the files
ever reach your machine.

The open ones sound obviously better until you try to run one
yourself, at which point the constraint appears.

That constraint is not a licence or a price tag. It is what a model
actually costs to have working in front of you at all — and it is
steep enough that "free to download" and "usable on your machine" turn
out to be two different claims.

Press `n`.

---
id: agents/context
title: Context
part: Agents
section: Context
order: 2
summary: Every agent has a fixed amount of brainspace, and everything it touches fills a little of it.
keywords: [context, context window, tokens, brainspace, model, haiku, sonnet, opus, fable, size]
---

# Context

The reason each agent is separate is that each has its own **context
window**. Everyone shortens that to **context**, and so will we.

Think of context as **brainspace**. It is a fixed amount of room, and
literally everything the agent sees or touches takes up some of it.

## Everything means everything

Reading its instructions. Opening a file. Your question. Its answer. Your
correction. The file it opened because of your correction.

```
  a fresh agent      ██░░░░░░░░░░░░░░░░░░
  reads the bundle   ██████░░░░░░░░░░░░░░
  drafts the memo    ██████████░░░░░░░░░░
  you correct it     ████████████░░░░░░░░
  it redrafts        ███████████████░░░░░
```

Nothing here ever comes back out. The bar only ever fills. A conversation
is a one-way trip from left to right, and the only question is how fast
you make it.

Note the first line. An agent is not empty before you type — it has
already read its rules, the descriptions of every skill it can reach, and
the definition of every tool it can use. That is what a launch costs you.

## The unit

Context is measured in **tokens**, not words. A token is a chunk of text
roughly three-quarters of a word long, so:

```
  1,000 tokens  ≈  750 words   ≈  2 pages
```

Useful mainly for sanity checks. A forty-page witness statement is
somewhere near 20,000 tokens before the agent has done anything with it.

## How much room there is

That depends entirely on the model the agent is running.

| Model | Context |
|---|---|
| Haiku | 200,000 |
| Sonnet, before Sonnet 5 | 200,000 |
| Sonnet 5 and later | 1,000,000 |
| Opus | 1,000,000 |
| Fable | 1,000,000 |

A million tokens sounds like more than you could ever use. It is not, and
the next article is why.

## This is what Setup was really about

Look back at *Location matters*. The rule there was **more is worse** —
every extra agent and skill on the walk-up path makes the session worse at
everything, including questions none of it touched.

Context is the mechanism. Every one of those extras is read at launch and
sits in the window from the first word onward, on the bar above, in the
`██` you had before you typed. Party Trick #1 works because it starts you
further left.

Press `n`.

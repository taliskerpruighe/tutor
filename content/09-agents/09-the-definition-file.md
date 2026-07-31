---
id: agents/definition
title: The definition file
part: Agents
section: Custom Agents
order: 9
summary: Two parts — frontmatter for the settings, body for the instructions — and most documented settings are noise.
keywords: [definition, frontmatter, YAML, body, instructions, role, markdown, the boss]
---

# The definition file

*v0.1.0*

Open one of those files and you find two parts, always, in this order.

```
---
name: bundler
model: haiku
---

You read disclosure bundles and report what is
relevant. You never write to a file.
```

Everything between the two `---` lines is the **frontmatter**. Everything
after is the **body**. That is the entire shape of an agent definition.

| Part | What it is | Written in |
|---|---|---|
| frontmatter | the settings | YAML |
| body | the instructions | plain prose |

## The body

The body is free. Whatever you write here is what the agent knows about
itself before you have said a word, and there is no format to follow.

Useful things to put in it:

- **What its role is.** *"You review disclosure for relevance."*
- **What it must not do.** *"Never draft. You report; someone else
  drafts."*
- **The context it works in.** *"This is a commercial dispute. The client
  is the defendant."*
- **What to reach for.** *"Use the bluebook skill for every citation."*

Write it the way you would brief a new paralegal on their first morning.
That is genuinely the right register — say what the job is, say where the
edges are, and do not assume anything is obvious.

There is one thing worth knowing about the body. When this agent is
called by another agent to do a job, the body **replaces** its normal
instructions rather than sitting on top of them. So it has to stand on its
own. An instruction that only makes sense as an afterthought to something
else will not survive.

## The frontmatter

The frontmatter is the settings, written in **YAML** — a format where each
line is `key: value` and the spelling of the key has to be exact.

That last part matters more than it should. A key Claude Code does not
recognise is **ignored in silence**. No error, no warning, nothing in red.
The file loads perfectly and the setting you thought you set was never
read. This is the single most common way an agent definition goes wrong,
and it looks exactly like an agent definition going right.

## The fields, and the truth about them

The official documentation lists a great many fields you can put in there,
with a great deal of explanation for each.

> **From the Boss:** *"Most of them are either lies or useless."*

Unless you are building software to sell to other people, six fields do
real work and the rest is decoration. The next article is those six.

Press `n`.

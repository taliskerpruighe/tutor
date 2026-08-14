---
id: other-models/keys-and-membership
title: Keys and membership
level: Level 2
part: Other Models
section: Kimi
order: 9
summary: A Kimi key does not exist without a paid membership behind it, and the same tier decides what the key may be asked for
keywords: [kimi, api key, membership, subscription, console, secret, tier, context window, overflow, extra usage]
---

# Keys and membership

*v0.2.10*

A Kimi API key does not exist on its own. It sits inside a paid Kimi
membership with the coding benefit switched on, and until that
benefit is active the console will not let you make one — this is
the precondition the rest of the setup assumes, not an optional
add-on bought later.

Short: a console, a cap of five, and a secret worth treating like one.

## Making the key

Kimi hands out keys from a web console, not from inside the harness.
Sign in, open the console, and create one: name it, confirm, and the
key appears once, in full.

Copy it before you close that dialog. The console will not show the
whole string again — close it unread and the only remedy is making
another. A single account holds up to five keys at a time, so losing
count of them is a real limit, not a formality. The key is provisioned
entirely on Kimi's side, before any of it reaches Claude Code.

## A genuine secret

Ollama's harness-side credential, from *Signing in*, is a meaningless
string, sent and ignored. A Kimi key is the opposite kind of thing:
it is checked against your account, spends your membership's quota,
and is worth money the moment a call goes through on it. Treat it the
way you would treat a password, because that is functionally what it
is.

Where a credential like this lives permanently inside Claude Code's
own setup is covered later in the course. Wherever it ends up, a key
sitting in a plain file is a secret sitting in a plain file, and it
wants exactly that care.

## What the tier buys

Kimi sells the coding benefit in tiers, and one tier controls two
separate things: which models you may point the harness at, and how
large a context window you may ask for. Neither follows from the
other. Being allowed to name a model does not mean you are allowed
its largest window — that can sit behind a tier of its own, above the
one that unlocked the model itself.

Ask past either ceiling and the call fails outright, the same way a
model the tier does not cover fails. There is no partial answer, and
no quiet downgrade to what the tier does allow.

## When the quota runs dry

Membership buys a quota, and the quota is not open-ended. Beyond it
sits an overflow balance, billed by use rather than by subscription
and topped up separately from the membership itself — a subscriber
can turn it on so a run of work does not simply stop when the quota
does.

That balance is not exclusive to the coding benefit, either. It is
shared with Kimi's own web product, so spending it through the
harness and spending it through the ordinary chat interface draw
down the same number.

Press `n`.

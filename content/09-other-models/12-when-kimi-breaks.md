---
id: other-models/when-kimi-breaks
title: When Kimi breaks
level: Level 2
part: Other Models
section: Kimi
order: 12
summary: Five ways the redirect looks broken when it worked, or looks fine when it has quietly fallen back
keywords: [kimi, status, base url, v1, k3, "k3[1m]", context window, thinking, k2.6, model id, plan tier]
---

# When Kimi breaks

*v0.2.10*

Kimi does not fail with a red banner. It fails by looking exactly like
Claude Code working — the same model name reported back, the same
session, the same prompt — and the difference sits somewhere you have
to go and look for.

That is not a comment on Kimi. Point the harness at a different
address and the address is the only thing that changed; everything
else the harness prints about itself was written to describe the
Anthropic side, and it goes on saying those things regardless.

Five shapes this takes.

## The name is not the check

Open a session pointed at Kimi and the model name in `/status` still
reads Sonnet, or Opus, or whichever Claude name the session opened
with. That is not a leftover label the redirect forgot to update.
Every call is genuinely going to Kimi, and the display genuinely still
says Claude — the name was never wired to check anything, so it does
not change when the destination does.

The real check is the Base URL. If that reads Kimi's address, the
redirect worked, whatever the model name says next to it.

This is the likeliest false alarm in the whole setup, and it runs in
both directions. A working session looks broken, because the name
never moved. And a session that has silently fallen back to a
different model behind the same name looks fine, because the name
never moved there either.

## The wrong wire

Kimi's Anthropic-compatible endpoint is `https://api.kimi.com/coding/`,
nothing after the trailing slash. A `/v1` tacked onto that address is
not a Kimi problem — it is the address for a different protocol
entirely, the one a translating router uses to feed Kimi into a tool
that speaks another vendor's API instead of Anthropic's. Same host,
different door. Carry that form into `ANTHROPIC_BASE_URL` and the
harness is knocking on a door built for another visitor.

## A bracket in the wrong field

`k3[1m]`, brackets included, is a real form — but it does one job in
one place. Set as the model in Claude Code's own environment
variables, it tells the harness to open K3's full context window.
Anywhere else — a raw request, the model field of a different tool —
plain `k3` is what is wanted, and the bracketed form is not
recognised there. Carry it into the wrong field and the answer is a
flat refusal: no model by that name.

## A tier that does not reach that far

Ask for `k3` on a plan that does not carry it, or for its full context
window on a plan that only carries `k3` at the smaller size, and the
refusal is immediate rather than a quiet downgrade. The error names
what was asked for — but the two messages do not spell the model the
same way: one writes it as `kimi-k3`, the other as `k3`. Do not go
looking for one exact string to match against. Read what the message
says your plan does not cover, and act on that.

## Thinking, turned off

Turn thinking off and Kimi does not run K3, or K2.7 Code, on a shorter
leash. It runs K2.6 instead, silently, and the reply comes back
billed all the same. Nothing in the response says which model
actually answered — the setting you changed was never "less
thinking," it was "a different model."

That is the second half of the false alarm from earlier: a session can
look entirely healthy — right name, right address, an answer that
arrives promptly — while running on a model you did not choose. Keep
thinking on to use K3 or K2.7 Code; turning it off is not a lighter
version of either one.

---

That is Other Models. Claude Code Setup comes next — installing
Claude Code, launching it, and the `.claude` folder every one of these
articles has been deferring to.

Press `n`.

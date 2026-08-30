---
id: challenges/three
title: Challenge three
level: Level 2
part: Challenges
order: 3
summary: Small businesses want a web application that turns their uploaded paperwork into finished financial statements
keywords: [challenge, web application, accounts, upload, profit and loss, balance sheet, chat, hosting, period, statements]
---

# Challenge three

*v0.2.14*

Nobody need pay for accounting software again. That is the claim
behind this challenge, and the challenge is to prove it by building
the thing rather than arguing for it.

The proof has a specific shape. It is a web application the reader
hosts personally, reachable by a stranger who does no more than type
an address into a browser — not a spreadsheet dressed up to look
like one.

## The books coming in

A handful of invented small businesses have agreed to let the reader
put a year of their paperwork through whatever gets built. Each one
signs up inside the finished application, uploads what it would
otherwise hand a bookkeeper, and finds out whether the two statements
that come back are actually right.

The whole arrangement — every business, a year of its documents —
sits in `materials/challenge-three/`.

What arrives is bank statements, bills, receipts and invoices, out of
several sources and several formats, with nothing shaped to make the
job easier. The businesses differ from each other on purpose, so a
year of stock movements and a year of nothing but service invoices do
not quietly reduce to the same shape.

The input is a mess, and it should stay one. What comes out the other
end must not be.

## Two statements, unprompted

Out of whatever has been uploaded, the application should produce two
financial statements without being asked: a profit and loss, and a
balance sheet. Nobody sets a reporting period in advance.

The period is whatever the uploaded documents happen to cover,
whether that turns out to be a single month or several years, and
nothing about the design should assume otherwise.

Getting there means treating documents that disagree with each other
in format as figures that must agree with each other in substance,
reconciling anything that only states a balance against the material
that explains how it was reached.

## What has to be on the page

One page after login is enough for all of this to live on, and the
same account can be logged out of as easily as it was logged into.

- **Somewhere to upload.** A single place for whatever the business
  wants to add next.
- **Somewhere to browse.** Every document uploaded before, sitting
  where it can be opened again.
- **The two statements.** Sortable and filterable by period, not
  fixed to whatever range they first appeared in.
- **An agent, reachable through a chat box.** Tied to the account,
  and living on the same page as everything else.

Nothing else has to be there. Everything the business does with the
application, it does from that one page.

## The terms of the challenge

Nothing here says how to build it. No stack is specified, and no
particular way of handling a login is required. Only the finished
shape matters — what happens when a stranger opens the address and
starts using it.

Beyond that, Levels 1, 2 and 3 of this course are free to draw on,
and using them well matters more than being clever about what is
left out.

Running on the reader's own machine proves the mechanism works, and
nothing more than that. It counts for more once somebody else, on a
different machine entirely, can reach it without help. The furthest
version needs nobody at all — it survives a reboot, keeps taking
uploads and keeps producing statements while nobody is watching it.

Nobody marks this. The only proof that matters is that it works, and
that a second person, on a second machine, can pick it up and use it
without being told how.

Press `n`.

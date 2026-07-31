---
id: ai/renting-a-computer
title: Renting a computer
part: Agentic AI
section: Cloud Computing
order: 8
summary: When your own machine is not enough, you rent someone else's by the hour rather than buy one
keywords: [cloud, aws, amazon, google, microsoft, azure, box, rent, hourly, data centre, server]
---

# Renting a computer

*v0.2.0*

A laptop running twenty agents at once badly is not a laptop problem
you fix by buying a better laptop. It is answered by not using the
laptop at all.

**Cloud computing** is renting somebody else's computer, by the hour,
over the internet. **Amazon**, through Amazon Web Services, **Google**,
through Google Cloud, and **Microsoft**, through Azure, each own vast
buildings of machines and will let you use one for as long as you are
paying and not a minute longer.

## What you are actually renting

Not a service, not an app — a machine. It has a processor, memory and a
disk, sitting in a data centre somewhere, reachable only over the
network. Nothing about it is specific to AI; the same arrangement rents
a machine to host a website, run a database, or do anything else a
computer does. Running agents on it is one use among many the renters
never had to design for specially.

Colloquially, this machine is a **box**. You spin one up, you have a
box; you shut it down, the box is gone and so is the meter running
against you.

That is the whole difference from a laptop worth naming. A laptop is a
single machine you own, sized once, for the average day rather than
the busy one. A box is sized on purpose, per job, and there is no limit
on how many you can have running at once beyond what you are willing to
pay for.

## Paying by the hour

The bill is usage, not ownership. A box exists for as long as you keep
it running and costs nothing the moment you stop it — the opposite of
a laptop, which cost the same whether it sat idle or ran hot all night.

That is what answers the problem the last two articles built up. Twenty
agents at once needs twenty times the CPU and RAM one harness wants,
for the length of one job, and then never again. Renting a box sized
for that hour is cheaper and simpler than owning hardware that sits
mostly unused waiting for the next time you need it.

> Sizing is a real decision and a small one. A box comes in named sizes
> — more CPU, more RAM, more disk, all costing more per hour — and
> picking one only wants to be roughly right. Too small and a job runs
> slowly; too large and you paid for room you did not use. Either
> mistake costs you an hour's difference in price, not a wasted
> purchase.

The next article is what you actually do once the box exists.

Press `n`.

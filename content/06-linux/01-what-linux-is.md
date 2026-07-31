---
id: linux/what-linux-is
title: What Linux is
level: Level 1
part: Linux
section: The world runs on linux
order: 1
summary: A kernel, not an operating system — and the distributions that build one around it.
keywords: [linux, kernel, distribution, distro, open source, unix, debian, fedora, arch, nixos]
---

# What Linux is

*v0.1.0*

You have heard the name. It runs on most of the servers on the internet
and almost none of the desktops, and the reason for both is the same
fact: Linux is not an operating system. It is a **kernel**.

The article on the shell described the kernel as the layer that talks
to the hardware directly — reading the disk, drawing the screen, handing
out memory — and said nothing else gets that close to the metal. Linux
is one of those kernels, and a widely used one.

> It started in 1991 as a hobby project: a university student in
> Helsinki wanted a free Unix he could run on his own PC, and posted the
> source online to see whether anyone else cared. A great many people
> turned out to care.

## A kernel needs dressing

A kernel alone has no prompt, no windows, and no way to install
anything. Someone has to wrap a shell around it, add a package manager,
and — if the plan includes one — a desktop. That whole assembled bundle
is a **distribution**, usually shortened to **distro**, and it is what
you would actually install.

Different groups assembled the dressing differently, for different aims:

| Distro | Built for |
|---|---|
| Debian / Ubuntu | stability; the default choice |
| Fedora | new features, tested fast |
| Arch | minimal; you assemble it by hand |
| NixOS | reproducible configuration, as one file |

Same kernel under every row. What changes is the shell it ships with,
the package manager, the desktop environment if there is one, and how
much the defaults decide for you.

## Nobody owns it

Linux is open source: the code is published, anyone can read it, anyone
can propose a change to it, and no company can lock the result up.
Companies sell support and their own distros around it — Red Hat,
Canonical — but the kernel itself belongs to nobody, the way a published
proof belongs to nobody once it is out.

> *Your shell is zsh* already placed Linux in the family tree: your Mac
> is a certified Unix descendant, and Linux is an independent rebuild of
> the same design, done in the open. Related, not identical.

That is what Linux is. Where it actually runs — which is very nearly
everywhere except the desk you are sitting at — is the next article.

Press `n`.

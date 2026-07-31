---
id: claude-code/installing
title: Installing
level: Level 1
part: Claude
section: Claude Code setup
order: 6
summary: It is already on your Mac — how to check, how to sign in, and how to put it on the next machine.
keywords: [install, installer, update, version, sign in, login, account, doctor]
---

# Installing

*v0.1.0*

This one is short, because it has already been done for you and because
the official docs are genuinely good here. Read this, then move on.

## Checking it is there

In Ghostty:

```
claude --version
```

A version number back means it is installed and on your **path** — the
list of folders your shell searches when you type a command. If instead
you get `command not found`, it is not installed, and the next section is
for you.

## Putting it on a machine that lacks it

One line:

```
curl -fsSL https://claude.ai/install.sh | bash
```

That downloads a small script and runs it. It installs into your home
folder, so it never asks for your password. Close Ghostty and open it
again afterwards, so your shell picks up the new command.

> There are other ways — Homebrew, npm — and they all end up in the same
> place. Use the line above unless someone tells you otherwise. The
> current instructions are always in the [Claude Code
> docs](https://docs.claude.com/claude-code).

## Signing in

The first time you run `claude`, it will ask you to sign in and open a
browser window to do it. Log in with the Anthropic account your
subscription is on, and the browser will tell you to go back to
Ghostty. That is the whole of it.

It remembers. If you are ever asked again, sign in the same way.

## Keeping it current

To check for a newer version and install it if there is one:

```
claude update
```

And if something seems wrong with the installation itself:

```
claude doctor
```

That prints a check per line and says what to do about anything failing.

It is installed. The next article is starting it, and the one thing about
starting it that actually matters.

Press `n`.

---
id: shell/powerline-themes
title: Powerline themes
level: Level 1
part: The CLI
section: Command Lines and Prompts
order: 13
summary: A prompt built from coloured blocks called segments, each showing a single fact about where you are, and why the seams between them need a special font
keywords: [powerline, segment, nerd font, hack nerd font, p10k, powerline10k, git branch, ssh, hostname, google drive]
---

# Powerline themes

*v0.2.9*

The style you have seen in other people's terminals — a prompt built from
blocks of solid colour, each one a different shade, fitting together left
to right like a strip of film — is called a **powerline** theme.

It began as a plugin for a text editor, and the look outgrew it. A
powerline prompt is built entirely from little coloured facts rather than
plain text. Each block is a **segment**, and a segment shows exactly one
thing. It appears when that thing is true of where you are standing and
disappears when it is not, so the same prompt runs long inside a project
folder and short in your home directory.

## What a segment is for

A segment can say where you are, and that includes further than your own
folder. Connect to a client's server to check a file, and an ordinary
prompt gives no sign you left your own machine — you type a command meant
for your laptop into a shell running somewhere else. A powerline theme
puts the hostname in its own segment, coloured differently from the rest,
so the change of machine is the first thing you see rather than the thing
you discover afterwards.

Working in a folder Git is tracking, a segment can show the branch name,
and a second symbol if there are changes not yet committed. You get that
fact at every prompt, not only when you remember to ask for it with a
command.

## Outside code, the same trick

None of this needs programming to be useful. A segment can show which
dataset a folder holds or how many rows are in it, the same way a branch
segment shows which line of work you are on. A folder synced by Google
Drive can carry a segment of its own — showing whether the matter folder
underneath you has finished uploading, which matters when you close the
laptop lid straight after saving a document and trust it reached the
shared drive before you did.

## The symbol no ordinary font has

There is a catch, and it explains a detail of your setup nobody has told
you the reason for. The seam between two segments is drawn with a solid
arrow-shaped character, and no ordinary font contains it. **Nerd Fonts**
are ordinary fonts with a few thousand of these extra symbols bolted on —
arrows, folders, logos, brackets — which is why your terminal is set to a
font called *Hack Nerd Font* rather than plain Hack. Without it the seams
render as empty boxes, one per segment, instead of joining up.

## Powerline10k, and why it stopped

The theme most people mean by this is **Powerline10k**, a plugin written
for zsh specifically, and for years it was close to the default choice —
fast, heavily configurable, screenshotted everywhere it was used. Its own
authors have since said it will get no further work, which leaves it
stable but frozen: it runs, and nothing about it will improve or break,
because nobody is changing it any longer.

That is not the same as it disappearing. It is the reason something else
has taken its place as the one worth installing new — and that one is not
tied to zsh at all.

Press `n`.

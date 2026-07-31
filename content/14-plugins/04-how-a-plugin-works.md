---
id: plugins/how-it-works
title: How a plugin works
part: Plugins
section: Using Them
order: 4
summary: A manifest names it, a marketplace lists it, and installing it is a choice of scope you already know how to make
keywords: [plugin, manifest, plugin.json, marketplace, install, enable, disable, update, global, project]
---

# How a plugin works

*v0.2.0*

Two files decide whether Claude Code will treat a folder as an
installable plugin at all, and they do two different jobs.

## The manifest

`.claude-plugin/plugin.json` is the plugin's own identity — its name
and version, and a description of what it does. It says what the
plugin is. It does not say where to find it, and that is the second
file's job.

## The marketplace

A plugin cannot be installed on its own. It has to appear in a
**marketplace** — a JSON listing of plugins Claude Code can browse and
install from, the way a manifest is one plugin's identity card and a
marketplace is the shelf it sits on. A marketplace can be as small as
one plugin you built for yourself, or as large as a shared list a firm
maintains for everyone in it.

That requirement is the whole reason plugins are not simply "a folder
you point Claude Code at." Without a marketplace listing it, a folder
full of agents and skills is exactly that — a folder — and Claude Code
has no reason to treat it as installable rather than just readable.

## Installing it

From there, installing is a question of scope, and it is the same
question *More `.claude` directories* already answered for an ordinary
project: global, or one project.

Installed **globally**, a plugin is available in every session on the
machine, the same reach as anything sitting in `~/.claude`. Installed
**per project**, it is available only inside that one folder's
sessions, the same reach as anything written into that project's own
`.claude`. Nothing about a plugin changes that choice — it is the
identical layering, just arriving as an install rather than a file you
wrote by hand.

## Turning it off without removing it

A plugin does not have to be uninstalled to stop applying. It can be
**disabled** — in global settings, which switches it off everywhere at
once, or in one project's settings, which switches it off there alone
while it stays live in every other project it is installed into. That
is worth knowing before you reach for uninstalling anything: disabling
is the smaller, reversible move, and it is usually the one you want
when a suite is misbehaving in one place and nowhere else.

## Keeping it current

A plugin built once and improved later is still one folder — updating
it means pulling the newer version from wherever the marketplace
points, rather than reinstalling it into every project it reached. The
whole point of the voice-agent example from the last article was this:
one place to improve, felt everywhere it is installed, the moment you
update it.

Knowing the shape of all this is not the same as building one. The
next article is what that actually takes.

Press `n`.

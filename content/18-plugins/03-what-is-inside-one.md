---
id: plugins/inside
title: What is inside one
level: Level 2
part: Plugins
section: What They Are
order: 3
summary: The same folders as .claude, plus one extra folder that is what actually turns an ordinary directory into a plugin
keywords: [plugin, claude-plugin, agents, skills, hooks, mcps, settings, commands, manifest]
---

# What is inside one

*v0.2.0*

Open a plugin and it looks exactly like the inside of `.claude`,
because that is what it is.

```
  my-plugin/
  ├── .claude-plugin/
  ├── agents/
  ├── skills/
  ├── hooks/
  ├── mcps/
  └── settings.json
```

`agents/`, `skills/` and `hooks/` hold exactly what they hold in a
project's own `.claude` — nothing about being inside a plugin changes
what any of these files look like. `mcps/` is where a plugin's own MCP
connections live, for a suite that needs to reach a service outside
Claude Code entirely. An older plugin may also carry a `commands/`
folder; per the Boss, it is obsolete — a command was simply a skill
under an earlier name, and anything you would put there now goes in
`skills/` instead.

`settings.json` works the same way it does everywhere else in this
course: the place to override defaults. A plugin's `settings.json`
overrides the global ones for whatever project the plugin is installed
into, the same layering *More `.claude` directories* already showed
you between a project and `~/.claude`.

## The folder that makes it a plugin

None of that, on its own, is a plugin. An ordinary folder with an
`agents/` directory inside it is just an ordinary folder. What makes
it a plugin is `.claude-plugin/` — a folder Claude writes for you,
holding the manifest that names the plugin and describes what it is.
Without it, the folder is a pile of assets Claude Code has no reason
to treat as one thing.

## A worked example

A `bundle-tools` plugin, built around the exercise from *Step two — the
workers*, might look like this:

```
  bundle-tools/
  ├── .claude-plugin/
  │   └── plugin.json
  ├── agents/
  │   ├── bundle-reader.md
  │   └── bundle-consolidator.md
  └── skills/
      ├── bundle-read/
      └── bundle-consolidate/
```

Two agents, two skills, the manifest that names the bundle — nothing
in it that was not already sitting in a project's `.claude`, just
moved somewhere it can be installed from rather than only read from.

Press `n`.

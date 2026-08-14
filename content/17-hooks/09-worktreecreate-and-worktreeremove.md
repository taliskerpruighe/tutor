---
id: hooks/worktreecreate-and-worktreeremove
title: WorktreeCreate and WorktreeRemove
level: Level 2
part: Hooks
section: Using Them
order: 9
summary: the closing pair of triggers, firing when a second working copy of a repository appears or disappears beside the first
keywords: [worktreecreate, worktreeremove, worktree, git, settings.json, isolation, cleanup]
---

# WorktreeCreate and WorktreeRemove

*v0.2.9*

A worktree, as *Worktrees* already covered, is a second working folder
attached to one repository, appearing either at a main agent's own
launch or the moment a subagent spawns with `isolation: worktree` in
its frontmatter, and disappearing again once that subagent has
returned its answer. `WorktreeCreate` and `WorktreeRemove` are hooks
fired at exactly those two moments, from outside the mechanism that
causes them. Both watch a folder rather than a file, a tool call or a
conversation.

## What a fresh worktree is missing

A worktree gets the whole tracked history, but nothing that was
deliberately kept out of it — a local settings file, a credential,
anything a `.gitignore` was written to exclude. Checked out fresh, a
worktree can be missing a file the first checkout has always had, and
nothing tells the agent working inside it that anything is absent,
because there is nothing there to compare against.

A `WorktreeCreate` hook closes that gap on its own: matched to the
trigger, it copies the handful of untracked files a session actually
needs into the new folder the moment it is created, rather than
leaving an agent to discover the gap by hitting it. That matters most
where several worktrees are running at once, one agent editing each —
a workflow with no `WorktreeCreate` hook needs a person copying the
same handful of files into every new folder by hand, and a person is
exactly what a hook is for replacing.

```
{
  "hooks": {
    "WorktreeCreate": [{
      "hooks": [{
        "type": "command",
        "command": "./hooks/seed-worktree.sh"
      }]
    }]
  }
}
```

## What a departing worktree might be holding

`WorktreeRemove` sits on the other side of the same folder's life. A
worktree due for deletion can still hold uncommitted work — the reason
it existed in the first place, if it was set up so several agents
could edit different sections of one file at once without colliding.
A `WorktreeRemove` hook can check for exactly that before the removal
proceeds, and refuse it outright where the check comes up dirty, the
same refusal `PreToolUse` uses on an edit rather than a deletion. It
is the same question *PostToolUse and FileChanged* asks about saving
a file, aimed at an entire folder instead of one.

```
{
  "hooks": {
    "WorktreeRemove": [{
      "hooks": [{
        "type": "command",
        "command": "./hooks/guard-removal.sh"
      }]
    }]
  }
}
```

Losing a worktree by accident is losing work with no undo — the
folder is gone, not archived — which is the one case in this part
where a hook is not adding a safety net so much as being the only one
available at all.

---

That is Hooks. Plugins come next — the same agents, skills and hooks
you have just built, packaged so they travel to another project, or
another machine, without being rebuilt from nothing each time.

Press `n`.

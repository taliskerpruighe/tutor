# Level 1

## This Wiki

~ This version
  ~ Whats new
  + Whats next
    + Level 3: Automation and integration
      + Teaches how to plug claude code into anything, and have it run by itself
      + Covers databases, MCPs, LSPs, APIs, external hooks, channels, and agent sdk
    + Level 4: Machine learning
      + Teaches how to have claude code train and improve agents--by itself
      + Covers cloud computing and sessions, remotes, cron, loops, goals, and basics of machine learning 
    + Level 5: Business applications
      + Teaches how to put everything into practice
- About this wiki
- Changelog
- How to read this
- The companion agent
$ Exercises

## TUIs

### Terminals

- What a terminal is
- GUI and TUI
- What CLI, command line and prompt mean
- The terminals people use

### Ghostty
~ Your terminal is Ghostty
- What was set up for you
+ [insert crash course on main features]
  + tabs and splits
    + opening, closing, cycling tabs
    + splitting a pane and moving between splits
  + the config file
    + where it lives and how to edit it
    + reloading without restarting
  + keybindings
    + the defaults and how to see them
    + remapping one
  + themes and appearance
    + built-in themes
    + font and cursor tweaks
  + the quick terminal
    + summon it from anywhere with a hotkey
  + image support
    + why pictures render inline here
    + name the kitty graphics protocol

+ ### Tmux

+ [insert crash course on main features]
  + the prefix key
    + what it is and how to change it
  + sessions
    + starting, naming, listing, killing one
  + windows and panes
    + splitting a pane
    + moving between panes and windows
  + detaching and reattaching
    + the core trick, one command each way
  + the config file
    + .tmux.conf, common tweaks
  + copy mode
    + scrolling back and grabbing text
  + status bar
    + reading it, customizing it

### Shells

- What a shell is
- Why the shell is powerful
- The shells there are

### Zsh
~ Your shell is zsh
- Moving around
+ [insert crash course on main features]
  + make sure to include, if not already included
    + cd/..
    + zoxide
    + exporting permanent variables
    + globbing
    + grep
    + ripgrep
    + fzf

### Command Lines and Prompts

- Your prompt
$ Starship and powerline themes
+ Powerline themes
  + explain what they are
  + explain how they are useful
    + can show where you are in your computer, or even in a remote computer
      + provide some examples here
    + for coding purposes, can show things like git status
      + provide some examples here
    + for noncoding purposes, can show things like file status
      + provide an example in a database or a dataset here
      + provide an a google drive example for law here 
  + talk about powerline 10K being famous for zsh, but losing support
  + talk about starship being the modern replacement

+ Starship
  + [insert crash course on main features]
    + what it shows out of the box
      + directory, git branch, command duration
    + the config file
      + starship.toml, where it lives
    + presets
      + picking a preset instead of building one
    + modules
      + turning segments on and off
      + adding a custom one
    + installing it
      + one command, works in any shell

## Software

### Packages

- Every app is a wrapper
- Packages
- Package managers

### Homebrew

- What Homebrew is
- Formulae and casks
- Checking and updating

## Files

### Languages and Scripts

- What a programming language is
- Why plain text wins
- The formats you will meet

### Editors

- IDEs
- Editors in the terminal

$ ### Version Control

$ What git is
$ How git works
$ jj
$ GitHub

## Linux

### The world runs on linux

- What Linux is
- The world runs on Linux

### Why its better

- Why it is better
- You are the system

## Agentic AI

### LLMs

- What an LLM is
- What makes one model different from another
- The models there are
- What a model consumes

### Harnesses

- What a harness is
- The harnesses there are
- What a harness consumes

### Cloud Computing

- Renting a computer
- What you do with a box

# Level 2

## Claude

### Claude

- The models
- The harnesses

### Claude subscriptions

- The plans

### Claude Code

- Why Claude Code
- What it can do that the others cannot

### Claude Code setup

- Installing
- Launching Claude Code
- The .claude directory
- Inside .claude
- More .claude directories
- What a session sees
- Location matters

## Instructions

### The CLAUDE.md File

- The CLAUDE.md file
- CLAUDE.md tips

### Rules

- Rules
- Rules tips

## Agents

### Context

- What an agent is
$ Tabs and windows
- Context
- Context rot
- Managing context
+ ccstatusline
  + cc comes with its own builtin status line
  + the boss says: the builtin status line is dogshit
  + the boss recommends: the ccstatusline by sirmalloc (give the gh repo here)
  + infinite cofiguration and customization; ask an agent to know whats possible
  + the boss recommends a configuration that shows, at a minimum, context and permission modes

$ Moving between folders

+ ### Plans and Permissions

+ changing permission modes
  + you will see a "mode" at the bottom of interactive sessions
  + that is the permission mode, which is basically how often you need to manually approve commands agents try to run
  + you can change it manually with shift+tab
  + you can also ask an agent to set your default permission mode in your global settings
  
+ types of permission modes
  + default/manual mode: asks approval for most edits
  + accept edits: skips asking, except for edits to claude assets/settings
  + auto mode: skips asking based on criteria and judgment calls
  + bypass permissions: never asks anything
  + plan mode: a read-only mode used to plan a task

+ the boss recommends: auto mode
  + the boss recommends: set your default permission mode to auto mode
  + ask an agent to set it for you  
  + ask an agent to create an autoMode.environment setting for you in your global settings.json
  + tell it in plain english what kinds of files, or locations, you want to be careful with an have claude code ask for permission before doing certain things, like deleting
  + use this for sensitive files that you are not tracking with version control (*like git) or cloud storage (like google drive)

+ the boss recommends: plan mode
  + one feature that sets coding harnesses apart
  + originally meant for software development, given that so many different files depend on each other
  + but improves the efficiency and effectiveness of agents exponentially--especially later on when coordinating multiple agents, like subagents and workflows
  + turn plan mode on whenever you ask an agent to do something that takes several steps, like research then write or write then test: it will be worth it

+ ### Prompts

+ Prompt dos and donts
  + party trick #N from the boss: give objectives, not instructions--but in pieces
    + bad: giving quality targets, like "fix the code" or "make this sound like me"--at least without a battle-tested skill (more on that later)
    + good: give specific objectives, milestones, or benchmarks to test against
      + "fix the code until you see the columns align when the window opens"
      + "make this sound like me until another agent cannot tell the difference from this sample"
    + best: give context, instructions, and traps

+ prompt engineering
  + context: why the task
    + if there is a history or a goal for the agent to keep in mind, put it here
    + if there is stuff for the agent to read, research, or consider first, also goes here
  + objectives
    + this is where you list your instructions, but again as objectives
    + try to break down objectives and put them chronologically
  + traps
    + things the agent must avoid

+ long prompts
  + for longer prompts, hit control+g to edit the prompt in your default text editor
    + mention that you can change the default text editor in the global settings.json
  + in long prompts, use headings starting with #, ##, and ### to separate things

+ shorthands and key words
  + you can create shorthands or key words to use in prompts, and have claude code know exactly what you mean
  + just ask an agent to help you set any with a persisitent env setting in your settings.json, global or local
  + these work like variables in shells: you set any word to mean any thing you want, and claude code knows automatically
    + one common example is folder or file names that you use often
      + give some examples here
    + another common example is instructions you type often, but not every time
      + give some more examples hre
  + the boss recommends: have claude code set your env variables to work with $ in front, so that they do not get mixed up with regular text
+ The advisor tool
  + give the setting: advisorModel: "<model>"
  + the boss recommends: set it to Opus
  + note from the Boss: dual edged sword
    + very good to catch mistakes and have agents course correct before delivering something terrible
    + slow and expensive: agents call it way too often, including for basic things like reviewing basic searches

### Custom Agents

- The default agent
- Custom agents
- The definition file
- The fields that matter
+ Output styles
  + what they are: change how the agent to talk to you in an interactive session
  + you can ask the agent to structure replies in specific ways, like asking for headings, diagrams, etc
    + give some practical examples here
  + does not apply to anything else: subagents, noninteractive sessions, etcj
- Building one

## Skills

### When To Build One

- Start with never
- What a skill is
- The frontmatter
- The body
- Supporting files

### Building One

- How to build one
- Start with examples
- Iterate with corrections
- Building your first skill

### Making Them Fire

- How skills work
- Always invoke manually
- Reading your own prompt

## Subagents

### Chains

- What a subagent is
- Chain engineering
- Out of the box
- Designing a chain
- The door

### Build a Chain

- Step one — the project
- Step two — the workers
- Step three — the door
- Step four — run it
- Step five — watch it

## Workflows

### What They Are

- What a workflow is
- What they buy and what they cost
- When to use one
- Sessions that survive

### Building One

- How to build a workflow
- Making it thinner

+ ## Version Control

+ ### Git, Github, and Jujutsu
+ git
  + what it is
    + version control software
    + invented by the guy who invented linux
  + used mainly for code--so people assume thats all it can do
  + but it can do so much more in any field--especially when combined with coding harnesses
    + give examples here
    + one example can be how something like google drive only has the latest "sync'd version"--not all priors
  + if nothing else, the boss says this: its absolutely essential to use to insure against ai agents' trigger happiness with edits

+ how git works
  + repos
  + branches
  + tracking vs ignoring
  + staging
  + commits
  + fetch, push, pull: git remotes
    + multiple options, not just github online
    + for example, a server or external hard drive 

+ github
  + what it is
    + how it differs from git
    + how it works with git: as the remote/the backup
  + how its an absolute gold mine of scripts and software that ai can find and use to transform your life
    + give some examples here outside of software, like legal, data, business

+ jujutsu
  + what it is
    + how it differs from git
    + how it works with git: colocation
  + jj working copies
  + jj "saves" upon commands

+ git, github, and cli harnesses
  + how a lot of cli harnesses are built to work with git
  + making a folder/project a repo unlocks all kinds of features to supercharge the harness
    + being able to easily track changes--and change history
    + being able to have multiple agents work on the same file at once
    + building multiple versions of the same file, cherry picking the best pieces across all of them, and easily merging them into one

+ ### Worktrees

+ worktrees
  + what they are
  + how they work in cc
    + for a main agent, you can start a session at a worktree
    + for a subagents, easiest is to set isolation: worktree in the frontmatter
  + dont use it if your agents work sequentially: writer then editor then formatter
  + use it if your agents work on the same file at once: one writer for section 1, one writer for section 2 

+ forking
  + what it is, and how it differs from non forked subagents
  + dont use it for tasks that you want to break down because of context or because of specialization from different agents
  + use it if you want a second opinion or a parallel approach
    + give some examples of either scenario## tool tips


## Hooks

### What They Are

- What a hook is
- The triggers
- Scoping a hook

### Using Them

$ Worked examples
+ SessionStart/SubAgentStart examples
  + Injecting additional context not covered by Claude.md
    + Elaborate on a practical example and how it helps
  PreToolUse examples
    + Making sure an agent invokes the right skill before doing anything
      + Same: elaborate 
+ PostToolUse/FileChanged examples
  + Making sure a git or jj operation happens to "save" the file
    + Same: elaborate
+ SessionEnd/SubagentStop example
  + Making sure the agent did what it was supposed to do by checking the transcript for certain skills, files, commands
  + Same: elaborate
+ CwdChanged/DirectoryAdded examples
  + Having the agent read local claude.md's, settings, or rules
    + Same: elaborate
+ WorktreeCreate/WorktreeRemove examples
  + Examples of what all it could do here

## Plugins

### What They Are

- What a plugin is
- When to make one
- What is inside one

### Using Them

- How a plugin works
- Building one
- Exercises

## Headless Sessions

### Running Without a Chat

- What a headless session is
- When to use one
- Piping
- Watching

## Counter-Recommendations

- Builtin agents
- Background sessions and agent view
- Subagents spawning subagents
- Agent teams

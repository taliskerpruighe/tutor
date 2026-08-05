# Level 1

## This Wiki

- About this wiki
- This version
- Changelog
- How to read this
- The companion agent
- Exercises

## TUIs

### Terminals

- What a terminal is
- GUI and TUI
- What CLI, command line and prompt mean
- The terminals people use

### Ghostty

- Your terminal is Ghostty
- What was set up for you

### TMUX

- What tmux is
- What it is for

## The CLI

### Command Lines and Prompts

- Your prompt
- Starship and powerline themes

### Shells

- What a shell is
- Why the shell is powerful
- The shells there are

### Zsh

- Your shell is zsh
- Moving around

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

### Version Control

- What git is
- How git works
- jj
- GitHub

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
- Tabs and windows
- Context
- Context rot
- Managing context
- Moving between folders

### Custom Agents

- The default agent
- Custom agents
- The definition file
- The fields that matter
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

## Hooks

### What They Are

- What a hook is
- The triggers
- Scoping a hook

### Using Them

- Worked examples

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

# PIPELINE

## Gizmos

### Version Control

+ git
  + what it is
    + version control software
    + invented by the guy who invented linux
  + used mainly for code--so people assume thats all it can do
  + but it can do so much more in any field--especially when combined with coding harnesses
    + give examples here
    + one example can be how something like google drive only has the latest "sync'd version"--not all priors
  + if nothing else, the boss says this: its absolutely essential to use to insure against ai agents' trigger happiness with edits 

+ github
  + what it is
    + how it differs from git
    + how it works with git: as the remote/the backup
  + how its an absolute gold mine of scripts and software that ai can find and use to transform your life
    + give some examples here outside of software, like legal, data, business

+ git, github, and cli harnesses
  + how a lot of cli harnesses are built to work with git
  + making a folder/project a repo unlocks all kinds of features to supercharge the harness
    + being able to easily track changes--and change history
    + being able to have multiple agents work on the same file at once
    + building multiple versions of the same file, cherry picking the best pieces across all of them, and easily merging them into one

### Worktrees

+ worktrees
  + what they are
  + how they work in cc
  + set isolation: worktree at the agent level
  + dont use it if your agents work sequentially: writer then editor then formatter
  + use it if your agents work on the same file at once: one writer for section 1, one writer for section 2 

+ forking
  + what it is, and how it differs from non forked subagents
  + dont use it for tasks that you want to break down because of context or because of specialization from different agents
  + use it if you want a second opinion or a parallel approach
    + give some examples of either scenario## tool tips

### text editors
- micro
- nano
- hx
- vim
- neovim
- emacs

### zsh
- mv
- cp
- rm
- grep
- ripgrep
- xozide
- fzf
- glob
### yazi
- tui for files
- easier if you are having trouble with file management on the command line
### broot
### btop
### tmux
- panes to split
- panes to follow/mirror
### git
- what git is
  - version control
  - differences from github
- how it works
  - git staging
  - git commits
  - git diffs
  - git pushes/pulls
### jj
- what it is
  - version control
  - colocated
- what it does
  - working copies
  - snapshots
  - no more staging
### gh
- what it is
- how it works
- additional files
  - agents.md: technically what claude.md is, except claude.md reads automatically
  - readme.md: for people

### ccstatusline 
   - much better than the bultin stuff
  - ask cc to install and configure
  - run thru the options to see what is available
  - like a powerline, it takes any custom command
 
## other gimmicks
- themes
- output styles
- rewinding
- permissions
- prompt engineering
  - use control+g
  - headers
- permissions
  - plan mode
    - the boss recommends: use liberally
    - explain what it does
    - party trick: create a / command that you can use anywhere, and have it do only two things: enter plan mode and run in xhigh effort; if you ever need anything plan, run it at the start of the prompt (eg, "/plan-this [prompt]")--which is two birds
 
- the advisor
- give the setting
- say set it to opus
- note from the Boss: dual edged sword
  - very good to catch mistakes and have agents course correct before delivering something terrible
  - slow and expensive: agents call it way too often, including for basic things like reviewing basic searches

## git in cc
- forking
- worktrees

## convo management

- rewinding

# Level 3+
- agent memory
- cron
- loop
- goals
- remotes
- cloud sessions
- all things cloud computing
- machine learning
- mcps
- lsps
- apis

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

+ ## Counter-Recommendations

+ Builtin agents
  + explain how cc ships with builtin subagents
    + explain what they are 
  + the boss recommends: turn them off
    + give the setting to put in the global json
  + explain how they are not worth using
    + they are too dumb: you can make your own that does the same thing
    + your main agent calls them too often--even when its much easier for the main agent to just do whatever by itself
+ Background sessions and agent view
  + explain the features: /bg or --bg, agent view to watch agents in a dashboard
  + the boss recommends: dont use
    + give her the setting to put in the global json
  + explain how they are not worth using
    + sounds good in theory
    + but background sessions take way more resources (cpu, ram) than headless sessions
    + the agent view itself is its own process that eats up resources
    + not as user friendly as it seems
+ subagents spwaning subagents
  + explain how subagents can spawn their own subagents--up to 5 levels of subagents
  + the boss recommends: dont use it
    + make dedicated custom agents to operate only as subagents, not as main agents
    + remove the Agent tool from those dedicated subagents--so they cant spawn infinitely
  + explain why it sucks
    + hard to see/control: subagents can get wild with cost and scope of what they do
    + bugged: when a subagent spawns a second subagent and the second sugagent finishes, the main agent thinks that its the first subagent that finished--or vice versa
+ agent teams
  + explain the feature and how it differs from regular subagents: agents talking to each other
  + very promising; plus the visibility with tmux panes
  + but the boss recommends: turn if off
    + give the global setting to turn it off

# PIPELINE

## tool tips

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


# Level 1: Setup

[certain things in this level are going to be introduced, but not taught. they may say things like full course later or full course distributed. that means there should be an introductory article or two here, and then the remainder of articles--for an agent to outline and write--teaching the tool over time should be spread out across remaining levels as the tool becomes more useful in conjunction with those levels (e.g., introducing zsh in level 1, then teaching zsh basic navigation when teaching where to launch claude from in level 2)]

## This Wiki

- Basics
  - Crash course for noncoders
  - Based on the Boss' biases and hard learned lessons
- Version
  - What this version adds
- Changelog
  - Full changelog from prior versions
- Moving around
- Companion agent: claude launched from the tutor/ directory
- Exercises

## TUIs

### Terminals

- what a terminal is: terminal emulator and the history/why its called that
- gui vs tui
- what is meant by cli
- what is meant by command line and command prompt
- popular terminals and their features: i2, wezterm, alacritty, kitty, ghostty

### Ghostty
- your terminal is ghostty
- why ghostty
- [full course distributed]

### TMUX

- what it is
- use cases: insuring/restoring sessions, mirroring, projecting, panes, layouts, etc
- how to use it: full course
  - prorated over levels

## The CLI

### Command Lines and Prompts

- what the command line is
- the fact that it can display anything
- powerlines and custom theme managers
  - examples: powerline 10K, starship [full course]

### Shells
- what a kernel is
- what a shell is
- what a shell can do
  - how its much faster and much more powerful than clicking around
  - plenty of concrete examples of everyday workflows
- common shells: bash, zsh, powershell
- newer specialized shells: fish for user friendliness, nushell for structured data

### Zsh
- your default shell is zsh
- full zsh course spread throughout

## Software

### Packages

- how all apps are lies: its all code at the end of the day
- apps are a bunch of code behind a veil, a pay wall, an installer, and a log
- enter packages: on a terminal, you can run anything
- common examples of packages replacing common paid apps (email, word, excel, adobe for pdf, etc)
- package managers in general
- package manageres on linux: dnf, apt, pacman, etc
- package manager on mac: homebrew

### Homebrew
- what it is
- basics of brew/casks/packages
- how to quickly check
- how to quickly update

## Files

### Languages and Scripts
- what programming languages are and how they differ from shells
- some common examples
- machine readable types of files (e.g., .md and .txt, .json and .jsonl) and how they are better than human readable types of files (e.g., .doc and .xls)
- machine readable extension (e.g., parquet) and component (e.g., yaml) examples

### Editors

- ide's: what they are 
- examples: vscode, jetbrains
- more for software developers
- text/tui editors
- examples: micro, nano, helix, vim, neovim, emcas

### Version Control

- git
  - what it is
  - how it works
  - full course distributed
- jj: same
- github: how it differs from git/jj
  - full course thruout as well

## Linux

### The world runs on linux
- Most servers, cell phones
- even claude.ai and claude cowork
- and why: linux is to operating systems what packages are to apps

### Why its better
- you are the system: with ai, infinitely customizable
- provide ample actual examples of what it can do that windows and macos would lock

## Agentic AI

### LLMs
- what an llm is
- how it works
- speciality: moe vs dense
- capability: size
- examples of llms
  - proprietary/cloud only llms: claude, gpt, gemini, etc
  - open source llms: llama, mistral, deepseek, kimi, qwen
- what it consumes: vram
- so while open source models are free, most personal computers do not have enough vram to run one locally

### Harnesses

- LLM is the brain, harness is the body
- what a harness is/how it works
- the harness as the body
- examples of online harnesses
- examples of desktop/gui harnesses (like antigravity)
- examples of cli/tui harnesses: qwen code, kimi code, opencode, and claude code
- what it consumes: cpu and ram
- so while most big models can handle almost anything, most personal computers do not have enough cpu and ram to run multiple agents locally

### Cloud Computing

- to get around hardware limitations, cloud computing
- available mainly from amazon, google, and microsoft
- you pay by the hour to run computer sitting in a data center, colloquially a "box"
- you install what you need to install, like llms, harnesses, and packages, run what you need to run, and download just the result
- almost all boxes run linux and are terminal only (no gui desktop)
- that used to require shell knowledge; now ai running in your computer can do the driving for you

## Claude

### Claude

- LLMs
  - Haiku (estimated parameters, 200K context)
  - Sonnet (same, 1m context)
  - Opus (same, 1m context)
  - Fable (same, 1m context)
- Harnesses
  - what claude.ai is
  - what claude cowork is
  - what claude code is

### Claude subscriptions

- free, pro, max 5x, max 20x
- the savings are actually exponential: max 5x and 20x are several more multiples of usage per dollar than pro
- will need max 5x or 20x to run most advanced features in claude code
- 5x is a good starting point; 20x for heavy models like fable or heavy usage like workflows

### Claude Code 
- how claude code differs from the other two
- what claude code can do that the others cannot
  - can use your software: finds and pulls the best, fastest, and free packages--while something like cowork runs on a vm with its own sandbox
  - can use your hardware: get a better computer, and claude code can run a script on overdrive--while something like claude cowork is limited to a vm with 4 cores (make a point thats half the size of a 2020 M1 Macbook Air)

### Claude Code setup
- installing [current article is fine]
- launching [current article is fine]
- .claude directories [current article is fine]
- what a session sees [current article is fine]
- location [current article is fine]

# Level 2: 

## Agents

[current content under agents is fine]

## Skills

[current content under skills is fine]

## Subagents

[current content under subagents is fine]

## Workflows

- what they are
  - works like subagents, but scripted
  - instead of a main agent that you can talk to calling subagents, a script calls every agent
  - you cannot interact with any of the agents in the pipeline: the script gives them their prompts
  - workflows live in the .claude/ directory alongside agents, skills, etc
  - workflows can "see" the same agents, skills, etc that agents can

- pros and cons
  - the upside of workflows is consistency and quality control: the script forces agents spawns and order, so nothing gets skipped
  - the downside of workflows is bloat: they are slow and expensive
    - it takes longer for the same agent to start and stop in a workflow than as a regular subagent
    - because workflows always involve way more agents than a typical subagent chain, the cost adds up fast
  
  - that means: use workflows when there are multiple pipelines of the same task
    - example 1: read, summarize, and review the summary of 10 different books
      - to manage context, you may need to send 8 agents to read each book, 4 to summarize, 2 to review summarie
      - if you make each book a subagent chain, you are asking the main agent to manage 14 subagents--which may blow the agents context
      - even if not, that would be 10 separate sessions, one per book, using 10 identical prompts
      - a workflow is one pipeline that you can run 10 times over--or 10 times at once, if you have the power--with no management required
  
- how to build workflows
  - always ask claude: do not attempt to build by hand
  - ask the main agent to build a workflow in the same way you ask it to build a chain of subagents
  - the main agent has a special effort level called "ultracode" meant to write and manage workflows: hit /effort and select ultracode before asking the main agent to write the workflow

- dos and donts
    - do not trust claude blindly: it will try to sell you on 10 times as many agents as you need, all of the highest cost
    - ask claude to suggest a workflow, then push back and ask how it can be made thinner
      - start with the number of agents: ask claude how to make it fewer
      - then push back on the models: ask claude which agents can be downgraded into lower models or, even better, just parts of the script that do not require an llm

## Hooks

- what they are
  - hooks are script triggers
  - they are the only way to actually force claude agentic behavior: all else (skills, prompts) are technically optional
  - hooks can be used in a variety of ways, but the most useful way is: as your subagent chains and workflows grow, you lose visibility into what agents are doing--so you need hooks to make sure they do what they are supposed to do

-types of hook triggers
  - knowing these gives you an idea of when to ask claude if a hook would make a difference 
  - several, but most useful:
    - SessionStart: fires when you launch claude
    - UserPromptSubmits: fires whenever you send a message
    - PreToolUse: before claude uses a tool
    - PostToolUse: after claude uses a tool
    - SubagentStart: when a subagent spawns
    - SubagentStop: when a subagent finishes
    - Stop: when claude finishes responding
    - SessionEnd: when a claude session closes

- how hooks are hit harder
  - like with everything else, customization is key
  - hooks can be restricted to a specific setting: they can be limited to certain agents, certain plugins, or certain projects
  - if you want to have just a few custom agents behave a certain way, use a hook instead of changing your claude.md

- useful examples
  - SessionStart: tell a specific custom agent to ignore part of your claude.md, or to follow special rules for that particular project
  - UserPromptSubmits: remind your agent to respond in two languages
  - PreToolUse: if the tool is Write, Edit, or Bash, make sure the file is already committed to git
  - PostToolUse: if the tool is Write or Edit, fire a subagent to review what was written
  - SubagentStart: preload a skill for that subagent
  - SubagentStop: make sure the agent actually used the desired skill in the middle of a large workflow
  - Stop: have claude re write the answer if it blew a word limit
  - SessionEnd: have claude save the session transcript in a special folder

## Plugins

- what a plugin is
  - easiest way to think of it: a remote, portable .claude/ directory
  - instead of writing assets into a project's .claude directory, you write it into a normal folder
  - but then you can install and deploy that folder in multiple projects, your entire machine, and even someone else's machine
- when to make one
  - when you need a suite of assets, but not very often--and dongentswant it cluttering/slowing down other agents
    - [insert examples]
  - when you need a suite of assets in two repos on the opposite side of the tree, but not higher up on the tree
    - [same]
  - when you want to save a suite of assets after using it for a single project
    - [same]
  - when you want to share a suite of assets
    - [same]
  - best use case: when you want to continuously improve a single piece of plumbing shared by multiple projects
    - example 1: a voice agent: you wrote an agent to sound like you, with a skill to write like you and skill to send emails for you, which you want to be working on work projects and personal project--but want to to continue to ::iterate it with new examples of your voice every day
    - [more examples]
- what it contains
  - a normal directory
  - but it looks like the inside of the .claude directory
  - contains any of the following 
    - agents
      - custom-agent-1
    - skills
      - custom-skill-1
      - custom0-skill-2
    - commands [note from the Boss: commands are now obsolete, theyre just skills]
    - hooks
      - hook-1.sh
    - mcps
      - whatever
    - settings.json
      - make a point that this is the place to override global settings
    - .claude-plugin/
      - claude writes this, but this is what makes the folder a plugin
    - [one or two full examples should follow]

- how it works
  - needs the claude-plugin/plugin.json manifest
  - needs to be in the global marketplace json
    - explain the marketplace json
  - installation: global/user or project/folder
  - enable/disable: same (in the global or project settings)
  - update
    
- how to write one
  - always ask claude

- exercises 

## Headless Sessions

- what they are
  - with claude code, you can run claude without starting on chat
  - a headless session is a session that you launch on your terminal with the flag --print, or just -p, and type the prompt directly
  - the session runs in the backgroun of your shell "non-interactively": it just delivers the outcome

- when to use
  - quick jobs that do not require back and forth:
  - established pipelines
    - battle tested subagent chains: instead of launching a main agent in a chat, invoking a skill to start a bunch of subagents, and having that chat open, launch the main agent headlessly, and the subagent chain runs from start to finish 
    - workflows: launch a headless agent to run a workflow and babysit it
    - piping
      - [the zsh part on piping needs to be in this 'chapter']
    - party trick #N from the boss: use your shell to "watch"
      - ask claude to build you realtime scripts of all subagents in a headless session

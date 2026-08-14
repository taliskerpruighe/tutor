# Level 1

## This Wiki

- This version
- About this wiki
- Changelog
- How to read this
- The companion agent

## TUIs

### Terminals

- What a terminal is
- GUI and TUI
- What CLI, command line and prompt mean
- The terminals people use

### Ghostty
- Your terminal is Ghostty
- What was set up for you

### Tmux

- The prefix key
- Sessions
- Windows and panes
- Detaching and reattaching
- The config file
- Copy mode
- The status bar

### Shells

- What a shell is
- Why the shell is powerful
- The shells there are

### Zsh
- Your shell is zsh
- Moving around
- zoxide
- Permanent variables
- Globbing
- grep
- ripgrep
- fzf

### Command Lines and Prompts

- Your prompt
- Powerline themes
- Starship

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
+ Running one yourself
  + *What a model consumes* ends "it will not do what you are about to
    see" — this article is the answer to that line, and belongs here
    rather than in a part of its own
  + Ollama: a program that runs models, installed as a background service
  + it listens on a local address and serves an API there
  + models are pulled by name and run by name
  + the escape from the VRAM ceiling — Ollama also serves *cloud* models,
    run on its hardware, reached through the very same local address
  + so the open-weight models named two articles ago are reachable after
    all, on a laptop, without the 24 GB card
  + do not explain what a harness would do with this yet; Level 2 does that

### Harnesses

- What a harness is
- The harnesses there are
- What a harness consumes

### Cloud Computing

- Renting a computer
- What you do with a box

# Level 2

## Claude

### The Claude Code Harness

- Why Claude Code
~ The harnesses
  ~ moved out of the old opening section and rewritten as a *follow-up* to
    *Why Claude Code*, not a lead-in to it
  ~ she now knows what Claude Code is before she is shown the alternatives,
    so this article contrasts rather than introduces
  ~ claude.ai in a browser and Claude Cowork in a sandbox, each measured
    against the one she is actually going to use
  ~ the axis that matters stays what it was — whose machine it runs on, and
    what that lets it reach
  ~ do not re-explain what a harness is; Level 1 did that
- What it can do that the others cannot

### Claude Models

~ The Claude models
  ~ retitled from *The models*, because a part called *Other Models* now
    follows and the old title no longer says which models it means
  ~ same content: Haiku, Sonnet, Opus, Fable, and what each is for
  ~ it now sits *after* the harness section rather than opening the part,
    so it can name Claude Code freely instead of holding it back
- The plans

$ What a subscription does not buy
  $ deleted as an article of its own
  $ its one live argument — a tier buys access and headroom, not a fixed
    quality — moves into *Pointing the harness elsewhere*, where it is the
    motive rather than a standalone complaint
  $ nothing else in it survives

## Other Models

### Running Other Models

~ Pointing the harness elsewhere
  ~ generic to any non-Claude model; nothing Ollama-specific in it
  ~ **this part now sits before *Claude Code Setup*, so nothing here may
    assume `.claude`, settings files, agents, skills or context management.
    Teach the redirect with inline shell variables only, and say plainly
    that the permanent home for them comes later.**
  ~ the opening: Level 1 taught that the harness and the model are separate
    things reached over a connection; the address of that connection is a
    setting she can change
  ~ ANTHROPIC_BASE_URL is the address; ANTHROPIC_AUTH_TOKEN the credential
  ~ point the first somewhere else and the harness goes there — anything at
    that address speaking the same API answers
  ~ the address is the root of whatever the provider gives her, and a
    stray /v1 is the single likeliest typo; each provider's own page is
    what settles the spelling
  ~ set them inline, in front of the command, for one run — that is the
    safe way to try it and needs nothing she has not been taught
  ~ one forward-looking sentence and no more: there is a permanent home for
    these in the next part, once she knows what `.claude` is
  ~ the motive, inherited from the deleted subscription article: a plan buys
    access and headroom, not a fixed quality; the same work can go well one
    week and badly the next with nobody to ask and nothing to appeal to,
    and being able to change the model is what turns that from a thing
    endured into a thing decided
  ~ name no mechanism for that variance — this repository is public and
    nothing sourced here supports a claim about the cause

~ What you give up
  ~ generic to any non-Claude endpoint; the provider-specific losses live
    in each provider's own section
  ~ a short factual list and nothing more: prompt caching ignored,
    tool_choice gone, token counts approximate, no PDFs, no image URLs, no
    batches, no citations, thinking budgets accepted and not enforced
  ~ what survives: streaming, system prompts, multi-turn, tools and tool
    results, vision, thinking, the permission flow, file edits
  ~ the sentence that matters, now written as a **promise about what is
    coming** rather than a callback to what she has read: almost everything
    this course is about to teach her — instructions, agents, prompting,
    skills, subagents, hooks, plugins — sits on the harness side and works
    the same whichever model is answering
  ~ name those as things she has not met yet, so the article does not
    depend on them
  ~ the loss with teeth is the approximate token count, and it should be
    stated flatly here and picked up again when context is taught

### Ollama

~ Signing in
  ~ *Running one yourself* in Level 1 already installed it and explained the
    daemon; this picks up from there
  ~ local models need no account at all
  ~ cloud models need an ollama.com account: ollama signin
  ~ the daemon authenticates the forwarded request itself, so the account
    lives there and the harness still sends a meaningless token
  ~ name the model with a :cloud suffix and nothing else changes
  ~ ignore OLLAMA_API_KEY: a different route, for scripts, not this one
  ~ the Anthropic subscription is not in play at all — not spent, not
    helping; a separate arrangement with a separate company
  ~ no price and no plan name; check before drafting and name neither

~ Running it
  ~ the shortest article here: the two variables inline, then claude with a
    model name, and the same command with a :cloud name for a cloud model
  ~ then the shortcut — ollama launch claude configures and starts it for
    her; --config configures without starting
  ~ --model skips the selector; --yes is non-interactive and requires
    --model; anything after a bare -- passes through to Claude Code
  ~ **drop the headless one-liner that was here.** Headless sessions are
    taught near the end of the course and she has not met -p; mention that
    the passthrough exists and leave the example for later
  ~ why the shortcut comes second in the article and not first: the
    variables are the mechanism and the mechanism transfers to any provider;
    the subcommand is only a command

~ Choosing a model
  ~ the hard requirement first — it must support tool calling, or it will
    chat pleasantly and never touch a file
  ~ that is the harness loop from Level 1 failing at its one hinge, which
    is the only prerequisite this article needs
  ~ size against the memory actually in the machine, which *What a model
    consumes* already sized for her
  ~ **cut the reference to Opus deciding and Haiku checking** — that is
    *Building one*, several parts away
  ~ the named recommendations of the day, local and cloud, marked as
    examples and not a list to memorise; say in the prose that names date
    faster than anything else here
  ~ one line on the alias trick for tools demanding real Anthropic model
    names; Claude Code does not need it

~ Context length
  ~ **the context window has not been taught yet.** Give it two sentences
    here — a model can only hold so much at once, and everything the
    session touches goes into that room — and say the subject is coming
  ~ then the number that does the work: Ollama defaults to 4k on a small
    machine, where the Claude models she has just read about carry 200k
    and 1M
  ~ a session is not empty before she types; instructions and tool
    definitions are already in the room
  ~ so at 4k the harness is finished before the first prompt, and this is
    the likeliest reason a correct setup looks broken
  ~ agents and coding tools want 64k or more; raise it when serving
  ~ check what was actually allocated, and whether the model was pushed
    onto the CPU
  ~ cloud models default to their maximum, so this is a local-model problem
  ~ leave a hook for the Agents part to pick up rather than teaching
    context rot here

~ When Ollama breaks
  ~ ordered by likelihood, not severity
  ~ nothing happens, or files are never edited: no tool calling
  ~ out of context immediately: the 4k default
  ~ connection refused: the daemon is not running
  ~ a cloud model is refused: ollama signin was never run
  ~ web search does nothing even on a local model: Ollama's web search
    wants an account too, which a purely-local reader will not have
  ~ a /v1 on the base URL: this wire is served from the root
  ~ **drop the settings.json failure mode** — she is setting these inline
    at this point in the course, so the global-versus-project trap does not
    exist for her yet
  ~ the model is weaker at the task: try another, the swap is one word

### Kimi

~ Kimi as an endpoint
  ~ the second worked example, deliberately the opposite shape to Ollama —
    no daemon, nothing on her machine, a paid cloud API over the internet
  ~ so the pattern generalises: the redirect is one address, and what sits
    at that address is somebody else's problem
  ~ Moonshot serves two wires; the Anthropic one is what Claude Code wants
  ~ the address ends at /coding/ with no v1, because the SDK appends the
    rest itself
  ~ a sister tool uses /coding/v1 on the same host — same machine,
    different protocol surface, and copying one into the other fails
    quietly
  ~ note that Kimi Code is Moonshot's own harness and is not the subject;
    she is keeping her harness and changing her model

~ Keys and membership
  ~ a paid Kimi membership with the coding benefit activated is the
    precondition, not an optional upgrade
  ~ keys are made in a web console, capped at five, and shown once — copy
    it then or make another
  ~ this is a genuine API key, unlike Ollama's meaningless token; treat it
    as a secret, and say what that means for putting it in a file later
  ~ the tier decides which models she may name and how much context she may
    ask for; the two are gated together
  ~ when the subscription quota runs out there is an overflow balance
    billed per use and shared with the web product
  ~ quote no figures — this is a pricing page and it will move

~ Pointing Claude Code at Kimi
  ~ the base URL and a genuine key, exactly the shape from *Pointing the
    harness elsewhere*
  ~ then the part Ollama never needed: naming the model
  ~ Claude Code keeps a slot per model tier and every slot has to be
    pointed at the Kimi model by hand
  ~ the consequence, stated without leaning on anything she has not read:
    every slot ends up on one model, so the three Claude models she met two
    sections ago stop being three
  ~ **there is a subagent slot in that list; name it as a term coming
    later** rather than explaining what a subagent is here
  ~ the context ceiling is set by hand too and must match what the tier
    allows
  ~ the 1M form is spelled with a bracket suffix, valid only in this
    setting — carry it into an API call or another tool's model field and
    it breaks
  ~ the documentation also prints a pre-launch script that edits a file
    inside `.claude`; **she has not been shown that folder yet**, so either
    defer the script to a pointer forward or show it with an explicit "this
    is covered in the next part" and a warning to read it before running it

~ Thinking and effort
  ~ effort levels do not map one to one: five on Claude Code's side land on
    three on Kimi's, so two pairs are indistinguishable upstream
  ~ the trap worth the whole article — turning thinking *off* does not give
    her the same model without thinking, it silently routes to an older,
    cheaper model, and she is billed for the answer
  ~ a reply arrives, it looks fine, and it is not the model she asked for
  ~ so on this endpoint, thinking stays on

~ When Kimi breaks
  ~ the display still names a Claude model even when every call is going to
    Kimi — the name is not the check, the base URL is
  ~ the likeliest false alarm in the whole thing, and it cuts both ways:
    she will think it failed when it worked, and think it worked when she
    has fallen back
  ~ a /v1 on the base URL: that is the other wire, for a different tool
  ~ the bracket model form used anywhere but this one setting
  ~ a model or context size the tier does not cover, which the error names
    — with one known spelling inconsistency in it, so do not tell her to
    grep for an exact string
  ~ answers from a model she did not choose: thinking was turned off

## Claude Code Setup

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
- Context
- Context rot
- Managing context
- ccstatusline

### Plans and Permissions

- Changing permission modes
- The permission modes there are
- The boss recommends: auto mode
- The boss recommends: plan mode

### Prompts

- Prompt dos and donts
- Prompt engineering
- Long prompts
- Shorthands and key words
- The advisor tool

### Custom Agents

- The default agent
- Custom agents
- The definition file
- The fields that matter
- Output styles
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

## Version Control

### Git, Github, and Jujutsu

- What git is
- How git works
- GitHub
- Jujutsu
- Git and the harness

### Worktrees

- Worktrees
- Forking

## Hooks

### What They Are

- What a hook is
- The triggers
- Scoping a hook

### Using Them

- SessionStart and SubagentStart
- PreToolUse
- PostToolUse and FileChanged
- SessionEnd and SubagentStop
- CwdChanged and DirectoryAdded
- WorktreeCreate and WorktreeRemove

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

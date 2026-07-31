
# Level 1: Setup

[certain things in this level are going to be introduced, but not taught. they may say things like full course later or full course distributed. that means there should be an introductory article or two here, and then the remainder of articles--for an agent to outline and write--teaching the tool over time should be spread out across remaining levels as the tool becomes more useful in conjunction with those levels (e.g., introducing zsh in level 1, then teaching zsh basic navigation when teaching where to launch claude from in level 2)]

---

**How to read this document.** `##` is a part — a tab along the top of the
reader, one directory under `content/`. `###` is a section — the side tabs
down the left. Numbered entries are articles, one markdown file each,
numbered from 1 within their own section. Bullets under an article are what
that article covers.

Each article carries a tag:

- `[HAVE path]` — written, moves across whole
- `[SPLIT path]` — written, but the article has to come apart because the
  plan files its halves under different headings
- `[NEW]` — nothing written

Sections are kept to nine articles or fewer, because `1`–`9` are the only
keys that jump straight to an article.

---

## This Wiki

**1. About this wiki**  `[HAVE 01-interface/01-about-this-wiki.md]`
- a crash course on Claude Code, for people who do not write code
- built on the Boss's biases and hard-learned lessons, not on a manual
- how it differs from Anthropic's documentation: theirs is the reference,
  this is the Party Tricks — what someone found out by doing it
- gathered from practice, testing, and commiseration with people who hit
  the same problems

**2. This version**  `[SPLIT 01-interface/01-about-this-wiki.md]`
- what this level covers and what it deliberately leaves out
- what the next levels add, and why each assumes the one before it
- REWRITE, not renumber: the written article is organised in release
  numbers (0.1.0 agents/skills/subagents, 0.2.0 hooks/MCP/plugins, 0.3.0
  crons/cloud/ML) and this plan reorganises around levels — and moves
  cloud computing forward into Level 1

**3. Changelog**  `[NEW]`
- what changed in each version before this one
- kept so a reader returning after an update can find the delta

**4. How to read this**  `[HAVE 01-interface/02-how-to-read-this.md]`
- parts across the top, sections and articles down the left
- the key table: `n` `p`, `←` `→`, `⇥`, `1`–`9`, `↑` `↓`, `/`, `?`, `q`
- the mouse works too
- what the formatting means: code, asides, links
- how to reopen it later
- CHECK: its "Where to start" list names Interface and Setup, two parts
  this plan dissolves

**5. The companion agent**  `[SPLIT 01-interface/02-how-to-read-this.md]`
- the second way in: `cd ~/tutor && claude` in a tab of its own
- an agent that has read the whole course and answers from it, citing the
  article it came from
- the intended working pattern: read in one tab, ask in the other

**6. Exercises**  `[NEW]`
- how the exercises in this course work and where they appear
- that they build something you keep rather than something you throw away
- the only ones written are the five in Level 2's Build a Chain

## TUIs

### Terminals

**1. What a terminal is**  `[HAVE 01-interface/03-what-a-terminal-is.md]`
- terminal emulator: the second word is the interesting one
- the physical thing it imitates — the beige unit, the room-sized machine,
  the cable
- why the arrangement outlived the hardware
- the browser analogy: an app whose job is to run other programs
- they are not all the same, and the axes they differ on

**2. GUI and TUI**  `[HAVE 01-interface/04-what-a-tui-is.md]`
- a GUI is made of pictures, a TUI of characters
- this reader is one, and so is Claude Code
- TUIs came first; the desktop was built on top of the text layer
- the comparison table, and the discovery problem: a GUI shows you what it
  can do, a TUI shows you nothing
- what you get in exchange — commands compose, buttons do not
- carries the only picture in the course, `images/the-reader.png`

**3. What CLI, command line and prompt mean**  `[NEW]`
- the four words pulled apart: terminal, console, command line, prompt
- what CLI means and what it does not
- why they are used interchangeably in ordinary speech
- SEED: the aside in article 1 already makes this point in three lines;
  either lift it out or let this article do the job properly
- does not teach the prompt itself — that is The CLI, two parts on

**4. The terminals people use**  `[NEW]`
- iTerm2, WezTerm, Alacritty, kitty, Ghostty
- what they actually differ on: draw speed, images, tabs, splits, config
- SET UP BY: article 1's closing section, which names these axes and no
  terminal but Apple's

### Ghostty

**1. Your terminal is Ghostty**  `[HAVE 01-interface/05-why-ghostty.md]`
- Ghostty was installed alongside the Terminal your Mac came with
- quick, because it draws through the graphics chip
- a proper Mac app, not a wrapped web page
- the same on Linux, from one config file
- sane defaults, and a config that is `setting = value` rather than a
  language
- the keys worth knowing: `Cmd-T`, `Cmd-N`, `Cmd-W`, `Cmd-,`

**2. What was set up for you**  `[SPLIT 01-interface/05-why-ghostty.md]`
- Catppuccin Mocha, Hack Nerd Font, slight transparency, no title bar,
  bell off
- what monospace means and why this reader depends on it
- none of it is fixed: changing it is a sentence to Claude Code
- CHECK: the written article points forward to "The Shell → Starship" by
  name, and this plan renames that part to The CLI

> DISTRIBUTED — the rest of Ghostty is not an article here. First
> instalment: tabs and windows, Level 2 → Agents → Context.

### TMUX

**1. What tmux is**  `[NEW]`
- a program that holds terminal sessions independently of the window
  showing them
- how that differs from a Ghostty tab, which dies with its window
- why something built in 1987's idiom is still the answer

**2. What it is for**  `[NEW]`
- insuring and restoring sessions: a long job survives a closed lid
- mirroring and projecting a session to someone else
- panes and layouts: several processes on one screen
- named sessions, so many of them stay legible

> DISTRIBUTED — the rest of tmux is not an article here. First instalment:
> sessions that survive, Level 2 → Workflows. Then panes and layouts,
> Level 2 → Headless Sessions → Watching.

## The CLI

### Command Lines and Prompts

**1. Your prompt**  `[HAVE 01-interface/09-your-prompt.md]`
- the prompt is written by your shell, fresh, every time it is ready
- it is a template, so it can say anything at all
- the one thing worth having in it: where you are, because commands act on
  the folder you are standing in
- `pwd`, and why a prompt that answers it retires the question
- the drift from `$` towards a dashboard

**2. Starship and powerline themes**  `[HAVE 01-interface/10-starship.md]`
- writing a prompt template by hand is unpleasant, so the prompt runs a
  program instead
- powerline themes: segments, each one fact, appearing only when they apply
- why a Nerd Font is needed — the seam character exists in no ordinary font
- Starship: shell-agnostic, quick, configured in `~/.config/starship.toml`
- changing it by describing the outcome rather than learning the file
- ADD: Powerlevel10k, named in the plan and absent from the article
- FIX: the article sends the reader to `cd ~/retirement_101:setup && claude`;
  everywhere else in the course says `cd ~/tutor && claude`

> DISTRIBUTED — the rest of Starship is not an article here. First
> instalment: the directory segment, Level 2 → Skills → Making Them Fire.

### Shells

**1. What a shell is**  `[HAVE 01-interface/06-what-a-shell-is.md]`
- something is already waiting when Ghostty opens, and it is not the
  terminal
- the kernel: the only layer allowed near the hardware, and wordless
- the shell as the literal wrapper around it
- the aside that the Finder and the dock are a shell too, a graphical one
- the pointing/typing table: `cd`, `ls`, `open`, `rm`, `find`, `shutdown`

**2. Why the shell is powerful**  `[HAVE 01-interface/07-why-it-is-powerful.md]`
- clicking is one thing at a time, and has no way to say *all of them*
- a command takes the address as part of the sentence, so navigation stops
  being a step
- worked examples: find every PDF, grep a folder for a name, bulk rename
- pipes, and the fact that buttons do not compose
- you are not expected to absorb the syntax — knowing the shape of what is
  possible is the point

**3. The shells there are**  `[SPLIT 01-interface/08-your-shell-zsh.md]`
- the family tree: sh (1977), bash (1989), zsh (1990)
- bash and zsh understand each other; instructions written for one work in
  the other
- fish for friendliness, nushell for structured data, and what each trades
- PowerShell, and the Boss's considered technical assessment of it

### Zsh

**1. Your shell is zsh**  `[SPLIT 01-interface/08-your-shell-zsh.md]`
- yours is zsh and you did not choose it; `echo $SHELL`
- Apple switched in 2019 over a licence, not a technical judgement
- Unix, and that your Mac is a certified descendant
- POSIX, and why that makes this worth learning once — the knowledge
  travels to any machine you ever touch

**2. Moving around**  `[HAVE 01-interface/11-moving-around.md]`
- a path is an address; absolute against relative
- `~`, `.`, `..`, and how `..` combines for a sideways move
- the four commands: `pwd`, `ls`, `cd`, `open`
- how a command is put together: program, flags, argument
- `Tab` to complete, `↑` for history, `Ctrl-C` to stop
- aliases and variables, asked for in English
- DECIDE: the bracket note at the top of this document points at this
  article. Either it stays whole here, or the navigation half is held back
  to Level 2 where launching from the right folder makes it matter.
  Piping is spoken for either way — Level 2's Headless Sessions claims it

> DISTRIBUTED — the rest of zsh is not an article here. First instalment:
> moving between folders, Level 2 → Agents → Context. Then piping,
> Level 2 → Headless Sessions → Piping.

## Software

### Packages

**1. Every app is a wrapper**  `[SPLIT 01-interface/12-packages.md]`
- every app you have paid for is a pile of code behind a veil, a paywall,
  an installer and a logo
- very little of it is secret and a surprising amount of it is not theirs
- what you are buying, most of the time, is the wrapper

**2. Packages**  `[SPLIT 01-interface/12-packages.md]`
- small self-contained pieces of code that do one job
- most are free as in published and openly maintained, not free as in trial
- tesseract came from HP and is kept by Google; pandoc was written by a
  professor of philosophy — these are what the paid app is wrapped around
- a package has no window, so a mouse cannot find it: that is why the world
  stays invisible and why a shell changes what is available
- the replacements table — `diff` and `git` for tracked changes, tesseract
  and pdftotext, qpdf, pandoc, ripgrep, ocrmypdf, ghostscript, exiftool
- you are one sentence away: ask for the outcome and let Claude Code pick
  the package

**3. Package managers**  `[NEW]`
- what a package manager is and what it does beyond downloading
- signed repositories, dependencies, one command to update everything
- on Linux: dnf, apt, pacman, and that the distro chooses for you
- on a Mac: Homebrew, which nothing ships with and everyone installs
- SETS UP: the Linux part's analogy, which cannot be made before this

### Homebrew

**1. What Homebrew is**  `[NEW]`
- the package manager macOS does not come with
- installing it, and where it puts things
- why nearly every instruction you find online assumes it

**2. Formulae and casks**  `[NEW]`
- a formula is a command-line package; a cask is a whole Mac app
- `brew install` against `brew install --cask`, with Ghostty as the worked
  example — the reader already has it and can see what installed it

**3. Checking and updating**  `[NEW]`
- `brew list` and `brew search`, to find out what you have and what exists
- `brew outdated`, `brew update`, `brew upgrade`
- `brew doctor` when something is wrong
- the habit: one command a week rather than fifteen update dialogs

## Files

### Languages and Scripts

**1. What a programming language is**  `[NEW]`
- how a language differs from a shell: one describes a program, the other
  drives a machine you already have
- common examples and what each is reached for
- what a script is, and why the boundary is blurrier than it sounds

**2. Why plain text wins**  `[NEW]`
- `.md` and `.txt`, `.json` and `.jsonl` against `.doc` and `.xls`
- a plain file can be read, diffed, searched, copied and edited by a machine
- a proprietary file can be opened by exactly one program
- PAYS A DEBT: Level 2 leans on this constantly and never explains it

**3. The formats you will meet**  `[NEW]`
- YAML for frontmatter, JSON for settings, TOML for config, JSONL for logs,
  parquet for data
- which of them are unforgiving about punctuation and which are not
- PAYS A DEBT: `02-setup/06` warns that one missing comma stops
  `settings.json` working, and Level 2's agent and skill articles rest on
  YAML frontmatter and on a misspelt key being ignored in silence

### Editors

**1. IDEs**  `[NEW]`
- what an integrated development environment is
- VS Code, the JetBrains family
- built for people whose day is writing code, which is not your day
- RECONCILE: `02-setup/04-launching.md` already argues against running
  Claude Code in an editor panel for exactly this reason — this article
  should set that up, not contradict it

**2. Editors in the terminal**  `[NEW]`
- micro and nano, which behave the way you expect
- helix, vim and neovim, which do not, and what the trade buys
- emacs
- which one to reach for when Claude Code hands you a file to glance at

### Version Control

**1. What git is**  `[NEW]`
- every version of every file, with a note on why it changed
- SET UP BY: the packages article, which already puts `diff` and `git` in
  the top two rows of its replacements table

**2. How git works**  `[NEW]`
- commits, history, branches — the model, not the commands
- what a remote is

**3. jj**  `[NEW]`
- the same job, a different model, and why anyone switched

**4. GitHub**  `[NEW]`
- how a host differs from the tool: git is on your machine, GitHub is not
- what it adds — issues, pull requests, other people

> DISTRIBUTED — the rest of git, jj and GitHub is not an article here. No
> instalment placed yet; too early. The earliest it earns a place is Level
> 2 → Hooks, whose PreToolUse example gates on a file being committed.

## Linux

### The world runs on linux

**1. What Linux is**  `[HAVE 01-interface/13-what-linux-is.md]`
- Linux is a kernel, not an operating system, which explains both of its
  reputations at once
- a kernel needs dressing: a shell, a package manager, maybe a desktop —
  and the assembled bundle is a distribution
- the distro table: Debian/Ubuntu, Fedora, Arch, NixOS
- nobody owns it; companies sell support and distros around it
- the 1991 origin as an aside

**2. The world runs on Linux**  `[SPLIT 01-interface/13-what-linux-is.md]`
- under three percent of desktops, the overwhelming majority of servers
- ADD: cell phones, and claude.ai and Cowork by name
- the model you have been talking to answers from a Linux machine in a data
  centre — you have been using it for weeks without meeting it
- ADD, and it is the closing turn: Linux is to operating systems what
  packages are to apps. This is why the Linux part now sits *after*
  Software; the analogy cannot be made before Packages has been read

### Why its better

**1. Why it is better**  `[HAVE 01-interface/14-why-it-is-better.md]`
- lighter: nothing runs that you did not put there, which shows most on old
  hardware
- effectively no viruses, and the three structural reasons why
- private: nothing phones home, because there is no company on the other end
- native to the way you are working right now — the terminal is the primary
  interface there, not a fallback
- honest about what is worse: no Word, no Acrobat, hardware that needs
  coaxing
- and then refuses to rest the case on any of it, handing over to the next

**2. You are the system**  `[HAVE 01-interface/15-you-are-the-system.md]`
- on a Mac you can replace what runs on macOS but never macOS
- the layer table: display protocol, window manager, desktop environment,
  shell, terminal, init, package manager — each a real choice
- a Mac is shaped how a product manager guessed you work; a Linux machine
  ends up shaped how you actually work
- why this used to not happen: a weekend of forum posts per decision
- that cost is what Claude Code removes, which is why the part is here at all
- CHECK: closes with "That is Interface. Setup is next" — a handover to a
  part this plan replaces

## Agentic AI

[this part and the next are the one structural rebuild in Level 1. Two
written articles — `02-setup/01-what-claude-code-is.md` and
`02-setup/02-why-claude-code.md` — each braid model, harness and
Claude-Code material into a single argument. The plan files those three
subjects under three different headings, so both come apart and their
pieces redistribute. Nothing is discarded; the joins are.]

### LLMs

**1. What an LLM is**  `[SPLIT 02-setup/01-what-claude-code-is.md]`
- a very large mathematical function that produces what plausibly comes next
- not a lookup and not a search of the internet
- built by adjusting billions of numbers until the guesses got very good,
  and why that turns out to require understanding
- the limitation: it reads text and writes text, and can reach nothing
- a brain in a jar
- NEEDS A NEW WAY IN: the written article opens by separating Claude from
  Claude Code, which now happens two parts later

**2. What makes one model different from another**  `[NEW]`
- size, and what a parameter count does and does not tell you
- mixture-of-experts against dense, and why the distinction shows up in
  price and speed rather than in the answer
- speciality: what a model is tuned for

**3. The models there are**  `[SPLIT 02-setup/02-why-claude-code.md]`
- cloud models you reach over the internet: Claude, GPT, Gemini
- open-weight models you can download: Llama, Mistral, Qwen
- ADD: DeepSeek and Kimi
- the open ones sound obviously better until you try to run one

**4. What a model consumes**  `[SPLIT 02-setup/02-why-claude-code.md]`
- billions of numbers held where they can be multiplied at once
- VRAM, on the card, and the quantities: tens to hundreds of gigabytes
  wanted against 24 on a serious desktop card
- the Apple Silicon aside: one shared pool, so a MacBook runs a small model
  — and *small* is doing real work in that sentence
- so an open model being free is not the same as it being available to you

### Harnesses

**1. What a harness is**  `[SPLIT 02-setup/01-what-claude-code-is.md]`
- the LLM is the brain, the harness is the body
- the agricultural image: a horse can pull, a harness connects the pulling
  to a cart
- the five-step loop, in full
- step four is the whole trick — the model never touched your disk, it
  asked, and an ordinary program did the work and reported back

**2. The harnesses there are**  `[NEW]`
- online harnesses
- desktop and GUI harnesses, Antigravity among them
- CLI and TUI harnesses: qwen code, kimi code, opencode, Claude Code
- the written article defines the word and then names exactly one, which is
  what makes this article necessary

**3. What a harness consumes**  `[SPLIT 02-setup/02-why-claude-code.md]`
- an ordinary program: CPU and RAM, and not much of either
- a ten-year-old laptop would do
- EXTEND: the written sentence concludes that the harness runs comfortably
  on your Mac. The plan needs the further step — that running *many* agents
  at once is what your machine cannot do — because that is what sets up
  the next section

### Cloud Computing

**1. Renting a computer**  `[NEW]`
- the hardware limits from the two sections above, answered
- Amazon, Google and Microsoft, and paying by the hour
- a machine in a data centre, colloquially a box

**2. What you do with a box**  `[NEW]`
- install what you need — models, harnesses, packages — run it, download
  only the result
- almost every box is Linux and terminal-only, with no desktop at all
- which used to mean you needed shell knowledge, and now means the AI on
  your own machine does the driving
- REPAYS: every word in that last bullet was taught earlier in this level
- NOTE: promised for 0.3.0 in the written *About this wiki*; bringing it
  forward is one of the reasons that article's roadmap is rewritten

## Claude

### Claude

**1. The models**  `[NEW]`
- Haiku, Sonnet, Opus, Fable — what each is for
- estimated parameter counts
- DECIDE: `03-agents/02-context.md` already carries the context-window
  table and needs it there, because the whole context-rot argument rests on
  it. Cleanest split is that this article names the four and their
  purposes, and the Level 2 article keeps the numbers — a window size means
  nothing to a reader who has not yet met the idea of a window filling up

**2. The harnesses**  `[NEW]`
- what claude.ai is, what Claude Cowork is, what Claude Code is
- FRAGMENTS THAT EXIST: `02-setup/05` opens "claude.ai is a website. Claude
  Cowork is a website. Claude Code is not", used there to explain why
  `.claude` sits on your disk; `03-agents/03-context-rot.md` carries the
  Boss on why the other two will never get you anywhere, since you cannot
  see context in either. The second stays where it lands in Level 2; this
  article makes the neutral comparison first

### Claude subscriptions

**1. The plans**  `[NEW]`
- free, pro, max 5x, max 20x
- the saving is exponential rather than linear: 5x and 20x are several more
  multiples of usage per pound than pro
- most of what this course teaches needs 5x or 20x
- 5x to start; 20x for heavy models like Fable or heavy usage like workflows
- LOOSE END IT TIES: `04-skills/09-building-your-first.md` says an effort
  level can be outranked by "an account limit" without ever saying what one is

### Claude Code

**1. Why Claude Code**  `[SPLIT 02-setup/02-why-claude-code.md]`
- the surviving half: it is a terminal program, so no separate app and no
  editor to adopt
- you watch it work — every file read, every command run, printed as it
  happens
- it asks before anything consequential
- it can be taught, which is what the rest of the course is
- PLUS `02-setup/01`'s closing table and "So, Claude Code": the harness owns
  the loop and decides what the model may see and touch

**2. What it can do that the others cannot**  `[NEW]`
- it uses your software: it finds and pulls the best, fastest and free
  packages, where Cowork runs in a sandboxed VM
- it uses your hardware: buy a better machine and it runs a script on
  overdrive, where Cowork is capped at four cores — half a 2020 M1 Air
- LANDS ONLY BECAUSE OF THIS LEVEL: "it can pull any package" means nothing
  to a reader who has not read Software
- TENSION TO RESOLVE: `02-setup/02` uses locality to make a *privacy*
  argument. This is a *capability* argument off the same fact

### Claude Code setup

**1. Installing**  `[HAVE 02-setup/03-installing.md]`
- `claude --version` to check, and what your path is
- the one-line installer, and why it never asks for your password
- signing in, updating, `claude doctor`

**2. Launching Claude Code**  `[HAVE 02-setup/04-launching.md]`
- type `claude`; that is the whole ceremony
- why from Ghostty rather than an editor panel
- what makes no difference: which shell, what else is open, other sessions
- what makes all the difference: the folder you are standing in
- the habit: `cd ~/tutor && claude`

**3. The .claude directory**  `[HAVE 02-setup/05-the-claude-directory.md]`
- what a dotfile is and why the dot hides it
- `ls -a ~`, and `Cmd-Shift-.` in Finder
- the global one at `~/.claude`, which applies everywhere
- plain files rather than settings inside an app, deliberately
- MOVES OUT: its opening line about claude.ai and Cowork, now that the
  Claude section above states that properly

**4. Inside .claude**  `[HAVE 02-setup/06-inside-the-claude-directory.md]`
- the tour: `settings.json`, `CLAUDE.md`, `rules/`, `agents/`, `skills/`,
  `hooks/`, `plugins/`
- `settings.json` is JSON and unforgiving; ask rather than edit
- `CLAUDE.md` is the invisible prompt, read before you say anything, and
  the highest-leverage file you will own

**5. More .claude directories**  `[HAVE 02-setup/07-more-claude-directories.md]`
- one per folder, in as many folders as you like, registered nowhere
- a folder holding one becomes a project
- it layers on the global one rather than replacing it
- so project instructions travel with the folder

**6. What a session sees**  `[HAVE 02-setup/08-what-a-session-sees.md]`
- the rule: start where you launched, walk up, collect every `.claude`
- up and only up — a sibling is never seen
- three launches on one machine, worked through
- the model is identical in all three; what differs is the material it was
  handed before you typed

**7. Location matters**  `[HAVE 02-setup/09-location-matters.md]`
- more is worse: every extra agent and skill costs you on every question,
  including the ones none of it touched
- Party Trick #1, content isolation
- the bad layout against the good one
- the habit: not *is this good* but *where does this belong*
- CHECK: closes with "That is Setup. Agents are next" — now a handover from
  the end of Level 1 into the start of Level 2

# Level 2:

## Agents

[current content under agents is fine]

### Context

**1. What an agent is**  `[HAVE 03-agents/01-what-an-agent-is.md]`
**2. Context**  `[HAVE 03-agents/02-context.md]`
**3. Context rot**  `[HAVE 03-agents/03-context-rot.md]`
**4. Managing context**  `[HAVE 03-agents/04-context-management.md]`

>>>>>>>>>>>>>>>>  INSERT: GHOSTTY 1 — TABS AND WINDOWS  <<<<<<<<<<<<<<<<
>
> WHERE  a new article between 1 and 2 above.
>
> WHY HERE  article 1's whole argument is one agent per conversation, and
>        it already draws three Ghostty tabs side by side with three
>        agents in them. It then says "open three Ghostty tabs and start
>        three conversations" as though that were free. It is the first
>        moment in the course where the reader has to keep more than one
>        thing open, so it is the first moment a tab is worth teaching.
>        Level 1's Ghostty article gives `Cmd-T` and stops.
>
> LESSON  running several agents at once
>        - `Cmd-T` for a tab, `Cmd-1`–`Cmd-9` to jump straight to one
>        - `Cmd-W` to close, `Cmd-N` when a job wants a window not a tab
>        - splits, so one tab can hold two agents facing each other
>        - naming and reordering tabs, so three identical `claude`
>          sessions can be told apart — the actual problem article 1
>          creates and does not solve

>>>>>>>>>>>>>>  INSERT: ZSH 1 — MOVING BETWEEN FOLDERS  <<<<<<<<<<<<<<
>
> WHERE  a new article immediately after 4 above, or folded into its
>        `/exit` section.
>
> WHY HERE  `/exit` is the only one of the three resets that sends the
>        reader back to the shell, and the article hands them
>        `cd ~/work/okonjo && claude` with no more explanation than that.
>        By this point the walk-up rule has made the landing folder
>        decisive, so getting there accurately is a Claude Code skill
>        rather than a shell aside. This is the placement the bracket note
>        at the top of Level 1 asks for.
>
> LESSON  moving between matters
>        - `cd`, `~`, `..`, and `../sibling` for the sideways move
>        - `pwd` to confirm before launching
>        - `Tab` completion, so a long matter path is never mistyped
>        - `↑` to bring back this morning's launch line
>        - `Ctrl-C` as the way out of a half-typed command
>
> LATER INSTALMENTS  `mkdir` and `&&` at Subagents step one, which opens on
>        `mkdir ~/tutor/bundle && cd ~/tutor/bundle && claude` — three
>        commands on one line, unexplained. Then piping, which the plan
>        already assigns to Headless Sessions.

### Custom Agents

**1. The default agent**  `[HAVE 03-agents/05-the-default-agent.md]`
**2. Custom agents**  `[HAVE 03-agents/06-custom-agents.md]`
**3. The definition file**  `[HAVE 03-agents/07-the-definition-file.md]`
**4. The fields that matter**  `[HAVE 03-agents/08-the-fields-that-matter.md]`
**5. Building one**  `[HAVE 03-agents/09-building-one.md]`

## Skills

[current content under skills is fine]

### When To Build One

**1. Start with never**  `[HAVE 04-skills/01-start-with-never.md]`
**2. What a skill is**  `[HAVE 04-skills/02-what-a-skill-is.md]`
**3. The frontmatter**  `[HAVE 04-skills/03-the-frontmatter.md]`
**4. The body**  `[HAVE 04-skills/04-the-body.md]`
**5. Supporting files**  `[HAVE 04-skills/05-supporting-files.md]`

### Building One

**1. How to build one**  `[HAVE 04-skills/06-how-to-build-one.md]`
**2. Start with examples**  `[HAVE 04-skills/07-start-with-examples.md]`
**3. Iterate with corrections**  `[HAVE 04-skills/08-iterate-with-corrections.md]`
**4. Building your first skill**  `[HAVE 04-skills/09-building-your-first.md]`

### Making Them Fire

**1. How skills work**  `[HAVE 04-skills/10-how-skills-work.md]`
**2. Always invoke manually**  `[HAVE 04-skills/11-always-invoke-manually.md]`

>>>>>>>>>>>>>  INSERT: STARSHIP 1 — THE DIRECTORY SEGMENT  <<<<<<<<<<<<<
>
> WHERE  a new article after 2 above, picking up its "It also tells you
>        what is visible" section.
>
> WHY HERE  that section teaches the reader to read the `/` picker as a
>        diagnostic — a skill missing from the list means this session
>        cannot see it, and one of the two causes it names is "you started
>        the session somewhere other than where you thought". The prompt is
>        the thing that would have told them before they started. Level 1
>        argues the prompt should carry the working directory; this is the
>        first article where not having it costs something concrete.
>
> LESSON  reading your own prompt as a status line
>        - what the directory segment shows, and how it shortens a long
>          path rather than printing all of it
>        - changing or adding one segment in `~/.config/starship.toml`, by
>          asking for it in English
>        - enough that the prompt answers "which folder is this session
>          rooted in" without typing `pwd`

## Subagents

[current content under subagents is fine]

### Chains

**1. What a subagent is**  `[HAVE 05-subagents/01-what-a-subagent-is.md]`
**2. Chain engineering**  `[HAVE 05-subagents/02-chain-engineering.md]`
**3. Out of the box**  `[HAVE 05-subagents/03-out-of-the-box.md]`
**4. Designing a chain**  `[HAVE 05-subagents/04-designing-a-chain.md]`
**5. The door**  `[HAVE 05-subagents/05-the-door.md]`

### Build a Chain

**1. Step one — the project**  `[HAVE 05-subagents/06-step-one-the-project.md]`
**2. Step two — the workers**  `[HAVE 05-subagents/07-step-two-the-workers.md]`
**3. Step three — the door**  `[HAVE 05-subagents/08-step-three-the-door.md]`
**4. Step four — run it**  `[HAVE 05-subagents/09-step-four-run-it.md]`
**5. Step five — watch it**  `[HAVE 05-subagents/10-step-five-watch-it.md]`

## Workflows

### What They Are

**1. What a workflow is**  `[NEW]`
- works like subagents, but scripted
- instead of a main agent you can talk to calling subagents, a script calls
  every agent
- you cannot interact with any agent in the pipeline: the script gives them
  their prompts
- workflows live in `.claude/` alongside agents and skills, and can see the
  same assets an agent can

**2. What they buy and what they cost**  `[NEW]`
- the upside is consistency and quality control: the script forces the
  spawns and their order, so nothing gets skipped
- the downside is bloat — they are slow and expensive
- the same agent takes longer to start and stop inside a workflow than as
  an ordinary subagent
- and a workflow always involves far more agents than a subagent chain, so
  the cost compounds

**3. When to use one**  `[NEW]`
- the rule: when there are multiple pipelines of the same task
- the worked example — read, summarise and review ten books
- managing context might need eight readers, four summarisers, two
  reviewers; as a subagent chain that is fourteen for the main agent to
  hold, which may blow its context
- and even if it does not, that is ten sessions and ten identical prompts
- a workflow is one pipeline run ten times over, or ten at once, with no
  management

>>>>>>>>>>>>  INSERT: TMUX 1 — SESSIONS THAT SURVIVE  <<<<<<<<<<<<
>
> WHERE  a new article after 3 above, before What To Do About It.
>
> WHY HERE  articles 2 and 3 have just established that workflows are slow
>        and expensive and that the point of one is running the same
>        pipeline ten times over. That is the first thing in the course
>        that runs longer than the reader's patience for sitting in front
>        of it, and the first where closing the terminal would destroy
>        work already paid for. Nothing earlier earns tmux — a subagent
>        chain finishes while you watch.
>
> LESSON  the persistence half only, not panes
>        - what a tmux session is, and how it differs from a Ghostty tab
>          that dies with its window
>        - starting one and running the workflow inside it
>        - detaching, and leaving it running with the lid shut
>        - listing what is running, and reattaching later or from elsewhere
>        - naming a session after its workflow, so ten stay legible
>
> LATER INSTALMENT  panes and layouts at Headless Sessions, where the plan
>        already asks for a watch script running beside the session it is
>        watching — two processes on one screen, which is what panes are for.

### Building One

**1. How to build a workflow**  `[NEW]`
- always ask Claude; do not attempt to write one by hand
- ask the main agent for a workflow the same way you ask for a chain of
  subagents
- the main agent has an effort level called ultracode meant for writing and
  managing workflows: `/effort`, select ultracode, then ask

**2. Making it thinner**  `[NEW]`
- do not trust Claude blindly — it will sell you ten times the agents you
  need, all on the most expensive model
- ask for a workflow, then push back and ask how it can be made thinner
- start with the count: how do we make it fewer agents
- then the models: which of these can drop to a lower one
- and the best question of all: which of these steps needs no LLM at all
  and can just be part of the script

## Hooks

### What They Are

**1. What a hook is**  `[NEW]`
- hooks are script triggers
- they are the only way to actually force Claude's behaviour — everything
  else, skills and prompts included, is technically optional
- the most useful framing: as your chains and workflows grow you lose
  visibility into what agents are doing, and hooks are how you get it back

**2. The triggers**  `[NEW]`
- knowing these is what tells you when to ask whether a hook would help
- SessionStart, when you launch Claude
- UserPromptSubmit, whenever you send a message
- PreToolUse and PostToolUse, either side of a tool call
- SubagentStart and SubagentStop
- Stop, when Claude finishes responding
- SessionEnd, when the session closes

**3. Scoping a hook**  `[NEW]`
- as with everything else, the customisation is the point
- a hook can be limited to certain agents, certain plugins, certain projects
- if you want a few custom agents to behave differently, that is a hook —
  not an edit to your `CLAUDE.md`

### Using Them

**1. Worked examples**  `[NEW]`
- SessionStart: tell one custom agent to ignore part of your `CLAUDE.md`,
  or to follow special rules on this project
- UserPromptSubmit: remind the agent to answer in two languages
- PreToolUse: on Write, Edit or Bash, check the file is committed first
- PostToolUse: on Write or Edit, fire a subagent to review what was written
- SubagentStart: preload a skill for that subagent
- SubagentStop: confirm the agent used the skill it was supposed to, in the
  middle of a large workflow
- Stop: have Claude rewrite the answer if it blew a word limit
- SessionEnd: save the transcript somewhere of your choosing
- SPLIT THIS if it runs long — the natural break is session-level hooks
  against tool-level ones

## Plugins

### What They Are

**1. What a plugin is**  `[NEW]`
- the easiest way to think of it: a remote, portable `.claude/` directory
- instead of writing assets into a project's `.claude`, you write them into
  an ordinary folder
- and then install that folder into several projects, your whole machine,
  or someone else's machine

**2. When to make one**  `[NEW]`
- when you need a suite of assets, but rarely, and do not want it cluttering
  and slowing every other agent
- when two repos on opposite sides of the tree need the same suite, and
  nothing higher up the tree should have it
- when you want to keep a suite after the project it was built for is done
- when you want to share one
- the best case: continuously improving a single piece of plumbing shared
  by several projects — a voice agent, with a skill to write like you and a
  skill to send your email, working across personal and work projects while
  you feed it new examples of your voice every day
- EACH BULLET WANTS A CONCRETE EXAMPLE; the plan marks four as missing

**3. What is inside one**  `[NEW]`
- an ordinary directory that looks like the inside of `.claude`
- `agents/`, `skills/`, `hooks/`, `mcps/`
- `commands/` — obsolete, per the Boss; they are just skills now
- `settings.json`, and that this is the place to override global settings
- `.claude-plugin/`, which Claude writes and which is what makes the folder
  a plugin
- one or two full worked examples

### Using Them

**1. How a plugin works**  `[NEW]`
- the `.claude-plugin/plugin.json` manifest
- the marketplace JSON, what it is and why a plugin has to be in one
- installing globally or per project
- enabling and disabling, in global or project settings
- updating

**2. Building one**  `[NEW]`
- always ask Claude

**3. Exercises**  `[NEW]`
- turn something already built into a plugin and install it in a second
  project

## Headless Sessions

### Running Without a Chat

**1. What a headless session is**  `[NEW]`
- with Claude Code you can run Claude without starting a chat
- launch it with `--print`, or just `-p`, and type the prompt directly
- it runs non-interactively in your shell and delivers only the outcome

**2. When to use one**  `[NEW]`
- quick jobs that need no back and forth
- established pipelines — a battle-tested subagent chain runs start to
  finish with no chat open
- workflows: launch a headless agent to run one and babysit it

**3. Piping**  `[NEW — and this is where zsh piping lands]`
- `|`, and feeding one command's output into the next
- feeding a headless session from a file or a command, and its answer into
  something else
- the instalment Level 1's Moving around deliberately held back

**4. Watching**  `[NEW — Party Trick #N]`
- use your shell to watch: ask Claude to build you realtime scripts
  reporting every subagent in a headless session
- INSERT, TMUX 2 — panes and layouts: the watch script running beside the
  session it is watching is two processes on one screen, which is the thing
  panes exist for, and it belongs in this article rather than in one of
  its own

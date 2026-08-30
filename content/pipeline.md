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
- Running one yourself

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
- The harnesses
- What it can do that the others cannot

### Claude Models

- The Claude models
- The plans

## Other Models

### Running Other Models

- Pointing the harness elsewhere
- What you give up

### Ollama

- Signing in
- Running it
- Choosing a model
- Context length
- When Ollama breaks

### Kimi

- Kimi as an endpoint
- Keys and membership
- Pointing Claude Code at Kimi
- Thinking and effort
- When Kimi breaks

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

## Challenges

- Challenge one

# Level 3

## Automating Agents

### Scripted vs Agentic Behavior

- What changes at level three
  + Until now you typed and something happened. From here a clock, a
    changed folder, a form or another service starts the work, and you
    are not at the machine when it does
  + Level two ended with a funnel — chained agents, each with its own
    skills, hooks and context, so that something dropped in at the top
    comes out the other end as the thing you wanted
  + Level three wires that funnel into the world: your own files, your
    own systems, the services you already pay for, reached without you
  + What it unlocks: work that happens while you are in court, and is
    finished when you get back
  + The trap: none of this is more capable than what you already have.
    It is the same Claude Code, started by something other than you

- The shape of an automated system
  + Four parts, and every automation in this level is an arrangement of
    them: a trigger that starts it, an input it picks up, the work
    itself, and an output somebody sees
  + The trigger is a clock, a folder that changed, a queue, or a request
    arriving over the network. There are no others
  + The work is where Claude Code sits, and it is the smallest of the
    four
  + The output has to leave the machine or nobody knows it ran — a
    message, a document, a page, a row in a table
  + What it unlocks: naming the four parts before you ask for a thing,
    so the request is one Claude can actually build
  + The trap: a system with no output is indistinguishable from one that
    never ran at all

- Less is more
  + Every agent turn is slower, dearer and less repeatable than the
    script that would do the same job
  + An agent earns its place where judgement is needed — reading a
    letter, deciding what a document is, drafting. Not where a rule
    would do
  + The test before asking for an agent: could this be written down as a
    rule? Then it should be written down
  + What it unlocks: systems that run overnight unsupervised, because
    most of what they do cannot surprise anyone
  + The trap: an agent at every step is how an automation becomes
    expensive and unpredictable at the same time

### Scripted Behavior

- What a script is for
  + A script is a fixed sequence of steps, written down once, that
    runs without deciding anything as it goes — the same
    instructions, in the same order, every time
  + What it unlocks: forty scanned letters land in the intake folder
    each morning; a script renames each by date and matter number,
    files it, and logs what it did — the same three steps, exactly,
    whether five arrive or five hundred
  + Claude writes the script; something else runs it — a watcher
    noticing a file, cron at three in the morning, a webhook arriving
  + What makes it worth asking for: it keeps running after the
    terminal is closed and the session has ended, which nothing built
    from a conversation with Claude does on its own
  + The trap: a script has no judgement. Feed it a letter shaped
    differently from what it expects and it does the wrong thing, or
    stops, and says nothing unless it was written to complain

- Python, Node and Bun
  + Python is the default: already on every machine Claude Code runs
    on, and a library exists for nearly anything asked of it —
    pulling dates from a bundle of pleadings, renaming a folder of
    scans, totalling a spreadsheet of disbursements
  + Node ships with the web world — anything that means talking to a
    modern service, checking a court listing, posting to Slack,
    fetching an exchange rate, usually has a Node example to start
    from first
  + Bun is Node's faster relative: the same language, quicker to
    start and run
  + What it unlocks: whichever of the three Claude reaches for, it is
    already on the machine — nothing to choose, only a name that
    appears in a script Claude writes
  + The trap: treating this as a choice worth making. Picking a side,
    or asking Claude to justify one over another, changes nothing
    about what the script does

- A script instead of an agent turn
  + An agent turn reasons every time it runs — reads, drafts,
    decides afresh — which costs money and time and can answer
    slightly differently on the tenth run than the first
  + A script, once written, is the same rule run identically the
    four hundredth time as the first, for close to nothing
  + Where a script is what to ask for: any decision that reduces to
    a rule — if a filename matches this pattern move it here, if a
    field is blank flag it, if a deadline has passed send a reminder
  + Where the agent still earns its place: reading a letter to work
    out what it is actually about, drafting the reply, judging
    whether a changed clause in a lease matters — nothing written
    down catches that
  + The spine of it: instead of asking Claude every week to check
    which invoices are still unpaid, ask it to write the script once
    — Claude's judgement goes into drafting the reminder, not into
    re-deriving the check each time
  + The trap: a script cannot notice when a case falls outside its
    own rule. It will file a date in the wrong month forever if the
    format changes, and it will not know it is wrong

### Environments

- Virtual environments
  + The script that OCRs a folder of scanned post stops working
    three days after Claude installs something for an unrelated
    invoicing job, with nothing in either job's output tying the
    two together — it just fails
  + Installed once for the whole machine, a package is shared by
    every project on it. Two projects wanting different versions of
    the same library collide, and fixing the version for one breaks
    it for the other
  + The fix is a folder called .venv, sitting inside the project
    itself, holding that project's own copy of its packages, checked
    before the shared, machine-wide copy. Delete the folder and the
    packages are gone, the rest of the machine untouched
  + The name is Python's; the problem is not. Node keeps a project's
    packages in a folder of their own without being asked; Go bakes
    them into the finished program. Python is the one this gets
    discussed for only because it was installed machine-wide for
    decades before the fix arrived
  + What to ask for: when work on one matter is disturbing work on
    another that has nothing to do with it, ask Claude to put the
    disturbed project in its own environment
  + The boundary: an environment isolates a project's libraries. A
    container isolates the whole operating system underneath them

- uv, pipx and conda
  + uv is the one to name for ordinary Python work — a script that
    renames a folder of scanned exhibits, or pulls the text out of a
    bundle of PDFs — doing the same job as the older standard tools
    in a fraction of the time
  + pipx is for a finished command-line program rather than a
    library: it gives that one program its own environment, so a
    tool installed for one job cannot collide with a tool installed
    for another
  + conda does both jobs, environment and package installer, in one
    tool, and goes further than uv or pipx: it installs the Python
    interpreter itself, plus non-Python pieces such as compilers,
    which is why heavier numerical and scientific tools lean on it
  + What that reach costs is weight and speed, against the lighter
    tools above
  + The trap: if conda is already installed and already working,
    there is nothing to fix. Naming uv or pipx is not a reason to
    unpick a working conda setup

### Logs

- Unattended work fails quietly
  + A job that silently skipped twelve matters and a job that
    correctly processed all twelve stop the same way: nothing on
    screen, because there was nobody there to see it
  + An exit code of zero says the process ended without crashing.
    It says nothing about whether the work inside it happened
  + Unattended work fails silently, and a written record made
    while it ran is the only evidence, afterwards, of what it
    actually did
  + The record turns an unanswerable question into a lookup:
    which run failed last night and why, whether a job actually
    ran on Tuesday, which matters were processed and which were
    quietly skipped
  + The trap is trusting silence — nothing came back to complain
    is not the same as nothing went wrong

- Where logs go
  + A command typed by hand prints to the screen, and that screen
    is the log — it disappears the moment the window closes
  + A job started by cron has no screen: unless somewhere is
    named to catch it, the output it produces goes nowhere
    durable at all
  + What it unlocks: naming one fixed file per job, in a known
    place, turns "what happened" from a memory to rely on into
    an address to check
  + The file does not need to be clever, only predictable — one
    job, one file, always the same location, so a question asked
    later starts by knowing where to look
  + A log line worth keeping records a timestamp, which job wrote
    it, what happened, and on a skip, why
  + The trap: a log file nobody ever opens is indistinguishable
    from no log file at all. Writing it down is half the job;
    someone or something reading it is the other half

- Log aggregators
  + Twelve unattended jobs each writing their own log file
    produce twelve files, and nobody reads twelve files; an
    aggregator collects them into one searchable place instead
  + What it unlocks: asking which of the overnight jobs failed
    and why, or what Claude cost this month per skill, across
    all of them at once — sums and searches no single job's log
    file can answer alone
  + The record it holds outlives the job that wrote it and stays
    searchable by time — a question about last Tuesday is
    answered the same way whether it is asked the next morning
    or next month
  + journalctl already does this for anything systemd runs, with
    nothing extra installed; Loki, or a plain SQLite table with
    one row per log line, does the same job for everything else
  + The ceiling: a dozen unattended jobs justify an aggregator;
    two do not
  + One file per job, in a known place, answers the same
    questions until the count of jobs makes checking them one at
    a time impractical

### Language Servers

- What a language server is
  + A language server is a program that understands a programming
    language properly and can answer questions about the code in
    front of it
  + It does not make Claude better at Python. It makes Claude better
    at *your* Python — the language was already known; the project
    was not
  + Without one, Claude greps and guesses at the answer, and
    guessing is where bugs enter
  + What it unlocks: an automation that has grown past one script —
    the intake form, the nightly archiver, the job that files
    scanned post — gets edited without Claude losing track of what
    calls what
  + The gain over grep: which of forty files defines a function, who
    calls it, what breaks if it changes. A grep search returns every
    mention, comments and same-named functions included; the server
    returns the actual definition and every genuine caller

- The servers there are
  + Language servers are not written for the occasion. They already
    exist, one per language — gopls for Go, pyright or ruff for
    Python
  + One per language, never per project and never per part of one.
    Count the languages in the repository and that is the count — a
    project mixing Go and Python runs two servers side by side, each
    indexing only the files of its own language
  + Scope is the repository open right now. A session starts the
    server and it indexes what sits under this folder
  + What it unlocks: a project that has grown past a handful of
    files — a set of scripts, a small web server, a growing plugin —
    gets a server that already knows all of them, without naming one
    by hand
  + The trap: open a different project and the exactness resets.
    Nothing learned in one repository carries into the next

- Wiring one into Claude Code
  + It is not typed by hand: a language server is declared in a
    `.lsp.json` file, or inside a plugin's own configuration — ask
    Claude to wire it up rather than opening the file
  + The one condition wiring cannot skip: the binary itself must
    already be installed on the machine, the ordinary way — with npm
    or pip. Naming a server that is not there wires nothing
  + The distinction worth having: wiring one into a project serves
    only that project; wiring one inside a plugin carries it to
    everyone who installs the plugin
  + What it unlocks: a plugin already built for your own work adds
    four lines and everybody who installs it gets the same symbol
    navigation, with nothing further to configure
  + The trap: asking for the wiring without the binary installed
    first quietly does nothing

- Diagnostics
  + Diagnostics is on by default, which means the running commentary
    is what you get from a language server unless you ask otherwise
  + On: every error the server sees is pushed into Claude's context
    the moment an edit is made — a broken line is caught the instant
    it is written, not when something later fails to run
  + Off: the navigation stays — go to definition, find references,
    hover — the commentary is what goes
  + The trap: a long session making many small edits pays for
    diagnostics in context, the same context every other file and
    every other tool call is competing for
  + The choice is real, not a toggle to leave alone: a session
    generating a stream of edits gets noisy and costly with it on; a
    single careful fix loses nothing with it off

## Triggers

### Schedulers

- What a scheduler is
  + A scheduler is a daemon the operating system runs on its own
    account: a time, and a command, fired at that time whether or
    not anyone is logged in, surviving a reboot without being told
    to restart — the machine's own alarm clock
  + What it unlocks: the Companies House check that runs at seven
    every morning, the status page regenerated overnight, the
    archive job that runs at 2am, none of them waiting on you to sit
    down and start them
  + Three implementations carry the idea: cron and systemd timers on
    Linux, launchd on macOS — different daemons, the same promise of
    a time and a command
  + What to ask for: name the job and the time it should run — "run
    this every weekday at 8am" is enough for Claude to wire the
    right one underneath
  + The trap: a scheduler fires unconditionally. It does not check
    whether yesterday's run finished, or whether the last one
    failed, before firing the next one

- cron
  + cron is the original: one line per job, naming a time and a
    command, kept in a file called a crontab
  + What it unlocks: the rented box behind an intake form runs
    `claude -p` against the skill that drafts an engagement letter,
    on a schedule, with nobody logged in to start it by hand
  + It is the name reached for by habit even off Linux, the way
    "googling" outlived one search engine — the job of naming a time
    and a command is cron's job first
  + The trap: cron does not check whether the last run of a job is
    still going before starting the next. A job that usually takes a
    minute and once takes an hour ends up running twice at once,
    with cron unaware either copy exists

- launchd
  + launchd is the scheduler on your own machine: the only one Apple
    properly supports, and the one a job on a Mac should be
    configured with
  + What it unlocks: whatever landed in the intake folder overnight
    gets OCR'd and filed at seven, before you sit down, and a status
    page regenerates while you sleep — both on the machine already
    on your desk, nothing rented
  + launchd is owned by the operating system itself rather than by a
    program that has to already be running: a job fires because
    macOS fires it, the same way a login item starts, with nothing
    separate to keep alive in the background
  + What to ask for: on a Mac, ask Claude to set the job up with
    launchd by name — it is the one that applies to the machine in
    front of you
  + The trap: cron is still present on macOS, and a crontab entry
    still runs. That is how a job meant for launchd ends up
    scheduled with the tool Apple does not properly support instead
    of the one it does

- systemd timers
  + systemd timers are the Linux replacement for cron, closer in
    spirit to launchd than to the crontab file it replaces
  + The improvement over cron: a missed run is caught rather than
    silently dropped, and the outcome of every run lands in the
    system journal rather than a file nobody opens
  + A timer can also wait on another service before firing — a job
    reading a database that has not finished starting does not run
    early and fail, an option cron does not have
  + What it unlocks: the same unattended `claude -p` run as cron's,
    on a rented Linux box, with a record afterwards of whether it
    actually ran
  + The trap: systemd timers are Linux only. A job set up this way
    on a rented box does not carry over to the Mac in front of
    you — the daemon and the way of describing the job are both
    different

- Claude Code's own scheduler
  + Claude Code has cron tools of its own, and they are not cron or
    launchd: they schedule work inside a session that is already
    running, not on the machine underneath it
  + Nothing fires if Claude Code itself is not running, a scheduled
    task expires after seven days, firing times jitter by up to
    thirty minutes, and a task only runs between turns — never
    mid-turn, never while the session is closed
  + What it is for: a reminder to check something later, inside a
    session already being kept open — not a substitute for
    unattended overnight work
  + For anything that has to run with nobody at the keyboard, the
    answer is the machine's own scheduler launching `claude -p`, not
    Claude Code's own tools — system cron and launchd do not care
    whether anything is already running, which is exactly the point
  + What to ask for: say which one you mean. A reminder inside the
    session in front of you and a job that runs whether or not any
    session is open are answered by two different schedulers, and
    the two do not overlap at all

- Machines that sleep
  + Neither cron nor launchd wakes a sleeping machine. Closing the
    lid at the wrong moment does not delay the scheduled job — it
    skips it, with nothing recorded to say so
  + launchd has one partial answer: `RunAtLoad`, which fires the job
    the moment the machine next wakes rather than at the missed time
    itself — a catch-up, not a guarantee of punctuality
  + Linux has its own partial answer in `anacron`, built for exactly
    this: it notices a run was missed and runs it late, rather than
    dropping it the way plain cron does
  + The honest answer for a job that has to run at 2am precisely,
    every night, is that it does not belong on a laptop at all — a
    laptop closes, sleeps, and travels, and a scheduler cannot see
    through any of that
  + What to ask for: a job that truly cannot be missed goes on a
    machine that never sleeps — a rented box left running — which is
    the argument for moving a routine off your own Mac

### Watchers

- What a watcher is
  + A watcher is a program that sits outside Claude Code and starts
    a session when a file appears or changes in a folder it is told
    to watch
  + Cron asks on a timer, every five minutes whether or not anything
    happened; a watcher is told by the operating system the moment
    it happens, with no polling and no delay
  + Concrete: an export from another system arrives and is ingested,
    unattended, without you having opened anything to receive it
  + The trap: a watcher only works while it is running. Close the
    terminal, sleep the machine, restart it, and the watcher is
    gone — nothing says so, and the folder keeps filling with files
    nothing is processing

- inotify, fswatch and entr
  + inotify is the Linux kernel's own mechanism — the part of the
    operating system actually doing the watching. It is Linux-only,
    so a recipe built on it does not run on a Mac
  + fswatch is the one to reach for on your machine: the
    cross-platform wrapper that does the same watching job on Linux
    and on macOS
  + entr is the friendliest of the three for a single, narrow job —
    hand it a list of files and a command, and it reruns the command
    the moment one of them changes
  + What to ask Claude for is the outcome, not the tool by name —
    watch this folder, do this when something lands — and let it
    pick between fswatch and entr underneath

- A folder as a trigger
  + The design idea: an ordinary folder in the Finder becomes the
    interface to an automation. No command to type, no session to
    open — the folder is the whole instruction
  + Concrete: the forty scanned letters that land in an intake
    folder each morning are OCR'd and filed by the time you sit
    down, without you having asked that morning at all
  + You ask Claude to build one watched folder per repeatable job,
    named for what happens to what lands in it, rather than one
    folder doing several jobs at once
  + The trap: a file mid-write is not a finished file. A watcher
    firing the instant something appears can pick up a document
    that is still being scanned, copied or saved, and process a
    fragment
  + A watcher worth trusting waits for a file to stop changing
    before treating it as arrived — logic you ask Claude to build
    in, not something a folder does for free

### Queues

- What a queue is
  + A queue is a waiting line for work, so documents arriving faster
    than they can be processed queue up instead of being lost or
    overwhelming the machine that has to handle them
  + Forty scanned documents land in the intake folder at once, each
    taking two minutes to process — run all forty together and the
    machine grinds to a halt, so instead they go into a queue and
    workers pull them off two at a time
  + What it unlocks: nothing that arrives is dropped, and the
    machine only ever does as much at once as it can actually manage
  + A job that fails goes back into the queue and is retried rather
    than vanishing — the document that failed at three in the
    morning is still there when you sit down
  + What puts work into the queue is separate from the queue itself
    — a clock, a watcher, a web request — the queue only holds what
    has already arrived

- Redis, SQLite and the serious version
  + A `jobs` table in SQLite is enough on one machine and installs
    nothing beyond what is already there
  + Redis with a worker library earns its place once several
    processes need to pull from the same line at once, which one
    SQLite file cannot do safely
  + RabbitMQ and Celery are the serious version, built for a fleet
    of workers spread across many machines — almost certainly not
    what you need
  + The path: start with the SQLite table; move to Redis only when
    more than one process is drawing from the same queue
  + The trap: reaching for RabbitMQ and Celery before the SQLite
    table has ever struggled — nothing that fits on one machine
    outgrows a jobs table

### Monitors

- What a monitor is
  + A monitor is a background command a plugin declares. It runs for
    the life of the session, and every line it prints to stdout is
    delivered to Claude as a notification
  + What it unlocks: Claude finds out about something without being
    asked, and without you noticing first — a log tailed that speaks
    up when an error appears, an incoming folder watched and
    announced, a long build followed, a growing queue reported
  + The boundary that matters: a monitor lives inside a running
    session and reports to it. A watcher starts a session from
    outside — a different thing entirely
  + It is experimental
  + It inherits the session's lifetime. Nothing is watched once the
    session ends

- Declaring one in a plugin
  + A monitor is declared inside a plugin, not pointed at a session
    yourself
  + `always` is the default. It starts the monitor the moment the
    session begins
  + `on-skill-invoke:<skill-name>` holds the monitor back until that
    skill is first dispatched
  + The reason for the choice: a session that never needs the skill
    never pays for the monitor running underneath it

## Integrations

### APIs

- What an API is
  + An API is a service answering a direct request rather than
    showing a page for a person to click through — the same case
    system, the same accounting package, asked for the answer
    instead of opened and read
  + What it unlocks: most services you currently log into and click
    through answer a direct request too, with no browser and no
    person in the loop
  + Nothing to install for most of it: an API is a request the
    service already answers for anyone who asks correctly, reached
    with the same kind of tool that fetches a web page
  + The trap: an API is not guaranteed. Plenty of services worth
    reaching publish nothing to call, and no request is shaped
    correctly when there is nothing on the other end to answer it

- curl and jq
  + curl is the tool that fetches a URL from the command line — the
    same request a browser makes, with nothing to click and nothing
    to render
  + jq is the tool that cuts up what comes back — pulls one field
    out of a mass of JSON, filters a list down to what matters,
    reshapes an answer into something usable
  + Together they are the cheapest integration there is: no server
    to run, no account to configure, nothing beyond the two of them,
    and they reach most of the world's data with no MCP server in
    sight
  + What it unlocks: check a case status every morning and have
    Claude report only what changed; pull the day's exchange rate
    into a fee calculation; fetch a filing from Companies House;
    download a court listing; ask accounting software what is unpaid
  + You never type either yourself. Claude writes the request and
    reads the answer; these two are what it reaches for the moment a
    service has no menu of its own
  + The trap: both tools answer exactly what was asked and nothing
    more. A malformed request comes back as an error page or nothing
    at all, and noticing that is on whoever reads the answer

- The API shapes there are
  + Every shape splits on one question: who speaks first, you or the
    service — the five run from you-ask to they-tell
  + REST is you asking: a request, an answer, the connection closes.
    It is the shape behind the vast majority of what gets reached
  + Webhooks are the service asking, in reverse: you hand over an
    address, and it calls that address when something happens — a
    payment landing, a status changing — with no request from you at
    all
  + WebSockets and server-sent events both keep the connection open
    rather than closing it after one answer. WebSockets carry
    traffic both ways for something continuous; server-sent events
    run one way only, service to you, which is how Claude streams
    its own replies as they are written
  + GraphQL stays in you-ask-they-answer territory but lets you name
    exactly which fields come back in one request, rather than
    taking whatever shape REST hands you
  + The trap: which shape you meet is the service's decision, made
    long before you arrived. Establishing which one it offers is the
    first question, because that decides whether you ask Claude for
    a poll or for something that waits to be called

- Polling and webhooks
  + A webhook is a gift: the service does the watching and calls you
    the moment something changes, and it exists only where the
    service bothered to build one
  + Polling is what you build when nobody is offering to tell you:
    cron fires, curl fetches, the result is compared against
    yesterday's saved copy, and Claude acts only on the difference
  + What it unlocks: a morning check on a court listing that reports
    only what changed since yesterday, without you opening the site
    yourself to find out
  + Webhooks assume something of yours is listening for the call;
    polling assumes only that you can ask again tomorrow — which is
    why it is the one you can always build
  + The trap: webhooks depend entirely on the third party offering
    one, and courts almost never do. Build the poll rather than wait
    for a webhook that is not coming

- Scraping
  + Scraping is what is left when a page has no API behind it at
    all: no REST endpoint, no webhook, nothing to call — only HTML
    meant for a person to read
  + What it unlocks: curl still fetches the page, and Claude reads
    the HTML directly for whatever a service publishes with no API
    and no webhook behind it — most government pages among them
  + The manners that keep this working: identify yourself with a
    proper User-Agent rather than pretending to be a browser, and do
    not hammer the server — once or twice a day bothers nobody
  + Where curl stops working: a page behind a login, or one that
    renders nothing until its own JavaScript runs. Driving a real
    browser is the answer there
  + The trap: a page changes its layout without warning, and nothing
    tells you the scrape broke. It keeps running and returning
    nothing, or the wrong thing, until someone checks

### MCPs

- What an MCP is
  + Without one, reaching a service means Claude writing curl
    commands and parsing whatever comes back. With one, the
    service's own operations are on the menu, described and typed
  + A small program advertises a list of tools, and Claude calls
    them the same way it calls anything built in — a server you
    configure yourself, as against a connector ticked on at
    claude.ai with no file touched
  + What it unlocks: a case-management database queried read-only,
    a document store filed into and retrieved from, errors pulled
    straight out of Sentry — anything a vendor has bothered to
    publish a server for
  + The trap: not every service has one yet. A capability with no
    published server still has to be reached with curl, same as
    before

- Adding one
  + You ask Claude to add a server, naming the service — the entry
    is not something you open a file and hand-type yourself
  + Servers are not written for the occasion. A vendor that already
    publishes one is worth searching for before assuming the gap
    has to be closed by hand
  + Adding one settles two things at once: where it runs — launched
    on your own machine, or reached at a URL somebody else runs —
    and which of three scopes it is added to
  + The trap: adding a local server means Claude launches somebody
    else's program on your machine, with your files in reach. An
    unvetted server is arbitrary code running with your access, not
    a menu item to try out
  + What it unlocks: a service you already use gets its own
    operations on the menu the same afternoon you find out a server
    for it exists, rather than waiting on a project to write one

- The transports
  + The transport decides whether the server runs on your own
    machine or on someone else's, and it is fixed the moment the
    server is added
  + `stdio` launches the server as a subprocess on your own
    machine — the common case for anything local, and the one most
    vendor instructions assume
  + `http` reaches a server that somebody else runs, elsewhere
  + `sse` is deprecated — worth recognising in older documentation,
    not worth building anything new on
  + What it unlocks: knowing which transport a given server needs
    before asking Claude to add it, rather than guessing from
    whatever a vendor's page happened to show
  + The trap: matching the wrong transport to a server connects
    nothing. A service running on someone else's machine will not
    answer to a `stdio` entry, and a local subprocess cannot be
    reached as though it were a URL

- Scopes and where they live
  + Three scopes: `local` — this project only, on this machine;
    `project` — every checkout of this repository; `user` — every
    project you open
  + `local` and `user` both live in `~/.claude.json`; `project`
    lives in `.mcp.json` at the root of the repository itself
  + What it unlocks: `project` scope travels with the code — add a
    server there and everyone working from that checkout has it,
    with nothing to set up per machine
  + The trap, stated exactly: MCP servers are not in
    `.claude/settings.json` with everything else, and Claude Code
    does not read `~/.claude/mcp.json`, however plausible that path
    looks
  + Choosing: a server only you use wants `local`; a server every
    matter on this machine should reach for wants `user`; a server
    the whole team needs behind the code wants `project`

- Authentication
  + Which authentication a server uses decides whether it survives
    running unattended overnight, not just whether it connects once
  + Concrete: an archiver that files documents against a
    case-management server at 3am is only as reliable as the
    token behind it — one expired over a weekend loses days of
    intake before anyone notices
  + A static header never refreshes. It has to be noticed and
    rotated by hand once it expires
  + OAuth refreshes its own token and retries once on a 401 — enough
    to cover most overnight running without anyone awake to help it
  + `headersHelper` runs a command that prints fresh headers on
    every connection, with no caching — how Kerberos and internal
    SSO get reached. It gets ten seconds to answer, and what it
    runs is arbitrary shell, so it belongs only in a trusted folder
  + The trap: picking whichever option was quickest to set up rather
    than the one that survives the hours nobody is watching it

- Tool search and output limits
  + Tool search is on by default: only a server's name and
    instructions load at startup, with the full schema for any
    given tool fetched only once Claude is actually about to call it
  + What it unlocks: a dozen MCP servers configured at once cost
    almost nothing to start, where loading every schema upfront
    would have spent context before a question was even asked
  + `MAX_MCP_OUTPUT_TOKENS` caps what a single call may return, at
    25,000 tokens by default, with a warning once a reply passes
    10,000
  + The trap: a call that returns something large — a full case
    file, an entire log — gets cut at that ceiling, past a point,
    with nothing asked to filter or page it first
  + `ENABLE_TOOL_SEARCH=false` reverts to loading every schema
    upfront. Worth knowing the switch exists, not worth reaching
    for on a setup that is already working

- Timeouts
  + A job left running overnight that fails has usually hit a
    timeout, not the work itself, and there are four separate
    clocks it could have hit
  + `MCP_TIMEOUT` allows 30 seconds for a server to start — a
    slow-starting server needs this raised before anything else
    about it is touched
  + A per-server `timeout`, in milliseconds, bounds how long one
    whole call is allowed to run
  + HTTP servers carry their own 60-second timer on every request,
    on top of whatever the per-server setting allows
  + Idle timeout closes a connection nobody has used: five minutes
    for a remote server, thirty for a local one
  + What it unlocks: matching an overnight failure to the clock
    that actually killed it, instead of guessing at the cause

- MCPs in unattended sessions
  + A project-scoped server in `.mcp.json` normally prompts before
    it loads, asking you to confirm that a repository you opened
    gets to run its own tools
  + Under `claude -p`, inside an SDK session, and in a cloud
    session, there is nobody there to answer that prompt, so the
    server loads without asking
  + State it as a security fact, not a convenience: anyone who can
    add an entry to a repository's `.mcp.json` gets it running,
    unattended, the moment that repository is opened non-interactively
  + `disabledMcpjsonServers` keeps a named server out regardless.
    Cutting off project-level settings entirely is the harder
    switch, for a process that should trust nothing from the
    checkout it is working in
  + Managed MCP is the same control at enterprise scale — a
    system-level file that fixes what is allowed to load, set by an
    administrator rather than by you. Worth knowing it exists; the
    decisions it makes are somebody else's

- Driving a browser headlessly
  + A browser-driving MCP server — Playwright is the name to know —
    is one more entry on the same menu as any other server: no
    window opens, nothing to watch, added and scoped the same way
  + What it unlocks: a page with no API gets its content pulled the
    same way any typed tool is called, and the result — text, a
    screenshot, a structured extract — comes back as a tool result
    rather than something read off a screen
  + No display is needed at all, which is why this is the browser
    option that still works in an unattended run or a cloud
    session, where there is no screen to open a window on
  + The trap: nothing about the run is visible while it happens. A
    page that behaves unexpectedly, a form that failed to submit, a
    CAPTCHA — none of it is caught until the result comes back
    wrong, because there is no window to notice it in
  + Where it earns its place: a page plain enough that no eyes are
    needed on the run — checking a listing, extracting a table,
    confirming a status — not a filing you would want to watch
    happen

- When an MCP breaks
  + The single most common malformed config: an entry with a `url`
    and no `type` is skipped outright, with nothing that announces
    which entry or why
  + A server that will not start looks identical, from the
    conversation, to a server that was never loaded. The first sign
    of either is that its tools are not on the menu
  + An empty tool list is not proof a server is broken. Under tool
    search it can mean the server started and genuinely has nothing
    to offer until something more specific is asked of it
  + The distinction worth holding onto: a server that failed leaves
    some trace of the attempt; a server that was never loaded —
    wrong scope, disabled, missing from configuration entirely —
    leaves none. Telling the two apart is where to start looking
  + What it unlocks: asking Claude to check what actually loaded and
    list it out, rather than assuming a missing tool means the
    capability does not exist
</content>

### Browser and Screen Control

- What Chrome control is
  + Chrome is an extension that drives a browser you can see, one of
    two ways Claude works a graphical interface instead of an API
  + It clicks, types, navigates and reads a real Chrome window, the
    same window you would use, rather than calling an endpoint
    somebody documented
  + What it unlocks: any site with no API and no clean way in through
    the terminal becomes something Claude can operate directly
  + The companion capability, computer use, drives the whole desktop
    by screenshot rather than one browser — a different tool for when
    the graphical interface is not a webpage

- The browser's own login
  + Chrome shares the browser's own login state, and that is the
    entire reason to prefer it over `curl`
  + Anything you are already signed into, Claude reaches without a
    credential of its own — no password typed into a prompt, no API
    key issued for a system that does not offer one
  + What it unlocks: a site you log into by hand once and Claude
    operates from inside that same session afterwards
  + Nothing is exported or stored for Claude to use later — the
    access lasts as long as the browser session that is signed in

- The portal with no API
  + The use case: a portal behind a login with no API, which
    describes most court and government systems
  + A page that renders nothing until its JavaScript runs, a form
    that must be filled and submitted, a filing whose confirmation
    exists only on screen — none of it reachable by any other route
    this course teaches
  + It runs in a visible window in real time, so a filing in progress
    is a filing you can watch rather than a job running unseen
  + It pauses and hands control back to you for a login page or a
    CAPTCHA — the parts a browser cannot click through on its own
  + Read-only calls — reading the page, searching it, a screenshot —
    go through without a prompt; clicking, typing and navigating ask
    first

- Computer use
  + Computer use is a built-in MCP server that drives the whole
    desktop, screenshot by screenshot, rather than one browser window
  + macOS and Windows only, and only on a Pro or Max subscription
  + Approval is per application per session, and only one session
    machine-wide can hold control at a time
  + Not available under `-p` at all — an unattended run cannot reach
    for it
  + Escape aborts a run in progress, and the terminal Claude is
    running in is hidden from its own screenshots
  + Shown, never required — every ceiling above is the point, not a
    caveat to work around

- Reach for these last
  + The ladder: an MCP server first, then Bash, then Chrome, then
    computer use
  + An API is faster, cheaper and does not break when a button moves
    on a page or a menu shifts on a desktop
  + Screen control is what you use when there is nothing behind the
    screen — no API, no endpoint, no file to script against
  + The judgement is the whole article: reach for a connector or a
    server before reaching for a screenshot

### Connectors

- What a connector is
  + A connector is an MCP server somebody else runs, added by ticking
    it on at `claude.ai/customize/connectors` rather than at the
    command line
  + Not a different technology from an MCP server you configure
    yourself: the same protocol, the same tools, a shorter install,
    and no config file touched
  + Because a connector is remote it is reached over HTTP, and
    because the authorisation happens on Anthropic's side rather than
    yours, it is the only way to reach a service that refuses a local
    OAuth round trip — Gmail, Google Calendar, Microsoft 365, Slack
  + What it unlocks: read the calendar to find a hearing date, pull a
    client's thread out of Gmail, check what a shared Drive folder
    now contains, post the outcome of a run into a Slack channel

- Turning one on
  + The tick at `claude.ai/customize/connectors` is the install —
    there is no config file to edit and nothing to add on the
    command line
  + Because the server is remote, nothing is installed on your own
    machine
  + Authorisation happens in the browser, on Anthropic's side, rather
    than as a local OAuth round trip run from your terminal
  + The tick is made once, against your claude.ai account, not once
    per project

- The subscription condition
  + Connectors load only when the session is signed in with a
    claude.ai subscription
  + Set `ANTHROPIC_API_KEY`, use an `apiKeyHelper`, hold a
    `claude setup-token` token, or run through Bedrock, Vertex or
    Foundry, and connectors silently do not appear — no warning, no
    error, an empty list
  + They ride on the claude.ai session token. When that lapses, the
    connector reports itself rejected
  + Re-authorising the connector does not mend a lapsed login — the
    login itself has to be renewed by a person
  + The ceiling this leaves: a connector can be reached for, but an
    unattended job must not assume one is there

- Precedence
  + A server you configured yourself under the same name wins over a
    connector, which sits at the bottom of the stack
  + The match is made by endpoint URL, not by name, so a name clash
    is not what settles it
  + When your own server and a connector point at the same endpoint,
    yours is the one that answers
  + What it unlocks: a connector that behaves badly can be overridden
    without turning it off, by configuring your own server against the
    same endpoint
  + The trap: because the match is on the endpoint and not the name,
    renaming your own server changes nothing, and two entries you
    believe are separate may be the same one

### Channels

- What a channel is
  + An MCP server that pushes events *into* a running Claude Code
    session from outside, so Claude reacts to something that happened
    elsewhere
  + Every other integration has Claude reaching out; a channel is the
    one where the world reaches in
  + What it unlocks: a webhook from a case system arrives and Claude
    acts on the status change, a message from your phone steers a run
    already in progress, a job finishes and reports, an approval is
    granted from a train
  + A channel is not a notification. Notifications are you being
    reached when you are away from the machine; a channel is the
    world reaching a session that is open and working right now

- The channels there are
  + Telegram, Discord and iMessage ship as plugins
  + A webhook receiver listens on a local port for anything that can
    POST — the general-purpose one, for a case system or any other
    service that can send a request
  + Requires an Anthropic login. Unsupported on Bedrock, Vertex and
    Foundry
  + Blocked by default on Team and Enterprise until an owner enables
    it

- Switching one on
  + Installed as a plugin, then configured with a token before it can
    receive anything
  + Named on the command line for the session — that is what actually
    turns a channel on
  + The trap: being listed in `.mcp.json` is not enough. A channel
    that is configured but never named on the command line receives
    nothing, and nothing tells you that is why
  + Off by default otherwise, deliberately — an unnamed channel is a
    channel that cannot reach the session at all
  + Events arrive only while a local session is open — not the web,
    not the desktop app
  + An always-on channel means a session parked in tmux, or left
    running as a `-p` worker, for as long as you want it listening

- Two-way and the permission relay
  + Two-way only if the channel offers a reply tool — some channels
    receive only, and cannot be steered back
  + Where it does, a message from your phone can redirect a run that
    is already under way
  + The permission relay goes further: an approval prompt appears
    both in the terminal and on the channel at once
  + Whichever answers first wins — approving from a train while the
    terminal sits untouched is the same as approving at the keyboard

- Gating the sender
  + The rule is not optional: gate on the sender's own ID, never on
    the room
  + Gate on the room instead and anyone who can reach that room is
    putting text in front of Claude, not only the people you meant to
    hear from
  + The same is true of the webhook receiver: anyone who can reach
    the endpoint is putting text in front of Claude, whether or not
    they should be able to
  + An ungated channel is a prompt-injection hole with an address —
    say it that plainly, not softened as a caveat
  + This is the one check every channel needs before it is trusted
    with anything, whatever else about it is left loose

### Deep Links

- What a deep link is
  + A deep link is a URL that opens Claude Code in a new terminal
    window with the prompt box already filled in — the scheme is
    `claude-cli://open`
  + It carries a prompt, an absolute working directory, and a GitHub
    `owner/name` repository slug resolved against clones Claude Code
    has already seen
  + What it unlocks: a link in an alert that opens a session pointed
    at the thing that broke, a runbook where each step is a link
    rather than a paragraph you copy, a dashboard row that becomes an
    investigation in one click
  + It never runs on its own — the prompt lands in the box, and a
    warning that the text came from an external link stays visible
    until you press Enter
  + That is the design, not a limitation: it is the hand-off point
    between an automation that noticed something and a human who
    decides

- Firing one
  + It fires from anywhere the operating system can open a URL —
    `open` on macOS — so any script can produce one
  + The handler registers itself the first time you type a prompt in
    an interactive session, and a setting stops it registering at all
  + The trap: sites that strip unknown URL schemes render the link as
    plain text instead of a working link — GitHub Markdown among them
  + Put the link inside a code block and it stays copyable even on a
    page that will not fire it

### Credentials

- Where keys should live
  + An automation reaching a dozen services needs a dozen credentials,
    and every one written into a config file, a script or a repository
    is a liability sitting in the open
  + What it unlocks: an unattended job at 3am that needs an API key,
    with nobody there to type a password, because the key lives
    somewhere the job can fetch it rather than somewhere you pasted it
  + A database password shared across several scripts lives in one
    place, so rotating it means changing it once rather than editing
    six files
  + The same principle keeps a key out of a repository that later gets
    shared — the key was never written into a file that could travel
    with it
  + The rule underneath all four cases: a secret is fetched at the
    moment something needs it, not stored in every place that uses it

- The keychain, direnv and password managers
  + Keychain, already on your Mac, holds a password and hands it back
    only to the process that asks for it correctly, with nothing
    written to disk in the clear
  + An `.env` file kept out of version control, loaded automatically by
    `direnv` the moment you enter a project folder, is the working
    answer for a script that needs a handful of values
  + Bitwarden or 1Password, driven by their own command-line tool, is
    the answer once the number of credentials outgrows what a keychain
    entry or an `.env` file comfortably holds
  + Vault or a cloud provider's own secret manager is the serious
    version, built for a team spread across many machines — not what
    you need
  + Whichever of these you use, a script asks for a key by name and is
    handed it back; it does not keep its own copy

- Keys and the transcript
  + The trap specific to Claude Code, stated flatly: a key pasted into
    a prompt, a `.env` file read into context, or a credential typed on
    a command line ends up in the transcript
  + Transcripts persist on disk once the session ends — a secret typed
    into one is not a moment that passes, it is a record that stays
  + The fix is timing, not care: fetch the secret at the moment of use,
    inside the process that needs it, and never hold it in the
    conversation itself
  + What it unlocks: asking Claude to write and run a script that
    reaches a service without ever telling Claude the key
  + The same caution covers anything else read into context for an
    unrelated reason — an email, a document — that happens to contain a
    credential

- apiKeyHelper and sandbox credentials
  + `apiKeyHelper` produces the key at the moment Claude Code connects,
    by running a command, rather than storing the key anywhere Claude
    Code itself holds it
  + What it buys: the key never sits in a settings file waiting to be
    read, copied or committed by mistake
  + `sandbox.credentials` goes further for a sandboxed process, denying
    or masking credentials from it entirely
  + What it buys: a process you do not fully trust runs without ever
    being handed the keys that would let it do damage
  + Both are Claude Code's own machinery for the same problem the rest
    of this subsection solves by hand — keep the secret out of reach of
    anything that does not need it at that instant

## Databases

### Why Database Anything

- What a database is
  + A folder of files answers one question: where is this document.
    A database answers questions a folder cannot
  + Which matters are still open, and which of ten thousand letters
    mentions a covenant — questions like these have no folder
    answer, only an open-every-file answer
  + A database holds the same facts as a matter, a client, an
    invoice — as records to ask about together, not files to open
    one at a time
  + Several shapes of database exist, suited to different kinds of
    question
  + The trap: a database is a shape for facts, not a guarantee they
    are correct or current. It answers confidently and wrongly the
    moment what it holds stops matching what is true

- Why put your own files in one
  + The matters, clients, invoices, correspondence and scanned post
    already on the machine become something that answers questions,
    instead of something searched through one folder at a time
  + Nothing is thrown away and nothing moves: the files stay exactly
    where they are. The database holds facts about them and points
    back to them
  + The forty scanned letters landing in the intake folder each
    morning stop being forty things to search and start being forty
    entries you can ask about the day they land
  + What it unlocks: what you billed a client per month for three
    years, or when a deadline first appeared in the correspondence —
    answered by asking, not by opening every file in a matter
  + The trap: a database answers only what has been entered into it.
    A letter filed but never recorded is invisible to every question
    asked afterward

- SQLite first
  + SQLite is one file, no server, nothing to install. It ships
    inside Python already
  + It is the default for anything living on one machine: your own
    matters, your own invoices, your own correspondence
  + The honest position: install nothing else until a second machine
    needs to reach the same data. That is the one condition that
    changes the answer
  + Reaching for a server-based database before that point solves a
    problem you do not have yet, at a cost — installation,
    configuration, something else running in the background — you
    do not need to pay
  + You ask Claude to build the database and put your files into it.
    Naming SQLite is enough; the file itself, and what goes in it,
    is Claude's work, not yours

### Relational

- Relational databases
  + Records with fixed columns, and relations between those records
    — a client has matters, a matter has invoices, and the database
    holds the connection rather than you holding it in your head
  + It is the shape your own material already has: matters, clients,
    invoices. A relational database does not ask you to think
    differently, only to make that shape explicit
  + What it unlocks: every unpaid invoice across every open matter
    for a client, answered directly, rather than opened folder by
    folder to add up by eye
  + The trap: getting the connections wrong is not a typo to fix —
    it means reshaping the records that already went in, not
    renaming a folder

- PostgreSQL
  + The serious open-source database server, and the step up from a
    single SQLite file once a second machine needs to reach the same
    data
  + It also handles JSON, full-text search and vectors, so one
    Postgres instance often covers three separate kinds of database
    that would otherwise need three separate tools
  + What it unlocks: several people, or several automations, reading
    and writing the same matters and invoices at once, safely
  + A server is a standing thing rather than a file — something has
    to keep it running, unlike SQLite, which sits on disk until
    opened
  + The trap: nothing answers while the server is not running, so an
    automation that worked last night can fail silently after a
    reboot with nobody there to notice

- DuckDB and the others
  + MySQL and its fork MariaDB are older and hugely deployed, mostly
    sitting behind websites — something you inherit already running,
    not something you choose to start with
  + SQL Server and Oracle are commercial and licensed, built for
    organisations with a database administrator on staff — named so
    you recognise them, not so you install them
  + DuckDB has SQLite's shape, one file and no server, but is
    columnar rather than row-based, and reads CSV and Parquet files
    directly without a separate import step
  + What it unlocks: a question answered across a folder of exported
    spreadsheets or court data dumps without loading them into a
    database first
  + None of this is a decision to make. For one practice on one
    machine, SQLite and Postgres already cover it, and the rest is
    here to be recognised, not adopted

### The Other Kinds

- Document databases
  + A document database stores whatever shape a record happens to be
    in — a scraped web page, an API reply — rather than forcing every
    record into the same columns before you save it
  + What it unlocks: you save a result before deciding its structure,
    so a new field on next week's version of the same API does not
    break anything already stored
  + Use case: the raw output of a nightly pull from a court listing
    or a filing service, where every source hands you back a
    different set of fields
  + The trap: nothing enforces a shape on the way in, so a typo in a
    field name is not an error — it is a new field, silently sitting
    next to the one you meant
  + The path: a JSON column inside SQLite or Postgres holds the same
    documents without a second database to run

- Key-value stores
  + A key-value store holds one value per key with nothing else
    attached — no columns, no relations, nothing but an answer to
    "have you seen this key before"
  + What it unlocks: a notepad that survives between runs, so an
    archiver checking a message ID every ten minutes does not process
    the same message twice
  + Use case: the same shape covers an expensive lookup you do not
    want to pay for twice, a "job already running, do not start
    another" flag, and a count of how many letters arrived today
  + The trap: nothing forgets on its own — every key you write is a
    key that sits there until you explicitly clear it
  + The path: a two-column table in SQLite does this on one machine
    with nothing installed; reach further only when several processes
    need to share the same notepad at once

- Columnar databases
  + A columnar database answers a question about every row at once,
    rather than fetching one row at a time and reading it whole
  + What it unlocks: a relational database reads a whole row to get
    one column out of it; a columnar one reads only the columns you
    asked about, which is why the same question often runs a
    hundred times faster
  + Use case: totalling what you billed per client per month across
    three years of invoices, or finding which hours in a year of logs
    were errors
  + The trap: the same speed advantage makes it a poor fit for
    fetching one record at a time — asking for a single client's
    single invoice is the slow case here, not the fast one
  + The path: SQLite or Postgres until a question that touches every
    row of three years of invoices takes long enough to notice

- Graph databases
  + A graph database stores connections as the primary thing, not
    records with connections bolted on — who owns whom, who is
    related to whom, what depends on what
  + What it unlocks: a question like "everyone connected to this
    person within four steps" is direct to ask in a graph and painful
    to express as a relational join
  + Use case: tracing a corporate ownership chain, running a
    conflict-of-interest check across your client base, or mapping
    family relationships in an immigration matter
  + The trap: the appeal is the depth of chain it can follow — a
    graph built for three matters answers the same simple lookups a
    spreadsheet already gives you, no faster
  + The path: SQLite's own recursive queries reach four steps out
    without a second database — install a graph engine once the
    chains themselves, not the record count, are what slows you down

- Time-series databases
  + A time-series database stores the same measurement taken over and
    over, each one stamped with when it happened
  + What it unlocks: questions shaped by time — what this looked like
    last Tuesday, what the daily average is, when it spiked — answered
    by a database built to keep summaries and discard old detail
    rather than hold on to every reading forever
  + Use case: tracking what an automation costs you per day, how long
    each overnight run took, or a rate that changes month to month
  + The trap: without deciding what to discard, "keep everything"
    quietly becomes the retention policy, and the table meant to
    summarise years of readings ends up holding every one of them
  + The path: a timestamp column in SQLite covers most of this — a
    dedicated engine earns its place once the readings themselves,
    not only the questions about them, arrive continuously

### Search

- Full-text search
  + grep opens every file every time and matches only the exact
    letters you typed — misspell a name or use the wrong tense and
    a document that is there does not surface
  + An index is built once and after that answers instantly, ranks
    the best hits first, and knows that filed, filing and files are
    the same word
  + What it unlocks: every letter and pleading in an archive going
    back decades, searchable on a half-remembered phrase rather than
    the exact wording it was written in
  + SQLite FTS5 is already inside SQLite — start there. Postgres
    does the same job through `tsvector` if the matter is already
    sitting in Postgres for another reason
  + Tantivy, Meilisearch and Elasticsearch are standalone search
    servers built for a scale an archive of matters does not reach —
    almost certainly not needed
  + The trap: an index goes stale. A pleading filed this morning is
    invisible to search until something rebuilds the index, and nothing
    announces that it has not happened yet

- Vector search
  + Full-text finds the word typed. Vector search finds the meaning —
    it locates the clause about ending the agreement early even
    though the clause never uses the word termination
  + Mechanism: a model turns each document into a list of numbers,
    and documents with similar meaning end up with similar numbers.
    The search is for what sits nearby, not for what matches exactly
  + What it unlocks: a question phrased in your words finds a
    document phrased in someone else's — the clause found by what it
    does rather than by the term the drafter happened to choose
  + sqlite-vec extends SQLite the way FTS5 does — start there.
    pgvector does the same for Postgres, so a database already doing
    full-text can be asked to do this too without adding software
  + Chroma, Qdrant and LanceDB are standalone vector databases, built
    for a scale an archive of matters does not reach — almost
    certainly not needed
  + The trap: change the model that turns documents into numbers and
    every number already stored is now meaningless against new
    queries. Nothing announces this — the search keeps answering, only
    worse, until the whole archive is turned back into numbers again

- Retrieval in practice
  + No model can be handed ten thousand documents at once, however
    large its context. Retrieval is the step in between: find the six
    passages that are actually relevant, and hand only those to the
    model
  + What it unlocks: an archive of any size becomes something a
    question can be put to. Ten years of correspondence answers a
    question the way ten emails would, because ten emails is what the
    model is actually shown
  + Full-text and vector answer different questions, and a retrieval
    setup commonly wants both — full-text for a name, a reference
    number, a citation typed exactly as it appears; vector for a
    clause or an argument raised in words that never appear in the
    document being searched for
  + The honest limit: an answer built on the wrong six passages reads
    exactly as confident as one built on the right six. Nothing in
    the wording of the answer shows which one happened
  + The trap: the archive can hold the answer while retrieval misses
    it entirely. That is a failure with no error message and no red
    text — not the model reasoning badly, but the model never being
    shown the material that mattered

### With the Harness

- Getting your material in
  + Your material arrives as scanned post with no text layer,
    exported PDFs, Word documents, spreadsheets and email — none of
    it already shaped like a table
  + Getting it in means three things: extracting the text, deciding
    what each document is, and recording where the original still
    lives
  + A scan gives up its text as a separate step, before any of this
    starts
  + The database holds what makes the material answerable; the
    original file stays where it is and is never replaced
  + What to ask for: point Claude at the folder and ask it to build
    the thing that reads it, not a description of the tables you
    want
  + The trap: a document that fails to import fails silently — it
    is not in any answer, and nothing in the answer says so

- Asking questions of your own data
  + Once the material is in, the questions you could not previously
    ask become ordinary
  + Which of ten thousand letters mentions a covenant, what a
    client cost per month for three years, which matters have had
    no activity in ninety days
  + You ask in English; Claude writes the query
  + The relational, columnar and full-text pieces already covered
    are what answer these questions — this is what they were built
    for
  + The trap: Claude writing the query means the query can be wrong
    in ways the answer never reveals
  + A number that looks right is not evidence it is right — ask to
    see what was actually counted

## Automatic Outputs

### Document Automation

- Document pipelines
  + Document pipelines are commands, not libraries: poppler, tesseract,
    pandoc and LibreOffice headless are each run, one after another, not
    imported into code
  + What it unlocks: a scanned document is a picture and nothing can read
    it. OCR turns it into text, and once it is text, everything else you
    already know how to ask Claude for applies to it
  + The archive it opens up: a twenty-year run of scanned post,
    correspondence and pleadings goes from a shelf of images to
    something searchable by a half-remembered phrase
  + Together, these tools run in both directions: a document becomes
    something Claude can read, and Claude's own output becomes a document
    a client or a court will accept
  + The trap: a PDF exported from a system already carries real text
    inside it; a PDF made by scanning paper does not. The two look
    identical on screen and need different tools

- poppler and pdftotext
  + poppler reads PDFs, and pdftotext is the part that matters most: it
    pulls the text straight out of a PDF that already carries a text
    layer
  + What it unlocks: the text of a filed pleading or a bundle exhibit,
    out in seconds, ready to search or hand to Claude, with no retyping
  + poppler also splits a bundle into single pages, merges pages back
    into one document, and renders a page as an image — pulling a
    document apart and putting it back together with the same tool
  + Running pdftotext against a document doubles as the test for which
    kind it is: text comes back and the PDF already had a layer; nothing
    usable comes back and it is a scan, headed for OCR instead
  + Reach for pdftotext first. Most PDFs that cross your desk — anything
    drafted, exported or filed electronically — already carry a text
    layer and need nothing more than this

- tesseract and OCR
  + tesseract is OCR: it looks at a scan with no text layer and produces
    the text that is written on it
  + What it unlocks: the forty scanned letters that land in an intake
    folder each morning, a faxed order, an exhibit that arrived as a
    photograph — each becomes text Claude can read rather than a picture
    it cannot
  + The trap: OCR on a poor scan produces confident wrong text. A
    smudged date or a folded signature becomes a plausible-looking wrong
    one, and nothing downstream flags it
  + The other trap: a PDF that already has a text layer does not need
    OCR, and running tesseract on it anyway replaces good text with
    tesseract's guess and makes the document worse
  + Check which case you are in before running OCR at all, rather than
    running it on everything as a habit

- pandoc
  + pandoc converts between text formats: Markdown to DOCX, DOCX to
    Markdown, HTML to PDF, and most pairings built from text
  + What it unlocks: a letter Claude drafts in Markdown becomes a DOCX a
    secretary can mark up in Word, and a DOCX that arrives from someone
    else becomes Markdown Claude can read and edit directly
  + The trap: converting into a format loses whatever that format cannot
    express, and the loss runs one way. Markdown holds no page numbers,
    headers, footers or tracked changes, so a DOCX put through it comes
    out stripped of them, and pandoc cannot add back what a plainer
    format never held
  + Choose the format for what has to survive the conversion, not for
    convenience — a document that must keep its letterhead is not a
    Markdown-to-DOCX job

- LibreOffice headless
  + LibreOffice headless is Word and Excel with no window: the same
    programs, driven from a script rather than clicked through
  + What it unlocks: a DOCX Claude has drafted or edited becomes a PDF
    for filing or emailing, without anyone opening Word to run an export
    by hand
  + Reach for it over pandoc when the original formatting, styles and
    layout have to survive exactly — LibreOffice reads the file the way
    Word itself would
  + It handles Excel the same way: a spreadsheet of costs or time
    entries converts to PDF or to a plain format from a script, on a
    schedule, with nobody at the machine
  + The trap: it is still office software underneath. A document built
    on a macro, an unavailable font, or an unusual template renders
    differently than it did in Word or Excel on your own laptop

### Templates

- Templating
  + A template is a document with named holes, filled from data —
    an engagement letter with the client's name and the matter
    type left for filling, written once and used for every client
  + The point is not saved typing: the model does not draft the
    boilerplate, it only supplies the values, so the wording that
    was approved cannot drift between one use and the next
  + An engagement letter filled a hundred times from a hundred
    rows says exactly what it said when it went through approval,
    on the first fill and on the hundredth
  + The trap runs the other way too — anything the model drafts
    freely can come out differently each time, and in a document
    that has already been through compliance that is not a small
    thing
  + What it unlocks: a precedent letter, a standard notice, a fee
    estimate — held once as approved wording and produced again
    for every new matter without retyping or re-approving it
  + The values that fill the holes come from somewhere already —
    a matter record, an intake form — the template only places
    them where they belong

- Jinja and docxtpl
  + Jinja is the templating engine most Python tooling reaches for
    — the thing that reads a document with holes and a set of
    values and produces the filled version
  + docxtpl applies that to an actual Word document, and keeps the
    formatting: the firm's letterhead, styles and layout survive
    untouched, and only the marked values change
  + What it unlocks: an engagement letter, a client care letter, a
    costs estimate — kept as one formatted Word template and
    filled per matter without retyping or reformatting a single
    one
  + The output is a real, editable Word document, not an image of
    one — it goes back to a colleague or to compliance the same
    way any other letter would
  + You ask Claude to build the filling script; the template
    itself is the asset worth keeping, not the code that fills it

- Filling a form PDF
  + A form PDF already carries named fields built into its
    structure — an immigration form such as the N-400 is the
    clearest example
  + Filling one means putting a value into each named field, then
    flattening the result so the values are fixed and cannot be
    edited or unchecked afterward
  + That is filling, not templating: there is no boilerplate to
    protect, only fields to complete correctly, and flattening is
    what makes the result behave like a signed paper form rather
    than an editable one
  + What it unlocks: an official form submitted with values already
    held for the matter, filled directly rather than retyped by
    hand into the PDF's own fields
  + A PDF built from scratch is the opposite case: it never had
    named fields, so it is templated as a Word document or in
    Typst and only turned into a PDF at the end
  + The trap is treating the two as the same problem — a form PDF
    already has its holes; a blank PDF has none, and needs a
    template built somewhere else first

- Typst and LaTeX
  + Word templating covers a letter; Typst and LaTeX are for
    output that must be properly typeset — a pleading bundle, a
    contract, anything where the layout itself has rules
  + Typesetting buys exact page breaks, running headers that stay
    consistent, and clause numbers and cross-references that
    renumber themselves when a clause is inserted or removed
  + The same argument as templating still applies: the fixed
    structure and numbering are the approved form, and the model
    still only supplies the values that go into it
  + Typst is the newer of the two and increasingly the first one
    asked for — plainer to read, faster to produce a result from
  + LaTeX is the older, more established choice, with decades of
    use behind it and a house style or class file already built
    for many kinds of formal document
  + The trap: reaching for a typesetting engine for an ordinary
    letter is more than the job needs — it earns its place only
    where a Word document's layout would need constant fixing by
    hand to stay correct

### Artifacts

- What an artifact is
  + An artifact is a self-contained web page Claude Code publishes
    from a session to a private URL on claude.ai
  + One HTML file, styles and script inline, with no server behind it
  + What it unlocks: the cheapest way for work to leave the terminal
    and become something a person can open — a matter status page for
    a client, a summary of an overnight run someone else needs to
    read
  + Also a chart of what was processed this month, or a checklist
    that fills in while a long job proceeds
  + Requires a paid plan and a login on the Anthropic API — not
    Bedrock, Vertex or Foundry

- Publishing and revising
  + Publishing prompts once per artifact, and the URL it produces is
    the one that lasts
  + Revising means editing the file and publishing again to the same
    URL — anyone with the page open sees it change
  + Each publish is kept as a version
  + The trap: from a later session, hand Claude the URL, or you get a
    second artifact instead of an update
  + Private to you on creation. Pro and Max share by link to anyone;
    Team and Enterprise share inside the organisation, with public
    links off until an owner turns them on

- Connectors inside an artifact
  + A page may call connectors when it loads
  + What it unlocks: a status page fetches its own fresh data every
    time it is opened, using the viewer's connectors and the viewer's
    account
  + The automation that built the page does not have to run again to
    keep it current — the page does the asking, each time someone
    looks
  + Two people opening the same status page can see two different
    results, each drawn from their own connectors and their own
    access
  + The trap: a client with no connectors of their own opens a page
    that cannot fill itself in, and you, opening the same URL with
    your own connectors working, will never see it happen

- The content policy
  + Every external script, stylesheet, font and image is blocked
  + So is all fetch, XHR and WebSocket traffic
  + Everything is inlined, or it does not load
  + Sixteen megabytes is the ceiling on the one file
  + It is what makes an artifact a page, not an application

### Static Sites

- Static site generators
  + Mechanism: a generator turns a folder of Markdown into a finished
    website — plain HTML files, no server logic, nothing running
    behind the pages at all
  + Because the output is just files, they work wherever they are
    put — copied to a folder, dropped on a host, moved without
    touching a database or a config
  + Hugo, Zola, Eleventy and MkDocs do the conversion; GitHub Pages
    hosts the result at no cost
  + What it unlocks: an internal reference built from your own notes,
    or a published version of something like a course, produced
    without running a web server
  + The trap: a site put up this way is public the moment it is
    hosted, unless something is put in front of it to restrict who
    can reach the address

- Publishing what an automation makes
  + Why this is the cheapest way for an automation to put something
    in front of a person: an overnight job writes Markdown, the
    generator turns the folder into a site, and the site is files
    that can sit anywhere
  + Concrete: a client-facing status page an automation regenerates
    nightly, current by the time you open your laptop and without
    you having built or sent anything
  + Nothing runs when the page is opened — the visitor is reading
    files a job already produced, not waiting on a program that
    answers on demand
  + The trap: a page rebuilt nightly from live material publishes a
    mistake exactly as readily as a correct result. Nobody sits
    between the automation and whoever opens the page
  + What to ask Claude for: point it at where the Markdown is written
    and which generator to run, and let it wire the regeneration
    together — not at the HTML or the site's layout

## Hosting and Serving

### Web Servers

- What a web server is
  + A web server is a program that listens on a port and sends back
    an answer to whatever asks it — a browser, another program, a
    script triggered on a schedule — the same job whoever is asking
  + What it unlocks: a front door that opens on its own. A client
    filling in a form, or another service calling a URL the moment
    something happens, starts work on your machine with nobody sat
    at the keyboard
  + Answering a request can mean handing back a file unchanged, or
    running code that decides the answer — a page that accepts a
    submission, writes files and starts work is the second kind
  + A web server on your own machine, by default, only answers your
    own network — reaching it from the open internet is a separate
    matter, decided by whatever sits in front of it
  + The trap: a web server only opens the front door while it keeps
    running. Stop it, even by accident, and the form is gone with
    nothing telling you so

- Reverse proxies
  + A reverse proxy sits between the internet and your web server,
    taking every request first and deciding what happens to it
    before your own code ever sees it
  + What it unlocks: several separate services — the intake form, a
    status page, a small API — answered from one address, each one
    routed to the right service behind the scenes
  + It carries the HTTPS certificate, so your own web server never
    has to know how to encrypt a connection or renew one
  + It refuses what you did not invite — traffic aimed at names or
    addresses you never set up is turned away before it reaches
    anything of yours
  + The trap: a reverse proxy is one more piece between a client and
    your form. When something breaks, the fault is either its
    routing or the page behind it, and a browser error does not say
    which

- Caddy, nginx and certificates
  + A certificate is what turns a plain address into one a browser
    marks as secure. Without it, a client's browser warns before the
    form even loads
  + Caddy gets a certificate the first time it starts serving an
    address, and renews it again on its own, with nothing further
    asked of you
  + nginx is the standard, running behind most things at scale, but
    it treats the certificate as a separate step rather than
    something it does for you by default
  + What to ask for: a form or address needed in a hurry is Caddy's
    case. An existing setup already running nginx is not worth
    replacing for it
  + The trap: a certificate belongs to a domain name, not a machine.
    Point the name somewhere else and the certificate has to be
    fetched again for wherever it now lands

- Tunnels
  + The problem a tunnel solves: your machine needs a name and an
    address reachable from outside, without opening every port on it
    to get one
  + It works by running an outbound connection from your machine
    out, and handing back an address that reaches your machine
    through that connection — nothing is left open for the internet
    to find on its own
  + What it unlocks: a form, an API, or a status page reachable from
    outside a home network or office, with no fixed address, no
    router reconfigured, and no hosting account
  + Tailscale is the name to start with — a private network between
    your own devices and whatever is serving, reached by name rather
    than by exposing anything to the open internet at all
  + The trap: a tunnel changes how the machine is reached, not what
    is listening on it. Whatever your web server would answer to a
    stranger, it still answers to whoever the tunnel lets through

- Self-hosting
  + The machine is the website — nothing else. A client's browser
    connects to it directly, and the files a submitted form carries
    land on your own disk, with no third party holding a copy in
    between
  + A domain name is worth about ten pounds a year, and it points at
    your own machine exactly as well as it points at a host's — a
    name is memorable where a number is not, and it keeps working
    when a home address changes underneath it
  + What paid hosting sells past that is someone else's electricity,
    a connection that does not drop, and blame that lands elsewhere
    when it breaks
  + For a form only you depend on, your own machine is fine, on one
    condition: it has to stay awake

- A worked example — the intake form
  + A small web server on your own machine serves one page — name,
    matter type, upload a passport scan — with nothing else running
    behind it yet
  + Caddy fronts that page with a proper HTTPS address to send to a
    client, so the form looks like any other secure page a client is
    asked to fill in
  + Submitting it writes the files into a case folder, adds a row to
    a database, and drops a job in a queue — three separate records
    of one event, each doing a different job
  + Something already watching the queue picks the job up and runs
    Claude against the intake skill, which reads the uploaded
    documents, extracts the details, and drafts the engagement
    letter
  + What comes back to you is not a notification to act on. It is a
    drafted letter and a filed matter, waiting the next time you
    look
  + The trap: a front door is a door. Anything reachable from the
    internet gets found and tried, and a form that accepts uploads
    is accepting files from strangers

### Containers

- What a container is
  + A container is a sealed box holding a program and everything it
    needs: its own filesystem, its own packages, its own version of
    Python
  + It runs identically on a laptop, a rented box, or someone else's
    machine, and touches nothing outside itself — a Postgres you
    experiment with vanishes the moment you delete it
  + For Claude Code it is also containment: an agent working inside
    a container cannot damage the machine around it
  + Docker is the tool; a devcontainer is the same idea wired into
    an editor
  + What to ask for: name what the thing needs to run, and let
    Claude write the recipe that seals it in — you do not describe
    the box yourself
  + The ceiling, stated flatly: containers are Linux only — no
    macOS, no Windows

- Images and registries
  + What you build is an image; running it produces a container,
    and one image can produce many identical containers
  + An image travels through a registry: push it from here, pull it
    down there
  + Watch the architecture — the laptop's chip and the rented box's
    chip may differ, so build for the target or build on the box
    itself
  + Services like Cloud Run skip the machine entirely: hand over an
    image and they run it, with no server of your own to manage
  + What it unlocks: the image tested on your laptop is the exact
    thing that runs on the rented box, not a reinstalled
    approximation of it

- Reproducibility
  + Take safety out of the picture and reproducibility is still why
    people reach for a container
  + A container is a written-down recipe of every dependency, so
    what worked in March still works in December, on a machine not
    yet built
  + What it unlocks: two projects needing incompatible versions of
    the same software, sitting side by side, neither disturbing the
    other
  + Also unlocked: trying a piece of software once, deleting it, and
    leaving nothing behind on the machine you tried it on
  + The trap: a container reproduces what is inside it. Anything the
    program reaches outside the box is not covered by that guarantee

- Running one on a box that never sleeps
  + The scheduling problem a laptop cannot solve: an intake pipeline
    that must answer at 3am needs a machine that is awake then, and
    a laptop closed on a desk is not it
  + The answer: install Docker on a rented box, pull the image, run
    it — the dependencies are inside the image, so the box itself
    needs nothing else installed
  + What it unlocks: an automation running on a schedule or waiting
    on events, without your own laptop staying open to provide it
  + The trap: building and running are different acts. A container
    can build a Mac or Windows binary and still not be able to run
    it — and a container is not a virtual machine either

## Agent SDK

### The SDK Harness

- What the Agent SDK is
  + The Agent SDK is the same agent loop that runs Claude Code, packaged
    as a library your own program calls, in Python or TypeScript, rather
    than a thing you sit in front of and type into.
  + The distinction from everything else in this course: there is no
    terminal. Your program decides when a turn starts, sees every
    message the moment it arrives, and can refuse a tool call in code
    before it runs.
  + What it unlocks: Claude stops being an assistant you operate and
    becomes a component another piece of software operates — wired into
    a form, a queue, a phone number, whatever sits in front of it.
  + It is still Claude Code underneath — the same model, the same
    skills, the same CLAUDE.md — wearing a different front door.
  + The trap: the SDK is a library, not a product you switch on.
    Something still has to write and run the program that calls it, you
    or someone you commission — the SDK removes the terminal, not the
    engineering.

- How it differs from headless sessions
  + The prior question, before anything about the SDK itself, is
    whether it is needed at all: a headless session run from any
    language does the non-interactive part already, and can be asked to
    hand its answer back as structured data a program parses rather
    than a paragraph a person reads.
  + That is the cheaper answer, and usually the right one. A program
    that fires a headless session and picks apart the structured answer
    it hands back needs nothing further built.
  + The SDK earns its place only when the program has to step into the
    run rather than wait for its end: approving a tool conditionally,
    showing a user partial output as it is produced, holding one
    conversation open across many exchanges, or billing a customer by
    the turn.
  + The shape of the difference: a headless session is one prompt in,
    one answer out, then gone. The SDK keeps the loop open and visible
    from the inside for as long as the program wants it.
  + The trap: reaching for the SDK because it sounds like the serious
    option. If the program only needs to fire a prompt and collect what
    comes back, the SDK buys nothing a headless session did not already
    give you, at the cost of a program to write and keep running.

- Use cases
  + The back end of an intake form: a client submits documents, and the
    program watches the run and hands back the answer the moment it
    lands, rather than a person opening a session and waiting to be
    told when to look.
  + A service running one agent per customer, each customer's own files
    walled off from every other customer's, all driven by a single
    program rather than a person opening a session per client.
  + Anything with someone waiting on the other end of a connection — the
    thread through every case here. A headless session suits work you
    fire and collect later; the SDK suits work with a person or another
    system on the line while it happens.
  + What it is not for: your own work, at your own machine. Getting
    something done yourself calls for a session, headless or otherwise,
    not a program built to run one on your behalf.
  + The trap: building an SDK program to save yourself typing a prompt.
    That is what a session, or a skill, is for. The SDK earns its keep
    serving somebody else's request, not shortening your own.

### Building an SDK

- Running a query and holding a session
  + Two entry points exist, in either supported language, and the
    choice between them is the first decision your program makes
  + One entry point runs a single question through and returns a
    stream of messages, then ends — nothing is left open afterward
  + The other entry point keeps a session alive across many
    exchanges, and lets your program send an interrupt mid-thought,
    something the single-question entry point has no way to do
  + What it unlocks: the intake form's back end submits a document,
    waits for the answer, then sends a follow-up question into the
    same session minutes later rather than starting the conversation
    over
  + The trap in the single-question entry point: once a run is going
    there is no way into it — no interrupt, no follow-up, nothing to
    do but wait for it to finish and then open a fresh conversation
  + Which entry point to reach for follows from the shape of the
    exchange: one question and one answer, or a conversation that
    keeps going

- The messages that come back
  + What comes back is not a block of text but a sequence of typed
    messages, each one tagged with what kind of thing it is
  + The first message carries the session's own identifying number,
    which is how your program finds this exact conversation again
    later
  + One message arrives for each reply Claude gives, and one for each
    result a tool produced, so a reply can be shown the moment it
    exists rather than after the whole run finishes
  + One trip through a reply followed by its tool results is a turn
  + A final message closes the sequence, carrying the cost, the token
    count, and the session's identifying number together
  + What it unlocks: a status line that updates as the run happens, a
    bill worked out per exchange, a log that records exactly what ran
    and what it cost

- Stopping it running forever
  + Two settings exist to stop a session running forever, and neither
    of them is a clock
  + One counts turns — specifically turns that used a tool — and
    stops once a set number is reached
  + The other watches a running estimate of what the session has cost
    in dollars, and stops once a ceiling is crossed
  + The trap, stated plainly: a session has no overall timeout.
    Nothing ends it on its own, and a session that fits under both
    limits — few tools, low running cost, doing nothing but thinking
    for a long time — carries on indefinitely
  + What it unlocks: a turn limit caps a runaway loop of tool calls,
    and a budget caps what any one customer can cost, but only once
    you set them — the default is neither
  + An unattended program needs both set, since a session stalled
    between the two limits still has to be found and stopped by
    something else watching from outside

- The permission callback
  + Your program can supply a callback that decides, in your own
    code, whether a tool call is allowed to run
  + The trap: it fires only when the decision would otherwise have
    gone to a prompt. Anything already settled by an allow rule, or
    by the permission mode the session is running under, never
    reaches it
  + That is how a callback that looks like a security boundary turns
    out not to be one — a rule settled earlier in the stack waves a
    tool through before the callback ever sees it
  + Six permission modes exist, governing how much is asked versus
    allowed automatically, and the callback sits underneath all of
    them, not above
  + The mode that skips every prompt refuses to start at all when the
    program is running as a root user, and a deny rule outranks it
    regardless of which mode is set
  + What it unlocks: a program that approves some tool calls on its
    own logic and hands the rest to a person, with no terminal prompt
    involved

- One process, many customers
  + The machinery that governs an interactive session — its
    settings, its project instructions, its hooks, its skills, its
    subagents — loads into an SDK session too, unless your program
    shuts it out
  + Shutting it out is exactly what a program running one process per
    customer does, alongside a separate working directory for each
    customer and a separate configuration directory for each
  + The risk it manages, stated plainly: without that separation, one
    customer's files, or one customer's configuration, can reach
    another customer's agent inside the same running process
  + What it unlocks: a single running program serving many customers
    at once, each walled off from what the others have uploaded or
    configured
  + The walling-off is not an afterthought for a service built to run
    one agent per customer — it is the design the whole service rests
    on

- Sessions and where they live
  + A session persists as a file on disk once it exists, kept under a
    projects directory of past sessions rather than living only in
    memory
  + Any session can be resumed later by its identifying number,
    picking the conversation back up where it left off
  + A session can also be forked into a branch: a copy that carries
    the history forward while leaving the original session exactly as
    it was
  + What it unlocks: trying a second approach from the same starting
    point without losing the first attempt, or resuming a customer's
    conversation days later without them repeating themselves
  + The trap: those files live on the machine the program runs on. An
    adapter exists to mirror sessions to S3, Redis or Postgres
    instead, and it stops being optional the moment the program runs
    somewhere that gets rebuilt or replaced rather than sitting on
    one disk permanently

- What it consumes
  + Every run spawns the same program that runs Claude Code as its
    own separate process — nothing lighter, nothing shared between
    runs
  + Twenty customers held open at once means twenty separate
    processes running side by side, not one process serving twenty
  + Reckon on a floor of a gigabyte of memory, five gigabytes of
    disk, and a processor core, for each one running, before any of
    them has done real work
  + The trap: the running cost figure reported at the end of a
    session is an estimate, read from a price table built into the
    program rather than a live figure billed by Anthropic
  + What it unlocks: that estimate is good enough to enforce a budget
    ceiling, but not good enough to put on an invoice to a customer —
    treat it as a guardrail, never as a bill

### Deploying and Integrating SDKs

- The shapes a deployment takes
  + An SDK program is a program. It can sit behind a terminal, a web
    page, a desktop window, or a phone screen, and the person using
    it sees only whichever face you built
  + Nobody looking at that face knows Claude is inside it — no
    terminal, no prompt, no sign that an agent is doing the work
  + Choosing between the four is a question about who is using it
    and where they are, not a question about the agent behind them
  + You alone, at your own machine, want the cheapest face. A
    client who has never opened a terminal wants one that looks
    like every other page or app they use
  + The trap: building the face you already know how to build, not
    the one the person on the other end actually needs

- Behind a TUI
  + A terminal front end wrapped around the same program — text in,
    text back, on the machine you are sitting at
  + The cheapest of the four to build, because it assumes a
    terminal is already open and asks nothing further of whoever is
    using it
  + What it unlocks: a tool for yourself, or for a colleague on the
    same machine, without a window, a browser, or an address to
    hand anyone
  + It goes no further than the terminal it runs in. Anyone reaching
    it has to be sitting at that machine, or already connected to it
  + The trap: it reads as a developer tool even when the person
    using it is not one, and a screen of scrolling text is the
    first thing that makes a colleague decide this is not for them

- Behind a web page
  + A browser reaches it, which means anyone with the address can
    use it, not only someone at the keyboard
  + This is the shape that makes the program reachable by someone
    who is not you and does not use a terminal — a client, a
    colleague in another office, anyone with a link
  + None of that reachability arrives on its own — it needs a front
    door in front of it, and a web page over an SDK program does
    not come with one
  + What it unlocks: a client uploading the scanned post from their
    own end through an address you send in an engagement email,
    while the page itself looks like any other form they are asked
    to fill in
  + The trap: anything reachable by other people is reachable by
    anyone who finds it, whether or not you meant them to

- Inside a desktop app
  + A window with an icon, opened and closed like any other program,
    with no terminal in sight anywhere
  + The point of this shape is that nothing about it announces
    itself as a developer tool — it looks like the accounting
    software or the case management system already on the machine
  + What it unlocks: the colleague down the corridor checking a
    deadline against a matter, inside a window that looks like the
    case system already on their desk, not a program announcing
    itself as something new
  + The trap: it still runs on the machine it is installed on.
    Moving it to another desk, or pushing an update, means doing
    that installing again there, not visiting an address that is
    already current
  + Nothing about the window says whether the agent is running on
    that machine itself or reaching out to one elsewhere — the
    window hides that question, it does not answer it

- On a phone
  + The honest fact first: the agent does not run on the phone. The
    phone talks to something that runs elsewhere and shows what
    comes back
  + What that means in practice: the phone needs a connection to
    reach whatever is doing the work, and without one it has
    nothing to show
  + What it unlocks: approving a step from outside court, or reading
    the finished answer on the train home, not only from the desk
    the program actually runs on
  + The cheapest version of this face is the same web page, opened
    in the phone's own browser, rather than a separate app built
    for the phone
  + The trap: treating the phone as though it is doing the work
    invites confusion the moment the connection drops and nothing
    updates, with no obvious reason why

- Where the process actually runs
  + Every one of the four faces asks the same question behind it:
    where is the program itself actually running
  + Three answers: your own machine, a rented box kept for the
    purpose, or something managed by someone else on your behalf
  + A laptop that sleeps is not a host. The moment it closes or the
    screen goes dark, whatever depends on it stops answering, front
    door or not
  + What it unlocks, once the process runs somewhere that stays
    awake: a client submitting the intake form at nine at night,
    with your own laptop shut on your desk the whole time
  + The trap: mistaking "it works when I test it" for "it works
    when I am not there" — the two only match once the process runs
    somewhere that does not depend on you

- Streaming to someone waiting
  + An agent produces its answer in pieces as it works, not all at
    once at the end, and the front end has to decide what to show
    while that is happening
  + A person watching a blank screen assumes it is broken. Waiting
    without anything changing on screen reads as a hang within
    seconds, whatever is actually happening behind it
  + What it unlocks: a line marking each of forty scanned letters
    as it is read, so the person who submitted them sees the pile
    moving rather than a screen that has not changed
  + This matters most exactly where the person waiting is not you.
    You know an agent is thinking; a client watching their own
    submission does not
  + The trap: a step that takes a long time without producing any
    message of its own — a document being read, a search running —
    still looks like a stall even in a program built to stream

- Keeping it up
  + A deployment behind any of the four faces has to survive a
    restart, a crash, and a machine reboot, none of which wait for
    you to be there
  + Someone else using it raises the stakes further: their session
    has to still be there tomorrow, not only for the run they made
    today
  + What it unlocks, done properly: a client returning next week to
    the same thread about their matter, picking it up mid-way
    rather than explaining the whole thing again from the start
  + The trap that costs money loudly: every person using it costs
    money on every turn it takes, and more people using it is a
    running bill, not a one-off cost
  + The trap that costs money quietly: a run that loops without
    stopping, with a customer attached to the other end, spends
    money the whole time nobody is watching it

### Notifications

- Notification transports
  + The job runs at 3am. Something needs a decision or something
    broke, and without a way to reach you, you find out when you
    next look — which may be days later
  + What it unlocks: a run failed overnight, a document is drafted
    and waiting on your approval, a deadline was detected in a
    letter that landed in this morning's post, twelve matters were
    processed and one could not be
  + A transport is only an address you already check — a chat, a
    phone's push tray, an inbox, the screen in front of you.
    Choosing one is a question of where you already look, not of
    which is cleverest
  + A two-way transport adds the reply. The job does not only
    speak, it reads what comes back, so a run held up on a decision
    is steered from your phone instead of waiting for you to sit
    down at the machine
  + The trap: a notification for everything is a notification for
    nothing. A job that reports success every single night trains
    you to stop reading it, and the one night it reports failure is
    the night you do not notice

- Telegram, ntfy and email
  + Telegram or Discord, through a bot, posts into a chat you
    already have open — nothing new to check, only a new message in
    a window you already watch
  + ntfy is built for phone push: a plain alert with no chat and no
    account, closer to a text message landing than to an app you
    have to remember to open
  + Email through an API lands in the inbox you read every morning
    regardless, with no new address and no new app to learn
  + A desktop notification is local only. It reaches you at the
    machine you are sitting near but not looking at, and it is the
    one option that does nothing once you have actually left the
    room
  + Choosing between them is not about capability. It is about
    which one lands somewhere you were already going to check today

- Claude Code in Slack
  + Slack is supported, but it is not a channel — that is a
    separate integration, its own reach into a session already
    open. Claude Code in Slack is its own thing: mentioning Claude
    in a Slack channel spawns a new session in the cloud, not the
    one running on your machine
  + It is two-way: it posts status as the work proceeds, posts a
    summary when it finishes, and offers a button that opens a pull
    request from the result
  + It needs a claude.ai login, a connected GitHub account and a
    paid plan. It does not run on Bedrock, Vertex or Foundry
  + The ceiling: channels only, never a direct message, and one
    pull request per session — a second from the same conversation
    is not what it does
  + On Team and Enterprise it is being replaced by Claude Tag


+ Challenge two
  + The hook
    + A firm writes noncompetes in all fifty states
    + Every draft it has ever sent out is sitting in a folder, and none of
      that work is reachable. The wording that survived a challenge in
      New Jersey is in a file nobody can find
    + The firm wants the folder turned into something it can draw from
  + What to build
    + A provision library that lives on the reader's own machine. Nothing
      published, nothing hosted
    + Drop a noncompete into a folder and it is taken apart on its own —
      each provision identified for what it is, filed under the states it
      works in, and added to what is already there
    + The library therefore grows. Every contract fed to it makes the next
      draft better, which is the thing to sell in the opening paragraph
    + When a kind of provision turns up that the library has not seen, it
      goes looking — searches, fetches what it finds, and something judges
      whether what came back is worth keeping
    + A master template for the contract as a whole, with the provisions
      as the parts that slot into it
  + What the reader operates it with
    + A TUI, run from a terminal. No web page, no browser
    + Pick a state; the provisions narrow to the ones that work there
    + The template on one side, the provisions available to drop into it
      on the other
    + Fill the variables it asks for — party names, duration, geographic
      scope, subject-matter scope — and a finished draft comes out
    + Search by wording when the phrase is known, and by meaning when it
      is not
  + The rules
    + Same as challenge one — anything from levels one through three, and
      nothing said about how to build it
    + This one is local by design. That is the contrast with challenge three,
      and worth stating so the reader sees the two halves of the level
  + Rungs
    + It parses a contract dropped in the folder and the TUI shows it
    + A new kind of provision sends it out to the web unprompted
    + It runs without being asked — the folder watched, a summary arriving
      on a schedule, a message when something new lands
  + Materials
    + Nine noncompetes, three each from New Jersey, New York and
      Connecticut
    + Three invented deal profiles — emails or notes of the kind a partner
      actually sends, carrying the employee's name, the company, the term,
      the territory. The variables arrive buried in prose, not on a form
    + Enough that the reader can feed the library, then draft against it
    + The corpus exists, at content/21-challenges/materials/challenge-two/

+ Challenge three
  + The hook
    + What if nobody ever had to pay for accounting software again
    + It turns out they need not, and the reader is going to prove it
    + A challenge, not a tutorial — the firm-and-its-problem framing of
      challenge one, with an invented small business in place of the firm
  + What to build
    + A web application the reader hosts themselves, that a stranger can
      reach in a browser by typing an address
    + Accounts — create one, log in, log out
    + Upload the things you would otherwise hand a bookkeeper: bank
      statements, bills, receipts, invoices
    + Out of that, unprompted, two financial statements — a profit and
      loss, and a balance sheet
    + The period is whatever the uploaded documents cover. No fixed range,
      no limit
  + What has to be on the page
    + One page after login is enough; nothing here needs more
    + Somewhere to upload
    + Somewhere to browse and open what was uploaded before
    + The two statements, sortable and filterable by period
    + An agent with a chat box, tied to that account
    + Say nothing about what the chat box is for. Leave the reader to
      discover it can be asked about their own documents
  + The rules
    + Anything from levels one, two and three is fair game
    + Nothing is said about how to build it — no stack, no back end, no
      named tool. Only what a finished one looks like
    + Nobody is marking it. The proof is that it works and that somebody
      else can open it
  + Rungs, in the escalating voice of challenge one
    + It runs, and the reader can use it on their own machine
    + Somebody else can reach it from another machine
    + It stays up — survives a reboot, runs with nobody watching
  + Materials, framed as challenge one frames them
    + Three invented small businesses, of three different types, each in
      its own folder under `materials/challenge-three/`
    + The conceit: these companies have agreed to let the reader put their
      books through the thing they are about to build. Sign each of them
      up, upload their year, see whether the statements come out right
    + Different types on purpose, so the trader with stock, the service
      business with none, and the one with a loan do not all reduce to the
      same shape
    + What is in each folder: bank statements, bills, receipts, invoices.
      Several sources and several formats, some scanned and some exported,
      so nothing can be hardcoded to one layout
    + As in challenge one, the input is a mess and varies by client; what
      comes out the other end must not
    + Enough months that a quarter and a year both mean something
    + Still to be built — the fake corpus does not exist yet

# Level 3 Backlog

The rant, still being processed into the outline above.

## Theme

Automation and integration.

Level 2 taught the funnel: chained agents, each with its own skills, hooks
and context, so that something dropped in at the top comes out the other
end as the thing you wanted. Level 3 wires that funnel into the world.

The reader stops running Claude Code and starts building things that run
on it — their own small applications, driven by or otherwise using Claude
Code, reaching their own systems rather than only their own terminal.

## Topics

- Connectors — an MCP server somebody else runs, added by ticking it on at
  `claude.ai/customize/connectors` rather than at the command line. Not a
  different technology from the entry below: the same protocol, the same
  tools, a shorter install and no config file touched. Because they are
  remote they are HTTP, and because the authorisation is handled on
  Anthropic's side they are the only way to reach the services that refuse
  a local OAuth round trip — Gmail, Google Calendar, Microsoft 365, Slack.
  - Use cases — read the calendar to find a hearing date; pull a client's
    thread out of Gmail; check what a shared Drive folder now contains;
    post the outcome of a run into a Slack channel.
  - The condition that governs everything else: connectors load only when
    the session is signed in with a claude.ai subscription. Set
    `ANTHROPIC_API_KEY`, use an `apiKeyHelper`, hold a `claude
    setup-token` token, or run through Bedrock, Vertex or Foundry, and
    they silently do not appear. No warning, no error — an empty list.
  - They also ride on the claude.ai session token. When that lapses the
    connector reports itself rejected, and re-authorising the connector
    does not mend it; the login itself has to be renewed by a person.
  - Precedence — a server you configured yourself under the same name
    wins. Connectors sit at the bottom of the stack, matched by endpoint
    URL rather than by name.

- MCPs — the standard way to hand Claude a capability it does not ship
  with. A small program advertises a list of tools; Claude calls them like
  any built-in. Without one, reaching a service means Claude writing curl
  commands and parsing what comes back. With one, the service's own
  operations are on the menu, described and typed.
  - Use cases — query a case-management database in read-only mode; file
    and retrieve from a document store; drive a browser through Playwright;
    read errors out of Sentry; anything a vendor has bothered to publish a
    server for.
  - Three transports. `stdio` launches the server as a subprocess on your
    machine — the common case for anything local. `http` reaches a server
    somebody else runs. `sse` is deprecated. Added with
    `claude mcp add --transport http <name> <url>`, or for a local one
    `claude mcp add <name> -- <command>`, where the bare `--` matters: it
    separates the server's own arguments from Claude Code's.
  - Three scopes, and the file each lives in. `local` is this project only,
    stored in `~/.claude.json`. `project` is `.mcp.json` in the repository
    root, which is the one that travels with the code. `user` is every
    project, also in `~/.claude.json`. Note the trap: MCP servers are not
    in `.claude/settings.json` with everything else, and Claude Code does
    not read `~/.claude/mcp.json` however plausible that path looks.
  - A JSON entry with a `url` and no `type` is skipped outright — the
    single most common malformed config.
  - Authentication, in ascending order of what survives unattended. A
    static `headers.Authorization` never refreshes and must be rotated by
    hand. OAuth refreshes its own token and retries once on a 401, which
    covers most overnight running. `headersHelper` runs a command that
    prints a JSON object of headers, fresh on every connection with no
    caching, which is how Kerberos and internal SSO are reached — it gets
    ten seconds and it executes arbitrary shell, so it only runs in a
    trusted folder.
  - Tool search is on by default and is why a dozen servers cost almost
    nothing at startup: only names and instructions load, with the full
    schemas fetched on demand. `ENABLE_TOOL_SEARCH=false` reverts to
    loading everything upfront. `MAX_MCP_OUTPUT_TOKENS` caps what one call
    may return, defaulting to 25,000 with a warning at 10,000.
  - Timeouts worth knowing before a long job fails at midnight:
    `MCP_TIMEOUT` for startup (30s), a per-server `timeout` in
    milliseconds for the whole call, a 60-second per-request timer on HTTP
    servers, and an idle timeout of five minutes remote, thirty local.
  - The unattended point: a project-scoped server in `.mcp.json` normally
    prompts before it loads. Under `claude -p`, in an SDK session and in a
    cloud session there is nobody to prompt, so it loads without asking.
    Keep one out with `disabledMcpjsonServers`, or cut project settings
    off entirely with `--setting-sources`.
  - Managed MCP is the enterprise counterpart — a `managed-mcp.json` in a
    system directory that fixes what may load. Worth knowing exists;
    largely somebody else's problem.

- LSPs — the language-server configuration inside Claude Code, as against
  the general idea covered under language servers below. A plugin declares
  its servers in a `.lsp.json` at the plugin root, or inline in
  `plugin.json` under `lspServers`.
  - The two fields that are compulsory: `command`, the binary, which must
    already be on `PATH`; and `extensionToLanguage`, which maps `.py` to
    `python` so Claude Code knows which files belong to which server.
  - The useful optional ones — `args`, `env`, `startupTimeout`,
    `restartOnCrash` (on by default), `maxRestarts`, and `diagnostics`,
    which is on by default and is the interesting switch. Leave it on and
    every error the server sees is pushed into Claude's context the moment
    an edit is made. Turn it off and you keep the navigation — go to
    definition, find references, hover — without the running commentary.
  - Named in the documentation: `typescript-language-server` for
    TypeScript, `pyright` for Python, `rust-analyzer` for Rust. Installed
    the ordinary way, with npm or pip.
  - Shipping one inside a plugin is the point. The reader who has built a
    plugin for their own work adds four lines and everybody who installs
    it gets symbol navigation, with nothing further to configure.

- Agent SDK — the same agent loop that runs Claude Code, as a library you
  call from your own Python or TypeScript program. The distinction from
  everything in level two: there is no terminal. Your program decides when
  to start a turn, sees every message as it arrives, and can refuse a tool
  call in code.
  - The prior question is whether it is needed at all. Shelling out to
    `claude -p` with `--output-format json` also runs Claude
    non-interactively, from any language, in one line of shell. That is
    the cheaper answer and often the right one. The SDK earns its place
    when the program needs to intervene mid-run — approve tools
    conditionally, stream partial output to a user, hold a session open
    across many exchanges, or bill a customer by the turn.
  - Use cases — the intake form's back end, which submits documents and
    watches for the answer; a service that runs one agent per customer
    with each customer's files walled off from every other's; anything
    with a user waiting on the other end of a connection.
  - Two entry points in either language. `query()` runs once and returns a
    stream of messages. Python's `ClaudeSDKClient` and TypeScript's
    streaming input keep a session alive for repeated exchanges and allow
    an interrupt mid-thought.
  - What comes back is a sequence of typed messages: a `SystemMessage`
    with subtype `init` carrying the session ID, an `AssistantMessage` per
    reply, a `UserMessage` per tool result, and a `ResultMessage` at the
    end holding cost, tokens and the session ID. One trip through
    assistant-then-tools is a turn.
  - The two ways to stop it running forever: `max_turns`, which counts
    tool-using turns only, and `max_budget_usd`, which stops on a
    client-side cost estimate. Neither is a clock — a session has no
    overall timeout and will not end on its own.
  - `can_use_tool` is the permission callback, and it fires only when the
    decision would otherwise have gone to a prompt. Anything already
    covered by an allow rule or by the permission mode never reaches it.
    Six modes exist; `bypassPermissions` refuses to run as root, and deny
    rules outrank it regardless.
  - The `.claude` machinery carries over. Settings, CLAUDE.md, filesystem
    hooks, skills and subagents all load unless you pass
    `setting_sources: []` to shut them out — which is what you do when one
    process serves several customers, alongside a separate working
    directory and `CLAUDE_CONFIG_DIR` for each.
  - Sessions persist as JSONL under `~/.claude/projects/`, resumable by ID
    and forkable into a branch that leaves the original intact. A
    `SessionStore` adapter mirrors them to S3, Redis or Postgres, which
    matters the moment the program runs somewhere that gets rebuilt.
  - Every `query()` spawns the `claude` binary as a subprocess, so
    twenty concurrent sessions are twenty processes. Reckon on a gigabyte
    of memory, five gigabytes of disk and a CPU apiece as a floor.
  - `total_cost_usd` is an estimate from a price table compiled into the
    build. Useful for a budget cap, not for invoicing anyone.

- Channels — an MCP server that pushes events *into* a Claude Code session
  from outside, so Claude reacts to something that happened elsewhere.
  Every other integration has Claude reaching out; this is the one where
  the world reaches in.
  - Use cases — a webhook from a case system arrives and Claude acts on
    the status change; a message from your phone steers a run in progress;
    a job finishes and reports; an approval is granted from a train.
  - What ships: Telegram, Discord and iMessage as plugins, a webhook
    receiver that listens on a local port for anything that can POST, and
    a browser-based demo for testing. Custom ones are written against the
    ordinary MCP SDK.
  - Installed as a plugin, configured with a token that lands in
    `~/.claude/channels/<name>/.env`, then switched on for the session with
    `claude --channels plugin:telegram@claude-plugins-official`. Being in
    `.mcp.json` is not enough — a channel must be named on the command
    line.
  - Two-way if the channel offers a reply tool, and the permission relay
    goes further: an approval prompt appears both in the terminal and on
    your phone, and whichever answers first wins.
  - The constraint that shapes every design around it — events arrive only
    while a local session is open. Not the web, not the desktop app, not
    Remote Control. An always-on channel means a session parked in tmux or
    a `-p` worker left running.
  - The security point is not optional. Gate on the sender's own ID, never
    on the room, or anyone who can reach the endpoint is putting text in
    front of Claude. An ungated channel is a prompt-injection hole with an
    address.
  - Requires an Anthropic login; unsupported on Bedrock, Vertex and
    Foundry, and blocked by default on Team and Enterprise until an owner
    enables it.

- Chrome and computer use — the two ways Claude works a graphical
  interface rather than an API. Chrome is an extension driving a browser
  you can see; computer use is a built-in MCP server driving the whole
  desktop, screenshot by screenshot.
  - Use cases for Chrome — a portal behind a login with no API, which
    describes most court and government systems; a page that renders
    nothing until its JavaScript runs; a form that must be filled and
    submitted; a filing whose confirmation exists only on screen.
  - Chrome shares the browser's own login state, which is the entire
    reason to prefer it over curl. Anything you are already signed into,
    Claude reaches without a credential of its own.
  - It runs in a visible window in real time, and pauses to hand a login
    page or a CAPTCHA back to you. Read-only calls — reading the page,
    searching it, screenshots — go through without a prompt in plan mode;
    clicking, typing and navigating ask.
  - Computer use is the last resort in the ladder: an MCP server first,
    then Bash, then Chrome, then this. It reaches native applications with
    no other way in. macOS and Windows only, Pro or Max only, approval per
    application per session, one session at a time machine-wide, and not
    available under `-p` at all. Escape aborts, and the terminal is hidden
    from its own screenshots.
  - The judgement to teach: reach for these last. An API is faster,
    cheaper and does not break when a button moves. Screen control is what
    you use when there is nothing behind the screen.

- Monitors — a background command a plugin declares, which runs for the
  life of the session and delivers every line it prints to stdout to
  Claude as a notification. A watcher living inside Claude Code, where the
  watchers further down this file live outside it and start sessions.
  - Declared in `monitors/monitors.json` at the plugin root, or inline in
    `plugin.json` under `experimental.monitors`. Three compulsory fields:
    `name`, unique within the plugin so a reload does not spawn a second
    copy; `command`; and `description`, saying what is being watched.
  - `when` decides the start. `always` is the default and fires at session
    start. `on-skill-invoke:<skill-name>` holds it back until that skill is
    first dispatched, so the cost is only paid by sessions that need it.
  - Use cases — tail a log and speak up when an error appears; watch an
    incoming folder and announce what landed; follow a long build; report
    a queue growing.
  - `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` and
    `${CLAUDE_PROJECT_DIR}` expand inside the command, so a monitor can
    call a script shipped alongside it.
  - Experimental, and it inherits the session's lifetime: nothing is
    watched once the session ends.

- Artifacts — a self-contained web page Claude Code publishes from a
  session to a private URL on claude.ai. One HTML file, styles and script
  inline, no server behind it. The cheapest way for work to leave the
  terminal and become something a person can open.
  - Use cases — a matter status page for a client; a summary of an
    overnight run someone else needs to read; a chart of what was
    processed this month; a checklist that fills in while a long job
    proceeds.
  - Publishing prompts once per artifact. Revising means editing the file
    and publishing again to the same URL, and anyone with the page open
    sees it change. Each publish is kept as a version. From a later
    session, hand Claude the URL or you will get a second artifact instead
    of an update.
  - Private to you on creation. Pro and Max share by link to anyone;
    Team and Enterprise can share inside the organisation, with public
    links off until an owner turns them on.
  - The capability worth the whole entry: a page may call MCP connectors
    when it loads. So a status page fetches its own fresh data every time
    it is opened, using the *viewer's* connectors and the viewer's
    account, and the automation that built it does not have to run again
    to keep it current.
  - A strict content policy blocks every external script, stylesheet, font
    and image, and all fetch, XHR and WebSocket traffic. Everything is
    inlined or it does not load. Sixteen megabytes, maximum.
  - Requires a paid plan and a `/login` session on the Anthropic API — not
    Bedrock, Vertex or Foundry. Set `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` so
    a headless run does not try to open a browser.

- Deep links — a URL that opens Claude Code in a new terminal window with
  the prompt box already filled in. The scheme is `claude-cli://open`,
  taking `q` for the prompt text, `cwd` for an absolute working directory,
  and `repo` for a GitHub `owner/name` slug resolved against clones Claude
  Code has already seen.
  - Use cases — a link in an alert that opens a session pointed at the
    thing that broke; a runbook where each step is a link rather than a
    paragraph to copy; a dashboard row that becomes an investigation in
    one click; the last mile of a monitoring setup.
  - It never runs on its own. The prompt is placed in the box and a person
    presses Enter, with a warning that the text came from an external
    link staying visible until they do. That is the design, not a
    limitation to work around: it is the hand-off point between an
    automation that noticed something and a human who decides.
  - Fired from anywhere the operating system can open a URL — `open` on
    macOS, `xdg-open` on Linux, `start` on Windows — so any script can
    produce one.
  - The handler registers itself the first time you type a prompt in an
    interactive session, and `disableDeepLinkRegistration` in
    `settings.json` prevents it. Sites that strip unknown URL schemes,
    GitHub Markdown among them, render the link as plain text; put it in a
    code block so it can be copied.

## Peripheral tooling

- Databases — SQLite, Postgres, DuckDB
- Search indexes — full-text, vector stores
- Schedulers — cron, systemd timers, launchd. A daemon the operating
  system runs: five fields and a command, fired at those times whether or
  not anyone is logged in, surviving reboots. The machine's own alarm
  clock.
  - Against Claude Code's own cron tools, which schedule inside a running
    session: nothing fires if Claude Code is not running, tasks expire
    after seven days, they jitter by up to thirty minutes, and they only
    run between turns. For unattended work, system cron launches
    `claude -p`. Claude's own scheduler is for a session already alive.
  - systemd timers — the Linux replacement for cron. Catch missed runs,
    log to the journal, depend on other services.
  - launchd — the macOS equivalent, and the only scheduler Apple
    properly supports. Fires on events as well as times, such as a
    folder changing.
  - Neither wakes a sleeping machine. A missed slot is simply missed.
    `launchd` on macOS has `RunAtLoad` to fire on next wake, and
    `anacron` on Linux catches missed runs. Or the job does not live on
    the laptop at all — a rented box that never sleeps, which is the
    argument for cloud routines.
- Queues and job runners — a waiting line for work, so things arriving
  faster than they can be processed are not lost. Forty documents land at
  once, each taking two minutes. Rather than running forty at a time and
  melting the machine, they go into a queue and workers pull them off two
  at a time. If one fails it goes back in the line and is retried rather
  than vanishing. The gain is that nothing is dropped and load is
  controlled.
  - Redis with a worker library, or a `jobs` table in SQLite.
  - RabbitMQ and Celery for the serious version.
- Web servers and reverse proxies — a web server listens on a port and
  answers requests. That is how an automation gets a front door: a form a
  client fills in, or a URL another service calls when something happens,
  which then triggers Claude. A reverse proxy sits in front and handles
  what you would not want to write yourself — the certificate for HTTPS,
  routing several services behind one address, refusing traffic you did
  not invite.
  - Caddy gets certificates automatically. nginx is the standard.
    Tailscale or a tunnel avoids opening the machine to the internet at
    all.
  - Worked example — a client intake form. A small web server on your own
    machine serves one page: name, matter type, upload a passport scan.
    Caddy fronts it with a proper HTTPS address to send to a client. The
    client submits; the server writes the files into a case folder, adds
    a row to SQLite, drops a job in the queue. Cron picks it up and runs
    `claude -p` with the intake skill, which reads the documents,
    extracts the details, drafts the engagement letter. You come back to
    a drafted letter and a filed matter.
  - The page is not published elsewhere — the machine *is* the website.
    The client's browser connects to it directly and the files land on
    your disk, with no third party in between. The address is the only
    trick: the machine needs a name on the internet, which the tunnel
    provides without exposing the rest of it.
  - Self-hosting is common and this is it. A domain is worth about ten
    pounds a year and can point at your own machine as easily as at a
    host's: a name is memorable, a number is not, and home addresses
    change. What paid hosting sells beyond that is someone else's
    electricity, a connection that does not drop, and blame that lands
    elsewhere when it breaks. For a form only you depend on, your own
    machine is fine — provided it stays awake.
- HTTP clients and API tooling — the other direction from a web server:
  instead of answering requests, you make them. `curl` fetches a URL from
  the command line, with headers, an API key, a POST body — most of the
  world's data, with no MCP server in sight. `jq` cuts up the JSON that
  comes back: pull one field, filter a list, reshape it. Together, the
  cheapest integration there is. The client is the caller, the API is the
  callee: curl is an HTTP client, so is a browser, so is WebFetch.
  - Use cases — check a case status every morning and report only the
    change; pull the day's exchange rate into a fee calculation; post to
    Slack or Telegram when a run finishes; send email through a
    provider's API; fetch filings from Companies House; download a court
    listing; ask accounting software what is unpaid. Anything with an API
    and no MCP server, which is most services.
  - API shapes, split by who initiates:
    - REST — you ask, it answers, connection closes. The vast majority.
    - Webhooks — the reverse. You paste an address reaching your machine
      into the service's settings; their server calls you when something
      happens. Stripe on payment, GitHub on a pull request, a case system
      on a status change. Needs the front door — the web server above.
    - WebSockets — the line stays open both ways, for continuous streams.
    - Server-sent events — open line, one direction, them to you. How
      Claude streams its own replies.
    - GraphQL — still you-ask-they-answer, but you name exactly which
      fields, in one request.
  - Webhooks depend on the third party offering one, and courts almost
    never do. The fallback is polling: REST requests on a timer. Cron
    fires, curl fetches, compare against yesterday's saved copy, act on
    the difference. Works against a plain HTML page with no API at all —
    that is scraping, and where Chrome control earns its place for sites
    behind a login or heavy JavaScript. Send a `User-Agent` that
    identifies you and do not hammer the server; once or twice a day
    bothers nobody. Webhooks are a gift when offered; polling is what you
    build when they are not.
- Language servers — a program that understands a programming language
  properly and answers questions about your code. It does not make Claude
  better at Python; it makes Claude better at *your* Python. The language
  is already known; the project is not — which of forty files defines
  that function, who calls it, what breaks if it changes. Without one,
  Claude greps and guesses, and guessing is where bugs enter.
  - Not written by you. They already exist: `gopls` for Go, `pyright` or
    `ruff` for Python. Install the binary, name it in `.lsp.json` mapping
    an extension to it, or ship it inside a plugin.
  - One per language, not per project or per part of a project. No
    granularity decision to make: count the languages in the repository,
    that is the count. Tutor would run two side by side, each indexing
    only the files of its own language.
  - Scope is this repository. The server starts when a session opens here
    and indexes what is under this folder; open a different project and
    it indexes that one instead.
  - The gain is exactness, not just speed. Grep for a function name
    returns every mention, comments and same-named functions included.
    The server returns the definition and every genuine caller. It also
    reports a broken line the instant it is written, rather than when
    something fails to run.
- Containers — Docker, devcontainers. A sealed box holding a program and
  everything it needs: its own filesystem, its own packages, its own
  version of Python. It runs identically on a laptop, a rented box, or a
  reader's machine, and touches nothing outside itself, so a Postgres you
  experiment with vanishes when deleted. For Claude Code it is also
  containment — an agent inside cannot damage the machine around it.
  Docker is the tool; a devcontainer is the same thing wired into an
  editor.
  - Use cases beyond safety. Reproducibility: the container is a
    written-down recipe of every dependency, so what worked in March
    still works in December, on a machine not yet built. Deployment: move
    the box to a rented server rather than reinstalling forty things and
    finding the versions differ. Version conflicts: two projects needing
    incompatible Postgres versions, side by side. Trying software: one
    command, use it, delete it, nothing left behind. Parallelism: twenty
    identical boxes doing the same job at once. Take safety out and
    reproducibility is still why people reach for it.
  - On a rented box — install Docker, pull the image, run it. The
    dependencies are inside; the box needs nothing else. The image
    travels through a registry (Docker Hub, or a cloud's own artifact
    registry): push from here, pull there. Watch the architecture — the
    laptop's chip and the rented box's chip may differ, so build for the
    target or build on the box. Services like Cloud Run skip the machine
    entirely: hand over an image, they run it.
  - What it is not. Containers are Linux only — no macOS, no Windows,
    not a virtual machine. It will test against a clean machine holding
    none of your installed tools, which catches "works here because I
    have it" bugs, and it will *build* Mac and Windows binaries, since Go
    cross-compiles. Building and running are different acts: the
    container emits `tutor.exe` and cannot open it. For a TUI the risk is
    the terminal emulator anyway, and a container has none.
- Virtual environments and package managers — a folder holding one
  project's packages, so they do not mix with another project's. Install
  system-wide and every project shares it; two projects needing different
  versions of the same library then collide, and upgrading for one breaks
  the other. A `.venv` folder sits inside the project, Python looks there
  first, and deleting the folder deletes the packages. The same idea as a
  container, one layer lighter: it isolates the libraries, not the whole
  operating system.
  - The name is Python's, the problem is not. Node solves it by default
    with `node_modules` in the project. Go builds dependencies into the
    binary. Ruby has bundler, Rust has cargo. Python is awkward because
    it installed globally for decades, so the fix is bolted on rather
    than built in — which is why it is only ever discussed there.
  - Conda — Anaconda, Miniconda, Miniforge — is both halves in one tool,
    environment and package manager. It goes further than `.venv`: it
    installs the Python interpreter itself, and non-Python things like
    compilers and CUDA libraries, which is why the scientific world uses
    it. The cost is weight and speed.
  - `uv` does the same job for pure-Python work in a fraction of the
    time; `pipx` installs command-line tools each in their own
    environment. If conda already works, there is nothing to fix.
- Watchers — a program that watches a folder and runs a command the
  instant a file appears or changes. Cron asks every five minutes; a
  watcher is told by the operating system the moment it happens, with no
  polling and no delay. It turns a folder into a trigger: drop something
  in, work happens.
  - Use cases — drop a PDF into a folder and it is OCR'd and filed; save
    a source file and the tests run; a scanner writes to a folder and
    Claude processes what lands; an export from another system arrives
    and gets ingested.
  - `inotify` is the Linux kernel's own mechanism, the thing doing the
    watching; `inotifywait` is the command that uses it.
  - `fswatch` is the cross-platform wrapper — the same job on Linux and
    macOS.
  - `entr` is the friendliest: pipe it a list of files and a command, and
    it reruns the command whenever one changes.
- Document pipelines — commands rather than libraries: things you run,
  not code you import. Together they are how a document becomes something
  Claude can read, and how Claude's output becomes a document.
  - pandoc — converts between text formats. Markdown to DOCX, DOCX to
    Markdown, HTML to PDF.
  - poppler — reads PDFs. `pdftotext` pulls the text out; it also splits,
    merges and renders pages.
  - tesseract — OCR. A scan with no text layer becomes text.
  - LibreOffice headless — Word and Excel with no window. Convert a DOCX
    to PDF from a script.
- Templating and rendering engines — a document with holes in it, filled
  from data. An engagement letter with `{{client_name}}` and
  `{{matter_type}}` where the details go: written once, filled a hundred
  times from a hundred rows. The point is not saved typing. It is that
  the model does not draft the boilerplate — it only supplies the values,
  so the approved wording cannot drift.
  - Jinja for Python. docxtpl fills Word documents keeping the
    formatting. Typst or LaTeX where the output must be typeset.
  - PDFs, two ways. A form PDF with named fields — an N-400, say — is
    filled by name with `pdftk` or `pypdf` and then flattened; that is
    filling, not templating. A PDF created from scratch is templated as
    DOCX or Typst and converted at the end.
- Log aggregators and telemetry collectors — somewhere to put the record
  of what the automations did, so questions about them can be answered
  afterwards. Twelve unattended jobs each write their own log file, and
  nobody reads twelve files; an aggregator collects them into one
  searchable place.
  - Use cases — which run failed last night and why; what Claude cost
    this month, per skill; whether the intake job actually ran on
    Tuesday; which matters were processed and which were silently
    skipped.
  - That last one is the reason. Unattended work fails silently, and the
    log is the only evidence it did.
  - `journalctl` if systemd is already there. Loki, or a SQLite table.
- Secret managers and credential helpers — where the API keys live so
  they are not sitting in a config file, a script, or a repository. An
  automation reaching a dozen services needs a dozen credentials, and
  every one of them is a liability if it is written down in the open.
  - Use cases — an API key an unattended job needs at 3am with nobody
    there to type a password; a database password shared across several
    scripts; rotating a key without editing six files; keeping the key
    out of a repository that later gets shared.
  - The specific trap for Claude Code: a key pasted into a prompt, a
    `.env` read into context, or a credential in a command line ends up
    in the transcript. Secrets should be fetched at the moment of use,
    not held in the conversation.
  - Tools — the OS keychain (Keychain on macOS, Secret Service or
    `pass` on Linux); `.env` files with `direnv`, kept out of version
    control; Bitwarden or 1Password with a CLI; HashiCorp Vault or a
    cloud provider's secret manager for the serious version.
  - Claude Code's own hooks here: `apiKeyHelper` runs a command to
    produce the key at connection time rather than storing it, and
    `sandbox.credentials` can deny or mask credentials from a sandboxed
    process entirely.
- Scripting runtimes — the thing that actually runs the glue code between
  everything above. Claude writes a script; something has to execute it.
  - Python is the default: on every machine, and every library needed
    exists. Node comes with the web world. Bun is Node, faster, with
    TypeScript built in and no build step.
  - The point worth teaching: a script is often cheaper and more reliable
    than another agent turn.
- Static site and publishing tooling — a program that turns a folder of
  Markdown into a finished website: plain HTML files, no server logic,
  nothing to run. The output is just files, so they work anywhere they
  are put.
  - Use cases — a client-facing status page an automation regenerates
    nightly; an internal reference built from your notes; a published
    version of something like tutor.
  - Hugo, Zola, Eleventy, MkDocs. GitHub Pages hosts the result free.
  - It belongs here because it is the cheapest way for an automation to
    publish something a person can read.
- Notification transports — how an unattended job reaches you when you
  are not at the machine. The job runs at 3am; something needs a decision
  or something broke, and without a transport you find out when you next
  look, which may be days.
  - Use cases — a run failed; a document is drafted and awaits approval;
    a deadline was detected in an incoming letter; twelve matters
    processed, one could not be.
  - Telegram or Discord via a bot, ntfy for phone push, email through an
    API, a desktop notification locally. A two-way channel adds the
    reply: steer it from your phone.
  - Slack is supported but is *not* a channel. It is its own integration,
    "Claude Code in Slack": `@Claude` in a channel spawns a cloud session,
    not a local one. Two-way — status, summaries, a button to open a PR.
    Needs a claude.ai login, GitHub, and a paid plan; no Bedrock, Vertex
    or Foundry. Channels only, never DMs; one PR per session. Being
    replaced by Claude Tag on Team and Enterprise. Note the English docs
    carry no `slack.md` — only the German set does.

## Database types

- Relational — records with fixed columns and relations between them.
  Matters, clients, invoices.
  - SQLite — one file, no server, no setup. Ships inside Python. The
    default for anything on one machine.
  - PostgreSQL — the serious open-source server. Handles JSON, full-text
    search and vectors too, so one database often covers three of the
    types below.
  - MySQL and its fork MariaDB — older, hugely deployed, mostly behind
    websites.
  - SQL Server and Oracle — commercial, enterprise, licensed.
  - DuckDB — SQLite's shape, but columnar; reads CSV and Parquet directly.
  - The path: SQLite, then Postgres when a second machine needs access.
- Document — JSON blobs of varying shape. Scraped pages, API responses.
  - MongoDB — the one everyone names. Collections of JSON documents, no
    fixed schema.
  - CouchDB — older, syncs well between machines.
  - Firestore and DynamoDB — hosted, by Google and Amazon.
  - Postgres with a `jsonb` column — the pragmatic answer. Document
    storage without a second database.
  - The path: `jsonb` in Postgres, or a JSON column in SQLite, before
    installing MongoDB.
- Key-value — one value per key, fast. In practice: remembering that
  something was already done, so it is not done twice. The archiver runs
  every ten minutes and asks, key by message ID — seen this? Same shape
  for an expensive API answer not worth paying for twice, a "job already
  running, do not start another", a count of how many times something
  happened today. A notepad that survives between runs. No tables, no
  queries.
  - Redis — the standard. A server holding everything in memory, so it is
    very fast. Valkey is the open fork after Redis changed licence.
  - Memcached — older, simpler, cache only.
  - LMDB and RocksDB — embedded, a file on disk, no server. Used inside
    other programs.
  - etcd and Consul — for machines agreeing on shared settings across a
    network.
  - The path: a two-column SQLite table on one machine, installing
    nothing. Redis earns its place when several processes need the same
    notepad at once.
- Columnar — answering a question about all the rows at once, rather
  than fetching one row. "What did I bill per client per month for three
  years." "Which of these 400,000 log lines are errors, grouped by hour."
  A relational database reads every row whole to answer that; a columnar
  one reads only the columns asked about, so it is often a hundred times
  faster.
  - DuckDB — the one that matters here. One file, no server, and it
    queries CSV and Parquet on disk directly.
  - ClickHouse — server, for constant streams.
  - BigQuery, Snowflake, Redshift — hosted, enterprise.
- Full-text search — finding the words in ten thousand documents without
  opening them. `grep` scans every file every time and matches only what
  was typed exactly. A full-text index is built once, then answers
  instantly, ranks the best hits first, and knows "filed", "filing" and
  "files" are the same word. For a practitioner: search across every
  letter and pleading in an archive.
  - SQLite FTS5 — built into SQLite already. Start here.
  - Postgres `tsvector` — the same idea, in Postgres.
  - Tantivy and Meilisearch — standalone, better ranking.
  - Elasticsearch — the heavyweight, a server.
- Vector — searching by meaning instead of by word. Full-text finds
  "termination"; vector finds the clause about ending the agreement
  early, though it never says "termination". Each document is turned into
  a list of numbers by a model; similar meanings land near each other,
  and the search is for what is nearby. This is what sits under a Claude
  Code retrieval setup: find the six relevant passages out of ten
  thousand, hand only those to the model.
  - sqlite-vec — an extension to SQLite. Start here.
  - pgvector — the same for Postgres.
  - Chroma, Qdrant, LanceDB — standalone.
- Graph — where the connections matter more than the records. Who is
  related to whom, which company owns which, what depends on what. A
  relational database can store that, but asking "everyone connected to
  this person within four steps" becomes painful; a graph database
  answers it directly. For a practitioner: corporate ownership chains,
  conflict-of-interest checks across a client base, family relationships
  in an immigration matter.
  - Neo4j — the standard, a server.
  - SQLite with recursive queries — often enough.
  - Kuzu — embedded, one file.
  - Memgraph — server, faster.
- Time-series — the same measurement taken over and over, stamped with
  when. The question is always shaped by time: what did this look like
  last Tuesday, what is the daily average, when did it spike. The
  database is built to throw away old detail and keep summaries. For a
  practitioner: tracking what an automation costs per day, how long each
  run took, or prices and rates over months.
  - SQLite with a timestamp column — enough for most of this.
  - InfluxDB and TimescaleDB — purpose-built.
  - Prometheus — for machine metrics.

## Left out on purpose

- Computer use — macOS and Windows only, Pro or Max only, dead under `-p`.
  Shown, never required.
- Log aggregators — twelve unattended jobs justify one, two challenges do
  not.
- Connectors are gated on a claude.ai subscription, so they can be reached
  for but never depended on.

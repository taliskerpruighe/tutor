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
  + Level two's funnel ran when you typed; level three's runs on its own —
    a `claude -p` job at 06:00 off a `launchd` plist while you are in
    court.
  + The reader stops running Claude Code by hand and starts building
    applications that use it, reaching their own systems instead of only
    the terminal.
  + The machine that runs it is either a box that never sleeps or the
    laptop in your bag, and that choice decides every other decision in
    this level.

- The shape of an automated system
  + Four parts, seen on the intake form: Caddy taking a POST is the
    trigger, the passport scan is the input, `claude -p` with the intake
    skill is the work, and the drafted engagement letter in
    `matters/smith/` is the output.
  + Four kinds of trigger: a clock (`cron`), a file appearing
    (`inotifywait`), a request arriving (a webhook POST), or a message
    pushed in (a Telegram channel).
  + Claude Code is the work step and never the trigger; something outside
    it always starts the run.
  + Output that stays in the transcript is not output — it has to land as
    a file in the matter folder, a row in SQLite, or an artifact URL.

- Less is more
  + An agent turn costs tokens, seconds, and a different answer on every
    run; `pdftotext scan.pdf -` costs none of the three and returns the
    same bytes each time.
  + Deciding which of forty scans has no text layer reduces to a rule;
    deciding which of forty letters mentions a deadline needs judgement.

### Scripted Behavior

- What a script is for
  + Claude writes the script; something else — cron, a shell, a scheduled
    job — executes it on its own after the session that produced it
    ends.
  + Cheaper and more reliable than another agent turn every time it runs:
    no tokens spent, no seconds of latency, no chance the wording changes
    between runs.
  + The filing rule agreed in March still fires in December, because a
    script outlives the session that wrote it — no context window has to
    hold it.

- Python, Node and Bun
  + Python is the default because it is on every machine already and
    every library needed exists there; Node comes bundled with the
    web-development world instead.
  + Bun is Node, but faster, with TypeScript built in and no separate
    build step.
  + You name the outcome — "file the scans by matter number" — and
    Claude picks the runtime itself; the choice shows up afterward as a
    `.py` file you can read, not a decision you make first.

- A script instead of an agent turn
  + An agent turn repeats itself on every run: the same task, phrased
    slightly differently, with a different number of tokens spent doing
    it.
  + A script guarantees the same operation happens the same way every
    time — the same rename, the same checksum, the same arithmetic, with
    nothing to reinterpret.
  + Some decisions reduce to a rule — moving `2026-08-30-smith.pdf` into
    `matters/smith/`, computing a 21-day deadline from a service date,
    checksumming an import against the file count.
  + Others do not — deciding whether a letter contains a deadline at all,
    or which of two spellings is the same client.
  + A script cannot notice that a scan is upside down, or that the
    covering letter contradicts the enclosure it describes.
  + A script cannot notice that the matter number written on the form is
    wrong.

### Environments

- Virtual environments
  + Installing a library system-wide means every project shares it; when
    two projects need different versions of the same package, the second
    install breaks the first.
  + `.venv` is a folder inside the project itself; Python looks there
    before anywhere else, so what a project needs never has to touch the
    system install.
  + Deleting the `.venv` folder deletes the packages with it — there is
    nothing else to clean up.
  + The name is Python's; the problem is not: Node solves it by default
    with `node_modules`, Go builds dependencies into the binary, Ruby has
    bundler, Rust has cargo.
  + Python is awkward here because it installed system-wide for decades,
    so the fix is bolted on rather than built in — which is why virtual
    environments are only ever discussed in Python's context.
  + The same idea as a container, one layer lighter: an environment
    isolates the libraries; a container isolates the whole operating
    system underneath them too.

- uv, pipx and conda
  + `uv` does the same pure-Python job as `.venv` and `pip`, in a
    fraction of the time.
  + `pipx` installs command-line tools each into its own isolated
    environment, rather than mixing their dependencies into a project's.
  + Conda goes further than either: it installs the Python interpreter
    itself plus non-Python things like compilers and CUDA libraries — the
    cost is weight and slower installs.
  + If a conda setup already works, there is nothing to fix by switching
    to `uv`.

### Logs

- Unattended work fails quietly
  + A run that OCR'd nothing and a run that filed twelve matters leave an
    identically empty terminal at 08:00 — nothing distinguishes success
    from failure by looking.
  + Exit code zero means the last command in the pipeline returned zero —
    not that the right documents were filed, or that any were.
  + A record written during the run is the only evidence of what
    happened, because unattended work fails silently and nothing else is
    watching.

- Where logs go
  + A typed command's output goes to your terminal and dies with the
    window; a cron job's stdout goes to mail, or nowhere, unless you
    redirect it.
  + One job, one file, one known place: `>> ~/logs/intake.log 2>&1`.
  + A usable log line carries the time, the matter it concerns, what was
    done, and the exit status.
  + A log nobody reads answers no question afterwards, which makes it not
    a log — just disk space.

- Log aggregators
  + Twelve unattended jobs each writing their own log file cost you:
    nobody reads twelve separate files, so a failure sits unnoticed until
    something downstream breaks.
  + An aggregator collects those twelve files into one searchable place,
    so a question about any of them is one query rather than twelve
    terminals.
  + Answers questions no single file can: which run failed last night and
    why, and what Claude cost this month per skill.
  + Also answers whether the intake job actually ran on Tuesday, and
    which matters were processed against which were silently skipped.
  + `journalctl` if systemd is already on the box; otherwise Loki, or a
    plain SQLite table with a timestamp column.
  + Twelve unattended jobs justify building one; two challenges running
    on a laptop do not.

### Language Servers

- What a language server is
  + A language server answers questions about your code, not about the
    language — which of forty files defines a function, who calls it,
    what breaks if it changes.
  + It knows the language already; the difference is knowing your
    project — the same server that understands Python syntax has to be
    pointed at this repository to know what `charge_client` means here.
  + Without one, Claude greps and guesses, and guessing is where bugs
    enter.
  + Grep returns every mention of a name, comments and same-named
    functions included; the server returns the actual definition and
    every genuine caller.

- The servers there are
  + They already exist, one per language — nobody writes their own.
  + `gopls` covers Go; Python has a choice between `pyright` and `ruff`;
    `typescript-language-server` and `rust-analyzer` cover their own
    languages — all named in Claude Code's own docs and installed the
    ordinary way, with npm or pip.
  + One per language, not per project or per part of one — count the
    languages in the repository and that is the count.
  + Tutor itself would run two side by side, one for the Go reader and
    one for the Python parity oracle, each indexing only its own
    language's files.
  + A server's scope is this repository: it starts when a session opens
    here and indexes what is under this folder.
  + Open a different project and it indexes that one instead, from a
    standing start.

- Wiring one into Claude Code
  + A server is declared in `.lsp.json` at the plugin root, or inline in
    `plugin.json` under `lspServers`.
  + Two fields are compulsory: `command`, the binary, and
    `extensionToLanguage`, which maps an extension like `.py` to a
    language like `python` so Claude Code knows which files belong to
    which server.
  + The binary named in `command` has to already be on `PATH` —
    `.lsp.json` names `pyright`, it does not install it; `pip install
    pyright` is a separate step done first.
  + Optional fields cover the rest: `args`, `env`, `startupTimeout`,
    `restartOnCrash` (on by default), and `maxRestarts`.
  + `typescript-language-server`, `pyright` and `rust-analyzer` are the
    ones named in Claude Code's own docs, installed the ordinary way with
    npm or pip.
  + Wiring into a project's own `.lsp.json` serves that repository alone;
    wiring into a plugin's ships the same server configuration to
    everyone who installs the plugin.
  + Shipping one in a plugin is four lines, and every installer gets
    symbol navigation — go-to-definition, find-references, hover — with
    nothing further to configure.

- Diagnostics
  + On by default, and it pushes every error the server sees into
    Claude's context the moment an edit is made.
  + Turned off, go-to-definition, find-references and hover still work —
    what is lost is the running commentary, not the navigation.
  + A long editing session with diagnostics on pays for that commentary
    in context space on every single edit, against catching a broken
    line the instant it is written.

## Triggers

### Schedulers

- What a scheduler is
  + A scheduler is an OS daemon that fires a command at set times — the
    intake run at 06:00, say — whether or not anyone is logged in, and
    even after a reboot: the machine's own alarm clock.
  + Five fields and a command is the whole shape of a job, however it is
    declared, before cron, launchd or systemd timers differ in the
    details.
  + cron, launchd and systemd timers are three implementations of the
    same idea, chosen by platform rather than by what the job needs to
    do.

- cron
  + `0 6 * * 1-5` is the schedule and `/usr/bin/claude -p "run the
    intake skill"` is the command; adding `>> ~/logs/intake.log 2>&1`
    keeps a record of what ran.
  + On a rented box that never sleeps, cron is what fires `claude -p`
    unattended; Claude Code's own scheduler only runs inside a session
    already open.
  + Cron is the name people reach for because every Linux and Mac
    machine already has it running, with nothing to install.
  + Cron does not check whether yesterday's run is still going, so two
    `claude -p` processes racing over one matter folder is prevented
    with `flock`, not with cron.

- launchd
  + `~/incoming/scans/` filling with a new scan is enough to trigger a
    launchd job on its own — it fires on events as well as on set
    times, with no polling loop required.
  + launchd is the macOS scheduler, and the only one Apple actually
    supports; cron still runs there, but Apple's own tooling assumes
    launchd.
  + `RunAtLoad` is launchd's answer to a missed slot: a job due while the
    Mac was asleep fires as soon as it next wakes, rather than being
    lost.

- systemd timers
  + systemd timers are the Linux replacement for cron: a `.timer` file
    paired with a `.service` file, and they exist only on Linux —
    nothing equivalent on macOS.
  + `OnCalendar=Mon..Fri 06:00` sets the schedule; `Persistent=true` on
    the timer catches a run that was due while the box was off and
    fires it on the next boot instead of skipping it.
  + The record of what happened lives in `journalctl -u intake.service`,
    not in a log file that has to be created and redirected by hand.
  + A timer can wait on another systemd unit before firing — the intake
    job held until the database service is confirmed up.

- Claude Code's own scheduler
  + Claude Code's own scheduler queues a task inside a session that is
    already running — a reminder to check tomorrow's hearing list before
    the session ends, say — it is not a system-level cron replacement.
  + Nothing fires if Claude Code is not running: close the terminal
    running the evening session and the whole schedule closes with it.
  + A scheduled task expires after seven days if it never gets the
    chance to run.
  + Firing time jitters by up to thirty minutes, so it is not a precise
    alarm clock.
  + Tasks fire only between turns, never interrupting one already in
    progress.
  + For anything that has to run with nobody logged in, system cron
    launching `claude -p` is the tool; Claude's own scheduler is for a
    session already alive.

- Machines that sleep
  + Neither cron nor launchd wakes a sleeping machine; a job due while
    the laptop is closed is simply missed, full stop.
  + `RunAtLoad` on macOS fires a launchd job as soon as the machine next
    wakes, rather than waiting for the next scheduled slot.
  + `anacron` on Linux does the equivalent: it catches jobs that were
    missed while the box was off and runs them once it is back.
  + A job that truly cannot be missed does not belong on a laptop that
    sleeps — it belongs on a rented box that never does.

### Watchers

- What a watcher is
  + A scan landing in `~/incoming/scans/` is enough to run a watcher's
    command instantly — the folder itself becomes the trigger.
  + Cron asks every five minutes whether anything changed; a watcher is
    told by the operating system the moment it happens, with no polling
    and no delay.
  + It only works while the watching process itself is running — close
    the terminal it lives in and nothing fires until it is started
    again.

- inotify, fswatch and entr
  + A scanner writing to `~/incoming/scans/` is caught by `inotify`, the
    Linux kernel mechanism doing the actual watching; `inotifywait` is
    the command that uses it, and neither exists outside Linux.
  + `fswatch` is the cross-platform wrapper, doing the same job on Linux
    and macOS.
  + `entr` reruns its command whenever a file in the list it was piped
    changes — the friendliest of the three.

- A folder as a trigger
  + `~/incoming/scans/` can be the entire interface: the scanner writes
    there, `inotifywait -m -e close_write` fires, and `claude -p` files
    whatever landed — drop a PDF in and it is OCR'd and filed with
    nothing else in between.
  + Each job watches its own folder, so two watchers never race for the
    same file.
  + `-e create` fires on a half-written forty-megabyte scan the instant
    the first byte lands, not on the finished file.
  + Waiting for `close_write`, or for the file's size to stop changing,
    is what tells a watcher the write is actually done.

### Queues

- What a queue is
  + A queue is a waiting line for work: forty scanned documents arriving
    at once do not get processed forty at a time and melt the machine.
  + Workers pull from the front of the line at a controlled rate — two
    at a time, say, while the other thirty-eight wait their turn.
  + A job that fails goes back into the line and is retried, rather than
    silently vanishing.
  + Nothing is dropped and load stays controlled — that is the entire
    point of putting a queue between the trigger and the work.
  + The trigger and the queue are two separate jobs: a watcher's only
    work is to add a row to the queue and get out of the way, not to run
    the OCR itself.

- Redis, SQLite and the serious version
  + A `jobs` table in SQLite is enough when one machine does the work: a
    row per job, a status column, and a script that claims the next
    pending row.
  + Redis with a worker library earns its place once more than one
    process needs to pull from the same queue — two intake workers, say,
    splitting forty scanned documents between them.
  + RabbitMQ and Celery are built for the serious version: many workers,
    many queues, retries and routing rules that a `jobs` table cannot
    express.
  + The path runs in that order — SQLite first, Redis once a second
    process needs the same queue, RabbitMQ and Celery only when that
    stops being enough.

### Monitors

- What a monitor is
  + A monitor is a background command a plugin declares, running for the
    life of the session.
  + Every line it prints to stdout is delivered to Claude as a
    notification — the output reaches the model mid-session, not a
    person directly.
  + Tailing a log to speak up on an error, watching an incoming folder
    and announcing what landed, following a long build, and reporting a
    queue growing are the jobs it is built for.
  + It differs from the watchers described elsewhere in this outline in
    where it lives: those run outside Claude Code and start sessions; a
    monitor runs inside one, watching on the model's behalf.
  + Experimental, and it inherits the session's lifetime — nothing is
    watched once the session ends.

- Declaring one in a plugin
  + `monitors/monitors.json` at the plugin root, or `plugin.json` under
    `experimental.monitors` inline, is where a monitor gets declared.
  + Three fields are compulsory: `name`, `command` and `description`.
  + `name` has to be unique within the plugin, so reloading the plugin
    does not spawn a second copy of the same monitor.
  + `when` decides the start; left unset it defaults to `always`, which
    fires at session start.
  + `on-skill-invoke:<skill-name>` defers the start until that named
    skill is first dispatched, instead of firing immediately.
  + The choice matters because it decides who pays the cost: `always`
    runs for every session, `on-skill-invoke` only for the ones that
    actually reach that skill.
  + `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` and
    `${CLAUDE_PROJECT_DIR}` expand inside `command`, so a monitor can
    call a script shipped alongside the plugin rather than a hardcoded
    path.

## Integrations

### APIs

- What an API is
  + The client is the caller and the API is the callee — `curl` is an
    HTTP client, and so are a browser and `WebFetch`.
  + The portal a client clicks through calls the same endpoints `curl`
    would; nothing installs, it is a URL and a key.
  + Companies House publishes an API for company filings; most county
    court listing pages do not.

- curl and jq
  + `curl` fetches a URL from the command line with headers, an API
    key and a POST body; `jq` cuts up the JSON that comes back —
    together the cheapest integration there is.
  + A morning `curl` of the case-status endpoint reports only what
    changed since yesterday.
  + The day's exchange rate drops into a fee calculation; a Slack or
    Telegram post fires the moment a run finishes.
  + `curl` fetches filings from Companies House, downloads a court
    listing, and asks accounting software what invoices are unpaid.

- The API shapes there are
  + Every shape splits on the same question: who speaks first.
  + REST — you ask, it answers, the connection closes; the vast
    majority of APIs.
  + Webhooks — the reverse: you paste an address reaching your machine
    into the service's settings, and their server calls you when
    something happens — Stripe on a payment, GitHub on a pull request,
    a case management system on a status change.
  + WebSockets keep a line open both ways for a continuous stream;
    server-sent events keep it open one way, them to you — the way
    Claude streams its own replies.
  + GraphQL is still you-ask-they-answer, but you name exactly which
    fields you want, in one request.
  + The service chose the shape, not you — `curl` and `jq` work
    against whichever one you're handed.

- Polling and webhooks
  + A webhook needs the front door — a web server of your own the
    service can reach — and a case management system that offers one
    calls it on every status change.
  + Courts almost never offer one.
  + The fallback is polling: cron fires, `curl` fetches, the result is
    compared against yesterday's saved copy, and the difference is
    acted on.
  + Webhooks are a gift when offered; polling is what you build when
    they are not.

- Scraping
  + Polling a plain HTML page with no API at all is scraping — the
    same cron-and-compare loop, aimed at markup instead of JSON.
  + A court listing page is HTML written for a person: the hearing
    date sits in a table cell with no id, nothing marking it as data.
  + A redesign moves that cell without throwing any error — the fetch
    still succeeds, and the extracted value is simply wrong.
  + Where `curl` stops working — a login wall or heavy JavaScript — is
    where Chrome control earns its place.
  + The manners are cheap: a `User-Agent` that identifies who is
    calling, and a fetch once or twice a day, which bothers nobody.

### MCPs

- What an MCP is
  + An MCP server advertises a list of tools; Claude calls them like any
    built-in, typed and described instead of guessed at
  + Without one, reaching a service means Claude writing curl commands
    and parsing whatever comes back
  + Use cases: a read-only case-management database, a document store,
    a Playwright browser, errors pulled out of Sentry
  + Same protocol and same tools as a connector; what differs is the
    install — a server is added at the command line, a connector is
    ticked on at `claude.ai`

- Adding one
  + A remote server is added with
    `claude mcp add --transport http <name> <url>`
  + A local one is added with `claude mcp add <name> -- <command>`,
    where the bare `--` separates the server's own arguments from
    Claude Code's
  + A published server usually exists already — vendors ship them for
    Sentry, Playwright and Postgres — so writing your own is rarely
    the first move
  + A `stdio` server runs as a subprocess with your own files and your
    own network access, so adding one is a trust decision, not a
    convenience

- The transports
  + `stdio` launches the server as a subprocess on your machine — the
    case-management database on your own disk is the common case
  + `http` reaches a server somebody else runs, such as a document
    portal's own service
  + `sse` is deprecated

- Scopes and where they live
  + `local` scope is this project only, stored in `~/.claude.json`
  + `project` scope lives in `.mcp.json` in the repository root — the
    file that travels with the code, arriving with the clone on the
    office machine
  + `user` scope reaches every project, also in `~/.claude.json`
  + MCP servers are not configured in `.claude/settings.json` with
    everything else — the first wrong guess
  + `~/.claude/mcp.json` is never read, however plausible the path
    looks — the second wrong guess
  + `project` scope suits a server the whole team should get on every
    clone; `local` scope suits one this checkout alone should keep

- Authentication
  + A static `headers.Authorization` value, the kind used against an
    internal document-store server, never refreshes and must be
    rotated by hand each quarter
  + OAuth refreshes its own token and retries once on a 401, which
    covers most overnight running
  + `headersHelper` runs a command that prints a JSON object of headers
    fresh on every connection with no caching — how Kerberos and
    internal SSO are reached
  + It gets ten seconds and executes arbitrary shell, so it only
    belongs in a trusted folder

- Tool search and output limits
  + Tool search is on by default, so a dozen servers cost almost
    nothing at startup — only names and instructions load
  + Full schemas are fetched on demand, the moment a tool is actually
    called
  + `ENABLE_TOOL_SEARCH=false` reverts to loading every schema upfront
  + `MAX_MCP_OUTPUT_TOKENS` caps what a single call may return,
    defaulting to 25,000 tokens
  + A document-store call returning two hundred filings can pass the
    10,000-token warning long before the 25,000 cap is hit

- Timeouts
  + Four separate clocks govern an MCP call, and a job hung at
    midnight is usually one of them running out
  + `MCP_TIMEOUT` covers startup, and defaults to 30 seconds
  + The per-server `timeout`, set in milliseconds, bounds the whole
    call
  + HTTP servers carry a 60-second per-request timer on top of that
  + Idle timeout is five minutes for a remote server, thirty minutes
    for a local one
  + Matching a failure to the clock that caused it is the diagnostic
    step: a startup hang is `MCP_TIMEOUT`, a stalled call is the
    per-server `timeout` or the HTTP timer, silence after replies is
    the idle timeout

- MCPs in unattended sessions
  + A project-scoped server in `.mcp.json` normally prompts for
    approval before it loads
  + Under `claude -p`, in an SDK session, and in a cloud session there
    is nobody to answer that prompt, so a server committed to the
    matters repo loads unasked when a 06:00 intake run starts
  + The security consequence: anyone who can commit a `.mcp.json` to
    the repo can get a server run unattended, with nobody there to
    say no
  + `disabledMcpjsonServers` keeps a specific one out;
    `--setting-sources` cuts project settings off entirely
  + Managed MCP is the enterprise counterpart — a `managed-mcp.json`
    in a system directory fixes what may load regardless of what a
    project asks for

- Driving a browser headlessly
  + The Playwright MCP server is what drives a browser headlessly —
    it renders into memory, so no display is needed and the box can
    be a rented Linux one
  + Nothing about the run is visible, so a login page or a CAPTCHA
    becomes a silent hang rather than a prompt anybody can answer
  + A page plain enough to run unwatched has a stable form and no
    login
  + A court portal behind a sign-in is not one of those pages, and
    belongs to Chrome control instead

- When an MCP breaks
  + A JSON entry with a `url` and no `type` is skipped outright — the
    single most common malformed config, and why a document-store
    server can show no tools the morning after an edit
  + The fix is naming the transport explicitly, `"type": "http"` or
    `"type": "stdio"`, alongside the `url`
  + `claude mcp list` and `/mcp` inside a session are how you find out
    what actually loaded
  + A server that failed to start and a server that was never
    configured both look like nothing on the menu — the failure is
    silent either way
  + An empty tool list can equally mean tool search deferred the
    schemas; it proves nothing about the server on its own

### Browser and Screen Control

- What Chrome control is
  + Chrome control is an extension that drives a browser window you
    can see — the same window, taking the same actions a person would.
  + It exists for the site with no API and no way in through the
    terminal: a login-gated portal, a page that renders only after its
    JavaScript runs.
  + Computer use, by contrast, is a built-in MCP server driving the
    whole desktop, screenshot by screenshot — not just the browser.

- The browser's own login
  + It shares the browser's own login state — the entire reason to
    prefer it over `curl` for a signed-in site.
  + Anything the browser is already signed into, Claude reaches
    without a credential of its own: no separate API key, no service
    account.
  + A solicitor's Chrome already signed into the county court's
    e-filing portal — Claude reaches that same session, not a fresh
    login of its own.

- The portal with no API
  + The use case is a portal behind a login with no API — most court
    and government systems.
  + Chrome control reaches a page that renders nothing until its
    JavaScript runs, and fills a form that must be clicked into field
    by field and submitted.
  + A filing confirmation exists only on screen, and no API can hand
    it back instead — a screenshot is the record.
  + It runs in a visible window in real time — watchable, not
    headless.
  + It pauses and hands control back at a login page or a CAPTCHA.
  + Read-only calls — reading the page, searching it, screenshots —
    pass without a prompt in plan mode; clicking, typing and
    navigating ask first.

- Computer use
  + It reaches native applications with no other way in — a desktop
    e-filing client, a case-management program with no browser and no
    API — after an MCP server, Bash and Chrome have all failed.
  + It runs on macOS and Windows only, and on Pro or Max only.
  + Approval is scoped per application, per session.
  + Only one session machine-wide may hold control at a time.
  + It is unavailable under `-p`, so no unattended run reaches it.
  + Escape aborts a run in progress.
  + The terminal is hidden from its own screenshots.

- Reach for these last
  + The ladder runs MCP server, then Bash, then Chrome, then computer
    use — each rung reached only once the one before it has failed.
  + An API is faster and cheaper, and does not break when a button
    moves.
  + Screen control is what's left when nothing behind the screen can
    be reached any other way.

### Connectors

- What a connector is
  + A connector is an MCP server somebody else runs, ticked on at
    `claude.ai/customize/connectors` rather than added at the command
    line
  + Same protocol and same tools as a server you configure yourself —
    what differs is a shorter install and no config file touched
  + Because it is remote it is HTTP, and because Anthropic handles the
    authorisation it reaches services that refuse a local OAuth round
    trip: Gmail, Google Calendar, Microsoft 365, Slack
  + The calendar connector answers when the Smith hearing is listed;
    the Gmail connector pulls a client's thread into the session
  + A shared Drive folder's current contents are readable, and an
    overnight run's outcome posts into a Slack channel

- Turning one on
  + The tick is made at `claude.ai/customize/connectors`
  + Nothing installs on your machine and no config file changes — the
    whole action is the tick itself
  + The tick is made once per account, not once per matter repo, so
    every session that account opens sees it

- The subscription condition
  + Connectors load only when the session is signed in with a
    claude.ai subscription
  + Setting `ANTHROPIC_API_KEY` kills them silently
  + So does an `apiKeyHelper`, a `claude setup-token` token, or
    running through Bedrock, Vertex or Foundry
  + No warning and no error in any of those cases — just an empty
    list where the connectors should be
  + They also ride the claude.ai session token itself, so when that
    lapses the connector reports itself rejected
  + Re-authorising the connector does not mend a lapsed login — the
    login has to be renewed by a person, which an unattended job
    cannot do

- Precedence
  + A server you configure yourself at the same endpoint URL wins
    over a connector reaching that endpoint
  + Pointing your own server at a connector's endpoint overrides it
    without unticking the connector first
  + The match is made on endpoint URL, not on name
  + Renaming your own server changes nothing about precedence, since
    the match never looked at the name in the first place

### Channels

- What a channel is
  + A channel is an MCP server that pushes events into a running
    session from outside — the one integration where the world
    reaches in rather than Claude reaching out.
  + It reverses every other integration in this course: connectors,
    MCPs and Chrome have Claude call out; a channel has something
    outside call in.
  + Use case: a case-management webhook arrives and Claude acts on
    the status change without anyone opening a terminal.
  + Use case: a message from a paralegal's phone redirects a run
    already underway, or an approval is granted from a train.

- The channels there are
  + Ships as plugins: Telegram, Discord and iMessage, plus a webhook
    receiver listening on a local port for anything that can POST,
    and a browser demo for testing.
  + Custom channels are written against the ordinary MCP SDK, so a
    firm's own case-management webhook does not have to wait for a
    shipped plugin.
  + The webhook receiver is the one built for a firm's own systems:
    point a case-management server's status-change webhook at the
    local port instead of picking a chat app.
  + Needs an Anthropic login, and does not run on Bedrock, Vertex or
    Foundry.
  + Blocked by default on Team and Enterprise until an owner enables
    it.

- Switching one on
  + Installed as a plugin, with a token landing in
    `~/.claude/channels/<name>/.env`.
  + Switched on for the session by naming it on the command line —
    `claude --channels plugin:telegram@claude-plugins-official` —
    not by editing a config file.
  + Being listed in `.mcp.json` is not enough; a channel not named on
    the command line never loads.
  + Events arrive only while a local session is open — not the web,
    not the desktop app, not Remote Control.
  + An always-on channel means a session parked in tmux, or a
    `claude -p` worker left running for the purpose.
  + A paralegal wanting a Telegram alert on every filed matter has to
    leave that session running all day, not just open it when
    checking.

- Two-way and the permission relay
  + Two-way requires the channel to offer a reply tool — not every
    channel does.
  + The permission relay puts the same approval prompt in two places
    at once: the terminal and the phone.
  + Whichever answer arrives first wins, so approving from a phone
    while stepping out of a hearing beats a terminal sitting
    untouched back at the office.

- Gating the sender
  + Sender-ID gating is the rule that holds; the room a message
    arrives in is not a safe boundary to gate on.
  + Gating on the room instead lets anyone who can reach that room
    put text in front of Claude — a client's own group chat, say, not
    just the paralegal running it.
  + The same rule applies to the webhook receiver: gate on which case
    system or account sent the POST, not on the port being reachable.
  + An ungated channel is a prompt-injection hole with an address —
    anyone who finds it can steer the session.

### Deep Links

- What a deep link is
  + A deep link opens Claude Code in a new terminal window with the
    prompt box already filled — scheme `claude-cli://open`.
  + It carries `q` for the prompt text, `cwd` for an absolute working
    directory, and `repo` for a GitHub `owner/name` slug resolved
    against clones Claude Code has already seen.
  + Use case: an alert link that opens a session pointed straight at
    whatever broke — a failed intake run, say.
  + Use case: a runbook written as links rather than paragraphs to
    copy, so each step is one click.
  + Use case: a dashboard row for an overdue filing that becomes an
    investigation in one click.
  + It never runs on its own — the prompt lands in the box, a person
    presses Enter, and an external-link warning stays visible until
    they do; that hand-off is the design, not a limitation.

- Firing one
  + Fired from anywhere the OS can open a URL — `open` on macOS,
    `xdg-open` on Linux, `start` on Windows — so any script can
    produce one.
  + A monitor watching the intake queue can print a deep link
    straight into its notification, landing a session pointed at the
    stuck matter with one click.
  + The handler registers itself the first time a prompt is typed
    into an interactive session.
  + `disableDeepLinkRegistration` in `settings.json` prevents that
    registration.
  + Sites that strip unknown URL schemes — GitHub Markdown among
    them — render the link as plain text, so put it in a code block
    so it can still be copied.

### Credentials

- Where keys should live
  + A dozen services reached from automations means a dozen
    credentials, and each one written down in the open is its own
    liability.
  + Use case: an unattended job running at 3am needs an API key with
    nobody there to type a password.
  + Use case: rotating a shared database password in one place rather
    than editing six scripts.
  + Use case: keeping a key out of a repository that later gets
    shared with a client or a new hire.
  + The rule: a key is fetched at the moment of use, not stored
    everywhere it might be needed.

- The keychain, direnv and password managers
  + The OS keychain — Keychain on macOS, Secret Service or `pass` on
    Linux — holds a credential outside any file a script or
    repository can expose.
  + `.env` files paired with `direnv`, kept out of version control,
    load a key into environment variables only inside that directory.
  + Bitwarden or 1Password with a CLI reaches the same vault a person
    already uses for the firm's other passwords.
  + HashiCorp Vault or a cloud provider's secret manager is the
    serious version, for a script, a colleague and a scheduled job
    all pulling from the same store.
  + A script asks the keychain by name at the moment it calls out and
    keeps no copy of what comes back.
  + A firm running Telegram, a case-management API and an email
    provider keeps three keys in one keychain rather than three
    `.env` files scattered across matter folders.

- Keys and the transcript
  + Three ways a secret reaches the transcript: pasted into a prompt,
    a `.env` file read wholesale into context, or a credential typed
    on a command line.
  + The transcript persists as a JSONL file long after the terminal
    window closes, so a secret typed into it does not vanish with
    the session.
  + The fix is timing, not carefulness: fetch the key at the moment
    of use rather than trying never to type it.
  + A script can fetch a key straight from the keychain and call the
    API itself, so Claude reads the result but never the credential.

- apiKeyHelper and sandbox credentials
  + `apiKeyHelper` runs a command to produce the key at connection
    time, so it is never written into a settings file at all.
  + `sandbox.credentials` denies or masks credentials from a
    sandboxed process entirely — the process runs without ever
    holding the value.
  + Both keep a key out of the places a transcript or a shared config
    file could expose it — the settings file for one, the process
    environment for the other.

## Databases

### Why Database Anything

- What a database is
  + The question a folder answers is "what files are here"; the
    question it cannot answer is "which matters have an unbilled
    hearing in the next fourteen days".
  + A database holds rows with named columns and links between them —
    a `matters` table, a `clients` table, one row per invoice.
  + The most common shape is relational — fixed columns and links
    between them, such as `matters`, `clients`, and `invoices` — but
    several other shapes exist for different needs.
  + Recording that a letter states the deadline as 14 October does not
    make 14 October correct; a database stores claims, not facts.

- Why put your own files in one
  + The archive stays exactly where it is; what goes into the
    database is a row per document saying what it is, which matter it
    belongs to, and the path on disk.
  + Once the rows exist, one query returns every noncompete sent to a
    New Jersey client since 2023, with no folder opened.
  + A document nobody indexed is invisible to every query, and the
    query returns no error saying so.

- SQLite first
  + SQLite is one file, no server, no setup — it ships inside Python
    already, and it is the default for anything living on one
    machine.
  + `sqlite3 matters.db` creates the database on the spot; deleting
    the file deletes the database, with nothing else to clean up.
  + Reaching for Postgres before it is needed costs a server process
    to keep running and a connection string to manage, for a machine
    that never needed either.
  + The path is SQLite first, moving to Postgres only when a second
    machine needs to reach the same data — that is the one condition
    that changes the answer.
  + The questions to answer are named up front; Claude designs the
    tables from them, not the other way round.

### Relational

- Relational databases
  + Every row in a `matters` table, a `clients` table, or an
    `invoices` table carries the same named columns and can link to
    rows in another table.
  + A `matters` row points at a `clients` row and at many `documents`
    rows; that link is the thing a folder cannot hold.
  + Matters, clients, and invoices already exist as record-shaped data
    in most practices, so relational is usually the shape already at
    hand, not one invented for the occasion.
  + Changing a link's shape after rows exist means migrating every row
    that used the old shape, not just adding a column.

- PostgreSQL
  + Postgres is the serious open-source server — the step up from
    SQLite once a single file and no server stop being enough.
  + It handles JSON, full-text search, and vectors natively, so one
    Postgres instance often covers three of the other database types
    covered later in this part.
  + The path SQLite leads to runs through Postgres the moment a
    second machine, a second person, or a second automation needs to
    reach the same data at once.
  + A server process differs from a file: something has to start it,
    keep it running, and grant a connection to it, rather than just
    opening a path.
  + Several people or automations reading and writing the same
    `matters` table at once is exactly the condition Postgres is
    built for and a single SQLite file is not.
  + Nothing answers while the server is stopped — a stopped Postgres
    instance is not a slower file, it is no database at all until
    restarted.

- DuckDB and the others
  + MySQL, and its fork MariaDB, are older and hugely deployed —
    mostly the database behind existing websites, not a first choice
    for a new one.
  + SQL Server and Oracle are commercial and licensed — databases a
    practice inherits from an enterprise case-management system, not
    ones it installs by choice.
  + DuckDB has SQLite's shape, one file and no server, but it is
    columnar rather than row-based, built to answer questions across
    many rows at once.
  + DuckDB queries CSV and Parquet files directly, where they already
    sit on disk, with no import step first.
  + None of MySQL, SQL Server, Oracle, or DuckDB is chosen from
    scratch — they show up because an existing system already uses
    one, not because SQLite and Postgres stopped being enough.
  + A firm's billing export lands as a folder of CSVs each month;
    DuckDB queries them directly for "total billed per client this
    quarter" with no database to load them into first.

### The Other Kinds

- Document databases
  + Document databases hold JSON blobs of varying shape — no fixed
    columns, so one record can carry a field another record lacks.
  + MongoDB is the one everyone names: collections of JSON documents
    with no fixed schema. CouchDB is older and syncs well between
    machines. Firestore and DynamoDB are hosted, by Google and
    Amazon.
  + A scraped court listing shows why: one hearing's record carries a
    room number, the next does not, and a typo in a key silently
    becomes a new field that nothing queries, with no error raised.
  + The use case is saving scraped or API data before deciding its
    final structure, since the shape can vary record to record and
    nothing is rejected for not matching.
  + A `jsonb` column in Postgres, or a JSON column in SQLite, covers
    this without installing MongoDB — the pragmatic answer before
    reaching for a dedicated document database.

- Key-value stores
  + A key-value store holds one value per key and nothing else — no
    columns, no relations, just a fast lookup by name.
  + In practice it is a notepad that survives between runs: an
    archiver running every ten minutes asks, key by message ID, "seen
    this?" before processing it again.
  + The same shape covers an expensive API answer not worth paying for
    twice, a "job already running, do not start another" flag, and a
    count of how many times something happened today.
  + Redis is the standard — a server holding everything in memory, so
    lookups are very fast; Valkey is the open fork that continued
    after Redis changed its licence.
  + Memcached is cache-only and simpler; LMDB and RocksDB are
    embedded, a file on disk with no server, used inside other
    programs; etcd and Consul are for machines agreeing on shared
    settings across a network.
  + Nothing expires on its own unless the code that wrote the key also
    sets an expiry — a "seen this" flag stays forever unless something
    deletes it.
  + The path is a two-column SQLite table on one machine, installing
    nothing new; Redis earns its place only when several processes
    need to share the same notepad at once.

- Columnar databases
  + A columnar database reads only the columns a query asks for,
    rather than fetching every row whole — that is what makes
    across-every-row questions much faster.
  + "What did I bill per client per month for three years" or "which
    of these 400,000 log lines are errors, grouped by hour" run
    roughly a hundred times faster columnar than relational.
  + DuckDB is the one that matters for a single practice; ClickHouse
    is the server version for constant streams; BigQuery, Snowflake,
    and Redshift are the hosted, enterprise-scale versions.
  + It is bad at the opposite question — fetching one matter's whole
    record, which is what most days actually require — because that
    means touching every column instead of the few a report needs.
  + It earns its place once reporting across the whole archive —
    total billed, error counts, trends over years — starts being
    asked for, not before.

- Graph databases
  + A graph database stores the connections as the primary thing —
    who owns what, who is related to whom — and answers "everyone
    connected to this person within four steps" directly, where a
    relational join chain makes that painful.
  + Corporate ownership chains, conflict-of-interest checks across a
    client base, and family relationships in an immigration matter
    are what a practice would actually build one for.
  + Neo4j is the standard, run as a server; Kuzu is embedded, one
    file; Memgraph is a faster server option.
  + A client base of two hundred with one owner each buys nothing from
    a graph database — SQLite's recursive queries reach further than
    most practices ever need.

- Time-series databases
  + A time-series database stores the same measurement taken
    repeatedly and stamped with when, built to throw away old detail
    and keep only summaries — tracking what an automation costs per
    day, how long each run took, or rates over months.
  + InfluxDB and TimescaleDB are purpose-built for this; Prometheus is
    for machine metrics specifically.
  + A SQLite table with a timestamp column is enough for most of
    this, without a dedicated time-series database at all.

### Search

- Full-text search
  + `grep` scans every file every time it runs and matches only what
    was typed exactly — nothing is prebuilt, so nothing is wrong, but
    nothing is fast either.
  + A full-text index is built once and then answers instantly,
    ranking the best hits first instead of returning matches in file
    order.
  + Stemming means the index knows "filed", "filing", and "files" are
    the same word, so a search for one finds all three without asking
    for each separately.
  + SQLite FTS5 is built into SQLite already, so search across every
    letter and pleading in an archive needs nothing installed.
  + Postgres `tsvector` does the same job inside Postgres, for an
    archive that already lives there.
  + Tantivy and Meilisearch are standalone and rank better than
    either built-in option; Elasticsearch is the heavyweight, a
    server of its own, for an archive that outgrows both.
  + An index built on Monday does not know about Tuesday's filings —
    it goes stale silently, returning a confident empty result
    instead of an error saying it is out of date.

- Vector search
  + Full-text finds "termination" as a word; vector search finds the
    clause about ending the agreement early even though it never uses
    that word.
  + Each document becomes a list of numbers from an embedding model;
    similar meanings land near each other in that space, and a search
    looks for what is nearby.
  + The use case is finding the clause about early termination, or
    the passage capping liability, across a contract archive without
    knowing the exact wording each one used.
  + `sqlite-vec` adds vector search to SQLite as an extension, with no
    separate service to run.
  + `pgvector` does the same job inside Postgres, for an archive that
    already lives there.
  + Chroma, Qdrant, and LanceDB are standalone vector databases, for
    an archive that outgrows an extension bolted onto an existing
    one.
  + Changing the embedding model makes every vector already stored
    meaningless against the new ones — the whole archive has to be
    re-embedded, not just the new documents.

- Retrieval in practice
  + No model can be handed the whole archive at once — a Claude Code
    retrieval setup finds the six relevant passages out of ten
    thousand and hands only those to the model.
  + Full-text and vector search answer different questions — "every
    letter using the word 'forfeiture'" against "the clause about
    ending it early" — so a working setup usually runs both, not one
    or the other.
  + Retrieval sits in between the archive and the model: it narrows
    ten thousand documents down to the handful actually relevant to
    the question asked.
  + An answer built on the wrong six passages reads exactly as
    confident as one built on the right six — nothing in the reply
    signals that retrieval picked badly.

### With the Harness

- Getting your material in
  + Material arrives as scanner PDFs, DOCX from clients, email
    attachments, and exports from a case-management system — not as
    one clean format.
  + Getting it in is three steps: extract the text, classify what it
    is (engagement letter, pleading, invoice), and record where it
    lives.
  + `pdftotext` is the test for whether OCR is needed at all: a blank
    result means the PDF needs tesseract before anything else.
  + tesseract does the OCR itself — a scan with no text layer becomes
    text once tesseract has run over it.
  + The original PDF never moves — the database row records only its
    path, not a copy of the file.
  + An import that OCR'd a blank page writes a row with empty text and
    no error; the fix is counting rows against files afterward to
    catch the gap.

- Asking questions of your own data
  + Questions worth asking become ordinary once the material is in:
    "which matters have no engagement letter on file", "every letter
    mentioning an appeal deadline last quarter", "what did I bill
    Ramirez between March and June".
  + The question is asked in plain language; Claude writes the SQL
    that answers it.
  + The pieces already covered do the work together: FTS5 finds the
    word, sqlite-vec finds the clause phrased differently, and the
    `matters` table says whose record it belongs to.
  + A query that joins the wrong way returns a number that looks
    exactly as authoritative as a right one — the check is running it
    against a matter whose answer is already known and comparing.

## Automatic Outputs

### Document Automation

- Document pipelines
  + Document pipelines are commands you run, not libraries you import.
  + Together they turn an incoming document into something Claude can
    read, and Claude's output into a document a person can open.
  + Which command depends on what arrived: `pdftotext` for a text PDF,
    `tesseract` for a scan, `pandoc` for a format swap, LibreOffice
    headless for an Office file that has to become a PDF.
  + A scanned bundle and a filed PDF look identical in Preview and are
    not the same thing at all — one has a text layer, one is pictures.

- poppler and pdftotext
  + poppler is a command-line PDF toolkit; `pdftotext` is the command in
    it that pulls a PDF's text out as plain text.
  + It also splits a bundle into single pages, merges pages into one
    file, and renders a page to an image.
  + `pdftotext scan.pdf -` returning nothing is the test: no text back
    means the PDF is pictures, not words, and needs tesseract next.
  + It is the first command to run on any incoming filing or scanned
    exhibit: it costs nothing and names which kind of PDF just arrived.
  + On a text PDF it returns the whole document in under a second, which
    is why it beats guessing from how the file looks.

- tesseract and OCR
  + tesseract is OCR: it turns a scan with no text layer into text,
    reading the pixels of a scanned filing the way a person would.
  + Used on incoming scanned exhibits, faxed correspondence, and old
    filings that only exist as images — anything `pdftotext` came back
    empty on.
  + A poor scan produces confident wrong text — a `1` misread as a `7`
    in a deadline date, with nothing in the output flagging the error.
  + Running it on a PDF that already has a text layer throws the good
    text away and replaces it with tesseract's guess.
  + A PDF that already answers `pdftotext` never needs OCR, which is
    why that check comes first.

- pandoc
  + pandoc converts between text formats — Markdown to DOCX, DOCX to
    Markdown, HTML to PDF — with one command.
  + Markdown to DOCX keeps the words and loses the styling; DOCX back to
    Markdown loses tracked changes and comments outright — the loss
    that bites when a redlined engagement letter comes back from
    opposing counsel and gets converted to Markdown.
  + A first draft survives the round trip through Markdown; a document
    already carrying revisions and comments only survives by staying
    in DOCX.

- LibreOffice headless
  + LibreOffice headless runs Word and Excel with no window, driven from
    a script instead of a person clicking File > Export.
  + `soffice --headless --convert-to pdf letter.docx` is the whole
    command, and it keeps the firm's letterhead where pandoc would strip
    it.
  + It reads XLSX too — a billing spreadsheet goes in and a table
    Claude can read comes out.
  + Fonts missing on the machine running the conversion are substituted
    silently, so a letter rendered on the server does not always match
    the one on your desk.

### Templates

- Templating
  + A template is a document with holes filled from data — an
    engagement letter with `{{client_name}}` and `{{matter_type}}` where
    the details go, written once and filled a hundred times.
  + The point is not saved typing: the model does not draft the
    boilerplate, it only supplies the values.
  + The fixed parts of the letter — the firm's boilerplate, terms and
    closing language — never move; only the holes like
    `{{client_name}}` and `{{matter_type}}` change row to row.
  + Free drafting lets approved wording drift a little every time; a
    template is the only way it cannot.
  + The values come from a row of data — a client intake form, a matter
    record, a spreadsheet — not from Claude drafting them fresh.

- Jinja and docxtpl
  + Jinja is the templating engine for Python — the general tool behind
    the `{{ }}` holes.
  + docxtpl fills a DOCX in place, so letterhead, styles and numbering
    survive untouched around the filled-in values.
  + The output is a real, editable Word document, not a rendered image
    of one, so a lawyer can still mark it up after Claude fills it in.
  + docxtpl is the asset worth keeping: it does the Word-specific part
    that Jinja alone does not touch.

- Filling a form PDF
  + A form PDF like an immigration Form N-400 already carries named
    fields — the blanks exist before anything is filled in.
  + Filling one means writing values into those existing fields by
    name, with `pdftk` or `pypdf`, not building the page from nothing.
  + Flattening turns the filled-in fields into fixed page content, so
    the values can no longer be edited or tabbed through afterward.
  + That distinction is why filling is not templating: nothing is
    generated from holes in a document — the fields were already there.
  + An N-400's fields are written from the client's intake record, one
    row per applicant, the same `pdftk` or `pypdf` script run down a
    list rather than typed by hand.
  + The opposite case — a PDF built from scratch, with no fields to
    fill — is templated as DOCX or Typst first and converted to PDF at
    the end, the same route as any other typeset document.

- Typst and LaTeX
  + Typesetting is for documents where page breaks, running headers and
    automatic renumbering have to be exactly right — a bundle index, an
    exhibit list — not for a document that is mostly words.
  + Typst and LaTeX are the two typesetting engines; both take source
    text and control the layout in ways a word processor does not.
  + For a two-page engagement letter, either one is more machinery than
    the job needs — docxtpl is the right answer there instead.
  + Typst and LaTeX are for output templated from scratch that has to
    be typeset, not for values filled into an existing Word layout.

### Artifacts

- What an artifact is
  + An artifact is a self-contained web page Claude Code publishes from
    a session to a private URL on claude.ai — the cheapest way for work
    to leave the terminal and become something a person can open.
  + The file itself is one HTML file with styles and script inline and
    no server behind it — nothing to host, nothing to keep running.
  + Used for a matter status page a client can check, a summary of an
    overnight run, a chart of the month's processing, or a checklist
    that fills in while a long job proceeds.
  + Requires a paid plan and a `/login` session on the Anthropic API —
    not Bedrock, Vertex or Foundry.
  + `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` stops a headless run from
    trying to open a browser that is not there.

- Publishing and revising
  + Publishing prompts once per artifact — after the first publish, the
    same artifact is revised, not republished from scratch.
  + Revising means editing the file and publishing again to the same
    URL; anyone already looking at the page sees it change under them.
  + Every publish is kept as a version, so a prior state of the page is
    never simply lost.
  + A later session not given the existing URL publishes a second,
    separate artifact instead of updating the first.
  + An artifact is private to its creator on creation, on every plan.
  + Pro and Max share by sending the link to anyone; Team and
    Enterprise share inside the organisation only, with public links
    off until an owner turns them on.

- Connectors inside an artifact
  + A published page may call MCP connectors when it loads — the same
    connectors described earlier in this level, running inside the
    page.
  + A status page built this way fetches its own fresh data every time
    it is opened, using the viewer's connectors and account.
  + That means the automation that built the page does not have to run
    again to keep it current — the page does the refreshing itself.
  + Two viewers can see different things on the same URL, because each
    one runs on their own connectors — a client with none sees an empty
    page where the firm sees live data.

- The content policy
  + The content policy blocks every external script, stylesheet, font
    and image — nothing loads in from outside the page.
  + It blocks all fetch, XHR and WebSocket traffic too — no outbound
    request from inside the page's own script.
  + Everything the page needs has to be inlined into the one HTML file,
    styles, scripts and images alike, or it does not render.
  + Sixteen megabytes is the ceiling on that single file.
  + Together that is what makes something an artifact rather than an
    ordinary web page: self-contained, and bounded in size.

### Static Sites

- Static site generators
  + A generator turns a folder of Markdown into plain HTML files with
    no server logic — nothing to run, nothing to keep alive.
  + Because the output is just files, it works wherever it is put: a
    folder on a laptop, a bucket, any static host.
  + Hugo, Zola, Eleventy and MkDocs are the generators named here;
    `mkdocs build` over a folder of notes gives a searchable internal
    reference with a search box and no server behind it.
  + GitHub Pages hosts the result for free, straight from the same repo
    the Markdown lives in.
  + A site hosted this way is public by default to anyone with the
    URL — nothing about publishing it asks first.

- Publishing what an automation makes
  + This is the cheapest way for an automation to publish something a
    person can read: a client-facing status page regenerated nightly,
    an internal reference built from your own notes, a published
    version of something like this course.
  + A nightly `claude -p` run rewrites `content/status.md`, the
    generator rebuilds the site, and the client opens the same URL to
    this morning's position — no new link to send.
  + A static page is only as current as its last build — it is
    generated ahead of time, not built on request — which is what
    makes the nightly rebuild load-bearing.
  + A GitHub Pages site is public to anyone with the URL, so a matter
    status page with client names on it belongs behind Tailscale or
    inside an artifact instead.

## Hosting and Serving

### Web Servers

- What a web server is
  + A web server listens on one port and answers whatever request
    arrives at it.
  + The door is open only while the process runs; stop it and the
    form and the webhook both go dark at once.
  + It is how an automation gets a front door: a client fills in a
    form, or another service calls a URL when something happens — a
    case system posting a status change, say.
  + It answers with a page built for a person, or with `JSON` built
    for another program — the same listener, a different reply
    depending on who is asking.

- Reverse proxies
  + A reverse proxy sits in front of the real web server and takes on
    the HTTPS certificate, so it is renewed and served in one place
    rather than inside every app behind it.
  + A browser error says only that the site cannot be reached; it
    does not say whether the proxy is down or the server behind it is
    — the cost of the extra hop.
  + Several services can sit behind one address — the intake form and
    a status page, say — routed to different backends.
  + It refuses traffic that was not invited, so the app behind it
    never sees a connection that should not have reached it.

- Caddy, nginx and certificates
  + Caddy gets a certificate automatically: a Caddyfile as short as
    `intake.example.com { reverse_proxy localhost:8080 }` is enough,
    and the certificate appears on its own.
  + A certificate belongs to a name, not a machine: moving the box to
    a new address does not break it, but changing the name does.
  + nginx is the standard and leaves certificates to you — it wants
    `certbot` obtaining and renewing them separately.
  + A certificate is what turns the address into a real `https://`
    one to hand to a client, rather than one a browser warns about
    before the page loads.

- Tunnels
  + Tailscale and a tunnel are two separate ways to avoid opening the
    machine to the internet at all.
  + A tunnel is what gives the machine a name reachable from outside;
    the client's browser still connects straight to it, with no
    hosting layer in between.
  + It changes how the machine is reached, not what is listening on
    it — the web server behind the tunnel is the same one Caddy
    already fronts.

- Self-hosting
  + Self-hosting means the files genuinely land on your own disk: the
    client's browser connects straight to your machine, with no third
    party holding a copy in between.
  + A domain name costs around ten pounds a year and can point at
    your own machine exactly as easily as at a host's — a name is
    memorable, a number is not, and home addresses change.
  + The one condition is that the machine stays awake: a laptop that
    sleeps overnight takes the form down with it.
  + What paid hosting sells beyond that is someone else's electricity,
    a connection that does not drop, and blame that lands elsewhere
    when something breaks.
  + For a form only you depend on — the intake page, say — your own
    machine is a reasonable choice.

- A worked example — the intake form
  + The page itself is small: three fields — name, matter type, and
    an upload for a passport scan.
  + A web server on your own machine serves that one page directly,
    with nothing published elsewhere.
  + Caddy fronts it with a real `https://` address, the one that
    actually gets sent to the client.
  + Submitting writes three things at once: the uploaded files into a
    case folder, a row into SQLite recording the matter, and a job
    into the queue.
  + Cron picks the job up and runs `claude -p` with the intake skill.
  + That skill reads the uploaded documents, extracts the client's
    and matter's details, and drafts the engagement letter.
  + The letter is drafted and the matter filed before anyone opens
    the laptop — the whole intake ran unattended.
  + A form that accepts uploads accepts files from strangers, so the
    size is capped, the type checked, and what arrives is never
    handed straight to a shell.

### Containers

- What a container is
  + A container is a sealed box holding a program and everything it
    needs — its own filesystem, its own packages, its own version of
    Python.
  + It runs identically on a laptop, a rented box, or a reader's
    machine — nothing outside the box is touched, so a Postgres you
    experiment with inside it vanishes cleanly when deleted.
  + Containers are Linux only, and not a virtual machine — running
    one against a clean machine catches "works here because I have
    it" bugs that a laptop full of installed tools hides.
  + A container can still *build* Mac and Windows binaries, since Go
    cross-compiles — building and running are different acts, and the
    container that emits `tutor.exe` cannot open it.
  + For Claude Code it is also containment: an agent working inside
    one cannot damage the machine around it.
  + Docker is the tool; a devcontainer is the same idea wired into an
    editor.

- Images and registries
  + The image travels through a registry — Docker Hub, or a cloud's
    own artifact registry — pushed from here, pulled there.
  + On a rented box the sequence is three steps: install Docker, pull
    the image, run it.
  + The image you tested is the thing that runs; rebuilding on the
    box produces a different image, which may not behave the same
    way.
  + The dependencies travel inside the image, so the box itself needs
    nothing else installed — an image built to OCR scanned filings
    needs nothing more than Docker on the box it runs on.
  + Architecture matters: a laptop's chip and a rented box's chip can
    differ, so the image has to be built for the target, or built on
    the box itself.
  + Services like Cloud Run skip the machine entirely — hand over an
    image and it runs it, with no box to manage.

- Reproducibility
  + A container is a written-down recipe of every dependency, so what
    worked in March still works in December, on a machine not yet
    built.
  + Reproducibility alone accounts for most container use, with the
    containment of an agent as a bonus on top of it.
  + Deployment is easier — move the box to a rented server rather
    than reinstalling forty things and finding the versions differ.
  + Two projects needing incompatible versions — different Postgres
    versions, say — sit side by side without conflict.
  + Trying software costs one command: use it, delete it, and nothing
    is left behind on the machine.
  + Twenty identical boxes can run the same job in parallel, each one
    processing its own batch of matters overnight.

- Running one on a box that never sleeps
  + A laptop cannot run an unattended job overnight if it is closed or
    asleep — a rented box that never sleeps is the fix, running the
    same container.
  + It runs what cannot wait for a laptop lid to open: a scheduled
    cron job, or a server backing something like the intake form.
  + The box needs only Docker installed; everything else the job
    needs travels inside the image, exactly as it does on a laptop.
  + Building and running are different acts: an image built for the
    box does not have to be built on the laptop, and the box needs
    only the ability to run what already exists.

## Agent SDK

### The SDK Harness

- What the Agent SDK is
  + The Agent SDK is the same agent loop that runs Claude Code, offered
    as a library for your own Python or TypeScript program.
  + There is no terminal: your program decides when to start a turn, not
    a person pressing Enter.
  + Your program sees every message as it arrives, and can refuse a tool
    call in code — denying a write outside a client's own matter
    folder, say — rather than at a permission prompt.
  + What is unchanged underneath is the same agent loop, the same tools,
    and the same `.claude` machinery Level Two built.
  + It removes the terminal, not the engineering — sessions, permissions
    and cost still have to be designed, just in code instead of a
    prompt.

- How it differs from headless sessions
  + The prior question is whether the SDK is needed at all: `claude -p
    --output-format json` also runs Claude non-interactively, from any
    language, in one line of shell.
  + A headless session is that one line, fired from cron or a script,
    with one shot at a final answer and nothing seen in between.
  + The SDK earns its place in four cases: approving tools conditionally,
    streaming partial output to a user, holding a session open across
    many exchanges, or billing a customer by the turn.
  + The shape of the difference is mid-run intervention: `claude -p`
    hands back one final answer, the SDK hands back every message as it
    happens.
  + A nightly job that OCRs the day's scans and exits only needs
    `claude -p`; a paralegal's intake tool that streams status back to a
    browser needs the SDK.

- Use cases
  + The back end of an intake form: it submits documents and watches for
    the answer as messages arrive, rather than waiting on one blocking
    call.
  + A service runs one agent per customer, with each customer's files
    walled off from every other's.
  + Anything with a user waiting on the other end of a connection, where
    a blank screen for the length of a headless run is not acceptable.

### Building an SDK

- Running a query and holding a session
  + Two entry points exist in either language, one for a single question
    and one for a held-open session.
  + `query()` answers a single question and ends — whether a bundle has
    a text layer, say — returning a stream of messages for that one run.
  + Python's `ClaudeSDKClient` and TypeScript's streaming input keep a
    session alive across repeated exchanges, the shape a paralegal's
    back-and-forth on one matter needs.
  + The session-holding entry point also allows interrupting the run
    mid-thought, which `query()` cannot do.

- The messages that come back
  + What comes back is a sequence of typed messages, not a single string
    reply.
  + The first message is a `SystemMessage` with subtype `init`, carrying
    the session ID.
  + An `AssistantMessage` arrives per reply, as the model produces it.
  + A `UserMessage` arrives per tool result, one per tool call answered.
  + A turn is one trip through assistant-then-tools — a reply followed by
    the tool calls it made.
  + The final message is a `ResultMessage`, holding cost, tokens and the
    session ID — the number to check against a per-matter budget.
  + That sequence makes live status possible, per-turn billing, and a
    log of exactly what happened and when.

- Stopping it running forever
  + Two limits exist, and neither is a clock: `max_turns` and
    `max_budget_usd`.
  + `max_turns` counts tool-using turns only.
  + `max_budget_usd` stops on a client-side cost estimate, not a metered
    bill.
  + A session has no overall timeout and will not end on its own, so an
    unattended program needs something watching from outside it — a
    systemd timeout, or `timeout 3600` wrapped around an overnight
    intake run.

- The permission callback
  + `can_use_tool` is the permission callback: it decides whether a
    specific tool call proceeds or is refused, in code rather than at a
    prompt.
  + It fires only when the decision would otherwise have gone to a
    prompt: an allow rule for `Read` never reaches it at all.
  + That is why it is not the full security boundary it looks like — a
    call already cleared by an allow rule is never judged by the
    callback.
  + Six permission modes exist, and the callback sits beneath all of
    them, seeing only what the mode does not already resolve.
  + A deny rule on writes outside `matters/<client>/` outranks
    everything, including `bypassPermissions`, which itself refuses to
    run as root.

- One process, many customers
  + By default, an SDK session loads the same `.claude` machinery Level
    Two built: settings, CLAUDE.md, filesystem hooks, skills and
    subagents.
  + `setting_sources: []` shuts all of that out, which is what running
    one process for several customers requires.
  + Each customer additionally needs its own working directory — a
    client's own matter folder — and its own `CLAUDE_CONFIG_DIR`, so one
    customer's settings cannot leak into another's session.
  + Without that separation, one client's CLAUDE.md, skills or files
    reach a different client's run.

- Sessions and where they live
  + Sessions persist as JSONL files under `~/.claude/projects/`.
  + A session can be resumed by its ID — picking up the Ramirez matter's
    thread next week exactly where it left off.
  + A session can also be forked into a new branch, to draft a second
    engagement letter without losing the first.
  + Forking leaves the original session intact, untouched by whatever
    the fork does next.
  + A `SessionStore` adapter mirrors sessions to S3, Redis or Postgres
    instead of the local JSONL file.
  + That mirroring matters the moment the program runs somewhere that
    gets rebuilt — a container redeploy wipes `~/.claude/projects/`
    along with it.

- What it consumes
  + Every `query()` spawns the `claude` binary as its own subprocess.
  + Twenty concurrent intake sessions on one box means twenty processes
    running at once, not twenty threads inside one.
  + Reckon on a gigabyte of memory, five gigabytes of disk and a CPU
    core, per process, as the floor.
  + `total_cost_usd` is an estimate, read from a price table compiled
    into the build, not a metered figure from Anthropic.
  + That estimate is good enough for a budget cap; it is not accurate
    enough to invoice a customer from.

### Deploying and Integrating SDKs

- The shapes a deployment takes
  + The four faces are a terminal program, a web page, a desktop
    application and a phone — the same SDK code runs behind every one.
  + The paralegal using the intake tool never learns Claude is behind
    it; they see a form and a drafted letter.
  + Choosing between the four is about who is on the other side and what
    they already have open, not about the SDK underneath.
  + The face worth building is the one already within reach — a Python
    TUI that gets finished beats a React app that does not.

- Behind a TUI
  + `ClaudeSDKClient` in a loop with `input()` and `print()` is a
    deployment.
  + No server, no certificate and no hosting bill, and it runs where the
    matter folders already are.
  + It reaches exactly one person on one machine, and stops dead at the
    colleague who will not open a terminal.

- Behind a web page
  + A small FastAPI or Express server holds the SDK; the browser holds
    the form — the intake page from Web Servers, with the SDK behind it
    instead of a queue.
  + Anyone who can reach the URL can use it, which is the whole gain and
    the whole problem.
  + No authentication arrives with a browser: a login, a shared secret,
    or a Tailscale-only address is yours to add.
  + Files uploaded through it land on your disk under your own
    permissions, and the SDK runs directly against them.

- Inside a desktop app
  + Electron or Tauri wraps the same web page, installed with an icon,
    so to the user it is a program rather than a website.
  + Code signing on macOS, an updater, and every colleague's machine
    sitting at a different version all become your job.
  + The window hides where the work happens: the model call still leaves
    the machine, and a client's documents go with it.

- On a phone
  + The agent runs on the box; the phone holds only a page or a chat
    window.
  + The phone therefore needs nothing but a browser and a connection —
    no install, no key.
  + The cheapest version is the web page above, opened on a phone; a
    Telegram channel is cheaper still.
  + Approving a redaction from a train is the case that justifies
    building this face at all.
  + A dropped connection must not lose the run: the session lives on the
    box, resumable by ID, and the phone simply reconnects to it.

- Where the process actually runs
  + The process runs in one of three places: on your own machine, on a
    rented box, or in a container on something like Cloud Run.
  + A laptop that sleeps is not a host — an intake form nobody can
    submit at 11pm is a form that does not work.
  + Working when you tested it standing over it is not evidence it works
    at 3am from a client's phone.

- Streaming to someone waiting
  + The SDK hands you an `AssistantMessage` per reply and a
    `UserMessage` per tool result as they arrive; that stream is what
    you put on the screen.
  + Ninety seconds of blank screen reads as broken, and the client
    reloads and submits the form twice.
  + What holds the wait is the tool names as they run — "reading the
    passport scan", "checking the matter number".
  + The long step produces no message of its own: OCR on a forty-page
    bundle is one tool call, so print something before it starts.

- Keeping it up
  + A deployment has to survive the box rebooting and the API key
    rotating — the operational half of staying up.
  + It also has to survive a model version changing underneath it,
    unannounced, since the SDK always calls the latest.
  + Someone else using it raises the need for a log of what actually
    happened.
  + It also raises the need for a way to say what broke, and a person to
    say it to — not a stack trace nobody reads.
  + Resuming a customer's thread next week means the session JSONL
    outliving the machine — a `SessionStore` to Postgres or S3, not
    `~/.claude/projects/`.
  + The loud cost is the model bill, visible in `total_cost_usd`; the
    quiet cost is a gigabyte of memory per concurrent session, and your
    evenings spent answering "it did not work".

### Notifications

- Notification transports
  + A notification transport is how an unattended job reaches you
    when you are not at the machine; without one, you find out only
    when you next look, which may be days later.
  + A notification for every processed matter is a notification for
    none — what earns a message is what failed and what needs a
    decision, not what went fine.
  + A run that failed, a document drafted and awaiting approval, a
    deadline detected in an incoming letter, or the one matter in
    twelve that could not be processed — all clear that bar.
  + A two-way transport adds the reply: a decision can be sent back
    from the phone rather than waiting until you are at the machine.

- Telegram, ntfy and email
  + Telegram or Discord reaches you through a bot posting into a chat
    you already have open.
  + `ntfy` pushes straight to a phone, needing nothing more than a
    topic name.
  + Email through a provider's API suits a record that should sit in
    an inbox, not just an alert.
  + A desktop notification is the simplest of the four and dies at
    the edge of the machine — nobody on the train sees it.
  + Where you already look decides which transport works: an email
    sent at 3am is read at 9, however fast it sent.

- Claude Code in Slack
  + Slack is not simply another notification channel — "Claude Code
    in Slack" is its own integration.
  + `@Claude` mentioned in a channel spawns a cloud session, not a
    session running on your own machine.
  + It is two-way: it posts status and summaries back into the
    channel as it works — the intake skill's change, say, narrated as
    it runs.
  + It ends with a button to open a pull request from what it did.
  + It works in channels only, never in DMs, and opens one pull
    request per session.
  + It needs a claude.ai login, a connected GitHub account, and a
    paid plan — Bedrock, Vertex and Foundry cannot use it.
  + It is being replaced by Claude Tag on Team and Enterprise plans.


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
    + Three noncompetes, one each from New Jersey, New York and Connecticut
    + Three invented deal profiles — emails or notes of the kind a partner
      actually sends, carrying the employee's name, the company, the term,
      the territory. The variables arrive buried in prose, not on a form
    + Enough that the reader can feed the library, then draft against it
    + Still to be built — the corpus does not exist yet

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

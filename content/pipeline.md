# Level 1 ## This Wiki - This version - About this wiki
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
  - Explain how level 2 was all manual: start sessions, ask agents
  - Explain how level 2 depended on agents to do everything; more tokens and more risk
  - Explain that it gets a lot easier, a lot cheaper, and a lot better
    - Everything is code--including what agents do
    - Move the code from agents to scripts, and everything gets much faster, much safer, and much cheaper
      - Give one or two examples here, with visuals, of a level 2-like pipeline (agent/subagent chain only) versus a scripted pipeline to do the same thing (starts automatically, works/logs automatically, sends/notifies of results automatically, starts the next session automatically, etc)
  - Explain that with Claude Code features and software packages like automators, connectors, databases, and servers, and you can automate your life--and any business
    - Give ample examples here as well    
  - Explain that the reader stops running Claude Code by hand and starts building things that run on it, reaching their own systems instead of only the terminal

- The shape of an automated system
  - Four parts to any automated pipeline: trigger, input, work, output
    - Walk one pipeline through all four parts end to end: what triggers it, what arrives as input, what Claude Code does as the work step, what lands as output
  - Four kinds of trigger: a clock, a file appearing, a request arriving, a message pushed in
  - Claude Code is the work step, never the trigger
  - Output has to land somewhere real -- not sit in the transcript

- Less is more
  - Touch the cost point in a line, not a section -- it was already made above
  - What reduces to a rule belongs in a script; what needs judgement stays with the agent

### Scripted Behavior

- What a script is for
  - Claude writes the script; something else -- cron, a shell, a scheduled job -- runs it later, after the session ends
  - A script outlives the session that wrote it
    - A filing rule agreed in March still firing in December, unattended, months after that session is gone, is the example this point needs

- Python, Node and Bun
  - Python is the default -- already on every machine, every library already there
  - Node comes bundled with the web-development world instead
  - Bun: Node, but faster, TypeScript built in, no build step
  - The reader names the outcome, not the runtime; the choice shows up after, as a file

- A script instead of an agent turn
  - An agent turn repeats itself slightly differently each run; a script repeats identically
  - The split that decides which gets used
    - Reduces to a rule: filing by filename, computing a deadline, checksumming a count
    - Needs judgement: whether a letter mentions a deadline, whether two spellings name the same client
  - What a script cannot detect at all
    - A scan that's upside down
    - A wrong matter number written on the form

### Environments

- Virtual environments
  - System-wide installs collide: two projects needing different versions of the same package, one breaks the other
  - `.venv` sits inside the project; Python looks there first, before the system install
    - A diagram would do this best: the same package at two versions, one in `.venv`, one system-wide, and which one actually runs
  - Delete the folder, the packages are gone -- nothing else to clean up
  - The name is Python's, not the problem: `node_modules`, Go's static binary, bundler, cargo all solve it another way
  - Bolted on rather than built in, because Python installed system-wide for decades
  - One layer lighter than a container: isolates the libraries, not the whole operating system

- uv, pipx and conda
  - `uv`: the same job as `.venv` and `pip`, a fraction of the time
  - `pipx`: installs CLI tools each into their own environment, not mixed into a project's
  - Conda goes further: installs the interpreter itself, plus non-Python things like compilers and CUDA -- costs weight and speed
  - Nothing to fix by switching to `uv` if conda already works

### Logs

- Unattended work fails quietly
  - A silent terminal doesn't mean nothing went wrong
    - Put two terminals side by side, one from a run that did nothing, one from a run that worked -- both empty, so looking tells you nothing
  - Exit code zero only means the last command returned zero, not that the work was done
  - The only evidence of what happened is a record written during the run

- Where logs go
  - A typed command's output dies with the terminal; a cron job's stdout goes to mail, or nowhere, unless redirected
  - The pattern: one job, one file, one known place -- `>> ~/logs/intake.log 2>&1`
  - A usable log line carries the time, the matter, what was done, the exit status
  - A log nobody reads is disk space, not a log

- Log aggregators
  - Twelve log files means nobody reads all twelve -- a failure sits unnoticed
  - An aggregator makes them one searchable place instead of twelve terminals
  - Answers what no single file can: which run failed and why, what Claude cost this month, whether a job ran, what was silently skipped
  - `journalctl` if systemd's already there; otherwise Loki or a timestamped SQLite table
  - A threshold call: twelve jobs justify one, two challenges on a laptop don't

### Language Servers

- What a language server is
  - Answers questions about your code, not the language -- which file defines a function, who calls it, what breaks if it changes
  - Knows the language already; has to be pointed at your project to know what a name means here
  - Without one, Claude greps and guesses -- guessing is where bugs enter
  - Grep returns every mention; the server returns the actual definition and every genuine caller
    - Put grep's hits next to the language server's for the same function name, and let the false hits grep includes that the server doesn't make the point

- The servers there are
  - They already exist, one per language -- nobody writes their own
  - One per language, not per project -- count the languages in the repo, that's the count
  - Tutor runs two side by side: one for the Go reader, one for the Python parity oracle
  - Scope is the repository: indexes what's under the folder, starts fresh in a different one

- Wiring one into Claude Code
  - Declared in `.lsp.json` at the plugin root, or inline in `plugin.json` under `lspServers`
  - Two compulsory fields: `command`, the binary already on `PATH`, and `extensionToLanguage`, mapping an extension to a language
    - A minimal `.lsp.json` for one language, with just the two compulsory fields and nothing else, makes this concrete fastest
  - Optional fields: `args`, `env`, `startupTimeout`, `restartOnCrash` (on by default), `maxRestarts`
  - Named in Claude Code's own docs: `typescript-language-server`, `pyright`, `rust-analyzer` -- installed with npm or pip
  - Project-scoped serves that repository alone; plugin-scoped ships to everyone who installs it
  - Four lines in a plugin buys every installer symbol navigation, nothing further to configure

- Diagnostics
  - On by default: every error the server sees lands in Claude's context the moment you edit
  - Off: navigation still works -- go-to-definition, find-references, hover; only the running commentary is lost
  - The trade-off: context space on every edit, against catching a broken line the instant it's written

## Triggers

### Schedulers

- What a scheduler is
  - An OS daemon that fires commands at set times, logged in or not, even through a reboot
  - cron, launchd and systemd timers are the same idea, picked by platform rather than by the job
  - The shape underneath all three: five fields and a command

- cron
  - Explain the shape of a cron line: a schedule, a command, and redirected output that keeps the record
    - `0 6 * * 1-5` is the schedule, `claude -p "run the intake skill"` the command, `>> ~/logs/intake.log 2>&1` the redirect
  - Already installed and running on every Linux and Mac box, nothing to add
  - Fires unattended on a box that never sleeps; Claude Code's own scheduler only runs inside a session already open
  - Doesn't check whether yesterday's run finished -- two runs racing over one matter folder need `flock`, not cron

- launchd
  - The macOS scheduler -- the only one Apple's own tooling assumes, though cron still runs there too
  - Fires on events as well as times, with no polling loop required
  - `RunAtLoad` fires a job missed while asleep on the next wake

- systemd timers
  - systemd timers are the Linux replacement for cron: a `.timer` paired with a `.service`, Linux only
    - Runs log to `journalctl -u intake.service`, not a hand-redirected file
  - `OnCalendar` sets the schedule; `Persistent=true` fires a missed run on the next boot
  - A timer can wait on another unit -- the intake job held until the database is up

- Claude Code's own scheduler
  - It queues a task inside a session already running -- not a system-level cron replacement
    - Give an example of a task scheduled mid-session -- check tomorrow's hearing list -- firing between turns before the session ends, and show it never interrupts work in progress
  - All its limits come from that one fact: it lives inside the session
    - Nothing fires if Claude Code isn't running -- close the terminal and the schedule closes with it
    - Expires after seven days unmet, jitters by up to thirty minutes, and fires only between turns
  - The rule: system cron for anything unattended, Claude's own scheduler only for a session already alive

- Machines that sleep
  - Neither cron nor launchd wakes a sleeping machine -- a missed job is simply missed
  - Both platforms catch up: `RunAtLoad` fires on next wake, `anacron` does the same on Linux
  - A job that can't be missed belongs on a box that never sleeps, not a laptop -- the case for cloud automation

### Watchers

- What a watcher is
  - Turns a folder into a trigger: something landing in it runs a command instantly
    - A scan, a saved file or an export lands in the folder, and a command fires immediately with nothing else in between -- the folder itself is the only interface a reader has to build
  - Cron polls every five minutes; a watcher is told by the OS the instant it happens, no delay
  - Only works while the watching process itself is running -- close its terminal and nothing fires

- inotify, fswatch and entr
  - `inotify` is the Linux kernel mechanism; `inotifywait` is the command that uses it -- Linux only
  - `fswatch` is the cross-platform wrapper, the same job on Linux and macOS
  - `entr` reruns its command whenever a watched file changes -- the friendliest of the three

- A folder as a trigger
  - A folder can be the entire interface -- something arrives, the watcher fires, Claude Code processes it
    - Walk a scan folder through end to end: a scanner writes into it, the watcher fires on the finished write, `claude -p` files what landed -- dropping a file in is the entire workflow a reader has to perform
  - Each job watches its own folder, so two watchers never race for the same file
  - `-e create` fires on the first byte, catching a scan half-written -- not what you want
    - Wait for `close_write`, or for the file size to stop changing, to know the write is actually done

### Queues

- What a queue is
  - Keeps forty documents landing at once from being processed forty at a time and melting the machine
    - Picture forty scans arriving together, two workers pulling off the front at a controlled rate while the other thirty-eight wait their turn
  - A failed job goes back into the line and gets retried, rather than vanishing
  - The trigger and the queue are separate jobs -- a watcher adds a row and gets out of the way

- Redis, SQLite and the serious version
  - A `jobs` table in SQLite is enough on one machine -- a row per job, a status column
  - Redis with a worker library earns its place once a second process needs the same queue
  - RabbitMQ and Celery are the serious version: many workers, many queues, routing a table can't express
  - Explain the order: SQLite, then Redis, then RabbitMQ and Celery, each earned only once the last stops being enough

### Monitors

- What a monitor is
  - A background command a plugin declares, running for the life of the session
  - Every line it prints to stdout reaches Claude as a notification -- the model hears it, not a person
  - Unlike the watchers earlier, a monitor runs inside a session -- it can't start an unattended run, only report
  - Experimental, and it inherits the session's lifetime -- nothing is watched once the session ends

- Declaring one in a plugin
  - Declared in `monitors/monitors.json` at the plugin root, or inline in `plugin.json` under `experimental.monitors`
  - Three fields are compulsory: `name`, `command` and `description`
    - `name` must be unique within the plugin, so a reload doesn't spawn a second copy
  - `when` decides the start: `always` (the default) fires at session start; `on-skill-invoke:<name>` waits for that skill
    - Explain the tradeoff: `always` costs every session, `on-skill-invoke` only the ones that reach that skill
  - `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` and `${CLAUDE_PROJECT_DIR}` expand inside `command`, letting it call a script shipped with the plugin

## Integrations

### APIs

- What an API is
  - An API is a contract to call, not a UI to click through -- `curl`, a browser and `WebFetch` are all just clients speaking to it
  - The portal you click through calls the same endpoints a script could call directly
  - Not every service publishes one -- Companies House does for company filings, most court listing pages don't

- curl and jq
  - `curl` fetches a URL with headers, a key and a POST body; `jq` cuts up the JSON that comes back -- the cheapest integration there is
  - Use cases: a morning check of a case-status endpoint reporting only what changed, the day's exchange rate dropped into a fee calculation, a Slack or Telegram post when a run finishes, filings pulled from Companies House, a court listing downloaded, accounting software asked what's unpaid
    - Run one `curl | jq` pipeline end to end and show the fetch next to the field pulled out of it

- The API shapes there are
  - Every shape splits on the same question: who speaks first
  - REST -- you ask, it answers, the connection closes; the vast majority of APIs
  - Webhooks -- the reverse: you hand the service an address, it calls you when something happens (Stripe on a payment, GitHub on a pull request)
  - WebSockets hold a line open both ways for a stream; server-sent events hold it open one way, them to you -- how Claude streams its own replies
  - GraphQL is still you-ask-they-answer, but you name exactly which fields in one request
  - The service picked the shape, not you -- `curl` and `jq` work against whichever one you're handed

- Polling and webhooks
  - A webhook needs a front door of your own the service can call -- something a case system offers, a court almost never does
  - Where there's no webhook, polling is the fallback: fetch on a timer, compare to yesterday's saved copy, act on the difference
  - Webhooks are a gift when offered; polling is what you build when they're not

- Scraping
  - Scraping is polling aimed at markup instead of JSON -- the same cron-and-compare loop, run against a page with no API behind it
  - The page was written for a person, not a machine: a hearing date sitting in a table cell with no id and nothing marking it as data
    - A page redesign that moves that cell is the example: the fetch still succeeds, but the extracted value comes back silently wrong
  - Where a login wall or heavy JavaScript stops `curl` working, that's where Chrome control takes over
  - Basic manners cost nothing: identify yourself in the `User-Agent`, and a fetch once or twice a day bothers no one

### MCPs

- What an MCP is
  - An MCP server advertises a list of tools; Claude calls them typed and described, like any built-in
  - Without one, reaching a service means Claude writing `curl` commands and guessing at what comes back
  - Use cases: a read-only case database, a document store, a Playwright browser, errors pulled out of Sentry
  - Same protocol and same tools as a connector -- what differs is the install: a server is added at the command line, a connector is ticked on at claude.ai

- Adding one
  - A remote server: `claude mcp add --transport http <name> <url>`
  - A local server: `claude mcp add <name> -- <command>`, where the bare `--` separates the server's arguments from Claude Code's
  - A published server usually exists already -- Sentry, Playwright and Postgres are shipped by their vendors -- so writing your own is rarely the first move
  - A `stdio` server runs as a subprocess with your own files and network access: adding one is a trust decision, not just a convenience

- The transports
  - `stdio` -- a subprocess on your own machine, the common case for a local database or file store
  - `http` -- a server somebody else runs, such as a document portal's own service
  - `sse` -- deprecated

- Scopes and where they live
  - Three scopes: `local` (this project only), `project` (the whole team, every clone), `user` (every project you open)
    - `local` and `user` both live in `~/.claude.json`; `project` lives in `.mcp.json` in the repo root, which is the one that travels with the code
      - A `.mcp.json` committed to a repo next to a `~/.claude.json` holding a `local` entry shows which file a given server actually lives in
  - Two traps worth naming: MCP servers are not in `.claude/settings.json` with everything else, and `~/.claude/mcp.json` is never read, however plausible the path looks
  - `project` scope suits a server the whole team should get on every clone; `local` suits one only this checkout should keep

- Authentication
  - Three ways, in ascending order of what survives running unattended
    - A static `headers.Authorization` value never refreshes -- rotate it by hand
    - OAuth refreshes its own token and retries once on a 401, which covers most overnight running
    - `headersHelper` runs a command that prints fresh headers on every connection, with no caching -- how Kerberos and internal SSO get reached
      - It gets ten seconds and executes arbitrary shell, so it only belongs in a trusted folder

- Tool search and output limits
  - Tool search is on by default: a dozen servers cost almost nothing at startup, since only names and instructions load until a tool is actually called
  - `ENABLE_TOOL_SEARCH=false` reverts to loading every schema upfront
  - `MAX_MCP_OUTPUT_TOKENS` caps what a single call may return -- 25,000 tokens by default, with a warning at 10,000
    - A call that returns two hundred filings is worth showing -- it clears the warning long before it hits the cap

- Timeouts
  - Four separate clocks govern an MCP call -- a job hung at midnight is usually one of them running out
    - `MCP_TIMEOUT` for startup, 30 seconds by default
    - The per-server `timeout`, in milliseconds, bounding the whole call
    - A 60-second per-request timer on HTTP servers, on top of that
    - Idle timeout: five minutes remote, thirty minutes local
  - Matching a failure to its clock is the diagnostic step: a startup hang is `MCP_TIMEOUT`, a stalled call is the per-server timeout or the HTTP timer, silence after replies is the idle timeout

- MCPs in unattended sessions
  - A project-scoped server in `.mcp.json` normally prompts for approval before it loads
  - Under `claude -p`, in an SDK session, or in a cloud session there's nobody to answer that prompt -- it loads unasked
    - Show a server committed to a matters repo loading itself into a 06:00 intake run with nobody there to say no
  - The security consequence: anyone who can commit a `.mcp.json` to the repo can get a server run unattended
  - `disabledMcpjsonServers` keeps a specific one out; `--setting-sources` cuts project settings off entirely
  - Managed MCP is the enterprise counterpart -- a `managed-mcp.json` in a system directory that fixes what may load regardless of what a project asks for

- Driving a browser headlessly
  - The Playwright MCP server drives a browser headlessly -- it renders into memory, so no display is needed and the box can be a rented Linux one
  - Nothing about the run is visible, so a login page or a CAPTCHA becomes a silent hang, not a prompt anyone can answer
  - A page plain enough to run unwatched has a stable form and no login -- a court portal behind a sign-in isn't one of them, and belongs to Chrome control instead

- When an MCP breaks
  - A JSON entry with a `url` and no `type` is skipped outright -- the single most common malformed config
    - A document-store server with no tools on the menu the morning after an edit dropped the `type` field, and the fix -- naming it explicitly as `"type": "http"` or `"type": "stdio"` -- makes a good pair to show
  - `claude mcp list` and `/mcp` inside a session are how you find out what actually loaded
  - A server that failed to start and one that was never configured both look like nothing on the menu -- the failure is silent either way
  - An empty tool list can just as easily mean tool search deferred the schemas -- it proves nothing about the server on its own

### Browser and Screen Control

- What Chrome control is
  - Chrome control is an extension driving a browser window you can see -- the same actions a person would take
  - It exists for the site with no API and no way in through the terminal: a login-gated portal, a page that only renders after its JavaScript runs
  - Computer use, by contrast, drives the whole desktop screenshot by screenshot, not just the browser

- The browser's own login
  - It shares the browser's own login state -- the whole reason to prefer it over `curl` for a signed-in site
  - Whatever the browser is already signed into, Claude reaches with no credential of its own: no API key, no service account
    - A solicitor's Chrome already signed into a county court's e-filing portal is the example -- Claude reaching that same session rather than logging in fresh

- The portal with no API
  - The use case: a portal behind a login with no API -- most court and government systems
  - It reaches a page that renders nothing until its JavaScript runs, and fills a form field by field before submitting
  - A filing confirmation that exists only on screen has no API to hand it back through -- a screenshot is the record
  - It runs in a visible window in real time, watchable rather than headless, and hands control back at a login page or a CAPTCHA
  - Permission split: reading, searching and screenshots pass without a prompt in plan mode; clicking, typing and navigating ask first

- Computer use
  - What it's for: native applications with no other way in -- a desktop e-filing client, a case-management program with no browser and no API -- reached only after an MCP server, Bash and Chrome have all failed
  - The constraints stack up
    - macOS and Windows only, Pro or Max only
    - Approval scoped per application, per session
    - Only one session machine-wide may hold control at a time
    - Unavailable under `-p` -- no unattended run reaches it
  - Escape aborts a run in progress, and the terminal is hidden from its own screenshots

- Reach for these last
  - The ladder: MCP server, then Bash, then Chrome, then computer use -- each rung tried only once the one before has failed
  - An API is faster and cheaper, and doesn't break when a button moves
  - Screen control is the last resort, for when nothing behind the screen can be reached any other way

### Connectors

- What a connector is
  - A connector is an MCP server somebody else runs, ticked on at `claude.ai/customize/connectors` instead of added at the command line
  - Same protocol and same tools as a server you configure yourself -- what differs is a shorter install and no config file touched
  - Because it's remote it's HTTP, and because Anthropic handles the authorisation it reaches services that refuse a local OAuth round trip -- Gmail, Google Calendar, Microsoft 365, Slack
  - Use cases: the calendar connector answers when a hearing is listed, Gmail pulls a client's thread into the session, a shared Drive folder's contents are readable, an overnight run's outcome posts to Slack

- Turning one on
  - The tick is made at `claude.ai/customize/connectors` -- nothing installs, no config file changes
  - It's made once per account, not once per repo -- every session that account opens sees it

- The subscription condition
  - Connectors load only when the session is signed in with a claude.ai subscription
  - Any of these kill them silently, with no warning and no error -- just an empty list: `ANTHROPIC_API_KEY`, an `apiKeyHelper`, a `claude setup-token` token, or running through Bedrock, Vertex or Foundry
  - They also ride the claude.ai session token itself -- when that lapses, the connector reports itself rejected
  - Re-authorising the connector doesn't mend a lapsed login -- a person has to renew it, which an unattended job can't do

- Precedence
  - A server you configure yourself wins over a connector reaching the same endpoint, without having to untick the connector first
  - The match is made on endpoint URL, not on name -- renaming your own server changes nothing

### Channels

- What a channel is
  - State that a channel is an MCP server pushing events in from outside
    - Contrast it with connectors, MCPs and Chrome, which have Claude call out instead
  - Show an event arriving from outside and acting on a session with nobody at the terminal -- a case-management webhook flipping a status, a phone message redirecting a run already underway, or an approval granted from a train

- The channels there are
  - Ships as plugins: Telegram, Discord, iMessage, a webhook receiver, a browser demo for testing
  - Custom channels use the ordinary MCP SDK -- no waiting on a shipped plugin
    - The webhook receiver already covers it: point a case system's webhook at the local port
  - Needs an Anthropic login, not Bedrock, Vertex or Foundry; blocked by default on Team and Enterprise until an owner enables it
  - Slack is a separate integration, not a channel -- it opens its own new cloud session rather than pushing into the local one already running

- Switching one on
  - Installed as a plugin, with a token landing in `~/.claude/channels/<name>/.env`
  - Switched on per session by naming it on the command line: `claude --channels plugin:telegram@claude-plugins-official`
    - Not by editing a config file -- listed in `.mcp.json` alone does nothing
  - Events arrive only while a local session is open, not the web, desktop app, or Remote Control
    - Staying always-on means a session parked in tmux, or a `claude -p` worker left running
    - A paralegal wanting a Telegram alert on every filed matter has to leave that session running all day, not just open it when checking -- worth spelling out

- Two-way and the permission relay
  - Two-way needs the channel to offer a reply tool -- not every channel does
  - The permission relay puts the same approval prompt in the terminal and on the phone -- first answer wins
    - Approving from a phone leaving a hearing beats a terminal sitting untouched back at the office

- Gating the sender
  - Gate on the sender's own ID -- the room it arrives in is not a safe boundary
    - Gating on the room instead lets anyone who can reach it put text in front of Claude
  - Same rule for the webhook receiver: gate on which system sent the POST, not the port
  - An ungated channel is a prompt-injection hole with an address

### Deep Links

- What a deep link is
  - A deep link opens a new terminal window with the prompt already filled -- scheme `claude-cli://open`
    - Three parameters: `q` the prompt text, `cwd` an absolute working directory, `repo` a GitHub slug resolved against known clones
  - Give a few examples of what a deep link is for: an alert that opens a session on whatever broke, a runbook written as one-click links instead of paragraphs to copy, a dashboard row that becomes an investigation in one click
  - It never runs on its own -- the prompt lands in the box, a person presses Enter
    - A warning it came from an external link stays up until they do -- the hand-off is the design

- Firing one
  - Fired from anywhere the OS can open a URL -- `open`, `xdg-open`, `start` -- any script can make one
    - A monitor watching the intake queue that prints a deep link into its own notification, landing a session on the stuck matter in one click, is worth a picture
  - The handler registers on first use in an interactive session; `disableDeepLinkRegistration` turns that off
  - Scheme-stripping sites like GitHub Markdown show it as plain text -- keep it copyable in a code block

### Credentials

- Where keys should live
  - A dozen services means a dozen credentials, and each one sitting in the open is a liability
    - Two examples earn their place here: an unattended 3am job needing a key with no one to type a password, and rotating one shared database password instead of editing six scripts
  - The rule: fetch a key at the moment of use, not store it everywhere it might be needed
    - Also keeps a key out of a repo later shared with a client or a new hire

- The keychain, direnv and password managers
  - Order the options by one axis: how many things need the same secret
    - One machine, one key: the OS keychain -- Keychain on macOS, Secret Service or `pass` on Linux
    - One project: a `.env` file with `direnv`, kept out of version control
    - Many consumers, one secret: HashiCorp Vault or a cloud provider's secret manager
  - If a password manager is already in use, its CLI reaches the same vault -- Bitwarden or 1Password, nothing new to run
  - A script asks the keychain by name and keeps no copy of the answer
    - Picture a firm keeping three keys -- Telegram, a case-management API, an email provider -- in one keychain rather than three scattered `.env` files

- Keys and the transcript
  - Three ways a secret reaches the transcript: pasted, a `.env` loaded into context, or typed on a command line
  - The transcript is a JSONL file that outlives the terminal -- a secret in it doesn't vanish
  - The fix is timing, not carefulness -- fetch the key at the point of use
    - A script can fetch the key itself and call the API, so Claude sees the result, never the credential

- apiKeyHelper and sandbox credentials
  - Grade any credential mechanism by whether it survives unattended, with nobody there to renew it
    - A pasted or hardcoded key needs a person to rotate it; something that fetches itself doesn't
    - MCP's own ladder makes the same point and is worth pointing back to: a static header needs rotating by hand, OAuth refreshes itself, `headersHelper` produces fresh headers on every connection
  - `apiKeyHelper` is Claude Code's version: produces the key at connection time, never written to a settings file
  - `sandbox.credentials` denies or masks credentials from a sandboxed process -- it runs without ever holding the value
  - Both keep the key out of what could leak it: a settings file, a process environment

## Databases

### Why Database Anything

- What a database is
  - A folder answers "what files are here"; a database answers a question about the data itself
    - Show "which matters have an unbilled hearing in the next fourteen days" asked of a folder listing that can't answer it, then asked of the database
  - A database stores claims, not facts -- recording a deadline doesn't make it correct
  - Other shapes beyond rows-and-columns exist for other needs, covered later in this part

- Why put your own files in one
  - The archive doesn't move -- a database adds a row per document, not a copy of it
    - The row records what the document is, which matter it belongs to, and its path on disk
  - Once the rows exist, a query answers instantly what would otherwise mean opening every folder
    - Give the query "every noncompete sent to a New Jersey client since 2023" and show it answered instantly, against what opening every folder would take
  - An unindexed document is invisible to every query, and nothing says so -- no error, just absence

- SQLite first
  - SQLite first, moving to Postgres only once a second machine needs the same data
    - One file, no server, ships inside Python already
    - `sqlite3 matters.db` creates it; deleting the file removes it
    - Reaching for Postgres before that point means a server running for no benefit yet
  - Name the questions the database has to answer -- Claude designs the tables from them, not the other way round

### Relational

- Relational databases
  - Rows carry named columns and can link to rows in another table
    - That link is what a folder can't hold
    - A diagram of one `matters` row branching to one `clients` row and many `documents` rows, showing a query traverse the link from matters through both
  - Matters, clients and invoices are already record-shaped, so relational is usually the shape already at hand
  - Changing a link's shape later means migrating every row that used it, not just adding a column

- PostgreSQL
  - Postgres is the serious open-source server -- the step up once a single file and no server aren't enough
  - It earns its place once a second machine, person or automation needs the same data at once
  - A server process differs from a file -- something has to start it, keep it running, grant access to it
  - It handles JSON, full-text search and vectors natively, covering three of the other types this part goes on to name
  - A stopped Postgres instance isn't a slower file -- it's no database at all until restarted

- DuckDB and the others
  - None of these are chosen from scratch -- an existing system already uses one
    - MySQL and its fork MariaDB are older and hugely deployed, mostly behind existing websites
    - SQL Server and Oracle are commercial and licensed -- inherited from a case-management system, not installed by choice
  - DuckDB has SQLite's shape -- one file, no server -- but is columnar, built for questions across many rows
    - It queries CSV and Parquet files directly where they already sit on disk, with no import step first
    - Show a folder of monthly billing CSVs queried directly for "total billed per client this quarter", with nothing loaded into anything first

### The Other Kinds

- Document databases
  - Document databases hold JSON blobs of varying shape -- no fixed columns, so records can differ
    - The use case is scraped or API data whose shape isn't settled yet
      - Walk through a scraped court listing where one hearing's record has a room number and the next doesn't
      - Show a typo in a key silently becoming a new field that nothing queries, with no error raised
  - A `jsonb` column in Postgres, or a JSON column in SQLite, covers this without installing a dedicated document database
  - Standalone options earn a mention only once a `jsonb` column or JSON column isn't enough -- MongoDB, CouchDB, Firestore, DynamoDB

- Key-value stores
  - A key-value store holds one value per key and nothing else -- no columns, no relations, just a fast lookup
    - The shape is a notepad that survives between runs
      - Show an archiver asking, key by message ID, "seen this?" before reprocessing it every ten minutes, and skipping the message it already has a key for
    - The same shape covers a cached API answer not worth paying for twice
    - It also covers a "job already running" flag, or a count of how many times something happened today
  - Nothing expires on its own unless the code that set a key also sets its expiry
  - The path is a two-column SQLite table on one machine, installing nothing
    - A dedicated store earns its place only when several processes need to share the same notepad at once
  - Name the rest only as needed -- Redis, Valkey, Memcached, LMDB, RocksDB, etcd and Consul

- Columnar databases
  - A columnar database reads only the columns a query asks for, instead of fetching every row whole
    - A diagram of that difference -- row-wise touching every cell in a row versus column-wise touching only the three columns a query needs
    - Give the two queries "total billed per client per month for three years" and "which of 400,000 log lines are errors, grouped by hour", and show them running roughly a hundred times faster columnar than relational
  - It's bad at the opposite question -- fetching one matter's whole record, which is what most days actually require
  - It earns its place once reporting across the whole archive starts being asked for, not before
  - DuckDB is the one that matters for a single practice; ClickHouse and hosted warehouses are for scale beyond that

- Graph databases
  - A graph database stores connections as the primary thing, not the records themselves
    - It answers "everyone connected to this person within four steps" directly, where a relational join chain makes that painful
  - The use cases are specific: corporate ownership chains, conflict-of-interest checks across a client base, family relationships in an immigration matter
  - Most practices don't need one -- SQLite's recursive queries reach as far as most client bases ever require
  - Neo4j, Kuzu and Memgraph are worth naming only once that headroom is actually needed

- Time-series databases
  - A time-series database stores the same measurement taken repeatedly and stamped with when, built to throw away old detail and keep summaries
  - The use case is tracking what an automation costs per day, how long each run took, or rates over months
  - A SQLite table with a timestamp column covers most of this; a dedicated database is rarely needed

### Search

- Full-text search
  - `grep` matches only what was typed, scanning every file every time
    - Nothing prebuilt, so nothing is wrong, but nothing is fast either
  - A full-text index is built once and answers instantly, ranked best-match-first instead of file order
    - Stemming catches "filed", "filing" and "files" as the same word without asking for each separately
    - Show a search across an archive returning ranked results, best match first, against the same search run with `grep`
  - SQLite FTS5 needs nothing installed; Postgres `tsvector` does the same job for an archive already in Postgres
    - A standalone engine like Tantivy, Meilisearch or Elasticsearch earns its place only once both are outgrown
  - An index built on Monday doesn't know about Tuesday's filings
    - It goes stale silently -- a confident empty result, not an error

- Vector search
  - Full-text finds "termination" as a word; vector search finds the clause even when it never says that word
    - Each document becomes a list of numbers from an embedding model, and similar meanings land near each other
    - A diagram of documents as points in space, showing the liability clause and the termination clause sitting near each other despite sharing no words
    - Show a contract archive search that finds the clause capping liability, or the passage on early termination, without matching the search word itself
  - `sqlite-vec` adds it to SQLite as an extension, `pgvector` does the same for Postgres
    - Chroma, Qdrant and LanceDB are standalone, for an archive that outgrows an extension bolted onto an existing database
  - Changing the embedding model breaks every vector already stored
    - The whole archive has to be re-embedded, not just the new documents

- Retrieval in practice
  - No model can be handed the whole archive at once
    - Retrieval finds the handful of relevant passages and hands only those to the model
  - Full-text and vector search answer different questions
    - "every letter using the word 'forfeiture'" against "the clause about ending it early"
    - A working setup usually runs both, not one or the other
  - An answer built on the wrong six passages reads exactly as confident as one built on the right six
    - Nothing in the reply signals that retrieval picked badly

### With the Harness

- Getting your material in
  - Material arrives as scanner PDFs, DOCX from clients, email attachments and case-management exports -- not one clean format
  - Getting it in is three steps: extract the text, classify what it is, and record where it lives
    - extract: `pdftotext` tests whether OCR is needed -- a blank result means running tesseract first
      - Walk through a three-format ingest run -- a clean PDF, a DOCX and a scan with no text layer -- ending with all three searchable
    - classify: sort what comes out into engagement letter, pleading, invoice and the rest
    - record: the row holds what the document is, which matter it belongs to, and its path
      - The original file never moves
  - An import that OCR'd a blank page writes a row with empty text and no error
    - The fix is counting rows against files afterward to catch the gap

- Asking questions of your own data
  - The question is asked in plain language; Claude writes the SQL that answers it
    - For instance: "which matters have no engagement letter on file", "every letter mentioning an appeal deadline last quarter", "what did I bill Ramirez between March and June"
  - The pieces already covered work together on one question
    - FTS5 finds the word, sqlite-vec finds the clause phrased differently, the `matters` table says whose record it belongs to
  - A query that joins the wrong way returns a number that looks exactly as authoritative as a right one
    - The check is running it against a matter whose answer is already known, and comparing

## Automatic Outputs

### Document Automation

- Document pipelines
  - Document pipelines are chained shell commands, not libraries you import
    - Together they turn what comes in into something Claude can read, and what Claude writes into something a person can open
      - Which command depends on what arrived: `pdftotext` for text, `tesseract` for a scan, `pandoc` for a format swap, LibreOffice for an Office file
  - A scanned bundle and a filed PDF look the same in Preview -- only one of them has a text layer

- poppler and pdftotext
  - poppler is a command-line PDF toolkit -- `pdftotext` is the piece of it that turns a PDF into plain text
    - poppler's other tools split a bundle apart, glue pages back into one file, or turn a page into an image
  - Run `pdftotext scan.pdf -`: nothing back tells you the PDF is pictures, not words, and hands the job to tesseract
  - It's the first thing worth trying on anything that arrives -- costs nothing, and tells you which kind of PDF you've got
    - The example that shows this: `pdftotext` against a text PDF returning the whole document in under a second, the same command against a scan returning nothing

- tesseract and OCR
  - tesseract reads the pixels of a scan and produces text, the way a person reading it would
    - It only helps once `pdftotext` comes back empty -- on a PDF with a text layer already, it just replaces good text with a worse guess
  - Used on scanned exhibits, faxed correspondence, and old filings that exist only as images
    - Show a poor scan that produces confident wrong text -- a misread digit in a deadline date, nothing in the output flagging the error

- pandoc
  - pandoc converts between text formats in one command -- Markdown to DOCX, DOCX to Markdown, HTML to PDF
  - Each direction loses something different: Markdown to DOCX drops styling, DOCX to Markdown drops tracked changes and comments
    - One example worth giving: a redlined engagement letter from opposing counsel converted to Markdown and back, with the redlines gone
  - A plain first draft can make that round trip fine -- one already marked up with revisions has to stay in DOCX

- LibreOffice headless
  - LibreOffice headless puts Word and Excel behind a script -- no window, no person clicking File > Export
    - `soffice --headless --convert-to pdf letter.docx` is the whole command, and it keeps the letterhead pandoc would strip
      - A side-by-side image would do the work here -- the same DOCX letter converted to PDF with LibreOffice headless and with pandoc, showing what pandoc's version lost
  - It reads XLSX too -- a billing spreadsheet in, a table Claude can read out
  - Missing fonts on the conversion machine get substituted silently, so the server's version can look different from yours

### Templates

- Templating
  - A template is boilerplate written once with holes in it, and every use just fills the holes from data
    - The model doesn't draft the boilerplate, it only supplies the values that go in the holes
  - Only the holes move; the fixed parts of the document -- the boilerplate, the terms, the closing language -- never do
    - Walk through an engagement letter with `{{client_name}}` and `{{matter_type}}` holes, filled from a row of client intake data
  - Draft it fresh each time and approved wording drifts a little more every run -- a template is what stops that

- Jinja and docxtpl
  - Jinja is the templating engine behind the `{{ }}` holes, the general Python tool underneath
  - docxtpl edits a DOCX where it stands, leaving letterhead, styles and numbering alone
  - That output is a real, editable Word document, not a picture of one -- someone can still mark it up once Claude's done

- Filling a form PDF
  - A form PDF -- an immigration Form N-400, say -- already has named fields sitting in it before anyone fills anything in
    - Filling means writing values into fields that already exist, by name, using `pdftk` or `pypdf` -- there's no page to build
      - Give an example of an N-400's fields written from a client's intake record, one row per applicant, the same script run down a list rather than typed by hand
    - Flattening locks the filled values into the page as fixed content -- nothing left to edit or tab through
  - Draw the distinction between filling and templating -- reaching for docxtpl on a form that already has fields is wasted work
  - With no fields to start from, template the PDF instead -- DOCX or Typst, converted at the end

- Typst and LaTeX
  - Typst and LaTeX take source text and control layout the way a word processor doesn't -- the two typesetting engines
  - They earn their place when layout has to be exact: page breaks, running headers, automatic renumbering, a bundle index, an exhibit list
  - A two-page engagement letter doesn't need either one -- that's still docxtpl's job

### Artifacts

- What an artifact is
  - An artifact is a self-contained web page that a session in Claude Code puts up at a private claude.ai URL -- the cheapest way for work to leave the terminal
    - One HTML file, styles and script inline -- nothing to host, nothing to keep running
  - A screenshot earns its place here: a published artifact -- a status page, an overnight run's summary, a monthly chart -- with its private URL, showing what actually lands in the reader's browser
  - It needs a paid plan with a `/login` session on the Anthropic API -- Bedrock, Vertex and Foundry don't support it
    - `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` keeps a headless run from trying to open a browser that isn't there

- Publishing and revising
  - Publishing prompts once per artifact -- after that, editing the file and publishing again revises the same URL
    - Someone with the page already open watches it update in front of them
  - Each publish keeps its own version, so an earlier state of the page is always still there
  - Skip passing the existing URL to a later session and you get a second, separate artifact, not an update to the first
  - An artifact starts private to whoever created it, on every plan
    - Pro and Max share it by sending the link to anyone
    - Team and Enterprise keep it inside the organisation by default -- an owner has to flip a setting before a public link works

- Connectors inside an artifact
  - The connectors inside a published page are the same MCP connectors covered under Integrations -- they just run inside the page now, on load
  - It fetches fresh data on every open using the viewer's own connectors, so the automation that built it never has to run again
    - Picture the same status page URL opened by two viewers with different connectors -- a client with none sees an empty page where the firm sees live data

- The content policy
  - The content policy blocks everything from outside the page -- external scripts, stylesheets, fonts, images, and all outbound fetch, XHR and WebSocket traffic
  - Everything the page needs has to be inlined into that one HTML file, or it doesn't render
  - Sixteen megabytes is the ceiling on that file
  - Self-contained and bounded in size is what makes something an artifact instead of an ordinary web page

### Static Sites

- Static site generators
  - A generator compiles a folder of Markdown into plain HTML -- nothing to run, nothing to keep alive once it's built
    - The output is nothing but files, so it runs anywhere: a laptop folder, a bucket, any static host
  - Hugo, Zola, Eleventy and MkDocs are the generators worth naming
    - A worked example belongs here: `mkdocs build` run over a folder of notes, producing a searchable internal reference with a search box and no server behind it
  - The same repo that holds the Markdown can serve the built site too, for free, through GitHub Pages
    - Nothing stops anyone with the URL from reading it -- GitHub Pages defaults to public

- Publishing what an automation makes
  - An automation publishing this way is about as cheap as it gets
    - A status page rebuilt nightly, an internal reference from your own notes, a published version of something like tutor
  - A static page only shows what the last build put there -- generated ahead of time, not served fresh on request
    - Trace a nightly `claude -p` run rewriting a status file, the generator rebuilding the site, and the client opening the same URL to this morning's position -- no new link to send
  - A matter status page with client names doesn't belong on public GitHub Pages -- Tailscale or an artifact instead

## Hosting and Serving

### Web Servers

- What a web server is
  - A web server listens on a port and answers whatever request arrives
    - Same listener, different reply depending on who's asking -- a page for a person, JSON for a program
  - It's the front door for an automation: a form filled in, or a URL another service calls
  - Open only while the process runs
    - Start the server and hit it, see the reply -- then stop it and hit it again, and show the failure

- Reverse proxies
  - A reverse proxy sits in front of the real server
    - Takes over the HTTPS certificate, renewed once instead of inside every app behind it
    - Several services can sit behind one address, routed to different backends
    - Refuses traffic that wasn't invited, before the app behind it ever sees the connection
  - The cost of the extra hop: a browser error only says the site's unreachable, not which layer is down

- Caddy, nginx and certificates
  - It's what turns the address into a real `https://` instead of one the browser warns about
  - Caddy gets a certificate automatically -- a couple of lines in a Caddyfile, issued and renewed on its own
  - nginx is the standard, and leaves certificates to you, via `certbot`
  - A certificate belongs to a name, not a machine -- move the box, nothing breaks; change the name, it does

- Tunnels
  - Tailscale and a tunnel are two different ways to avoid opening the machine to the internet directly
  - A tunnel gives the machine a reachable name -- the browser connects straight to it, no hosting layer between
    - It changes how the machine is reached, not what's listening on it -- same server, same Caddy in front

- Self-hosting
  - Self-hosting means the files land on your own disk, no third party holding a copy
    - The client's browser connects straight to your machine
  - A domain costs about ten pounds a year
    - Points at your own machine as easily as at a host's -- a name is memorable, a number isn't, and home addresses change
  - The one condition: the machine has to stay awake
  - What paid hosting sells beyond that: someone else's electricity, a connection that doesn't drop, blame elsewhere when it breaks
    - Skippable for a form only you depend on

- A worked example — the intake form
  - A worked example ties the section together: an intake form (name, matter type, a passport-scan upload) served from your own machine and fronted by Caddy with a real address; submitting writes to a case folder, a database row and a queue at once; cron picks the job up and `claude -p` with the intake skill drafts the engagement letter, matter filed before anyone opens the laptop
  - A form that accepts uploads accepts them from strangers
    - Cap the size, check the type, never hand what arrives straight to a shell

### Containers

- What a container is
  - A container is a sealed box holding a program and everything it needs
    - Its own filesystem, its own packages, its own version of Python
    - Build one running something like Postgres, show its version and files differ from the host's, run it unchanged on a second machine, then delete it and show nothing is left behind
  - It runs identically anywhere -- laptop, rented box, a reader's machine -- and touches nothing outside itself
  - Containers share the host's kernel instead of booting their own -- fast to start, and Linux-only rather than a virtual machine
    - Running against a clean machine catches "works here because I have it" bugs a laptop full of installed tools hides
  - Building and running are different acts: a container can cross-compile a Windows binary without being able to open it
  - For Claude Code it's also containment -- an agent working inside one can't damage the machine around it
  - Docker is the tool; a devcontainer is the same idea wired into an editor

- Images and registries
  - An image travels through a registry -- Docker Hub, or a cloud's own -- pushed from here, pulled there
  - Getting it onto a rented box is three steps: install Docker, pull the image, run it
    - Nothing else to install -- the dependencies travel inside the image
  - The image you tested is the thing that runs -- rebuilding on the box produces a different image
  - Architecture matters -- laptop and box can run different chips, so build for the target, or build on the box
  - Services like Cloud Run skip the machine entirely: hand over an image and it runs it

- Reproducibility
  - A container is a written-down recipe of every dependency -- what worked in March still works in December, on a machine not yet built
  - Reproducibility alone accounts for most container use -- containment is a bonus on top
  - Deployment gets easier: move the box to a rented server instead of reinstalling forty things
  - Nothing installed collides with anything else, and nothing survives being deleted -- incompatible versions sit side by side, trying new software costs one command
  - Twenty identical boxes can run the same job in parallel, each on its own batch of matters overnight

- Running one on a box that never sleeps
  - A laptop closed or asleep can't run an unattended job overnight -- a box that never sleeps can
  - It runs what can't wait for the lid to open
    - A scheduled cron job, or a server backing something like the intake form

## Agent SDK

### The SDK Harness

- What the Agent SDK is
  - The same agent loop that runs Claude Code, packaged as a library for Python or TypeScript
  - No terminal: your program decides when a turn starts, not someone pressing Enter
  - Your program sees every message and can refuse a tool call in code instead of at a prompt
    - Walk through a callback denying a write outside a client's own matter folder, so the reader sees the call stopped in code before it ever reaches a prompt
  - Same tools and the same `.claude` machinery run underneath -- what changes is who's driving, not what's driving it
  - It removes the terminal, not the engineering: sessions, permissions and cost are still your job, just written in code

- How it differs from headless sessions
  - Ask first whether the SDK is needed at all -- `claude -p --output-format json` already runs Claude non-interactively, from any language, in one line
  - A headless session is that one line: one shot at a final answer, nothing seen in between
  - The SDK earns its place on mid-run intervention
    - Conditional tool approval, streaming partial output, a session held open across exchanges, per-turn billing
    - Give one example of each side of that line -- a nightly OCR job that only needs `claude -p` and exits, next to a paralegal's intake tool that needs the SDK to stream status to a browser -- so the reader can place their own job on it

- Use cases
  - The intake form's back end: submits documents, watches the answer arrive as messages rather than blocking on one call
  - A service running one agent per customer, each customer's files walled off from every other's
  - Anything with someone waiting on a connection, where a headless run's blank screen won't do

### Building an SDK

- Running a query and holding a session
  - Two entry points in either language: one for a single question, one for a session held open across exchanges
  - `query()` answers one question and ends, returning a stream of messages for that run
    - Give an example of a `query()` call in use -- whether a bundle has a text layer, say -- so the reader sees one question go in and a stream of messages come back with nothing held open after
  - Python's `ClaudeSDKClient` and TypeScript's streaming input keep a session alive for repeated exchanges -- a paralegal's back-and-forth on one matter
  - Only the session-holding entry point can be interrupted mid-thought; `query()` can't

- The messages that come back
  - What comes back is a sequence of typed messages, not one string reply
    - `SystemMessage` (subtype `init`) first, carrying the session ID
    - `AssistantMessage` per reply, `UserMessage` per tool result
    - `ResultMessage` last, holding cost, tokens and the session ID
  - A turn is one trip through assistant-then-tools -- a reply followed by the tool calls it made
  - That sequence is what makes live status, per-turn billing and a full log of what happened all possible
    - Walk through reading a `ResultMessage` after a turn and checking its cost against a per-matter budget cap, so the reader sees where in the stream that number actually lands

- Stopping it running forever
  - Two limits exist and neither is a clock: `max_turns` and `max_budget_usd`
    - `max_turns` counts tool-using turns only
    - `max_budget_usd` stops on a client-side cost estimate, not a metered bill
  - A session has no timeout and won't end on its own -- an unattended program needs something watching from outside it
    - Show `timeout 3600` wrapped around an overnight intake run, or the equivalent systemd unit, so the reader sees the limit sitting outside the SDK rather than inside it

- The permission callback
  - `can_use_tool` is the permission callback -- it decides whether a specific tool call proceeds, in code instead of at a prompt
  - It only fires when a prompt would otherwise have fired -- an allow rule never reaches it at all
    - Worth flagging: that's not the full security boundary it looks like
  - Six permission modes exist and the callback sits beneath all of them, seeing only what the mode leaves unresolved
  - A deny rule outranks everything, including `bypassPermissions` -- which itself refuses to run as root
    - Walk through a deny rule blocking a write outside `matters/<client>/`, then show it still holding once `bypassPermissions` is turned on, so the reader watches the rule win rather than just reads that it does

- One process, many customers
  - By default an SDK session loads the same `.claude` machinery Level Two built -- settings, CLAUDE.md, hooks, skills, subagents
  - `setting_sources: []` shuts all of that out, which is what running one process for several customers requires
  - Each customer also needs its own working directory (its own matter folder) and its own `CLAUDE_CONFIG_DIR`
    - Without that separation, one client's CLAUDE.md, skills or files reach another client's run
  - Run two customers' sessions side by side -- one pair sharing a working directory and `CLAUDE_CONFIG_DIR`, one pair with its own -- so the reader watches the leak happen before seeing what stops it

- Sessions and where they live
  - Sessions persist as JSONL files under `~/.claude/projects/`, resumable by ID
    - Give an example of resuming a session by ID -- picking up the Ramirez matter's thread a week later exactly where it left off -- so the reader sees the whole prior exchange come back, not just a note that it happened
  - A session can be forked into a new branch, leaving the original untouched -- draft a second letter without losing the first
  - A `SessionStore` adapter mirrors sessions to S3, Redis or Postgres instead of the local JSONL file
  - That mirroring matters the moment the program runs somewhere that gets rebuilt -- a container redeploy wipes `~/.claude/projects/` with it

- What it consumes
  - Every `query()` spawns the `claude` binary as its own subprocess -- twenty concurrent sessions are twenty processes, not twenty threads
  - Reckon on a gigabyte of memory, five gigabytes of disk and a CPU core per process as the floor
  - `total_cost_usd` is an estimate from a price table compiled into the build, not a metered figure from Anthropic
  - Good enough for a budget cap; not accurate enough to invoice a customer from

### Deploying and Integrating SDKs

- The shapes a deployment takes
  - A terminal program, a web page, a desktop application, a phone -- four faces, the same SDK code behind each
  - The choice between them is about who's on the other side and what they already have open, not about the SDK
    - Give the paralegal's intake tool as the example -- she sees a form and a drafted letter, never a mention of Claude -- so the reader sees the SDK doing the choosing rather than showing up as a feature
  - The face worth building is the one already within reach -- a finished Python TUI beats a React app that never ships

- Behind a TUI
  - `ClaudeSDKClient` in a loop with `input()` and `print()` is already a deployment
  - No server, no certificate, no hosting bill -- it runs where the matter folders already are
  - It reaches exactly one person on one machine, and stops dead at the colleague who won't open a terminal

- Behind a web page
  - A small FastAPI or Express server holds the SDK; the browser holds the form
    - The same intake page from Web Servers, with the SDK behind it instead of a queue
  - Anyone who can reach the URL can use it -- the whole gain and the whole problem
  - No authentication arrives with a browser -- add a login, a shared secret, or a Tailscale-only address
  - Files uploaded through it land on your disk, under your own permissions, with the SDK running directly against them

- Inside a desktop app
  - Electron or Tauri wraps the same web page behind an icon -- a program to the user, not a website
  - Code signing on macOS, an updater, and every colleague's machine sitting at a different version all become your job
  - The window hides where the work actually happens -- the model call still leaves the machine, and a client's documents go with it

- On a phone
  - The agent runs on the box; the phone holds only a page or a chat window
    - Nothing but a browser and a connection needed -- no install, no key
  - The cheapest version is the web page above, opened on a phone; a Telegram channel is cheaper still
  - Approving a redaction from a train is the case that justifies building this face at all
  - A dropped connection must not lose the run
    - The session lives on the box, resumable by ID; the phone just reconnects to it

- Where the process actually runs
  - Pick your own machine, a rented box, or a container on something like Cloud Run
  - A laptop that sleeps is not a host -- an intake form nobody can submit at 11pm doesn't work
  - Working when you tested it standing over it is not evidence it works at 3am from a client's phone

- Streaming to someone waiting
  - The message stream from Building an SDK is what goes on the screen
    - An `AssistantMessage` per reply, a `UserMessage` per tool result, as they arrive
  - A blank screen for ninety seconds reads as broken -- the client reloads and submits the form twice
  - What holds the wait is the tool names as they run
    - Give a couple of status lines built off real tool names -- "Reading the passport scan", "checking the matter number" -- so the reader sees the wording comes from the call, not from its result
  - A long step produces no message of its own -- OCR on a forty-page bundle is one tool call
    - Print something before it starts
  - Walk the screen through those ninety seconds start to finish -- status lines appearing as calls land, the flat stretch while OCR runs, then the printed line that covers it -- so the reader watches the wait rather than reads a description of it

- Keeping it up
  - Survive the operational basics: the box rebooting, the API key rotating
    - Also the model version changing underneath you unannounced -- the SDK always calls the latest
  - Someone else using it raises two needs: a log of what happened
    - And a way to say what broke to a person, not a stack trace nobody reads
    - Show the same failure two ways -- a raw traceback in a terminal nobody but you reads, next to a one-line message a paralegal would actually understand -- so the reader sees why the second one is the job
  - Resuming a customer's thread next week means the session outliving the machine -- a `SessionStore` to Postgres or S3, not `~/.claude/projects/`
  - The loud cost is the model bill, visible in `total_cost_usd`
    - The quiet cost is a gigabyte of memory per concurrent session, and your evenings spent answering "it did not work"

### Notifications

- Notification transports
  - A notification transport is how an unattended job reaches you away from the machine
    - Without one, you find out only when you next happen to look, which may be days
  - A notification for every processed matter is a notification for none
    - What earns one is what failed or needs a decision, not what went fine
  - A failed run, a document awaiting approval, a spotted deadline, one matter in twelve that failed -- all clear that bar
  - A two-way transport adds the reply -- a decision sent back from the phone, not held until you're at the machine

- Telegram, ntfy and email
  - Pick the transport by where you'll actually see it
    - Telegram or Discord: a bot posting into a chat you already have open
    - `ntfy`: pushes straight to a phone off nothing more than a topic name
    - Email through a provider's API: for a record that belongs in an inbox, not just an alert
    - A desktop notification: simplest of the four, and dies at the edge of the machine -- nobody on the train sees it
  - Where you already look decides which one works, not which is technically best
    - Show an email sent at 3am and not opened until 9, next to an `ntfy` push that lands on the phone the same minute, so the reader sees the delay come from the channel and not from Claude

- Claude Code in Slack
  - Slack isn't just another transport from the list above -- "Claude Code in Slack" is its own integration
    - Running a cloud session rather than one on your machine, started by `@Claude` mentioned in a channel
  - Two-way: it narrates as it works, posting status and summaries back into the channel
    - Picture the intake skill's change, narrated turn by turn as it runs, ending with a button to open a pull request
  - Channels only, never DMs, and one pull request per session
  - Needs a claude.ai login, a connected GitHub account and a paid plan -- not available on Bedrock, Vertex or Foundry
  - Being replaced by Claude Tag on Team and Enterprise plans


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

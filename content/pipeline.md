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
  + What level two ended with
  + What starts the work now, when it is not you
  + Where the machine is when it runs
  + What this level does not add

- The shape of an automated system
  + The four parts: trigger, input, work, output
  + The four kinds of trigger
  + Where Claude Code sits among them
  + Why the output has to leave the machine

- Less is more
  + What an agent turn costs against a script
  + Where judgement is needed and where a rule will do
  + The test to apply before asking for an agent

### Scripted Behavior

- What a script is for
  + What a script is
  + What it does not do
  + Who writes it and what runs it
  + Why it outlives the session

- Python, Node and Bun
  + What Python is for and why it is the default
  + What Node is for
  + What Bun is
  + That the choice is not yours to make

- A script instead of an agent turn
  + What an agent turn repeats on every run
  + What a script guarantees instead
  + Decisions that reduce to a rule
  + Decisions that do not
  + What a script cannot notice

### Environments

- Virtual environments
  + Why one project's install breaks another
  + What `.venv` is and where it sits
  + How to delete one
  + Why this is called a Python problem
  + Where an environment stops and a container starts

- uv, pipx and conda
  + What uv is for
  + What pipx is for
  + What conda does that neither does
  + What conda costs
  + When to leave a working setup alone

### Logs

- Unattended work fails quietly
  + How a failed run and a clean run look the same
  + What an exit code of zero means
  + Why a record written during the run is the only evidence
  + What that record lets you ask afterwards

- Where logs go
  + Where the output of a typed command goes
  + Where the output of a scheduled job goes
  + One job, one file, one known place
  + What belongs in a log line
  + Why a log nobody reads is not a log

- Log aggregators
  + What twelve separate log files cost you
  + What an aggregator collects them into
  + The questions only answerable across all of them
  + journalctl, Loki, and a SQLite table
  + How many jobs justify one

### Language Servers

- What a language server is
  + What a language server is
  + The difference between knowing the language and knowing your project
  + What Claude does without one
  + What it answers that grep cannot

- The servers there are
  + That they already exist, one per language
  + gopls, pyright, ruff
  + How many a mixed repository runs
  + What a server's scope is
  + What happens when you open a different project

- Wiring one into Claude Code
  + Where a server is declared
  + The binary has to be installed first
  + Wiring into a project against wiring into a plugin
  + What a plugin carries to whoever installs it

- Diagnostics
  + That it is on by default
  + What arrives in context with it on
  + What still works with it off
  + What a long editing session pays for it
  + How to choose

## Triggers

### Schedulers

- What a scheduler is
  + What a scheduler is and what it survives
  + The three implementations
  + What to say when asking for one
  + That it fires whether or not the last run finished

- cron
  + What a crontab line holds
  + What runs on the rented box
  + Why cron is the name people reach for
  + Overlapping runs

- launchd
  + What launchd is and Apple's position on it
  + Why being owned by the operating system matters
  + What to ask for on a Mac
  + That cron still runs on macOS

- systemd timers
  + What they replace and what they resemble
  + What happens to a missed run
  + Where the outcome is recorded
  + Waiting on another service before firing
  + That they are Linux only

- Claude Code's own scheduler
  + What its cron tools actually schedule
  + The limits: no session, seven days, jitter, between turns only
  + What they are for
  + What to use instead for unattended work

- Machines that sleep
  + That neither cron nor launchd wakes a machine
  + What `RunAtLoad` does
  + What `anacron` does
  + Where a job that cannot be missed belongs

### Watchers

- What a watcher is
  + What a watcher is and what it starts
  + Being told against asking on a timer
  + That it only works while it is running

- inotify, fswatch and entr
  + What inotify is and why it is Linux only
  + What fswatch is for
  + What entr is for
  + Asking for the outcome, not the tool

- A folder as a trigger
  + The folder as the whole interface
  + One watched folder per job
  + That a file mid-write is not a finished file
  + Waiting for a file to stop changing

### Queues

- What a queue is
  + What a queue is and what it prevents
  + How many workers pull from it at once
  + What happens to a job that fails
  + That the trigger is separate from the queue

- Redis, SQLite and the serious version
  + When a `jobs` table is enough
  + When Redis earns its place
  + What RabbitMQ and Celery are built for
  + The path from one to the next

### Monitors

- What a monitor is
  + What a monitor is and where its output goes
  + What it is useful for
  + How it differs from a watcher
  + That it is experimental
  + What its lifetime is tied to

- Declaring one in a plugin
  + Where a monitor is declared
  + `always`
  + `on-skill-invoke:<skill-name>`
  + Why the choice matters

## Integrations

### APIs

- What an API is
  + What an API is
  + That most services you click through answer requests too
  + What has to be installed
  + That not every service has one

- curl and jq
  + What curl does
  + What jq does
  + Why the two together are the cheapest integration there is
  + What they reach: case status, exchange rates, court listings, unpaid invoices
  + That you never type either yourself

- The API shapes there are
  + The question every shape splits on: who speaks first
  + REST
  + Webhooks
  + WebSockets and server-sent events
  + GraphQL
  + That the service chose the shape, not you

- Polling and webhooks
  + What a webhook does, and where it exists
  + How polling is built
  + Why polling is the one you can always build
  + That courts do not offer webhooks

- Scraping
  + What scraping is left to do
  + Reading HTML meant for a person
  + The manners: User-Agent, and how often
  + Where curl stops working
  + That a layout change breaks it silently

### MCPs

- What an MCP is
  + What an MCP server is
  + How it differs from writing curl commands
  + How it differs from a connector
  + That not every service has one

- Adding one
  + How a server is added
  + Searching for a published server first
  + The two things adding one settles
  + What a local server is running with your access

- The transports
  + What the transport decides
  + `stdio`
  + `http`
  + `sse`, and that it is deprecated
  + What happens when the transport is wrong

- Scopes and where they live
  + `local`, `project`, `user`
  + Which file each lives in
  + What `project` scope carries with the code
  + The two paths that look right and are not
  + How to choose

- Authentication
  + What the choice decides beyond connecting once
  + A static header
  + OAuth, and what it does on a 401
  + `headersHelper`, its ten seconds, and where it belongs
  + Which one survives the hours nobody is watching

- Tool search and output limits
  + What tool search loads at startup and what it defers
  + What a dozen servers cost with it on
  + `MAX_MCP_OUTPUT_TOKENS`, its default, and its warning
  + What happens to a large reply
  + `ENABLE_TOOL_SEARCH=false`

- Timeouts
  + That there are four separate clocks
  + `MCP_TIMEOUT`
  + The per-server `timeout`
  + The HTTP request timer
  + Idle timeout, local and remote
  + Matching a failure to the clock that caused it

- MCPs in unattended sessions
  + What a project-scoped server normally prompts for
  + What happens when nobody is there to answer
  + The security fact that follows
  + `disabledMcpjsonServers`, and the harder switch
  + What Managed MCP is

- Driving a browser headlessly
  + What a browser-driving server is
  + Playwright
  + Why no display is needed
  + That nothing about the run is visible
  + Which pages are plain enough to run unwatched

- When an MCP breaks
  + The most common malformed config: `url` with no `type`
  + Why a broken server looks like an absent one
  + What an empty tool list does and does not prove
  + How to tell a failure from an absence
  + Asking Claude what actually loaded
</content>

### Browser and Screen Control

- What Chrome control is
  + What Chrome control is
  + What it does to a real window
  + The site with no API and no way in through the terminal
  + What computer use drives instead

- The browser's own login
  + What it shares with the browser
  + What it reaches without a credential of its own
  + That nothing is exported or stored
  + How long the access lasts

- The portal with no API
  + The use case: court and government systems
  + The page that renders nothing until its JavaScript runs
  + That it runs in a visible window, watchable
  + Where it hands control back: logins, CAPTCHAs
  + Which calls prompt and which do not

- Computer use
  + What computer use is
  + Which platforms and which plans
  + How approval is scoped, and how many sessions may hold control
  + That it does not work under `-p`
  + Escape, and what is hidden from its screenshots

- Reach for these last
  + The ladder: MCP, Bash, Chrome, computer use
  + Why an API is faster and does not break when a button moves
  + What screen control is actually for

### Connectors

- What a connector is
  + What a connector is and where it is ticked on
  + How it differs from a server you configure
  + Why remote authorisation reaches services a local one cannot
  + Gmail, Calendar, Microsoft 365, Slack

- Turning one on
  + Where the tick is made
  + What is installed on your machine
  + Where authorisation happens
  + How often the tick is made

- The subscription condition
  + What the session must be signed in with
  + The five setups that make connectors disappear
  + That they disappear silently
  + What happens when the login lapses
  + What an unattended job must not assume

- Precedence
  + Which wins, your own server or a connector
  + What the match is made on
  + Overriding a connector without turning it off
  + Why renaming changes nothing

### Channels

- What a channel is
  + What a channel does, and in which direction
  + How that reverses every other integration here
  + What it is used for
  + How a channel differs from a notification

- The channels there are
  + Telegram, Discord, iMessage
  + The webhook receiver
  + Which login it needs, and where it does not run
  + What Team and Enterprise do by default

- Switching one on
  + Installing and configuring it
  + Naming it on the command line
  + That `.mcp.json` alone is not enough
  + Why it is off by default
  + Where events arrive and where they do not
  + What an always-on channel means in practice

- Two-way and the permission relay
  + What two-way depends on
  + Redirecting a run from your phone
  + What the permission relay puts in two places
  + Which answer wins

- Gating the sender
  + Gate on the sender, not the room
  + What gating on the room lets through
  + The same problem with a webhook receiver
  + That an ungated channel is a prompt-injection hole with an address

### Deep Links

- What a deep link is
  + What a deep link opens, and the scheme
  + What it carries: prompt, directory, repository
  + What it is used for
  + That it never runs on its own

- Firing one
  + Where it can be fired from
  + When the handler registers, and what stops it
  + That some sites strip the scheme
  + Putting it in a code block

### Credentials

- Where keys should live
  + What a dozen services means for a dozen credentials
  + The 3am job that needs a key with nobody there
  + Rotating a shared password in one place
  + Keeping a key out of a repository that gets shared
  + The rule: fetched at the moment of use, not stored everywhere

- The keychain, direnv and password managers
  + Keychain
  + `.env` and `direnv`
  + Bitwarden and 1Password
  + Vault and cloud secret managers
  + That a script asks by name and keeps no copy

- Keys and the transcript
  + The three ways a secret reaches a transcript
  + How long transcripts last
  + Why the fix is timing, not care
  + Reaching a service without telling Claude the key
  + What else read into context carries the same risk

- apiKeyHelper and sandbox credentials
  + What `apiKeyHelper` does and when
  + What it keeps out of a settings file
  + What `sandbox.credentials` does
  + What both are for

## Databases

### Why Database Anything

- What a database is
  + The question a folder answers
  + The questions it cannot
  + What a database holds instead
  + That several shapes exist
  + That a database does not make its contents true

- Why put your own files in one
  + What your existing material becomes
  + That nothing moves and nothing is thrown away
  + What you can then ask
  + That anything not recorded is invisible

- SQLite first
  + What SQLite is
  + What it is the default for
  + The one condition that changes the answer
  + What reaching further early costs
  + What to name, and what to leave to Claude

### Relational

- Relational databases
  + What a relational database holds
  + What it holds between records
  + Why it is the shape your material already has
  + That connections are hard to change later

- PostgreSQL
  + What Postgres is and what it is the step up from
  + JSON, full-text and vectors in one instance
  + Several people or automations at once
  + How a server differs from a file
  + That nothing answers while it is stopped

- DuckDB and the others
  + MySQL and MariaDB
  + SQL Server and Oracle
  + What DuckDB is and how it differs from SQLite
  + Querying CSV and Parquet where they sit
  + That none of this is a decision to make

### The Other Kinds

- Document databases
  + What a document database stores
  + Saving before deciding the structure
  + What it is used for
  + That a typo becomes a new field
  + What a JSON column covers instead

- Key-value stores
  + What a key-value store holds
  + The notepad that survives between runs
  + What it is used for
  + That nothing expires on its own
  + What a two-column table covers instead

- Columnar databases
  + What a columnar database reads
  + Why the same question runs faster
  + What it is used for
  + The case it is bad at
  + When it earns its place

- Graph databases
  + What a graph database stores as the primary thing
  + The question that is direct here and painful elsewhere
  + What it is used for: ownership, conflicts, family
  + That a small graph buys nothing
  + How far SQLite's recursive queries reach

- Time-series databases
  + What a time-series database stores
  + The questions shaped by time
  + What it is used for
  + What it discards, and what happens if you never decide
  + What a timestamp column covers instead

### Search

- Full-text search
  + What grep does every time
  + What an index does once
  + Ranking, and stemming
  + SQLite FTS5 and Postgres `tsvector`
  + Tantivy, Meilisearch, Elasticsearch
  + That an index goes stale silently

- Vector search
  + What full-text finds against what vector search finds
  + How it works
  + What it is used for
  + sqlite-vec and pgvector
  + Chroma, Qdrant, LanceDB
  + What changing the model does to everything stored

- Retrieval in practice
  + Why no model can be handed the whole archive
  + What retrieval does in between
  + Why a setup commonly wants both kinds of search
  + That an answer on the wrong passages reads exactly as confident

### With the Harness

- Getting your material in
  + What form the material arrives in
  + The three steps: extract, classify, record where it lives
  + The OCR step a scan needs first
  + That the original never moves
  + What to point Claude at
  + That a failed import fails silently

- Asking questions of your own data
  + What becomes ordinary once the material is in
  + The questions worth asking
  + Who writes the query
  + Which pieces already covered answer them
  + That a wrong query produces a confident number

## Automatic Outputs

### Document Automation

- Document pipelines
  + That these are commands, not libraries
  + What OCR makes possible
  + What the archive becomes
  + That the tools run in both directions
  + The two kinds of PDF, and why they look identical

- poppler and pdftotext
  + What poppler is
  + What pdftotext pulls out
  + Splitting, merging and rendering
  + Using it as the test for which kind of PDF you have
  + Why it is the first thing to try

- tesseract and OCR
  + What tesseract does
  + What it is used for
  + That a poor scan produces confident wrong text
  + What running it on a text PDF destroys
  + Checking which case you are in first

- pandoc
  + What pandoc converts between
  + What it is used for
  + What a conversion loses, and which way
  + Choosing the format for what has to survive

- LibreOffice headless
  + What LibreOffice headless is
  + Turning a DOCX into a PDF from a script
  + When to reach for it over pandoc
  + What it does with Excel
  + Macros, fonts and templates that render differently

### Templates

- Templating
  + What a template is
  + Why the point is not saved typing
  + What stays fixed between the first fill and the hundredth
  + What free drafting does to approved wording
  + Where the values come from

- Jinja and docxtpl
  + What Jinja is
  + What docxtpl adds
  + What survives untouched: letterhead, styles, layout
  + That the output is a real editable document
  + Which of the two is the asset worth keeping

- Filling a form PDF
  + What a form PDF already carries
  + What filling one means
  + What flattening does and why
  + Why this is not templating
  + The opposite case: a PDF built from scratch

- Typst and LaTeX
  + What typesetting is for that word processing is not
  + What it buys: page breaks, running headers, renumbering
  + What Typst is
  + What LaTeX is
  + When it is more than the job needs

### Artifacts

- What an artifact is
  + What an artifact is and where it is published
  + What the file itself is
  + What it is used for
  + What plan and login it requires

- Publishing and revising
  + How often publishing prompts
  + What revising means, and what viewers see
  + That each publish is kept as a version
  + What to hand Claude from a later session
  + Who it is private to, and how sharing differs by plan

- Connectors inside an artifact
  + What a page may do when it loads
  + The status page that fetches its own data
  + What that means for the automation behind it
  + Why two viewers can see different things
  + The viewer with no connectors of their own

- The content policy
  + What is blocked
  + What network traffic is blocked
  + What has to be inlined
  + The size ceiling
  + What all of it makes an artifact

### Static Sites

- Static site generators
  + What a generator produces
  + Why the output works wherever it is put
  + Hugo, Zola, Eleventy, MkDocs
  + GitHub Pages
  + That a hosted site is public by default

- Publishing what an automation makes
  + Why this is the cheapest way to reach a person
  + The status page regenerated nightly
  + What runs when the page is opened
  + That a mistake publishes as readily as a correct result
  + What to point Claude at

## Hosting and Serving

### Web Servers

- What a web server is
  + What a web server does
  + What it is used for
  + The two kinds of answer it can give
  + Who it answers by default
  + That the door is open only while it runs

- Reverse proxies
  + Where a reverse proxy sits
  + Several services behind one address
  + That it carries the certificate
  + What it refuses
  + That a browser error does not say which side broke

- Caddy, nginx and certificates
  + What a certificate does
  + What Caddy does on its own
  + What nginx is, and what it leaves to you
  + Which to ask for
  + That a certificate belongs to a name, not a machine

- Tunnels
  + The problem a tunnel solves
  + How it works
  + What it is used for
  + Tailscale
  + That it changes how the machine is reached, not what is listening

- Self-hosting
  + What self-hosting means for where files land
  + What a domain name costs and buys
  + What paid hosting sells past that
  + The one condition: the machine has to stay awake

- A worked example — the intake form
  + The page the web server serves
  + What Caddy puts in front of it
  + What submitting writes: files, a row, a job
  + What picks the job up and runs it
  + What is waiting when you next look
  + That a form accepting uploads accepts files from strangers

### Containers

- What a container is
  + What a container holds
  + Where it runs identically
  + What it means for an agent working inside one
  + Docker, and devcontainers
  + That containers are Linux only

- Images and registries
  + Image against container
  + How an image travels
  + Architecture, and building for the target
  + Cloud Run and its kind
  + That the tested image is the thing that runs

- Reproducibility
  + Why people reach for containers apart from safety
  + What the recipe guarantees
  + Two projects with incompatible dependencies
  + Trying software and leaving nothing behind
  + That the guarantee stops at the edge of the box

- Running one on a box that never sleeps
  + The problem a laptop cannot solve
  + What the rented box needs installed
  + What it is used for
  + That building and running are different acts

## Agent SDK

### The SDK Harness

- What the Agent SDK is
  + What the Agent SDK is, and in which languages
  + What your program decides that a terminal used to
  + What Claude becomes inside another program
  + What is unchanged underneath
  + That it removes the terminal, not the engineering

- How it differs from headless sessions
  + The prior question: whether it is needed at all
  + What a headless session already does
  + The four cases where the SDK earns its place
  + The shape of the difference
  + What it buys when the program only fires and collects

- Use cases
  + The back end of an intake form
  + One agent per customer
  + Anything with someone waiting on the line
  + What it is not for

### Building an SDK

- Running a query and holding a session
  + That there are two entry points
  + What the single-question one does
  + What the session one keeps alive
  + Interrupting mid-thought
  + How to choose between them

- The messages that come back
  + What comes back instead of text
  + What the first message carries
  + Which messages arrive during the run
  + What a turn is
  + What the final message carries
  + What that makes possible: live status, per-turn billing, a log

- Stopping it running forever
  + That there are two limits and neither is a clock
  + The turn limit
  + The cost limit
  + That there is no overall timeout
  + Why an unattended program needs something watching from outside

- The permission callback
  + What the callback decides
  + When it fires, and when it does not
  + Why it is not the security boundary it appears to be
  + The six permission modes, and where the callback sits
  + What a deny rule outranks

- One process, many customers
  + What loads into an SDK session by default
  + What a per-customer process separates
  + The risk that separation manages
  + Why it is the design, not an afterthought

- Sessions and where they live
  + Where a session persists
  + Resuming by identifier
  + Forking a session
  + What that is used for
  + When mirroring to S3, Redis or Postgres stops being optional

- What it consumes
  + What every run spawns
  + What twenty concurrent customers means
  + The floor: memory, disk, a core
  + That the reported cost is an estimate from a built-in price table
  + What that estimate is good for, and what it is not

### Deploying and Integrating SDKs

- The shapes a deployment takes
  + The four faces
  + That nobody sees Claude behind any of them
  + What choosing between them is actually about
  + Building the face you know how to build

- Behind a TUI
  + What it is
  + Why it is the cheapest
  + What it is for
  + How far it goes
  + What it signals to a colleague who is not a developer

- Behind a web page
  + What a browser reaching it changes
  + Who it makes the program available to
  + What does not arrive on its own
  + That anything reachable is reachable by anyone

- Inside a desktop app
  + What it is
  + What it does not announce itself as
  + What it is for
  + What installing and updating costs
  + The question the window hides

- On a phone
  + Where the agent actually runs
  + What the phone therefore needs
  + What it is for
  + The cheapest version: the same web page
  + What happens when the connection drops

- Where the process actually runs
  + The question behind all four faces
  + The three answers
  + Why a laptop that sleeps is not a host
  + The difference between working when tested and working when you are away

- Streaming to someone waiting
  + How an agent produces its answer
  + What a blank screen reads as
  + What to show while it works
  + Why it matters most when the person waiting is not you
  + The long step that produces no message of its own

- Keeping it up
  + What a deployment has to survive
  + What someone else using it raises
  + Resuming a customer's thread next week
  + The cost that is loud
  + The cost that is quiet

### Notifications

- Notification transports
  + What happens at 3am without a way to reach you
  + What is worth being told
  + What a transport is, and how to choose one
  + What a two-way transport adds
  + That a notification for everything is a notification for nothing

- Telegram, ntfy and email
  + Telegram and Discord through a bot
  + ntfy
  + Email through an API
  + Desktop notifications, and where they stop
  + That the question is where you already look

- Claude Code in Slack
  + That Slack is not a channel, and what it is instead
  + What it posts, and what it offers at the end
  + What it needs, and where it does not run
  + The ceiling: channels only, one pull request
  + Claude Tag on Team and Enterprise


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

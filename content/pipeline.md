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
  - Establish the four-part shape of any automated pipeline -- trigger, input, work, output -- as a skeleton the reader can hang every later system on, before naming any part individually
    - Carry a single pipeline all the way through the four slots in one pass, so the shape is proven by use rather than defined and then left: show a new scan landing in the intake folder (trigger and input), Claude Code reading and refiling it (work), and a log line plus a message to the paralegal (output)
  - List the four kinds of trigger -- a clock, a file appearing, a request arriving, a message pushed in -- against a plausible law-firm case for each, so the taxonomy is not left abstract: a nightly deadline sweep, a scan dropped into a folder, a client's web form, a message arriving from opposing counsel's system
  - State and defend the rule that Claude Code is the work step and never the trigger; a reader arriving from level 2, where opening a session was itself the start of the work, needs told directly that this stops being true here
  - Insist that output has to land somewhere real and durable -- a file, a log, a database row, a message sent -- not sit in the transcript of a session nobody reopens; name the transcript-as-output habit from level 2 as exactly what has to be unlearned

- Less is more
  - Recall the cost point in a single line -- it was already made when the level opened -- rather than re-arguing it here; this article's job is the split, not the pitch
  - Draw the line that decides what becomes a script and what stays an agent turn: anything that reduces to a fixed rule goes to a script, anything that needs a judgement call stays with the agent
    - Set one matter-folder decision on each side of that line: filing a scan by a pattern in its filename is a rule; deciding whether a letter's tone signals a settlement offer is judgement
  - Stop at the boundary itself. "A script instead of an agent turn" is where each side of that line gets worked through in full; do not pre-empt it here

### Scripted Behavior

- What a script is for
  - Draw the boundary between authoring and running: Claude writes the script during a session, but something else entirely -- cron, a shell, a scheduled job -- is what runs it, and that happens only after the session has already ended
  - Make the point that a script outlives the session that wrote it, and carry it with a dated example rather than an abstract claim
    - Walk the filing rule written into a session in March: by December the session is long closed and nobody remembers writing it, yet the rule is still filing scans into matter folders every night, unattended
  - Contrast this against level 2's agent turn, which exists only for the length of the conversation that asked for it, to make plain why "outlives the session" is the whole reason a script gets written at all

- Python, Node and Bun
  - Name Python as the default choice and say why: it is already on every machine the reader is likely to touch, and every library they will reach for is already installed
  - Introduce Node as the alternative that arrives already bundled with the web-development world, rather than one the reader would pick cold
  - Introduce Bun as what replaces Node when speed is the reason to switch: the same ecosystem, TypeScript understood natively, no separate build step first
    - Demonstrate that the runtime choice is just a file extension by writing one small task -- checking a folder for new scans every minute -- once as a `.py` file, once as a `.js` file, once as a `.ts` file: three names on one outcome, not three competing decisions
  - The choice is not the reader's to make consciously. They name the outcome they want; the runtime only shows up afterward, as whichever file extension Claude happened to write

- A script instead of an agent turn
  - Open on the contrast that motivates everything else in this article: an agent turn re-derives its answer every run and can drift slightly from one run to the next, where a script performs the identical steps every time, for better and for worse
  - Work through the split "Less is more" drew but left unopened, one side at a time rather than as a single mixed list
    - Show what a rule actually looks like, not just the word, by putting three rule-side cases side by side: filing a scan by a pattern in its filename, computing a deadline from a date already on the page, checksumming a count against an expected total
    - Set two judgement-side cases against them: deciding whether a letter mentions a deadline at all, deciding whether "Jon Smith" and "Jonathan Smyth" name the same client -- both demand reading for meaning, and no pattern gets either one right
  - Name a third category that sits on neither side of the split and needs saying plainly: things a script cannot detect at all, however carefully it's written
    - A scan fed in upside down
    - A wrong matter number typed onto the form by hand
    - State why: a script only checks what it was told to check, and neither of these announces itself as a problem to a rule -- only a human, or an agent actually looking at the page, would catch it

### Environments

- Virtual environments
  - Open with the collision that makes virtual environments necessary at all: two projects on one machine needing different versions of the same package, and a system-wide install can only hold one version, so one project breaks
  - Explain what `.venv` actually does about it: it sits inside the project folder, and Python looks there before it looks at the system install, so the project's own version wins locally without touching anything else on the machine
    - Draw the same package pinned at two different versions -- one inside `.venv`, one system-wide -- and mark which one actually runs when the project is opened; the shape is the point, not the mechanism
  - Give this its own short line rather than folding it into the paragraph above: state that deleting the `.venv` folder takes every package inside it down with it, and nothing else on the machine needs cleaning up afterward
  - Correct an assumption the name invites: this is not a problem unique to Python, only named after Python's version of the fix -- `node_modules`, Go's static binaries, a bundler, cargo all solve the identical collision their own way
  - Place virtual environments on the timeline: bolted on after the fact, not designed in from the start, because Python was already installing system-wide for decades before the problem got named
  - Position `.venv` against a container for the reader who has heard of both: one layer lighter, since it isolates the libraries rather than the whole operating system

- uv, pipx and conda
  - Position `uv` as a faster replacement for the `.venv`-and-`pip` combination just covered -- same job, done in a fraction of the time, nothing conceptually new for the reader to learn
    - Set the two side by side on one setup: `python -m venv` plus `pip install` for the intake script's dependencies, timed, against `uv` doing the identical install, timed -- the seconds are the whole pitch
  - Separate `pipx` out by what it is for rather than how it works: installing command-line tools each into its own isolated environment, so they never get mixed into whichever project happens to be open
  - Push `conda` further along the same spectrum: it installs the interpreter itself, not just libraries, and reaches past Python entirely into compilers and CUDA -- name the cost that buys, in both weight and speed
  - Close with a refusal: a reader whose lab already runs on conda has nothing to fix by switching to `uv` -- this article is not a case for always using the newest tool

### Logs

- Unattended work fails quietly
  - Flag the habit a reader carries over from level 2 as no longer safe: back then, a quiet terminal after a session usually meant nothing needed attention; at level 3, a silent terminal proves nothing either way
    - Put a terminal from a run that did nothing next to a terminal from a run that correctly filed six scans -- both blank, both equally silent, so the point lands rather than just gets stated
  - Exit code zero is not proof of success. It only reports that the last command in a chain returned zero -- not that the work upstream of it happened at all
  - State plainly the conclusion this article turns on: the only evidence of what an unattended run did is a record written down during the run itself, which is what makes logging non-optional rather than a nicety

- Where logs go
  - Explain why the habit changes from level 2: a typed command's output dies with the terminal it ran in, but a cron job has no terminal to die with -- its stdout goes to mail if anywhere, and more often nowhere at all, unless the job redirects it itself
  - Show the redirect sitting on an actual cron line, in the order schedule, command, redirect, rather than displaying the syntax floating alone -- one job, one file, one known place, written as `>> ~/logs/intake.log 2>&1` -- to give the pattern as a fixed shape rather than a rule to derive
  - Specify what a usable log line has to carry: the time, which matter it concerned, what was actually done, and the exit status -- note that dropping any one of the four turns a later debugging session into guesswork
  - State plainly that a log nobody reads is disk space, not a log, so that the next article's aggregator reads as a consequence, not an add-on

- Log aggregators
  - Motivate the whole idea from the previous article's failure mode, at scale: twelve separate log files means nobody actually reads all twelve, and a failure buried in the ninth one sits unnoticed indefinitely
    - Pose one real question -- did the intake job run on the 14th -- and show what answering it costs against twelve raw files: opening each one by hand, in date order, looking for a line that may not be there. That is the case for a single query before a single tool name is offered
  - State what an aggregator buys concretely: one searchable place standing in for twelve separate files, and specifically the questions no single file can answer alone -- which run failed and why, what Claude has cost this month across every job, whether a job ran at all last night, what got silently skipped
  - Name the actual choices rather than leaving "an aggregator" abstract: `journalctl` if systemd is already running the jobs, otherwise something like Loki or even a timestamped SQLite table for a smaller setup
  - Frame the decision as a threshold call rather than a best practice to always follow: twelve jobs running across a real practice justify the overhead, two challenge scripts on a laptop do not -- tell the reader plainly not to build this until the first case is true

### Language Servers

- What a language server is
  - Define a language server by what it answers, not what it is: questions about the reader's specific code -- which file defines this function, who actually calls it, what breaks if it changes -- not questions about the language in general
  - Separate what it arrives already knowing from what it has to learn: the language's grammar comes built in, but it has to be pointed at the reader's actual project before it knows what any particular name refers to there
  - Without one, Claude falls back to grepping and guessing. Guessing is exactly where bugs get introduced, and the reader should hear that named, not just implied
  - Set grep and the language server against each other on one concrete search, so the difference is undeniable rather than asserted
    - Run both against the same function name in a real file: grep returns every line containing that string, including a comment and an unrelated variable sharing the name; the language server returns only the actual definition and the calls that genuinely invoke it -- the gap between the two lists is the whole argument

- The servers there are
  - Set expectations before naming any: these already exist, one per language, and nobody -- including the reader -- writes their own
  - Fix the counting unit clearly: one server per language, not one per project, so the number the reader needs is just the count of languages actually used in their repository
  - Ground this in tutor's own setup as a worked case rather than a hypothetical: two language servers run side by side here, one for the Go reader, one for the Python parity oracle, because the repository genuinely contains two languages
  - Scope what a server actually indexes: everything under the folder it is pointed at, and nothing else -- open a different repository and it starts fresh, with no memory of the last one

- Wiring one into Claude Code
  - Name the two places this gets declared: a standalone `.lsp.json` at the plugin root, or inline inside `plugin.json` under an `lspServers` key -- the same information in two locations, depending on what else the plugin already has
  - Give the two fields that are compulsory, and only those two, before anything optional gets mentioned: `command`, the binary already sitting on `PATH`, and `extensionToLanguage`, mapping a file extension to the language it belongs to
    - Show the smallest `.lsp.json` that actually works: just those two fields, wiring one extension to one command, so the reader has a working baseline before any option gets added on top of it
  - Layer the optional fields onto that baseline rather than listing them alongside the compulsory ones: `args`, `env`, `startupTimeout`, `restartOnCrash` (already on by default), `maxRestarts`
  - Point at real servers instead of leaving `command` abstract: `typescript-language-server`, `pyright`, `rust-analyzer` are named in Claude Code's own docs, and all three install with `npm` or `pip`
  - Distinguish project scope from plugin scope: a project-scoped server serves that one repository alone, a plugin-scoped one ships automatically to everyone who installs the plugin
  - Close on the payoff against the effort: four lines in a plugin buys every installer symbol navigation for free, with nothing further for them to configure

- Diagnostics
  - State the default plainly: diagnostics are on, meaning every error the server sees lands directly in Claude's context the moment an edit is made, without being asked for
    - Put the same broken edit under both settings: with diagnostics on, the type error's actual text arrives in context unasked; with them off, nothing arrives at all, and Claude only finds out if it runs the file or the reader says something
  - Say what turning it off does and does not cost: navigation keeps working exactly as before -- go-to-definition, find-references, hover -- only the running commentary on errors disappears
  - This is a trade-off, not a setting with an obviously right answer. Weigh context space spent on every edit against catching a broken line the instant it's written, and leave the answer to the reader's own project rather than picking for them

## Triggers

### Schedulers

- What a scheduler is
  - Open by naming what a scheduler actually is: an OS-level daemon, not a Claude Code feature, that fires a command at a set time whether or not anyone is logged in, and survives a reboot doing it
    - Set this against a typed command sitting in a terminal, since that's the mental model a reader arrives with: kill the terminal and the command dies with it; a scheduler has no terminal to kill
  - Cron, launchd and systemd timers are three names for one idea, not three competing designs, and which one a reader meets is decided by platform rather than by which is "best" -- say so plainly before naming a single one of them
    - Hand the reader the deciding rule now, ahead of the three articles that name each tool: a Mac defaults to launchd, most current Linux distributions default to systemd timers, cron runs on both as the oldest common ground
  - Draw the five-field spine bare, with no tool's syntax attached to it yet -- minute, hour, day-of-month, month, day-of-week, then a command
    - Sketch it as five slots feeding one command, since the shape itself is the point here: cron's line, launchd's plist and systemd's `OnCalendar` will each map back onto these same five slots when the reader meets them, so the picture, not the wording, is what should stick

- cron
  - Show the whole anatomy of one cron line in a single breath, because a reader who can read one can read all of them: `0 6 * * 1-5 claude -p "run the intake skill" >> ~/logs/intake.log 2>&1`
    - Break it into its three jobs: the five fields set the schedule (six every weekday morning), the middle is the command exactly as it would be typed live, and the redirect turns a one-off run into a record that survives after the terminal closes
  - Note that nothing needs installing first -- cron is already running on the machine, Mac or Linux, before the reader writes a single line
  - Set cron against Claude Code's own scheduler on one point only, because the two get confused: cron fires whether or not Claude Code, or anything else, is even open; the built-in scheduler only ever fires inside a session that's already running
  - Warn about the gap cron doesn't cover: it has no memory of whether yesterday's six o'clock run actually finished, so a slow run and today's six o'clock run can both grab the same matter folder at once
    - Walk through what that collision looks like on the intake skill specifically -- two `claude -p` processes both mid-write to the same folder -- and name `flock` as the fix that makes the second run wait its turn instead of colliding

- launchd
  - Anchor this one by contrast with cron rather than by repeating cron's shape: launchd is the scheduler Apple's own tools assume by default, even though cron still runs quietly underneath on a Mac
  - Cron only ever knows clock time; launchd can also fire on an event -- a disk mounting, a login happening -- with nothing polling in the background to notice it, and that difference in kind matters more here than any syntax comparison
    - Make the event case concrete instead of leaving "an event" abstract: picture a backup job wired to fire the moment an external drive is actually plugged in and mounted, never running at all on a day nobody plugs one in, which is a schedule cron has no way to express
  - Cover how a launchd job is actually declared, since the reader has just seen cron's one-liner but nothing yet for this one: a property list file, loaded by the daemon, holding both the trigger and the command together in one place
  - Close on `RunAtLoad`: a job due while the Mac was asleep doesn't just vanish -- it catches it and fires it the moment the machine wakes, which is the detail that matters most to a laptop reader

- systemd timers
  - Frame systemd timers as the structural opposite of cron's one-liner: where cron is a single line, a systemd timer is two paired files -- a `.timer` that sets the schedule and a `.service` that names the command -- and both must exist for the job to run at all
    - Put the two files for the intake job side by side, as short as they'd actually be written, to show two small files standing in for cron's one line: the `.timer` carrying `OnCalendar` and `Persistent=true`, the `.service` carrying nothing but the `ExecStart` line for `claude -p "run the intake skill"`
  - Note the platform limit up front and move past it: Linux only, no Mac equivalent, none of cron's cross-platform reach
  - Set `Persistent=true` against launchd's `RunAtLoad` as the same fix under a different name, and say plainly that a machine off when the job should have fired gets caught up on either platform, just through a different key
  - Redirect the reader's instinct to reach for `>> ~/logs/intake.log 2>&1` -- that habit doesn't apply here; a systemd service's output already lands in `journalctl -u intake.service` with no redirect written by hand
  - Cover the one thing neither cron nor launchd can do: a timer can name another unit as a dependency, so the intake job simply waits until the database service is confirmed up instead of firing on schedule and hoping

- Claude Code's own scheduler
  - Open by placing this scheduler correctly against the three just covered: it is not a fourth system-level option, it is a queue living inside a session that is already open, and every property below follows from that one fact
  - Walk through the scenario this is actually for: mid-session, the reader asks Claude to check tomorrow's hearing list before the session ends; the task sits queued, fires between turns without interrupting whatever's mid-flight, and reports back in the same conversation
  - List the limits as consequences of living inside a session, not as a bare feature table: nothing fires once the terminal closes, because there's no session left to fire inside; an unmet task expires after seven days; the fire time jitters by up to thirty minutes rather than landing on the dot; and it only ever fires in the gap between turns, never mid-turn
  - Land the rule the reader needs in order to actually choose correctly: cron, launchd or a systemd timer for anything that must run unattended, this scheduler only for something that can wait for a session the reader is already going to have open

- Machines that sleep
  - Head off the assumption a reader is likely carrying over from the last few articles: none of cron, launchd or a systemd timer can wake a sleeping machine to run a job
    - Walk a single laptop through a weekend to make the gap concrete: the lid closes Friday evening, the six a.m. Saturday run simply never happens because nothing is awake to fire it, and Monday morning the reader finds no filed documents and no error either -- just silence where a result should be
  - Distinguish "doesn't happen" from "never happens" for cron and launchd specifically: `RunAtLoad` on launchd and `anacron` on Linux both catch a missed run the moment the machine wakes, rather than skipping it forever
    - Set systemd timers alongside this rather than folding them in: `Persistent=true`, covered in the previous article, already does the same catching-up, and a server that's rarely off rarely needs to lean on it
  - Close on the decision this forces: a job that genuinely cannot be missed -- a filing deadline, not a convenience check -- doesn't belong on a laptop that sleeps overnight; it belongs on a machine that's always on, which is the opening argument for running automation in the cloud rather than at a desk

### Watchers

- What a watcher is
  - Introduce the shift from the last section in one line: a scheduler asks "is it time yet" on its own clock; a watcher instead waits to be told the instant something happens
  - Show what that removes for the person doing the work: a scan, a saved file or an export lands in a folder, and that's the entire task a reader performs -- no command to type, no skill to invoke, the folder itself is the whole interface
    - Set this against a matter-folder filing rule keyed off a schedule: same folder, but now dropping the file in is the trigger itself, not a step that happens before one
  - Deflate the "cron but faster" comparison before the reader reaches for it: explain that cron polls, checking every five minutes whether anything changed, while a watcher is told by the operating system the instant a file event happens, with no polling delay at all
  - Flag the one condition the whole idea depends on, before moving to the tools that implement it: a watcher is a running process, and it only watches while it's alive -- close its terminal, or let its host reboot without it restarting, and nothing fires until it's running again

- inotify, fswatch and entr
  - Name the three in the order a reader will actually meet them, not alphabetically: `inotify` is the Linux kernel mechanism itself, and `inotifywait` is the command a script actually calls to use it -- Linux only, nothing to install on a Mac
  - Position `fswatch` as the answer to that gap: the same watching job, one command, working the same way on both Linux and macOS
  - Give `entr` its own line rather than lumping it in as a third wrapper: it's built around rerunning one command every time a watched file changes, which makes it the simplest of the three to reach for when the job is that plain
    - Put the shape of an `entr` line side by side with a folder-watching `inotifywait` line: "rerun this on change" and "fire once on arrival" are different jobs, answered by different tools, not two spellings of the same command

- A folder as a trigger
  - Walk the scan folder all the way through, start to finish, since this is where the whole idea stops being abstract: a scanner writes a PDF into the folder, the watcher notices the write finish, and `claude -p` picks it up and files it against the right matter -- the reader's entire job is dropping the page onto the scanner
  - Make the one-folder-per-job rule explicit and say why it matters: two jobs sharing one watched folder means two watchers racing to grab the same file, so intake gets its own folder and nothing else does
  - Give the counter-example before the fix, because the wrong way is the instinctive one: watching for `-e create` fires the instant the file's first byte lands, which for a slow scanner means Claude tries to file a half-written PDF
    - Show the fix against that same scan: wait on `close_write`, or poll the file size until two checks in a row agree it's stopped growing, before treating the file as arrived

### Queues

- What a queue is
  - Open with the problem a queue solves, not the definition: forty scans landing in the same ten minutes and all being processed at once would melt the machine, or blow through the day's budget in one run
    - Picture the fix directly: forty scans arrive together, two workers pull jobs off the front of the line at a controlled rate, and the other thirty-eight simply wait their turn instead of running at once
  - Draw the boundary a reader will otherwise blur: the watcher's job ends at adding a row to the queue and getting out of the way; it is not the watcher's job to process anything, and it is not the queue's job to notice the file
  - State what a queue buys beyond pacing: a job that fails doesn't vanish, it goes back into the line for another attempt, which a bare watcher-fires-a-command setup has no way to do at all

- Redis, SQLite and the serious version
  - Present the three as a ladder climbed only under pressure, not a menu picked from up front: SQLite first, Redis next, RabbitMQ and Celery last, each one reached for only once the previous rung has actually run out of road
  - Describe the `jobs` table in SQLite -- one row per job, one status column -- as already the whole queue for a single machine, one that most of this course's matter-folder pipelines never outgrow; tell the reader to start here rather than reaching past it out of habit
  - Resist moving up a rung until there's a named trigger rather than a feeling: Redis with a worker library only earns its place the day a second process needs to pull from the same queue that SQLite was ever meant to serve alone
  - Name RabbitMQ and Celery as the top rung and say what finally forces it: many workers, many queues, and routing logic -- send this kind of job here, that kind there -- that a single status column simply cannot express
    - Contrast the SQLite table and a RabbitMQ routing setup on the same story: the forty scans from the earlier queue example, first handled by two workers reading one table, then by a fleet of workers each subscribed to a different queue by document type

### Monitors

- What a monitor is
  - Define a monitor against the watcher just covered, since the two are easy to confuse: both notice something happening, but a watcher is a standalone process a reader starts by hand, while a monitor is a background command a plugin declares that runs for exactly as long as the session does
  - Every line a monitor prints to stdout reaches Claude as a notification, not a person watching the terminal -- make that concrete with the line itself: a monitor tailing a hearing-list feed prints `hearing added: Doe v Roe, 9:30 Thursday`, and Claude, not the reader, is what reads it and decides whether to act before the next turn
  - Correct the natural assumption that a monitor could replace a watcher: it cannot start an unattended run, because it only exists inside a session that's already open; it reports, it doesn't trigger
  - Flag its status honestly before the reader builds on it: still experimental, and tied entirely to the session's lifetime -- nothing is being watched the moment the session ends, with no equivalent of a watcher surviving in the background

- Declaring one in a plugin
  - Give the two places a monitor can be declared and let the reader pick by plugin size: a standalone `monitors/monitors.json` at the plugin root, or an inline `experimental.monitors` block in `plugin.json` for a plugin small enough not to need a separate file
  - Give the three compulsory fields their due in one line each -- `name`, `command`, `description` -- since none needs more; the one worth a second look is `name`, which has to stay unique within the plugin or a reload spawns a second copy running alongside the first
  - Show the two settings `when` accepts and the cost each one carries: `always`, the default, starts the monitor the moment every session opens, whether or not the reader ever touches the skill it's watching for; `on-skill-invoke:<name>` waits, and only starts once that specific skill is actually reached
    - Put a concrete number on the tradeoff rather than leaving it abstract: a plugin used in ninety sessions a week whose watched skill only fires in ten of them pays the `always` cost eighty times for nothing
  - Close on the three variables that make a declared command actually reach the plugin's own files: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` and `${CLAUDE_PROJECT_DIR}` all expand inside `command`, which is what lets a one-line declaration call a full script shipped inside the plugin instead of inlining logic there

## Integrations

### APIs

- What an API is
  - The API is a contract two programs agree to call, not a screen a person reads -- open with that distinction before naming any tool
    - `curl`, a browser clicking through a portal, and Claude's own `WebFetch` tool are three different callers speaking to the identical contract
  - Make it felt, not just stated, that clicking and scripting are the same act: the portal a solicitor clicks through is calling the same endpoints a script could call directly
    - Show, as a paired example, one click and one script call returning the identical response body: a case-status webpage set beside the JSON endpoint sitting behind its own "check status" button
  - Not every service publishes one, and the reader should not assume otherwise -- Companies House does, for company filings; most court listing pages don't
    - That gap is why the next few articles exist: where there's no API, `curl` and `jq` stop being an option and scraping becomes the fallback

- curl and jq
  - Frame `curl` and `jq` as a pair, not two separate tools: `curl` fetches a URL with headers, a key and a POST body, and `jq` cuts the JSON reply down to the one field that matters
    - No library to install, no server to run, no MCP to configure: two command-line tools already sitting on the machine, which is what makes this the cheapest integration there is
  - Group the use cases by what they're doing rather than list them flat -- recurring checks such as a morning read of a case-status endpoint that reports only what changed, values pulled into other work such as the day's exchange rate dropped into a fee calculation, notifications such as a Slack or Telegram post when a run finishes, and bulk pulls such as filings from Companies House, a court listing, or an unpaid-balance query against the accounting software
  - Do not stop at describing the pipeline -- show it running once, end to end: the literal `curl` command against a case-status endpoint, the raw JSON it returns, and the `jq` filter that narrows that reply down to the single field worth reading
    - That demonstration is the article's real argument: the reader should see for themselves how little stands between nothing automated and the one number they wanted, extracted

- The API shapes there are
  - Organize the whole article around one question, not a list of names to memorize: who speaks first
  - Take REST first and lean on what the reader half-knows already: ask, get an answer, the connection closes; say outright that this is the shape behind the vast majority of APIs, so the three that follow read as departures from it
  - Turn the question around for webhooks: the reader hands the service an address and waits to be called, and the article should present that as REST run backwards rather than as a second thing to learn
    - Stripe calling out on a completed payment and GitHub calling out on an opened pull request are the two triggers worth naming
    - Show "who speaks first" as two shapes of one job, not two unrelated ideas, by writing the same case-status check twice -- once as a poll the reader's own script initiates on a timer, once as a webhook the case system fires the moment status changes
  - Set the streaming pair side by side so their difference is visible: a WebSocket holds a line open in both directions, server-sent events hold it open in one, service to client
    - Server-sent events are the shape the reader has already watched happen -- it's how Claude's own replies stream onto the screen as they're generated
    - Do not explain how to open or maintain a WebSocket -- the reader will never write one; they only need to recognize the shape when a vendor's docs mention it
  - Cut GraphQL down to a variant rather than a fifth category -- keep it to a short paragraph noting it is still ask-and-answer, with the one difference that the request names the exact fields wanted instead of taking whatever REST hands back
  - The service picks the shape, never the reader, and `curl`/`jq` work against whichever one they're handed -- close on that, since it outranks all the naming above

- Polling and webhooks
  - Webhooks existing and being able to receive one are different things -- receiving one means standing up a front door of your own that the service can call
    - A case-management system usually offers that front door; a court almost never does
  - Where no door exists, polling is the fallback discipline: fetch on a schedule, compare against yesterday's saved copy, act only on the difference
    - Example: yesterday's saved hearing list next to today's fetch, with the one changed line being the only thing that fires an action -- everything else in the fetch is discarded unread
  - Treat the choice as a constraint, not a preference -- take the webhook when a service hands you one, and reach for polling only because there was no other way in

- Scraping
  - Scraping is the same cron-and-compare loop from the previous article, redirected at markup instead of JSON, for a page with no API behind it at all
  - The page was written for a person's eyes, not a machine's fields -- a hearing date can sit in a table cell with no id and nothing marking it as data, so the scrape is a guess about layout, not a request against a contract
    - Example: a page redesign moves that cell -- the fetch keeps succeeding, the script keeps running on schedule, and the extracted value comes back silently wrong with nothing to flag it
  - Where a login wall or heavy JavaScript rendering stops `curl` cold, hand off cleanly to Chrome control as the tool that takes over past that line
  - Spell out the etiquette a scrape owes that an API call doesn't: instruct the reader to identify the requester in the `User-Agent` and to keep the fetch to once or twice a day -- cheap enough that it bothers no one

### MCPs

- What an MCP is
  - Define an MCP server as something that advertises a list of tools, typed and described, which Claude then calls the same way it calls any built-in tool
  - Without one, reaching that same service means Claude writing its own `curl` commands and guessing at the shape of what comes back -- set the definition against that baseline
  - Ground it in use cases the reader will recognize the shape of, not the specifics of: a read-only case database, a document store, a Playwright-driven browser, error reports pulled out of Sentry
  - Example: put the same question two ways -- "what's unpaid on the Fenwick matter" answered by Claude improvising `curl` calls against the accounting API, against the same question answered by calling a typed `query_invoices` tool -- so the reader feels the difference an MCP server makes rather than just being told it exists
  - MCP and a connector are not the same thing to configure even though they're the same thing underneath: identical protocol, identical tools -- the only difference is how it gets switched on, a server added at the command line versus a connector ticked on inside claude.ai

- Adding one
  - Show the two add commands side by side, since the shape of the server decides which one applies: the remote form, `claude mcp add --transport http <name> <url>`, takes an address; the local form, `claude mcp add <name> -- <command>`, takes a process to launch
    - Call out what the bare `--` in the local form is actually doing: separating the server's own arguments from Claude Code's, not decoration
  - Redirect the reader's instinct before it fires: check for a server that already exists before writing one -- Sentry, Playwright and Postgres ship their own, and writing a server from scratch is rarely the first move
  - Reframe adding a `stdio` server as a trust decision rather than a convenience: it runs as a subprocess with the same file and network access the reader has, so approving one is closer to installing software than flipping a setting

- The transports
  - Lay out the two live transports against what each is for, not just what each is named: `stdio` for a subprocess on the reader's own machine, the common case for a local database or file store; `http` for a server somebody else runs, such as a document portal's own service
    - Example: show which fields belong to which transport by setting a `stdio` entry with its `command` field beside an `http` entry with its `url` field
  - `sse` is deprecated -- dispose of it in a line, not a real third choice
  - Do not explain the protocol running underneath either transport -- the reader needs to know which one to type when adding a server, nothing more

- Scopes and where they live
  - Lay out the three scopes by reach: `local` (this project only), `project` (the whole team, every clone), `user` (every project the reader opens)
  - The names don't sort the way the reader would guess where they live on disk: `local` and `user` both sit inside `~/.claude.json`, while `project` sits in `.mcp.json` at the repo root -- the one file that travels with the code itself
    - Pin down which file a given server actually depends on with a concrete pair: a committed `.mcp.json` holding a project-scoped server next to a `~/.claude.json` holding a `local` entry for a different server
  - Correct a reasonable-but-wrong guess with both traps named directly: MCP servers are never configured in `.claude/settings.json` alongside everything else, and `~/.claude/mcp.json` is never read no matter how plausible that path looks
  - The decision rule the reader actually needs: `project` scope for a server the whole team should get on every clone, `local` scope for one only this checkout should keep

- Authentication
  - Order the three methods by what survives running unattended, not by how they're configured, and keep that order: a static header, then OAuth, then `headersHelper`
  - Present the static header as the weak case: point out that a `headers.Authorization` value never refreshes itself, so rotating it is a manual chore -- fine for a session run by hand, a liability for one left running overnight
  - OAuth mostly solves the overnight problem on its own: it refreshes its own token and retries once on a `401`, which covers most unattended running without anyone intervening
  - Frame `headersHelper` as the escape hatch neither of the first two reaches: describe it as a command run fresh on every connection, printing headers with no caching, and name it as the route into Kerberos and internal SSO
    - Its two costs arrive together and should be named together: it gets ten seconds to run, and it executes arbitrary shell, so it belongs only in a folder the reader trusts completely
  - Example: run the escalation side by side -- a static `Authorization` header rotated by hand every few weeks, an OAuth token refreshing itself unattended overnight, and a `headersHelper` script minting a fresh Kerberos ticket on every single connection

- Tool search and output limits
  - Tool search is on by default and it's what makes a dozen servers affordable at session start: only names and instructions load, full schemas wait until a tool is actually called
  - Do not explain how tool search ranks or matches tool names to a request -- the default behaves correctly, and the reader only needs to know that schemas load lazily
  - Present `ENABLE_TOOL_SEARCH=false` as a reversal, not a tweak: tell the reader that setting it loads every schema upfront again, trading the startup saving back out
  - Set `MAX_MCP_OUTPUT_TOKENS` apart from the setting above it before the numbers land: it caps a single call, not the whole session -- 25,000 tokens by default, with a warning firing at 10,000
    - Example: a document-store server returning two hundred filings is worth showing in full, and clears the warning threshold long before it gets anywhere near the cap -- giving the reader a felt sense of scale rather than two bare numbers

- Timeouts
  - Four separate clocks govern an MCP call, not one -- open with that plurality, since it's exactly why a job hung at midnight resists diagnosis by feel alone
  - Walk the four in the order a call actually meets them: `MCP_TIMEOUT` bounds startup, 30 seconds by default; the per-server `timeout`, set in milliseconds, bounds the call as a whole; a 60-second per-request timer sits on top of that for HTTP servers specifically; an idle timeout closes the connection after silence -- five minutes remote, thirty minutes local
  - Reframe the four as a diagnostic table rather than a list of numbers: a hang before anything runs points to `MCP_TIMEOUT`, a call that starts and then stalls points to the per-server `timeout` or the HTTP timer, silence that only begins after replies were already arriving points to the idle timeout
    - Example: carry one failure through that table -- a Companies House filings lookup that returns nothing at 06:00 -- check whether it ever started, then how long the call ran, then how long since the last reply, to land on which of the four clocks actually fired

- MCPs in unattended sessions
  - Start from the normal case as the baseline: a project-scoped server in `.mcp.json` ordinarily stops and asks for approval before it loads
  - Under `claude -p`, inside an SDK session, or in a cloud session, there's no one to answer that prompt -- say plainly that the server loads unasked rather than being refused
    - Example: a server committed to a matters repo's `.mcp.json` loading itself into a 06:00 intake run with nobody at the keyboard -- the approval step doesn't fail closed, it simply doesn't happen
  - The security consequence deserves its own line, not a footnote: anyone with commit access to that repo can get a server run unattended, which makes `.mcp.json` worth reviewing the way code is reviewed
  - Present two controls that push back against that: `disabledMcpjsonServers` to exclude one named server, `--setting-sources` to cut project settings off entirely
  - Managed MCP sits above both, for the reader who needs it: a `managed-mcp.json` placed in a system directory, fixing what may load regardless of what any individual project asks for

- Driving a browser headlessly
  - Headless buys the run its stage before it costs anything: the Playwright MCP server renders a page into memory with no display attached, which is why it can sit on a rented Linux box instead of needing a desktop
  - With nothing visible, a login page or a CAPTCHA that a person could solve in a normal browser becomes a silent hang instead -- name that as the specific failure headless creates, not a vague downside
  - A page plain enough to run unwatched needs a stable form and no login -- draw that eligibility line precisely
    - Example: a court portal sitting behind a sign-in fails it and belongs to Chrome control instead, while something like an internal filings index with a fixed form and no login is exactly the shape headless can run

- When an MCP breaks
  - Open with the single most common failure and state it plainly: a JSON entry with a `url` but no `type` gets skipped outright, with no error and nothing on the menu to explain why
    - Example: a document-store server missing its `type` field the morning after an edit, its tools gone from the list, set directly against the one-line correction -- naming it explicitly as `"type": "http"` or `"type": "stdio"`
  - Give the reader one move to make first whenever a server seems to have vanished: run `claude mcp list` from outside a session, or `/mcp` from inside one
  - Do not let an empty tool list read as one clear cause -- it can mean a server that failed to start, a server that was never configured, or tool search simply deferring the schemas until a tool gets called: three different causes behind one identical blank menu

### Browser and Screen Control

- What Chrome control is
  - Define Chrome control precisely before anything else: it is a browser extension attached to a visible window, carrying out the same clicks, typing and scrolling a person would do by hand -- not a script reading the page's underlying data
  - Name the two shapes of site it exists for, since both defeat Bash and an ordinary MCP server
    - A portal locked behind a login screen
    - A page that stays blank until its own JavaScript finishes drawing it
    - Show why each defeats a plain fetch: a login wall hands back a sign-in page instead of content, and a JavaScript-heavy page hands back markup with nothing rendered in it yet
  - Anchor the JavaScript case in the idiom rather than leaving it abstract: a legal-aid means-test portal that shows an empty screen until its script populates the form -- Chrome control has to wait for that render to finish before there is a field worth filling
  - Draw the line to computer use immediately, since the two get confused: Chrome control only ever reaches inside the browser tab, while computer use reaches the whole screen, the keyboard, and every other window on it -- leave the detail on computer use for its own article ahead
  - Contrast it with the headless Playwright MCP server covered earlier in the pipeline: that one renders in memory with nobody watching and fails silently at a login page; Chrome control exists for the opposite reason -- a visible window, because the sites it targets are exactly the ones where a stuck login or a CAPTCHA needs a human eye on it

- The browser's own login
  - State the mechanism plainly: Chrome control rides the browser's own login state, so whatever session is already sitting in that window is what Claude uses -- it never receives, stores or needs a credential of its own
  - Contrast that against curl or an MCP server reaching the same signed-in service: those need an API key, a token or a service account handed to them, and a site that issues none of those is closed to them entirely
  - Give the case that makes the reason concrete: a solicitor's Chrome already signed into a county court's e-filing portal, one tab open beside a dozen others -- Claude reaches that same live session rather than being handed a password to log in fresh
    - Note what this buys beyond convenience: no credential to rotate, revoke or leak, because none was ever created in the first place
  - Warn about the flip side in the same breath: Claude sees whatever that login can see, no more and no less -- if the portal shows every matter on the solicitor's own account, so does Claude

- The portal with no API
  - Set the scope first: this is for the portal that is both behind a login and has no API at all -- true of most court and government systems, which is why the case comes up constantly in this line of work
  - Walk the mechanics in order: the page renders nothing until its JavaScript finishes, Chrome control fills the form field by field rather than posting a bundle of data in one shot, and only then submits
  - Make the recording problem explicit before the example: a filing confirmation that exists only as text drawn on screen has no API to hand it back through, so a screenshot is the only record there is to keep
    - Show it end to end: a probate registry accepts a submission and returns nothing but an on-screen "Application received" banner -- the screenshot of that banner is what goes in the matter file, not a returned receipt
  - Note what "watchable" buys operationally: the window runs in real time rather than headless, so a stuck submission is visible as it happens rather than discovered later as a silent hang
  - Specify where control hands back to a person, and why: at a login prompt or a CAPTCHA, both places Chrome control cannot get past on its own
  - Lay out the permission split precisely, because it is not all-or-nothing
    - Reading, searching and taking screenshots pass without a prompt, even in plan mode
    - Clicking, typing and navigating each ask first, every time

- Computer use
  - Define its purpose narrowly: computer use is for a native application with no other way in -- a desktop e-filing client, a case-management program with neither a browser nor an API -- and it belongs here only after an MCP server, Bash and Chrome control have each already failed
  - Order the four constraints as a checklist, since each one has cut off a real session and none should be compressed away
    - Platform: macOS and Windows only
    - Plan: Pro or Max only
    - Scope: approval is granted per application, per session -- it does not carry over to the next app or the next day
    - Concurrency: only one session machine-wide may hold control at a time, so a second session reaching for it finds the desktop already claimed
  - State the unattended-run consequence on its own, since it is easy to miss inside a list of constraints: computer use is unavailable under `-p`, so no unattended run -- no cron job, no overnight intake -- can ever reach it
    - Give the concrete failure this produces: a scheduled matter-intake job that would need to click through a case-management program's desktop client simply cannot be built this way; it needs a person at the keyboard, or a different tool higher up the ladder
  - Cover the two remaining operational details together, since both concern losing track of the run: Escape aborts a run already in progress, and the terminal itself is hidden from the screenshots computer use takes -- a command typed to check on it will never appear in what Claude sees
  - Close by tying it back to the ladder that governs when to reach for this at all, without repeating that ladder's detail here: this is the tool of last resort, reserved for what nothing behind an API or a browser can touch

- Reach for these last
  - Lay out the ladder in order and say plainly that it is sequential, not a menu: MCP server first, then Bash, then Chrome control, then computer use -- each rung is tried only once the one before it has actually failed, not skipped because it looks easier
  - Justify the ordering rather than just stating it: an API is faster and cheaper to call, and it keeps working when a page redesign moves a button that screen control would have clicked -- reasons enough to always try it before touching a screen at all
  - Walk one matter through all four rungs so the ordering reads as a decision, not a rule to memorize: a costs-assessment lookup starts as an API call, fails because no server exists for that portal, drops to a Bash script scraping the page, fails again because the page needs a signed-in session, moves to Chrome control, and only reaches computer use if the assessment tool turns out to be a desktop program with no browser front end at all
  - Restate the last-resort framing as a refusal, not a preference: screen control is not to be reached for because it is simpler to describe to Claude -- it is for when nothing behind the screen can be reached any other way, full stop

### Connectors

- What a connector is
  - Define a connector against the MCP servers already covered rather than from scratch: it's the same kind of server, just one somebody else runs, switched on with a tick at `claude.ai/customize/connectors` instead of a line added at the command line
  - State what's identical and what differs, since the temptation is to treat it as a different technology underneath: same protocol, same tools once it's loaded -- what changes is a shorter install, and the fact that no config file in any repo is ever touched
  - Explain the transport and the authorisation together, since one causes the other: being remote makes it HTTP, and Anthropic handling the authorisation is what lets it reach services that would otherwise refuse a local OAuth round trip
    - Name the four that come up most: Gmail, Google Calendar, Microsoft 365, Slack
  - Give each of those four its own working case rather than a bare list, since each solves a different daily problem
    - The calendar connector answers whether a hearing is listed for a given date
    - Gmail pulls a client's email thread straight into the session
    - A shared Drive folder's documents become readable without a download step
    - An overnight run's result posts itself to Slack rather than sitting in a transcript nobody opens

- Turning one on
  - State the action precisely: turning a connector on is a single tick made at `claude.ai/customize/connectors` -- not an install, and not an edit to any file in any repo
  - Do not let the MCP-server model stand: this is not scoped to a project the way `.mcp.json` is -- the tick is made once per account, and every session that account opens afterward, in any repo, sees it already there
  - Carry that through a concrete case: the reader ticks the Google Drive connector on once from their account settings while working a Harrow matter, then weeks later opens a session for an unrelated Bellweather matter and finds the connector simply present with no setup step -- state both the one-time enabling click and the later session where it just shows up

- The subscription condition
  - State the condition as a gate, not a preference: connectors load only when the session is signed in with a claude.ai subscription -- nothing about the connector itself changes when that's missing, the whole category simply doesn't appear
  - List every path that fails the gate, because each looks like ordinary configuration rather than a connector problem: an `ANTHROPIC_API_KEY` set in the environment, an `apiKeyHelper`, a `claude setup-token` token, or running through Bedrock, Vertex or Foundry -- any one of these kills the connector list silently, with no warning and no error to explain why it's empty
  - Give the case that makes the silence dangerous: an overnight matter-intake job authenticated with an `ANTHROPIC_API_KEY` for cost reasons runs clean all night, never touching the calendar connector it was meant to check, and nobody sees an error because there wasn't one
  - Distinguish a second failure mode from the first, since it looks identical but fixes differently: connectors also ride the claude.ai session token itself, so a subscription that's otherwise fine but has simply lapsed makes the connector report itself rejected rather than absent
  - Close on the unattended consequence, because it's the one that catches people out: re-authorising the connector does not mend a lapsed login -- a person has to renew the login itself, which is exactly the step an unattended job cannot perform on its own

- Precedence
  - State the precedence rule plainly: a server configured locally wins over a connector reaching the same endpoint, and it wins automatically -- nothing needs to be unticked first
  - Correct the natural guess about how the match is made: it's the endpoint URL being compared, not the name given to either one -- a solicitor renaming a locally configured Gmail server to something else entirely changes nothing about which one Claude actually calls
  - Land the rule with one case: a firm with a Gmail server configured locally and the equivalent connector switched on against the same endpoint -- say which one Claude actually reaches

### Channels

- What a channel is
  - Define a channel as an MCP server that pushes events into a running session, rather than waiting to be called, and keep the server mechanics to a clause, not a paragraph -- the reader already met servers, transports and scopes two articles back
  - Set the contrast up front, before the definition settles: a channel is the one integration in this whole run that reaches in, where MCPs, connectors and Chrome control all wait for Claude to reach out first -- a reader arriving straight from Connectors will otherwise assume "channel" is just another way to reach a service
  - Show three arrivals landing on a session nobody is watching, and what each one does to it: a case-management webhook flipping a matter's status, a text message redirecting a job already underway, and a permission approval granted from a phone on a train

- The channels there are
  - List the channels that ship as plugins: Telegram, Discord, iMessage, a webhook receiver, and a browser demo kept for testing
  - Devote the most weight to the webhook receiver, not the plugin roster -- it's the one a firm is most likely to actually wire up, since it needs no waiting on a shipped integration and no SDK opened
    - Walk one occurrence through it end to end: the case-management system's own outbound webhook pointed at the local port, one status change arriving as a POST, and the session already open acting on it before anyone checks the queue
  - Note in passing that a firm not served by any shipped plugin can build its own with the ordinary MCP SDK -- this is the fallback, not the first move
  - State the account requirement plainly: a channel needs an Anthropic login, not Bedrock, Vertex or Foundry, and it is blocked by default on Team and Enterprise until an owner turns it on
  - Get ahead of what a reader will likely assume here: Slack is not on this list -- it is a separate integration that opens its own new cloud session, not a channel pushing into the one already running

- Switching one on
  - Walk through turning one on end to end: install it as a plugin, watch its token land in `~/.claude/channels/<name>/.env`, then switch it on for that session by naming it on the command line
    - Show the actual command and what confirms it worked: `claude --channels plugin:telegram@claude-plugins-official`, followed by the channel announcing itself as connected in the session's own startup output -- that line is the only confirmation there is
  - Warn against the natural mistake before it happens: listing the channel in `.mcp.json` does nothing by itself, because switching on happens at the command line, not in a config file -- don't let the reader assume the two config surfaces are interchangeable
  - Establish the scope of "on" precisely: events arrive only while a local session sits open -- not the web, not the desktop app, not Remote Control
  - Draw out what "always-on" costs in practice, since the reader will not compute it unprompted: a paralegal wanting a Telegram alert on every filed matter has to leave a session parked in tmux, or a `claude -p` worker running, for the whole working day -- not just open it when she happens to check

- Two-way and the permission relay
  - Draw the one-way/two-way line before anything else, since everything after depends on which side of it a given channel falls: two-way requires the channel to offer its own reply tool, and not every channel does
  - Treat the permission relay as the reason two-way is worth having, not as a separate feature: the same approval prompt surfaces in the terminal and on the phone at once, and whichever is answered first is the one that counts
    - Carry through the scenario that makes the relay concrete: a paralegal approving a filing from her phone on the way out of a hearing beats a terminal sitting untouched back at the office

- Gating the sender
  - Give the rule before the reason, since the reason is what makes it stick: gate a channel on the sender's own ID, never on the room it arrives in
    - Trace why the room fails as a boundary, one step at a time
      - A Telegram group or Discord channel is reachable by anyone added to it, not only the paralegal it was set up for
      - Anyone who can reach it can put text in front of Claude, indistinguishable at the transport layer from the person it was meant for
      - Gating on the room polices who can find the door, not who is allowed to knock -- the two are not the same check
  - Carry the same rule to the webhook receiver without treating it as a separate case: gate on which system sent the POST, not on which port it landed on
  - Name what an ungated channel actually is, without softening it: a prompt-injection hole with an address attached

### Deep Links

- What a deep link is
  - Define a deep link as a URL that opens a new terminal window with a prompt already typed into it, under the scheme `claude-cli://open`
    - Name its three parameters and what each supplies: `q` the prompt text, `cwd` the absolute working directory to open it in, `repo` a GitHub slug resolved against clones already known
    - Show one fully assembled rather than merely described: a link naming the matters repo and a prompt asking after a specific hearing, with the scheme, the parameters and the encoding sitting together on the page instead of separated in the abstract
  - Show three different jobs the one shape can do, without spending equal words on each: an alert that opens straight onto whatever broke, a runbook rewritten as links a paralegal clicks instead of paragraphs she copies by hand, and a dashboard row that turns into an investigation in one click
  - Draw the line firmly: a deep link never runs on its own -- the prompt lands in the box, and a person still has to press Enter
    - Point out the safeguard that enforces it: a warning that the prompt arrived from an external link stays on screen until they do, because the pause is the point, not an oversight

- Firing one
  - Note that firing one needs nothing special, and say so plainly so the reader doesn't over-build: anywhere the OS can open a URL -- `open`, `xdg-open`, `start` -- a script can construct and fire a deep link on its own, no library required
    - Sketch the shape worth drawing out: an intake-queue monitor that notices a matter has stalled and prints its own deep link into the notification it sends, so clicking the alert lands a session directly on that matter, no queue to search through first
  - Cover the registration mechanics only far enough to explain the setting: the handler registers itself the first time an interactive session opens one, and `disableDeepLinkRegistration` turns that off for machines that shouldn't register it at all
  - Flag the one place this breaks silently, since it will otherwise surface as a support question: a site that strips schemes, GitHub's own Markdown among them, renders the link as inert plain text -- keep it inside a code block so it stays copyable

### Credentials

- Where keys should live
  - Frame the scale of the problem before the rule, so the rule lands as a solution rather than an abstraction: a dozen services integrated means a dozen credentials, and every place one sits out in the open is a liability waiting to be found
  - State the rule everything below leans on, in one line the reader can hold onto: fetch a key at the moment of use, never store it everywhere it might be needed
    - Show two situations the rule actually solves, chosen because they fail in opposite ways without it: a 3am filing job that needs a key with nobody awake to type a password into it, and a shared database password rotated once instead of hunted down and edited into six different scripts
  - Add the consequence that outlives the running system, since it's the one a reader is least likely to have considered: a key stored inside the repo is still there the day that repo gets shared with a client or handed to a new hire

- The keychain, direnv and password managers
  - Order the options along one axis, not as a flat list: how many things need to share the same secret
    - One machine, one key: the OS keychain -- Keychain on macOS, Secret Service or `pass` on Linux
      - Refuse the temptation to explain how the OS keychain encrypts things at rest -- the reader needs to know it exists and how to ask it for a secret, not how it works inside
    - One project: a `.env` file loaded by `direnv`, kept out of version control
      - Note the failure this tier is built to prevent: a `.env` committed by mistake once a project reaches its second contributor
    - Many consumers sharing one secret: HashiCorp Vault or a cloud provider's own secret manager
      - Name the point at which a firm should move up from `.env` to this tier: the moment a second script, on a second machine, needs the same secret
  - Note the shortcut for a firm already running a password manager: its CLI reaches the same vault -- Bitwarden or 1Password, nothing new to install or run
  - Show the pattern a script should follow, as a worked call rather than a description of one: a keychain lookup by name on the command line, and the value it returns handed straight to the next command rather than printed or saved
    - Picture a firm's three keys -- Telegram, the case-management API, the email provider -- sitting in that one keychain, against the alternative of three `.env` files scattered across three project folders, each one another place to lose track of

- Keys and the transcript
  - Name the three ordinary ways a secret ends up in the transcript anyway: pasted straight into the chat, loaded into context from a `.env` file, or typed out on a command line Claude ran
  - Dispel the instinct to treat this as a carelessness problem: a transcript is a JSONL file that outlives the terminal it came from, so a secret written into it once does not vanish when the session closes
  - Give the wrong way first, since it is the one every reader will try: a paralegal pastes the case-management API key into the chat so Claude can "just use it," and now that key sits in a plaintext file on disk for as long as the transcript is kept, findable by anyone with a reason to grep for it
  - Set the right way against it: a script fetches the key itself and calls the API directly, so Claude sees only the result that comes back, never the credential that produced it
  - Land the fix as timing, not vigilance: no amount of care with the paste fixes this -- only moving the fetch to the point of use does

- apiKeyHelper and sandbox credentials
  - Grade any credential mechanism on one test: does it survive running unattended, with nobody there to renew it
    - Point back to MCP's own authentication ladder as the same test already made once: a static header needs rotating by hand, OAuth refreshes its own token, and `headersHelper` prints fresh headers on every connection -- a pasted or hardcoded key fails for the same reason a static header does
  - Introduce `apiKeyHelper` as Claude Code's own answer, and show why by contrast rather than by naming it: a settings file with a key sitting in it as a literal string, next to an `apiKeyHelper` line naming a command whose output arrives fresh at connection time -- only one of the two has anything for a leak to find
  - Introduce `sandbox.credentials` alongside it as a different answer to a related problem, and say plainly where it stops: it denies or masks credentials from a sandboxed process entirely, so that process runs without ever holding the value -- it protects against the process, not against whoever already has the settings file
  - Close on what both share: neither leaves a key sitting in a settings file or a process environment for something else to read later

## Databases

### Why Database Anything

- What a database is
  - Draw the line between a folder and a database: a folder answers only "what files are here"; a database answers questions about what's inside them
    - Show "which matters have an unbilled hearing due in the next fourteen days" asked of a folder listing -- it can't answer that -- then asked against a database, where it's a single query
  - State plainly that a database stores claims, not verified facts: writing a deadline into a table doesn't make that deadline correct, any more than writing it on a sticky note does
    - A row can be wrong the same way a person can be wrong; the database just remembers what it was told
  - Note that "database" doesn't mean rows and columns specifically -- documents, key-value pairs, graphs and time-stamped readings are all databases too, each suited to a different question, and each gets its own article later in this part

- Why put your own files in one
  - Explain that putting a file "into" a database doesn't mean moving it: the document stays exactly where it sits on disk, and the database just adds a row describing it -- what it is, which matter it belongs to, and its path
  - Contrast the before and after directly: show the request "find every noncompete sent to a New Jersey client since 2023" first as a task that means opening every matter folder by hand, then as one query answered as soon as it's typed, because the rows already exist
  - Flag the failure mode that has no symptom: a document nobody ever gave a row to is invisible to every query that follows -- not a wrong answer, not an error, just silent absence from a result that looks complete

- SQLite first
  - State the default plainly: reach for SQLite first, and move to Postgres only once a second machine or person needs to touch the same data at the same time
    - Name what "one file, no server" buys in practice: nothing to install, since SQLite already ships inside Python
    - Show the whole setup as one line: `sqlite3 matters.db` creates the database; deleting that file removes it completely, with no server to stop and nothing to uninstall
    - Warn against reaching for Postgres before that point: it means running a server for a benefit nobody is using yet
  - Direct the reader on how to start a new database honestly: don't design tables first -- name the questions the database has to answer, and hand those to Claude to design the tables from, not the other way round
    - Carry one example through: the question "list every client with more than two open matters" is enough for Claude to propose `clients` and `matters` tables and the link between them, before a single table is drawn by hand

### Relational

- Relational databases
  - Explain the core relational idea: rows carry named columns, and a row can link to rows in another table -- and that link is precisely what a folder of files can never hold
    - Draw a `matters` row branching to one `clients` row and many `documents` rows, and walk a single query across both links: starting from a client, reaching every one of their matters, reaching every document filed under each
  - Note why relational tends to be the default for a firm's core data specifically: matters, clients and invoices already come as fixed-field records, so relational is usually the shape already sitting there, not one imposed on the data
  - Warn that the convenience has a later cost: changing what a link points to, or what it's allowed to mean, means migrating every row that used it -- unlike adding a plain column, which touches nothing that already exists

- PostgreSQL
  - Contrast Postgres directly against SQLite: it's the step up once "one file, no server" stops being enough, because a second machine, person or automation now needs to reach the same data at the same time
    - Carry a concrete trigger for that step: a hearing-reminder automation and the intake skill both writing to the same matters table at the same moment -- something a single file tolerates poorly and a server is built for
  - Spell out what actually changes once it's a server instead of a file: something has to start it, keep it running, and decide who is allowed to connect -- none of which a file ever required
  - Name forward what's coming: Postgres handles JSON, full-text search and vector search natively, which covers three of the database families this part goes on to introduce separately -- a firm already running Postgres may already have those, without adding anything
  - Warn against reading a stopped server as a locked file: a stopped Postgres instance isn't a slower version of the database, it's no database at all until it's started again

- DuckDB and the others
  - Frame the first four as inherited, not chosen: nobody sets out to install MySQL, MariaDB, SQL Server or Oracle for a new project -- they show up already running underneath something else
    - MySQL and its fork MariaDB are older and hugely deployed, mostly sitting behind an existing website
    - SQL Server and Oracle are commercial and licensed, arriving as part of a case-management system a firm already bought, not a choice made from scratch
  - Set DuckDB apart from that list: it has SQLite's shape -- one file, no server -- but reads data column by column rather than row by row, which the columnar family later in this part covers in full
  - Demonstrate what that buys immediately: DuckDB queries CSV and Parquet files directly, right where they already sit on disk, with no import step first
    - Show a folder of a year's monthly billing CSVs queried straight through for "total billed per client this quarter" -- nothing copied, nothing loaded, nothing set up beforehand

### The Other Kinds

- Document databases
  - Explain the shape that sets these apart: a document database holds JSON blobs of varying shape, with no fixed columns, so two records of the same kind don't have to carry the same fields
  - Pin down when that's actually needed rather than merely available: scraped or API data whose shape isn't settled yet
    - Walk through a scraped court listing where one hearing's record has a room number and the next simply doesn't -- both are valid records, and a fixed-column table would have rejected one of them
    - Warn about the failure this shape allows: a typo in a field name doesn't raise an error, it silently becomes a brand-new field that nothing ever queries, sitting there unnoticed
  - Redirect before naming any product: a `jsonb` column in Postgres, or a plain JSON column in SQLite, covers this without installing a dedicated document database at all
  - Name the standalone options only as the ceiling, not the starting point: MongoDB, CouchDB, and the hosted Firestore and DynamoDB, worth reaching for only once a `jsonb` or JSON column has actually been outgrown

- Key-value stores
  - Define the shape tightly before naming anything: one value per key and nothing else -- no columns, no relations, no query language, just a fast lookup, working as a notepad that survives between runs
  - Ground that shape in the jobs it actually does for a firm, not as one example but several, since the same shape covers all of them:
    - Show an archiver checking a message ID before reprocessing it -- "seen this key before?" -- running every ten minutes and skipping anything it already has an entry for
    - A cached API answer not worth the cost of asking for twice
    - A "job already running" flag, or a running count of how many times something happened today
  - Flag the gotcha before it bites: nothing expires on its own -- a key lives forever unless the code that wrote it also set when it should die
  - State the default path plainly: a two-column SQLite table on one machine, installing nothing at all; a dedicated store only earns its place once several separate processes need to share that same notepad at the same time
  - Name the rest for recognition only, not as a shopping list: Redis and its open fork Valkey, Memcached, the embedded LMDB and RocksDB, and etcd and Consul for machines agreeing on shared settings

- Columnar databases
  - Explain the mechanical trick behind "columnar": it reads only the columns a query actually asks for, instead of fetching every row whole
    - Contrast the two access patterns directly: row-wise touches every cell in a row it reads; column-wise touches only the three columns a query names, and nothing else
    - Run the same contrast in numbers: "total billed per client per month for three years" and "which of 400,000 log lines are errors, grouped by hour" both come back roughly a hundred times faster columnar than relational
  - Undercut the temptation to switch everything over: a columnar database is bad at the opposite question -- fetching one matter's whole record -- which is what most working days actually ask for
  - State when it earns its place instead of being adopted by default: once reporting across the whole archive starts getting asked for, not before
  - Name what that means in practice: DuckDB is the one that matters for a single practice; ClickHouse and hosted warehouses like BigQuery or Snowflake are for scale a firm this size won't reach

- Graph databases
  - Explain the inversion at the heart of a graph database: it stores the connections as the primary thing, not the records at either end
    - Build the example around a conflict-of-interest check: walk the ownership chain of a named client, say Meridian Holdings, out four steps through shell companies and directorships to find who else the firm already represents -- the graph answers that walk directly, while the same question against the relational database chases a fresh join for every step, and the cost climbs with each one
  - Keep the use cases narrow and named, because they are narrow: corporate ownership chains, conflict-of-interest checks across a client base, family relationships inside an immigration matter -- not a general substitute for the relational database already in place
  - Say plainly that most practices don't need one: SQLite's own recursive queries reach as far as most client bases will ever require
  - Name Neo4j, Kuzu and Memgraph only as what's past that ceiling, not as a starting point

- Time-series databases
  - Explain the shape: a time-series database stores the same measurement taken over and over, each stamped with when, and is built to throw away fine-grained old detail while keeping summaries
  - Ground it in the one use case worth naming here: tracking what a running automation costs per day, how long each run takes, or a rate drifting over months
    - Show what that looks like at its simplest: a timestamp column next to a cost column, queried for "average run time over the last thirty days" -- no dedicated database in sight
  - Be blunt about the default: a SQLite table with a timestamp column covers most of this, and a dedicated time-series database is rarely needed for a single practice

### Search

- Full-text search
  - Start from what the reader already has: `grep` matches only exactly what was typed, scanning every file every time -- nothing prebuilt, so nothing about it is broken, but nothing about it is fast either
  - Contrast that with what a built index buys: it's built once, answers instantly, and comes back ranked best-match-first instead of in file order
    - Show stemming doing real work: a search for "filing" also catches "filed" and "files" without asking for each spelling separately
    - Run one search two ways to make the difference visible -- through `grep`, and through the index -- and show the index coming back ranked, against `grep`'s flat list in file order
  - Name the defaults before any standalone engine: SQLite FTS5 needs nothing installed; Postgres `tsvector` does the same job for an archive already living in Postgres -- a dedicated engine like Tantivy, Meilisearch or Elasticsearch earns its place only once both of those are outgrown
  - Warn that an index has a memory, not a pulse: one built on Monday doesn't know about Tuesday's filings, and it goes stale silently -- a confident empty result, never an error

- Vector search
  - Open by contrasting this directly with full-text search: full-text finds "termination" as a literal word; vector search finds the clause that means the same thing even when that word never appears in it
    - Note the mechanism just enough to make the result trustworthy rather than magic: an embedding model turns each document into a list of numbers, and documents with similar meaning land near each other in that space
    - Sketch documents as points in that space, with the liability-cap clause and the early-termination clause sitting close together despite sharing no words
    - Show a contract-archive search that surfaces the liability cap, or the early-termination passage, with neither found by matching the search term itself
  - Name the defaults: `sqlite-vec` adds this to SQLite as an extension, `pgvector` does the same for Postgres; standalone options like Chroma, Qdrant and LanceDB are for an archive that has outgrown an extension bolted onto a database already there
  - Warn hard about one trap: changing the embedding model breaks every vector already stored, so a firm that switches providers isn't re-embedding just the new contracts -- it's re-embedding the whole archive, years of it included

- Retrieval in practice
  - State the constraint retrieval exists to solve: no model can be handed a firm's whole archive at once, so retrieval's only job is finding the handful of relevant passages and handing over just those
  - Contrast full-text and vector as answering different questions rather than competing for the same one: "every letter using the word 'forfeiture'" needs the word; "the clause about ending it early" needs the meaning -- a working setup usually runs both together, not one instead of the other
  - Warn about the trap that has no visible symptom: an answer built on the wrong six passages reads exactly as confident as one built on the right six, because nothing in the reply signals that retrieval picked badly
    - Show two answers side by side that read identically fluent, one resting on the passages that actually answer the question and one resting on six that don't, so the only way to tell them apart is checking what was actually retrieved

### With the Harness

- Getting your material in
  - Name the mess before proposing order: material arrives as scanner PDFs, DOCX from clients, email attachments and case-management exports -- not one clean format, so the pipeline has to handle all of them, never assume one
  - Break ingestion into its three steps and keep them in this order, because each depends on the one before:
    - extract: run `pdftotext` first, since it doubles as the test for whether OCR is needed -- a blank result means the document is a scan, and `tesseract` runs before anything else can happen to it
      - Walk through one ingest pass covering all three shapes at once: a clean PDF, a DOCX, and a scan with no text layer at all, ending with every one of the three searchable
    - classify: sort whatever text came out into engagement letter, pleading, invoice, and everything left over
    - record: write a row holding what the document is, which matter it belongs to, and its path on disk -- the original file itself never moves
  - Warn about the failure that produces no error at all: an import that ran OCR on a blank page writes a row with empty text and nothing to flag it
    - The fix isn't a smarter import step, it's a check run afterward: count rows against files and let the gap between the two numbers surface the ones that failed silently

- Asking questions of your own data
  - State the interaction as plainly as it works: the question gets asked in ordinary language, and Claude writes the SQL that answers it
    - Give the range in one line each, not one: "which matters have no engagement letter on file", "every letter mentioning an appeal deadline last quarter", "what did I bill Ramirez between March and June" -- a lookup, a search, and a sum, all asked the same way
  - Walk one of those questions through the pieces this whole part built, tracing where they meet on a single job instead of staying separate: "every letter mentioning an appeal deadline last quarter" needs FTS5 to find the word, sqlite-vec to catch it phrased differently, and the `matters` table to say whose record each hit belongs to
  - Close on the caveat that matters most, because it's the one with no built-in warning: a query that joins the wrong way returns a number that looks exactly as authoritative as one that joined correctly
    - The check is running the same query against a matter whose real answer is already known by hand, and comparing the two before trusting the rest

## Automatic Outputs

### Document Automation

- Document pipelines
  - Open by drawing a line for the reader before naming any tool: a document pipeline is a chain of separate command-line programs run one after another, not a library your code imports
    - Say plainly that poppler, tesseract, pandoc and LibreOffice each get invoked as external commands across the next four articles, so nothing here reads like a Python API
  - Organize the whole article around two directions of travel that structure everything after it: getting what arrives into a form Claude can read, and turning what Claude writes into a form a person can open
    - Note which of the four tools ahead mostly handle the incoming direction and which mostly handle the outgoing one, so the reader has a map before the detail starts
  - Lay out the decision that starts every pipeline: what arrived determines which command runs, not preference
    - State the mapping without solving it: `pdftotext` for text, `tesseract` for a scan, `pandoc` for a format swap, LibreOffice for an Office file -- tell the reader each branch gets its own article next
  - Walk a scenario rooted in the firm: one email lands in a matter folder with three attachments -- a text-native filed pleading, a scanned exhibit, and a DOCX cover letter -- and name which single tool would take each one, leaving how for the articles that follow
  - Correct an assumption the reader is likely to bring in: a scanned bundle and a filed, text-native PDF look identical in Preview
    - State that nothing about the icon or the thumbnail tells you which kind you have -- that gap is the reason this pipeline has to check rather than assume

- poppler and pdftotext
  - Introduce poppler as a toolkit rather than a single tool, and place `pdftotext` as just one utility inside it
    - Name at least one or two of the others by what they do, not their flag syntax: splitting a bundle apart, gluing pages back into one file, turning a page into an image -- enough that the reader knows the family exists
  - Direct the reader to make `pdftotext` the first move on anything that arrives, before reaching for anything heavier, because it costs nothing to try and answers a real question: which kind of PDF is this
  - Show the worked command and both of its outcomes side by side: run `pdftotext scan.pdf -` against a text-native filed pleading and it prints the whole document to the terminal in under a second; run the identical command against a scanned intake bundle and nothing comes back at all
    - State plainly that the empty result is not an error to troubleshoot -- it is the answer
  - Close on the handoff: empty output is the signal that hands the file to tesseract, which the next article covers -- point forward without re-explaining what tesseract does

- tesseract and OCR
  - Define tesseract against what the previous article already established: it reads the pixels of a scan and guesses text the way a person sighted-reading it would, rather than extracting a text layer that was already there
  - Order this tool correctly for the reader: it only belongs in the pipeline once `pdftotext` has already come back empty
    - Correct the tempting shortcut of running it anyway on a PDF that already has a text layer -- state plainly that this replaces good, exact text with a worse guess, it does not add anything
  - Name where this actually comes up in the firm's world: scanned exhibits, faxed correspondence, old filings that exist only as images -- nothing born digital
  - Give the sharpest example available: a poor-quality scan of a filing where OCR turns a deadline date into a confidently wrong one -- say "March 14" misread as "March 11" -- and nothing in tesseract's own output marks that line as uncertain
    - Land the point the example is for: OCR failure is silent, so a human or agent has to already know which fields are worth checking by hand

- pandoc
  - Introduce pandoc as a converter between text formats in a single command, and name the directions worth knowing: Markdown to DOCX, DOCX to Markdown, HTML to PDF
  - State the asymmetry plainly rather than as a footnote: each direction loses something different -- Markdown to DOCX drops styling, DOCX to Markdown drops tracked changes and comments entirely
  - Walk a before-and-after tied to the firm's world: opposing counsel sends a redlined engagement letter as a DOCX; it gets converted to Markdown so Claude can read the substance, then converted back to DOCX
    - Show the result of that round trip precisely: the redlines are simply gone, and nothing in the file says they were ever there
  - Draw the rule of thumb straight out of that example: a clean first draft can round-trip through pandoc without loss; anything already carrying revision marks has to stay in DOCX and go to LibreOffice or docxtpl instead -- point forward rather than repeating what those articles cover

- LibreOffice headless
  - Contrast LibreOffice headless against pandoc before describing it: this runs the real desktop suite from a script, full Office fidelity, no window and no person clicking File > Export -- not a lossy text conversion
  - Show the worked command as the whole of it: `soffice --headless --convert-to pdf letter.docx` is the entire pipeline step, and it keeps the letterhead that pandoc would strip
    - Convert the same DOCX letter to PDF twice, once through LibreOffice headless and once through pandoc, and set the two side by side as the proof: point at exactly what pandoc's version is missing
  - Extend the tool past Word: it reads XLSX too, so a billing spreadsheet goes in and a table Claude can read comes out -- name this as its own use, not a footnote to the letter case
  - Warn about the failure mode that never raises an error: fonts missing on the machine doing the conversion get substituted silently, so a document rendered on a server can look different from the one on the drafting machine, with nothing flagging the swap

### Templates

- Templating
  - Define a template sharply: boilerplate written once with holes in it, filled from data on every use
    - State the model's role narrowly, as a correction against the reader's likely assumption: it does not draft the boilerplate, it only supplies the values that go into the holes
  - Specify what stays fixed as the more important half of the definition: the boilerplate, the defined terms, the closing language never move -- only the holes do
    - Play out one concrete case to a filled sentence, spelling out the substitution itself: an engagement letter template carrying `{{client_name}}` and `{{matter_type}}` holes, filled from a single row of client intake data
  - Make the case for why this exists at all, contrasted against drafting fresh: a letter written from scratch each time lets the firm's approved wording drift a little further every run, and a template is specifically what stops that drift

- Jinja and docxtpl
  - Name the two layers without conflating them: Jinja is the general-purpose engine behind the `{{ }}` syntax itself; docxtpl is built on top of it specifically to edit a DOCX
    - State plainly that Jinja on its own never touches a Word file -- docxtpl is the part that does
  - Specify what docxtpl leaves alone as it edits the document where it stands: letterhead, styles, numbering all survive untouched
    - Set this against pandoc's format conversion from two articles back, which drops styling -- the contrast is why templating and converting are different jobs, not competing ones
  - Close on what the output actually is: a real, editable Word document, not a flattened picture of one
    - Give a short example that proves it: after docxtpl fills the letter, a reviewing partner opens it in Word and marks it up directly, exactly as they would any other draft

- Filling a form PDF
  - Define filling as a different job from templating, right from the first sentence: a form PDF such as Form N-400 already ships with named fields sitting in it before anyone touches it -- filling means writing values into fields that already exist, using `pdftk` or `pypdf`, with no layout to build
  - Give a worked example that scales past one document: an N-400's fields written from a single client's intake record, then the same script run down a whole list of applicants, one row each, rather than any of them typed by hand
  - Specify flattening as a distinct, later step: it locks the filled values into the page as fixed content, removing the fields a person could still tab through
    - Note when this matters: once a form is finalized and ready to file, not while it might still need a correction
  - Draw the sharp line the reader is most likely to cross without warning: reaching for docxtpl on a form that already has named fields is wasted work -- the previous article's tool does not belong here
  - Cover the inverse case before moving on: with no fields to start from, template the document instead, in DOCX or Typst, and convert to PDF only at the end -- point forward to Typst without repeating what it covers

- Typst and LaTeX
  - Introduce Typst and LaTeX together as a pair of typesetting engines: source text compiled into exact layout, contrasted against a word processor's manual, drag-and-click control
  - Name concretely what "layout has to be exact" means, rooted in the firm's paperwork rather than in the abstract: page breaks that fall in the right place, running headers, automatic renumbering, a bundle index, an exhibit list
  - Walk a scenario where the need is unmistakable: a multi-exhibit filing bundle where every exhibit must be tabbed, numbered, and kept correct in a table of contents even as exhibits get added or pulled at the last minute
  - Refuse the wrong reach firmly, as scope discipline rather than a footnote: a two-page engagement letter needs neither engine -- that is still docxtpl's job, from two articles back

### Artifacts

- What an artifact is
  - Define an artifact plainly and place it against what comes later: a self-contained web page a Claude Code session publishes to a private claude.ai URL, framed as the cheapest way for work to leave the terminal -- unlike a web server, nothing here needs a process left running
  - Specify the technical shape because it explains the constraints the next two articles describe: one HTML file, styles and script inlined, nothing to host separately
  - Point to a rendered example rather than a description: a published status page, an overnight run's summary, or a monthly chart, shown at its actual private URL -- specify that the example should let the reader see the destination itself, not just hear about it
  - State the access requirement precisely, since it changes who can follow along: a paid plan with a `/login` session against the Anthropic API is required, and note plainly that Bedrock, Vertex and Foundry do not support this at all
  - Give the operational detail tied to a real unattended run rather than left as a floating setting: `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` stops a headless nightly job from trying to open a browser that isn't there

- Publishing and revising
  - Lay out the publish-and-revise lifecycle in order: the first publish mints the URL; every edit and republish after that updates the same URL rather than creating a new one
    - Give the live-viewing example that makes this concrete: someone with the status page already open in a browser tab watches it change in place the moment the session republishes, with no refresh needed
  - State the versioning guarantee as reassurance, not trivia: every publish keeps its own version, so an earlier state of the page is always still there to go back to
  - Warn about the single most likely mistake with its own sentence: a later session that isn't handed the existing URL will publish a second, separate artifact instead of updating the first one
  - Set out the sharing model as one place to look rather than three scattered facts: every artifact starts private to whoever created it, on every plan
    - Pro and Max share by sending the link to anyone
    - Team and Enterprise default to organisation-only, and an owner has to flip a setting before a public link works at all

- Connectors inside an artifact
  - Tie this straight back to Integrations rather than re-teaching connectors: the connectors available inside a published page are the identical MCP connectors covered there -- nothing new, just a new place they run
  - State the mechanism precisely: they run on load, inside the viewer's own browser, using the viewer's own authorized connectors -- so the page fetches fresh data every time it opens, and the automation that originally built the page never has to run again
  - Give the contrast example that makes viewer-dependence concrete rather than abstract: the same status page URL opened by two different people -- a firm staffer whose connector to the matter database is authorized sees live figures, while a client with no connector configured opens the identical link and sees an empty page

- The content policy
  - State the policy in full rather than as a summary: everything from outside the page is blocked -- external scripts, stylesheets, fonts, images, and all outbound fetch, XHR and WebSocket traffic
  - Resolve the apparent contradiction with the previous article before the reader notices it themselves: connectors still work because they are the one channel the policy explicitly permits, not a hole in it -- a short corrective aside, not a rehash of how connectors work
  - Spell out the practical consequence plainly: anything the page needs -- a font, a chart library, an image -- has to be inlined into that single HTML file, or the page does not render at all, with no partial fallback
  - Give the hard number and treat it as a real constraint rather than trivia: sixteen megabytes is the ceiling on that one file
    - Ground it in something the reader would actually do: embedding a firm logo as a base64 image already eats a real share of that budget
  - Close by landing the definition this whole section has been building toward: being self-contained and bounded in size is what makes something an artifact rather than an ordinary web page, and it is the same cheapness the very first article in this section opened with

### Static Sites

- Static site generators
  - Define a generator against both neighbours already covered: it compiles a folder of Markdown into plain HTML once, ahead of time -- nothing kept running the way a web server later in the course needs, and no single-file ceiling the way an artifact has
  - State the portability payoff concretely rather than abstractly: the output is nothing but files, so it runs from a laptop folder, a cloud bucket, or any static host without caring which
  - Name the generators worth knowing without comparing them feature by feature: Hugo, Zola, Eleventy and MkDocs -- placing them is enough, a full comparison is not this article's job
  - Give the worked example specified by the material: `mkdocs build` run over a folder of the firm's own notes, producing a searchable internal reference complete with a search box and no server behind it -- show this as the actual deliverable, not the command in isolation
  - Give the free hosting path plainly, then immediately pair it with its hazard: the same repository holding the Markdown can serve the built site too, at no cost, through GitHub Pages -- but GitHub Pages defaults to public, so anyone holding the URL can read it, which sets up the caution the next article closes on

- Publishing what an automation makes
  - Open on the economics once the generator and the host are already set up: this route is about as cheap as automation gets, no server bill and no process to babysit -- ground it in the firm's own examples, a status page rebuilt nightly, an internal reference built from the firm's own notes, a published version of a course like this one
  - State the defining limitation as a correction the reader needs before relying on this: a static page shows only what the last build produced -- it is generated ahead of time, not served fresh on request
    - Contrast this directly against the web server section that follows, so the reader understands why a live database query cannot live here
  - Trace the full pipeline end to end as one worked example, naming what each step touches in turn: a nightly `claude -p` run rewrites a status file, the generator rebuilds the site from that file, and the client opens the same URL the next morning to this morning's position -- no new link ever needs sending
  - Close with the sharpest caution in the section, as a direct callback rather than a fresh warning: a matter status page carrying client names does not belong on public GitHub Pages -- Tailscale or an artifact instead, precisely because of the public-by-default behavior the previous article just named

## Hosting and Serving

### Web Servers

- What a web server is
  - Open by placing a web server against the artifact from the previous section: an artifact is a finished page that ships once and sits still, a web server is a process that stays running and answers each request as it arrives
    - Note the requirement that follows from this: nothing behind a web server is reachable unless something is actively listening, unlike the artifact's private URL that just exists on its own
  - State what "listening on a port" means in plain terms: the process claims a numbered address, and any request sent to that number gets routed to it
    - Show a request from a person's browser and a request from another program hitting the same port and getting different replies back -- a page for one, JSON for the other, the same listener both times
  - Position the web server as the front door for automation from this point on in the course: a form a client fills in, or a URL another service calls, is what gets a pipeline started
  - Demonstrate the lifecycle directly rather than describing it: start a small server, hit it and see the reply, stop the process, then hit it again and show the connection failing outright
    - Draw the conclusion plainly, then point forward: a server is only as reachable as the process behind it staying up, and keeping that process fronted, certified and running is the practical work still ahead

- Reverse proxies
  - Introduce the reverse proxy as the layer standing between the internet and the actual server work, forwarding only what it decides to let through
    - Contrast this with the bare server from the previous article: instead of one process answering everything itself, a request hits the proxy first, and the proxy decides where it goes next
  - Cover the three jobs a reverse proxy centralises as three separate points, not one folded sentence
    - It holds the certificate once, instead of every app behind it needing its own
    - It routes several services behind a single address out to different backends
    - It refuses traffic that was never invited before an app behind it ever sees the connection
  - Show a concrete shape carrying all three jobs at once: one address in front of an intake form on port 8080, a status page on 8081 and an admin tool on 8082, with only the proxy holding a certificate and deciding which port a request reaches
  - Warn that the hop this adds is not free, folding the consequence into the same line rather than stating it separately: when something breaks, a browser only reports the site as unreachable, so checking the proxy's own logs comes before assuming the fault sits in the app behind it

- Caddy, nginx and certificates
  - State directly what a certificate does at this layer: it turns the address into a real `https://` rather than one that trips the browser's warning
  - Set Caddy and nginx against each other rather than covering them separately: Caddy issues and renews its own certificate automatically from a couple of lines in a Caddyfile, while nginx is the more established choice and leaves certificate handling to a separate tool, `certbot`
    - Show both sides of that difference concretely: the couple of Caddyfile lines that point a name at a backend and quietly pick up a certificate for it, next to the nginx config plus the standalone `certbot` command and renewal job needed to get the same result
  - Correct an assumption a reader is likely to carry over from ordinary hosting: a certificate is issued to a name, not a machine, so replacing the hardware behind an address changes nothing, but renaming the address invalidates it
    - Tie this back to the reverse proxy from the previous article: it is the proxy holding the certificate that makes this true, since nothing behind it needs a certificate of its own

- Tunnels
  - Draw the line between Tailscale and a tunnel before going further, since both solve "don't open the machine directly to the internet" but land in different places: Tailscale keeps the machine reachable only to devices on your own network, a tunnel gives it a name anyone on the open internet can reach
    - Recall the earlier Tailscale mention -- the matter status page kept off public GitHub Pages -- and set the tunnel against it as the public-facing alternative to that private option
  - Draw both as one picture rather than two separate descriptions: the same server and the same Caddy sitting unchanged behind two different fronts, one reachable only from your own devices, the other reachable from any browser holding the tunnel's name -- what changes between the two panels is only how the machine is reached, never what answers once it is
  - State what a tunnel specifically changes relative to self-hosting a bare address: the browser connects straight to the tunnel's name with no separate hosting layer in between
  - Refuse to go further into tunnel provider mechanics here -- naming the choice and what it changes is this article's job, not comparing providers against each other

- Self-hosting
  - Define self-hosting in one clear line before its costs and conditions: the files and data sit on your own disk, no third party holds a copy, and the client's browser talks straight to your machine
  - Cover the domain name as a separate, small cost: roughly ten pounds a year, pointed at your own machine exactly as it would point at a rented one
    - Give the reason a name beats a raw address: a name is memorable where a number isn't, and a home connection's number changes under you, so the name is what stays constant
  - State the one hard condition self-hosting imposes, as a condition rather than a footnote: the machine has to stay awake, full stop, or nothing behind the name answers
  - Set out what paid hosting actually sells once the domain and the machine are covered either way: someone else's electricity, a connection that doesn't drop, and somewhere else to point blame when it does
    - Weigh that against skipping it, rather than presenting paid hosting as simply worth the money
      - Give the skippable case: a form only you depend on, where an outage costs you an evening and nobody else notices
      - Give the case where skipping it costs more than it saves: a form clients rely on daily, where the same outage costs the firm a client relationship

- A worked example — the intake form
  - Open by naming this as the section's worked example, then walk it step by step in the order a request would actually travel, rather than describing the finished result up front
  - Start at the front door: an intake form collecting a client's name, matter type, and a passport-scan upload, sitting on a machine you are self-hosting rather than a rented box
  - Move to how the request reaches that machine: Caddy in front, holding the certificate, so the form sits at a real `https://` address rather than a bare IP
  - Walk through what a single submission does the moment it lands, and be specific that it happens all at once rather than in sequence: a case folder gets created, a database row gets written, and a job lands on a queue
  - Continue to the pickup: cron finds the queued job on its own schedule, with no one watching for it
  - Finish the chain at the automation itself: `claude -p` runs with the intake skill against the new matter's data and drafts the engagement letter, so the matter is filed before anyone has opened a laptop
  - Close the walkthrough with the one plain risk this shape creates, rather than folding it into the steps above: a form that accepts uploads accepts them from strangers, not only from clients
    - Direct the fix as three concrete rules rather than a general warning: cap the upload size, check the file type before touching it, and never pass what arrives straight to a shell command

### Containers

- What a container is
  - Define a container in one line before anything else: a sealed box holding a program and everything that program needs to run
    - List what "everything it needs" means concretely: its own filesystem, its own packages, its own version of something like Python
  - Anchor the definition in a full worked sequence rather than leaving it abstract, walked as four ordered acts rather than one run-on sentence
    - Build a container running something like Postgres
    - Show that its version and its files differ from whatever the host machine has installed
    - Run that same container unchanged on a second machine
    - Delete it and show nothing survives the deletion
  - State the payoff of that sequence plainly: it runs identically on a laptop, a rented box, or a reader's own machine, and never reaches outside itself into whatever else happens to be installed there
  - Explain the mechanism that makes containers fast where a virtual machine isn't: a container shares the host's kernel instead of booting one of its own, which is also why containers are Linux-only where a virtual machine isn't
    - Connect this to a debugging habit worth adopting: running work against a clean container catches "it works here because I happen to have this installed" bugs that a laptop cluttered with old tools hides completely
  - Separate building a container from running it as two different acts, and make the distinction concrete: a container can cross-compile a Windows binary while being completely unable to open or run that binary itself
  - Add the reason this matters specifically for Claude Code, beyond portability: an agent working inside a container cannot damage the machine around it, which is a reason to reach for one even on a single laptop
  - Close by naming the tools rather than leaving them implicit: Docker is the tool that does this work, and a devcontainer is the same idea wired directly into an editor

- Images and registries
  - Explain how an image gets from a laptop to wherever it runs: it travels through a registry, Docker Hub or a cloud provider's own, pushed from one place and pulled down at the other
  - Walk through getting an image onto a rented box as three steps and nothing more: install Docker, pull the image, run it
    - Note what's conspicuously absent from that list: no separate dependency install, because everything the program needs already travelled inside the image
  - Correct a shortcut a reader might reach for: rebuilding the image on the box instead of pulling the tested one produces a different image, not a copy of it -- the thing that was tested and the thing that runs have to be the same artifact
    - Show the counter-example directly: the same tag pulled onto the box behaves identically to the one already tested locally, while rebuilding that tag on the box from source can pick up a newer base layer or a different package version, quietly producing a different image under the same name
  - Cover the architecture caveat before it causes a confusing failure: a laptop and a rented box can run different chips, so an image has to be built for the target chip, or built on the box itself rather than carried over
  - Name the services that remove the box from this picture entirely: something like Cloud Run takes the image directly and runs it, with no machine for anyone to install Docker onto in the first place

- Reproducibility
  - Pin the core claim of this article at the top so the rest reads as consequence of it: a container is a written-down recipe of every dependency, and that recipe still runs correctly in December on a machine that doesn't exist yet, having been true in March
  - Reorder the emphasis against the previous two articles: reproducibility, not containment, is why most containers get used day to day -- treat containment as a bonus sitting on top of this, not the main reason
  - Give the deployment payoff concretely: moving work to a rented server means moving the box, not reinstalling forty things onto a fresh machine by hand
  - Set the local payoff beside it without repeating the same framing: incompatible versions of the same tool can sit side by side without colliding, nothing installed inside one container survives its deletion, and trying an unfamiliar piece of software costs one command instead of a commitment
  - Close with a directed example of the scaling case a single machine can't offer: picture twenty identical containers started at once overnight, each working through its own batch of matters, and show what the next morning looks like -- twenty finished jobs, none of them having queued behind another

- Running one on a box that never sleeps
  - Position this article as the payoff of a condition already stated rather than as a new fact: self-hosting required the machine to stay awake, and this is what happens when it doesn't
    - Demonstrate why the condition matters instead of just naming it: put a laptop closed at eleven, missing whatever was scheduled for midnight, against a box that never sleeps running that same job on time
  - Name the two shapes of work that specifically need a box that never sleeps, tying each back to where the reader has already met it: a scheduled cron job like the one picking up the intake queue, and a server that has to answer whenever something like the intake form is submitted, not only while a laptop happens to be open
  - Point back to the self-hosting-versus-rented-box question rather than reopening it here, since the condition is the same one already stated there: something has to stay awake, whichever machine that turns out to be

## Agent SDK

### The SDK Harness

- What the Agent SDK is
  - Ground the reader before anything else: the SDK is the same agent loop this course has been using all along, packaged as a library called from Python or TypeScript code instead of driven from a terminal
  - Contrast the driving seat, not the machinery: the tools, the `.claude` directory, CLAUDE.md, hooks, skills and subagents all run exactly as before -- what changes is who decides when a turn starts and who reads the messages as they arrive
  - Say plainly what a terminal gave away for free that code does not: nobody is pressing Enter, so the calling program itself decides when the next turn begins
  - State the corrective this article leans on: removing the terminal removes the terminal, not the job -- sessions, permissions and cost tracking are still the developer's responsibility, just written in code instead of configured at a prompt
  - Show a permission callback mid-run, denying a write the moment it tries to land outside a client's own matter folder: a decision that used to arrive as a prompt, now resolved in code before the write ever reaches disk
  - Refuse to reopen the agent loop itself here -- it was covered earlier in the course; this article's job is only what changes when that loop is driven by a program instead of a person

- How it differs from headless sessions
  - Put the gating question before any feature list: is this a job `claude -p --output-format json` already answers, since that single line already runs Claude non-interactively from any language
  - Draw the line precisely between the two: a headless session is one shot at a final answer with nothing visible in between; the SDK is what a program reaches for when it needs to act mid-run
    - Conditional tool approval, streaming partial output, a session held open across exchanges, billing per turn -- name these as the shape of "mid-run", not as a checklist to memorise
  - Assume the reader already has piping and watching a headless run from earlier in the course -- do not re-teach either, only place the SDK on the far side of that line
  - Set a nightly OCR job that shells out to `claude -p` and exits against a paralegal's intake tool that has to keep a browser tab updated with "still working" -- pair the two so the reader can drop their own job onto one side or the other

- Use cases
  - State the shared pattern up front: someone or something is waiting on a live connection, and a headless run's blank screen for the length of the job will not hold their attention
  - Walk the intake form's back end through it end to end: a client uploads documents, the form calls the SDK, and the page updates as messages arrive instead of the browser stalling on one long request
  - Name the multi-tenant shape as the second case, pointing ahead rather than explaining it: one process running one agent per customer, each customer's files walled off from every other's, with the actual wall covered in the article on separating customers

### Building an SDK

- Running a query and holding a session
  - Frame the two entry points as a fork the reader chooses at the start, not something to discover later: one call for a single question, one object for a session held open across exchanges
  - Show `query()` concretely: pass in whether a bundle has a text layer and get back a stream of messages for that one run, nothing left open once the last message arrives
  - Name the session-holding side by language: `ClaudeSDKClient` in Python, streaming input in TypeScript -- both built for something like a paralegal's back-and-forth on one matter across several exchanges
  - Flag a capability gap directly instead of burying it: only the session-holding side can be interrupted mid-thought -- a `query()` call runs to completion once it starts

- The messages that come back
  - Dislodge the assumption a single `claude -p` call leaves behind: nothing here returns one string reply -- every run comes back as a sequence of typed messages, in a fixed order
  - Direct the writer against a type-hierarchy dump: show one message-handling loop actually unfolding, and let the four types below earn their place inside it rather than being listed as a taxonomy up front
  - Name the four types in the order they actually appear in a run
    - `SystemMessage`, subtype `init`, opens the sequence and carries the session ID
    - `AssistantMessage` marks each reply, `UserMessage` marks each tool result
    - `ResultMessage` closes the sequence, holding the cost, the tokens and the session ID
  - Define a turn precisely, since everything else in this article leans on it: one trip through assistant-then-tools, a reply followed by whatever tool calls it made
  - Explain why the typed sequence is worth knowing rather than treating it as trivia: it is what makes live status on screen, billing per turn, and a full log of what happened all possible from one stream
  - Show a `ResultMessage` being read after a turn, its cost checked against a per-matter budget cap, and point at that number as the one place the stream hands it over

- Stopping it running forever
  - The reader will go looking for a clock inside the SDK; say up front that there is none -- a session has no timeout and will not end on its own
  - Name the two limits that do exist, and be precise about what each one actually counts
    - `max_turns` counts tool-using turns only, nothing else
    - `max_budget_usd` stops on a client-side cost estimate, not a metered bill
  - State the consequence before the example: an unattended overnight run needs something watching it from outside the process, since neither limit above is a wall-clock timer
  - Keep the limit visibly outside the SDK, not something it provides on its own, by demonstrating that outside watcher two ways: `timeout 3600` wrapped around an overnight intake run, and the equivalent systemd unit

- The permission callback
  - Name the callback and its job in one line: `can_use_tool` decides whether a specific tool call proceeds, the same decision a prompt would otherwise make, now made in code
  - State what it actually receives and what it can hand back: the tool's name and its input arguments in, and one of allow, deny with a reason, or an edited version of the input, out
  - Place it precisely in the stack: it only fires when a prompt would otherwise have fired, so an allow rule resolves the call before the callback ever sees it
  - Assume the six permission modes are already familiar from earlier in the course -- direct only how the callback relates to them: it sits beneath all six, seeing whatever a given mode leaves unresolved, not what each mode itself does
  - Contrast the mechanism with a hook the reader may already know from Level Two: a hook runs as a shell command the settings file configures, while this callback runs as code inside the program itself
  - Warn the reader against over-trusting it here, not as an aside: seeing every call does not make the callback a complete security boundary, and code that assumes otherwise has a gap in it
  - Rank the deny rule above everything else in the stack, `bypassPermissions` included
    - Note in passing that `bypassPermissions` itself refuses to run as root
  - Demonstrate the ranking instead of asserting it: set a deny rule against writes outside `matters/<client>/`, then turn on `bypassPermissions` and show the same write still refused, so the reader watches the rule win rather than takes the claim on faith

- One process, many customers
  - Start from the default, since it is the trap: an SDK session loads the same `.claude` machinery Level Two built for one user -- settings, CLAUDE.md, hooks, skills, subagents -- and that default is wrong the moment one process serves more than one customer
  - Refuse to relitigate what each piece of that machinery does -- it was covered in full earlier in the course; this article's job is only the one flag and the two settings that wall customers apart
  - Give the fix its exact name: `setting_sources: []` shuts that machinery out entirely
  - Add the two settings that shutting it out alone will not cover: a separate working directory -- each customer's own matter folder -- and a separate `CLAUDE_CONFIG_DIR` per customer
    - Without both, one client's CLAUDE.md, skills or files reach another client's run
  - Show the failure before the fix: run two customers' sessions side by side sharing one working directory and one `CLAUDE_CONFIG_DIR`, let the reader watch one client's files leak into the other's run, then run the same pair with each given its own and show the leak close

- Sessions and where they live
  - State where a session actually lives by default: a JSONL file under `~/.claude/projects/`, resumable later by its ID
  - Show a resume happening, not just described: pick the Ramirez matter's thread back up a week later by its session ID, and let the reader see the whole prior exchange return, not a note that resuming is possible
  - Cover forking next to resuming, since the two get confused: a fork branches a session into a new one and leaves the original untouched -- the difference between drafting a second letter and overwriting the first
  - Tie this back to containers by name, not by gesture: the same disposability that made containers useful earlier in the course -- nothing survives being deleted -- is exactly what wipes `~/.claude/projects/` the moment a redeploy happens
    - A `SessionStore` adapter mirrors sessions to S3, Redis or Postgres instead, for a program that has to survive being rebuilt

- What it consumes
  - Correct a natural assumption up front: twenty concurrent `query()` calls are twenty separate `claude` subprocesses, not twenty threads sharing one -- the SDK does not multiplex
  - Refuse to cover what happens to those processes after they spawn -- supervising them, restarting a crashed one, pooling them across customers belongs to the deployment articles ahead, not here
  - Reckon on a gigabyte of memory, five gigabytes of disk and a full CPU core per process as the floor
  - Show it as a table, not an abstraction: the same per-process floor set against what the firm's own box actually has, so twenty concurrent matters becomes a row the reader can check before promising a client same-day turnaround
  - Separate `total_cost_usd` from a real bill: it is an estimate read off a price table compiled into the build, not a metered figure Anthropic issues
  - State the boundary of what that estimate is fit for: good enough to trip a budget cap before it is exceeded, not accurate enough to put on an invoice

### Deploying and Integrating SDKs

- The shapes a deployment takes
  - Open by naming the four shapes a deployment can take -- terminal program, web page, desktop application, phone -- and state plainly that the SDK code behind each one is the same; only the wrapper around it changes
  - Correct the reader's likely assumption up front: this is not a ladder of sophistication where the phone or the desktop app is the "best" choice -- a shape is only defensible next to who has to use it
  - Direct the choice by an audience question, not a technology question: what does the person on the other side already have open, and what do they already trust
    - Show that question answered for one colleague: the paralegal keeps a browser open all day and has never typed a command, which alone rules out a terminal and points toward a web page or a desktop app before any SDK detail gets decided
  - Give the paralegal's intake tool as the example that shows the SDK disappearing into the choice instead of announcing itself as a feature: she sees a form and a drafted letter, never a mention of Claude behind either
  - Set the shapes against each other for effort, not ambition: a finished Python TUI a colleague can use today beats a React app still three weekends from shipping
  - Close by pointing forward: each of the next four sections takes one shape and asks what it costs to build and what it still can't reach

- Behind a TUI
  - Say plainly, before showing any code: a `ClaudeSDKClient` sitting in a loop with `input()` and `print()` already counts as a shipped deployment, not a prototype waiting for a real interface
    - Show the loop itself to make the point that little separates "deployment" from "conversation": a few lines reading a matter number from `input()`, holding the session open across turns, and printing each reply as it comes back
  - Explain what that shape buys for free: no server process to keep running, no certificate to renew, no hosting bill arriving monthly -- it runs on the same machine where the matter folders already sit
  - Draw the line this shape can't cross: it reaches exactly one person, at one keyboard, in one sitting -- name the colleague who won't open a terminal as the reader this face already fails
  - Set it against the faces still to come without repeating them: it is the cheapest of the four to build and the narrowest to reach, and every section after this one trades away some of that cheapness for more reach

- Behind a web page
  - Explain the split this shape introduces: a small FastAPI or Express server holds the SDK session, and the browser holds nothing but the form -- unlike the TUI's one process doing both jobs at once
    - Point back at the intake page built in Web Servers: it's the same page, with the SDK now answering directly where a queue used to sit
  - Name the trade in one line and don't soften it: anyone who can reach the URL can use the form, and that is the whole gain over a TUI and the whole new exposure, at once
  - Say plainly what a reader will assume wrongly: a browser does not arrive with a login already attached
    - Spell out the three ways to add one anyway -- a real login, a shared secret baked into the URL, or restricting the address itself to a Tailscale network -- and that choosing none of them is choosing the first
  - Explain the file-handling consequence that follows from where the server sits: a document uploaded through the form lands on your own disk, under your own account's permissions, and the SDK then reads it directly -- a malformed upload is your machine's problem, not a sandboxed one
    - Show the same intake page set up two ways -- open on the office LAN with no gate, and the same page behind a shared secret in the URL -- to draw out that "reachable" and "reachable safely" are not the same claim

- Inside a desktop app
  - Explain what this shape actually is: Electron or Tauri wrapping the same web page from the previous section behind an icon, so a colleague launches a program instead of typing a URL -- nothing about the SDK code underneath changes
  - List what wrapping it buys against what it costs in the same breath: it stops looking like a website, but code signing on macOS, shipping an updater, and every colleague's copy drifting to a different version all become your job now, not a browser vendor's
  - Knock down the assumption the icon creates: the window makes the work look local; say plainly it isn't -- the model call still leaves the machine exactly as it did behind the web page, and whatever client document went with it leaves too
    - Before the reader can dismiss drift as theoretical, put two colleagues on the same matter on two different app versions, one still on last month's build and silently missing a fix, and follow it through to the support call it creates

- On a phone
  - State the shape plainly: the agent still runs on the box covered in the previous two sections; the phone only ever holds a page or a chat window, never the SDK itself
    - Explain what that buys on the phone's end: nothing but a browser and a connection is needed -- no install, no key to manage, no app store review
  - Order the options by cost, cheapest first: the same web page already built, just opened on a phone's browser, and cheaper again, a Telegram channel that needs no page at all
  - Name the case that actually justifies building this face, rather than treating it as a checkbox: approving a redaction from a train, where the alternative is leaving it unapproved until you're back at a desk
  - Explain the one failure this face cannot tolerate: a dropped connection must not lose the run
    - Show why it doesn't: the session lives on the box exactly as covered in Building an SDK, resumable by ID -- the phone reconnecting is all that's needed, not resuming the work itself

- Where the process actually runs
  - Lay out the three hosting choices in order of whose problem the machine becomes: your own always-on machine, a rented box, or a container on something like Cloud Run
  - Weigh the last two against each other on the axis that matters here: a rented box costs money whether or not anyone uses it that day, while a container that scales to zero costs nothing between requests -- but say plainly that scaling to zero brings a cold start the first person to submit a form has to sit through
  - Correct the obvious mistake before it gets made: a laptop that closes and sleeps is not a host, however good the code on it is -- an intake form nobody can submit at 11pm has already failed, whatever happens at 9am
  - Draw the distinction that catches people out: testing a deployment while standing over it proves nothing about whether it survives unattended
    - Give the concrete gap between those two moments: standing over it, you'd notice the box stall and restart it by hand; at 3am nobody does that, and the form just doesn't respond

- Streaming to someone waiting
  - Connect this straight back to Building an SDK: the message stream already covered there -- an `AssistantMessage` per reply, a `UserMessage` per tool result -- isn't just data, it's what actually goes on the screen while someone waits
  - State the failure a silent wait produces, concretely: a blank screen for ninety seconds reads as broken, not as thinking, and the person on the other end reloads and submits the same form twice
  - Explain what closes that gap: the tool names already arriving in the stream, turned into a status line before the tool has a result to show
    - Show the wording rule directly: a status line reads "Reading the passport scan" or "checking the matter number" because it's built off the tool call itself, not off what the call returns -- the words have to exist before the answer does
  - Flag the one case that breaks the pattern: a single long-running call, like OCR on a forty-page bundle, produces exactly one message and then nothing until it finishes
    - Direct the fix precisely: print a line before that call starts, since nothing else will arrive in the stream to trigger one partway through
  - Close with a worked walkthrough of the whole ninety seconds -- status lines landing as each tool call starts, the flat silence while OCR runs, then the printed line placed to cover exactly that silence -- so the reader watches the wait resolve instead of reading a rule about it

- Keeping it up
  - List the operational basics a deployment has to survive without you noticing: the box rebooting, the API key rotating, and one the reader won't expect -- the model version changing underneath it unannounced, because the SDK always calls the latest
  - Explain why "someone else is using this now" changes the job: it creates two needs a solo TUI never had -- a record of what happened, and a way to explain a failure to a person who isn't you
    - Show the same failure rendered two ways: a raw traceback sitting in a terminal nobody but you reads, next to the one line a paralegal would actually understand -- and say plainly that writing the second one is the actual job, not an afterthought to the first
  - Connect resuming a customer's thread next week to a decision made back in Building an SDK: the session has to outlive the machine, which means a `SessionStore` writing to Postgres or S3, not the local JSONL files under `~/.claude/projects/`
  - Separate the two costs the reader will conflate: the loud one is the model bill sitting in `total_cost_usd`, visible any time you look
    - Name the quiet one directly, since it won't show up on an invoice: a gigabyte of memory per concurrent session, and your evenings spent answering "it did not work"

### Notifications

- Notification transports
  - Define the term before naming any tool: a notification transport is how an unattended job reaches you when you're away from the machine it's running on
    - State the alternative it replaces: without one, you find out only when you next happen to check, which could be days after a run finished or failed
  - Undercut the instinct to notify on everything: a notification sent for every processed matter is, in practice, a notification nobody reads, because noise trains the reader to ignore the channel entirely
  - Set the bar for what earns a notification, as a working list rather than an exhaustive one: something failed, a document is sitting there awaiting approval, a deadline got spotted, or one matter in twelve silently failed while the other eleven went fine
  - Distinguish one-way from two-way transports as a real fork, not a detail: a two-way transport lets a decision travel back from the phone, where a one-way transport only ever reports that something happened and leaves the fix waiting for the machine
  - Use the redaction-approval case carried forward from On a phone as the concrete test of exactly what "adds the reply" removes from the workflow: a one-way transport tells you a document is waiting; a two-way one lets you approve or reject it from the same message

- Telegram, ntfy and email
  - Open with the deciding question the rest of the section answers, not a feature comparison: which of these do you already look at, not which is the most capable
  - Walk through the four options against that question, cheapest to set up first:
    - A desktop notification: the simplest of the four to wire up, and it dies at the edge of the machine -- nobody on the train sees it
    - Telegram or Discord: a bot posting into a chat you already have open, so it needs a channel you're already checking, not a new one you'll forget
    - `ntfy`: pushes straight to a phone off nothing more than a topic name -- no bot, no account, no inbox
    - Email through a provider's API: the right choice when what's needed is a record sitting in an inbox, not just a ping -- slower to notice, but it doesn't disappear once read
  - Show that the delay comes from the channel chosen, not from anything Claude did, by sending the same event two ways from the same run: an email landing at 3am and sitting unopened until 9, next to an `ntfy` push landing on the phone the same minute

- Claude Code in Slack
  - Correct the reader's likely filing of this one first: Slack does not belong on the transport list from the previous two sections -- it's not a notification channel bolted onto your own deployment, it's Anthropic's own integration, and that difference decides everything else in this section
  - Explain where the session actually runs, since the channel makes it easy to miss: `@Claude` mentioned in a channel starts a cloud session, not one on your own box or under your own SDK code -- none of the deployment shapes or hosting choices from earlier in this part apply here
  - Explain the two-way behaviour that makes it worth using at all: it narrates as it works, posting status and a summary back into the same channel as it goes, rather than staying silent until done
    - Walk a concrete run through it to show narration standing in for the log file and the translated failure message from Keeping it up: the intake skill gets a small change requested in a channel, Claude posts each step as it happens, and the thread ends with a button to open a pull request
  - State the hard limits plainly, since they'll surprise a reader used to bots that DM: channels only, never a direct message, and exactly one pull request produced per session, not an open-ended back-and-forth
  - List what has to already be true before any of this works, and where it flatly doesn't run at all: a claude.ai login, a GitHub account connected to it, and a paid plan on one side; Bedrock, Vertex and Foundry ruled out on the other
  - Close with the fact that dates this section: it's being replaced by Claude Tag on Team and Enterprise plans -- say this without implying the mechanics just covered are wasted detail, since Tag inherits the same shape


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

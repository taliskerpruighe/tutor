# TBD
- yazi
- broot
- btop
- forking
- worktrees
- rewinding
- counter recommended features
  - agent teams
  - background sessions/agent view
- remote control
- agent memory
  - can be set to user, local, or project
  - engineer like the rest: isolate
  - agents load their memory up front: divide accordingly
  - only the first 200 lines auto load, so trim
- session names/colors
- loops
- goals
- remotes
- cloud sessions
- databases
- google cloud storage
- google compute engine
- permissions
- zsh
  - glob
  - grep
  - ripgrep
  - hash d
  - variables and expanding them in cc
- rewinds
- prompt engineering
  - use control+g to build a big one
  - use headers with #, ##, ###
- forked subagents
- scoping mcps to custom agents  
- plan mode
- disabling builtin agents
- claude.md practices
- rules
- output styles
  - custom ones are worthless
- lsp's
- artifacts
- machine learning
- 

# Level 1

- ccstatusline
  - much better than the bultin stuff
  - ask cc to install and configure
  - run thru the options to see what is available
  - like a powerline, it takes any custom command
  
- readme.md and agents.md
  - will see referenced
  - because its in git repos
  - claude.md is basically agents.md: written for coding agents
  - but claude.md

- permission modes
  - shift-tab to cycle thru
  - manual: approve everything
  - accept edits: auto most everything, except for edits to claude itself
  - auto: model judges based on previous directions
  - bypass permissions: pretty much everything goes
  - plan mode: read only except for plan edits--highly recommended

- plan mode
  - the boss recommends: use liberally
  - explain what it does
  - party trick: create a / command that you can use anywhere, and have it do only two things: enter plan mode and run in xhigh effort; if you ever need anything plan, run it at the start of the prompt (eg, "/plan-this [prompt]")--which is two birds
  

# Level 2

## Claude (this entire part gets moved from Level 1 to Level 2)

## Instructions (after Claude, before Agents)

### The Claude.md file

- What it is
- What it does
- Where the global/default one is
- How there can be more than one: literally one per folder
- How it loads
  - At start: walks up, not down or sideways
  - Also loads whenever claude touches a file in the given directory
    - Illustrate this with multiple graphics/examples

### Claude.md tips

- Keep it short
  - Claude reads the whole thing--and that takes context
- Where things go matters
  - Claude does best with things at the top, bad with things at the bottom, worst within things in the middle
  - So put a short summary of the instructions up top, a checklist/reminder at the bottom, and the middle just expands on the top
    - Illustrate with plenty of graphics/examples
- Any instructions that only apply to certain situations should go into a rule instead

### Rules

- What they are
- What they do
- Where the global/default ones are
- How there can be more than one set: one per claude.md directory
- How they load
  - How you can @ from claude.md's to load at startup
  - How you can scope them
    - Illustrate this with plenty of examples/graphics

### Rules Tips

- Keep them short
- Use @ in a claude.md to automatically load any rule that is specific, but always applies
- Otherwise use separate rules
- When to use rules vs claude.md: for certain types of files/operations
  - 1 example: a rule that applies only to client folders, like make a copy of any file before you edit it
  - another example: a rule that applies only to certain file types, like flatten any pdf before you consider it done


## Custom Agents

### Advisor (between 'the fields that matter' and 'building one')
- give the setting
- say set it to opus
- note from the Boss: dual edged sword
  - very good to catch mistakes and have agents course correct before delivering something terrible
  - slow and expensive: agents call it way too often, including for basic things like reviewing basic searches

### Teach Micro
- give the brew to install micro
- give the setting to make micro the default editor
- explain control+g to expand prompts in interactive sessions

# Level 3

## MCPs

### Create

1. claude mcp add --transport http (to run on a url) <name> <url>

2. stores into projects by default, add --scope user to save globally

3. claude mcp list (to list mcps in projects)

4. claude mcp remove <name> (removes)

5. ask cc to do it, and it writes the json, kinda like a plugin

### Find

1. There is a directory of prebuilt mcp servers: https://mcpservers.org

2. ask claude if there is one to connect to whatever app/website you want

3. mcp servers have github repos; have cc read the documentation first to tell you what it can do for you

### Local

1. local mcps to connect with local tools, like databases

2. websocket mcp servers are bidirectional: they receive notifications from external services when events happen, like when you get email

### Warnings

1. mcp servers are heavy and degrade performance

2. better for dedicated agents in headless sessions?

3. load up front like skills do: so engineer visibility accordingly

### Login/Auth

1. Some servers will ask you to authenticate/login

### CC as an MCP Server

1. You can turn cc into an mcp server to let other applications connect to

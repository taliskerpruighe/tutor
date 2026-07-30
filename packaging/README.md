# tutor

A short course on getting the most out of Claude Code, fastest.

It comes in two halves. One you read; one answers questions.

## Setting it up

You should have a folder called `tutor` in your home folder. If it ended up
somewhere else, move it there first. Then, in Ghostty:

```bash
bash ~/tutor/install.sh
```

That takes a second or two and prints what it did. It only writes inside your
home folder and never asks for a password.

## Reading it

Open a **new** Ghostty tab and type:

```bash
tutor
```

You get a wiki. The parts of the course run across the top; the articles in
whichever part you are in run down the left, under the section headings that
group them; the article itself fills the rest.

Press `?` at any time for the full list of keys. The ones worth knowing now:

| Key | What it does |
|---|---|
| `n` | the next article — press it repeatedly to read straight through |
| `←` `→` | move between parts |
| `⇥` | move between sections |
| `↑` `↓` | scroll |
| `/` | search everything |
| `q` | quit |

Nothing in there can break anything. Press keys and see.

## Asking it questions

In a different tab, start Claude Code from inside the tutor folder:

```bash
cd ~/tutor
claude
```

Then ask it anything about Claude Code in plain English. It reads the same
course you do and answers from it.

Keep both tabs open. Read in one, ask in the other.

## Being taught it

If you would rather be taken through it than read it alone, type:

```
/learn
```

It works out where you have got to, tells you what to read next, asks you a
couple of questions when you come back, and gives you one thing to try. One
section at a time. Type `/learn` again whenever you want the next one.

## If something goes wrong

```bash
tutor doctor
```

It prints one line per check and tells you what to do about anything that
failed. Running `bash ~/tutor/install.sh` again fixes most things.

## What is in the folder

```
~/tutor/
├── content/        the course itself, one folder per part
├── tui/bin/        the reader; install.sh copies it to ~/.local/bin/tutor
├── .claude/        the skills Claude Code loads to help you
├── install.sh      run it whenever something seems off
└── CLAUDE.md       notes for Claude Code — you can ignore these
```

Nothing here needs building or updating by hand. Move the whole folder if you
like, then run `bash ~/tutor/install.sh` again so the `tutor` command knows
where it went.


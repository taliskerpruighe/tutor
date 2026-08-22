# Challenge 1 — notes

Running capture of what the user dictates. Notes only, no drafting yet.

## What this is

- An article, not a doc page in the usual sense.
- Sits at the **end of Level 2**, under a heading like **Challenges**.
- This one is **Challenge 1**.
- Form: essentially a **prompt** — the wiki speaking directly to the reader,
  setting them an objective to achieve.

## Objective

The reader must produce a **plugin they can ship** — via GitHub, which the
course already covers.

### What the plugin may contain

- A plugin folder mixing whatever the course has covered up to Level 2:
  agents, skills, workflows, and anything else — the reader's choice.

### The hard requirement

Whatever the reader builds, once they install the plugin on their own machine:

1. They go to a particular folder — the plugin folder or another folder.
2. From **within that folder**, they run a **single command**: `naturalize`
   (one word, no capitalisation).
3. That command takes an **argument**: a path to any folder on their machine.
4. `naturalize <folder>` alone, on the strength of the plugin's machinery,
   must do the **entire job start to finish** — take that folder as input and
   turn it into a complete **naturalization packet**.

## Open questions

- What *is* a naturalization packet? Needs a definition the reader can be held to.
- Is `naturalize` a slash command, a shell entry point, or something else?
- Does the run happen inside Claude Code, or at a plain shell?
- What counts as passing? Who or what checks the packet?
- Any constraint on the input folder's contents?

## Dictation log


## The corpus the reader is given

Two sets ship with the challenge:

1. **Worked examples** — complete naturalization packets, each with its
   **input** and its **output**.
2. **Input-only sets** — same kind of input, no output yet. These are what the
   reader's plugin has to handle.

### Input side (synthetic client material)

- A folder of fake client data and documents for one pretend client.
- Emails where the client states their details ("my name is…, my date of
  birth is…").
- Other document types — e.g. a spreadsheet a pretend client filled in with
  name, date of birth, and the rest of the information that feeds the packet.
- Other synthetic attachments, e.g. a fake tax return.

### Output side (the packet, done my way)

Synthetic versions of packets as I have built them in the past, with my rhythm:

- Cover pages for tabs and documents.
- A table of contents.
- Documents in a **particular order**:
  1. The **N-400** — the application form, filled.
  2. Then a handful of others: the client documents attached (the synthetic
     tax return, etc.).
- Delivered as a **merged PDF**.

## What success looks like

Point `naturalize` at one input-only folder. The plugin carries it start to
finish and produces an output **as close as possible** to the worked examples:
same format, same organization, same type of content — down to it being a
merged PDF, the font, and so on.

## Framing of the article (the prompt itself)

A **law firm that does naturalization** is issuing the challenge. It wants a
plugin it can run on its Claude Code harness to build entire naturalization
packets.

The firm has shared **a few examples**. Each example is **one past client**,
and each has:

- the **input** — what the client gave the firm;
- the **output** — the naturalization packet the firm made for that client.

Point to make to the reader: the **input always looks different** — it varies
by client — but the **output has a rhyme and a reason** to it. That is the way
the firm likes its naturalization packets done.

### What the firm asks for — three parts

1. **Where it runs.** The plugin can run on *your* computer, but the firm
   would be all the more impressed if you could share the plugin with them and
   have them run it on *their* computer. Either way, it runs on the **Claude
   Code harness** — yours or theirs.

2. **What it does.** Take an input folder from any given client and turn it
   into an output folder as close as possible to what the examples show. To
   let you test and prove the plugin, the firm also provides **a few more**
   client input folders with no output folder — packets still to be built.
   (Do not say "five".)

3. **How simply it works.** One single command on a terminal, with one single
   argument: the client input folder to be made into a naturalization packet.
   The firm will be all the more impressed if that command is the word
   `naturalize`, followed by the path on that computer to the client's input
   folder.

## "Feel free to cheat" (a small section in the article)

- The firm would like you to use just the topics covered in **Levels 1 and 2**
  of the tutor Claude Code course.
- Beyond that: feel free to cheat. Work smart, not hard.
- Point an agent running in Claude Code at this challenge, at the rest of the
  course, and at the materials provided — that should take you a long way.

## Open decisions for the draft (flagged, not resolved)

- **Spelling.** Draft uses US "naturalization" throughout, to sit beside the
  literal command `naturalize` and the N-400 (a US federal form). House style
  is otherwise British. Say if you want "naturalisation" in prose instead.
- **Version tag.** Draft carries `*v0.2.10*` — the newest tag in the corpus.
  A new part may want a new number.
- **The close.** This lands at the end of Level 2. If it is the last article
  of the last part, the corpus wants `---` and a paragraph naming the part
  coming — but there is nothing after it, and the voice guide forbids saying a
  part is the last. Draft ends plainly on `Press \`n\`.` pending your call.
- **`part` / `section` / `order`.** Nothing named "challenges" exists in
  `pipeline.md` or `index.json` yet; draft assumes part `Challenges`, section
  `Challenges`, order 1.

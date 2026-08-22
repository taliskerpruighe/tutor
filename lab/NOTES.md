# challenges/spike-002 — working notes

Spike purpose: build the synthetic data for challenge one (Level 2), per
`content/21-challenges/01-challenge-one.md`.

## Decisions

### 2026-08-21 — how many synthetic clients

Six synthetic clients, in two sets of three:

- **Three worked examples** — each is a matched pair of an *input* folder and
  an *output* folder. These are what the firm "gives" the challenge-taker to
  learn the target format from.
- **Three test clients** — *input* folder only, no output. These are what the
  challenge-taker runs their own plugin against to prove it works.

## Shape of the data (from the challenge prompt)

- **Input folders vary by client, deliberately.** An email stating biographic
  details, a filled-in spreadsheet, a tax return, scanned documents. The point
  is that no two inputs look alike.
- **Output folders do not vary.** The firm's house format: cover pages for
  tabs and documents, a table of contents, documents in a fixed order with the
  N-400 first, everything merged into one PDF in a consistent font.
- **Everything invented.** Names, dates of birth, addresses, A-numbers,
  employers, travel history. Nothing traceable to source material.

## Source material

`lab/` holds a set of client folders copied from the external drive, used as
reference for what these packets actually look like. Not yet read.

## Open

- Naming scheme for the six synthetic clients.
- Which input modality each of the six gets.
- Where the finished data lands in the repo.

### 2026-08-21 — which source folders define the output format

The source folders in `lab/` span more than a decade of the firm's work, so
they are *not* internally consistent. There is no single house style to be
read off the set as a whole, and averaging across all of them would produce
something the challenge prompt's "the output does not look different" claim
cannot support.

So the output format is not derived from the whole set. It is derived from
**two folders only**:

- `jacobs_brent`
- `zhu_vivian`

The synthetic outputs take their look and feel from a mix of those two — the
cover pages, the document order, the table of contents, the cover letters,
the merged-PDF conventions, the fonts.

The other folders (`izaguirre_jesus`, `malone_kyle`, `ossola_ylenia`) are not
format references. They may still be useful as evidence of how varied client
*input* gets, which is the one thing the challenge wants to stay messy.

### 2026-08-21 — the source folders are not split into input and output

The folders in `lab/` are not neatly divided the way the challenge's synthetic
data will be. They are mostly *output*, with *input* scattered through them —
often not sitting in any folder called "input" at all. An input document is
frequently recognisable only by being attached to an output: a scan behind a
tab, an exhibit stapled into a packet. Something the client handed over, sitting
inside the thing the firm built from it.

So the split has to be derived, not read off the directory names.

**Step one of the spike is therefore a mapping exercise, not a generation
exercise.** A wave of agents reviews every file in the source folders and
works out three things:

1. **What is input and what is output.** Per file. Including the inputs that
   only reveal themselves by being embedded in an output.
2. **How input becomes output.** What gets pulled from where. Which client
   fact lands in which field of which form. What is transcribed, what is
   attached wholesale, what is derived.
3. **How the packets are assembled.** Ordering, tabbing, cover pages, table
   of contents, cover letters, the merge.

That mapping is the artefact the generation step depends on. Nothing synthetic
gets written until it exists.

### 2026-08-21 — generation follows the mapping

With the mapping in hand:

- **Three outputs** are generated. They take their structure and their method
  of assembly from `jacobs_brent` and `zhu_vivian`.
- **Inputs are fabricated across** those three, working from the mapping so
  that each input actually accounts for what appears in its paired output.
- **Three further clients get inputs only** — same fabrication approach, no
  output built. Six input sets in total.

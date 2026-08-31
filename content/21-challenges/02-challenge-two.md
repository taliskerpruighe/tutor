---
id: challenges/two
title: Challenge two
level: Level 2
part: Challenges
order: 2
summary: A law firm wants every noncompete it has ever sent out turned into a library it can draft the next one from
keywords: [challenge, noncompete, provisions, library, template, terminal, states, search, meaning, draft]
---

# Challenge two

*v0.2.14*

A law firm has sent out noncompete agreements for years, and it can
no longer find them.

It would like you to turn what it has into a library it can draft
the next one from.

## What the firm has given you

The signed agreements sit in `materials/challenge-two/contracts/` —
nine files, governed by the law of New York, Connecticut or New
Jersey, saved as `.pdf`, `.docx` and one stray `.txt`.

As it is, the firm has a bunch of files and no way to track which
file uses which provisions. Two of them: `NONCOMPETE_FINAL_v3.docx`
and `Copy of Noncompete - Larkspur HVAC (M. Duarte) FINAL.pdf`.
Nobody at the firm can open one of those names and know what it
holds — a duration clause, a territory clause, or neither.

Alongside the contracts sits `materials/challenge-two/to-do/`,
three emails from a partner to an associate, each one asking for a
new hire's noncompete.

Each email buries the company name, the hire's name, the role, the
term, the territory and the industry scope inside ordinary prose.

One of the three also spends paragraphs on an unrelated Newark
closing, a dinner with the client's general counsel and a candidate
named Desmond Okafor, who withdrew from consideration weeks earlier
and still turns up in the file.

The firm wants a library it can draft from. Build it on your own
machine. It grows as you feed it.

## What the firm would like the library to do

Drop a noncompete into the folder and the library takes it apart
into provisions. A duration clause, a territory clause, a
garden-leave clause, a non-solicitation clause. It files each one
under the states where that wording holds up.

- **Files what it recognises.** Every provision it can identify gets
  sorted under its state.
- **Flags what it cannot place.** Instead of guessing, it sets the
  provision aside and says so.
- **Names a gap.** When a requested kind of provision has no
  precedent in the folder, it says so. Merrivale Diagnostics asked
  for a bar on poaching a client's reagent suppliers. Pell & Ottway
  asked for repayment of sponsored certification costs. Neither
  exists in the folder yet.
- **Finds the missing provision.** It searches for the missing
  provision itself. Then it judges whether what it finds is worth
  keeping.
- **Works unattended.** It watches the folder on its own, and
  reports when something lands.

Underneath the provisions sits a master template for the whole
contract — confidentiality, non-solicitation of customers, return of
company property and the rest. The provisions slot into it a clause
at a time.

## What drafting looks like

It runs in a terminal, not a browser. Pick a state. The available
provisions narrow to the ones that survive there.

The view has two sides: the template on one, the provisions
available to fill it on the other. You supply party names, duration,
geographic scope and subject-matter scope, and a finished draft
comes out.

Two ways to search: on wording when you know the wording, on meaning
when you only know the sense of it.

## Feel free to cheat

Everything in Levels 1, 2 and 3 of this course is fair game. How it
works is up to you.

Press `n`.

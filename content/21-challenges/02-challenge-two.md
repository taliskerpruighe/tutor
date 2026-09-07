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

Here is the situation. A law firm has been sending out noncompete agreements for years — governed by New York, Connecticut and New Jersey law — and the files are a mess. Nine contracts across PDF, DOCX and one stray TXT, sitting in `materials/challenge-two/contracts/`. The filenames are things like `NONCOMPETE_FINAL_v3.docx` and `Copy of Noncompete - Larkspur HVAC (M. Duarte) FINAL.pdf`. You open one, you have no idea whether it contains a duration clause, a territory clause, a garden-leave clause, or none of the above.

Alongside the contracts, in `materials/challenge-two/to-do/`, sit three emails from a partner to an associate. Each one is asking for a new hire's noncompete. The company, the name, the role, the term, the territory, the industry scope — all of it is in there, but it is buried in conversational prose. One of the three goes on about an unrelated Newark closing, a dinner with the client's general counsel, and a candidate named Desmond Okafor who withdrew weeks ago and has no business being in the file.

Here is what you are building: a provision library with a drafting interface, all of it running in the terminal.

The library does five things:

1. You drop a noncompete into the folder and it breaks the contract apart into provisions — duration, territory, garden-leave, non-solicitation, whatever it finds.
2. Each provision gets filed under the states where that language holds up. If it cannot place a provision, it sets it aside and says so rather than guessing.
3. When a type of provision has no precedent in the folder, it tells you. Merrivale Diagnostics asked for a bar on poaching a client's reagent suppliers. Pell & Ottway asked for repayment of sponsored certification costs. Neither one is in the folder.
4. It goes and finds the missing provision on its own, then makes a judgment on whether what it found is usable.
5. It watches the folder. A new contract lands, it gets processed — no manual trigger.

Underneath the provisions sits a master template for the full contract: confidentiality, non-solicitation of customers, return of company property, the rest. Provisions slot into it one clause at a time.

The drafting interface has two sides. On one side, the template. On the other, the provisions available to fill it. You pick a state and the provisions narrow to the ones that survive there. You supply the party names, the duration, the geographic scope and the subject-matter scope, and a finished draft comes out the other end.

Two ways to search: by exact wording when you know it, by meaning when you only know what you are looking for.

Everything in Levels 1, 2 and 3 of this course is fair game. How you build it is up to you.

Press `n`.

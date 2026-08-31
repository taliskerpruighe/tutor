---
id: challenges/three
title: Challenge three
level: Level 2
part: Challenges
order: 3
summary: Small businesses want a web application that turns their uploaded paperwork into finished financial statements
keywords: [challenge, web application, accounts, upload, profit and loss, balance sheet, chat, hosting, period, statements]
---

# Challenge three

*v0.2.14*

Three small businesses in New York — a limited liability company, a
partnership and a corporation — want a web application. It turns
whatever paperwork they upload into a profit and loss and a balance
sheet. You are building it.

## What the three businesses have given you

`materials/challenge-three/` holds three folders, one per business.

`ferrone-provisions-llc` is a food business in Sunset Park,
Brooklyn. It carries stock. Its filing is tidy: a folder tree by
document type, two bank accounts, the whole of 2025.

`halloran-vance-design` is a design partnership on West 23rd
Street. It is a service business with no stock. Its invoices and
receipts sit in dated batches, running from July 2024 to August
2025.

`bright-harbor-fabrication` is a manufacturer in Long Island City,
a corporation with stock, equipment and loans.

It has over a hundred files in one flat folder for calendar 2025,
with names like `Copy of card statement.pdf`, `bank aug pt1.pdf`
and `scan3021.pdf`. Many are scanned pages with no text in them.

Each folder opens with a letter from the business's previous
accountant, stating the cash, receivables, payables and capital at
the end of the last engagement.

`bright-harbor-fabrication` keeps it as `opening_position_letter.pdf`,
loose in the flat folder. `ferrone-provisions-llc` keeps it in
`opening/`. `halloran-vance-design` keeps it in the first batch
folder.

Everything after that letter has to reconcile against its figures.

Formats run to `.pdf`, `.docx`, `.xlsx`, `.csv`, `.jpg` and `.txt`.
No two of the three periods share a start or an end.

A year of stock movements and a year of service invoices do not
reduce to the same shape.

## What the application has to produce

Out of whatever has been uploaded, the application produces a
profit and loss and a balance sheet without being asked for
either.

Nobody sets the reporting period. It is whatever the uploaded
documents happen to cover: a single month for one business, years
for another.

A document that only states a balance — the opening letter, or a
running total on a bank statement — has to be reconciled against
the material that explains how it was reached.

## What has to be on the page

One page after login holds all of this. The account logs out as
easily as it logs in.

- **Somewhere to upload.** One place for whatever gets added next.
- **Somewhere to browse.** Every document uploaded before, open
  again.
- **The two statements.** Sortable and filterable by period.
- **An agent, reachable through a chat box.** Tied to the account,
  on the same page.

## How far you take it

No stack is specified. No particular way of handling a login is
required. Levels 1, 2 and 3 of this course are all fair game.

Build it on your own machine first. Then host it: a second person,
on a second machine, reaches it with an address in a browser and
uses it without being told how. It has to survive a reboot and keep
working unwatched.

Nobody marks this. The only test is that it works.

Press `n`.

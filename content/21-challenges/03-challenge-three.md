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

Here is the situation. Three small businesses in New York want an application that turns their paperwork into financial statements. A limited liability company, a partnership and a corporation — each one different enough that the same approach will not work for all three. You are building the application, and it runs in a browser, not a terminal.

The three businesses and their paperwork sit in `materials/challenge-three/`.

`ferrone-provisions-llc` is a food business in Sunset Park, Brooklyn. It carries stock. Its filing is tidy: a folder tree organized by document type, two bank accounts, the whole of 2025.

`halloran-vance-design` is a design partnership on West 23rd Street. Service business, no stock. Its invoices and receipts sit in dated batches running from July 2024 to August 2025.

`bright-harbor-fabrication` is a manufacturer in Long Island City — a corporation with stock, equipment and loans. It has over a hundred files dumped into one flat folder for calendar 2025, with names like `Copy of card statement.pdf`, `bank aug pt1.pdf` and `scan3021.pdf`. Many of them are scanned pages with no selectable text.

Each folder opens with a letter from the business's previous accountant, stating the cash, receivables, payables and capital at the end of the last engagement. Where the letter sits depends on the business: `bright-harbor-fabrication` keeps it loose as `opening_position_letter.pdf`, `ferrone-provisions-llc` keeps it in `opening/`, `halloran-vance-design` keeps it in the first batch folder. Everything after that letter has to reconcile against its figures.

Formats run to PDF, DOCX, XLSX, CSV, JPG and TXT. No two of the three periods share a start or an end. A year of stock movements and a year of service invoices do not reduce to the same shape.

Here is what the application does. A business signs up, uploads what it would otherwise hand a bookkeeper, and gets back two financial statements: a profit and loss and a balance sheet. Nobody sets the reporting period — it is whatever the uploaded documents happen to cover. A document that only states a balance (the opening letter, a running total on a bank statement) has to be reconciled against the material that explains how it was reached.

The whole thing fits on one page after login:

1. A place to upload whatever gets added next.
2. A place to browse everything uploaded before.
3. The two statements, sortable and filterable by period.
4. A chat box tied to the account, on the same page as everything else.

No stack is specified. No particular login mechanism is required. Everything in Levels 1, 2 and 3 of this course is fair game.

Build it on your own machine first, then host it. A second person on a second machine types an address into a browser and uses it without being told how. It survives a reboot and keeps working with nobody watching it.

Nobody marks this. The only test is that it works.

Press `n`.

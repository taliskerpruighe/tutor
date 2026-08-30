# Challenge Three — SPEC.md (frozen contract for Stage B)

**Shared files are FROZEN after Stage A.** `lib/ledger.py`, `lib/render.py`,
`validate.py` and this file (`SPEC.md`) must NOT be edited by any Stage B
worker. If a worker needs a change to one of these, it reports the need to
the lead and waits — it does not edit the file itself and does not work
around the limitation by duplicating/forking the frozen file. Each Stage B
worker owns exactly one company's output: its own `lab/challenge-three/<slug>/`
data files and its own `content/21-challenges/materials/challenge-three/<slug>/`
document tree. Stage B workers read ONLY this file, not the plan that
produced it.

---

## 0. On-disk layout

```
lab/challenge-three/
  SPEC.md                       <- this file, frozen
  lib/ledger.py                 <- frozen
  lib/render.py                 <- frozen
  validate.py                   <- frozen
  fixtures/                     <- Stage A's own proof, not touched by Stage B
  <slug>/ledger.jsonl            <- Stage B writes these four files
  <slug>/documents.jsonl
  <slug>/statements.jsonl
  <slug>/opening_position.json
  <slug>/answer-key.md           <- prose answer key, see §7

content/21-challenges/materials/challenge-three/<slug>/
  ...the shipped documents themselves (PDFs, DOCX, XLSX, CSV, JPG, TXT)...
```

`<slug>` is one of `ferrone-provisions-llc`, `halloran-vance-design`,
`bright-harbor-fabrication`.

Everything under `lab/challenge-three/<slug>/` is current-period ledger,
statement and answer-key data and **never leaves that directory** — it is
the answer key, not part of the shipped corpus. Everything a reader is
meant to receive lives under `content/21-challenges/materials/challenge-three/<slug>/`.

All dates inside `ledger.jsonl`, `documents.jsonl`, `statements.jsonl` and
`opening_position.json` are ISO `YYYY-MM-DD` strings. Source *documents*
under `content/.../<slug>/` deliberately vary their date format — see
Mandated Defect 6. All amounts in these four files are **integer cents**
(e.g. `$1,234.56` is `123456`). Every `path` field is relative to the repo
root (e.g. `content/21-challenges/materials/challenge-three/ferrone-provisions-llc/bank/operating/2025-01.pdf`),
never an absolute path and never relative to `lab/`.

---

## 1. The ledger schema

### 1.1 `ledger.jsonl` — one journal *line* per record

Fields, exact names: `entry_id, date, account_code, account_name, debit, credit, memo, counterparty, doc_ids[]`.

- `entry_id`: groups the lines of one journal entry. All lines sharing an
  `entry_id` must have `sum(debit) == sum(credit)` across that group
  (double-entry, enforced by `validate.py` check 7). Opening-balance
  entries — the ledger's encoding of the prior-period closing position —
  use `entry_id` prefixed `OB-` (e.g. `OB-1`) and are dated the day before
  `period_start` (`2024-12-31` for Ferrone and Bright Harbor, `2024-06-30`
  for Halloran & Vance).
- `date`: ISO `YYYY-MM-DD`.
- `account_code` / `account_name`: from the shared chart of accounts, §2.
  `account_name` must exactly match the chart's name for that code. This
  is a contract requirement but is **not** independently enforced by
  `validate.py` (only `account_code` drives every check) — get it right
  anyway; a mismatch here is a real bug even though nothing in §8 will
  catch it for you.
- `debit`, `credit`: integer cents. On every line, exactly one of the two
  is non-zero and the other is `0`.
- `memo`: short free text. Where a line records a mandated defect (e.g. an
  inter-account transfer, a personal expense treated as a distribution),
  the memo should name what it is in plain language — this is what a
  reader and the validator's human reviewer use to sanity-check treatment.
- `counterparty`: the named person/entity on the other side of the
  transaction, or `""` for lines with no natural counterparty (e.g. a
  depreciation entry).
- `doc_ids`: non-empty list of `doc_id`s (§1.2) that evidence this
  specific line. **Every line, cash or non-cash, needs at least one.** A
  cash line is typically evidenced by the bank statement document that
  contains it; a non-cash line (AR, AP, depreciation, inventory movement,
  accrual) is evidenced by the specific invoice/bill/schedule/letter that
  created it.

### 1.2 `documents.jsonl` — the document registry, one record per shipped file

Fields, exact names: `doc_id, kind, path, format, scanned, issued_date, counterparty, amount`.

- `doc_id`: unique string, referenced from `ledger.jsonl` and
  `statements.jsonl`.
- `kind`: one of `opening_letter, bank_statement, bank_export_csv,
  invoice_out, credit_note, bill_in, receipt, cash_receipt_handwritten,
  payroll_summary, payroll_register, stock_count, loan_amortization,
  credit_card_statement, multi_document_bundle`, or another short
  snake_case kind if a company genuinely needs one — keep the vocabulary
  small and consistent within a company.
- `path`: relative to repo root, under
  `content/21-challenges/materials/challenge-three/<slug>/`.
- `format`: one of `pdf, docx, xlsx, csv, jpg, txt`.
- `scanned`: boolean — true for image-only scans and photographed
  receipts (i.e. anything that went through `scanify()` or
  `photograph_receipt()`), false for text-native documents.
- `issued_date`: the date printed ON the document, in whatever format that
  document uses (this is the field that legitimately varies in format —
  see Mandated Defect 6 — unlike every date in the four machine-readable
  files, which is always ISO).
- `counterparty`: the named party the document is with/from.
- `amount`: integer cents for documents with one natural headline amount
  (an invoice, a bill, a receipt); `null` for documents without one (a
  stock count, an amortisation schedule, a multi-document bundle, an
  opening letter carrying several figures).

### 1.3 `statements.jsonl` — bank/credit-card statement registry

Not in the original two-file description — added because `validate.py`
checks 1, 2, 3 and 9 need the statement's own **stated** opening balance,
closing balance and line items as an independent source to check the
ledger against. If the validator derived a statement from the ledger and
then compared it to the ledger, every one of those checks would be a
tautology that cannot fail. `statements.jsonl` is what a human reading the
bank statement PDF would transcribe by hand. Fields, exact names:

`stmt_id, account_code, stmt_period_start, stmt_period_end, opening_balance, closing_balance, doc_ids[], lines[]`

Each entry in `lines[]` is an object:
`{date, description, amount, direction, entry_id}` where:
- `amount` is a positive integer in cents.
- `direction` is `"in"` (money added to the account — a deposit/credit) or
  `"out"` (money removed — a withdrawal/debit). This is the bank's
  perspective, not the ledger's debit/credit convention: a statement
  `"in"` line corresponds to a ledger **debit** on that (asset) cash
  account, and a statement `"out"` line to a ledger **credit** — because
  cash is a debit-normal account. Do not confuse the two conventions.
- `entry_id` is the `ledger.jsonl` entry that this statement line
  corresponds to. `validate.py` check 1 requires this link to resolve
  both ways: every statement line must name a real ledger entry on that
  account with a matching cents amount, and every ledger line touching a
  cash account (dated on/after that account's `period_start`) must appear
  in some statement's `lines[]`.

One `statements.jsonl` record exists per statement period per account —
i.e. one company-month per bank/credit-card account (Bright Harbor's
credit card is itself an `account_code`-bearing "statement" for this
purpose even though it is a liability, not an asset — Mandated Defect 8).

Opening-balance (`OB-`) ledger entries are exempt from the statement-trace
requirement (there is no statement covering the day before `period_start`)
— they are evidenced instead via the opening letter and checked
separately by check 9.

### 1.4 `opening_position.json` — the prior-period closing position, structured

One object per company, mirroring the prior-CPA opening letter (Hard Rule
Two) in machine-readable form so `validate.py` can check it independently
of the ledger:

```json
{
  "period_start": "2025-01-01",
  "period_end": "2025-12-31",
  "as_of": "2024-12-31",
  "cash_by_account": {
    "1000": {"amount_cents": 0, "doc_ids": ["..."]},
    "1010": {"amount_cents": 0, "doc_ids": ["..."]}
  },
  "accounts_receivable": [
    {"debtor": "Named Debtor LLC", "amount_cents": 0, "doc_ids": ["..."]}
  ],
  "accounts_payable": [
    {"creditor": "Named Creditor Inc", "amount_cents": 0, "doc_ids": ["..."]}
  ],
  "equity_components": {
    "label": {"account_code": "3000", "amount_cents": 0, "doc_ids": ["..."]}
  },
  "other_balances": {
    "account_code": {"amount_cents": 0, "doc_ids": ["..."]}
  },
  "depreciation_policy": "prose, Bright Harbor only"
}
```

`cash_by_account` MUST have one entry per cash account the company uses
(Ferrone: two — operating and payroll). `validate.py` check 9 requires
each account's `amount_cents` here to equal that account's first
in-period statement's `opening_balance` exactly. `accounts_receivable` and
`accounts_payable` must be non-empty per Hard Rule Two. `other_balances`
holds anything else the opening letter states that isn't cash/AR/AP/equity
— inventory, sales tax payable, fixed assets and accumulated depreciation,
loan balances, as applicable per company.

### 1.5 The shared chart of accounts

`account_code` in every ledger line must be a key in the `CHART` dict
defined in `lib/ledger.py`. That dict is the single source of truth; the
table below mirrors it for reading convenience. `type` and `normal_side`
drive `validate.py` check 7's accounting-equation check.

| Code | Name | Type | Normal side |
|---|---|---|---|
| 1000 | Cash - Operating | asset | debit |
| 1010 | Cash - Payroll | asset | debit |
| 1020 | Cash - Secondary Operating | asset | debit |
| 1200 | Accounts Receivable | asset | debit |
| 1300 | Inventory | asset | debit |
| 1400 | Prepaid Expenses | asset | debit |
| 1500 | Fixed Assets - Equipment | asset | debit |
| 1510 | Fixed Assets - Vehicles | asset | debit |
| 1590 | Accumulated Depreciation | asset (contra) | credit |
| 2000 | Accounts Payable | liability | credit |
| 2100 | Sales Tax Payable | liability | credit |
| 2200 | Accrued Payroll Liabilities | liability | credit |
| 2300 | Credit Card Payable | liability | credit |
| 2400 | Loan Payable - Current Portion | liability | credit |
| 2410 | Loan Payable - Long-Term Portion | liability | credit |
| 3000 | Member Capital - A. Ferrone | equity | credit |
| 3010 | Member Capital - L. Ferrone | equity | credit |
| 3020 | Member Distributions - A. Ferrone | equity (contra) | debit |
| 3030 | Member Distributions - L. Ferrone | equity (contra) | debit |
| 3100 | Partner Capital - Halloran | equity | credit |
| 3110 | Partner Capital - Vance | equity | credit |
| 3120 | Partner Draws - Halloran | equity (contra) | debit |
| 3130 | Partner Draws - Vance | equity (contra) | debit |
| 3200 | Common Stock | equity | credit |
| 3210 | Additional Paid-In Capital | equity | credit |
| 3220 | Retained Earnings | equity | credit |
| 3230 | Shareholder Distributions | equity (contra) | debit |
| 4000 | Sales Revenue | income | credit |
| 4900 | Other Income | income | credit |
| 5000 | Cost of Goods Sold | expense | debit |
| 6000 | Rent Expense | expense | debit |
| 6010 | Utilities Expense | expense | debit |
| 6020 | Wages Expense | expense | debit |
| 6030 | Payroll Tax Expense | expense | debit |
| 6040 | Subcontractor Expense | expense | debit |
| 6050 | Office Supplies Expense | expense | debit |
| 6060 | Insurance Expense | expense | debit |
| 6070 | Professional Fees Expense | expense | debit |
| 6080 | Bank Fees Expense | expense | debit |
| 6090 | Interest Expense | expense | debit |
| 6100 | Depreciation Expense | expense | debit |
| 6110 | Vehicle Expense | expense | debit |
| 6130 | Advertising & Marketing Expense | expense | debit |
| 6140 | Repairs & Maintenance Expense | expense | debit |
| 6150 | Telephone & Internet Expense | expense | debit |
| 6900 | Miscellaneous Expense | expense | debit |

Use only the equity accounts relevant to your company: Ferrone uses
3000/3010 (capital) and 3020/3030 (distributions); Halloran & Vance uses
3100/3110 (capital) and 3120/3130 (draws); Bright Harbor uses
3200/3210/3220 (stock/APIC/retained earnings) and 3230 (distributions).
Sales tax collected is **never** routed through an income account — it
posts directly to liability 2100 on the same entry as the sale.

Company-specific *named* equity holders (the two Ferrone members, the two
Halloran & Vance partners) must use identical names everywhere they
appear — the chart-of-accounts names above are the actual names to use
throughout; do not invent different surnames per document.

---

## 2. The three companies (verbatim)

**1. `ferrone-provisions-llc` — Ferrone Provisions LLC.** New York LLC,
Sunset Park, Brooklyn. Specialty Italian food importer/wholesaler selling
to restaurants and small grocers. Two members. Revenue $1.4–1.8M, 4
employees. The trader with stock: inventory, COGS, supplier payables,
physical stock count at period end. Collects NY sales tax on a minority of
sales (retail counter business), remits quarterly, so sales tax payable is
a live liability. **Period: 1 Jan – 31 Dec 2025.**

**2. `halloran-vance-design` — Halloran & Vance Design Partners.** New
York general partnership, Flatiron District. Interior architecture and
design consultancy. Two partners, one salaried employee, two regular
subcontractors. Revenue $600–850K. Service business, no stock: no
inventory, no COGS, revenue billed by project phase, significant unpaid
(NOT unbilled) work at period end. **Fiscal year ending 30 June.**
Documents run July 2024 through August 2025 — fourteen months. **Period: 1
Jul 2024 – 30 Jun 2025**; the July–August 2025 trailing stub must still be
bank-reconciled and document-evidenced but is excluded from the answer key
and the P&L-to-equity tie.

**3. `bright-harbor-fabrication` — Bright Harbor Fabrication Inc.** New
York business corporation (S election), Long Island City, Queens. Small
architectural metal fabrication shop. One officer-shareholder plus a
second minority shareholder, 6 employees. Revenue $900K–1.2M. The one with
a loan: a five-year equipment term loan drawn Q2 2025 against a press
brake purchase, plus an older vehicle loan running off, plus a business
credit card. Fixed assets, accumulated depreciation, current and
long-term portions of debt. **Period: 1 Jan – 31 Dec 2025.**

---

## 3. Conventions

- Every entity, person, bank, CPA firm, payroll provider, lender,
  customer and vendor is **invented**. Never a real company or bank name.
- Invent one bank per company, each with a **visibly different statement
  layout** from the others.
- Invent CPA firms (the prior-period one AND, if a company mentions its
  current one, that one too), a payroll provider, a lender (Bright
  Harbor), and every customer and vendor named anywhere.
- Addresses: real New York streets and neighbourhoods, invented street
  numbers.
- EINs: format `99-XXXXXXX` (invented digits).
- Bank and card numbers: masked to last four digits everywhere they
  appear (`****4417`), never a full number.
- Phone numbers: 555 exchange (`(718) 555-01XX` etc.)
- No watermarks, no "SAMPLE" stamps, no disclaimers of any kind in any
  shipped document — they must read as genuine business records.
- Names, addresses, account numbers and EINs are **identical everywhere**
  they appear within a company's corpus. Any cross-document discrepancy
  is a bug **except** for the mandated defects in §6, which are
  deliberate and must be recorded in that company's `answer-key.md`.

---

## 4. Hard rules (restated in full)

**Rule One — one ledger, everything rendered from it.** Each company's
corpus is generated from a single deterministic double-entry ledger that
is the sole source of truth. Every shipped document is rendered FROM that
ledger, never hand-written. A bank statement line, an invoice, a receipt
and a bill are four views of ledger entries and must agree to the cent.
Nothing is hand-typed into a document that is not in the ledger; nothing
is in the ledger that no shipped document evidences. Seed every random
draw with a fixed integer.

**Rule Two — nothing shipped may carry a current-period derived total.**
*Required:* a prior-period opening position document per company — one
letter from an invented previous CPA firm giving the closing balance sheet
as at the day before the period begins (31 Dec 2024 for Ferrone and
Bright Harbor; 30 Jun 2024 for Halloran & Vance). PDF letter, figures in
running prose plus a simple table, not a machine-readable export. Each
opening letter must also carry **non-zero opening accounts receivable and
accounts payable** — named debtors and creditors with amounts. Their
in-period settlement must appear in the bank statements and must be
excluded from current-period income and expense; record the treatment in
the answer key. **Bright Harbor's opening letter must state the
depreciation policy explicitly** — method, useful lives, rates by asset
class — and the press brake invoice must carry cost and in-service date.
*Forbidden under `content/21-challenges/materials/challenge-three/`:* any
current-period P&L, balance sheet, trial balance, general ledger,
year-end summary, management accounts, tax return, or bookkeeping-software
export stating a current-period total. When in doubt, it does not ship.
Current-period ledgers, statements and answer keys live only in
`lab/challenge-three/<slug>/` and never leave it.

**Rule Three — the equity section carries the entity type.**
- Ferrone (LLC): opening letter breaks equity into two named members'
  capital accounts. In-year member distributions appear as identifiable
  dated bank withdrawals whose memo names them.
- Halloran & Vance (partnership): opening letter gives per-partner capital
  accounts, unequal, with the profit-sharing ratio stated in prose.
  Partner draws are recurring monthly bank withdrawals, different amounts
  per partner. One partner contributes additional capital once in the
  period, evidenced by a deposit and a short note.
- Bright Harbor (corporation): opening letter gives common stock,
  additional paid-in capital and retained earnings separately. Officer
  salary runs through payroll (the S-corp tell); one shareholder
  distribution appears as a bank withdrawal late in the year.

**Rule Four — the quarters must mean something.**
- Ferrone: Q4 spike — holiday wholesale orders roughly double Oct–Dec
  volume, matching inventory build in Q3 (purchases up, cash down),
  January receivables catch-up.
- Halloran & Vance: summer lull — July and August billings fall to about a
  third of the spring peak; one large project completes in fiscal Q2 with
  a milestone invoice dominating the quarter.
- Bright Harbor: press brake purchase and loan draw both land in Q2 2025
  — fixed assets jump, cash moves twice, depreciation begins.

**Rule Five — different shape of mess per company.**
- *Ferrone, the tidy client:* foldered by kind and month — `opening/`
  (prior accountant letter PDF); `bank/operating/` (12 monthly statements,
  text PDF, one bank layout); `bank/operating/export/` (CSV export
  covering **Jan–Jun only**, different column names and date format from
  the PDFs); `bank/payroll/` (12 monthly statements, second account);
  `invoices-out/2025-01/ ...` (sales invoices, PDF from an invoicing
  tool); `bills-in/2025-01/ ...` (supplier bills, mixed text PDF and
  scanned); `receipts/` (photographed till and fuel receipts, JPG);
  `payroll/` (provider summary PDFs + one XLSX register); `inventory/`
  (opening and closing stock counts, XLSX).
- *Halloran & Vance, the email client:* nothing foldered by kind. Batches
  named `NNNNNN_YYYY-MM-DD_slug/`, each containing a `body.txt` email and
  its attachments — this is challenge one's own verified convention (see
  `content/21-challenges/materials/challenge-one/to-do/tran_daniel/` for
  the real thing; read a `body.txt` there for register and tone). Roughly
  20–28 batches across fourteen months. Bank statements arrive as
  attachments inside those emails, sometimes two months late, sometimes
  two at once. Some issued invoices are `.docx` from the partnership's own
  template; some months of expenses arrive only as a self-maintained
  `.xlsx` log with receipts attached separately.
- *Bright Harbor, the shoebox:* a flat dump, no subdirectories, human
  filenames with no convention — `IMG_4417.jpg`, `scan0021.pdf`,
  `Statement (3).pdf`, `march bills.pdf`, `Scanned Documents 2.pdf`,
  `bank apr.pdf`, `receipt_001.jpeg`, `Copy of payroll.xlsx`. At least
  three **multi-document PDFs** (one file containing three to six
  unrelated vendor bills scanned in one pass), and one month's bank
  statement split across two separate scan files. Bank statements here
  are **image-only scans** needing OCR.

---

## 5. Additional rulings (resolve real traps — each stated explicitly)

1. **Shared files are FROZEN after Stage A.** Restated from the top of
   this file for visibility: `lib/ledger.py`, `lib/render.py`,
   `validate.py` and `SPEC.md` are not to be edited by Stage B. Report the
   need and wait.

2. **Per-company budgets.** Global cap: 40 MB and 250–400 files across all
   three companies combined. Per company:
   - Ferrone ≤ 12 MB, 80–110 files
   - Halloran & Vance ≤ 10 MB, 80–110 files
   - Bright Harbor ≤ 16 MB, 90–130 files
   Each Stage B worker reports its own total bytes and file count at the
   end of its run (e.g. `find content/.../<slug> -type f | wc -l` and
   `du -sb content/.../<slug>`).

3. **Revenue recognition is on invoice issuance. Unbilled work-in-progress
   is FORBIDDEN in the ledger.** Halloran & Vance has significant
   *unpaid* work at period end (accounts receivable, evidenced by issued
   invoices) but NO accrued unbilled revenue. A WIP schedule would be a
   forbidden current-period derived total (Rule Two), and unbilled
   revenue could never be evidenced by a shipped document, so it would
   fail check 6 outright. Every dollar of Halloran & Vance revenue in the
   ledger must trace to an issued invoice document.

4. **A physical stock count is a source document, not a summary.**
   Ferrone's opening and closing stock count XLSX files MUST carry
   quantities, unit costs, and extended line totals (qty × unit cost).
   Without unit costs the closing inventory valuation is unreachable from
   the folder. This is an explicit carve-out from Rule Two ("nothing
   shipped may carry a current-period derived total") — a stock count's
   own extended-total column is not a forbidden derived total, it is the
   raw count. Do not strip the unit costs or the extensions to make the
   file "safer"; that would make the corpus internally unsolvable.

5. **The opening letter's cash figure must equal, per account, the
   opening balance on that account's first in-period statement.** Ferrone
   has two accounts (operating + payroll): the letter must give cash
   broken out per account, and each must tie to that account's January
   2025 opening balance. `validate.py` check 9 enforces exactly this via
   `opening_position.json`'s `cash_by_account` against
   `statements.jsonl`'s earliest statement per account — this is not
   otherwise caught by any other check, so get `cash_by_account` right.

6. **Halloran & Vance needs a payroll document class.** It has one
   salaried employee. Wages, withholding, and any accrued payroll
   liability need shipped evidence. Emailed payroll-provider summary PDFs
   inside the email batches fit its organisational shape (Rule Five).

7. **New York sales tax quarters are NOT calendar quarters.** NY
   quarterly filing periods are fixed as:

   | Period | Due date |
   |---|---|
   | 1 Mar – 31 May | 20 Jun |
   | 1 Jun – 31 Aug | 20 Sep |
   | 1 Sep – 30 Nov | 20 Dec |
   | 1 Dec – 28/29 Feb | 20 Mar |

   This exact table is the constant `NY_SALES_TAX_QUARTERS` in
   `lib/ledger.py` (it also carries the quarters bracketing Ferrone's
   period on both sides, since the Dec–Feb quarter spans the year
   boundary). Ferrone's remittance bank withdrawals must land on the due
   dates from this table (20 Mar, 20 Jun, 20 Sep, 20 Dec 2025 within the
   2025 period), and Ferrone's period-end (31 Dec 2025) sales-tax-payable
   balance must be exactly the tax collected since the last remittance
   (1–31 Dec 2025, since the Dec–Feb quarter isn't due until 20 Mar 2026).
   Symmetrically, the 20 Mar 2025 remittance settles the Dec 2024–Feb
   2025 quarter, so **the 1 Dec–31 Dec 2024 slice of that liability must
   appear as Ferrone's opening sales-tax-payable balance** in
   `opening_position.json`'s `other_balances` and the opening letter. Do
   not let the generator assume Mar/Jun/Sep/Dec calendar quarters
   anywhere in Ferrone's logic.

---

## 6. Mandated defects (every company's answer key records each, with its correct treatment)

1. One duplicate receipt per company — same purchase shipped twice in two
   different formats.
2. One clearly personal expense on a business account per company (flight,
   restaurant, household purchase), correctly treated as an owner's draw /
   member distribution / shareholder distribution, **not** an expense.
3. Ferrone's inter-account transfers between operating and payroll
   accounts, appearing on both statements — income to neither.
4. At least four sales invoices unpaid at period end per company (AR) and
   at least four vendor bills unpaid at period end (AP).
5. One issued invoice later cancelled by a credit note (Ferrone).
6. Inconsistent date formats across sources within the same company —
   `03/04/2025`, `2025-04-03`, `3 Apr 2025` (this variance belongs only in
   `documents.jsonl`'s `issued_date` / the rendered documents themselves —
   `ledger.jsonl`, `statements.jsonl` and `opening_position.json` are
   always ISO, no exceptions).
7. One handwritten-looking cash receipt per company, photographed at an
   angle (`lib/render.py`'s `handwritten_note_image()` + implicit
   `photograph_receipt()` pass).
8. Bright Harbor's credit card statements for the full year — a liability
   with its own balance, paid down monthly from the bank account.
9. Bright Harbor's loan: an amortisation schedule PDF from the lender, and
   monthly bank payments that must be split between interest (expense)
   and principal (liability reduction).
10. Ferrone's CSV bank export covers January to June, the same months the
    PDF statements already cover — a reader ingesting both double-counts
    half a year. Deliberate; the answer key must document that the CSV
    export is a duplicate view of Jan–Jun, not additional activity.

Ferrone's sales invoices must show subtotal, New York sales tax, and total
as three separate line items.

Formats across the corpus: text PDF, image-only scanned PDF, DOCX, XLSX,
CSV, JPG, TXT. No company uses only one. Raster content at most 500 KB
**per page**, not per file (this is what `lib/render.py`'s `scanify()`
noise parameters are tuned to — see the comment at its noise step before
changing anything, and re-measure per-page bytes on a dense fixture if you
believe you must).

---

## 7. The answer key

Each company ships `lab/challenge-three/<slug>/answer-key.md`, prose,
covering at minimum: each of the ten mandated defects (§6) with its
correct treatment and where to find the evidence; the opening AR/AP
settlement treatment (Rule Two); for Bright Harbor, the depreciation
policy and how it was applied; for Halloran & Vance, the profit-sharing
ratio and how the trailing stub is scoped out of the period; for Ferrone,
how the NY sales tax constant drove the remittance dates and period-end
payable. This file is not read by `validate.py` — it is for the human/LLM
solving the challenge to check its own work against, and for you to prove
to yourself that every defect is real and locatable before you call your
run done.

---

## 8. `validate.py` — the pass condition (for reference; frozen, do not edit)

Usage: `python lab/challenge-three/validate.py <slug>`. Checks, printed by
name with PASS/FAIL and offending items, non-zero exit on any failure:

1. **Bidirectional bank-statement/ledger trace.** Every statement line
   traced to a ledger entry, and every ledger entry touching a bank
   account traced to a statement line (opening-balance entries exempted,
   §1.3).
2. **Statement arithmetic.** `opening + credits − debits == closing` per
   statement.
3. **Month-to-month continuity.** Closing balance of month N equals
   opening balance of month N+1, per account, no date gaps.
4. **Inter-account transfers.** Present on both accounts' statements,
   recognised as transfers — never income on one side or expense on the
   other.
5. **Non-cash entries evidenced.** Every entry with no cash-account leg
   (receivables/payables, depreciation, inventory movement, accruals) has
   every line traced to a specific shipped document.
6. **The master check: an explicitly printed, explicitly empty list of
   unevidenced ledger entries**, across ALL lines (cash and non-cash). A
   non-empty list is a FAILURE regardless of what else balances — this is
   the real pass condition for the whole deliverable.
7. **Period accounting identity.** Within `period_start`/`period_end`
   only: `assets == liabilities + equity + income − expense` as of
   `period_end` (this is the standard extended trial-balance identity;
   because it also requires every entry's own debits to equal its own
   credits, it catches transcription bugs even though a fully
   double-entry-consistent ledger satisfies it by construction).
   Halloran & Vance's July–August 2025 trailing stub (dated after
   `period_end`) is excluded from this check only, not from checks 1–6.
8. **No forbidden documents; no files outside the two permitted trees.**
   Scans `content/21-challenges/materials/challenge-three/<slug>/` by
   filename and by content for the Rule Two forbidden-document patterns.
   Content scanning is cheap and bounded, not exhaustive: `.txt`/`.csv`
   read in full, `.docx` first 200 paragraphs, `.xlsx` first 20 rows per
   sheet, `.pdf` **first 10 pages only** (this matters for Bright
   Harbor's multi-document bundles, which run 3-6 unrelated bills per
   file). Scanned/photographed image formats (`.jpg`, image-only `.pdf`)
   are not OCR'd by this check — filename discipline and the answer key
   are what keep those honest. A file that cannot be parsed at all is
   reported as `unreadable, content not scanned: <path>` rather than
   silently treated as clean. Separately diffs the full repo tree against
   the baseline manifest at `/tmp/spike006-pre.txt` and fails on any file
   that is both new and outside
   `content/21-challenges/materials/challenge-three/` and
   `lab/challenge-three/`.
9. **Opening letter cash ties to statements.** Per account,
   `opening_position.json`'s `cash_by_account[code].amount_cents` equals
   that account's first in-period statement's `opening_balance` exactly
   (§5 ruling 5).

An entry/line is **evidenced** (checks 5 and 6) iff its `doc_ids` is
non-empty, every id resolves in `documents.jsonl`, and the resolved
`path` exists on disk under the repo root. There is no exemption list —
transfers cite both statements, bank fees cite the statement, opening
entries cite the opening letter. Do not invent a category of ledger line
that is allowed to skip `doc_ids`.

---

## 9. `lib/render.py` — what's available (for reference; frozen)

- `render_html_to_pdf(html, out_path, css=None)` — text PDF via the
  `weasyprint` CLI (shelled out to, not imported — it's pipx-installed in
  its own venv on this environment).
- `scanify(src_pdf_path, out_pdf_path, seed, dpi=200, jpeg_quality=75,
  max_rotation_deg=0.7)` — rasterises via ghostscript (not
  ImageMagick/`convert`, which is commonly policy-blocked from reading
  PDFs), degrades in Pillow, re-embeds as an image-only PDF via reportlab.
  Verified OCR-legible with `tesseract` (dates, counterparty, totals
  recoverable) and under 500KB/page on a dense table page — see the
  comment at its noise step for the size/quality tradeoff before touching
  parameters; if you need to run OCR yourself for QA, use
  `tesseract <page.png> out --psm 6`, not the default `--psm 3`, which can
  fail completely on a sparse page (a known tesseract quirk, unrelated to
  scan quality).
- `photograph_receipt(src_image_path, out_jpg_path, seed)` — perspective
  warp, rotation, uneven lighting, JPEG artefacts.
- `handwritten_note_image(lines, out_jpg_path, seed, ...)` — renders short
  text with per-word jitter, then runs it through `photograph_receipt()`.
- `concat_pdfs(pdf_paths, out_path)` — merges several PDFs into one
  multi-document PDF.
- `render_docx(out_path, title, paragraphs, table_rows=None)` — via
  `python-docx`.
- `render_xlsx(out_path, sheets)` — via `openpyxl`, `sheets` is
  `{sheet_name: [[row...], ...]}`.
- `write_csv(out_path, rows, header=None)`.

Every function that makes a random choice takes a mandatory `seed: int`
and builds its own local `random.Random(seed)` — never draw from the
global `random` module, and never call these without a seed. This is what
makes a given company's generation deterministic and reproducible.

---

## 10. `lib/ledger.py` — what's available (for reference; frozen)

`CHART` (the chart of accounts dict, §1.5), `CASH_ACCOUNTS`,
`NY_SALES_TAX_QUARTERS` (§5 ruling 7), plus: `read_ledger`/`write_ledger`,
`read_documents`/`write_documents`, `read_statements`/`write_statements`,
`read_opening_position`/`write_opening_position` (deterministic sort order
on every write), `account_balance_cents`, `running_balance`,
`trial_balance`, `entry_balances`, `unbalanced_entries`,
`balance_sheet_totals`, `filter_period`. Import as
`from lib import ledger as L` after adding `lab/challenge-three` to
`sys.path` (see `validate.py` for the pattern), or run your generator
script from within `lab/challenge-three/<slug>/` and adjust the relative
import path accordingly.

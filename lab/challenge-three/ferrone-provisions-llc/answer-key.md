# Ferrone Provisions LLC — Answer Key

Period: **1 January 2025 – 31 December 2025**. Generated deterministically by
`generate.py` (seed `34871271`). This file, the four `lab/challenge-three/
ferrone-provisions-llc/*.jsonl|.json` data files, and this answer key are the
solution artifacts and never ship to the reader — only
`content/21-challenges/materials/challenge-three/ferrone-provisions-llc/`
ships.

## 1. Company

Ferrone Provisions LLC, a New York LLC based at 4102 3rd Avenue, Sunset Park,
Brooklyn, NY 11232 (EIN 99-4471256). Specialty Italian food importer /
wholesaler selling to restaurants and small grocers, with a minority of
taxable direct sales. Two members: Antonio Ferrone ("A. Ferrone", capital
account 3000) and Lucia Ferrone ("L. Ferrone", capital account 3010). Four
employees on GothamPay Payroll Services. Banks at Narrows Point Savings Bank
(operating account ****4417, payroll account ****2290). Prior accountants:
Doria & Marsh CPAs LLP. Current bookkeeping/compliance: Ridgewood Ledger
CPAs.

## 2. Profit & Loss, year ended 31 December 2025

| | |
|---|---:|
| Sales Revenue (net of the cancelled invoice, Defect 5) | $1,705,000.00 |
| Cost of Goods Sold (incl. $3,200.00 period-end shrinkage) | $1,230,800.00 |
| **Gross Profit** | **$474,200.00** |
| Rent Expense | $78,000.00 |
| Utilities Expense | $11,559.07 |
| Wages Expense | $192,000.00 |
| Payroll Tax Expense | $17,280.00 |
| Office Supplies Expense | $2,400.00 |
| Insurance Expense | $9,600.00 |
| Professional Fees Expense | $6,000.00 |
| Bank Fees Expense | $508.35 |
| Vehicle Expense | $1,320.42 |
| Telephone & Internet Expense | $3,148.94 |
| Miscellaneous Expense | $52.00 |
| **Total Operating Expenses** | **$321,868.78** |
| **Net Income** | **$152,331.22** |

Sales tax collected from taxable customers is never revenue — it posts
directly to Sales Tax Payable (2100) on the same entry as the sale, per
SPEC §1.5. Revenue above is wholesale/retail subtotal only. Utilities,
telephone and bank fees carry realistic month-to-month variation (seasonal
refrigeration/HVAC load, occasional overage and wire charges) rather than
flat recurring constants — only the fixed monthly lease (Rent) is a true
constant, as a real lease would be.

## 3. Balance Sheet as of 31 December 2025

| Assets | |
|---|---:|
| Cash – Operating | $98,420.72 |
| Cash – Payroll | $30,000.00 |
| Accounts Receivable | $495,325.00 |
| Inventory | $96,591.00 |
| **Total Assets** | **$720,336.72** |

| Liabilities | |
|---|---:|
| Accounts Payable | $208,393.00 |
| Sales Tax Payable | $2,662.50 |
| **Total Liabilities** | **$211,055.50** |

| Equity | |
|---|---:|
| Member Capital – A. Ferrone (3000) | $220,000.00 |
| Member Capital – L. Ferrone (3010) | $246,800.00 |
| Member Distributions – A. Ferrone (3020, contra) | ($61,850.00) |
| Member Distributions – L. Ferrone (3030, contra) | ($48,000.00) |
| **Total Capital (net of distributions)** | **$356,950.00** |
| Net Income – current period (not yet closed to capital) | $152,331.22 |
| **Total Equity** | **$356,950.00 + $152,331.22 = $509,281.22** |

**Total Liabilities + Equity = $720,336.72**, tying to Total Assets (the
ledger does not close net income into capital at period end, so a
balance sheet drawn from the raw ledger shows current-period net income as
its own equity line, exactly as a pre-closing trial-balance-derived
balance sheet would).

## 4. Trial Balance as of 31 December 2025

| Code | Account | Balance (own normal side) |
|---|---|---:|
| 1000 | Cash - Operating | $98,420.72 |
| 1010 | Cash - Payroll | $30,000.00 |
| 1200 | Accounts Receivable | $495,325.00 |
| 1300 | Inventory | $96,591.00 |
| 2000 | Accounts Payable | $208,393.00 |
| 2100 | Sales Tax Payable | $2,662.50 |
| 3000 | Member Capital - A. Ferrone | $220,000.00 |
| 3010 | Member Capital - L. Ferrone | $246,800.00 |
| 3020 | Member Distributions - A. Ferrone | $61,850.00 |
| 3030 | Member Distributions - L. Ferrone | $48,000.00 |
| 4000 | Sales Revenue | $1,705,000.00 |
| 5000 | Cost of Goods Sold | $1,230,800.00 |
| 6000 | Rent Expense | $78,000.00 |
| 6010 | Utilities Expense | $11,559.07 |
| 6020 | Wages Expense | $192,000.00 |
| 6030 | Payroll Tax Expense | $17,280.00 |
| 6050 | Office Supplies Expense | $2,400.00 |
| 6060 | Insurance Expense | $9,600.00 |
| 6070 | Professional Fees Expense | $6,000.00 |
| 6080 | Bank Fees Expense | $508.35 |
| 6110 | Vehicle Expense | $1,320.42 |
| 6150 | Telephone & Internet Expense | $3,148.94 |
| 6900 | Miscellaneous Expense | $52.00 |

`validate.py` check 7 verifies: Assets ($720,336.72) = Liabilities + Equity
+ Income − Expense ($211,055.50 + $356,950.00 + $1,705,000.00 −
$1,552,668.78 = $720,336.72). ✓ Note: `lib/ledger.py`'s
`balance_sheet_totals()` sums each account **type** in that type's
canonical direction (assets/expenses debit-positive; liabilities/
equity/income credit-positive) rather than each account's own
`normal_side` — this is what correctly *subtracts* the contra-equity
distribution accounts (3020/3030) from the equity bucket instead of
adding them. Distributions are posted only to 3020/3030 all year, exactly
as SPEC §1.5 directs, with no year-end closing entry needed or used.

## 5. Unpaid at period end (Mandated Defect 4)

**Accounts Receivable — 4 invoices unpaid at 31 Dec 2025** (total
$495,325.00 outstanding AR):
- INV-1021, Trattoria Rosso NYC, $210,000.00, issued 2025-11-05
- INV-1022, Amalfi Table Catering, $32,662.50, issued 2025-11-15
- INV-1023, Trattoria Rosso NYC, $220,000.00, issued 2025-12-05
- INV-1024, Amalfi Table Catering, $32,662.50, issued 2025-12-15

**Accounts Payable — 4 bills unpaid at 31 Dec 2025** (total $208,393.00
outstanding AP — each import vendor's final Q4 shipment, still within its
Net 30 term at period end):
- FP-4006, Salumeria Adriatica Import Co., $57,926.00, issued 2025-11-05
- FP-4012, Molino d'Oro Pasta Imports LLC, $40,361.00, issued 2025-11-13
- FP-4018, Caseificio Del Ponte USA, $54,945.00, issued 2025-10-27
- FP-4023, Frantoio Import Traders, $55,161.00, issued 2025-11-25

## 6. The ten mandated defects

**1. Duplicate receipt (same purchase, two formats).** The Molino d'Oro
Pasta Imports LLC shipment ($39,279.00, 2025-02-11) is billed once as a
text-PDF vendor invoice (`bills-in/2025-02/FP-4007.pdf`, doc
`DOC-BILL-0007` — this is the document actually cited in `ledger.jsonl`)
and appears a second time as a photographed delivery receipt / packing
slip (`receipts/receipt-molino-doro-delivery.jpg`, doc `DOC-RCT-0001`).
The second document is registered in `documents.jsonl` but is never cited
by any `ledger.jsonl` line — a naive ingestion process that assumes every
document is a distinct transaction would double the $39,279.00 purchase.
**Correct treatment: book the purchase once, from the bill; the packing
slip is corroborating evidence for the same purchase, not a second one.**

**2. Personal expense misfiled as a business expense.** A. Ferrone's
$1,850.00 JetAzzurro Airlines flight (JFK–NAP–JFK, 2025-07-18), charged to
the operating card, is evidenced by `receipts/receipt-jetazzurro-flight.jpg`
(doc `DOC-RCT-0002`). It is booked as a debit to **3020 Member
Distributions – A. Ferrone**, credit Cash – Operating — never to an expense
account. **Correct treatment: owner draw, not a deductible business
expense.**

**3. Inter-account transfers (operating ↔ payroll).** Twelve monthly
transfers fund the payroll account three days ahead of each pay date. Each
appears as an "out" line on the operating statement and an "in" line on
the payroll statement for the same entry_id, with no income or expense leg
on either side (`validate.py` check 4). **Correct treatment: a transfer
between the company's own accounts — income to neither account.**

**4. See §5 above** (≥4 unpaid sales invoices, ≥4 unpaid vendor bills).

**5. Cancelled invoice via credit note.** Invoice INV-1025 to Ponte Vecchio
Ristorante ($6,200.00 subtotal, non-taxable wholesale, issued 2025-03-12)
is fully cancelled by Credit Note CN-2025 (2025-04-10,
`invoices-out/2025-04/CN-2025.pdf`, doc `DOC-CN-0001`), reason: "Order
cancelled in transit; goods returned to inventory undamaged." Both the
revenue/AR ($6,200.00) and the COGS/inventory relief booked against the
March sale ($4,464.00) are reversed in April. The credit note itself is
itemised with the returned goods — see §10.1 for exactly how a reader
reaches the $4,464.00 figure from the folder alone, with no undisclosed
margin assumption. **Correct treatment: zero net effect on 2025 revenue,
COGS and AR — the invoice and its credit note net to nothing and must not
be counted as a completed sale.**

**6. Inconsistent date formats.** Deliberate and confined to
`documents.jsonl`'s `issued_date` and the rendered documents themselves
(never in `ledger.jsonl`/`statements.jsonl`/`opening_position.json`, which
are always ISO). Invoices and credit notes print US slash dates (e.g.
`04/10/2025`); goods bills print ISO dates (e.g. `2025-02-11`); the
handwritten receipt prints `9/15/25`; the fuel and personal-expense
receipts print day-month-year (e.g. `18 Jul 2025`); the opening letter and
payroll summaries print long-form prose dates (e.g. `January 15, 2025`);
the CSV export prints `07/02/2025` for its own issuance stamp but ISO
inside its transaction rows. **Correct treatment: normalize on ingestion;
do not infer month/day order from a single source.**

**7. Handwritten-looking cash receipt.** `receipts/receipt-handwritten-cash-
tip.jpg` (doc `DOC-RCT-0007`, kind `cash_receipt_handwritten`): $52.00 cash
reimbursement to D. Wu for a driver's toll and parking, dated `9/15/25`,
rendered via jittered handwriting text then photographed at an angle.
Booked to 6900 Miscellaneous Expense. **Correct treatment: a legitimate
small reimbursed expense; evidenced despite the informal source document.**

**8 / 9.** Not applicable to Ferrone (Bright Harbor's credit card and loan
amortisation defects).

**10. CSV bank export duplicates Jan–Jun PDF statements.**
`bank/operating/export/operating-export-2025-01-to-06.csv` (doc
`DOC-CSVOP-0001`) mirrors the same six months already covered by
`bank/operating/2025-01.pdf` through `2025-06.pdf`, using different column
headers (`Txn Date, Memo, Debit Amount, Credit Amount, Running Balance` vs.
the PDF's `Date, Description, Withdrawals, Deposits, Balance`) and an ISO
date column instead of the PDF's US-slash dates. It is registered in
`documents.jsonl` but is **not** cited by any `ledger.jsonl` line — the six
months of activity it contains are already fully booked and evidenced by
the PDF statements. **Correct treatment: this file is a duplicate view of
January–June, not six additional months of activity; a reader who sums
both sources double-counts H1 2025 entirely.**

## 7. Opening AR/AP settlement (Rule Two)

The prior CPA firm's closing letter (`opening/opening-letter.pdf`, doc
`DOC-OPEN-0001`) states non-zero opening receivables and payables as of
31 December 2024:
- AR: Trattoria Rosso NYC $22,000.00; Trattoria Vialardi $18,000.00
- AP: Salumeria Adriatica Import Co. $15,000.00; Molino d'Oro Pasta Imports
  LLC $12,000.00

These settle in January 2025 (AR: 2025-01-12 and 2025-01-19; AP: 2025-01-15
and 2025-01-22), each appearing as an ordinary line on the January
operating bank statement. **Both settlements are excluded from 2025 income
and expense** — they are pure balance-sheet movements (cash for
receivable, payable for cash), not new 2025 sales or purchases.

## 8. NY sales tax mechanics (SPEC §5 ruling 7)

Only Amalfi Table Catering lacks a resale certificate and is charged NY
sales tax at 8.875%; every other wholesale customer is resale-exempt (the
invoice still prints Subtotal / Sales Tax / Total as three lines, with
Sales Tax shown as $0.00 and labelled "Resale Exempt" for exempt
customers, per the mandate that all Ferrone invoices show the three-line
breakdown). Sales tax collected is tracked by calendar month, then remitted
using `NY_SALES_TAX_QUARTERS` (not calendar quarters):

| Remittance date | Filing period | Amount |
|---|---|---:|
| 2025-03-20 | 1 Dec 2024 – 28 Feb 2025 | $4,306.25 (= $1,200.00 opening slice + Jan $1,331.25 + Feb $1,775.00) |
| 2025-06-20 | 1 Mar – 31 May 2025 | $5,502.50 |
| 2025-09-20 | 1 Jun – 31 Aug 2025 | $5,857.50 |
| 2025-12-20 | 1 Sep – 30 Nov 2025 | $7,277.50 |

The opening letter and `opening_position.json`'s `other_balances["2100"]`
carry the **1–31 December 2024** slice ($1,200.00) — the portion of the
Dec 2024–Feb 2025 filing period that had accrued before the books opened,
correctly remitted with the March 2025 payment rather than assumed to be
zero. The 31 December 2025 Sales Tax Payable balance ($2,662.50) is exactly
December 2025's collections, since the Dec 2025–Feb 2026 filing period
isn't due until 20 March 2026 — it is **not** a calendar-quarter-end
balance.

## 9. Distributions

Both members draw $27,000.00/quarter combined ($15,000.00 A. Ferrone /
$12,000.00 L. Ferrone) on 2025-03-28, 06-27, 09-26 and 12-29, each an
identifiable operating-account withdrawal whose memo names the member,
posted to the dedicated Member Distributions contra accounts (3020/3030)
through the year, plus the $1,850.00 personal-flight reclassification
(Defect 2, §6). Full-year totals: $61,850.00 (A. Ferrone) and $48,000.00
(L. Ferrone). These remain as standalone contra-equity balances at period
end — no closing entry is posted (see §4) — and the balance sheet (§3)
presents them as a deduction from gross member capital.

## 10. Inventory

Opening inventory (per the physical count `inventory/stock-count-2024-12-
31.xlsx`, doc `DOC-STOCKOPEN-0001`) was $175,000.00. Purchases from the
four import vendors totalled $1,152,391.00 across 28 irregular shipments —
each vendor receives a different number of shipments per quarter at
irregular dates and sizes (not a flat quarterly constant), weighted toward
Q3 (**$455,727.00**, nearly double Q1's $209,359.00 and noticeably above
Q4's $253,904.00) to build stock ahead of the Q4 holiday wholesale spike
(Rule Four). Perpetual COGS relief posts monthly at (internally) 72% of
that month's invoiced subtotal ($1,235,264.00 gross COGS debits across the
year, including the $3,200.00 period-end shrinkage), net $1,230,800.00
after the $4,464.00 Defect 5 reversal. **The 72% rate itself is never
printed in any shipped document and is not needed to reach either
current-period figure that used to depend on it — see §10.1.** The annual
COGS total remains independently reachable from the folder via the
periodic formula: opening inventory ($175,000.00) + purchases
($1,152,391.00) − closing inventory ($96,591.00) = $1,230,800.00, matching
§2 exactly.

The closing physical count (`inventory/stock-count-2025-12-31.xlsx`, doc
`DOC-STOCKCLOSE-0001`) found $96,591.00 on hand — inventory drew down over
the year because purchases, while heavily weighted to Q3, did not fully
keep pace with the much larger Q4 sales volume, consistent with a
wholesaler selling through its holiday build. Both stock counts carry
quantity, unit cost and extended-total columns per SKU (SPEC ruling 4) —
the extended-total column is the raw count, not a forbidden derived total.

### 10.1 Reaching the $4,464.00 and $3,200.00 figures from the folder alone

These two figures previously rested on the undisclosed 72% margin and were
not independently verifiable. Both are now reachable from shipped source
documents only, with no ledger, spec, answer key or generator:

**$4,464.00 COGS/inventory reversal (Defect 5).** Credit Note CN-2025
(`invoices-out/2025-04/CN-2025.pdf`) is itemised with a "Goods returned to
inventory in good order" table giving SKU and quantity (deliberately no
unit cost or dollar total on this document — it is issued *to* the
customer, Ponte Vecchio Ristorante, and a wholesaler does not disclose its
landed cost, and therefore its margin, to the party it sold to):

| SKU | Description | Qty Returned |
|---|---|---:|
| SAL-002 | Parmigiano Reggiano DOP, wheel (~80lb) | 2 |
| SAL-005 | Prosciutto di Parma DOP, whole leg (~16lb) | 12 |

A reader prices these same two SKUs from either physical stock count's own
Unit Cost column — `inventory/stock-count-2024-12-31.xlsx` and
`inventory/stock-count-2025-12-31.xlsx` both price SAL-002 at $912.00/wheel
and SAL-005 at $220.00/leg identically (SPEC ruling 4 permits a stock
count's own unit-cost and extended-total columns as raw count data, not a
forbidden derived total):

2 × $912.00 + 12 × $220.00 = $1,824.00 + $2,640.00 = **$4,464.00**

**$3,200.00 inventory shrinkage.** The closing stock count
(`inventory/stock-count-2025-12-31.xlsx`) carries both a "Book Qty
(Perpetual)" and a "Qty Counted (Physical)" column, plus Unit Cost and a
"Variance vs. Book" column, computed on the sheet itself. The only nonzero
row is SAL-006 (Aged Balsamic Vinegar of Modena, case): Book Qty 30, Qty
Counted 22, Unit Cost $400.00. (30 − 22) × $400.00 = **$3,200.00**. Every
other SKU's book and counted quantities match (variance $0.00), so the
sheet's own Variance total ties to $3,200.00 without consulting any other
document. The physical count is the source document; the "book" quantity
is what the perpetual (year-round) inventory ledger says should be on
hand, and the count's own numbers show exactly where and by how much the
two diverge — normal shrinkage/breakage reconciliation practice, not a
forbidden current-period derived total (SPEC ruling 4: a stock count's own
extended-total and reconciliation columns are the raw count, not a P&L,
balance sheet, trial balance or year-end summary).

## 11. Quarterly shape (Rule Four)

| Quarter | Revenue (net of Defect-5 reversal) | Purchases | Note |
|---|---:|---:|---|
| Q1 (Jan–Mar) | $306,200.00 | $209,359.00 | baseline (includes the $6,200.00 invoice later cancelled in Q2) |
| Q2 (Apr–Jun) | $323,800.00 | $233,401.00 | baseline growth (net of the $6,200.00 April credit note) |
| Q3 (Jul–Sep) | $355,000.00 | $455,727.00 | inventory build ahead of Q4; purchases well above sales, cash draws down (operating cash briefly dips to ~$57k in September) |
| Q4 (Oct–Dec) | $720,000.00 | $253,904.00 | holiday wholesale spike, ~2.2x the Jan–Sep monthly average |

(Quarterly revenue figures sum to $1,705,000.00, matching the annual P&L
in §2.) January 2025 cash receipts are boosted by the settlement of the
two opening AR balances (§7), the "January receivables catch-up" called
for by Rule Four.

## 12. File budget

102 files, 2,317,648 bytes (2.32 MB) under
`content/21-challenges/materials/challenge-three/ferrone-provisions-llc/`
— within the ≤12 MB / 80–110 file budget. Format breakdown: 91 PDF (text
and image-only scanned), 7 JPG, 3 XLSX, 1 CSV — no DOCX/TXT, consistent
with Ferrone's "tidy client" shape (Rule Five) and satisfying "no company
uses only one format" (SPEC §6). The expense side alone carries 28
irregular vendor shipment bills plus insurance/packaging/professional-fee
bills, deliberately dense and lumpy rather than a handful of clean
recurring constants.

# Halloran & Vance Design Partners -- Answer Key (Challenge Three)

Fiscal year ended 30 June 2025 (period 2024-07-01 to 2025-06-30). Source
documents span July 2024 through August 2025 (fourteen months); the
July-August 2025 trailing stub is bank-reconciled and document-evidenced
like every other month but is **excluded** from every figure in this answer
key and from the period balance sheet / P&L below (validator check 7 scopes
it out the same way).

## 1. Profit-sharing ratio and the trailing stub

Per the prior CPA firm's closing letter (`content/21-challenges/materials/challenge-three/halloran-vance-design/000001_2024-07-03_closing-financials-june-30/opening_letter.pdf`), profits and
losses are shared **60% to Margaret Halloran / 40% to Owen Vance**. This
ratio is informational prose from the opening letter; it is not journaled
as an automatic allocation of current-year income into the partners'
capital accounts anywhere in `ledger.jsonl` (doing so would require a
current-period-derived net-income figure to be committed to a ledger
entry, which is fine internally, but the point of the ratio for this
exercise is descriptive). If a reader wants to state each partner's implied
share of FY2025 net income, it is illustrative, not booked:
Halloran $122,354.72 (60%), Vance $81,569.82 (40%).

The trailing stub (July-August 2025) contains two invoices, one payroll pay
run, ordinary monthly rent/utilities/telephone/insurance/bank-fee/storage
entries, a handful of subcontractor bills, and both partners' draws for
those two months, all bank-reconciled in the July and August 2025
statements. None of it is included in the FY2025 revenue, expense, P&L,
balance sheet, or trial balance figures below -- validator check 7
evaluates strictly as of `period_end` (2025-06-30), and the stub's own
draws/expenses are dated after that, so they never enter the FY2025
accounting identity even though 3120/3130 keep accumulating through August.

## 2. Opening AR/AP settlement treatment

The prior CPA's closing letter as at 30 June 2024 states three opening
receivables (Bellcourt Retail Group, Ansel Family Residence, Larkspur
Hospitality LLC; combined $80,400.00) and three
opening payables (Reyes Drafting Studio, Ionescu Lighting Consultants,
Tribeca Paper & Print Co; combined $16,400.00).
Each is collected/paid in full within the first quarter of the period
(entries `OBSETTLE-AR-*` / `OBSETTLE-AP-*` in `ledger.jsonl`, dated
July-September 2024) and appears as an ordinary deposit/withdrawal on the
relevant month's bank statement. None of these six settlements touch
Sales Revenue (4000) or any expense account -- they clear a receivable or
payable that was already recognized as at 30 June 2024, so booking them
to income/expense in FY2025 would double count revenue/expense already
implicitly recognized in the prior period. Evidenced by the opening letter
(`content/21-challenges/materials/challenge-three/halloran-vance-design/000001_2024-07-03_closing-financials-june-30/opening_letter.pdf`) plus the relevant month's bank statement.

## 3. Mandated defects

### Defect 1 -- duplicate receipt (same purchase, two formats)

The $215.00 Tribeca Paper & Print Co purchase on
2024-09-11 is shipped **twice**: once as a clean text-native PDF receipt
emailed the same month (`content/21-challenges/materials/challenge-three/halloran-vance-design/000006_2024-09-27_invoices-bills-payroll-september/tribeca_paper_receipt.pdf`), and again a month later as a
photographed JPG attached to the September self-maintained expense log
(`content/21-challenges/materials/challenge-three/halloran-vance-design/000007_2024-10-08_september-expense-log/receipt_tribeca_paper_print_co_2024-09-11.jpg`). There is exactly **one** real ledger entry for this
expense (`SUPPLIES-001`, debit 6050 / credit 1000, 2024-09-11), which cites
the PDF receipt's `doc_id` plus that month's bank statement. The
photographed JPG is a real shipped file but is deliberately **not**
referenced by any ledger line --
a naive ingestion pass that treats every shipped receipt as a distinct
transaction will double-count this $215.00. Correct
treatment: one expense, $215.00, Office Supplies Expense.

### Defect 2 -- personal expense on the business account

A $612.00 Atlantic Crest Airlines round-trip (Margaret
Halloran's personal weekend trip to Miami, 2025-02-14) was charged to
the firm's operating account. Receipt at `content/21-challenges/materials/challenge-three/halloran-vance-design/000016_2025-02-26_invoices-bills-payroll-february/atlanticcrest_receipt_personal.pdf`; the same
month's email batch (`content/21-challenges/materials/challenge-three/halloran-vance-design/000016_2025-02-26_invoices-bills-payroll-february/body.txt`) has
Margaret flagging it explicitly. Correct treatment: **not** a business
expense -- booked as a debit to Partner Draws - Halloran (3120), credit
Cash (1000), entry `PERSONAL-001`. It stands in 3120 alongside her other
FY2025 monthly draws (no closing entry moves it anywhere); see &sect;4 for
how the open draws balance is netted into equity at period end.

### Defect 4 -- AR and AP unpaid at period end

At least four sales invoices and at least four vendor bills remain unpaid
as of 30 June 2025.

Unpaid sales invoices (accounts receivable, 5 clients,
$135,000.00 total):
- Fenwick Hospitality Group: $23,000.00
- Larkspur Hospitality LLC: $25,000.00
- Meridian Law Offices: $27,000.00
- Pemberton Townhouse: $28,000.00
- Whitfield Family Trust: $32,000.00

Unpaid vendor bills (accounts payable, by vendor; 8 vendors
carrying open balances):
- Bellweather Procurement & FF&E Sourcing: $13,500.00
- Cobalt Structural Engineering PLLC: $9,200.00
- Fillmore Bookkeeping & Tax LLC: $1,050.00
- Gramercy Print & Copy: $2,600.00
- Ionescu Lighting Consultants: $9,000.00
- Rendercraft Visualization Studio: $8,800.00
- Reyes Drafting Studio: $12,400.00
- Third Rail Code & Egress Consulting: $2,200.00

Individually, 12 separate bills are unpaid at period end
(most of them pages inside a monthly bundled attachment rather than their
own file -- see the `vendor_bills_<month>.pdf` documents):
- Rendercraft Visualization Studio (issued 2025-03-14): $4,600.00
- Third Rail Code & Egress Consulting (issued 2025-04-16): $2,200.00
- Cobalt Structural Engineering PLLC (issued 2025-05-16): $9,200.00
- Bellweather Procurement & FF&E Sourcing (issued 2025-05-19): $13,500.00
- Reyes Drafting Studio (issued 2025-05-20): $6,600.00
- Ionescu Lighting Consultants (issued 2025-05-23): $4,800.00
- Gramercy Print & Copy (issued 2025-05-27): $1,200.00
- Rendercraft Visualization Studio (issued 2025-06-11): $4,200.00
- Reyes Drafting Studio (issued 2025-06-18): $5,800.00
- Ionescu Lighting Consultants (issued 2025-06-20): $4,200.00
- Gramercy Print & Copy (issued 2025-06-20): $1,400.00
- Fillmore Bookkeeping & Tax LLC (issued 2025-06-30): $1,050.00

This satisfies the "at least four vendor bills unpaid" requirement on a
bill-count basis as well as a vendor-count basis. Correct treatment: these
remain live Accounts Receivable (1200) / Accounts Payable (2000) balances
at period end; revenue and expense were already recognized on invoice/bill
issuance, so no further P&L impact at collection/payment.

### Defect 6 -- inconsistent date formats across sources

`documents.jsonl`'s `issued_date` field (and the documents themselves)
deliberately vary date format by rotating through three styles as invoices
and bills are issued, e.g. invoice HV-1041 shows
`07/08/2024`, invoice HV-1042 shows
`2024-07-22`, and invoice HV-1043 shows
`7 Aug 2024` -- MM/DD/YYYY, ISO YYYY-MM-DD, and "D Mon YYYY"
all appear across the corpus (bills-in rotate through the same three
styles independently). Every date inside `ledger.jsonl`, `statements.jsonl`,
and `opening_position.json` is, as required, always ISO with no
exceptions; only the rendered documents' own printed dates and
`documents.jsonl.issued_date` vary.

### Defect 7 -- handwritten-looking cash receipt, photographed at an angle

A $84.00 hardware purchase from Chelsea Hardware & Supply on
2025-04-11 is evidenced by a handwritten-style receipt image, rendered via
`handwritten_note_image()` and passed through the photograph pass (slight
rotation, perspective warp, uneven lighting): `content/21-challenges/materials/challenge-three/halloran-vance-design/000020_2025-04-29_invoices-bills-payroll-april/chelsea_hardware_receipt.jpg`. Booked
to Repairs & Maintenance Expense (6140), entry `REPAIRS-001`.

### Defects 3, 5, 8, 9, 10 -- not applicable to Halloran & Vance

Inter-account transfers (3) and the cancelled-invoice credit note (5) are
Ferrone Provisions LLC's defects; the credit-card statement (8) and loan
amortization schedule (9) are Bright Harbor Fabrication's. Halloran & Vance
uses a single cash account, has no credit card or loan in its chart of
accounts usage, and issues no credit notes -- none of these apply here.

## 4. Additional structural notes

- **Vendor bill bundling**: most months' subcontractor and vendor bills do
  not arrive as one file per bill -- they are scanned/rendered together
  into a single `vendor_bills_<month>.pdf` (kind `multi_document_bundle`),
  the way a real client actually forwards a stack of paperwork in one
  attachment. Each individual bill inside is still its own `ledger.jsonl`
  entry (its own amount, date, and account code); all of that month's bill
  entries simply cite the same bundle `doc_id`. A vendor's bill is page N
  of that file, not its own filename -- check the attachment note in each
  `body.txt` for which vendors are inside before assuming a bundle is a
  single transaction. The November 2024 bundle
  (`content/21-challenges/materials/challenge-three/halloran-vance-design/000010_2024-11-26_invoices-bills-payroll-november/vendor_bills_2024-11.pdf`)
  is image-only (scanned) and needs OCR; the rest are text-native PDFs.
- **"Two regular subcontractors" (SPEC &sect;2)**: Reyes Drafting Studio
  (drafting) and Ionescu Lighting Consultants (lighting) are the two
  regular, near-monthly subcontractors. Cobalt Structural Engineering
  PLLC, Rendercraft Visualization Studio, Third Rail Code & Egress
  Consulting, and Bellweather Procurement & FF&E Sourcing are occasional,
  project-linked sub-consultants billing only when a specific phase (most
  often the Whitfield hospitality project) needs their scope -- together
  with Reyes and Ionescu they make up the full Subcontractor Expense
  (6040) balance below.
- **Revenue recognition**: every dollar of Sales Revenue (4000) traces to
  an issued invoice document (`invoice_out`); there is no unbilled/WIP
  revenue anywhere in `ledger.jsonl`.
- **Partner capital contribution**: Owen Vance contributed an additional
  $45,000.00 on 2024-12-02, evidenced by a deposit on
  that month's bank statement plus a short note (`content/21-challenges/materials/challenge-three/halloran-vance-design/000012_2024-12-23_whitfield-milestone-invoice-capital-december/vance_capital_contribution_note.txt`); entry
  `CAPCONTRIB-001` (debit 1000 / credit 3110).
- **Partner draws**: recurring monthly withdrawals, different per partner
  (Halloran $6,500.00/month, Vance $4,800.00/month),
  posted to the contra-equity Draws accounts (3120/3130) and left standing
  open at period end -- Halloran $78,612.00, Vance
  $57,600.00 through 2025-06-30. No closing entry moves them; each
  individual draw is evidenced by its own dated bank withdrawal.
  `lib/ledger.py`'s `balance_sheet_totals` (and the trial-balance/equity
  figures below) net every equity-type account by its own debit/credit
  activity, so these debit balances correctly reduce total equity rather
  than inflate it -- no derived closing entry is needed for the accounting
  identity (validator check 7) to hold.
- **Accrued payroll**: Priya Nair's June 2025 salary and employer
  payroll tax (combined $6,480.00) is earned by period end
  but not paid until 2025-07-05 (the payroll provider's regular pay-date
  lag). Accrued at period end to Accrued Payroll Liabilities (2200),
  evidenced by the payroll provider's advance notice
  (`content/21-challenges/materials/challenge-three/halloran-vance-design/000024_2025-06-26_invoices-bills-payroll-june/payroll_accrual_notice_june.pdf`), and
  settled in July against that liability, not against expense again.
- **NY sales tax**: not applicable. Halloran & Vance is a professional
  design-services partnership; its fees are not subject to New York sales
  tax, so account 2100 (Sales Tax Payable) does not appear anywhere in
  this company's ledger.

## 5. Profit & Loss -- fiscal year ended 30 June 2025

| Revenue | Amount |
|---|---|
| Sales Revenue | $714,000.00 |

| Expense | Amount |
|---|---|
| Rent Expense | $67,500.00 |
| Utilities Expense | $6,068.00 |
| Wages Expense | $72,000.00 |
| Payroll Tax Expense | $5,760.00 |
| Subcontractor Expense | $305,200.00 |
| Office Supplies Expense | $22,283.00 |
| Insurance Expense | $7,500.00 |
| Professional Fees Expense | $8,245.00 |
| Bank Fees Expense | $230.00 |
| Advertising & Marketing Expense | $1,350.00 |
| Repairs & Maintenance Expense | $4,284.00 |
| Telephone & Internet Expense | $2,212.46 |
| Miscellaneous Expense | $7,443.00 |
| **Total Expense** | **$510,075.46** |

**Net Income: $203,924.54**

## 6. Balance Sheet -- as at 30 June 2025

| Assets | Amount |
|---|---|
| Cash - Operating (1000) | $154,942.54 |
| Accounts Receivable (1200) | $135,000.00 |
| **Total Assets** | **$289,942.54** |

| Liabilities | Amount |
|---|---|
| Accounts Payable (2000) | $58,750.00 |
| Accrued Payroll Liabilities (2200) | $6,480.00 |
| **Total Liabilities** | **$65,230.00** |

| Equity | Amount |
|---|---|
| Partner Capital - Halloran (3100) | $70,000.00 |
| Partner Capital - Vance (3110) | $87,000.00 |
| Partner Draws - Halloran (3120, contra-equity) | ($78,612.00) |
| Partner Draws - Vance (3130, contra-equity) | ($57,600.00) |
| Current-year net income (undistributed; see &sect;1 for the 60/40 illustrative split) | $203,924.54 |
| **Total Equity** | **$224,712.54** |

**Total Liabilities + Equity: $289,942.54**
(ties to Total Assets above, per validator check 7's accounting identity.)

## 7. Trial Balance -- as at 30 June 2025

| Code | Account | Debit | Credit |
|---|---|---|---|
| 1000 | Cash - Operating | $154,942.54 |  |
| 1200 | Accounts Receivable | $135,000.00 |  |
| 2000 | Accounts Payable |  | $58,750.00 |
| 2200 | Accrued Payroll Liabilities |  | $6,480.00 |
| 3100 | Partner Capital - Halloran |  | $70,000.00 |
| 3110 | Partner Capital - Vance |  | $87,000.00 |
| 3120 | Partner Draws - Halloran | $78,612.00 |  |
| 3130 | Partner Draws - Vance | $57,600.00 |  |
| 4000 | Sales Revenue |  | $714,000.00 |
| 6000 | Rent Expense | $67,500.00 |  |
| 6010 | Utilities Expense | $6,068.00 |  |
| 6020 | Wages Expense | $72,000.00 |  |
| 6030 | Payroll Tax Expense | $5,760.00 |  |
| 6040 | Subcontractor Expense | $305,200.00 |  |
| 6050 | Office Supplies Expense | $22,283.00 |  |
| 6060 | Insurance Expense | $7,500.00 |  |
| 6070 | Professional Fees Expense | $8,245.00 |  |
| 6080 | Bank Fees Expense | $230.00 |  |
| 6130 | Advertising & Marketing Expense | $1,350.00 |  |
| 6140 | Repairs & Maintenance Expense | $4,284.00 |  |
| 6150 | Telephone & Internet Expense | $2,212.46 |  |
| 6900 | Miscellaneous Expense | $7,443.00 |  |
| | **Totals** | **$936,230.00** | **$936,230.00** |

## 8. Corpus stats

- Files: 105
- Total bytes: 4458100 (4.46 MB)
- Format breakdown: {'pdf': 57, 'txt': 30, 'docx': 6, 'jpg': 5, 'xlsx': 7}
- Batches: 29

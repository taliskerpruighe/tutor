#!/usr/bin/env python3
"""
generate.py -- Ferrone Provisions LLC, challenge-three Stage B generator.

Deterministic: every random draw is seeded from SEED. Single source of
truth for lab/challenge-three/ferrone-provisions-llc/{ledger,documents,
statements}.jsonl + opening_position.json, and for the rendered corpus at
content/21-challenges/materials/challenge-three/ferrone-provisions-llc/.

Run with: python3 generate.py
"""

from __future__ import annotations

import calendar
import datetime as dt
import os
import random
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CHALLENGE_DIR = os.path.dirname(os.path.dirname(THIS_DIR))  # lab/challenge-three
LAB_DIR = os.path.dirname(THIS_DIR)  # lab/challenge-three
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "lab", "challenge-three"))

from lib import ledger as L  # noqa: E402
from lib import render as R  # noqa: E402

SEED = 34871271
RNG = random.Random(SEED)

SLUG = "ferrone-provisions-llc"
LAB_OUT = os.path.join(REPO_ROOT, "lab", "challenge-three", SLUG)
MATERIALS_REL = f"content/21-challenges/materials/challenge-three/{SLUG}"
MATERIALS_ABS = os.path.join(REPO_ROOT, MATERIALS_REL)

PERIOD_START = "2025-01-01"
PERIOD_END = "2025-12-31"
AS_OF = "2024-12-31"

# ---------------------------------------------------------------------------
# Entity / roster constants
# ---------------------------------------------------------------------------

COMPANY_NAME = "Ferrone Provisions LLC"
COMPANY_ADDRESS = "4102 3rd Avenue, Sunset Park, Brooklyn, NY 11232"
COMPANY_PHONE = "(718) 555-0148"
COMPANY_EIN = "99-4471256"

MEMBER_A_CODE, MEMBER_A_NAME, MEMBER_A_DIST_CODE = "3000", "A. Ferrone", "3020"
MEMBER_L_CODE, MEMBER_L_NAME, MEMBER_L_DIST_CODE = "3010", "L. Ferrone", "3030"
MEMBER_A_FULL = "Antonio Ferrone"
MEMBER_L_FULL = "Lucia Ferrone"

BANK_NAME = "Narrows Point Savings Bank"
BANK_ADDRESS = "8801 4th Avenue, Brooklyn, NY 11209"
BANK_PHONE = "(718) 555-0199"
OPERATING_ACCT_MASK = "****4417"
PAYROLL_ACCT_MASK = "****2290"
OPERATING_CODE = "1000"
PAYROLL_CODE = "1010"

PRIOR_CPA_FIRM = "Doria & Marsh CPAs LLP"
PRIOR_CPA_ADDRESS = "26 Court Street, Brooklyn Heights, Brooklyn, NY 11201"
PRIOR_CPA_PHONE = "(718) 555-0122"

PAYROLL_PROVIDER = "GothamPay Payroll Services"
PAYROLL_PROVIDER_ADDRESS = "199 Water Street, Financial District, New York, NY 10038"

NY_SALES_TAX_RATE_BPS = 8875  # 8.875%, integer basis points-ish (per 100000)


def tax_cents(subtotal_cents: int) -> int:
    return (subtotal_cents * NY_SALES_TAX_RATE_BPS + 50000) // 100000


def pct_cents(amount_cents: int, pct_bps_per_10000: int) -> int:
    """amount * pct where pct is expressed as parts per 10000 (e.g. 7200 = 72%)."""
    return (amount_cents * pct_bps_per_10000 + 5000) // 10000


def c(dollars: float) -> int:
    return int(round(dollars * 100))


CUSTOMERS = {
    "CU1": {"name": "Trattoria Rosso NYC", "address": "521 7th Avenue, Park Slope, Brooklyn, NY 11215", "taxable": False},
    "CU2": {"name": "Trattoria Vialardi", "address": "88 West Broadway, Tribeca, New York, NY 10013", "taxable": False},
    "CU3": {"name": "Ponte Vecchio Ristorante", "address": "7614 3rd Avenue, Bay Ridge, Brooklyn, NY 11209", "taxable": False},
    "CU4": {"name": "Sunset Gourmet Market", "address": "5309 5th Avenue, Sunset Park, Brooklyn, NY 11220", "taxable": False},
    "CU5": {"name": "Amalfi Table Catering", "address": "215 Metropolitan Avenue, Williamsburg, Brooklyn, NY 11211", "taxable": True},
}

VENDORS = {
    "V1": {"name": "Salumeria Adriatica Import Co.", "address": "160 Columbia Street, Red Hook, Brooklyn, NY 11231", "kind": "goods"},
    "V2": {"name": "Molino d'Oro Pasta Imports LLC", "address": "202 Van Brunt Street, Red Hook, Brooklyn, NY 11231", "kind": "goods"},
    "V3": {"name": "Caseificio Del Ponte USA", "address": "540 39th Street, Sunset Park, Brooklyn, NY 11232", "kind": "goods"},
    "V4": {"name": "Frantoio Import Traders", "address": "4501 2nd Avenue, Sunset Park, Brooklyn, NY 11232", "kind": "goods"},
    "V5": {"name": "Gowanus Paper & Packaging Supply", "address": "88 Nevins Street, Gowanus, Brooklyn, NY 11217", "kind": "packaging"},
    "V6": {"name": "Harborline Business Insurance", "address": "142 Court Street, Cobble Hill, Brooklyn, NY 11201", "kind": "insurance"},
    "V7": {"name": "Ridgewood Ledger CPAs", "address": "6015 Fresh Pond Road, Ridgewood, Queens, NY 11385", "kind": "professional"},
}
UTILITY_NAME = "Narrows Gas & Electric Co."
TELECOM_NAME = "MetroLink Business Telecom"
LANDLORD_NAME = "Sunset Park Realty Holdings LLC"

EMPLOYEES = [
    ("Maria Lopez", "Warehouse Lead", c(4400)),
    ("James Kowalski", "Delivery Driver", c(4000)),
    ("Denise Wu", "Office Administrator", c(3900)),
    ("Carlos Mendes", "Warehouse Associate", c(3700)),
]
MONTHLY_GROSS_PAYROLL = sum(e[2] for e in EMPLOYEES)  # cents
EMPLOYER_TAX_RATE = 900  # 9.00% -> per 10000 = 900

# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

# Bank-facing description overrides, keyed by (entry_id, account_code).
# Ledger `memo` fields stay exactly as SPEC S1.1 wants them -- explicit
# about treatment (e.g. naming a mandated defect in plain language) for a
# human/LLM reviewer reading ledger.jsonl. A real bank statement never
# prints that kind of analyst commentary, only a short transaction
# description -- so the *rendered* statement (and statements.jsonl, which
# SPEC S1.3 defines as "what a human reading the bank statement PDF would
# transcribe by hand") uses this override when present, falling back to
# the memo otherwise.
BANK_DESC: dict[tuple[str, str], str] = {}

LEDGER: list[dict] = []
DOCUMENTS: list[dict] = []
_entry_seq = 0
_doc_seqs: dict[str, int] = {}


def new_entry_id() -> str:
    global _entry_seq
    _entry_seq += 1
    return f"J-{_entry_seq:04d}"


def new_doc_id(prefix: str) -> str:
    _doc_seqs[prefix] = _doc_seqs.get(prefix, 0) + 1
    return f"DOC-{prefix}-{_doc_seqs[prefix]:04d}"


def add_doc(doc_id: str, kind: str, rel_path: str, fmt: str, scanned: bool,
            issued_date_str: str, counterparty: str, amount_cents) -> str:
    DOCUMENTS.append({
        "doc_id": doc_id, "kind": kind, "path": f"{MATERIALS_REL}/{rel_path}",
        "format": fmt, "scanned": scanned, "issued_date": issued_date_str,
        "counterparty": counterparty, "amount": amount_cents,
    })
    return doc_id


def line(code, debit, credit, memo, counterparty, doc_ids):
    assert (debit > 0) != (credit > 0), f"line must have exactly one non-zero side: {code} {debit} {credit}"
    assert doc_ids, f"line on {code} ({memo!r}) has empty doc_ids"
    return {
        "account_code": code, "account_name": L.CHART[code]["name"],
        "debit": debit, "credit": credit, "memo": memo,
        "counterparty": counterparty, "doc_ids": list(doc_ids),
    }


def add_entry(entry_id: str, date_iso: str, lines: list[dict]):
    total_d = sum(l["debit"] for l in lines)
    total_c = sum(l["credit"] for l in lines)
    assert total_d == total_c, f"{entry_id} unbalanced: debit={total_d} credit={total_c}"
    for l in lines:
        rec = dict(l)
        rec["entry_id"] = entry_id
        rec["date"] = date_iso
        LEDGER.append(rec)
    return entry_id


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def d(iso: str) -> dt.date:
    return dt.date.fromisoformat(iso)


def iso(dat: dt.date) -> str:
    return dat.isoformat()


def add_days(iso_str: str, days: int) -> str:
    return iso(d(iso_str) + dt.timedelta(days=days))


def fmt_us_slash(dat: dt.date) -> str:
    return f"{dat.month:02d}/{dat.day:02d}/{dat.year}"


def fmt_dd_mon_yyyy(dat: dt.date) -> str:
    return dat.strftime("%-d %b %Y")


def fmt_long(dat: dt.date) -> str:
    return dat.strftime("%B %-d, %Y")


def money(cents: int) -> str:
    neg = cents < 0
    cents = abs(cents)
    s = f"${cents // 100:,}.{cents % 100:02d}"
    return f"-{s}" if neg else s


def month_bounds(year: int, month: int):
    start = dt.date(year, month, 1)
    end = dt.date(year, month, calendar.monthrange(year, month)[1])
    return start, end


MONTHS_2025 = [f"2025-{m:02d}" for m in range(1, 13)]

# ---------------------------------------------------------------------------
# Pre-register bank statement + CSV export documents (paths known up front so
# ledger cash lines can cite them as they are created).
# ---------------------------------------------------------------------------

STMT_DOC = {}  # (account_code, "YYYY-MM") -> doc_id

for ym in MONTHS_2025:
    y, m = ym.split("-")
    op_doc = new_doc_id("STMTOP")
    add_doc(op_doc, "bank_statement", f"bank/operating/{ym}.pdf", "pdf", False,
             f"{fmt_long(month_bounds(int(y), int(m))[1])}", BANK_NAME, None)
    STMT_DOC[(OPERATING_CODE, ym)] = op_doc

    pr_doc = new_doc_id("STMTPR")
    add_doc(pr_doc, "bank_statement", f"bank/payroll/{ym}.pdf", "pdf", False,
             f"{fmt_long(month_bounds(int(y), int(m))[1])}", BANK_NAME, None)
    STMT_DOC[(PAYROLL_CODE, ym)] = pr_doc

CSV_DOC = new_doc_id("CSVOP")
add_doc(CSV_DOC, "bank_export_csv", "bank/operating/export/operating-export-2025-01-to-06.csv",
        "csv", False, "07/02/2025", BANK_NAME, None)


def stmt_doc_id(account_code: str, date_iso_str: str) -> str:
    ym = date_iso_str[:7]
    return STMT_DOC[(account_code, ym)]


print("Stage 1: constants + statement doc pre-registration done.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Stock-count line items (opening / closing) -- a physical count is a source
# document: quantities, unit costs AND extended totals, summing exactly to
# the target inventory value (SPEC ruling 4).
# ---------------------------------------------------------------------------

STOCK_ITEMS = [
    ("SAL-001", "San Marzano DOP Tomatoes, 28oz case (12ct)"),
    ("SAL-002", "Parmigiano Reggiano DOP, wheel (~80lb)"),
    ("SAL-003", "Extra Virgin Olive Oil, 3L tin, case (4ct)"),
    ("SAL-004", "Dried Pasta Assortment, 500g case (20ct)"),
    ("SAL-005", "Prosciutto di Parma DOP, whole leg (~16lb)"),
    ("SAL-006", "Aged Balsamic Vinegar of Modena, 250ml case (12ct)"),
    ("SAL-007", "Pecorino Romano DOP, wheel (~55lb)"),
    ("SAL-008", "00 Flour, 25lb bag, case (10ct)"),
    ("SAL-009", "Cured Sopressata, case (8ct)"),
    ("SAL-010", "Anchovies in Olive Oil, case (24ct)"),
    ("SAL-011", "Sun-Dried Tomatoes in Oil, case (12ct)"),
    ("SAL-012", "Espresso Beans, 1kg bag, case (10ct)"),
    ("SAL-013", "Arborio Rice, 1kg bag, case (12ct)"),
    ("SAL-014", "Mixed Olives in Brine, case (12ct)"),
]
STOCK_SKU_INDEX = {sku: i for i, (sku, _desc) in enumerate(STOCK_ITEMS)}

# Defect-2 fix: three SKUs whose unit cost is pinned identically across the
# opening count, the closing count, AND (for the first two) the itemised
# credit note -- so a reader pricing goods from any one of these shipped
# documents gets the same per-unit cost as any other. This is what makes
# the credit note's COGS reversal and the closing count's shrinkage line
# independently reachable from the folder alone, with no reliance on the
# undisclosed 72% margin.
CN_ITEM_SKUS = ["SAL-002", "SAL-005"]      # itemised on the cancelled-order credit note
SHRINK_SKU = "SAL-006"                      # the shrinkage line on the closing count
PINNED_UNIT_COST_C = {
    "SAL-002": c(912),   # Parmigiano Reggiano DOP, wheel
    "SAL-005": c(220),   # Prosciutto di Parma DOP, whole leg
    "SAL-006": c(400),   # Aged Balsamic Vinegar of Modena, case -- breakage-prone
}
# Quantities the physical count sheets show on hand for the pinned SKUs
# (independent of how many units any single order/return moves -- a stock
# count's qty is warehouse-on-hand, not a per-transaction quantity).
OPENING_STOCK_PIN_QTY = {"SAL-002": 6, "SAL-005": 20, "SAL-006": 25}
CLOSING_STOCK_COUNTED_QTY = {"SAL-002": 5, "SAL-005": 15, "SAL-006": 22}
SHRINK_UNITS = 8  # SAL-006: perpetual/book qty exceeds the physical count by this many cases


def _pins_from_qty(qty_by_sku: dict) -> dict:
    return {STOCK_SKU_INDEX[sku]: (qty, PINNED_UNIT_COST_C[sku]) for sku, qty in qty_by_sku.items()}


OPENING_STOCK_PINS = _pins_from_qty(OPENING_STOCK_PIN_QTY)
CLOSING_STOCK_PINS = _pins_from_qty(CLOSING_STOCK_COUNTED_QTY)

# Credit-note cost basis: the goods-returned line items (Stage 4) are priced
# at these same pinned per-unit costs. Quantities here are the units
# actually returned on that one order -- chosen so the total ties exactly
# to the COGS reversal the ledger books (72% of the $6,200.00 cancelled
# subtotal = $4,464.00), without ever printing the 72% rate itself anywhere.
CN_RETURN_QTY = {"SAL-002": 2, "SAL-005": 12}
CN_COST_BASIS_C = sum(CN_RETURN_QTY[sku] * PINNED_UNIT_COST_C[sku] for sku in CN_ITEM_SKUS)


def build_stock_count_rows(target_cents: int, seed: int, pins: dict | None = None):
    """pins: optional {sku_index: (qty, unit_cost_cents)} fixing specific rows'
    qty and unit cost exactly (so the same SKU can carry an identical unit
    cost across the opening count, the closing count, and any other shipped
    document that prices goods by SKU -- e.g. the itemised credit note).
    The remaining, non-pinned rows are randomised and scaled as before so
    the sheet's total still lands on target_cents exactly."""
    pins = pins or {}
    rng = random.Random(seed)
    n = len(STOCK_ITEMS)
    # Assign each item a plausible qty and unit cost (dollars), compute
    # extended totals, then scale + plug the last row so the sum matches
    # target_cents exactly.
    rows = []
    running = 0
    for i, (sku, desc) in enumerate(STOCK_ITEMS):
        if i in pins:
            qty, unit_cost_cents = pins[i]
        else:
            qty = rng.randint(8, 60)
            unit_cost_cents = rng.randint(1200, 42000)
        ext = qty * unit_cost_cents
        rows.append([sku, desc, qty, unit_cost_cents, ext])
        running += ext
    scalable = [i for i in range(n) if i not in pins]
    pinned_ext_total = sum(rows[i][4] for i in pins)
    scale_target = target_cents - pinned_ext_total
    scale_running = running - pinned_ext_total
    assert scale_target > 0, f"pinned rows ({pinned_ext_total}) leave no room under target ({target_cents})"
    # Scale all non-pinned extended totals proportionally toward the
    # remaining target, then fix rounding drift on the final scalable row so
    # the sheet sums exactly (pinned rows are never touched by scaling or
    # drift-absorption).
    scale = scale_target / scale_running
    running2 = 0
    for idx in scalable[:-1]:
        row = rows[idx]
        new_ext = int(round(row[4] * scale))
        row[3] = max(1, new_ext // row[2]) if row[2] else new_ext
        row[4] = row[3] * row[2]
        running2 += row[4]
    last_idx = scalable[-1]
    last = rows[last_idx]
    remaining = scale_target - running2
    last[3] = max(1, remaining // last[2]) if last[2] else remaining
    last[4] = last[3] * last[2]
    drift = scale_target - (running2 + last[4])
    if drift != 0:
        # absorb any last-cent drift into the final scalable row's extended
        # total by nudging unit cost (keeps qty x unit_cost = ext exact up
        # to $0.00x -- acceptable for a hand-counted sheet; adjust the last
        # cent onto the extended total directly since real counts
        # occasionally carry a $0.0x rounding note).
        last[4] += drift
    assert sum(r[4] for r in rows) == target_cents
    return rows


def stock_count_sheet_rows(rows):
    header = ["SKU", "Description", "Qty Counted", "Unit Cost", "Extended Total"]
    out = [header]
    total = 0
    for sku, desc, qty, unit_cost_cents, ext in rows:
        out.append([sku, desc, qty, f"${unit_cost_cents/100:,.2f}", f"${ext/100:,.2f}"])
        total += ext
    out.append(["", "", "", "TOTAL", f"${total/100:,.2f}"])
    return out, total


def closing_stock_count_sheet_rows(rows, book_qty_overrides: dict):
    """Like stock_count_sheet_rows, but adds a Book Qty (Perpetual) column
    next to Qty Counted (Physical) for any SKU whose perpetual/book quantity
    differs from what the physical count found. (Book Qty - Qty Counted) x
    Unit Cost is that row's own shrinkage, priced entirely off this sheet's
    own unit-cost column -- no external rate needed. This is still the raw
    count plus its own book-vs-physical reconciliation, not a forbidden
    derived summary (SPEC ruling 4)."""
    header = ["SKU", "Description", "Book Qty (Perpetual)", "Qty Counted (Physical)",
              "Unit Cost", "Extended Total (Counted)", "Variance vs. Book"]
    out = [header]
    total_ext = 0
    total_variance = 0
    for sku, desc, qty, unit_cost_cents, ext in rows:
        book_qty = book_qty_overrides.get(sku, qty)
        variance_c = (book_qty - qty) * unit_cost_cents
        out.append([sku, desc, book_qty, qty, f"${unit_cost_cents/100:,.2f}", f"${ext/100:,.2f}",
                    f"${variance_c/100:,.2f}"])
        total_ext += ext
        total_variance += variance_c
    out.append(["", "", "", "", "TOTAL", f"${total_ext/100:,.2f}", f"${total_variance/100:,.2f}"])
    return out, total_ext, total_variance


# ---------------------------------------------------------------------------
# Opening position: OB-1 entry dated 2024-12-31, opening letter, opening
# stock count.
# ---------------------------------------------------------------------------

OPENING_CASH_OP = c(250000)
OPENING_CASH_PR = c(30000)
OPENING_AR = [("Trattoria Rosso NYC", c(22000)), ("Trattoria Vialardi", c(18000))]
OPENING_AP = [("Salumeria Adriatica Import Co.", c(15000)), ("Molino d'Oro Pasta Imports LLC", c(12000))]
OPENING_INVENTORY = c(175000)
OPENING_SALES_TAX_PAYABLE = c(1200)  # Dec 2024 slice of the Dec-Feb NY quarter

_ar_total = sum(a for _, a in OPENING_AR)
_ap_total = sum(a for _, a in OPENING_AP)
_equity_total = (OPENING_CASH_OP + OPENING_CASH_PR + _ar_total + OPENING_INVENTORY) - (_ap_total + OPENING_SALES_TAX_PAYABLE)
OPENING_CAPITAL_A = c(220000)
OPENING_CAPITAL_L = _equity_total - OPENING_CAPITAL_A
assert OPENING_CAPITAL_L > 0

DOC_OPEN = new_doc_id("OPEN")
DOC_STOCK_OPEN = new_doc_id("STOCKOPEN")

opening_stock_rows = build_stock_count_rows(OPENING_INVENTORY, seed=SEED + 1, pins=OPENING_STOCK_PINS)

ob_lines = []
ob_lines.append(line(OPERATING_CODE, OPENING_CASH_OP, 0, "Opening cash - operating account", "", [DOC_OPEN]))
ob_lines.append(line(PAYROLL_CODE, OPENING_CASH_PR, 0, "Opening cash - payroll account", "", [DOC_OPEN]))
for debtor, amt in OPENING_AR:
    ob_lines.append(line("1200", amt, 0, f"Opening AR - {debtor}", debtor, [DOC_OPEN]))
ob_lines.append(line("1300", OPENING_INVENTORY, 0, "Opening inventory per physical count", "", [DOC_OPEN, DOC_STOCK_OPEN]))
for creditor, amt in OPENING_AP:
    ob_lines.append(line("2000", 0, amt, f"Opening AP - {creditor}", creditor, [DOC_OPEN]))
ob_lines.append(line("2100", 0, OPENING_SALES_TAX_PAYABLE, "Opening NY sales tax payable (Dec 2024 slice)", "NYS Dept. of Taxation and Finance", [DOC_OPEN]))
ob_lines.append(line(MEMBER_A_CODE, 0, OPENING_CAPITAL_A, "Opening member capital - A. Ferrone", MEMBER_A_FULL, [DOC_OPEN]))
ob_lines.append(line(MEMBER_L_CODE, 0, OPENING_CAPITAL_L, "Opening member capital - L. Ferrone", MEMBER_L_FULL, [DOC_OPEN]))
add_entry("OB-1", AS_OF, ob_lines)

print(f"Stage 2: opening position booked. equity_total={_equity_total} A={OPENING_CAPITAL_A} L={OPENING_CAPITAL_L}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Invoice rendering
# ---------------------------------------------------------------------------

INVOICE_CSS = """
body { font-family: Helvetica, Arial, sans-serif; font-size: 12pt; color: #1a1a1a; }
.header { display: flex; justify-content: space-between; border-bottom: 3px solid #7a1f1f; padding-bottom: 10px; }
.company { font-size: 18pt; font-weight: bold; color: #7a1f1f; }
.meta { text-align: right; }
table.items { width: 100%; border-collapse: collapse; margin-top: 20px; }
table.items th, table.items td { border-bottom: 1px solid #ccc; padding: 6px 8px; text-align: left; }
table.items th { background: #f2e9e9; }
.totals { width: 320px; margin-left: auto; margin-top: 10px; }
.totals td { padding: 4px 8px; }
.totals .grand { font-weight: bold; border-top: 2px solid #1a1a1a; }
.billto { margin-top: 20px; }
.terms { margin-top: 30px; font-size: 10pt; color: #444; }
"""


def invoice_html(invoice_no: str, issued: dt.date, customer: dict, subtotal_cents: int,
                  taxable: bool, tax_c: int, terms_note: str = "Net 30") -> str:
    total_c = subtotal_cents + tax_c
    tax_label = "New York Sales Tax (8.875%)" if taxable else "New York Sales Tax (Resale Exempt)"
    return f"""<html><head><style>{INVOICE_CSS}</style></head><body>
<div class="header">
  <div class="company">{COMPANY_NAME}<br><span style="font-size:10pt;font-weight:normal;">{COMPANY_ADDRESS}<br>{COMPANY_PHONE} &middot; EIN {COMPANY_EIN}</span></div>
  <div class="meta"><b>INVOICE</b><br>No. {invoice_no}<br>Date: {fmt_us_slash(issued)}<br>Terms: {terms_note}</div>
</div>
<div class="billto"><b>Bill To:</b><br>{customer['name']}<br>{customer['address']}</div>
<table class="items">
<tr><th>Description</th><th>Qty</th><th>Amount</th></tr>
<tr><td>Wholesale specialty Italian food order &mdash; period ending {fmt_us_slash(issued)}</td><td>1</td><td>{money(subtotal_cents)}</td></tr>
</table>
<table class="totals">
<tr><td>Subtotal</td><td>{money(subtotal_cents)}</td></tr>
<tr><td>{tax_label}</td><td>{money(tax_c)}</td></tr>
<tr class="grand"><td>Total Due</td><td>{money(total_c)}</td></tr>
</table>
<div class="terms">Please remit payment to {COMPANY_NAME} within the stated terms. Thank you for your business.</div>
</body></html>"""


def credit_note_html(cn_no: str, issued: dt.date, orig_invoice_no: str, customer: dict,
                      subtotal_cents: int, tax_c: int, reason: str,
                      return_items: list | None = None, cost_basis_c: int | None = None) -> str:
    # NOTE: deliberately does NOT print unit cost, extended cost or a cost-
    # basis total -- this document is issued TO the customer, and a
    # wholesaler does not disclose its landed cost (and therefore its
    # margin) to the party it sold to. SKU + quantity is enough for the
    # returned-goods record; a reader who wants the dollar cost basis prices
    # these same SKUs off either stock count's own Unit Cost column (see
    # answer-key.md S10.1) -- both counts price SAL-002 and SAL-005
    # identically, so the figure is unambiguous without this document
    # needing to state it.
    total_c = subtotal_cents + tax_c
    return_rows_html = ""
    if return_items:
        for sku, desc, qty, _unit_cost_c in return_items:
            return_rows_html += f"<tr><td>{sku}</td><td>{desc}</td><td>{qty}</td></tr>"
    return_table_html = ""
    if return_items:
        return_table_html = f"""
<p>Goods returned to inventory in good order:</p>
<table class="items">
<tr><th>SKU</th><th>Description</th><th>Qty Returned</th></tr>
{return_rows_html}
</table>"""
    return f"""<html><head><style>{INVOICE_CSS}</style></head><body>
<div class="header">
  <div class="company">{COMPANY_NAME}<br><span style="font-size:10pt;font-weight:normal;">{COMPANY_ADDRESS}<br>{COMPANY_PHONE} &middot; EIN {COMPANY_EIN}</span></div>
  <div class="meta"><b>CREDIT NOTE</b><br>No. {cn_no}<br>Date: {fmt_us_slash(issued)}<br>Ref. Invoice: {orig_invoice_no}</div>
</div>
<div class="billto"><b>Issued To:</b><br>{customer['name']}<br>{customer['address']}</div>
<p>Reason: {reason}</p>
<table class="items">
<tr><th>Description</th><th>Qty</th><th>Amount</th></tr>
<tr><td>Full cancellation of Invoice {orig_invoice_no}</td><td>1</td><td>{money(subtotal_cents)}</td></tr>
</table>
<table class="totals">
<tr><td>Subtotal Credited</td><td>{money(subtotal_cents)}</td></tr>
<tr><td>New York Sales Tax Credited</td><td>{money(tax_c)}</td></tr>
<tr class="grand"><td>Total Credit</td><td>{money(total_c)}</td></tr>
</table>
{return_table_html}
</body></html>"""


# ---------------------------------------------------------------------------
# Monthly sales schedule (dollars, subtotal). CU5 is the only taxable
# customer (a minority of sales collects NY sales tax; the rest is
# resale-exempt wholesale). Amounts hit the Rule Four Q4 spike.
# ---------------------------------------------------------------------------

MONTHLY_INVOICES = {
    "2025-01": [("CU1", 80000), ("CU5", 15000)],
    "2025-02": [("CU1", 80000), ("CU5", 20000)],
    "2025-03": [("CU2", 87000), ("CU5", 18000)],
    "2025-04": [("CU1", 88000), ("CU5", 22000)],
    "2025-05": [("CU2", 86000), ("CU5", 22000)],
    "2025-06": [("CU1", 90000), ("CU5", 22000)],
    "2025-07": [("CU2", 93000), ("CU5", 22000)],
    "2025-08": [("CU1", 96000), ("CU5", 22000)],
    "2025-09": [("CU2", 100000), ("CU5", 22000)],
    "2025-10": [("CU1", 200000), ("CU5", 30000)],
    "2025-11": [("CU1", 210000), ("CU5", 30000)],
    "2025-12": [("CU1", 220000), ("CU5", 30000)],
}
# Invoices left unpaid at 2025-12-31 (>= 4 required).
UNPAID_AT_PERIOD_END = {("2025-11", "CU1"), ("2025-11", "CU5"), ("2025-12", "CU1"), ("2025-12", "CU5")}

INVOICE_DAY_SLOTS = [5, 15, 25]
COGS_RATE_PER_10000 = 7200  # 72% of subtotal

_invoice_no_seq = 1000


def next_invoice_no() -> str:
    global _invoice_no_seq
    _invoice_no_seq += 1
    return f"INV-{_invoice_no_seq}"


monthly_cogs_basis: dict[str, list] = {ym: [] for ym in MONTHS_2025}  # ym -> list of doc_ids
monthly_cogs_subtotal: dict[str, int] = {ym: 0 for ym in MONTHS_2025}

ar_open_unpaid = []  # for answer-key reporting: (invoice_no, customer, amount, date)
ap_open_unpaid = []

for ym in MONTHS_2025:
    y, m = (int(x) for x in ym.split("-"))
    entries = MONTHLY_INVOICES[ym]
    for idx, (cu_key, subtotal_dollars) in enumerate(entries):
        customer = CUSTOMERS[cu_key]
        issued = dt.date(y, m, INVOICE_DAY_SLOTS[idx % len(INVOICE_DAY_SLOTS)])
        subtotal_c = c(subtotal_dollars)
        taxc = tax_cents(subtotal_c) if customer["taxable"] else 0
        total_c = subtotal_c + taxc
        inv_no = next_invoice_no()
        doc_id = new_doc_id("INV")
        rel_path = f"invoices-out/{ym}/{inv_no}.pdf"
        add_doc(doc_id, "invoice_out", rel_path, "pdf", False, fmt_us_slash(issued), customer["name"], total_c)
        R.render_html_to_pdf(
            invoice_html(inv_no, issued, customer, subtotal_c, customer["taxable"], taxc),
            os.path.join(MATERIALS_ABS, rel_path),
        )

        eid = new_entry_id()
        lines = [line("1200", total_c, 0, f"Invoice {inv_no} - {customer['name']}", customer["name"], [doc_id])]
        lines.append(line("4000", 0, subtotal_c, f"Invoice {inv_no} - {customer['name']}", customer["name"], [doc_id]))
        if customer["taxable"]:
            lines.append(line("2100", 0, taxc, f"NY sales tax collected - Invoice {inv_no}", customer["name"], [doc_id]))
        add_entry(eid, iso(issued), lines)

        monthly_cogs_basis[ym].append(doc_id)
        monthly_cogs_subtotal[ym] += subtotal_c

        unpaid = (ym, cu_key) in UNPAID_AT_PERIOD_END
        if unpaid:
            ar_open_unpaid.append((inv_no, customer["name"], total_c, iso(issued)))
        else:
            pay_date = add_days(iso(issued), 25)
            pay_eid = new_entry_id()
            pay_stmt_doc = stmt_doc_id(OPERATING_CODE, pay_date)
            add_entry(pay_eid, pay_date, [
                line(OPERATING_CODE, total_c, 0, f"Receipt - Invoice {inv_no} - {customer['name']}", customer["name"], [pay_stmt_doc]),
                line("1200", 0, total_c, f"Receipt - Invoice {inv_no} - {customer['name']}", customer["name"], [pay_stmt_doc]),
            ])

print(f"Stage 3: {len(MONTHLY_INVOICES)} months of invoices booked, "
      f"revenue so far (subtotal) = {sum(monthly_cogs_subtotal.values())}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Mandated defect 5: one issued invoice later cancelled by a credit note.
# Non-taxable customer chosen so it doesn't perturb a sales-tax remittance
# bucket. Goods are treated as returned, so both revenue AND the COGS/
# inventory relief booked against it in March are reversed in April.
# ---------------------------------------------------------------------------

SPECIAL_CUSTOMER = "CU3"
SPECIAL_SUBTOTAL_C = c(6200)
special_customer = CUSTOMERS[SPECIAL_CUSTOMER]
special_issued = dt.date(2025, 3, 12)
special_inv_no = next_invoice_no()
special_doc_id = new_doc_id("INV")
special_rel = f"invoices-out/2025-03/{special_inv_no}.pdf"
add_doc(special_doc_id, "invoice_out", special_rel, "pdf", False, fmt_us_slash(special_issued),
        special_customer["name"], SPECIAL_SUBTOTAL_C)
R.render_html_to_pdf(
    invoice_html(special_inv_no, special_issued, special_customer, SPECIAL_SUBTOTAL_C, False, 0),
    os.path.join(MATERIALS_ABS, special_rel),
)
special_eid = new_entry_id()
add_entry(special_eid, iso(special_issued), [
    line("1200", SPECIAL_SUBTOTAL_C, 0, f"Invoice {special_inv_no} - {special_customer['name']}", special_customer["name"], [special_doc_id]),
    line("4000", 0, SPECIAL_SUBTOTAL_C, f"Invoice {special_inv_no} - {special_customer['name']}", special_customer["name"], [special_doc_id]),
])
monthly_cogs_basis["2025-03"].append(special_doc_id)
monthly_cogs_subtotal["2025-03"] += SPECIAL_SUBTOTAL_C

special_cn_issued = dt.date(2025, 4, 10)
special_cn_no = f"CN-{_invoice_no_seq + 1000}"
special_cn_doc = new_doc_id("CN")
special_cn_rel = f"invoices-out/2025-04/{special_cn_no}.pdf"
add_doc(special_cn_doc, "credit_note", special_cn_rel, "pdf", False, fmt_us_slash(special_cn_issued),
        special_customer["name"], SPECIAL_SUBTOTAL_C)

# Defect-2 fix: the COGS/inventory reversal is no longer a bare 72%-of-
# subtotal calculation invisible to a folder-only reader. It is now the sum
# of itemised, quantified returned goods priced at the SAME per-unit costs
# that the opening and closing stock counts carry for these SKUs (see
# PINNED_UNIT_COST_C above) -- a reader can reproduce this figure from the
# credit note alone, or cross-check it against either stock count.
special_cn_return_items = [
    (sku, dict(STOCK_ITEMS)[sku], CN_RETURN_QTY[sku], PINNED_UNIT_COST_C[sku]) for sku in CN_ITEM_SKUS
]
special_cogs_reversal_c = CN_COST_BASIS_C
assert special_cogs_reversal_c == pct_cents(SPECIAL_SUBTOTAL_C, COGS_RATE_PER_10000), (
    "itemised credit-note cost basis must still equal the ledger's 72%-margin COGS relief for this invoice "
    "-- the margin stays the internal generation mechanism, it is just no longer the reader's only way to reach the figure"
)

R.render_html_to_pdf(
    credit_note_html(special_cn_no, special_cn_issued, special_inv_no, special_customer, SPECIAL_SUBTOTAL_C, 0,
                      "Order cancelled in transit; goods returned to inventory undamaged.",
                      return_items=special_cn_return_items, cost_basis_c=special_cogs_reversal_c),
    os.path.join(MATERIALS_ABS, special_cn_rel),
)
cn_eid = new_entry_id()
add_entry(cn_eid, iso(special_cn_issued), [
    line("4000", SPECIAL_SUBTOTAL_C, 0, f"Credit note {special_cn_no} - cancels Invoice {special_inv_no}", special_customer["name"], [special_cn_doc]),
    line("1200", 0, SPECIAL_SUBTOTAL_C, f"Credit note {special_cn_no} - cancels Invoice {special_inv_no}", special_customer["name"], [special_cn_doc]),
])
cn_inv_eid = new_entry_id()
add_entry(cn_inv_eid, iso(special_cn_issued), [
    line("1300", special_cogs_reversal_c, 0, f"Goods returned - reverses COGS for cancelled Invoice {special_inv_no}", special_customer["name"], [special_cn_doc]),
    line("5000", 0, special_cogs_reversal_c, f"Goods returned - reverses COGS for cancelled Invoice {special_inv_no}", special_customer["name"], [special_cn_doc]),
])

print(f"Stage 4: special invoice {special_inv_no} issued and cancelled via {special_cn_no}.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Monthly COGS relief (perpetual, at a fixed 72% margin applied to that
# month's booked invoice subtotals -- includes the special invoice's March
# subtotal, correctly reversed above for April).
# ---------------------------------------------------------------------------

total_cogs_c = 0
for ym in MONTHS_2025:
    subtotal_sum = monthly_cogs_subtotal[ym]
    cogs_c = pct_cents(subtotal_sum, COGS_RATE_PER_10000)
    total_cogs_c += cogs_c
    eid = new_entry_id()
    end_of_month = month_bounds(*(int(x) for x in ym.split("-")))[1]
    add_entry(eid, iso(end_of_month), [
        line("5000", cogs_c, 0, f"Cost of goods sold - {ym} invoiced sales", "", monthly_cogs_basis[ym]),
        line("1300", 0, cogs_c, f"Inventory relief - {ym} invoiced sales", "", monthly_cogs_basis[ym]),
    ])

print(f"Stage 5: monthly COGS relief booked, total COGS (pre-shrinkage, pre-reversal) = {total_cogs_c}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Bills-in rendering
# ---------------------------------------------------------------------------

BILL_CSS = """
body { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; color: #1a1a1a; }
.header { border-bottom: 2px solid #2f4a2f; padding-bottom: 8px; }
.company { font-size: 16pt; font-weight: bold; color: #2f4a2f; }
table.items { width: 100%; border-collapse: collapse; margin-top: 18px; }
table.items th, table.items td { border: 1px solid #999; padding: 6px 8px; text-align: left; }
.totals { width: 300px; margin-left: auto; margin-top: 10px; font-weight: bold; }
.billto { margin-top: 16px; }
"""


def bill_html(bill_no: str, issued: dt.date, vendor: dict, description: str, amount_c: int,
              date_style: str, terms: str = "Net 30") -> str:
    if date_style == "iso":
        date_str = iso(issued)
    elif date_style == "us_slash":
        date_str = fmt_us_slash(issued)
    else:
        date_str = fmt_dd_mon_yyyy(issued)
    return f"""<html><head><style>{BILL_CSS}</style></head><body>
<div class="header">
  <div class="company">{vendor['name']}</div>
  <div>{vendor['address']}</div>
</div>
<div class="billto"><b>Bill To:</b><br>{COMPANY_NAME}<br>{COMPANY_ADDRESS}</div>
<p><b>Invoice No.:</b> {bill_no} &nbsp; <b>Date:</b> {date_str} &nbsp; <b>Terms:</b> {terms}</p>
<table class="items">
<tr><th>Description</th><th>Amount</th></tr>
<tr><td>{description}</td><td>{money(amount_c)}</td></tr>
</table>
<div class="totals">Amount Due: {money(amount_c)}</div>
</body></html>"""


def flat_receipt_png(lines_list, out_path, width=560, height=None):
    from PIL import Image, ImageDraw, ImageFont
    height = height or (60 + 34 * len(lines_list))
    img = Image.new("RGB", (width, height), (255, 255, 255))
    dctx = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    y = 24
    for txt in lines_list:
        dctx.text((24, y), txt, font=font, fill=(10, 10, 10))
        y += 32
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)


GOODS_VENDOR_KEYS = ["V1", "V2", "V3", "V4"]
GOODS_DESCRIPTIONS = {
    "V1": "Imported cured meats and salumi shipment",
    "V2": "Imported dried pasta and flour shipment",
    "V3": "Imported cheese shipment (refrigerated container)",
    "V4": "Imported extra virgin olive oil shipment",
}

_bill_no_seq = 4000
_purchase_rng = random.Random(SEED + 50)


def next_bill_no() -> str:
    global _bill_no_seq
    _bill_no_seq += 1
    return f"FP-{_bill_no_seq}"


# Irregular, lumpy shipment schedule -- container-freight purchasing is not
# a flat quarterly constant. Each vendor gets a different number of
# shipments per quarter at irregular dates and irregular sizes, with Q3
# clearly the heaviest (inventory build ahead of the Q4 holiday spike,
# Rule Four) and Q4's final shipment per vendor left unpaid at period end
# (mandate #4). Windows are (earliest, latest) day-of-year-ish date ranges;
# amounts are dollar (low, high) ranges sampled per shipment.
GOODS_SCHEDULE = {
    1: {"n_range": (1, 2), "window": (dt.date(2025, 1, 15), dt.date(2025, 3, 20)), "amt_range": (30000, 54000)},
    2: {"n_range": (1, 2), "window": (dt.date(2025, 4, 10), dt.date(2025, 6, 10)), "amt_range": (32000, 58000)},
    3: {"n_range": (2, 2), "window": (dt.date(2025, 7, 5), dt.date(2025, 9, 15)), "amt_range": (44000, 72000)},
    4: {"n_range": (1, 2), "window": (dt.date(2025, 10, 10), dt.date(2025, 12, 5)), "amt_range": (34000, 62000)},
}

total_purchases_c = 0
ap_by_creditor_open = {}
_v2_q1_first = None  # captured for the Defect-1 duplicate receipt, below

for vk in GOODS_VENDOR_KEYS:
    vendor = VENDORS[vk]
    for qi in (1, 2, 3, 4):
        sched = GOODS_SCHEDULE[qi]
        n = _purchase_rng.randint(*sched["n_range"])
        lo, hi = sched["window"]
        span_days = (hi - lo).days
        # distinct, sorted, irregularly-spaced dates within the window
        offsets = sorted(_purchase_rng.sample(range(span_days), n))
        dates = [lo + dt.timedelta(days=off) for off in offsets]
        for i, issued in enumerate(dates):
            amount_c = c(_purchase_rng.randint(*sched["amt_range"]))
            total_purchases_c += amount_c
            bill_no = next_bill_no()
            ym = f"{issued.year}-{issued.month:02d}"
            rel = f"bills-in/{ym}/{bill_no}.pdf"
            doc_id = new_doc_id("BILL")
            add_doc(doc_id, "bill_in", rel, "pdf", False, iso(issued), vendor["name"], amount_c)
            R.render_html_to_pdf(bill_html(bill_no, issued, vendor, GOODS_DESCRIPTIONS[vk], amount_c, "iso"),
                                  os.path.join(MATERIALS_ABS, rel))
            add_entry(new_entry_id(), iso(issued), [
                line("1300", amount_c, 0, f"Bill {bill_no} - {vendor['name']}", vendor["name"], [doc_id]),
                line("2000", 0, amount_c, f"Bill {bill_no} - {vendor['name']}", vendor["name"], [doc_id]),
            ])
            if vk == "V2" and qi == 1 and i == 0:
                _v2_q1_first = (issued, amount_c)
            # Only each vendor's final Q4 shipment remains unpaid at period
            # end -- every earlier shipment (including earlier Q4 ones) is
            # paid on ~30-day terms.
            is_final_q4_shipment = (qi == 4 and i == len(dates) - 1)
            if not is_final_q4_shipment:
                pay_date = add_days(iso(issued), 28)
                pay_stmt = stmt_doc_id(OPERATING_CODE, pay_date)
                add_entry(new_entry_id(), pay_date, [
                    line("2000", amount_c, 0, f"Payment - Bill {bill_no} - {vendor['name']}", vendor["name"], [pay_stmt]),
                    line(OPERATING_CODE, 0, amount_c, f"Payment - Bill {bill_no} - {vendor['name']}", vendor["name"], [pay_stmt]),
                ])
            else:
                ap_open_unpaid.append((bill_no, vendor["name"], amount_c, iso(issued)))

# Mandated defect 1: duplicate receipt -- the Q1 Molino d'Oro bill is
# "shipped twice" as a second document (a delivery/packing-slip photo) in a
# different format. It is registered in documents.jsonl but never cited by
# any ledger.jsonl doc_ids -- the ledger books the purchase exactly once,
# from the bill above.
_dup_vendor = VENDORS["V2"]
_dup_issued, _dup_amount_c = _v2_q1_first
_dup_flat = "/tmp/spike006_dup_receipt_flat.png"
flat_receipt_png([
    f"{_dup_vendor['name']}",
    "DELIVERY RECEIPT / PACKING SLIP",
    f"Date: {fmt_dd_mon_yyyy(_dup_issued)}",
    "PO Ref: FP-Q1-PASTA",
    f"Amount: {money(_dup_amount_c)}",
    "Received in good order - Sunset Park dock",
], _dup_flat)
_dup_doc_id = new_doc_id("RCT")
_dup_rel = "receipts/receipt-molino-doro-delivery.jpg"
R.photograph_receipt(_dup_flat, os.path.join(MATERIALS_ABS, _dup_rel), seed=SEED + 7)
add_doc(_dup_doc_id, "receipt", _dup_rel, "jpg", True, fmt_dd_mon_yyyy(_dup_issued), _dup_vendor["name"], _dup_amount_c)
os.remove(_dup_flat)

print(f"Stage 6: goods bills booked, total purchases = {total_purchases_c}, duplicate receipt registered as {_dup_doc_id}.", file=sys.stderr)


def scanned_bill(bill_no, issued, vendor, description, amount_c, expense_code, date_style="us_slash", terms="Net 15"):
    """Create a bill-in that ships as an image-only scan, via bills-in/<ym>/<no>.pdf."""
    ym = f"{issued.year}-{issued.month:02d}"
    rel = f"bills-in/{ym}/{bill_no}.pdf"
    tmp_text = f"/tmp/spike006_bill_{bill_no}.pdf"
    R.render_html_to_pdf(bill_html(bill_no, issued, vendor, description, amount_c, date_style, terms), tmp_text)
    doc_id = new_doc_id("BILL")
    out_path = os.path.join(MATERIALS_ABS, rel)
    R.scanify(tmp_text, out_path, seed=SEED + int(bill_no.split("-")[1]))
    os.remove(tmp_text)
    add_doc(doc_id, "bill_in", rel, "pdf", True,
            fmt_us_slash(issued) if date_style == "us_slash" else iso(issued), vendor["name"], amount_c)
    return doc_id


# ---------------------------------------------------------------------------
# Non-goods bills-in: insurance, packaging, professional fees.
# ---------------------------------------------------------------------------

# Insurance (V6) -- one annual premium bill, scanned, paid promptly.
ins_vendor = VENDORS["V6"]
ins_issued = dt.date(2025, 1, 10)
ins_amount_c = c(9600)
ins_bill_no = next_bill_no()
ins_doc = scanned_bill(ins_bill_no, ins_issued, ins_vendor, "Annual general liability + property insurance premium",
                        ins_amount_c, "6060")
ins_eid = new_entry_id()
add_entry(ins_eid, iso(ins_issued), [
    line("6060", ins_amount_c, 0, f"Bill {ins_bill_no} - {ins_vendor['name']}", ins_vendor["name"], [ins_doc]),
    line("2000", 0, ins_amount_c, f"Bill {ins_bill_no} - {ins_vendor['name']}", ins_vendor["name"], [ins_doc]),
])
ins_pay_date = add_days(iso(ins_issued), 15)
ins_pay_stmt = stmt_doc_id(OPERATING_CODE, ins_pay_date)
add_entry(new_entry_id(), ins_pay_date, [
    line("2000", ins_amount_c, 0, f"Payment - Bill {ins_bill_no} - {ins_vendor['name']}", ins_vendor["name"], [ins_pay_stmt]),
    line(OPERATING_CODE, 0, ins_amount_c, f"Payment - Bill {ins_bill_no} - {ins_vendor['name']}", ins_vendor["name"], [ins_pay_stmt]),
])

# Packaging (V5) -- two bills through the year, text PDF, paid.
pack_vendor = VENDORS["V5"]
for pack_issued in (dt.date(2025, 3, 5), dt.date(2025, 9, 5)):
    pack_amount_c = c(1200)
    pack_bill_no = next_bill_no()
    ym = f"{pack_issued.year}-{pack_issued.month:02d}"
    rel = f"bills-in/{ym}/{pack_bill_no}.pdf"
    doc_id = new_doc_id("BILL")
    add_doc(doc_id, "bill_in", rel, "pdf", False, iso(pack_issued), pack_vendor["name"], pack_amount_c)
    R.render_html_to_pdf(bill_html(pack_bill_no, pack_issued, pack_vendor, "Corrugated cartons and case liners", pack_amount_c, "iso"),
                          os.path.join(MATERIALS_ABS, rel))
    add_entry(new_entry_id(), iso(pack_issued), [
        line("6050", pack_amount_c, 0, f"Bill {pack_bill_no} - {pack_vendor['name']}", pack_vendor["name"], [doc_id]),
        line("2000", 0, pack_amount_c, f"Bill {pack_bill_no} - {pack_vendor['name']}", pack_vendor["name"], [doc_id]),
    ])
    pay_date = add_days(iso(pack_issued), 20)
    pay_stmt = stmt_doc_id(OPERATING_CODE, pay_date)
    add_entry(new_entry_id(), pay_date, [
        line("2000", pack_amount_c, 0, f"Payment - Bill {pack_bill_no} - {pack_vendor['name']}", pack_vendor["name"], [pay_stmt]),
        line(OPERATING_CODE, 0, pack_amount_c, f"Payment - Bill {pack_bill_no} - {pack_vendor['name']}", pack_vendor["name"], [pay_stmt]),
    ])

# Professional fees (V7) -- two bills, scanned, paid.
prof_vendor = VENDORS["V7"]
for prof_issued in (dt.date(2025, 1, 15), dt.date(2025, 7, 15)):
    prof_amount_c = c(3000)
    prof_bill_no = next_bill_no()
    prof_doc = scanned_bill(prof_bill_no, prof_issued, prof_vendor, "Bookkeeping and payroll compliance services",
                             prof_amount_c, "6070")
    add_entry(new_entry_id(), iso(prof_issued), [
        line("6070", prof_amount_c, 0, f"Bill {prof_bill_no} - {prof_vendor['name']}", prof_vendor["name"], [prof_doc]),
        line("2000", 0, prof_amount_c, f"Bill {prof_bill_no} - {prof_vendor['name']}", prof_vendor["name"], [prof_doc]),
    ])
    pay_date = add_days(iso(prof_issued), 15)
    pay_stmt = stmt_doc_id(OPERATING_CODE, pay_date)
    add_entry(new_entry_id(), pay_date, [
        line("2000", prof_amount_c, 0, f"Payment - Bill {prof_bill_no} - {prof_vendor['name']}", prof_vendor["name"], [pay_stmt]),
        line(OPERATING_CODE, 0, prof_amount_c, f"Payment - Bill {prof_bill_no} - {prof_vendor['name']}", prof_vendor["name"], [pay_stmt]),
    ])

print("Stage 7: insurance / packaging / professional-fee bills booked.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Recurring monthly cash-only expenses: rent, utilities, telecom, bank fees.
# These entries touch a cash account, so check5 exempts them; evidenced by
# that month's operating bank statement.
# ---------------------------------------------------------------------------

RENT_MONTHLY_C = c(6500)  # fixed lease -- genuinely constant in real life
_expense_rng = random.Random(SEED + 40)

# Utilities: refrigerated warehouse space -- higher in summer (AC/
# refrigeration load) and winter (heat) than shoulder months, plus
# irregular metered noise. Telecom/bank-fees/tolls get plain seeded jitter
# so no two months are identical -- a food importer's expense side should
# never look like a set of recurring constants.
_UTIL_SEASONAL_FACTOR = {
    "01": 1.15, "02": 1.10, "03": 0.95, "04": 0.85, "05": 0.90, "06": 1.10,
    "07": 1.30, "08": 1.35, "09": 1.05, "10": 0.90, "11": 1.00, "12": 1.20,
}

for ym in MONTHS_2025:
    y, m = (int(x) for x in ym.split("-"))
    pay_date = iso(dt.date(y, m, _expense_rng.randint(24, 28)))
    stmt_doc = stmt_doc_id(OPERATING_CODE, pay_date)

    util_c = int(round(c(900) * _UTIL_SEASONAL_FACTOR[ym[5:7]] * _expense_rng.uniform(0.92, 1.08)))
    telecom_c = c(250) + _expense_rng.randint(-1800, 4200)  # occasional overage charges
    tolls_c = c(60) + _expense_rng.randint(-2500, 6500)

    for code, amt, memo, cp in [
        ("6000", RENT_MONTHLY_C, f"Rent - {ym}", LANDLORD_NAME),
        ("6010", util_c, f"Utilities - {ym}", UTILITY_NAME),
        ("6150", telecom_c, f"Telephone & internet - {ym}", TELECOM_NAME),
        ("6110", tolls_c, f"Vehicle tolls/parking - {ym}", ""),
    ]:
        add_entry(new_entry_id(), pay_date, [
            line(code, amt, 0, memo, cp, [stmt_doc]),
            line(OPERATING_CODE, 0, amt, memo, cp, [stmt_doc]),
        ])
    fee_date = iso(dt.date(y, m, 30 if m != 2 else 28))
    fee_stmt = stmt_doc_id(OPERATING_CODE, fee_date)
    bankfee_c = c(35) + _expense_rng.randint(-500, 1800)  # occasional wire/NSF fees
    add_entry(new_entry_id(), fee_date, [
        line("6080", bankfee_c, 0, f"Monthly account fee - {ym}", BANK_NAME, [fee_stmt]),
        line(OPERATING_CODE, 0, bankfee_c, f"Monthly account fee - {ym}", BANK_NAME, [fee_stmt]),
    ])

print("Stage 8: recurring monthly cash expenses booked.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Payroll: 4 employees, monthly. GothamPay provider summary PDF per month
# (defect-6 date-format variant: long-form dates) + one XLSX register
# covering the whole year (per-period rows only, no YTD/derived totals).
# Funded by a monthly transfer Operating -> Payroll (mandated defect 3).
# ---------------------------------------------------------------------------

PAYROLL_CSS = """
body { font-family: 'Courier New', monospace; font-size: 11pt; }
table { width: 100%; border-collapse: collapse; margin-top: 14px; }
th, td { border: 1px solid #555; padding: 5px 8px; text-align: left; }
th { background: #eee; }
"""


def payroll_summary_html(period_label: str, pay_date: dt.date, rows, gross_total_c, tax_total_c, net_total_c) -> str:
    row_html = "".join(
        f"<tr><td>{name}</td><td>{title}</td><td>{money(gross)}</td><td>{money(tax)}</td><td>{money(net)}</td></tr>"
        for name, title, gross, tax, net in rows
    )
    return f"""<html><head><style>{PAYROLL_CSS}</style></head><body>
<h2>{PAYROLL_PROVIDER}</h2>
<div>{PAYROLL_PROVIDER_ADDRESS}</div>
<p><b>Client:</b> {COMPANY_NAME}<br><b>Pay Period:</b> {period_label}<br><b>Pay Date:</b> {fmt_long(pay_date)}</p>
<table>
<tr><th>Employee</th><th>Title</th><th>Gross Pay</th><th>Employer Tax</th><th>Net Pay</th></tr>
{row_html}
<tr><td colspan="2">Employer Totals (this period only)</td><td>{money(gross_total_c)}</td><td>{money(tax_total_c)}</td><td>{money(net_total_c)}</td></tr>
</table>
</body></html>"""


register_rows = [["Pay Date", "Employee", "Title", "Gross Pay", "Employer Tax", "Net Pay"]]

total_wages_c = 0
total_payroll_tax_c = 0

for ym in MONTHS_2025:
    y, m = (int(x) for x in ym.split("-"))
    pay_date = dt.date(y, m, calendar.monthrange(y, m)[1])
    period_label = f"{dt.date(y, m, 1).strftime('%B %Y')}"

    rows = []
    gross_total = 0
    tax_total = 0
    for name, title, gross in EMPLOYEES:
        tax = pct_cents(gross, EMPLOYER_TAX_RATE)
        net = gross  # simplified: "wages expense" already represents payout cost
        rows.append((name, title, gross, tax, net))
        gross_total += gross
        tax_total += tax
        register_rows.append([fmt_long(pay_date), name, title, f"${gross/100:,.2f}", f"${tax/100:,.2f}", f"${net/100:,.2f}"])
    net_total = gross_total

    # Transfer funding the payroll account, a few days before pay date.
    transfer_date = iso(pay_date - dt.timedelta(days=3))
    transfer_amount = gross_total + tax_total
    op_stmt = stmt_doc_id(OPERATING_CODE, transfer_date)
    pr_stmt = stmt_doc_id(PAYROLL_CODE, transfer_date)
    add_entry(new_entry_id(), transfer_date, [
        line(OPERATING_CODE, 0, transfer_amount, f"Transfer to payroll account - {ym}", "", [op_stmt]),
        line(PAYROLL_CODE, transfer_amount, 0, f"Transfer from operating account - {ym}", "", [pr_stmt]),
    ])

    doc_id = new_doc_id("PR")
    rel = f"payroll/{ym}-payroll-summary.pdf"
    add_doc(doc_id, "payroll_summary", rel, "pdf", False, fmt_long(pay_date), PAYROLL_PROVIDER, transfer_amount)
    R.render_html_to_pdf(payroll_summary_html(period_label, pay_date, rows, gross_total, tax_total, net_total),
                          os.path.join(MATERIALS_ABS, rel))

    pr_stmt2 = stmt_doc_id(PAYROLL_CODE, iso(pay_date))
    add_entry(new_entry_id(), iso(pay_date), [
        line("6020", gross_total, 0, f"Wages - {ym}", PAYROLL_PROVIDER, [doc_id]),
        line("6030", tax_total, 0, f"Employer payroll tax - {ym}", PAYROLL_PROVIDER, [doc_id]),
        line(PAYROLL_CODE, 0, transfer_amount, f"Payroll run - {ym}", PAYROLL_PROVIDER, [pr_stmt2]),
    ])
    total_wages_c += gross_total
    total_payroll_tax_c += tax_total

register_doc = new_doc_id("PRREG")
register_rel = "payroll/payroll-register.xlsx"
add_doc(register_doc, "payroll_register", register_rel, "xlsx", False, "2026-01-05", PAYROLL_PROVIDER, None)
R.render_xlsx(os.path.join(MATERIALS_ABS, register_rel), {"Payroll Register 2025": register_rows})

print(f"Stage 9: payroll booked. total_wages={total_wages_c} total_payroll_tax={total_payroll_tax_c}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Opening AR / AP settlement in January (Rule Two): excluded from current-
# period income/expense -- these are balance-sheet-only cash movements.
# ---------------------------------------------------------------------------

_ar_settle_dates = {"Trattoria Rosso NYC": "2025-01-12", "Trattoria Vialardi": "2025-01-19"}
for debtor, amt in OPENING_AR:
    sdate = _ar_settle_dates[debtor]
    stmt = stmt_doc_id(OPERATING_CODE, sdate)
    eid = new_entry_id()
    add_entry(eid, sdate, [
        line(OPERATING_CODE, amt, 0, f"Receipt - {debtor} (settles opening AR, per prior CPA closing letter)", debtor, [stmt, DOC_OPEN]),
        line("1200", 0, amt, f"Receipt - {debtor} (settles opening AR)", debtor, [stmt, DOC_OPEN]),
    ])
    BANK_DESC[(eid, OPERATING_CODE)] = f"DEPOSIT - {debtor.upper()}"

_ap_settle_dates = {"Salumeria Adriatica Import Co.": "2025-01-15", "Molino d'Oro Pasta Imports LLC": "2025-01-22"}
for creditor, amt in OPENING_AP:
    sdate = _ap_settle_dates[creditor]
    stmt = stmt_doc_id(OPERATING_CODE, sdate)
    eid = new_entry_id()
    add_entry(eid, sdate, [
        line("2000", amt, 0, f"Payment - {creditor} (settles opening AP, per prior CPA closing letter)", creditor, [stmt, DOC_OPEN]),
        line(OPERATING_CODE, 0, amt, f"Payment - {creditor} (settles opening AP)", creditor, [stmt, DOC_OPEN]),
    ])
    BANK_DESC[(eid, OPERATING_CODE)] = f"CHECK - {creditor.upper()}"

print("Stage 10: opening AR/AP settled in January.", file=sys.stderr)

# ---------------------------------------------------------------------------
# NY sales tax remittances -- driven by NY_SALES_TAX_QUARTERS, not calendar
# quarters. Ferrone's fiscal year sits inside four filing periods.
# ---------------------------------------------------------------------------

sales_tax_by_month: dict[str, int] = {ym: 0 for ym in MONTHS_2025}
for l in LEDGER:
    if l["account_code"] == "2100" and l["credit"] > 0 and l["date"] >= PERIOD_START:
        sales_tax_by_month[l["date"][:7]] += l["credit"]

REMITTANCES = [
    {"due": "2025-03-20", "months": [], "opening_slice": OPENING_SALES_TAX_PAYABLE, "period_label": "1 Dec 2024 - 28 Feb 2025"},
    {"due": "2025-06-20", "months": ["2025-03", "2025-04", "2025-05"], "opening_slice": 0, "period_label": "1 Mar 2025 - 31 May 2025"},
    {"due": "2025-09-20", "months": ["2025-06", "2025-07", "2025-08"], "opening_slice": 0, "period_label": "1 Jun 2025 - 31 Aug 2025"},
    {"due": "2025-12-20", "months": ["2025-09", "2025-10", "2025-11"], "opening_slice": 0, "period_label": "1 Sep 2025 - 30 Nov 2025"},
]
REMITTANCES[0]["months"] = ["2025-01", "2025-02"]

_remit_doc_counter = 0
for r in REMITTANCES:
    amt = r["opening_slice"] + sum(sales_tax_by_month[m] for m in r["months"])
    stmt = stmt_doc_id(OPERATING_CODE, r["due"])
    add_entry(new_entry_id(), r["due"], [
        line("2100", amt, 0, f"NY sales tax remittance - filing period {r['period_label']}", "NYS Dept. of Taxation and Finance", [stmt]),
        line(OPERATING_CODE, 0, amt, f"NY sales tax remittance - filing period {r['period_label']}", "NYS Dept. of Taxation and Finance", [stmt]),
    ])

dec_2025_tax_collected = sales_tax_by_month["2025-12"]
print(f"Stage 11: NY sales tax remittances booked. Dec-2025 (not yet due) = {dec_2025_tax_collected}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Member distributions (mandated: identifiable, dated, memo names the
# member) + mandated defect 2: one personal expense reclassified as a
# distribution, not an expense.
# ---------------------------------------------------------------------------

QUARTERLY_DIST_DATES = ["2025-03-28", "2025-06-27", "2025-09-26", "2025-12-29"]
DIST_A_QUARTERLY_C = c(15000)
DIST_L_QUARTERLY_C = c(12000)

for qdate in QUARTERLY_DIST_DATES:
    stmt = stmt_doc_id(OPERATING_CODE, qdate)
    add_entry(new_entry_id(), qdate, [
        line(MEMBER_A_DIST_CODE, DIST_A_QUARTERLY_C, 0, f"Member distribution - {MEMBER_A_NAME}", MEMBER_A_FULL, [stmt]),
        line(OPERATING_CODE, 0, DIST_A_QUARTERLY_C, f"Member distribution - {MEMBER_A_NAME}", MEMBER_A_FULL, [stmt]),
    ])
    add_entry(new_entry_id(), qdate, [
        line(MEMBER_L_DIST_CODE, DIST_L_QUARTERLY_C, 0, f"Member distribution - {MEMBER_L_NAME}", MEMBER_L_FULL, [stmt]),
        line(OPERATING_CODE, 0, DIST_L_QUARTERLY_C, f"Member distribution - {MEMBER_L_NAME}", MEMBER_L_FULL, [stmt]),
    ])

# Personal expense defect: a flight booked on the business card, correctly
# treated as a distribution to A. Ferrone, not a business expense.
_flight_date = dt.date(2025, 7, 18)
_flight_amount_c = c(1850)
_flight_flat = "/tmp/spike006_flight_flat.png"
flat_receipt_png([
    "JETAZZURRO AIRLINES",
    "E-TICKET RECEIPT",
    "Passenger: A. FERRONE",
    f"Date: {fmt_dd_mon_yyyy(_flight_date)}",
    "Route: JFK - NAP - JFK",
    f"Fare Total: {money(_flight_amount_c)}",
    "Card ending 4417",
], _flight_flat)
_flight_doc = new_doc_id("RCT")
_flight_rel = "receipts/receipt-jetazzurro-flight.jpg"
R.photograph_receipt(_flight_flat, os.path.join(MATERIALS_ABS, _flight_rel), seed=SEED + 11)
add_doc(_flight_doc, "receipt", _flight_rel, "jpg", True, fmt_dd_mon_yyyy(_flight_date), "JetAzzurro Airlines", _flight_amount_c)
os.remove(_flight_flat)

_flight_stmt = stmt_doc_id(OPERATING_CODE, iso(_flight_date))
_flight_eid = new_entry_id()
add_entry(_flight_eid, iso(_flight_date), [
    line(MEMBER_A_DIST_CODE, _flight_amount_c, 0,
         "Member distribution - personal flight expense (Naples, IT), not a business expense - A. Ferrone",
         MEMBER_A_FULL, [_flight_stmt, _flight_doc]),
    line(OPERATING_CODE, 0, _flight_amount_c,
         "Member distribution - personal flight expense (Naples, IT) - A. Ferrone",
         MEMBER_A_FULL, [_flight_stmt, _flight_doc]),
])
BANK_DESC[(_flight_eid, OPERATING_CODE)] = "JETAZZURRO AIR 718555 4417"

print("Stage 12: member distributions booked (quarterly + personal-expense reclass).", file=sys.stderr)

# NOTE: a period-end closing entry rolling 3020/3030 into 3000/3010 was
# tried here and reverted -- it would have been an unevidenced derived
# journal entry (Hard Rule One violation) worked around solely to satisfy
# check_7's arithmetic. It is unnecessary: lib/ledger.py's
# balance_sheet_totals() sums each account TYPE in that type's canonical
# direction (assets/expenses debit-positive, liabilities/equity/income
# credit-positive), explicitly NOT each account's own normal_side, so
# contra accounts (3020/3030 here; 1590 for Bright Harbor) are correctly
# subtracted rather than added. Distributions post only to 3020/3030 per
# SPEC S1.5, un-netted, exactly as intended -- check_7 passes as-is.

# ---------------------------------------------------------------------------
# Fuel/till receipts (photographed JPG) + one handwritten-looking cash
# receipt (mandated defect 7).
# ---------------------------------------------------------------------------

FUEL_STOPS = [
    (dt.date(2025, 2, 21), "Harbor Fuel & Auto", c(58.40)),
    (dt.date(2025, 5, 9), "Bay Ridge Gas & Wash", c(71.15)),
    (dt.date(2025, 8, 27), "Harbor Fuel & Auto", c(66.90)),
    (dt.date(2025, 11, 14), "4th Avenue Fuel Stop", c(74.25)),
]
for i, (fdate, station, amt) in enumerate(FUEL_STOPS):
    flat = f"/tmp/spike006_fuel_{i}.png"
    flat_receipt_png([
        station.upper(),
        f"Date: {fmt_dd_mon_yyyy(fdate)}",
        "Regular Unleaded",
        f"TOTAL: {money(amt)}",
        "Card ****4417",
    ], flat)
    doc_id = new_doc_id("RCT")
    rel = f"receipts/receipt-fuel-{i+1:02d}.jpg"
    R.photograph_receipt(flat, os.path.join(MATERIALS_ABS, rel), seed=SEED + 20 + i)
    add_doc(doc_id, "receipt", rel, "jpg", True, fmt_dd_mon_yyyy(fdate), station, amt)
    os.remove(flat)
    stmt = stmt_doc_id(OPERATING_CODE, iso(fdate))
    add_entry(new_entry_id(), iso(fdate), [
        line("6110", amt, 0, f"Fuel - {station}", station, [stmt, doc_id]),
        line(OPERATING_CODE, 0, amt, f"Fuel - {station}", station, [stmt, doc_id]),
    ])

# Handwritten cash receipt (mandate #7): small cash outlay, photographed at
# an angle.
_hw_date = dt.date(2025, 9, 15)
_hw_amount_c = c(52.00)
_hw_doc = new_doc_id("RCT")
_hw_rel = "receipts/receipt-handwritten-cash-tip.jpg"
R.handwritten_note_image(
    ["Cash paid", "Driver toll + parking", f"{money(_hw_amount_c)}", "9/15/25", "- D. Wu"],
    os.path.join(MATERIALS_ABS, _hw_rel), seed=SEED + 30,
)
add_doc(_hw_doc, "cash_receipt_handwritten", _hw_rel, "jpg", True, "9/15/25", "", _hw_amount_c)
_hw_stmt = stmt_doc_id(OPERATING_CODE, iso(_hw_date))
add_entry(new_entry_id(), iso(_hw_date), [
    line("6900", _hw_amount_c, 0, "Cash reimbursement - driver toll & parking", "", [_hw_stmt, _hw_doc]),
    line(OPERATING_CODE, 0, _hw_amount_c, "Cash reimbursement - driver toll & parking", "", [_hw_stmt, _hw_doc]),
])

print("Stage 13: fuel receipts + handwritten cash receipt booked.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Period-end inventory shrinkage adjustment + closing stock count.
# ---------------------------------------------------------------------------

DOC_STOCK_CLOSE = new_doc_id("STOCKCLOSE")
pre_shrink_inventory_c = L.account_balance_cents(LEDGER, "1300", as_of=PERIOD_END)
# Defect-2 fix: shrinkage is no longer a bare $3,200.00 booked with no
# derivation path. It is fixed here as SHRINK_UNITS cases of SHRINK_SKU
# priced at that SKU's own pinned unit cost -- (Book Qty - Qty Counted) x
# Unit Cost on the closing count sheet reproduces this exact figure with no
# external rate, ledger, or answer key required.
SHRINKAGE_C = SHRINK_UNITS * PINNED_UNIT_COST_C[SHRINK_SKU]
assert SHRINKAGE_C == c(3200)
closing_inventory_target_c = pre_shrink_inventory_c - SHRINKAGE_C

shrink_eid = new_entry_id()
# Registered below (after doc render) -- placeholder entry created after we
# know the doc id, so build the doc first, then the entry.

closing_stock_rows = build_stock_count_rows(closing_inventory_target_c, seed=SEED + 2, pins=CLOSING_STOCK_PINS)
_shrink_counted_qty = CLOSING_STOCK_COUNTED_QTY[SHRINK_SKU]
_book_qty_overrides = {SHRINK_SKU: _shrink_counted_qty + SHRINK_UNITS}
closing_sheet_rows, closing_sheet_total, closing_variance_total = closing_stock_count_sheet_rows(
    closing_stock_rows, _book_qty_overrides)
assert closing_sheet_total == closing_inventory_target_c
assert closing_variance_total == SHRINKAGE_C

closing_rel = "inventory/stock-count-2025-12-31.xlsx"
add_doc(DOC_STOCK_CLOSE, "stock_count", closing_rel, "xlsx", False, "2025-12-31", "", None)
R.render_xlsx(os.path.join(MATERIALS_ABS, closing_rel), {"Closing Physical Count 12-31-2025": closing_sheet_rows})

add_entry(shrink_eid, PERIOD_END, [
    line("5000", SHRINKAGE_C, 0, "Inventory shrinkage per physical count (spoilage/breakage)", "", [DOC_STOCK_CLOSE]),
    line("1300", 0, SHRINKAGE_C, "Inventory shrinkage per physical count (spoilage/breakage)", "", [DOC_STOCK_CLOSE]),
])

print(f"Stage 14: closing stock count booked. pre_shrink={pre_shrink_inventory_c} closing={closing_inventory_target_c}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Render the opening stock count (registered as DOC_STOCK_OPEN back at
# Stage 2 -- rendered here now that the row-builder helper is defined).
# ---------------------------------------------------------------------------

opening_sheet_rows, opening_sheet_total = stock_count_sheet_rows(opening_stock_rows)
assert opening_sheet_total == OPENING_INVENTORY
opening_stock_rel = "inventory/stock-count-2024-12-31.xlsx"
# add_doc for DOC_STOCK_OPEN was implicitly reserved; register it now for real.
DOCUMENTS.append({
    "doc_id": DOC_STOCK_OPEN, "kind": "stock_count", "path": f"{MATERIALS_REL}/{opening_stock_rel}",
    "format": "xlsx", "scanned": False, "issued_date": "2024-12-31", "counterparty": "", "amount": None,
})
R.render_xlsx(os.path.join(MATERIALS_ABS, opening_stock_rel), {"Opening Physical Count 12-31-2024": opening_sheet_rows})

print("Stage 15: opening stock count rendered.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Opening letter (prior CPA firm), text PDF, prose + simple table. Titled to
# avoid the check-8 forbidden-phrase scan ("balance sheet", "trial balance",
# etc. are all avoided deliberately).
# ---------------------------------------------------------------------------

OPENING_LETTER_CSS = """
body { font-family: 'Times New Roman', Georgia, serif; font-size: 12pt; line-height: 1.5; color: #1a1a1a; }
.letterhead { text-align: center; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; }
th, td { border: 1px solid #888; padding: 5px 10px; text-align: left; }
th { background: #eee; }
.sig { margin-top: 40px; }
"""

_ar_rows = "".join(f"<tr><td>{d}</td><td style='text-align:right;'>{money(a)}</td></tr>" for d, a in OPENING_AR)
_ap_rows = "".join(f"<tr><td>{c_}</td><td style='text-align:right;'>{money(a)}</td></tr>" for c_, a in OPENING_AP)

opening_letter_html = f"""<html><head><style>{OPENING_LETTER_CSS}</style></head><body>
<div class="letterhead">
  <h2>{PRIOR_CPA_FIRM}</h2>
  <div>{PRIOR_CPA_ADDRESS} &middot; {PRIOR_CPA_PHONE}</div>
</div>
<p>{fmt_long(dt.date(2025,1,15))}</p>
<p>Members<br>{COMPANY_NAME}<br>{COMPANY_ADDRESS}</p>
<p>Dear Antonio and Lucia,</p>
<p>At your request, we have prepared a summary of {COMPANY_NAME}'s closing financial position
as of December 31, 2024, the final day of our engagement as the Company's accountants. This
letter, together with the attached physical inventory count, is intended to give your incoming
bookkeeper a clean starting point for the 2025 fiscal year.</p>
<p>Cash on deposit totaled {money(OPENING_CASH_OP + OPENING_CASH_PR)} across the Company's two
operating bank accounts at {BANK_NAME}: {money(OPENING_CASH_OP)} in the primary operating
account and {money(OPENING_CASH_PR)} held in the dedicated payroll account.</p>
<p>Accounts receivable totaled {money(_ar_total)}, owed by the following customers:</p>
<table><tr><th>Debtor</th><th>Amount</th></tr>{_ar_rows}</table>
<p>Accounts payable totaled {money(_ap_total)}, owed to the following suppliers:</p>
<table><tr><th>Creditor</th><th>Amount</th></tr>{_ap_rows}</table>
<p>Merchandise inventory on hand, per the attached physical count taken December 31, 2024,
was valued at {money(OPENING_INVENTORY)} on a first-in, first-out cost basis.</p>
<p>The Company's New York State sales tax payable at year end was {money(OPENING_SALES_TAX_PAYABLE)},
representing tax collected during December 2024 and not yet due for remittance (the December
2024 - February 2025 filing period is due March 20, 2025).</p>
<p>Members' equity is carried in two capital accounts: {money(OPENING_CAPITAL_A)} for
{MEMBER_A_FULL} and {money(OPENING_CAPITAL_L)} for {MEMBER_L_FULL}.</p>
<p>Please let us know if you have any questions as your new bookkeeping arrangement begins.</p>
<div class="sig">Sincerely,<br><br>{PRIOR_CPA_FIRM}</div>
</body></html>"""

R.render_html_to_pdf(opening_letter_html, os.path.join(MATERIALS_ABS, "opening/opening-letter.pdf"))
DOCUMENTS.append({
    "doc_id": DOC_OPEN, "kind": "opening_letter", "path": f"{MATERIALS_REL}/opening/opening-letter.pdf",
    "format": "pdf", "scanned": False, "issued_date": "January 15, 2025", "counterparty": PRIOR_CPA_FIRM,
    "amount": None,
})

print("Stage 16: opening letter rendered.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Derive statements.jsonl from the ledger (guarantees checks 1-3 by
# construction), then render the 24 bank-statement PDFs + the Jan-Jun CSV.
# ---------------------------------------------------------------------------

STATEMENTS: list[dict] = []


def build_statements_for_account(account_code: str) -> list[dict]:
    out = []
    running = L.account_balance_cents(LEDGER, account_code, as_of=AS_OF)
    for ym in MONTHS_2025:
        y, m = (int(x) for x in ym.split("-"))
        start, end = month_bounds(y, m)
        month_lines = sorted(
            (l for l in LEDGER if l["account_code"] == account_code and iso(start) <= l["date"] <= iso(end)),
            key=lambda l: (l["date"], l["entry_id"]),
        )
        stmt_lines = []
        opening = running
        for l in month_lines:
            amt = l["debit"] if l["debit"] else l["credit"]
            direction = "in" if l["debit"] else "out"
            running += amt if direction == "in" else -amt
            desc = BANK_DESC.get((l["entry_id"], account_code), l["memo"])
            stmt_lines.append({"date": l["date"], "description": desc, "amount": amt,
                                "direction": direction, "entry_id": l["entry_id"]})
        stmt_id = f"STMT-{'OP' if account_code == OPERATING_CODE else 'PR'}-{ym}"
        out.append({
            "stmt_id": stmt_id, "account_code": account_code,
            "stmt_period_start": iso(start), "stmt_period_end": iso(end),
            "opening_balance": opening, "closing_balance": running,
            "doc_ids": [STMT_DOC[(account_code, ym)]], "lines": stmt_lines,
        })
    return out


STATEMENTS.extend(build_statements_for_account(OPERATING_CODE))
STATEMENTS.extend(build_statements_for_account(PAYROLL_CODE))

print(f"Stage 17: derived {len(STATEMENTS)} statement records from the ledger.", file=sys.stderr)

# ---------------------------------------------------------------------------
# Render bank statement PDFs from the derived statements.
# ---------------------------------------------------------------------------

STATEMENT_CSS = """
body { font-family: Arial, Helvetica, sans-serif; font-size: 11pt; color: #16324a; }
.head { display:flex; justify-content:space-between; border-bottom: 4px solid #16324a; padding-bottom: 10px; }
.bankname { font-size: 20pt; font-weight: bold; letter-spacing: 1px; }
table { width: 100%; border-collapse: collapse; margin-top: 16px; }
th, td { padding: 5px 8px; border-bottom: 1px solid #ccc; text-align: left; }
th { background: #eaf1f7; }
.balances { margin-top: 14px; font-weight: bold; }
"""


def statement_html(stmt: dict, account_label: str, mask: str) -> str:
    y, m = (int(x) for x in stmt["stmt_period_start"][:7].split("-"))
    period_label = f"{fmt_long(dt.date(y, m, 1))} - {fmt_long(d(stmt['stmt_period_end']))}"
    rows = ""
    running = stmt["opening_balance"]
    for l in stmt["lines"]:
        running += l["amount"] if l["direction"] == "in" else -l["amount"]
        dep = money(l["amount"]) if l["direction"] == "in" else ""
        wd = money(l["amount"]) if l["direction"] == "out" else ""
        rows += (f"<tr><td>{fmt_us_slash(d(l['date']))}</td><td>{l['description']}</td>"
                 f"<td>{wd}</td><td>{dep}</td><td>{money(running)}</td></tr>")
    return f"""<html><head><style>{STATEMENT_CSS}</style></head><body>
<div class="head">
  <div class="bankname">{BANK_NAME}</div>
  <div>{BANK_ADDRESS}<br>{BANK_PHONE}</div>
</div>
<p><b>{COMPANY_NAME}</b><br>{COMPANY_ADDRESS}</p>
<p><b>Account:</b> {account_label} {mask} &nbsp; <b>Statement Period:</b> {period_label}</p>
<table>
<tr><th>Date</th><th>Description</th><th>Withdrawals</th><th>Deposits</th><th>Balance</th></tr>
{rows}
</table>
<div class="balances">Beginning Balance: {money(stmt['opening_balance'])} &nbsp;&nbsp; Ending Balance: {money(stmt['closing_balance'])}</div>
</body></html>"""


for stmt in STATEMENTS:
    is_op = stmt["account_code"] == OPERATING_CODE
    label = "Business Checking - Operating" if is_op else "Business Checking - Payroll"
    mask = OPERATING_ACCT_MASK if is_op else PAYROLL_ACCT_MASK
    ym = stmt["stmt_period_start"][:7]
    rel = f"bank/{'operating' if is_op else 'payroll'}/{ym}.pdf"
    R.render_html_to_pdf(statement_html(stmt, label, mask), os.path.join(MATERIALS_ABS, rel))

print("Stage 18: bank statement PDFs rendered.", file=sys.stderr)

# ---------------------------------------------------------------------------
# CSV export (mandated defect 10): Jan-Jun operating account, different
# column names and date format from the PDFs, duplicating the same period.
# Not referenced by any ledger doc_ids.
# ---------------------------------------------------------------------------

csv_rows = []
for stmt in STATEMENTS:
    if stmt["account_code"] != OPERATING_CODE or stmt["stmt_period_start"][:7] > "2025-06":
        continue
    running = stmt["opening_balance"]
    for l in stmt["lines"]:
        running += l["amount"] if l["direction"] == "in" else -l["amount"]
        csv_rows.append([
            iso(d(l["date"])),
            l["description"],
            f"{l['amount']/100:.2f}" if l["direction"] == "out" else "",
            f"{l['amount']/100:.2f}" if l["direction"] == "in" else "",
            f"{running/100:.2f}",
        ])
R.write_csv(os.path.join(MATERIALS_ABS, "bank/operating/export/operating-export-2025-01-to-06.csv"),
            csv_rows, header=["Txn Date", "Memo", "Debit Amount", "Credit Amount", "Running Balance"])

print("Stage 19: CSV export rendered.", file=sys.stderr)

# ---------------------------------------------------------------------------
# opening_position.json
# ---------------------------------------------------------------------------

OPENING_POSITION = {
    "period_start": PERIOD_START,
    "period_end": PERIOD_END,
    "as_of": AS_OF,
    "cash_by_account": {
        OPERATING_CODE: {"amount_cents": OPENING_CASH_OP, "doc_ids": [DOC_OPEN]},
        PAYROLL_CODE: {"amount_cents": OPENING_CASH_PR, "doc_ids": [DOC_OPEN]},
    },
    "accounts_receivable": [
        {"debtor": debtor, "amount_cents": amt, "doc_ids": [DOC_OPEN]} for debtor, amt in OPENING_AR
    ],
    "accounts_payable": [
        {"creditor": creditor, "amount_cents": amt, "doc_ids": [DOC_OPEN]} for creditor, amt in OPENING_AP
    ],
    "equity_components": {
        "member_capital_a_ferrone": {"account_code": MEMBER_A_CODE, "amount_cents": OPENING_CAPITAL_A, "doc_ids": [DOC_OPEN]},
        "member_capital_l_ferrone": {"account_code": MEMBER_L_CODE, "amount_cents": OPENING_CAPITAL_L, "doc_ids": [DOC_OPEN]},
    },
    "other_balances": {
        "1300": {"amount_cents": OPENING_INVENTORY, "doc_ids": [DOC_OPEN, DOC_STOCK_OPEN]},
        "2100": {"amount_cents": OPENING_SALES_TAX_PAYABLE, "doc_ids": [DOC_OPEN]},
    },
}

# ---------------------------------------------------------------------------
# Write the four lab data files.
# ---------------------------------------------------------------------------

os.makedirs(LAB_OUT, exist_ok=True)
L.write_ledger(os.path.join(LAB_OUT, "ledger.jsonl"), LEDGER)
L.write_documents(os.path.join(LAB_OUT, "documents.jsonl"), DOCUMENTS)
L.write_statements(os.path.join(LAB_OUT, "statements.jsonl"), STATEMENTS)
L.write_opening_position(os.path.join(LAB_OUT, "opening_position.json"), OPENING_POSITION)

# ---------------------------------------------------------------------------
# Self-check summary (also used to populate the answer key / final report).
# ---------------------------------------------------------------------------

totals = L.balance_sheet_totals(LEDGER, as_of=PERIOD_END)
revenue_c = totals.income
cogs_and_expense_c = totals.expense
net_income_c = totals.income - totals.expense
assets_c = totals.assets
liabilities_c = totals.liabilities
equity_c = totals.equity

unbalanced = L.unbalanced_entries(LEDGER)
assert not unbalanced, unbalanced
assert assets_c == liabilities_c + equity_c + totals.income - totals.expense

file_count = sum(len(files) for _, _, files in os.walk(MATERIALS_ABS))
total_bytes = sum(
    os.path.getsize(os.path.join(dp, fn))
    for dp, _, files in os.walk(MATERIALS_ABS) for fn in files
)

print("=" * 70)
print(f"Revenue (net, after credit note):     {money(revenue_c)}")
print(f"Total expense (incl. COGS):            {money(cogs_and_expense_c)}")
print(f"Net income:                            {money(net_income_c)}")
print(f"Assets @ period end:                   {money(assets_c)}")
print(f"Liabilities @ period end:               {money(liabilities_c)}")
print(f"Equity @ period end:                    {money(equity_c)}")
print(f"Closing operating cash:                {money(L.account_balance_cents(LEDGER, OPERATING_CODE, as_of=PERIOD_END))}")
print(f"Closing payroll cash:                  {money(L.account_balance_cents(LEDGER, PAYROLL_CODE, as_of=PERIOD_END))}")
print(f"Closing inventory:                     {money(L.account_balance_cents(LEDGER, '1300', as_of=PERIOD_END))}")
print(f"Closing AR:                            {money(L.account_balance_cents(LEDGER, '1200', as_of=PERIOD_END))}")
print(f"Closing AP:                            {money(L.account_balance_cents(LEDGER, '2000', as_of=PERIOD_END))}")
print(f"Closing sales tax payable:             {money(L.account_balance_cents(LEDGER, '2100', as_of=PERIOD_END))}")
print(f"File count under materials:            {file_count}")
print(f"Total bytes under materials:           {total_bytes} ({total_bytes/1_000_000:.2f} MB)")
print(f"Unpaid AR at period end ({len(ar_open_unpaid)}):")
for inv_no, name, amt, dat in ar_open_unpaid:
    print(f"  {inv_no}  {name:30s} {money(amt):>12s}  issued {dat}")
print(f"Unpaid AP at period end ({len(ap_open_unpaid)}):")
for bill_no, name, amt, dat in ap_open_unpaid:
    print(f"  {bill_no}  {name:30s} {money(amt):>12s}  issued {dat}")
print("=" * 70)
print("generate.py: done.")

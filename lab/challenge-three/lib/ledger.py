"""
lib/ledger.py -- FROZEN after Stage A. Do not edit from Stage B.

Read/write helpers for the challenge-three ledger, document registry,
bank-statement registry and opening-position file, plus the shared chart
of accounts, balance computation, trial balance, and the NY sales-tax
quarter constant. See SPEC.md for the full contract these implement.

All amounts are integer cents. All dates are ISO 'YYYY-MM-DD' strings
inside these files (source documents may vary their date format
deliberately -- that variance lives only in rendered documents, never
in these machine-readable files).
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# Chart of accounts
#
# Every account code used in ledger.jsonl MUST appear here. "type" is one
# of asset/liability/equity/income/expense. "normal_side" is "debit" or
# "credit": the side on which a positive balance for that account sits.
# "is_cash" flags an account as a bank/cash account whose lines must be
# traceable to a statements.jsonl entry (see SPEC.md checks 1-3).
# ---------------------------------------------------------------------------

CHART: dict[str, dict[str, Any]] = {
    # --- Assets ---
    "1000": {"name": "Cash - Operating",              "type": "asset",     "normal_side": "debit",  "is_cash": True},
    "1010": {"name": "Cash - Payroll",                 "type": "asset",     "normal_side": "debit",  "is_cash": True},
    "1020": {"name": "Cash - Secondary Operating",     "type": "asset",     "normal_side": "debit",  "is_cash": True},
    "1200": {"name": "Accounts Receivable",            "type": "asset",     "normal_side": "debit",  "is_cash": False},
    "1300": {"name": "Inventory",                      "type": "asset",     "normal_side": "debit",  "is_cash": False},
    "1400": {"name": "Prepaid Expenses",                "type": "asset",     "normal_side": "debit",  "is_cash": False},
    "1500": {"name": "Fixed Assets - Equipment",        "type": "asset",     "normal_side": "debit",  "is_cash": False},
    "1510": {"name": "Fixed Assets - Vehicles",         "type": "asset",     "normal_side": "debit",  "is_cash": False},
    "1590": {"name": "Accumulated Depreciation",        "type": "asset",     "normal_side": "credit", "is_cash": False},
    # --- Liabilities ---
    "2000": {"name": "Accounts Payable",                "type": "liability", "normal_side": "credit", "is_cash": False},
    "2100": {"name": "Sales Tax Payable",               "type": "liability", "normal_side": "credit", "is_cash": False},
    "2200": {"name": "Accrued Payroll Liabilities",     "type": "liability", "normal_side": "credit", "is_cash": False},
    "2300": {"name": "Credit Card Payable",             "type": "liability", "normal_side": "credit", "is_cash": False},
    "2400": {"name": "Loan Payable - Current Portion",  "type": "liability", "normal_side": "credit", "is_cash": False},
    "2410": {"name": "Loan Payable - Long-Term Portion","type": "liability", "normal_side": "credit", "is_cash": False},
    # --- Equity: LLC (Ferrone) ---
    "3000": {"name": "Member Capital - A. Ferrone",     "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3010": {"name": "Member Capital - L. Ferrone",     "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3020": {"name": "Member Distributions - A. Ferrone","type": "equity",   "normal_side": "debit",  "is_cash": False},
    "3030": {"name": "Member Distributions - L. Ferrone","type": "equity",   "normal_side": "debit",  "is_cash": False},
    # --- Equity: Partnership (Halloran & Vance) ---
    "3100": {"name": "Partner Capital - Halloran",      "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3110": {"name": "Partner Capital - Vance",         "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3120": {"name": "Partner Draws - Halloran",        "type": "equity",    "normal_side": "debit",  "is_cash": False},
    "3130": {"name": "Partner Draws - Vance",           "type": "equity",    "normal_side": "debit",  "is_cash": False},
    # --- Equity: Corporation (Bright Harbor) ---
    "3200": {"name": "Common Stock",                    "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3210": {"name": "Additional Paid-In Capital",      "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3220": {"name": "Retained Earnings",                "type": "equity",    "normal_side": "credit", "is_cash": False},
    "3230": {"name": "Shareholder Distributions",        "type": "equity",    "normal_side": "debit",  "is_cash": False},
    # --- Income ---
    "4000": {"name": "Sales Revenue",                    "type": "income",    "normal_side": "credit", "is_cash": False},
    "4900": {"name": "Other Income",                     "type": "income",    "normal_side": "credit", "is_cash": False},
    # --- Cost of goods / expense ---
    "5000": {"name": "Cost of Goods Sold",                "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6000": {"name": "Rent Expense",                     "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6010": {"name": "Utilities Expense",                "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6020": {"name": "Wages Expense",                    "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6030": {"name": "Payroll Tax Expense",               "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6040": {"name": "Subcontractor Expense",             "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6050": {"name": "Office Supplies Expense",           "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6060": {"name": "Insurance Expense",                 "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6070": {"name": "Professional Fees Expense",         "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6080": {"name": "Bank Fees Expense",                 "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6090": {"name": "Interest Expense",                  "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6100": {"name": "Depreciation Expense",              "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6110": {"name": "Vehicle Expense",                   "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6130": {"name": "Advertising & Marketing Expense",   "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6140": {"name": "Repairs & Maintenance Expense",     "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6150": {"name": "Telephone & Internet Expense",      "type": "expense",   "normal_side": "debit",  "is_cash": False},
    "6900": {"name": "Miscellaneous Expense",             "type": "expense",   "normal_side": "debit",  "is_cash": False},
}

CASH_ACCOUNTS = {code for code, meta in CHART.items() if meta["is_cash"]}


def account_meta(code: str) -> dict[str, Any]:
    if code not in CHART:
        raise KeyError(f"account code {code!r} is not in the shared chart of accounts")
    return CHART[code]


def signed_amount_cents(line: dict[str, Any]) -> int:
    """Return this line's amount as +debit/-credit in cents (raw, not normal-side-adjusted)."""
    return int(line.get("debit", 0)) - int(line.get("credit", 0))


def normal_side_amount_cents(line: dict[str, Any]) -> int:
    """Return this line's amount in cents, sign-adjusted so a positive number
    always means 'increases the account's normal-side balance'."""
    meta = account_meta(line["account_code"])
    raw = signed_amount_cents(line)
    return raw if meta["normal_side"] == "debit" else -raw


# ---------------------------------------------------------------------------
# NY sales tax quarters (fixed constant -- see SPEC.md ruling on quarters).
# NY quarterly sales tax periods are NOT calendar quarters. Each dict gives
# the filing period and the date the remittance is due (20th of the
# following month). Stage B must derive Ferrone's remittance withdrawal
# dates and period-end sales-tax-payable balance from this table, not from
# assumed Mar/Jun/Sep/Dec boundaries.
# ---------------------------------------------------------------------------

NY_SALES_TAX_QUARTERS = [
    {"period_start": "2024-09-01", "period_end": "2024-11-30", "due_date": "2024-12-20"},
    {"period_start": "2024-12-01", "period_end": "2025-02-28", "due_date": "2025-03-20"},
    {"period_start": "2025-03-01", "period_end": "2025-05-31", "due_date": "2025-06-20"},
    {"period_start": "2025-06-01", "period_end": "2025-08-31", "due_date": "2025-09-20"},
    {"period_start": "2025-09-01", "period_end": "2025-11-30", "due_date": "2025-12-20"},
    {"period_start": "2025-12-01", "period_end": "2026-02-28", "due_date": "2026-03-20"},
]


# ---------------------------------------------------------------------------
# JSONL I/O -- deterministic ordering on write
# ---------------------------------------------------------------------------

def read_jsonl(path: str) -> list[dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def _ledger_sort_key(rec: dict[str, Any]) -> tuple:
    return (rec.get("date", ""), rec.get("entry_id", ""), rec.get("account_code", ""))


def _doc_sort_key(rec: dict[str, Any]) -> tuple:
    return (rec.get("issued_date") or "", rec.get("doc_id", ""))


def _stmt_sort_key(rec: dict[str, Any]) -> tuple:
    return (rec.get("account_code", ""), rec.get("stmt_period_start", ""))


def write_jsonl(path: str, records: Iterable[dict[str, Any]], sort_key=None) -> None:
    records = list(records)
    if sort_key is not None:
        records = sorted(records, key=sort_key)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, sort_keys=True, separators=(",", ":")))
            f.write("\n")


def read_ledger(path: str) -> list[dict[str, Any]]:
    return sorted(read_jsonl(path), key=_ledger_sort_key)


def write_ledger(path: str, records: Iterable[dict[str, Any]]) -> None:
    write_jsonl(path, records, sort_key=_ledger_sort_key)


def read_documents(path: str) -> list[dict[str, Any]]:
    return sorted(read_jsonl(path), key=_doc_sort_key)


def write_documents(path: str, records: Iterable[dict[str, Any]]) -> None:
    write_jsonl(path, records, sort_key=_doc_sort_key)


def read_statements(path: str) -> list[dict[str, Any]]:
    return sorted(read_jsonl(path), key=_stmt_sort_key)


def write_statements(path: str, records: Iterable[dict[str, Any]]) -> None:
    write_jsonl(path, records, sort_key=_stmt_sort_key)


def read_opening_position(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_opening_position(path: str, data: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


# ---------------------------------------------------------------------------
# Balance computation / trial balance / period filtering
# ---------------------------------------------------------------------------

def filter_period(ledger: list[dict[str, Any]], start: str | None, end: str | None) -> list[dict[str, Any]]:
    out = []
    for line in ledger:
        d = line["date"]
        if start is not None and d < start:
            continue
        if end is not None and d > end:
            continue
        out.append(line)
    return out


def account_balance_cents(ledger: list[dict[str, Any]], account_code: str,
                           as_of: str | None = None, since: str | None = None) -> int:
    """Signed balance in the account's own normal-side convention, in cents."""
    total = 0
    for line in ledger:
        if line["account_code"] != account_code:
            continue
        if since is not None and line["date"] < since:
            continue
        if as_of is not None and line["date"] > as_of:
            continue
        total += normal_side_amount_cents(line)
    return total


def running_balance(ledger: list[dict[str, Any]], account_code: str) -> list[dict[str, Any]]:
    """Chronological running balance for one account. Deterministic order:
    (date, entry_id). Returns list of {date, entry_id, memo, delta_cents, balance_cents}."""
    lines = sorted(
        (l for l in ledger if l["account_code"] == account_code),
        key=lambda l: (l["date"], l["entry_id"]),
    )
    out = []
    running = 0
    for l in lines:
        delta = normal_side_amount_cents(l)
        running += delta
        out.append({
            "date": l["date"],
            "entry_id": l["entry_id"],
            "memo": l.get("memo", ""),
            "delta_cents": delta,
            "balance_cents": running,
        })
    return out


def trial_balance(ledger: list[dict[str, Any]], as_of: str | None = None) -> dict[str, int]:
    """account_code -> signed normal-side balance in cents, as of a date (inclusive)."""
    codes = {l["account_code"] for l in ledger}
    return {code: account_balance_cents(ledger, code, as_of=as_of) for code in codes}


def entry_balances(ledger: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    """entry_id -> (total_debit_cents, total_credit_cents) across all its lines."""
    out: dict[str, list[int]] = {}
    for l in ledger:
        d, c = out.setdefault(l["entry_id"], [0, 0])
        out[l["entry_id"]][0] = d + int(l.get("debit", 0))
        out[l["entry_id"]][1] = c + int(l.get("credit", 0))
    return {k: (v[0], v[1]) for k, v in out.items()}


def unbalanced_entries(ledger: list[dict[str, Any]]) -> list[str]:
    """entry_ids whose lines' debits and credits do not sum equal."""
    return [eid for eid, (d, c) in entry_balances(ledger).items() if d != c]


@dataclass
class BalanceSheetTotals:
    assets: int = 0
    liabilities: int = 0
    equity: int = 0
    income: int = 0
    expense: int = 0


def balance_sheet_totals(ledger: list[dict[str, Any]], as_of: str) -> BalanceSheetTotals:
    """Sums each account TYPE in that type's canonical direction: assets and
    expenses debit-positive, liabilities, equity and income credit-positive.

    Deliberately does NOT use each account's own `normal_side`. Contra
    accounts -- accumulated depreciation (asset, credit-normal) and the
    distribution/draw accounts (equity, debit-normal) -- carry a normal_side
    opposite to their type's, so a per-account normalisation would add their
    balances to assets and equity instead of subtracting them, inflating both
    sides and letting the A = L + E identity pass on a ledger that does not
    actually balance."""
    totals = BalanceSheetTotals()
    for l in ledger:
        if l["date"] > as_of:
            continue
        meta = account_meta(l["account_code"])
        t = meta["type"]
        raw = signed_amount_cents(l)  # debit-positive
        amt = raw if t in ("asset", "expense") else -raw
        if t == "asset":
            totals.assets += amt
        elif t == "liability":
            totals.liabilities += amt
        elif t == "equity":
            totals.equity += amt
        elif t == "income":
            totals.income += amt
        elif t == "expense":
            totals.expense += amt
    return totals

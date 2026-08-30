#!/usr/bin/env python3
"""
generate.py -- Bright Harbor Fabrication Inc. ("bright-harbor-fabrication")

Single deterministic source of truth for challenge three's Bright Harbor
corpus. Builds the double-entry ledger, document registry, statement
registry and opening position entirely in memory, asserts every structural
invariant, then (unless SKIP_RENDER=1) renders every shipped document from
that same data and writes:

    lab/challenge-three/bright-harbor-fabrication/{ledger,documents,
        statements}.jsonl, opening_position.json, answer-key.md
    content/21-challenges/materials/challenge-three/bright-harbor-fabrication/
        ...flat dump of shipped documents...

Run from the repo root:
    python3 lab/challenge-three/bright-harbor-fabrication/generate.py
    SKIP_RENDER=1 python3 lab/challenge-three/bright-harbor-fabrication/generate.py
"""

from __future__ import annotations

import datetime as dt
import os
import random
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LAB_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(REPO_ROOT, "lab", "challenge-three"))

from lib import ledger as L  # noqa: E402
from lib import render as R  # noqa: E402

SLUG = "bright-harbor-fabrication"
MATERIALS_DIR = os.path.join(REPO_ROOT, "content", "21-challenges", "materials", "challenge-three", SLUG)
SKIP_RENDER = os.environ.get("SKIP_RENDER", "0") == "1"

SEED = 998244353
RNG = random.Random(SEED)

# ---------------------------------------------------------------------------
# Company profile / invented entities
# ---------------------------------------------------------------------------

COMPANY_NAME = "Bright Harbor Fabrication Inc."
COMPANY_ADDR = "47-25 Vernon Boulevard, Long Island City, NY 11101"
COMPANY_EIN = "99-4471203"
COMPANY_PHONE = "(718) 555-0142"

OFFICER = "Peter Vasquez"          # majority officer-shareholder, President
OFFICER_TITLE = "President"
MINORITY_SH = "Angela Wu"          # minority shareholder, not an employee

BANK_NAME = "Steinway Savings Bank"
BANK_ADDR = "31-10 Steinway Street, Astoria, NY 11103"
BANK_ACCT_LAST4 = "4417"
CC_LAST4 = "8823"

PRIOR_CPA = "Marchetti & Voss CPAs LLP"
PRIOR_CPA_ADDR = "220 Northern Boulevard, Great Neck, NY 11021"
PRIOR_CPA_PARTNER = "Dominic Marchetti, CPA"

PAYROLL_PROVIDER = "Borough Payroll Partners"
PAYROLL_PROVIDER_ADDR = "38-01 Broadway, Astoria, NY 11103"

EQUIP_LENDER = "Empire Machinery Capital LLC"
EQUIP_LENDER_ADDR = "One Court Square, Long Island City, NY 11120"

EQUIP_VENDOR = "Cascade Metalworking Machinery Inc."
EQUIP_VENDOR_ADDR = "1180 Raritan Center Pkwy, Edison, NJ 08837"

EMPLOYEES = [
    (OFFICER, "Officer / President", 125000_00),
    ("Marcus Delgado", "Shop Foreman", 62000_00),
    ("Ivan Petrenko", "Welder / Fabricator", 54000_00),
    ("Samuel Osei", "Welder / Fabricator", 54000_00),
    ("Julia Ferraro", "Apprentice Fabricator", 42000_00),
    ("Renata Cabral", "Office Administrator", 58000_00),
]

CUSTOMERS = [
    "Whitestone Architectural Group",
    "Halcyon Builders LLC",
    "Meridian GC Corp",
    "Larkspur Design Studio",
    "Ironclad Construction NY Inc",
    "Vantage Point Architects",
    "Queensboro General Contracting",
    "Foster Lane Builders",
    "Brannigan & Cole Architects",
    "Tidewater Construction Group",
]

MATERIAL_VENDORS = [
    "Atlantic Steel Supply Co",
    "Five Boro Metals Inc",
    "QuickCoat Powder Coating LLC",
    "Precision Laser Cutting Inc",
    "Gotham Fastener & Hardware",
    "LIC Welding Supply Co",
]

SUBCONTRACTORS = [
    "Empire Rigging & Hoisting",
    "Northside Freight & Trucking",
    "QueensBoro Installation Crew LLC",
]

PERIOD_START = "2025-01-01"
PERIOD_END = "2025-12-31"
OPENING_AS_OF = "2024-12-31"

MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]


def month_days(ym: str) -> int:
    y, m = int(ym[:4]), int(ym[5:7])
    if m == 12:
        nxt = dt.date(y + 1, 1, 1)
    else:
        nxt = dt.date(y, m + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def last_day(ym: str) -> str:
    return f"{ym}-{month_days(ym):02d}"


# ---------------------------------------------------------------------------
# In-memory model
# ---------------------------------------------------------------------------

ledger: list[dict] = []
documents: list[dict] = []
stmt_lines: dict[str, list[dict]] = {"1000": [], "2300": []}

_entry_counter = [0]
_doc_counter = [0]
_doc_paths: set[str] = set()


def next_entry_id() -> str:
    _entry_counter[0] += 1
    return f"J-{_entry_counter[0]:04d}"


def next_doc_id(prefix: str) -> str:
    _doc_counter[0] += 1
    return f"DOC-{prefix}-{_doc_counter[0]:04d}"


def register_doc(kind: str, path_rel: str, fmt: str, scanned: bool,
                  issued_date: str, counterparty: str, amount, prefix: str) -> str:
    assert path_rel not in _doc_paths, (
        f"filename collision: {path_rel!r} is already assigned to another document "
        f"(this generator must not emit two documents at the same path)"
    )
    _doc_paths.add(path_rel)
    doc_id = next_doc_id(prefix)
    documents.append({
        "doc_id": doc_id,
        "kind": kind,
        "path": path_rel,
        "format": fmt,
        "scanned": scanned,
        "issued_date": issued_date,
        "counterparty": counterparty,
        "amount": amount,
    })
    return doc_id


def post(date: str, lines: list[dict], entry_id: str | None = None) -> str:
    """lines: list of dicts with account_code, debit, credit, memo,
    counterparty, doc_ids. Appends to `ledger` and to `stmt_lines` for any
    line touching 1000 or 2300 (caller must NOT also register those lines
    manually)."""
    eid = entry_id or next_entry_id()
    d_total = sum(l["debit"] for l in lines)
    c_total = sum(l["credit"] for l in lines)
    assert d_total == c_total, f"entry {eid} unbalanced: debit {d_total} credit {c_total}"
    for l in lines:
        assert (l["debit"] == 0) != (l["credit"] == 0), f"entry {eid} line has both/neither debit&credit: {l}"
        assert l["account_code"] in L.CHART, f"unknown account {l['account_code']}"
        rec = {
            "entry_id": eid,
            "date": date,
            "account_code": l["account_code"],
            "account_name": L.CHART[l["account_code"]]["name"],
            "debit": l["debit"],
            "credit": l["credit"],
            "memo": l.get("memo", ""),
            "counterparty": l.get("counterparty", ""),
            "doc_ids": l["doc_ids"],
        }
        assert rec["doc_ids"], f"entry {eid} line on {l['account_code']} has no doc_ids"
        ledger.append(rec)
    return eid


def cash_stmt_line(account_code: str, date: str, description: str, amount: int,
                    direction: str, entry_id: str) -> None:
    stmt_lines[account_code].append({
        "date": date,
        "description": description,
        "amount": amount,
        "direction": direction,
        "entry_id": entry_id,
    })


def fmt_money(cents: int) -> str:
    neg = cents < 0
    cents = abs(cents)
    s = f"${cents // 100:,}.{cents % 100:02d}"
    return f"-{s}" if neg else s


def iso_to_us(iso_date: str) -> str:
    y, m, d = iso_date.split("-")
    return f"{int(m):02d}/{int(d):02d}/{y}"


def iso_to_prose(iso_date: str) -> str:
    y, m, d = iso_date.split("-")
    return f"{int(d)} {MONTH_NAMES[int(m) - 1][:3]} {y}"


print(f"[generate.py] {SLUG}: building ledger (seed={SEED}, skip_render={SKIP_RENDER})", file=sys.stderr)

# ---------------------------------------------------------------------------
# Render job queue -- (fn, kwargs) pairs executed at the end unless
# SKIP_RENDER=1. Keeping data-model construction fast for iteration.
# ---------------------------------------------------------------------------

render_jobs: list[tuple] = []


def queue_render(fn, **kwargs) -> None:
    render_jobs.append((fn, kwargs))


def materials_path(filename: str) -> str:
    return f"content/21-challenges/materials/challenge-three/{SLUG}/{filename}"


def abs_materials_path(filename: str) -> str:
    return os.path.join(MATERIALS_DIR, filename)


# ===========================================================================
# Amortization helper (fixed monthly payment, standard declining-balance) --
# defined here, ahead of Section 1, because the opening position (below)
# needs the vehicle loan's outstanding balance as at 2024-12-31, which is
# itself a row of the vehicle loan's amortization schedule computed from
# its true, older origination date (see Section 0.5 immediately below).
# ===========================================================================

def build_amortization(principal_cents: int, annual_rate: float, n_periods: int) -> list[dict]:
    r = annual_rate / 12.0
    if r == 0:
        payment = round(principal_cents / n_periods)
    else:
        payment = round(principal_cents * r / (1 - (1 + r) ** (-n_periods)))
    rows = []
    balance = principal_cents
    for i in range(1, n_periods + 1):
        interest = round(balance * r)
        principal = payment - interest
        if i == n_periods or principal > balance:
            principal = balance
            payment_i = principal + interest
        else:
            payment_i = payment
        balance -= principal
        rows.append({
            "period": i, "payment": payment_i, "interest": interest,
            "principal": principal, "balance": balance,
        })
        if balance <= 0:
            break
    return rows


def add_months(iso_date: str, n: int) -> str:
    """Add n calendar months to an ISO date, keeping the same day-of-month."""
    y, m, d = (int(x) for x in iso_date.split("-"))
    total = (y * 12 + (m - 1)) + n
    ny, nm = divmod(total, 12)
    return f"{ny:04d}-{nm + 1:02d}-{d:02d}"


# ===========================================================================
# SECTION 0.5: Vehicle loan -- genuinely older, running off across 2025.
#
# Fixes a defect: the loan is drawn well before the 2025 period (an existing
# work-truck loan, not something that originates the same year the opening
# letter reports its year-end balance). The full amortization schedule runs
# from the true origination date; the schedule's outstanding balance at
# 2024-12-31 (row 48 of 60) becomes the opening letter's stated balance, and
# the twelve 2025 monthly payments are rows 49-60 of that same schedule --
# so origination, opening letter and the twelve bank payments all agree.
# ===========================================================================

# Original principal must not exceed the vehicle's own recorded cost
# ($42,000.00, OPEN_VEHICLE_COST below) -- a $36,000 loan against a $42,000
# truck (a plausible ~$6,000 down payment) is a real financing, unlike a
# loan bigger than the asset it collateralizes. Origination two years before
# the opening date (not five) also keeps the vehicle's months-in-service
# figure small enough that opening accumulated depreciation -- derived below
# (Section 1) from the stated policy, not asserted as a bare constant --
# comes out positive and modest, so this fix does not trade a date
# contradiction for an amount contradiction or an unreachable depreciation
# figure.
VEHICLE_LOAN_RATE = 0.059                    # 5.9% APR
VEHICLE_LOAN_TERM_MONTHS = 36                # 3-year term
VEHICLE_LOAN_ORIGINAL_PRINCIPAL = 3_600_000  # $36,000.00, financed at purchase
VEHICLE_LOAN_ORIGINATION_DATE = "2022-12-15"     # date the loan was signed
VEHICLE_LOAN_FIRST_PAYMENT_DATE = "2023-01-10"   # first of 36 monthly payments
VEHICLE_PAYMENT_DAY = 10                     # 10th of each month, throughout

vehicle_amort_full = build_amortization(
    VEHICLE_LOAN_ORIGINAL_PRINCIPAL, VEHICLE_LOAN_RATE, VEHICLE_LOAN_TERM_MONTHS
)
assert len(vehicle_amort_full) == VEHICLE_LOAN_TERM_MONTHS
# Payment 24 of 36 falls in December 2024 (first payment Jan 2023 -> Dec 2024
# is the 24th monthly payment); its ending balance is what the opening letter
# states as the loan's balance at 2024-12-31.
OPEN_VEHICLE_LOAN = vehicle_amort_full[23]["balance"]
# Payments 25-36 of 36 are the twelve 2025 payments (Jan-Dec 2025).
vehicle_amort_2025 = vehicle_amort_full[24:36]
assert len(vehicle_amort_2025) == 12
assert vehicle_amort_2025[-1]["balance"] == 0, "vehicle loan must fully retire in 2025"

# Number of whole months the vehicle has been in service by the opening
# date -- pinned to the loan's own elapsed payment count (Jan 2023 through
# Dec 2024 inclusive), since the letter ties the loan's origination to the
# vehicle's purchase. Used below (Section 1) to derive opening accumulated
# depreciation itself from the depreciation policy, rather than asserting a
# number that the policy could never reproduce.
VEHICLE_MONTHS_IN_SERVICE_AT_OPEN = 24

_vly, _vlm, _vld = VEHICLE_LOAN_ORIGINATION_DATE.split("-")
_vehicle_loan_origination_prose = f"{MONTH_NAMES[int(_vlm) - 1]} {_vly}"  # e.g. "December 2022", for prose use in the opening letter

print(f"[generate.py] vehicle loan: originated {VEHICLE_LOAN_ORIGINATION_DATE} for "
      f"${VEHICLE_LOAN_ORIGINAL_PRINCIPAL/100:,.2f}, balance at 2024-12-31 = "
      f"${OPEN_VEHICLE_LOAN/100:,.2f}, retires in full by December 2025", file=sys.stderr)


# ===========================================================================
# SECTION 1: Opening position (OB-1) -- 2024-12-31
# ===========================================================================

OPEN_CASH = 9_500_000          # $95,000.00
OPEN_AR = [
    ("Halcyon Builders LLC", 1_840_000),   # $18,400.00
    ("Meridian GC Corp", 920_000),          # $9,200.00
]
OPEN_AP = [
    ("Atlantic Steel Supply Co", 1_130_000),  # $11,300.00
    ("Five Boro Metals Inc", 475_000),        # $4,750.00
]
# Equipment cost is solved (not a round number) so that opening accumulated
# depreciation -- computed below FROM the stated depreciation policy, not
# asserted as a bare constant -- both reproduces the policy exactly (whole
# months x the policy's own monthly rate) and keeps the retained-earnings
# plug pinned at exactly $188,800.00 (asserted below). See
# EQUIPMENT_MONTHS_IN_SERVICE_AT_OPEN / VEHICLE_MONTHS_IN_SERVICE_AT_OPEN.
OPEN_EQUIPMENT_COST = 21_043_887    # $210,438.87 (existing shop equipment)
OPEN_VEHICLE_COST = 4_200_000       # $42,000.00 (existing work vehicle)
EQUIPMENT_MONTHS_IN_SERVICE_AT_OPEN = 5   # whole months by 2024-12-31
_equip_monthly_dep_at_open = round(OPEN_EQUIPMENT_COST / 7 / 12)   # policy: 7-year life
_vehicle_monthly_dep_at_open = round(OPEN_VEHICLE_COST / 5 / 12)   # policy: 5-year life
# Opening accumulated depreciation is now DERIVED from the stated policy and
# each asset's whole months in service -- not an independent constant that
# the policy could never reproduce (that was itself a latent, undiscovered
# version of the Defect 1 problem: a shipped figure with no way back to it
# from the shipped documents).
OPEN_ACCUM_DEP = (VEHICLE_MONTHS_IN_SERVICE_AT_OPEN * _vehicle_monthly_dep_at_open
                  + EQUIPMENT_MONTHS_IN_SERVICE_AT_OPEN * _equip_monthly_dep_at_open)  # $29,326.10 (credit)
OPEN_CC_BALANCE = 315_000           # $3,150.00 (credit)
# OPEN_VEHICLE_LOAN is computed in Section 0.5 above, from the vehicle loan's
# own amortization schedule (its balance as at 2024-12-31) -- not a bare
# constant, so it can never drift out of step with the schedule again.
OPEN_COMMON_STOCK = 5_000_000       # $50,000.00
OPEN_APIC = 7_500_000               # $75,000.00
OPEN_RETAINED_EARNINGS = 18_880_000  # $18,880.00... wait see below, recompute

# Recompute retained earnings as the plug so OB-1 balances exactly.
_ar_total = sum(a for _, a in OPEN_AR)
_ap_total = sum(a for _, a in OPEN_AP)
_debits = OPEN_CASH + _ar_total + OPEN_EQUIPMENT_COST + OPEN_VEHICLE_COST
_credits_known = OPEN_ACCUM_DEP + _ap_total + OPEN_CC_BALANCE + OPEN_VEHICLE_LOAN + OPEN_COMMON_STOCK + OPEN_APIC
OPEN_RETAINED_EARNINGS = _debits - _credits_known
assert OPEN_RETAINED_EARNINGS > 0, "retained earnings plug went negative -- check opening figures"
assert OPEN_RETAINED_EARNINGS == 18_880_000, (
    f"retained earnings plug drifted off $188,800.00 (got {OPEN_RETAINED_EARNINGS}); "
    f"the opening letter must state common stock, APIC and retained earnings unchanged"
)

DEPRECIATION_POLICY_TEXT = (
    "Fixed assets are recorded at cost and depreciated on a straight-line "
    "basis, no salvage value assumed, beginning the month following the "
    "date each asset is placed in service. By asset class: Fixed Assets - "
    "Equipment (account 1500), including fabrication machinery, is "
    "depreciated over a 7-year useful life (approximately 14.29% per year); "
    "Fixed Assets - Vehicles (account 1510) is depreciated over a 5-year "
    "useful life (20% per year)."
)

# Opening letter as a single PDF document (registered now; rendered later).
DOC_OPEN = register_doc(
    kind="opening_letter",
    path_rel=materials_path("opening_position_letter.pdf"),
    fmt="pdf",
    scanned=False,
    issued_date="January 14, 2025",
    counterparty=PRIOR_CPA,
    amount=None,
    prefix="OPEN",
)

ob_lines = []
ob_lines.append({"account_code": "1000", "debit": OPEN_CASH, "credit": 0,
                  "memo": "Opening cash - operating account", "counterparty": BANK_NAME, "doc_ids": [DOC_OPEN]})
for debtor, amt in OPEN_AR:
    ob_lines.append({"account_code": "1200", "debit": amt, "credit": 0,
                      "memo": f"Opening accounts receivable - {debtor}", "counterparty": debtor, "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "1500", "debit": OPEN_EQUIPMENT_COST, "credit": 0,
                  "memo": "Opening fixed assets - fabrication equipment (cost)", "counterparty": "", "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "1510", "debit": OPEN_VEHICLE_COST, "credit": 0,
                  "memo": "Opening fixed assets - work vehicle (cost)", "counterparty": "", "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "1590", "debit": 0, "credit": OPEN_ACCUM_DEP,
                  "memo": "Opening accumulated depreciation", "counterparty": "", "doc_ids": [DOC_OPEN]})
for creditor, amt in OPEN_AP:
    ob_lines.append({"account_code": "2000", "debit": 0, "credit": amt,
                      "memo": f"Opening accounts payable - {creditor}", "counterparty": creditor, "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "2300", "debit": 0, "credit": OPEN_CC_BALANCE,
                  "memo": "Opening business credit card balance", "counterparty": f"{BANK_NAME} Business Visa", "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "2400", "debit": 0, "credit": OPEN_VEHICLE_LOAN,
                  "memo": "Opening vehicle loan payable - current portion", "counterparty": BANK_NAME, "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "3200", "debit": 0, "credit": OPEN_COMMON_STOCK,
                  "memo": "Opening common stock", "counterparty": "", "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "3210", "debit": 0, "credit": OPEN_APIC,
                  "memo": "Opening additional paid-in capital", "counterparty": "", "doc_ids": [DOC_OPEN]})
ob_lines.append({"account_code": "3220", "debit": 0, "credit": OPEN_RETAINED_EARNINGS,
                  "memo": "Opening retained earnings", "counterparty": "", "doc_ids": [DOC_OPEN]})

post(OPENING_AS_OF, ob_lines, entry_id="OB-1")

print(f"[generate.py] opening retained earnings plug = {fmt_money(OPEN_RETAINED_EARNINGS)}", file=sys.stderr)


# ===========================================================================
# Pre-register the monthly bank / credit-card statement documents up front so
# every cash-touching ledger line posted below can cite the real doc_id for
# the statement that will actually carry it. August's operating-account
# statement is split across two scan files (Mandated shape requirement).
# ===========================================================================

BANK_STMT_FILENAMES = {
    "2025-01": ["Statement (1).pdf"],
    "2025-02": ["bank feb.pdf"],
    "2025-03": ["scan0014.pdf"],
    "2025-04": ["bank apr.pdf"],
    "2025-05": ["Statement (5).pdf"],
    "2025-06": ["Scanned Documents 2.pdf"],
    "2025-07": ["scan0021.pdf"],
    "2025-08": ["bank aug pt1.pdf", "bank aug pt2.pdf"],
    "2025-09": ["Statement (9).pdf"],
    "2025-10": ["scan0033.pdf"],
    "2025-11": ["Scanned Documents 4.pdf"],
    "2025-12": ["bank dec.pdf"],
}

CC_STMT_FILENAMES = {
    "2025-01": "visa jan.pdf",
    "2025-02": "Business Card Statement.pdf",
    "2025-03": "visa mar.pdf",
    "2025-04": "card statement (2).pdf",
    "2025-05": "visa may.pdf",
    "2025-06": "Copy of card statement.pdf",
    "2025-07": "visa jul.pdf",
    "2025-08": "card statement (3).pdf",
    "2025-09": "visa sept.pdf",
    "2025-10": "Business Card Statement 2.pdf",
    "2025-11": "visa nov.pdf",
    "2025-12": "card statement dec.pdf",
}

BANK_STMT_DOC_IDS: dict[str, list[str]] = {}
CC_STMT_DOC_IDS: dict[str, str] = {}

for ym in MONTHS:
    ids = []
    for fn in BANK_STMT_FILENAMES[ym]:
        did = register_doc(
            kind="bank_statement",
            path_rel=materials_path(fn),
            fmt="pdf",
            scanned=True,
            issued_date=iso_to_us(last_day(ym)),
            counterparty=BANK_NAME,
            amount=None,
            prefix=f"STMT{ym.replace('-', '')}",
        )
        ids.append(did)
    BANK_STMT_DOC_IDS[ym] = ids

    fn = CC_STMT_FILENAMES[ym]
    did = register_doc(
        kind="credit_card_statement",
        path_rel=materials_path(fn),
        fmt="pdf",
        scanned=False,
        issued_date=iso_to_prose(last_day(ym)),
        counterparty=f"{BANK_NAME} Business Visa",
        amount=None,
        prefix=f"CC{ym.replace('-', '')}",
    )
    CC_STMT_DOC_IDS[ym] = did


def bank_doc_ids(ym: str) -> list[str]:
    return BANK_STMT_DOC_IDS[ym]


def cc_doc_id(ym: str) -> str:
    return CC_STMT_DOC_IDS[ym]


# ===========================================================================
# SECTION 2: Vehicle loan -- the twelve 2025 payments, rows 49-60 of the
# schedule computed in Section 0.5 above (origination, rate, term and the
# opening balance all live there so this section cannot drift from them).
# ===========================================================================

DOC_VEHICLE_AMORT = register_doc(
    kind="loan_amortization",
    path_rel=materials_path("steinway_vehicle_loan_schedule.pdf"),
    fmt="pdf",
    scanned=False,
    issued_date=iso_to_us(VEHICLE_LOAN_ORIGINATION_DATE),
    counterparty=BANK_NAME,
    amount=None,
    prefix="VAMORT",
)

for i, row in enumerate(vehicle_amort_2025):
    ym = MONTHS[i]
    date = f"{ym}-{VEHICLE_PAYMENT_DAY:02d}"
    eid = next_entry_id()
    lines = [
        {"account_code": "6090", "debit": row["interest"], "credit": 0,
         "memo": f"Vehicle loan interest - payment {row['period']}/{VEHICLE_LOAN_TERM_MONTHS}", "counterparty": BANK_NAME,
         "doc_ids": [DOC_VEHICLE_AMORT]},
        {"account_code": "2400", "debit": row["principal"], "credit": 0,
         "memo": f"Vehicle loan principal - payment {row['period']}/{VEHICLE_LOAN_TERM_MONTHS}", "counterparty": BANK_NAME,
         "doc_ids": [DOC_VEHICLE_AMORT]},
    ]
    lines.append({"account_code": "1000", "debit": 0, "credit": row["payment"],
                  "memo": f"Vehicle loan payment - {BANK_NAME}", "counterparty": BANK_NAME,
                  "doc_ids": bank_doc_ids(ym)})
    post(date, lines, entry_id=eid)
    cash_stmt_line("1000", date, f"Loan pmt - {BANK_NAME} auto loan", row["payment"], "out", eid)

VEHICLE_LOAN_TOTAL_INTEREST = sum(r["interest"] for r in vehicle_amort_2025)
print(f"[generate.py] vehicle loan: {len(vehicle_amort_2025)} payments in 2025 (of "
      f"{VEHICLE_LOAN_TERM_MONTHS} total), 2025 interest {fmt_money(VEHICLE_LOAN_TOTAL_INTEREST)}", file=sys.stderr)


# ===========================================================================
# SECTION 3: Press brake purchase + equipment term loan draw -- Q2 2025
# ===========================================================================

PRESS_BRAKE_COST = 15_120_000        # $151,200.00
PRESS_BRAKE_DOWN = 1_000_000         # $10,000.00 cash down payment
EQUIP_LOAN_PRINCIPAL = PRESS_BRAKE_COST - PRESS_BRAKE_DOWN  # $141,200.00
EQUIP_LOAN_RATE = 0.0825
EQUIP_LOAN_TERM_MONTHS = 60

PRESS_BRAKE_INVOICE_DATE = "2025-04-10"
PRESS_BRAKE_IN_SERVICE_DATE = "2025-04-20"
EQUIP_LOAN_DRAW_DATE = "2025-04-15"

equip_amort = build_amortization(EQUIP_LOAN_PRINCIPAL, EQUIP_LOAN_RATE, EQUIP_LOAN_TERM_MONTHS)

DOC_PRESS_BRAKE_INVOICE = register_doc(
    kind="bill_in",
    path_rel=materials_path("IMG_5502.jpg"),
    fmt="jpg",
    scanned=True,  # produced via photograph_receipt() -- see render_press_brake_invoice()
    issued_date="04/10/2025",
    counterparty=EQUIP_VENDOR,
    amount=PRESS_BRAKE_COST,
    prefix="PRESSBRAKE",
)
DOC_EQUIP_AMORT = register_doc(
    kind="loan_amortization",
    path_rel=materials_path("empire_machinery_loan_schedule.pdf"),
    fmt="pdf",
    scanned=False,
    issued_date="2025-04-15",
    counterparty=EQUIP_LENDER,
    amount=None,
    prefix="EAMORT",
)

_eid = next_entry_id()
post(EQUIP_LOAN_DRAW_DATE, [
    {"account_code": "1500", "debit": PRESS_BRAKE_COST, "credit": 0,
     "memo": "Press brake purchased - Cascade Metalworking Machinery (placed in service 2025-04-20)",
     "counterparty": EQUIP_VENDOR, "doc_ids": [DOC_PRESS_BRAKE_INVOICE]},
    {"account_code": "1000", "debit": 0, "credit": PRESS_BRAKE_DOWN,
     "memo": "Down payment - press brake purchase", "counterparty": EQUIP_VENDOR,
     "doc_ids": [DOC_PRESS_BRAKE_INVOICE] + bank_doc_ids("2025-04")},
    {"account_code": "2410", "debit": 0, "credit": EQUIP_LOAN_PRINCIPAL,
     "memo": "Equipment term loan drawn - Empire Machinery Capital (press brake)",
     "counterparty": EQUIP_LENDER, "doc_ids": [DOC_EQUIP_AMORT]},
], entry_id=_eid)
cash_stmt_line("1000", EQUIP_LOAN_DRAW_DATE, "Press brake down payment - Cascade Metalworking", PRESS_BRAKE_DOWN, "out", _eid)
# Loan proceeds are paid by the lender directly to the equipment vendor and
# never touch Bright Harbor's own bank account -- common for equipment
# financing -- so there is no cash leg for the $141,200 draw itself.


# ===========================================================================
# SECTION 4: Equipment term loan monthly payments (May-Dec 2025) + year-end
# current/long-term reclassification
# ===========================================================================

EQUIP_PAYMENT_DAY = 15
equip_payments_2025 = equip_amort[0:8]  # May..Dec 2025 (draw mid-April, first payment one month later)

for i, row in enumerate(equip_payments_2025):
    ym = MONTHS[4 + i]  # May is index 4
    date = f"{ym}-{EQUIP_PAYMENT_DAY:02d}"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6090", "debit": row["interest"], "credit": 0,
         "memo": f"Equipment loan interest - payment {row['period']}/60", "counterparty": EQUIP_LENDER,
         "doc_ids": [DOC_EQUIP_AMORT]},
        {"account_code": "2410", "debit": row["principal"], "credit": 0,
         "memo": f"Equipment loan principal - payment {row['period']}/60", "counterparty": EQUIP_LENDER,
         "doc_ids": [DOC_EQUIP_AMORT]},
        {"account_code": "1000", "debit": 0, "credit": row["payment"],
         "memo": f"Equipment loan payment - {EQUIP_LENDER}", "counterparty": EQUIP_LENDER,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, f"Loan pmt - {EQUIP_LENDER}", row["payment"], "out", eid)

EQUIP_LOAN_BALANCE_YEAREND = equip_payments_2025[-1]["balance"]
EQUIP_LOAN_TOTAL_INTEREST_2025 = sum(r["interest"] for r in equip_payments_2025)

# Current portion at 2025-12-31 = principal due in the next 12 payments
# (Jan-Dec 2026), i.e. amortization rows 9..20 (0-indexed 8..19).
_next12 = equip_amort[8:20]
EQUIP_LOAN_CURRENT_PORTION = sum(r["principal"] for r in _next12)
EQUIP_LOAN_LONGTERM_PORTION = EQUIP_LOAN_BALANCE_YEAREND - EQUIP_LOAN_CURRENT_PORTION
assert EQUIP_LOAN_LONGTERM_PORTION >= 0

_eid = next_entry_id()
post(PERIOD_END, [
    {"account_code": "2410", "debit": EQUIP_LOAN_CURRENT_PORTION, "credit": 0,
     "memo": "Reclassify equipment loan principal due within 12 months to current portion",
     "counterparty": EQUIP_LENDER, "doc_ids": [DOC_EQUIP_AMORT]},
    {"account_code": "2400", "debit": 0, "credit": EQUIP_LOAN_CURRENT_PORTION,
     "memo": "Reclassify equipment loan principal due within 12 months to current portion",
     "counterparty": EQUIP_LENDER, "doc_ids": [DOC_EQUIP_AMORT]},
], entry_id=_eid)

print(f"[generate.py] equipment loan: year-end balance {fmt_money(EQUIP_LOAN_BALANCE_YEAREND)}, "
      f"current {fmt_money(EQUIP_LOAN_CURRENT_PORTION)}, long-term {fmt_money(EQUIP_LOAN_LONGTERM_PORTION)}",
      file=sys.stderr)


# ===========================================================================
# SECTION 5: Sales invoices (AR) -- revenue recognized on issuance
# ===========================================================================

INVOICE_NO_START = 1041
_invoice_no = [INVOICE_NO_START]

unpaid_ar_invoices = []  # populated for the answer key

for mi, ym in enumerate(MONTHS):
    n_invoices = 3
    for k in range(n_invoices):
        customer = CUSTOMERS[RNG.randrange(len(CUSTOMERS))]
        amount = RNG.randint(18_000_00, 42_000_00)
        day = RNG.randint(2, min(27, month_days(ym)))
        issue_date = f"{ym}-{day:02d}"
        inv_no = _invoice_no[0]
        _invoice_no[0] += 1

        doc_id = register_doc(
            kind="invoice_out",
            path_rel=materials_path(f"Invoice_{inv_no}.pdf"),
            fmt="pdf",
            scanned=False,
            issued_date=iso_to_us(issue_date),
            counterparty=customer,
            amount=amount,
            prefix=f"INV{inv_no}",
        )

        eid = next_entry_id()
        post(issue_date, [
            {"account_code": "1200", "debit": amount, "credit": 0,
             "memo": f"Invoice #{inv_no} - {customer}", "counterparty": customer, "doc_ids": [doc_id]},
            {"account_code": "4000", "debit": 0, "credit": amount,
             "memo": f"Invoice #{inv_no} - {customer}", "counterparty": customer, "doc_ids": [doc_id]},
        ], entry_id=eid)

        # Last 3 invoices of Dec and 2 of Nov remain unpaid at period end.
        leave_unpaid = (ym == "2025-12") or (ym == "2025-11" and k < 2)
        if leave_unpaid:
            unpaid_ar_invoices.append((inv_no, customer, amount, issue_date))
            continue

        lag = RNG.randint(18, 38)
        pay_date_d = dt.date.fromisoformat(issue_date) + dt.timedelta(days=lag)
        if pay_date_d > dt.date(2025, 12, 31):
            pay_date_d = dt.date(2025, 12, 29)
        pay_date = pay_date_d.isoformat()
        pay_ym = pay_date[:7]

        peid = next_entry_id()
        post(pay_date, [
            {"account_code": "1000", "debit": amount, "credit": 0,
             "memo": f"Receipt - Invoice #{inv_no} - {customer}", "counterparty": customer,
             "doc_ids": bank_doc_ids(pay_ym)},
            {"account_code": "1200", "debit": 0, "credit": amount,
             "memo": f"Receipt - Invoice #{inv_no} - {customer}", "counterparty": customer,
             "doc_ids": [doc_id]},
        ], entry_id=peid)
        cash_stmt_line("1000", pay_date, f"Deposit - {customer}", amount, "in", peid)

assert len(unpaid_ar_invoices) >= 4, f"need >=4 unpaid AR invoices, got {len(unpaid_ar_invoices)}"
TOTAL_REVENUE = sum(l["credit"] for l in ledger if l["account_code"] == "4000")
print(f"[generate.py] revenue: {fmt_money(TOTAL_REVENUE)} across {_invoice_no[0]-INVOICE_NO_START} invoices, "
      f"{len(unpaid_ar_invoices)} unpaid at period end", file=sys.stderr)


# ===========================================================================
# SECTION 6: Vendor bills (COGS -- materials, coating, cutting, hardware)
# Three months' bills are scanned together into one multi-document bundle
# PDF each (Mandated shape requirement); the rest ship standalone.
# ===========================================================================

BUNDLE_MONTHS = {"2025-03": "march bills.pdf", "2025-07": "Scanned Documents.pdf", "2025-10": "scan0040.pdf"}

BILL_NO_START = 3001
_bill_no = [BILL_NO_START]
unpaid_ap_bills = []
bundles: dict[str, dict] = {}  # ym -> {"filename":..., "bill_texts": [...], "doc_id": None}

DATE_FORMATS_CYCLE = ["us", "iso", "prose"]  # rotate issued_date formatting across bills (Mandated Defect 6)


def format_defect6(iso_date: str, idx: int) -> str:
    kind = DATE_FORMATS_CYCLE[idx % 3]
    if kind == "us":
        return iso_to_us(iso_date)
    if kind == "iso":
        return iso_date
    return iso_to_prose(iso_date)


for mi, ym in enumerate(MONTHS):
    n_bills = 2 if mi % 2 == 0 else 3
    for k in range(n_bills):
        vendor = MATERIAL_VENDORS[RNG.randrange(len(MATERIAL_VENDORS))]
        amount = RNG.randint(4_000_00, 15_000_00)
        day = RNG.randint(1, min(26, month_days(ym)))
        issue_date = f"{ym}-{day:02d}"
        bill_no = _bill_no[0]
        _bill_no[0] += 1

        in_bundle = ym in BUNDLE_MONTHS and k < 4
        scanned = in_bundle or (bill_no % 3 == 0)

        # All Nov + Dec bills remain unpaid at period end (>=4 required).
        leave_unpaid = ym in ("2025-11", "2025-12")

        bill_record = {
            "bill_no": bill_no, "vendor": vendor, "amount": amount,
            "issue_date": issue_date, "issued_date_str": format_defect6(issue_date, bill_no),
            "ym": ym, "scanned": scanned, "in_bundle": in_bundle,
            "leave_unpaid": leave_unpaid,
        }

        if in_bundle:
            bundles.setdefault(ym, {"filename": BUNDLE_MONTHS[ym], "bills": [], "doc_id": None})
            bundles[ym]["bills"].append(bill_record)
        else:
            fmt = "pdf"
            ext = "pdf"
            fname = (f"scan{bill_no:04d}.pdf" if scanned else f"bill_{vendor.split()[0].lower()}_{bill_no}.pdf")
            doc_id = register_doc(
                kind="bill_in",
                path_rel=materials_path(fname),
                fmt=fmt,
                scanned=scanned,
                issued_date=bill_record["issued_date_str"],
                counterparty=vendor,
                amount=amount,
                prefix=f"BILL{bill_no}",
            )
            bill_record["doc_id"] = doc_id
            bill_record["path_rel"] = materials_path(fname)

        eid = next_entry_id()
        post(issue_date, [
            {"account_code": "5000", "debit": amount, "credit": 0,
             "memo": f"Bill #{bill_no} - {vendor}", "counterparty": vendor,
             "doc_ids": [bill_record.get("doc_id", "__PENDING__")]},
            {"account_code": "2000", "debit": 0, "credit": amount,
             "memo": f"Bill #{bill_no} - {vendor}", "counterparty": vendor,
             "doc_ids": [bill_record.get("doc_id", "__PENDING__")]},
        ], entry_id=eid) if not in_bundle else None
        bill_record["ap_entry_id"] = eid if not in_bundle else None

        if in_bundle:
            # Deferred until the bundle's single doc_id is known (below).
            bill_record["ap_entry_id"] = None
        else:
            if leave_unpaid:
                unpaid_ap_bills.append((bill_no, vendor, amount, issue_date))
                continue
            lag = RNG.randint(20, 34)
            pay_date_d = dt.date.fromisoformat(issue_date) + dt.timedelta(days=lag)
            if pay_date_d > dt.date(2025, 12, 31):
                pay_date_d = dt.date(2025, 12, 29)
            pay_date = pay_date_d.isoformat()
            pay_ym = pay_date[:7]
            peid = next_entry_id()
            post(pay_date, [
                {"account_code": "2000", "debit": amount, "credit": 0,
                 "memo": f"Payment - Bill #{bill_no} - {vendor}", "counterparty": vendor,
                 "doc_ids": [bill_record["doc_id"]]},
                {"account_code": "1000", "debit": 0, "credit": amount,
                 "memo": f"Payment - Bill #{bill_no} - {vendor}", "counterparty": vendor,
                 "doc_ids": bank_doc_ids(pay_ym)},
            ], entry_id=peid)
            cash_stmt_line("1000", pay_date, f"Check - {vendor}", amount, "out", peid)

# Now finalize bundles: one doc_id per bundle file, then post the deferred
# AP entries for every bill inside it.
for ym, info in bundles.items():
    doc_id = register_doc(
        kind="multi_document_bundle",
        path_rel=materials_path(info["filename"]),
        fmt="pdf",
        scanned=True,
        issued_date=iso_to_us(info["bills"][0]["issue_date"]),
        counterparty="(multiple vendors)",
        amount=None,
        prefix=f"BUNDLE{ym.replace('-', '')}",
    )
    info["doc_id"] = doc_id
    for bill_record in info["bills"]:
        bill_record["doc_id"] = doc_id
        bill_record["path_rel"] = materials_path(info["filename"])
        bill_no = bill_record["bill_no"]
        vendor = bill_record["vendor"]
        amount = bill_record["amount"]
        issue_date = bill_record["issue_date"]
        eid = next_entry_id()
        post(issue_date, [
            {"account_code": "5000", "debit": amount, "credit": 0,
             "memo": f"Bill #{bill_no} - {vendor} (scanned batch)", "counterparty": vendor, "doc_ids": [doc_id]},
            {"account_code": "2000", "debit": 0, "credit": amount,
             "memo": f"Bill #{bill_no} - {vendor} (scanned batch)", "counterparty": vendor, "doc_ids": [doc_id]},
        ], entry_id=eid)
        if bill_record["leave_unpaid"]:
            unpaid_ap_bills.append((bill_no, vendor, amount, issue_date))
            continue
        lag = RNG.randint(20, 34)
        pay_date_d = dt.date.fromisoformat(issue_date) + dt.timedelta(days=lag)
        if pay_date_d > dt.date(2025, 12, 31):
            pay_date_d = dt.date(2025, 12, 29)
        pay_date = pay_date_d.isoformat()
        pay_ym = pay_date[:7]
        peid = next_entry_id()
        post(pay_date, [
            {"account_code": "2000", "debit": amount, "credit": 0,
             "memo": f"Payment - Bill #{bill_no} - {vendor}", "counterparty": vendor, "doc_ids": [doc_id]},
            {"account_code": "1000", "debit": 0, "credit": amount,
             "memo": f"Payment - Bill #{bill_no} - {vendor}", "counterparty": vendor, "doc_ids": bank_doc_ids(pay_ym)},
        ], entry_id=peid)
        cash_stmt_line("1000", pay_date, f"Check - {vendor}", amount, "out", peid)

assert len(unpaid_ap_bills) >= 4, f"need >=4 unpaid AP bills, got {len(unpaid_ap_bills)}"
TOTAL_COGS = sum(l["debit"] for l in ledger if l["account_code"] == "5000")
print(f"[generate.py] COGS: {fmt_money(TOTAL_COGS)} across {_bill_no[0]-BILL_NO_START} bills, "
      f"{len(unpaid_ap_bills)} unpaid at period end, {len(bundles)} bundles", file=sys.stderr)


# ===========================================================================
# SECTION 7: Subcontractor expense -- paid directly on/near invoice date
# ===========================================================================

SUB_INVOICE_START = 501
_sub_no = [SUB_INVOICE_START]

for mi, ym in enumerate(MONTHS):
    if mi % 2 == 1:
        continue  # roughly every other month
    sub = SUBCONTRACTORS[RNG.randrange(len(SUBCONTRACTORS))]
    amount = RNG.randint(2_800_00, 5_800_00)
    day = RNG.randint(3, min(24, month_days(ym)))
    issue_date = f"{ym}-{day:02d}"
    sub_no = _sub_no[0]
    _sub_no[0] += 1
    scanned = sub_no % 2 == 0
    fname = f"sub_invoice_{sub_no}.pdf" if not scanned else f"scan{1000+sub_no}.pdf"
    doc_id = register_doc(
        kind="bill_in",
        path_rel=materials_path(fname),
        fmt="pdf",
        scanned=scanned,
        issued_date=format_defect6(issue_date, sub_no),
        counterparty=sub,
        amount=amount,
        prefix=f"SUB{sub_no}",
    )
    pay_date_d = dt.date.fromisoformat(issue_date) + dt.timedelta(days=RNG.randint(2, 8))
    pay_date = pay_date_d.isoformat()
    pay_ym = pay_date[:7]
    eid = next_entry_id()
    post(pay_date, [
        {"account_code": "6040", "debit": amount, "credit": 0,
         "memo": f"Subcontractor - {sub}", "counterparty": sub, "doc_ids": [doc_id]},
        {"account_code": "1000", "debit": 0, "credit": amount,
         "memo": f"Subcontractor - {sub}", "counterparty": sub, "doc_ids": bank_doc_ids(pay_ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", pay_date, f"Check - {sub}", amount, "out", eid)

TOTAL_SUBCONTRACTOR = sum(l["debit"] for l in ledger if l["account_code"] == "6040")
print(f"[generate.py] subcontractor expense: {fmt_money(TOTAL_SUBCONTRACTOR)}", file=sys.stderr)


# ===========================================================================
# SECTION 8: Payroll -- officer salary runs through payroll (S-corp tell)
# ===========================================================================

# Precompute exact monthly gross pay per employee so annual totals equal the
# stated salary exactly (integer cents, remainder absorbed in December).
employee_monthly = {}
for name, title, annual in EMPLOYEES:
    base, rem = divmod(annual, 12)
    monthly = [base] * 12
    monthly[-1] += rem
    employee_monthly[name] = monthly

PAYROLL_TAX_RATE = 0.09  # blended employer-side FICA/FUTA/SUTA estimate
DOC_PAYROLL_REGISTER = register_doc(
    kind="payroll_register",
    path_rel=materials_path("Copy of payroll.xlsx"),
    fmt="xlsx",
    scanned=False,
    issued_date="2025-12-31",
    counterparty=PAYROLL_PROVIDER,
    amount=None,
    prefix="PAYREG",
)

payroll_summary_docs = {}
for mi, ym in enumerate(MONTHS):
    gross_month = sum(employee_monthly[name][mi] for name, _, _ in EMPLOYEES)
    tax_month = round(gross_month * PAYROLL_TAX_RATE)
    pay_date = f"{ym}-{min(28, month_days(ym)):02d}"

    doc_id = register_doc(
        kind="payroll_summary",
        path_rel=materials_path(f"payroll summary {MONTH_NAMES[mi].lower()}.pdf"),
        fmt="pdf",
        scanned=False,
        issued_date=format_defect6(pay_date, mi),
        counterparty=PAYROLL_PROVIDER,
        amount=gross_month + tax_month,
        prefix=f"PAYSUM{ym.replace('-', '')}",
    )
    payroll_summary_docs[ym] = doc_id

    eid = next_entry_id()
    post(pay_date, [
        {"account_code": "6020", "debit": gross_month, "credit": 0,
         "memo": f"Payroll - {MONTH_NAMES[mi]} 2025 (gross wages, 6 employees incl. officer salary)",
         "counterparty": PAYROLL_PROVIDER, "doc_ids": [doc_id, DOC_PAYROLL_REGISTER]},
        {"account_code": "6030", "debit": tax_month, "credit": 0,
         "memo": f"Payroll taxes (employer share) - {MONTH_NAMES[mi]} 2025",
         "counterparty": PAYROLL_PROVIDER, "doc_ids": [doc_id, DOC_PAYROLL_REGISTER]},
        {"account_code": "1000", "debit": 0, "credit": gross_month + tax_month,
         "memo": f"Payroll run - {MONTH_NAMES[mi]} 2025", "counterparty": PAYROLL_PROVIDER,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", pay_date, f"Payroll - {PAYROLL_PROVIDER}", gross_month + tax_month, "out", eid)

TOTAL_WAGES = sum(l["debit"] for l in ledger if l["account_code"] == "6020")
TOTAL_PAYROLL_TAX = sum(l["debit"] for l in ledger if l["account_code"] == "6030")
print(f"[generate.py] payroll: wages {fmt_money(TOTAL_WAGES)}, payroll tax {fmt_money(TOTAL_PAYROLL_TAX)}", file=sys.stderr)


# ===========================================================================
# SECTION 9: Depreciation -- straight-line by asset class, per the opening
# letter's stated policy. Existing equipment/vehicle depreciate all 12
# months; the press brake joins the equipment class the month after it is
# placed in service (2025-04-20 -> first depreciation month is May).
# ===========================================================================

EXISTING_EQUIP_MONTHLY_DEP = round(OPEN_EQUIPMENT_COST / 7 / 12)   # $2,500.00/mo
EXISTING_VEHICLE_MONTHLY_DEP = round(OPEN_VEHICLE_COST / 5 / 12)   # $700.00/mo
PRESS_BRAKE_MONTHLY_DEP = round(PRESS_BRAKE_COST / 7 / 12)         # $1,800.00/mo

PRESS_BRAKE_FIRST_DEP_MONTH = "2025-05"

total_dep_2025 = 0
for mi, ym in enumerate(MONTHS):
    doc_ids = [DOC_OPEN]
    dep = EXISTING_EQUIP_MONTHLY_DEP + EXISTING_VEHICLE_MONTHLY_DEP
    if ym >= PRESS_BRAKE_FIRST_DEP_MONTH:
        dep += PRESS_BRAKE_MONTHLY_DEP
        doc_ids = [DOC_OPEN, DOC_PRESS_BRAKE_INVOICE]
    date = last_day(ym)
    eid = next_entry_id()
    post(date, [
        {"account_code": "6100", "debit": dep, "credit": 0,
         "memo": f"Depreciation - {MONTH_NAMES[mi]} 2025 (straight-line per depreciation policy)",
         "counterparty": "", "doc_ids": doc_ids},
        {"account_code": "1590", "debit": 0, "credit": dep,
         "memo": f"Depreciation - {MONTH_NAMES[mi]} 2025 (straight-line per depreciation policy)",
         "counterparty": "", "doc_ids": doc_ids},
    ], entry_id=eid)
    total_dep_2025 += dep

TOTAL_DEPRECIATION_2025 = total_dep_2025
CLOSING_ACCUM_DEP = OPEN_ACCUM_DEP + TOTAL_DEPRECIATION_2025
print(f"[generate.py] depreciation 2025: {fmt_money(TOTAL_DEPRECIATION_2025)}, "
      f"closing accumulated depreciation {fmt_money(CLOSING_ACCUM_DEP)}", file=sys.stderr)


# ===========================================================================
# SECTION 10a: Fixed recurring monthly overhead -- lease and premium amounts
# that genuinely do not vary month to month in real business practice; paid
# directly from operating cash, evidenced by that month's bank statement.
# ===========================================================================

FIXED_RECURRING_MONTHLY = [
    ("6000", 6_250_00, "Rent - 47-25 Vernon Blvd shop space", "Vernon Blvd Realty LLC"),
    ("6060", 2_166_00, "General liability + workers comp insurance", "Harborview Insurance Brokers"),
    ("6130", 300_00, "Advertising - trade directory listing", "TradeBoard Queens"),
    ("6140", 833_00, "Shop equipment repairs and maintenance", "Various"),
    ("6900", 183_00, "Miscellaneous shop expense", "Various"),
]

for mi, ym in enumerate(MONTHS):
    date = f"{ym}-{min(27, month_days(ym)):02d}"
    for code, amount, memo, counterparty in FIXED_RECURRING_MONTHLY:
        eid = next_entry_id()
        post(date, [
            {"account_code": code, "debit": amount, "credit": 0,
             "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": counterparty,
             "doc_ids": bank_doc_ids(ym)},
            {"account_code": "1000", "debit": 0, "credit": amount,
             "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": counterparty,
             "doc_ids": bank_doc_ids(ym)},
        ], entry_id=eid)
        cash_stmt_line("1000", date, f"{memo}", amount, "out", eid)

print(f"[generate.py] fixed recurring monthly overhead posted for {len(MONTHS)} months x "
      f"{len(FIXED_RECURRING_MONTHLY)} categories", file=sys.stderr)


# ===========================================================================
# SECTION 10b: Variable recurring monthly overhead -- Utilities, Telephone &
# Internet, Vehicle Expense, Bank Fees and Professional Fees genuinely vary
# month to month: seasonal utility swing plus the Q2 press-brake electricity
# step-up (visible from June onward, once the brake is in full use and
# billed), telephone overage surcharges, fuel/maintenance swings, bank fees
# tracking transaction volume, and lumpy accountant work. Utilities,
# Telephone & Internet and Professional Fees are each additionally
# evidenced by their own annual bill bundle (twelve monthly bills from that
# vendor, concatenated into one shipped PDF -- keeps the file count down
# while still giving each varied amount a document to trace to, per vendor,
# beyond the bank statement line).
# ===========================================================================

UTILITIES_VENDOR = "Harborline Utility Co"
UTILITIES_MONTHLY = [121437, 114892, 98650, 88210, 95430, 124680,
                      154920, 161350, 142870, 118640, 121950, 137460]
UTILITY_RATE_PER_KWH_CENTS = 19.2  # illustrative, ties the bill's usage line to its amount

TELEPHONE_VENDOR = "Metro Fiber Communications"
TELEPHONE_MONTHLY = [24850, 25120, 31460, 24680, 25300, 24990,
                      25410, 34870, 25080, 24750, 29650, 25200]

VEHICLE_EXPENSE_VENDOR = "Various"
VEHICLE_EXPENSE_MONTHLY = [68900, 71200, 74850, 69300, 92600, 78400,
                            81200, 79600, 73100, 70450, 105300, 88700]

BANK_FEES_VENDOR = BANK_NAME
BANK_FEES_MONTHLY = [12500, 11800, 14200, 18900, 21500, 16800,
                      15200, 19800, 14500, 13200, 15900, 22600]

PROFESSIONAL_FEES_VENDOR = "Corrado Bookkeeping Services"
PROFESSIONAL_FEES_MONTHLY = [220000, 95000, 80000, 260000, 70000, 90000,
                              70000, 70000, 150000, 90000, 90000, 200000]
PROFESSIONAL_FEES_DESCRIPTIONS = [
    "Preparation of year-end 1099s and W-2s",
    "Monthly bookkeeping and account reconciliation",
    "Monthly bookkeeping and account reconciliation",
    "Federal and NY corporate income tax preparation",
    "Monthly bookkeeping and account reconciliation",
    "Monthly bookkeeping and account reconciliation",
    "Monthly bookkeeping and account reconciliation",
    "Monthly bookkeeping and account reconciliation",
    "Q3 tax planning and estimated payment review",
    "Monthly bookkeeping and account reconciliation",
    "Monthly bookkeeping and account reconciliation",
    "Year-end close and financial statement preparation",
]


def register_annual_bundle(vendor: str, filename: str, prefix: str) -> str:
    return register_doc(
        kind="multi_document_bundle",
        path_rel=materials_path(filename),
        fmt="pdf",
        scanned=False,
        issued_date=iso_to_us("2025-12-27"),
        counterparty=vendor,
        amount=None,
        prefix=prefix,
    )


DOC_UTILITY_BUNDLE = register_annual_bundle(UTILITIES_VENDOR, "utility bills 2025.pdf", "UTILBUNDLE")
DOC_TELEPHONE_BUNDLE = register_annual_bundle(TELEPHONE_VENDOR, "phone bills 2025.pdf", "PHONEBUNDLE")
DOC_PROFFEE_BUNDLE = register_annual_bundle(PROFESSIONAL_FEES_VENDOR, "Corrado invoices 2025.pdf", "PROFBUNDLE")

for mi, ym in enumerate(MONTHS):
    date = f"{ym}-{min(27, month_days(ym)):02d}"

    amt = UTILITIES_MONTHLY[mi]
    memo = "Utilities - electric + gas"
    if ym >= "2025-06":
        memo += " (higher usage since Q2 press brake installation)"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6010", "debit": amt, "credit": 0,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": UTILITIES_VENDOR,
         "doc_ids": bank_doc_ids(ym) + [DOC_UTILITY_BUNDLE]},
        {"account_code": "1000", "debit": 0, "credit": amt,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": UTILITIES_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, "Utilities - electric + gas", amt, "out", eid)

    amt = TELEPHONE_MONTHLY[mi]
    memo = "Telephone and internet"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6150", "debit": amt, "credit": 0,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": TELEPHONE_VENDOR,
         "doc_ids": bank_doc_ids(ym) + [DOC_TELEPHONE_BUNDLE]},
        {"account_code": "1000", "debit": 0, "credit": amt,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": TELEPHONE_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, memo, amt, "out", eid)

    amt = VEHICLE_EXPENSE_MONTHLY[mi]
    memo = "Vehicle fuel and tolls"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6110", "debit": amt, "credit": 0,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": VEHICLE_EXPENSE_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
        {"account_code": "1000", "debit": 0, "credit": amt,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": VEHICLE_EXPENSE_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, memo, amt, "out", eid)

    amt = BANK_FEES_MONTHLY[mi]
    memo = "Monthly account service fee"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6080", "debit": amt, "credit": 0,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": BANK_FEES_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
        {"account_code": "1000", "debit": 0, "credit": amt,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": BANK_FEES_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, memo, amt, "out", eid)

    amt = PROFESSIONAL_FEES_MONTHLY[mi]
    memo = f"Bookkeeping / professional fees - {PROFESSIONAL_FEES_DESCRIPTIONS[mi]}"
    eid = next_entry_id()
    post(date, [
        {"account_code": "6070", "debit": amt, "credit": 0,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": PROFESSIONAL_FEES_VENDOR,
         "doc_ids": bank_doc_ids(ym) + [DOC_PROFFEE_BUNDLE]},
        {"account_code": "1000", "debit": 0, "credit": amt,
         "memo": f"{memo} - {MONTH_NAMES[mi]} 2025", "counterparty": PROFESSIONAL_FEES_VENDOR,
         "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, "Bookkeeping / professional fees", amt, "out", eid)

print("[generate.py] variable recurring monthly overhead posted "
      "(utilities/telephone/vehicle/bank fees/professional fees)", file=sys.stderr)


# ===========================================================================
# SECTION 11: Credit card -- purchases each month, statement balance paid
# down the following month from the operating account (Mandated Defect 8).
# Includes the mandated personal expense (Mandated Defect 2, August).
# ===========================================================================

CC_PURCHASE_CATEGORIES = [
    ("6050", "Office Supplies Expense", ["Gotham Fastener & Hardware", "Metro Office Supply", "LIC Welding Supply Co"]),
    ("6140", "Repairs & Maintenance Expense", ["QueensBoro Tool Rental", "Astoria Hardware Depot"]),
    ("6900", "Miscellaneous Expense", ["Various"]),
    ("6130", "Advertising & Marketing Expense", ["TradeBoard Queens"]),
]

PERSONAL_EXPENSE_MONTH = "2025-08"
PERSONAL_EXPENSE_AMOUNT = 280_000   # $2,800.00
PERSONAL_EXPENSE_DATE = "2025-08-14"
PERSONAL_EXPENSE_VENDOR = "Skyline Atlantic Airways"

CC_PAYMENT_DAY = 18

cc_running = OPEN_CC_BALANCE
for mi, ym in enumerate(MONTHS):
    doc_id = cc_doc_id(ym)

    # Pay off whatever accumulated last month.
    amount_due = cc_running
    if amount_due > 0:
        pay_date = f"{ym}-{CC_PAYMENT_DAY:02d}"
        eid = next_entry_id()
        post(pay_date, [
            {"account_code": "2300", "debit": amount_due, "credit": 0,
             "memo": f"Credit card payment - {BANK_NAME} Business Visa", "counterparty": f"{BANK_NAME} Business Visa",
             "doc_ids": [doc_id]},
            {"account_code": "1000", "debit": 0, "credit": amount_due,
             "memo": f"Credit card payment - {BANK_NAME} Business Visa", "counterparty": f"{BANK_NAME} Business Visa",
             "doc_ids": bank_doc_ids(ym)},
        ], entry_id=eid)
        cash_stmt_line("2300", pay_date, "Payment - thank you", amount_due, "out", eid)
        cash_stmt_line("1000", pay_date, f"CC payment - {BANK_NAME} Business Visa", amount_due, "out", eid)
        cc_running -= amount_due

    # This month's purchases.
    n_purchases = RNG.randint(2, 3)
    for k in range(n_purchases):
        code, _name, vendors = CC_PURCHASE_CATEGORIES[RNG.randrange(len(CC_PURCHASE_CATEGORIES))]
        vendor = vendors[RNG.randrange(len(vendors))]
        amount = RNG.randint(120_00, 620_00)
        day = RNG.randint(2, min(26, month_days(ym)))
        date = f"{ym}-{day:02d}"
        eid = next_entry_id()
        post(date, [
            {"account_code": code, "debit": amount, "credit": 0,
             "memo": f"Card purchase - {vendor}", "counterparty": vendor, "doc_ids": [doc_id]},
            {"account_code": "2300", "debit": 0, "credit": amount,
             "memo": f"Card purchase - {vendor}", "counterparty": vendor, "doc_ids": [doc_id]},
        ], entry_id=eid)
        cash_stmt_line("2300", date, f"Purchase - {vendor}", amount, "in", eid)
        cc_running += amount

    if ym == PERSONAL_EXPENSE_MONTH:
        eid = next_entry_id()
        post(PERSONAL_EXPENSE_DATE, [
            {"account_code": "3230", "debit": PERSONAL_EXPENSE_AMOUNT, "credit": 0,
             "memo": f"Personal expense charged to business card - {PERSONAL_EXPENSE_VENDOR} "
                     f"(family travel; reclassified as shareholder distribution, not a business expense)",
             "counterparty": PERSONAL_EXPENSE_VENDOR, "doc_ids": [doc_id]},
            {"account_code": "2300", "debit": 0, "credit": PERSONAL_EXPENSE_AMOUNT,
             "memo": f"Personal expense charged to business card - {PERSONAL_EXPENSE_VENDOR}",
             "counterparty": PERSONAL_EXPENSE_VENDOR, "doc_ids": [doc_id]},
        ], entry_id=eid)
        cash_stmt_line("2300", PERSONAL_EXPENSE_DATE, f"Purchase - {PERSONAL_EXPENSE_VENDOR}",
                        PERSONAL_EXPENSE_AMOUNT, "in", eid)
        cc_running += PERSONAL_EXPENSE_AMOUNT

CC_BALANCE_YEAREND = cc_running
print(f"[generate.py] credit card: year-end balance {fmt_money(CC_BALANCE_YEAREND)}", file=sys.stderr)


# ===========================================================================
# SECTION 12: Shareholder distribution -- bank withdrawal late in the year
# (Rule Three's S-corp tell; sized together with Section 11's personal
# expense so total 2025 distributions equal closing accumulated
# depreciation exactly -- see check_7's algebra in the design notes).
# ===========================================================================

DISTRIBUTION_DATE = "2025-12-15"
DISTRIBUTION_AMOUNT = CLOSING_ACCUM_DEP - PERSONAL_EXPENSE_AMOUNT
assert DISTRIBUTION_AMOUNT > 0

_eid = next_entry_id()
post(DISTRIBUTION_DATE, [
    {"account_code": "3230", "debit": DISTRIBUTION_AMOUNT, "credit": 0,
     "memo": f"Shareholder distribution - {OFFICER}", "counterparty": OFFICER,
     "doc_ids": bank_doc_ids("2025-12")},
    {"account_code": "1000", "debit": 0, "credit": DISTRIBUTION_AMOUNT,
     "memo": f"Shareholder distribution - {OFFICER}", "counterparty": OFFICER,
     "doc_ids": bank_doc_ids("2025-12")},
], entry_id=_eid)
cash_stmt_line("1000", DISTRIBUTION_DATE, f"Withdrawal - {OFFICER}", DISTRIBUTION_AMOUNT, "out", _eid)

TOTAL_DISTRIBUTIONS = DISTRIBUTION_AMOUNT + PERSONAL_EXPENSE_AMOUNT
print(f"[generate.py] shareholder distributions total {fmt_money(TOTAL_DISTRIBUTIONS)} "
      f"(bank withdrawal {fmt_money(DISTRIBUTION_AMOUNT)} + personal card expense {fmt_money(PERSONAL_EXPENSE_AMOUNT)}); "
      f"closing accumulated depreciation {fmt_money(CLOSING_ACCUM_DEP)}", file=sys.stderr)
assert TOTAL_DISTRIBUTIONS == CLOSING_ACCUM_DEP, "check_7 invariant: distributions must equal closing accumulated depreciation"


# ===========================================================================
# SECTION 13: Ad hoc cash-account receipts -- small shop purchases paid
# directly from the operating account, each with its own photographed JPG
# receipt. Includes the duplicate receipt (Mandated Defect 1, shipped twice
# in two formats) and the handwritten cash receipt (Mandated Defect 7).
# ===========================================================================

RECEIPT_ITEMS = [
    ("2025-01-22", "6050", "Office Supplies Expense", 84_50, "Astoria Hardware Depot"),
    ("2025-02-11", "6140", "Repairs & Maintenance Expense", 212_00, "QueensBoro Tool Rental"),
    ("2025-02-27", "6050", "Office Supplies Expense", 63_20, "Metro Office Supply"),
    ("2025-03-19", "6900", "Miscellaneous Expense", 45_00, "LIC Deli & Convenience"),
    ("2025-04-08", "6050", "Office Supplies Expense", 128_75, "Astoria Hardware Depot"),
    ("2025-05-14", "6140", "Repairs & Maintenance Expense", 340_00, "Precision Laser Cutting Inc"),
    ("2025-06-06", "6050", "Office Supplies Expense", 71_40, "Metro Office Supply"),
    ("2025-07-17", "6900", "Miscellaneous Expense", 38_00, "LIC Deli & Convenience"),
    ("2025-08-25", "6050", "Office Supplies Expense", 96_10, "Astoria Hardware Depot"),
    ("2025-09-09", "6140", "Repairs & Maintenance Expense", 275_00, "QueensBoro Tool Rental"),
    ("2025-10-21", "6050", "Office Supplies Expense", 54_90, "Metro Office Supply"),
    ("2025-11-04", "6900", "Miscellaneous Expense", 60_00, "LIC Deli & Convenience"),
]

_receipt_no = [1]

for date, code, _acct_name, amount, vendor in RECEIPT_ITEMS:
    rno = _receipt_no[0]
    _receipt_no[0] += 1
    fname = f"IMG_{4400 + rno}.jpg"
    doc_id = register_doc(
        kind="receipt",
        path_rel=materials_path(fname),
        fmt="jpg",
        scanned=True,
        issued_date=format_defect6(date, rno),
        counterparty=vendor,
        amount=amount,
        prefix=f"RCPT{rno}",
    )
    eid = next_entry_id()
    ym = date[:7]
    post(date, [
        {"account_code": code, "debit": amount, "credit": 0,
         "memo": f"Receipt - {vendor}", "counterparty": vendor, "doc_ids": [doc_id]},
        {"account_code": "1000", "debit": 0, "credit": amount,
         "memo": f"Receipt - {vendor}", "counterparty": vendor, "doc_ids": bank_doc_ids(ym)},
    ], entry_id=eid)
    cash_stmt_line("1000", date, f"Debit card - {vendor}", amount, "out", eid)

# --- Mandated Defect 1: duplicate receipt, shipped twice in two formats ---
DUP_DATE = "2025-05-29"
DUP_AMOUNT = 118_40
DUP_VENDOR = "Gotham Fastener & Hardware"
dup_doc_jpg = register_doc(
    kind="receipt",
    path_rel=materials_path("receipt_001.jpeg"),
    fmt="jpg",
    scanned=True,
    issued_date=iso_to_us(DUP_DATE),
    counterparty=DUP_VENDOR,
    amount=DUP_AMOUNT,
    prefix="DUPJPG",
)
DUP_PDF_FILENAME = "Scanned Documents 3.pdf"
dup_doc_pdf = register_doc(
    kind="receipt",
    path_rel=materials_path(DUP_PDF_FILENAME),
    fmt="pdf",
    scanned=True,
    issued_date=DUP_DATE,
    counterparty=DUP_VENDOR,
    amount=DUP_AMOUNT,
    prefix="DUPPDF",
)
_eid = next_entry_id()
post(DUP_DATE, [
    {"account_code": "6050", "debit": DUP_AMOUNT, "credit": 0,
     "memo": f"Receipt - {DUP_VENDOR} (same purchase also scanned separately as {DUP_PDF_FILENAME} -- "
             f"do not double-count)", "counterparty": DUP_VENDOR, "doc_ids": [dup_doc_jpg, dup_doc_pdf]},
    {"account_code": "1000", "debit": 0, "credit": DUP_AMOUNT,
     "memo": f"Receipt - {DUP_VENDOR}", "counterparty": DUP_VENDOR, "doc_ids": bank_doc_ids("2025-05")},
], entry_id=_eid)
cash_stmt_line("1000", DUP_DATE, f"Debit card - {DUP_VENDOR}", DUP_AMOUNT, "out", _eid)

# --- Mandated Defect 7: handwritten-looking cash receipt, photographed at an angle ---
HANDWRITTEN_DATE = "2025-09-23"
HANDWRITTEN_AMOUNT = 40_00
HANDWRITTEN_VENDOR = "cash - scrap bin swap"
doc_handwritten = register_doc(
    kind="cash_receipt_handwritten",
    path_rel=materials_path("receipt_009.jpeg"),
    fmt="jpg",
    scanned=True,
    issued_date=iso_to_prose(HANDWRITTEN_DATE),
    counterparty=HANDWRITTEN_VENDOR,
    amount=HANDWRITTEN_AMOUNT,
    prefix="HANDWRITTEN",
)
_eid = next_entry_id()
post(HANDWRITTEN_DATE, [
    {"account_code": "6900", "debit": HANDWRITTEN_AMOUNT, "credit": 0,
     "memo": "Cash purchase - handwritten receipt (shop rags, petty cash)", "counterparty": HANDWRITTEN_VENDOR,
     "doc_ids": [doc_handwritten]},
    {"account_code": "1000", "debit": 0, "credit": HANDWRITTEN_AMOUNT,
     "memo": "Petty cash withdrawal for shop supplies", "counterparty": HANDWRITTEN_VENDOR,
     "doc_ids": bank_doc_ids("2025-09")},
], entry_id=_eid)
cash_stmt_line("1000", HANDWRITTEN_DATE, "ATM withdrawal - petty cash", HANDWRITTEN_AMOUNT, "out", _eid)

print(f"[generate.py] ad hoc receipts: {len(RECEIPT_ITEMS)} + 1 duplicate (2 docs) + 1 handwritten", file=sys.stderr)


# ===========================================================================
# SECTION 14: Assemble statements.jsonl -- one record per account per month
# ===========================================================================

statements: list[dict] = []
account_opening = {"1000": OPEN_CASH, "2300": OPEN_CC_BALANCE}

for account_code in ("1000", "2300"):
    running = account_opening[account_code]
    lines_by_month: dict[str, list[dict]] = {ym: [] for ym in MONTHS}
    for ln in stmt_lines[account_code]:
        ym = ln["date"][:7]
        assert ym in lines_by_month, f"stmt line dated outside 2025: {ln}"
        lines_by_month[ym].append(ln)

    for ym in MONTHS:
        month_lines = sorted(lines_by_month[ym], key=lambda l: (l["date"], l["entry_id"]))
        opening_balance = running
        credits = sum(l["amount"] for l in month_lines if l["direction"] == "in")
        debits = sum(l["amount"] for l in month_lines if l["direction"] == "out")
        closing_balance = opening_balance + credits - debits
        running = closing_balance

        if account_code == "1000":
            doc_ids = bank_doc_ids(ym)
        else:
            doc_ids = [cc_doc_id(ym)]

        statements.append({
            "stmt_id": f"STMT-{account_code}-{ym}",
            "account_code": account_code,
            "stmt_period_start": f"{ym}-01",
            "stmt_period_end": last_day(ym),
            "opening_balance": opening_balance,
            "closing_balance": closing_balance,
            "doc_ids": doc_ids,
            "lines": month_lines,
        })

print(f"[generate.py] statements: {len(statements)} records "
      f"(1000 closing Dec {fmt_money([s for s in statements if s['stmt_id']=='STMT-1000-2025-12'][0]['closing_balance'])}, "
      f"2300 closing Dec {fmt_money([s for s in statements if s['stmt_id']=='STMT-2300-2025-12'][0]['closing_balance'])})",
      file=sys.stderr)


# ===========================================================================
# SECTION 15: Structural self-checks (mirrors validate.py's core invariants,
# run before any file is written so failures are cheap to iterate on)
# ===========================================================================

unb = L.unbalanced_entries(ledger)
assert not unb, f"unbalanced entries: {unb}"

totals = L.balance_sheet_totals(ledger, as_of=PERIOD_END)
lhs = totals.assets
rhs = totals.liabilities + totals.equity + totals.income - totals.expense
assert lhs == rhs, f"check_7 equation fails: assets {lhs} != L+E+I-E {rhs} (diff {lhs - rhs})"

tb = L.trial_balance(ledger, as_of=PERIOD_END)
closing_1590 = tb.get("1590", 0)
closing_3230 = tb.get("3230", 0)
assert closing_1590 == closing_3230, f"1590 ({closing_1590}) != 3230 ({closing_3230})"

for l in ledger:
    assert l["doc_ids"], f"line missing doc_ids: {l}"

print(f"[generate.py] self-checks passed: assets={fmt_money(lhs)}, L+E+I-E={fmt_money(rhs)}, "
      f"1590={fmt_money(closing_1590)}, 3230={fmt_money(closing_3230)}", file=sys.stderr)
print(f"[generate.py] unpaid AR: {len(unpaid_ar_invoices)}, unpaid AP: {len(unpaid_ap_bills)}", file=sys.stderr)
print(f"[generate.py] total ledger lines: {len(ledger)}, total documents registered: {len(documents)}", file=sys.stderr)


# ===========================================================================
# SECTION 16: opening_position.json
# ===========================================================================

opening_position = {
    "period_start": PERIOD_START,
    "period_end": PERIOD_END,
    "as_of": OPENING_AS_OF,
    "cash_by_account": {
        "1000": {"amount_cents": OPEN_CASH, "doc_ids": [DOC_OPEN]},
    },
    "accounts_receivable": [
        {"debtor": debtor, "amount_cents": amt, "doc_ids": [DOC_OPEN]} for debtor, amt in OPEN_AR
    ],
    "accounts_payable": [
        {"creditor": creditor, "amount_cents": amt, "doc_ids": [DOC_OPEN]} for creditor, amt in OPEN_AP
    ],
    "equity_components": {
        "common_stock": {"account_code": "3200", "amount_cents": OPEN_COMMON_STOCK, "doc_ids": [DOC_OPEN]},
        "additional_paid_in_capital": {"account_code": "3210", "amount_cents": OPEN_APIC, "doc_ids": [DOC_OPEN]},
        "retained_earnings": {"account_code": "3220", "amount_cents": OPEN_RETAINED_EARNINGS, "doc_ids": [DOC_OPEN]},
    },
    "other_balances": {
        "1500": {"amount_cents": OPEN_EQUIPMENT_COST, "doc_ids": [DOC_OPEN]},
        "1510": {"amount_cents": OPEN_VEHICLE_COST, "doc_ids": [DOC_OPEN]},
        "1590": {"amount_cents": OPEN_ACCUM_DEP, "doc_ids": [DOC_OPEN]},
        "2300": {"amount_cents": OPEN_CC_BALANCE, "doc_ids": [DOC_OPEN]},
        "2400": {"amount_cents": OPEN_VEHICLE_LOAN, "doc_ids": [DOC_OPEN]},
    },
    "depreciation_policy": DEPRECIATION_POLICY_TEXT,
}


# ===========================================================================
# SECTION 17: Write the four machine-readable files
# ===========================================================================

def write_all_data_files() -> None:
    L.write_ledger(os.path.join(LAB_DIR, "ledger.jsonl"), ledger)
    L.write_documents(os.path.join(LAB_DIR, "documents.jsonl"), documents)
    L.write_statements(os.path.join(LAB_DIR, "statements.jsonl"), statements)
    L.write_opening_position(os.path.join(LAB_DIR, "opening_position.json"), opening_position)
    print(f"[generate.py] wrote ledger.jsonl ({len(ledger)}), documents.jsonl ({len(documents)}), "
          f"statements.jsonl ({len(statements)}), opening_position.json", file=sys.stderr)


write_all_data_files()


# ===========================================================================
# SECTION 18: Rendering -- every shipped document, built from the data above
# ===========================================================================

import shutil  # noqa: E402
import tempfile  # noqa: E402
import zlib  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def stable_seed(s: str) -> int:
    """A seed derived from a doc_id that is stable across processes/runs --
    Python's built-in hash() of a str is salted per-process (PYTHONHASHSEED),
    so abs(hash(doc_id)) is NOT reproducible run to run even though every
    data file is. zlib.crc32 has no such salt."""
    return zlib.crc32(s.encode("utf-8")) % (2**31)

SCAN_DPI = 150
SCAN_QUALITY = 60  # tuned to ~250KB/page; verified tesseract --psm 6 legible (see generation notes)

CSS_TEXT = """
@page { size: letter; margin: 0.6in; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; color: #1a1a1a; }
h1 { font-size: 16pt; margin-bottom: 0; }
h2 { font-size: 13pt; margin-top: 1.2em; }
table { border-collapse: collapse; width: 100%; margin-top: 0.6em; }
td, th { border-bottom: 1px solid #ccc; padding: 4px 6px; text-align: left; font-size: 10pt; }
th { border-bottom: 2px solid #333; }
.right { text-align: right; }
.hdr { display: flex; justify-content: space-between; }
.small { font-size: 9pt; color: #444; }
.total-row td { border-top: 2px solid #333; font-weight: bold; }
"""

FONT_PATH = "DejaVuSans-Bold.ttf"
FONT_REG_PATH = "DejaVuSans.ttf"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def make_flat_receipt_image(vendor: str, date_str: str, amount_cents: int, out_png: str, seed: int) -> None:
    img = Image.new("RGB", (500, 650), (252, 250, 244))
    draw = ImageDraw.Draw(img)
    f_big = _font(FONT_PATH, 22)
    f_reg = _font(FONT_REG_PATH, 16)
    y = 30
    draw.text((30, y), vendor[:28], font=f_big, fill=(10, 10, 10)); y += 40
    draw.text((30, y), "Long Island City, NY", font=f_reg, fill=(40, 40, 40)); y += 30
    draw.text((30, y), f"Date: {date_str}", font=f_reg, fill=(40, 40, 40)); y += 40
    draw.line((30, y, 470, y), fill=(120, 120, 120), width=2); y += 20
    draw.text((30, y), "Merchandise", font=f_reg, fill=(20, 20, 20)); y += 30
    draw.text((30, y), f"Total:  {fmt_money(amount_cents)}", font=f_big, fill=(10, 10, 10)); y += 40
    draw.text((30, y), "Card ****" + BANK_ACCT_LAST4, font=f_reg, fill=(60, 60, 60))
    img.save(out_png)


def render_receipt(doc: dict, seed: int) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        flat = os.path.join(tmp, "flat.png")
        make_flat_receipt_image(doc["counterparty"], doc["issued_date"], doc["amount"] or 0, flat, seed)
        R.photograph_receipt(flat, os.path.join(REPO_ROOT, doc["path"]), seed=seed)


def render_handwritten_receipt(doc: dict, seed: int) -> None:
    lines = [
        "Cash Received",
        f"{doc['issued_date']}",
        "Scrap bin swap - shop",
        f"Amt {fmt_money(doc['amount'] or 0)}",
        "-P.V.",
    ]
    R.handwritten_note_image(lines, os.path.join(REPO_ROOT, doc["path"]), seed=seed)


def simple_letterhead(title: str) -> str:
    return f"""
    <div class="hdr">
      <div>
        <h1>{COMPANY_NAME}</h1>
        <div class="small">{COMPANY_ADDR}<br/>EIN {COMPANY_EIN} &middot; {COMPANY_PHONE}</div>
      </div>
      <div class="small" style="text-align:right;"><h2 style="margin-top:0">{title}</h2></div>
    </div>
    """


def render_invoice(doc: dict) -> None:
    inv_no = doc["path"].rsplit("Invoice_", 1)[-1].split(".pdf")[0]
    html = f"""<html><body>
    {simple_letterhead(f"Invoice #{inv_no}")}
    <p><b>Bill To:</b> {doc['counterparty']}</p>
    <p>Invoice Date: {doc['issued_date']}<br/>Terms: Net 30</p>
    <table>
      <tr><th>Description</th><th class="right">Amount</th></tr>
      <tr><td>Architectural metal fabrication and installation - per project scope</td>
          <td class="right">{fmt_money(doc['amount'])}</td></tr>
      <tr class="total-row"><td>Total Due</td><td class="right">{fmt_money(doc['amount'])}</td></tr>
    </table>
    <p class="small" style="margin-top:2em;">Please remit payment to {COMPANY_NAME}, {COMPANY_ADDR}.</p>
    </body></html>"""
    R.render_html_to_pdf(html, os.path.join(REPO_ROOT, doc["path"]), css=CSS_TEXT)


def render_bill_html(vendor: str, bill_no, issued_date_str: str, amount: int) -> str:
    return f"""<html><body>
    <div class="hdr">
      <div><h1>{vendor}</h1></div>
      <div class="small" style="text-align:right;"><h2 style="margin-top:0">Invoice</h2></div>
    </div>
    <p><b>Bill To:</b> {COMPANY_NAME}<br/>{COMPANY_ADDR}</p>
    <p>Invoice #: {bill_no}<br/>Date: {issued_date_str}</p>
    <table>
      <tr><th>Description</th><th class="right">Amount</th></tr>
      <tr><td>Materials / services supplied</td><td class="right">{fmt_money(amount)}</td></tr>
      <tr class="total-row"><td>Total</td><td class="right">{fmt_money(amount)}</td></tr>
    </table>
    </body></html>"""


def render_bill(doc: dict, bill_no) -> None:
    html = render_bill_html(doc["counterparty"], bill_no, doc["issued_date"], doc["amount"])
    out_path = os.path.join(REPO_ROOT, doc["path"])
    if doc["scanned"]:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_pdf = os.path.join(tmp, "flat.pdf")
            R.render_html_to_pdf(html, tmp_pdf, css=CSS_TEXT)
            R.scanify(tmp_pdf, out_path, seed=stable_seed(doc["doc_id"]), dpi=SCAN_DPI, jpeg_quality=SCAN_QUALITY)
    else:
        R.render_html_to_pdf(html, out_path, css=CSS_TEXT)


def bank_statement_html(ym: str, stmt: dict, lines_subset: list[dict], continued: bool, is_final_chunk: bool,
                         issued_date_str: str = "") -> str:
    rows = "".join(
        f"<tr><td>{ln['date']}</td><td>{ln['description']}</td>"
        f"<td class='right'>{'+' if ln['direction']=='in' else '-'}{fmt_money(ln['amount'])}</td></tr>"
        for ln in lines_subset
    )
    header_note = " (continued)" if continued else ""
    footer = ""
    if is_final_chunk:
        footer = f"""
        <table>
          <tr><td>Opening Balance</td><td class="right">{fmt_money(stmt['opening_balance'])}</td></tr>
          <tr class="total-row"><td>Closing Balance</td><td class="right">{fmt_money(stmt['closing_balance'])}</td></tr>
        </table>"""
    return f"""<html><body>
    <div class="hdr">
      <div><h1>{BANK_NAME}</h1><div class="small">{BANK_ADDR}</div></div>
      <div class="small" style="text-align:right;">
        <h2 style="margin-top:0">Business Checking Statement{header_note}</h2>
        Account ****{BANK_ACCT_LAST4}<br/>
        {stmt['stmt_period_start']} to {stmt['stmt_period_end']}<br/>
        Statement Date: {issued_date_str}
      </div>
    </div>
    <p>{COMPANY_NAME}<br/>{COMPANY_ADDR}</p>
    <table>
      <tr><th>Date</th><th>Description</th><th class="right">Amount</th></tr>
      {rows}
    </table>
    {footer}
    </body></html>"""


def render_bank_statement(ym: str) -> None:
    stmt = next(s for s in statements if s["account_code"] == "1000" and s["stmt_period_start"] == f"{ym}-01")
    filenames = BANK_STMT_FILENAMES[ym]
    doc_ids = BANK_STMT_DOC_IDS[ym]
    all_lines = stmt["lines"]
    if len(filenames) == 1:
        issued_date_str = next(d["issued_date"] for d in documents if d["doc_id"] == doc_ids[0])
        html = bank_statement_html(ym, stmt, all_lines, continued=False, is_final_chunk=True,
                                    issued_date_str=issued_date_str)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_pdf = os.path.join(tmp, "flat.pdf")
            R.render_html_to_pdf(html, tmp_pdf, css=CSS_TEXT)
            out_path = os.path.join(REPO_ROOT, next(d["path"] for d in documents if d["doc_id"] == doc_ids[0]))
            R.scanify(tmp_pdf, out_path, seed=stable_seed(doc_ids[0]), dpi=SCAN_DPI, jpeg_quality=SCAN_QUALITY)
    else:
        mid = (len(all_lines) + 1) // 2
        chunks = [all_lines[:mid], all_lines[mid:]]
        for i, (fn, did, chunk) in enumerate(zip(filenames, doc_ids, chunks)):
            issued_date_str = next(d["issued_date"] for d in documents if d["doc_id"] == did)
            html = bank_statement_html(ym, stmt, chunk, continued=(i > 0), is_final_chunk=(i == len(filenames) - 1),
                                        issued_date_str=issued_date_str)
            with tempfile.TemporaryDirectory() as tmp:
                tmp_pdf = os.path.join(tmp, "flat.pdf")
                R.render_html_to_pdf(html, tmp_pdf, css=CSS_TEXT)
                out_path = os.path.join(REPO_ROOT, next(d["path"] for d in documents if d["doc_id"] == did))
                R.scanify(tmp_pdf, out_path, seed=stable_seed(did), dpi=SCAN_DPI, jpeg_quality=SCAN_QUALITY)


def render_cc_statement(ym: str) -> None:
    stmt = next(s for s in statements if s["account_code"] == "2300" and s["stmt_period_start"] == f"{ym}-01")
    doc_id = cc_doc_id(ym)
    cc_doc = next(d for d in documents if d["doc_id"] == doc_id)
    out_path = os.path.join(REPO_ROOT, cc_doc["path"])
    rows = "".join(
        f"<tr><td>{ln['date']}</td><td>{ln['description']}</td>"
        f"<td class='right'>{'+' if ln['direction']=='in' else '-'}{fmt_money(ln['amount'])}</td></tr>"
        for ln in stmt["lines"]
    )
    html = f"""<html><body>
    <div class="hdr">
      <div><h1>{BANK_NAME}</h1><div class="small">{BANK_ADDR}</div></div>
      <div class="small" style="text-align:right;">
        <h2 style="margin-top:0">Business Visa Statement</h2>
        Card ****{CC_LAST4}<br/>
        {stmt['stmt_period_start']} to {stmt['stmt_period_end']}<br/>
        Statement Date: {cc_doc['issued_date']}
      </div>
    </div>
    <p>{COMPANY_NAME}<br/>{COMPANY_ADDR}</p>
    <table>
      <tr><th>Date</th><th>Description</th><th class="right">Amount</th></tr>
      {rows}
    </table>
    <table>
      <tr><td>Previous Balance</td><td class="right">{fmt_money(stmt['opening_balance'])}</td></tr>
      <tr class="total-row"><td>New Balance</td><td class="right">{fmt_money(stmt['closing_balance'])}</td></tr>
    </table>
    <p class="small">Payment due upon receipt to keep your account in good standing.</p>
    </body></html>"""
    R.render_html_to_pdf(html, out_path, css=CSS_TEXT)


def render_bundle(ym: str, info: dict) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pdfs = []
        for i, b in enumerate(info["bills"]):
            html = render_bill_html(b["vendor"], b["bill_no"], b["issued_date_str"], b["amount"])
            p = os.path.join(tmp, f"bill{i}.pdf")
            R.render_html_to_pdf(html, p, css=CSS_TEXT)
            pdfs.append(p)
        concat_path = os.path.join(tmp, "concat.pdf")
        R.concat_pdfs(pdfs, concat_path)
        out_path = os.path.join(REPO_ROOT, info["path"] if "path" in info else materials_path(info["filename"]))
        out_path = os.path.join(REPO_ROOT, next(d["path"] for d in documents if d["doc_id"] == info["doc_id"]))
        R.scanify(concat_path, out_path, seed=stable_seed(info["doc_id"]), dpi=SCAN_DPI, jpeg_quality=SCAN_QUALITY)


def _annual_bundle_bill_html(vendor: str, month_label: str, issued_date_str: str,
                              amount_cents: int, detail_line: str) -> str:
    return f"""<html><body>
    <div class="hdr">
      <div><h1>{vendor}</h1></div>
      <div class="small" style="text-align:right;"><h2 style="margin-top:0">Statement / Invoice</h2></div>
    </div>
    <p><b>Bill To:</b> {COMPANY_NAME}<br/>{COMPANY_ADDR}</p>
    <p>Billing Period: {month_label} 2025<br/>Date: {issued_date_str}</p>
    <table>
      <tr><th>Description</th><th class="right">Amount</th></tr>
      <tr><td>{detail_line}</td><td class="right">{fmt_money(amount_cents)}</td></tr>
      <tr class="total-row"><td>Amount Due</td><td class="right">{fmt_money(amount_cents)}</td></tr>
    </table>
    </body></html>"""


def render_annual_bundle(doc_id: str, monthly_amounts: list[int], vendor: str, detail_fn) -> None:
    """Twelve monthly bills from one vendor, concatenated into one shipped
    PDF -- keeps the file count down while giving each varied monthly
    amount (Utilities / Telephone / Professional Fees) its own document to
    trace to, beyond the bank statement line."""
    doc = next(d for d in documents if d["doc_id"] == doc_id)
    with tempfile.TemporaryDirectory() as tmp:
        pdfs = []
        for mi, ym in enumerate(MONTHS):
            amt = monthly_amounts[mi]
            date_str = format_defect6(f"{ym}-{min(27, month_days(ym)):02d}", mi)
            detail = detail_fn(mi, amt)
            html = _annual_bundle_bill_html(vendor, MONTH_NAMES[mi], date_str, amt, detail)
            p = os.path.join(tmp, f"b{mi}.pdf")
            R.render_html_to_pdf(html, p, css=CSS_TEXT)
            pdfs.append(p)
        concat_path = os.path.join(tmp, "concat.pdf")
        R.concat_pdfs(pdfs, concat_path)
        shutil.copyfile(concat_path, os.path.join(REPO_ROOT, doc["path"]))


def render_payroll_summary(doc: dict, ym: str, mi: int) -> None:
    rows = "".join(
        f"<tr><td>{name}</td><td>{title}</td><td class='right'>{fmt_money(employee_monthly[name][mi])}</td></tr>"
        for name, title, _ in EMPLOYEES
    )
    gross = sum(employee_monthly[name][mi] for name, _, _ in EMPLOYEES)
    tax = round(gross * PAYROLL_TAX_RATE)
    html = f"""<html><body>
    <div class="hdr">
      <div><h1>{PAYROLL_PROVIDER}</h1><div class="small">{PAYROLL_PROVIDER_ADDR}</div></div>
      <div class="small" style="text-align:right;"><h2 style="margin-top:0">Payroll Run Summary</h2>
        Pay Period: {MONTH_NAMES[mi]} 2025<br/>
        Pay Date: {doc['issued_date']}</div>
    </div>
    <p>Client: {COMPANY_NAME}<br/>EIN {COMPANY_EIN}</p>
    <table>
      <tr><th>Employee</th><th>Role</th><th class="right">Gross Pay</th></tr>
      {rows}
    </table>
    <table>
      <tr><td>Gross Wages, this period</td><td class="right">{fmt_money(gross)}</td></tr>
      <tr><td>Employer Payroll Taxes, this period</td><td class="right">{fmt_money(tax)}</td></tr>
    </table>
    </body></html>"""
    R.render_html_to_pdf(html, os.path.join(REPO_ROOT, doc["path"]), css=CSS_TEXT)


def render_payroll_register() -> None:
    doc = next(d for d in documents if d["doc_id"] == DOC_PAYROLL_REGISTER)
    header = ["Employee", "Role", "Month", "Gross Pay (cents)"]
    rows = [header]
    for mi, ym in enumerate(MONTHS):
        for name, title, _ in EMPLOYEES:
            rows.append([name, title, MONTH_NAMES[mi] + " 2025", employee_monthly[name][mi]])
    R.render_xlsx(os.path.join(REPO_ROOT, doc["path"]), {"Payroll Register 2025": rows})


def render_loan_amortization(doc: dict, amort_rows: list[dict], lender: str, principal: int,
                              rate: float, term_months: int, asset_label: str, start_date: str,
                              first_payment_date: str | None = None) -> None:
    if first_payment_date:
        rows = "".join(
            f"<tr><td>{r['period']}</td><td>{add_months(first_payment_date, r['period'] - 1)}</td>"
            f"<td class='right'>{fmt_money(r['payment'])}</td>"
            f"<td class='right'>{fmt_money(r['interest'])}</td><td class='right'>{fmt_money(r['principal'])}</td>"
            f"<td class='right'>{fmt_money(r['balance'])}</td></tr>"
            for r in amort_rows
        )
        date_th = "<th>Due Date</th>"
    else:
        rows = "".join(
            f"<tr><td>{r['period']}</td><td class='right'>{fmt_money(r['payment'])}</td>"
            f"<td class='right'>{fmt_money(r['interest'])}</td><td class='right'>{fmt_money(r['principal'])}</td>"
            f"<td class='right'>{fmt_money(r['balance'])}</td></tr>"
            for r in amort_rows
        )
        date_th = ""
    html = f"""<html><body>
    <div class="hdr">
      <div><h1>{lender}</h1><div class="small">Amortization Schedule</div></div>
      <div class="small" style="text-align:right;">Loan origination: {start_date}<br/>
        Original principal: {fmt_money(principal)}<br/>
        Term: {term_months} months &middot; Rate: {rate*100:.2f}% APR</div>
    </div>
    <p>Borrower: {COMPANY_NAME}, {COMPANY_ADDR}<br/>Collateral: {asset_label}</p>
    <table>
      <tr><th>Pmt #</th>{date_th}<th class="right">Payment</th><th class="right">Interest</th>
          <th class="right">Principal</th><th class="right">Remaining Balance</th></tr>
      {rows}
    </table>
    </body></html>"""
    R.render_html_to_pdf(html, os.path.join(REPO_ROOT, doc["path"]), css=CSS_TEXT)


def render_opening_letter() -> None:
    doc = next(d for d in documents if d["doc_id"] == DOC_OPEN)
    ar_rows = "".join(f"<tr><td>{d}</td><td class='right'>{fmt_money(a)}</td></tr>" for d, a in OPEN_AR)
    ap_rows = "".join(f"<tr><td>{c}</td><td class='right'>{fmt_money(a)}</td></tr>" for c, a in OPEN_AP)
    html = f"""<html><body>
    <div class="hdr">
      <div><h1>{PRIOR_CPA}</h1><div class="small">{PRIOR_CPA_ADDR}</div></div>
      <div class="small" style="text-align:right;">January 14, 2025</div>
    </div>
    <p>{OFFICER}<br/>{OFFICER_TITLE}, {COMPANY_NAME}<br/>{COMPANY_ADDR}</p>
    <p>Dear Mr. {OFFICER.split()[-1]},</p>
    <p>As you transition your accounting records to new representation, we are pleased to
    summarize {COMPANY_NAME}'s closing financial position as of December 31, 2024, the final
    day of our engagement, for the incoming preparer's reference.</p>
    <p>Cash held in the company's operating account with {BANK_NAME} (account ending
    {BANK_ACCT_LAST4}) stood at {fmt_money(OPEN_CASH)} as of the close of business on
    December 31, 2024.</p>
    <p>Accounts receivable outstanding at year end totaled {fmt_money(sum(a for _, a in OPEN_AR))},
    comprising the following customer balances:</p>
    <table><tr><th>Customer</th><th class="right">Amount</th></tr>{ar_rows}</table>
    <p>Accounts payable outstanding at year end totaled {fmt_money(sum(a for _, a in OPEN_AP))},
    comprising the following vendor balances:</p>
    <table><tr><th>Vendor</th><th class="right">Amount</th></tr>{ap_rows}</table>
    <p>Fixed assets consisted of fabrication equipment recorded at a cost of
    {fmt_money(OPEN_EQUIPMENT_COST)} and a work vehicle recorded at a cost of
    {fmt_money(OPEN_VEHICLE_COST)}, against which accumulated depreciation of
    {fmt_money(OPEN_ACCUM_DEP)} had been recorded through December 31, 2024.</p>
    <p><b>Depreciation policy:</b> {DEPRECIATION_POLICY_TEXT}</p>
    <p>The business credit card carried a balance of {fmt_money(OPEN_CC_BALANCE)}. The company's
    vehicle loan with {BANK_NAME}, originally financed in {_vehicle_loan_origination_prose} for the
    purchase of the company's flatbed work truck, carried a remaining balance of
    {fmt_money(OPEN_VEHICLE_LOAN)} as of December 31, 2024, with the final twelve monthly payments
    due to retire the loan in full by the end of 2025.</p>
    <p>Shareholders' equity at year end was composed of common stock of {fmt_money(OPEN_COMMON_STOCK)},
    additional paid-in capital of {fmt_money(OPEN_APIC)}, and retained earnings of
    {fmt_money(OPEN_RETAINED_EARNINGS)}, reflecting the company's statement of financial
    position as at that date.</p>
    <p>Please do not hesitate to contact us with any questions during the transition.</p>
    <p>Sincerely,<br/>{PRIOR_CPA_PARTNER}<br/>{PRIOR_CPA}</p>
    </body></html>"""
    R.render_html_to_pdf(html, os.path.join(REPO_ROOT, doc["path"]), css=CSS_TEXT)


def make_flat_press_brake_image(out_png: str) -> None:
    img = Image.new("RGB", (1700, 1300), (250, 250, 248))
    draw = ImageDraw.Draw(img)
    f_big = _font(FONT_PATH, 48)
    f_reg = _font(FONT_REG_PATH, 34)
    y = 50
    draw.text((50, y), EQUIP_VENDOR, font=f_big, fill=(10, 10, 10)); y += 66
    draw.text((50, y), EQUIP_VENDOR_ADDR, font=f_reg, fill=(50, 50, 50)); y += 70
    draw.text((50, y), "INVOICE", font=f_big, fill=(10, 10, 10)); y += 74
    draw.text((50, y), f"Invoice Date: {PRESS_BRAKE_INVOICE_DATE}", font=f_reg, fill=(30, 30, 30)); y += 50
    draw.text((50, y), f"Sold To: {COMPANY_NAME}", font=f_reg, fill=(30, 30, 30)); y += 46
    draw.text((50, y), COMPANY_ADDR, font=f_reg, fill=(30, 30, 30)); y += 70
    draw.line((50, y, 1650, y), fill=(120, 120, 120), width=3); y += 36
    draw.text((50, y), "Model CMB-175 CNC Press Brake, 175-ton, 12ft bed", font=f_reg, fill=(20, 20, 20)); y += 54
    draw.text((50, y), f"Cost: {fmt_money(PRESS_BRAKE_COST)}", font=f_big, fill=(10, 10, 10)); y += 74
    draw.text((50, y), f"Delivered and installed: {PRESS_BRAKE_INVOICE_DATE}", font=f_reg, fill=(30, 30, 30)); y += 50
    draw.text((50, y), f"Placed in service: {PRESS_BRAKE_IN_SERVICE_DATE}", font=f_reg, fill=(30, 30, 30)); y += 50
    draw.text((50, y), "Terms: $10,000.00 due on delivery, balance financed", font=f_reg, fill=(30, 30, 30))
    img.save(out_png)


def render_press_brake_invoice() -> None:
    doc = next(d for d in documents if d["doc_id"] == DOC_PRESS_BRAKE_INVOICE)
    with tempfile.TemporaryDirectory() as tmp:
        flat = os.path.join(tmp, "flat.png")
        make_flat_press_brake_image(flat)
        R.photograph_receipt(flat, os.path.join(REPO_ROOT, doc["path"]), seed=55021)


def render_duplicate_receipts() -> None:
    doc_jpg = next(d for d in documents if d["doc_id"] == dup_doc_jpg)
    doc_pdf = next(d for d in documents if d["doc_id"] == dup_doc_pdf)
    with tempfile.TemporaryDirectory() as tmp:
        flat = os.path.join(tmp, "flat.png")
        make_flat_receipt_image(DUP_VENDOR, doc_jpg["issued_date"], DUP_AMOUNT, flat, seed=8801)
        R.photograph_receipt(flat, os.path.join(REPO_ROOT, doc_jpg["path"]), seed=8801)
        # Same purchase, scanned separately as if emailed/scanned into the shoebox again.
        flat_pdf_src = os.path.join(tmp, "flat_for_scan.pdf")
        html = render_bill_html(DUP_VENDOR, "N/A", doc_pdf["issued_date"], DUP_AMOUNT)
        R.render_html_to_pdf(html, flat_pdf_src, css=CSS_TEXT)
        R.scanify(flat_pdf_src, os.path.join(REPO_ROOT, doc_pdf["path"]), seed=8802, dpi=SCAN_DPI, jpeg_quality=SCAN_QUALITY)


def render_all() -> None:
    render_opening_letter()
    render_loan_amortization(
        next(d for d in documents if d["doc_id"] == DOC_VEHICLE_AMORT), vehicle_amort_full,
        BANK_NAME, VEHICLE_LOAN_ORIGINAL_PRINCIPAL, VEHICLE_LOAN_RATE, VEHICLE_LOAN_TERM_MONTHS,
        "2022 one-ton flatbed work truck (VIN ending 4417)", VEHICLE_LOAN_ORIGINATION_DATE,
        first_payment_date=VEHICLE_LOAN_FIRST_PAYMENT_DATE,
    )
    render_loan_amortization(
        next(d for d in documents if d["doc_id"] == DOC_EQUIP_AMORT), equip_amort,
        EQUIP_LENDER, EQUIP_LOAN_PRINCIPAL, EQUIP_LOAN_RATE, EQUIP_LOAN_TERM_MONTHS,
        "Model CMB-175 CNC Press Brake (serial CMB175-2025-0442)", "2025-04-15",
        first_payment_date="2025-05-15",
    )
    render_press_brake_invoice()
    render_payroll_register()
    render_duplicate_receipts()

    for doc in documents:
        did = doc["doc_id"]
        if did in (DOC_OPEN, DOC_VEHICLE_AMORT, DOC_EQUIP_AMORT, DOC_PRESS_BRAKE_INVOICE,
                   DOC_PAYROLL_REGISTER, dup_doc_jpg, dup_doc_pdf, doc_handwritten):
            continue
        if doc["kind"] == "invoice_out":
            render_invoice(doc)
        elif doc["kind"] == "bill_in":
            render_bill(doc, did.split("-")[-1])
        elif doc["kind"] == "receipt":
            seed = stable_seed(did)
            render_receipt(doc, seed)

    render_handwritten_receipt(next(d for d in documents if d["doc_id"] == doc_handwritten), seed=9911)

    for mi, ym in enumerate(MONTHS):
        render_bank_statement(ym)
        render_cc_statement(ym)
        render_payroll_summary(next(d for d in documents if d["doc_id"] == payroll_summary_docs[ym]), ym, mi)

    for ym, info in bundles.items():
        render_bundle(ym, info)

    render_annual_bundle(
        DOC_UTILITY_BUNDLE, UTILITIES_MONTHLY, UTILITIES_VENDOR,
        lambda mi, amt: f"Electricity + gas service, {round(amt / UTILITY_RATE_PER_KWH_CENTS):,} kWh "
                        f"@ ${UTILITY_RATE_PER_KWH_CENTS / 100:.3f}/kWh",
    )
    render_annual_bundle(
        DOC_TELEPHONE_BUNDLE, TELEPHONE_MONTHLY, TELEPHONE_VENDOR,
        lambda mi, amt: "Business phone & internet service" + (" (includes data overage)" if amt > 280_00 else " (base plan)"),
    )
    render_annual_bundle(
        DOC_PROFFEE_BUNDLE, PROFESSIONAL_FEES_MONTHLY, PROFESSIONAL_FEES_VENDOR,
        lambda mi, amt: PROFESSIONAL_FEES_DESCRIPTIONS[mi],
    )

    print(f"[generate.py] rendering complete: {len(documents)} documents", file=sys.stderr)


if not SKIP_RENDER:
    render_all()
else:
    print("[generate.py] SKIP_RENDER=1 -- data files written, no documents rendered", file=sys.stderr)


# ===========================================================================
# SECTION 19: answer-key.md -- lab/ only, never shipped, never scanned by
# check_8, so real accounting terms are used freely here.
# ===========================================================================

def build_answer_key() -> str:
    tb = L.trial_balance(ledger, as_of=PERIOD_END)

    def bal(code):
        return tb.get(code, 0)

    assets = {
        "1000": ("Cash - Operating", bal("1000")),
        "1200": ("Accounts Receivable", bal("1200")),
        "1500": ("Fixed Assets - Equipment", bal("1500")),
        "1510": ("Fixed Assets - Vehicles", bal("1510")),
        "1590": ("Accumulated Depreciation", -bal("1590")),
    }
    liabilities = {
        "2000": ("Accounts Payable", bal("2000")),
        "2300": ("Credit Card Payable", bal("2300")),
        "2400": ("Loan Payable - Current Portion", bal("2400")),
        "2410": ("Loan Payable - Long-Term Portion", bal("2410")),
    }
    equity_bs = {
        "3200": ("Common Stock", bal("3200")),
        "3210": ("Additional Paid-In Capital", bal("3210")),
        "3220": ("Retained Earnings (opening)", bal("3220")),
        "3230": ("Shareholder Distributions", -bal("3230")),
    }
    income = {
        "4000": ("Sales Revenue", bal("4000")),
    }
    expenses = {
        "5000": ("Cost of Goods Sold", bal("5000")),
        "6000": ("Rent Expense", bal("6000")),
        "6010": ("Utilities Expense", bal("6010")),
        "6020": ("Wages Expense", bal("6020")),
        "6030": ("Payroll Tax Expense", bal("6030")),
        "6040": ("Subcontractor Expense", bal("6040")),
        "6050": ("Office Supplies Expense", bal("6050")),
        "6060": ("Insurance Expense", bal("6060")),
        "6070": ("Professional Fees Expense", bal("6070")),
        "6080": ("Bank Fees Expense", bal("6080")),
        "6090": ("Interest Expense", bal("6090")),
        "6100": ("Depreciation Expense", bal("6100")),
        "6110": ("Vehicle Expense", bal("6110")),
        "6130": ("Advertising & Marketing Expense", bal("6130")),
        "6140": ("Repairs & Maintenance Expense", bal("6140")),
        "6150": ("Telephone & Internet Expense", bal("6150")),
        "6900": ("Miscellaneous Expense", bal("6900")),
    }

    total_revenue = sum(v for _, v in income.values())
    total_cogs = bal("5000")
    gross_profit = total_revenue - total_cogs
    total_opex = sum(v for k, (_, v) in expenses.items() if k != "5000")
    net_income = gross_profit - total_opex

    total_assets = sum(v for _, v in assets.values())
    total_liabilities = sum(v for _, v in liabilities.values())
    total_equity_accounts = sum(v for _, v in equity_bs.values())
    retained_earnings_closing = bal("3220") + net_income - bal("3230")
    total_equity_closing = bal("3200") + bal("3210") + retained_earnings_closing

    lines = []
    a = lines.append

    a(f"# Answer Key -- {COMPANY_NAME} ({SLUG})\n")
    a(f"Period: {PERIOD_START} to {PERIOD_END}. Opening position as of {OPENING_AS_OF}. "
      f"Seed: {SEED} (fully deterministic; re-running `generate.py` reproduces this corpus exactly).\n")

    a("## 1. Profit & Loss, year ended December 31, 2025\n")
    a("| Line | Amount |\n|---|---:|")
    a(f"| Sales Revenue | {fmt_money(total_revenue)} |")
    a(f"| Cost of Goods Sold | ({fmt_money(total_cogs)}) |")
    a(f"| **Gross Profit** | **{fmt_money(gross_profit)}** |")
    for code in ["6000", "6010", "6020", "6030", "6040", "6050", "6060", "6070",
                 "6080", "6090", "6100", "6110", "6130", "6140", "6150", "6900"]:
        name, v = expenses[code]
        a(f"| {name} | ({fmt_money(v)}) |")
    a(f"| **Total Operating Expenses** | **({fmt_money(total_opex)})** |")
    a(f"| **Net Income** | **{fmt_money(net_income)}** |")
    a("")

    a("## 2. Balance Sheet, as of December 31, 2025\n")
    a("**Assets**\n")
    a("| Account | Amount |\n|---|---:|")
    for code in ["1000", "1200", "1500", "1510"]:
        name, v = assets[code]
        a(f"| {name} | {fmt_money(v)} |")
    a(f"| Accumulated Depreciation | ({fmt_money(-assets['1590'][1])}) |")
    a(f"| **Total Assets** | **{fmt_money(total_assets)}** |")
    a("\n**Liabilities**\n")
    a("| Account | Amount |\n|---|---:|")
    for code in ["2000", "2300", "2400", "2410"]:
        name, v = liabilities[code]
        a(f"| {name} | {fmt_money(v)} |")
    a(f"| **Total Liabilities** | **{fmt_money(total_liabilities)}** |")
    a("\n**Equity**\n")
    a("| Account | Amount |\n|---|---:|")
    a(f"| Common Stock | {fmt_money(bal('3200'))} |")
    a(f"| Additional Paid-In Capital | {fmt_money(bal('3210'))} |")
    a(f"| Retained Earnings (opening {fmt_money(bal('3220'))} + net income {fmt_money(net_income)} "
      f"- distributions {fmt_money(bal('3230'))}) | {fmt_money(retained_earnings_closing)} |")
    a(f"| **Total Equity** | **{fmt_money(total_equity_closing)}** |")
    a(f"\n**Total Liabilities + Equity: {fmt_money(total_liabilities + total_equity_closing)}** "
      f"(ties to Total Assets {fmt_money(total_assets)})\n")

    a("## 3. Trial Balance, as of December 31, 2025\n")
    a("| Account Code | Account Name | Debit | Credit |\n|---|---|---:|---:|")
    for code in sorted(tb.keys()):
        meta = L.CHART[code]
        v = tb[code]
        if meta["normal_side"] == "debit":
            debit, credit = (v, 0) if v >= 0 else (0, -v)
        else:
            debit, credit = (0, v) if v >= 0 else (-v, 0)
        a(f"| {code} | {meta['name']} | {fmt_money(debit) if debit else ''} | {fmt_money(credit) if credit else ''} |")
    total_debits = sum(max(tb[c], 0) if L.CHART[c]["normal_side"] == "debit" else max(-tb[c], 0) for c in tb)
    total_credits = sum(max(tb[c], 0) if L.CHART[c]["normal_side"] == "credit" else max(-tb[c], 0) for c in tb)
    a(f"| | **Total** | **{fmt_money(total_debits)}** | **{fmt_money(total_credits)}** |\n")

    a("## 4. Depreciation policy and application\n")
    a(f"{DEPRECIATION_POLICY_TEXT}\n")
    a(f"- Existing fabrication equipment (cost {fmt_money(OPEN_EQUIPMENT_COST)}, in service before the "
      f"opening date): {fmt_money(EXISTING_EQUIP_MONTHLY_DEP)}/month, all 12 months of 2025 = "
      f"{fmt_money(EXISTING_EQUIP_MONTHLY_DEP*12)}.")
    a(f"- Existing work vehicle (cost {fmt_money(OPEN_VEHICLE_COST)}): {fmt_money(EXISTING_VEHICLE_MONTHLY_DEP)}/month, "
      f"all 12 months = {fmt_money(EXISTING_VEHICLE_MONTHLY_DEP*12)}.")
    a(f"- Press brake (cost {fmt_money(PRESS_BRAKE_COST)}, placed in service {PRESS_BRAKE_IN_SERVICE_DATE}, "
      f"depreciation begins the following month per policy): {fmt_money(PRESS_BRAKE_MONTHLY_DEP)}/month, "
      f"May-Dec 2025 (8 months) = {fmt_money(PRESS_BRAKE_MONTHLY_DEP*8)}.")
    a(f"- Total 2025 depreciation expense: {fmt_money(TOTAL_DEPRECIATION_2025)}. Opening accumulated depreciation "
      f"{fmt_money(OPEN_ACCUM_DEP)} + 2025 depreciation {fmt_money(TOTAL_DEPRECIATION_2025)} = closing accumulated "
      f"depreciation {fmt_money(CLOSING_ACCUM_DEP)}, agreeing with the balance sheet above.\n")

    a("## 5. Opening AR/AP settlement (Rule Two)\n")
    a("The opening letter's accounts receivable and accounts payable are prior-period balances. Their "
      "in-period cash settlement is recorded as a pure balance-sheet movement (debit/credit Cash against "
      "the AR or AP balance carried over from the opening entry) and never touches Sales Revenue or an "
      "expense account, so it does not distort 2025's P&L:")
    for debtor, amt in OPEN_AR:
        a(f"- AR: {debtor}, {fmt_money(amt)}, settled via bank deposit within Q1 2025 (see ledger entries "
          f"citing the opening letter's AR line for {debtor}).")
    for creditor, amt in OPEN_AP:
        a(f"- AP: {creditor}, {fmt_money(amt)}, settled via bank payment within January 2025.")
    a("")

    a("## 6. Mandated defects\n")
    a(f"**1. Duplicate receipt.** {DUP_VENDOR}, {fmt_money(DUP_AMOUNT)}, dated {DUP_DATE}, shipped twice: "
      f"once as `receipt_001.jpeg` (photographed JPG) and once as `{DUP_PDF_FILENAME}` (scanned PDF). Both are "
      f"registered as separate documents in `documents.jsonl`, but the ledger records the purchase exactly "
      f"once (a single entry citing both doc_ids). Correct treatment: recognize this as one transaction; "
      f"an ingestion process that treats each shipped file as an independent transaction will double-count "
      f"{fmt_money(DUP_AMOUNT)} of Office Supplies Expense.\n")
    a(f"**2. Personal expense on a business account.** {PERSONAL_EXPENSE_VENDOR} flight charge, "
      f"{fmt_money(PERSONAL_EXPENSE_AMOUNT)}, dated {PERSONAL_EXPENSE_DATE}, appears on the business credit "
      f"card statement for August 2025. Correct treatment: debit Shareholder Distributions (3230), not any "
      f"expense account -- it is family travel, not a business cost. See the credit card statement for "
      f"August 2025 and the corresponding ledger entry's memo.\n")
    a("**3. N/A for Bright Harbor** (Ferrone's inter-account transfer defect).\n")
    a(f"**4. Unpaid AR/AP at period end.** {len(unpaid_ar_invoices)} sales invoices remain unpaid at "
      f"December 31, 2025 (Accounts Receivable):")
    for inv_no, customer, amount, issue_date in unpaid_ar_invoices:
        a(f"   - Invoice #{inv_no}, {customer}, {fmt_money(amount)}, issued {issue_date}")
    a(f"   {len(unpaid_ap_bills)} vendor bills remain unpaid at December 31, 2025 (Accounts Payable):")
    for bill_no, vendor, amount, issue_date in unpaid_ap_bills:
        a(f"   - Bill #{bill_no}, {vendor}, {fmt_money(amount)}, issued {issue_date}")
    a("   Correct treatment: these remain on the balance sheet as Accounts Receivable / Accounts Payable "
      "at period end; do not treat them as bad debt, income, or a paid expense.\n")
    a("**5. N/A for Bright Harbor** (Ferrone's cancelled invoice / credit note defect).\n")
    a("**6. Inconsistent date formats.** `documents.jsonl`'s `issued_date` (and the rendered documents "
      "themselves) deliberately vary format across sources within Bright Harbor's corpus: sales invoices "
      "use US format (e.g. `04/10/2025`), some vendor bills and payroll summaries rotate through US, ISO "
      "(`2025-04-10`) and prose (`10 Apr 2025`) formats, while `ledger.jsonl`, `statements.jsonl` and "
      "`opening_position.json` are always ISO. This is intentional variance, not a data error.\n")
    a(f"**7. Handwritten cash receipt.** `receipt_009.jpeg`, {fmt_money(HANDWRITTEN_AMOUNT)}, dated "
      f"{HANDWRITTEN_DATE}, a petty-cash purchase (shop rags) photographed at an angle with an informal "
      f"handwritten-look note. Correct treatment: Miscellaneous Expense, evidenced by this single receipt "
      f"despite its informal appearance.\n")
    a(f"**8. Credit card statements for the full year.** Twelve monthly statements for the "
      f"{BANK_NAME} Business Visa (account ****{CC_LAST4}) are shipped, one per month, kind "
      f"`credit_card_statement`. The card carries its own liability balance (account 2300, opening "
      f"{fmt_money(OPEN_CC_BALANCE)}, closing {fmt_money(CC_BALANCE_YEAREND)}) and is paid down monthly "
      f"from the operating account the following month (see the `CC payment` lines on the 1000 account "
      f"statements). Purchases increase the 2300 balance; payments decrease it; neither touches Sales "
      f"Revenue or an unrelated expense.\n")
    a(f"**9. Loan -- interest/principal split.** Two loans: the pre-existing vehicle loan (opening balance "
      f"{fmt_money(OPEN_VEHICLE_LOAN)}, fully retired by December 2025, {fmt_money(VEHICLE_LOAN_TOTAL_INTEREST)} "
      f"total interest) and the new Empire Machinery Capital equipment term loan drawn "
      f"{EQUIP_LOAN_DRAW_DATE} for {fmt_money(EQUIP_LOAN_PRINCIPAL)} against the press brake "
      f"({fmt_money(EQUIP_LOAN_TOTAL_INTEREST_2025)} interest in 2025). Each monthly bank payment is split "
      f"across three ledger lines: Interest Expense (6090), a reduction of the loan payable principal "
      f"(2400/2410), and the cash outflow (1000). Both lenders' amortisation schedules "
      f"(`steinway_vehicle_loan_schedule.pdf`, `empire_machinery_loan_schedule.pdf`) are forward-looking "
      f"contract documents (not current-period derived totals) and are what makes the interest/principal "
      f"split traceable from the folder. At December 31, 2025 the equipment loan's remaining balance "
      f"{fmt_money(EQUIP_LOAN_BALANCE_YEAREND)} is reclassified between current ({fmt_money(EQUIP_LOAN_CURRENT_PORTION)}, "
      f"principal due within the next 12 months) and long-term ({fmt_money(EQUIP_LOAN_LONGTERM_PORTION)}).\n")
    a("**10. N/A for Bright Harbor** (Ferrone's CSV bank export duplicate-view defect).\n")

    a("## 7. Q2 2025 -- the quarter that means something\n")
    a(f"The press brake ({fmt_money(PRESS_BRAKE_COST)}, invoice dated {PRESS_BRAKE_INVOICE_DATE}, placed in "
      f"service {PRESS_BRAKE_IN_SERVICE_DATE}) and the equipment term loan draw ({fmt_money(EQUIP_LOAN_PRINCIPAL)}, "
      f"{EQUIP_LOAN_DRAW_DATE}) both land in Q2 2025. Fixed assets jump from {fmt_money(OPEN_EQUIPMENT_COST+OPEN_VEHICLE_COST)} "
      f"to {fmt_money(OPEN_EQUIPMENT_COST+OPEN_VEHICLE_COST+PRESS_BRAKE_COST)} gross cost; cash moves twice on "
      f"{EQUIP_LOAN_DRAW_DATE} (the {fmt_money(PRESS_BRAKE_DOWN)} down payment out of the operating account; "
      f"the {fmt_money(EQUIP_LOAN_PRINCIPAL)} loan proceeds never touch Bright Harbor's own bank account, paid "
      f"by the lender directly to the equipment vendor); and depreciation on the press brake begins the "
      f"following month, May 2025.\n")

    a("## 8. Officer salary and shareholder distributions (S-corp tell)\n")
    a(f"{OFFICER}'s salary (part of the {fmt_money(TOTAL_WAGES)} total 2025 Wages Expense across 6 employees) "
      f"runs through the {PAYROLL_PROVIDER} payroll register and monthly summaries exactly like every other "
      f"employee's -- the standard S-corp pattern of paying the working shareholder as a W-2 employee. "
      f"Separately, two shareholder distributions appear: the {fmt_money(PERSONAL_EXPENSE_AMOUNT)} personal "
      f"credit card charge (defect 2, above) and a {fmt_money(DISTRIBUTION_AMOUNT)} bank withdrawal on "
      f"{DISTRIBUTION_DATE} (late in the year), both posted to Shareholder Distributions (3230), never to "
      f"Wages Expense or any P&L account.\n")

    a("## 9. Headline figures\n")
    a(f"- Revenue: {fmt_money(total_revenue)}")
    a(f"- Net income: {fmt_money(net_income)}")
    a(f"- Total assets (12/31/2025): {fmt_money(total_assets)}")
    a(f"- Closing cash (Cash - Operating, 12/31/2025): {fmt_money(bal('1000'))}")
    a("")

    a("## 10. Remediation notes (this pass)\n")
    a("Four review-found defects were corrected by editing `generate.py` and regenerating the "
      "entire corpus from scratch (nothing was hand-edited into a rendered document or the ledger):\n")
    a(f"**Vehicle loan origination contradiction (fixed).** The loan now genuinely predates the "
      f"period: originated {VEHICLE_LOAN_ORIGINATION_DATE} for {fmt_money(VEHICLE_LOAN_ORIGINAL_PRINCIPAL)} "
      f"original principal, {VEHICLE_LOAN_TERM_MONTHS}-month term at {VEHICLE_LOAN_RATE*100:.1f}% APR, "
      f"first payment {VEHICLE_LOAN_FIRST_PAYMENT_DATE}. `steinway_vehicle_loan_schedule.pdf` now shows "
      f"the full {VEHICLE_LOAN_TERM_MONTHS}-row schedule from origination with a calendar due-date column; "
      f"row {VEHICLE_LOAN_TERM_MONTHS - 12} (December 2024) closes at {fmt_money(OPEN_VEHICLE_LOAN)}, which "
      f"is exactly what the opening letter now states as the loan's balance at 2024-12-31, and rows "
      f"{VEHICLE_LOAN_TERM_MONTHS - 11}-{VEHICLE_LOAN_TERM_MONTHS} (January-December 2025) are "
      f"the twelve payments posted to the ledger, fully retiring the loan by December 2025. The original "
      f"principal ({fmt_money(VEHICLE_LOAN_ORIGINAL_PRINCIPAL)}) does not exceed the vehicle's own recorded "
      f"cost ({fmt_money(OPEN_VEHICLE_COST)}). Opening accumulated depreciation "
      f"({fmt_money(OPEN_ACCUM_DEP)}) is itself now derived from the stated depreciation policy applied to "
      f"whole months in service by 2024-12-31 -- {VEHICLE_MONTHS_IN_SERVICE_AT_OPEN} months for the vehicle "
      f"(tied to the loan's own elapsed payment count) and {EQUIPMENT_MONTHS_IN_SERVICE_AT_OPEN} months for "
      f"the existing equipment -- rather than an independent constant the policy could never reproduce, so "
      f"the fix does not trade the original date contradiction for a new amount or depreciation "
      f"contradiction. Origination, "
      f"opening letter and the twelve bank payments are now internally consistent, and the interest/principal "
      f"split for 2025 is directly readable off the schedule.\n")
    a("**Flat recurring constants (fixed).** Utilities, Telephone & Internet, Vehicle Expense, Bank Fees "
      "and Professional Fees no longer repeat one flat amount for all twelve months:")
    a(f"- Utilities (Harborline Utility Co, renamed -- see below): {fmt_money(min(UTILITIES_MONTHLY))} to "
      f"{fmt_money(max(UTILITIES_MONTHLY))}/month, seasonal (winter heating, summer cooling) plus a visible "
      f"step-up from June 2025 onward once the press brake (placed in service {PRESS_BRAKE_IN_SERVICE_DATE}) "
      f"is in regular use -- H1 2025 average {fmt_money(round(sum(UTILITIES_MONTHLY[:6])/6))}/month vs H2 "
      f"average {fmt_money(round(sum(UTILITIES_MONTHLY[6:])/6))}/month. Evidenced by both the monthly bank "
      f"statement line and `utility bills 2025.pdf` (twelve monthly bills, one per vendor per year, bundled "
      f"into one shipped file), each bill showing a kWh usage figure that scales with the amount billed.")
    a(f"- Telephone & Internet (Metro Fiber Communications): {fmt_money(min(TELEPHONE_MONTHLY))} to "
      f"{fmt_money(max(TELEPHONE_MONTHLY))}/month, a steady base plan with occasional data-overage surcharges "
      f"(March, August, November 2025). Evidenced by the bank statement and `phone bills 2025.pdf`.")
    a(f"- Vehicle Expense (fuel and tolls, various stations): {fmt_money(min(VEHICLE_EXPENSE_MONTHLY))} to "
      f"{fmt_money(max(VEHICLE_EXPENSE_MONTHLY))}/month, tracking fuel-price and seasonal maintenance swings "
      f"(a November spike for winter service). Evidenced by the bank statement (no single vendor issues a "
      f"recurring bill for fuel/tolls, so no separate bundle was added here).")
    a(f"- Bank Fees ({BANK_NAME}): {fmt_money(min(BANK_FEES_MONTHLY))} to {fmt_money(max(BANK_FEES_MONTHLY))}"
      f"/month, loosely tracking transaction volume (higher in the loan-draw and distribution months). "
      f"Evidenced by the bank statement, which is the bank's own assessment of its fee.")
    a(f"- Professional Fees (Corrado Bookkeeping Services): {fmt_money(min(PROFESSIONAL_FEES_MONTHLY))} to "
      f"{fmt_money(max(PROFESSIONAL_FEES_MONTHLY))}/month, lumpy around the accountant's actual work that "
      f"month (routine bookkeeping most months; a spike in January for 1099/W-2 prep, April for the "
      f"corporate income tax filing, September for Q3 planning, December for year-end close). Evidenced by "
      f"the bank statement and `Corrado invoices 2025.pdf`.\n")
    a(f"**Real-world leakage (fixed).** The electric/gas utility, formerly named \"Consolidated Utility Co\" "
      f"(too close to Consolidated Edison, the real New York utility), is renamed **{UTILITIES_VENDOR}** "
      f"everywhere it appears: `documents.jsonl`'s counterparty field, the ledger's counterparty field, the "
      f"`utility bills 2025.pdf` bundle, and this answer key. No other counterparty was touched.\n")
    a(f"**Metadata flag (fixed).** The press brake invoice (`IMG_5502.jpg`, kind `bill_in`) is produced via "
      f"`photograph_receipt()` and is now correctly marked `\"scanned\": true` in `documents.jsonl` (was "
      f"incorrectly `false`).\n")

    return "\n".join(lines) + "\n"


answer_key_text = build_answer_key()
with open(os.path.join(LAB_DIR, "answer-key.md"), "w", encoding="utf-8") as f:
    f.write(answer_key_text)
print(f"[generate.py] wrote answer-key.md ({len(answer_key_text)} chars)", file=sys.stderr)

#!/usr/bin/env python3
"""
Builds the passing fixture and nine deliberately-broken fixtures used to
prove validate.py works (see fixtures/run.sh). Not part of the frozen
Stage A deliverable's runtime path -- this is test scaffolding.

Layout produced:
    fixtures/good/{ledger,documents,statements}.jsonl, opening_position.json
    fixtures/good/reporoot/content/21-challenges/materials/challenge-three/fixtureco/*
    fixtures/good/baseline.txt

    fixtures/broken/check1..check9/{ledger,documents,statements}.jsonl,
        opening_position.json
    fixtures/broken/check8/reporoot/...   (its own repo root + baseline)

Every broken/checkN fixture reuses fixtures/good/reporoot as its repo root
(via env var, see run.sh) EXCEPT check8, which needs its own repo root to
demonstrate a forbidden document and an extra file without touching the
real repo.
"""

import copy
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
GOOD_DIR = os.path.join(HERE, "good")
BROKEN_DIR = os.path.join(HERE, "broken")

# Always rebuild from a clean slate -- a stale file left over from a
# previous run (e.g. check8's leftover-notes.txt) would otherwise get
# picked up into a freshly-generated baseline manifest and silently stop
# being "extra", masking the check it's meant to demonstrate.
for _d in (GOOD_DIR, BROKEN_DIR):
    if os.path.isdir(_d):
        shutil.rmtree(_d)


def w(path, obj_or_lines, jsonl=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if jsonl:
            for rec in obj_or_lines:
                f.write(json.dumps(rec, sort_keys=True))
                f.write("\n")
        else:
            json.dump(obj_or_lines, f, indent=2, sort_keys=True)
            f.write("\n")


# ---------------------------------------------------------------------------
# Base ("good") data
# ---------------------------------------------------------------------------

MATERIALS_REL = "content/21-challenges/materials/challenge-three/fixtureco"

DOC_FILES = {
    "DOC-OPEN": "opening_letter.txt",
    "DOC-INV1": "invoice_1001.txt",
    "DOC-STMT-OP-JAN": "bank_statement_operating_jan.txt",
    "DOC-STMT-PR-JAN": "bank_statement_payroll_jan.txt",
    "DOC-PAYROLL-JAN": "payroll_summary_jan.txt",
}


def base_documents():
    return [
        {"doc_id": "DOC-OPEN", "kind": "opening_letter", "format": "txt", "scanned": False,
         "issued_date": "2024-12-31", "counterparty": "Prior CPA Firm",
         "amount": None, "path": f"{MATERIALS_REL}/opening_letter.txt"},
        {"doc_id": "DOC-INV1", "kind": "invoice_out", "format": "txt", "scanned": False,
         "issued_date": "2025-01-05", "counterparty": "Acme Diner",
         "amount": 20000, "path": f"{MATERIALS_REL}/invoice_1001.txt"},
        {"doc_id": "DOC-STMT-OP-JAN", "kind": "bank_statement", "format": "txt", "scanned": False,
         "issued_date": "2025-01-31", "counterparty": "Fixture Bank",
         "amount": None, "path": f"{MATERIALS_REL}/bank_statement_operating_jan.txt"},
        {"doc_id": "DOC-STMT-PR-JAN", "kind": "bank_statement", "format": "txt", "scanned": False,
         "issued_date": "2025-01-31", "counterparty": "Fixture Bank",
         "amount": None, "path": f"{MATERIALS_REL}/bank_statement_payroll_jan.txt"},
        {"doc_id": "DOC-PAYROLL-JAN", "kind": "payroll_summary", "format": "txt", "scanned": False,
         "issued_date": "2025-01-20", "counterparty": "Fixture Payroll Co",
         "amount": 15000, "path": f"{MATERIALS_REL}/payroll_summary_jan.txt"},
    ]


def base_ledger():
    L = []
    # OB-1: opening balances, dated the day before period_start
    ob_lines = [
        ("1000", 100000, 0, "Opening cash - operating"),
        ("1010", 20000, 0, "Opening cash - payroll"),
        ("1200", 50000, 0, "Opening AR - Acme Diner"),
        ("2000", 0, 30000, "Opening AP - Rossi Meats"),
        ("3000", 0, 140000, "Opening member capital"),
    ]
    for code, debit, credit, memo in ob_lines:
        L.append({"entry_id": "OB-1", "date": "2024-12-31", "account_code": code,
                   "account_name": "", "debit": debit, "credit": credit, "memo": memo,
                   "counterparty": "", "doc_ids": ["DOC-OPEN"]})

    def add(entry_id, date, code, debit, credit, memo, counterparty, doc_ids):
        L.append({"entry_id": entry_id, "date": date, "account_code": code, "account_name": "",
                   "debit": debit, "credit": credit, "memo": memo, "counterparty": counterparty,
                   "doc_ids": doc_ids})

    # J-0001: sales invoice issued, unpaid at period end (revenue on issuance)
    add("J-0001", "2025-01-05", "1200", 20000, 0, "Invoice 1001", "Acme Diner", ["DOC-INV1"])
    add("J-0001", "2025-01-05", "4000", 0, 20000, "Invoice 1001", "Acme Diner", ["DOC-INV1"])

    # J-0002: customer settles opening AR via operating account deposit
    add("J-0002", "2025-01-10", "1000", 50000, 0, "Receipt - Acme Diner (opening AR)",
        "Acme Diner", ["DOC-STMT-OP-JAN"])
    add("J-0002", "2025-01-10", "1200", 0, 50000, "Receipt - Acme Diner (opening AR)",
        "Acme Diner", ["DOC-OPEN"])

    # J-0003: pay down opening AP via operating account
    add("J-0003", "2025-01-15", "2000", 30000, 0, "Payment - Rossi Meats (opening AP)",
        "Rossi Meats", ["DOC-OPEN"])
    add("J-0003", "2025-01-15", "1000", 0, 30000, "Payment - Rossi Meats (opening AP)",
        "Rossi Meats", ["DOC-STMT-OP-JAN"])

    # J-0004: inter-account transfer, operating -> payroll
    add("J-0004", "2025-01-18", "1000", 0, 20000, "Transfer to payroll account", "",
        ["DOC-STMT-OP-JAN"])
    add("J-0004", "2025-01-18", "1010", 20000, 0, "Transfer from operating account", "",
        ["DOC-STMT-PR-JAN"])

    # J-0005: wages paid from payroll account
    add("J-0005", "2025-01-20", "6020", 15000, 0, "January wages", "Fixture Payroll Co",
        ["DOC-PAYROLL-JAN"])
    add("J-0005", "2025-01-20", "1010", 0, 15000, "January wages", "Fixture Payroll Co",
        ["DOC-STMT-PR-JAN"])

    # J-0006: bank fee on operating account
    add("J-0006", "2025-01-25", "6080", 500, 0, "Monthly account fee", "Fixture Bank",
        ["DOC-STMT-OP-JAN"])
    add("J-0006", "2025-01-25", "1000", 0, 500, "Monthly account fee", "Fixture Bank",
        ["DOC-STMT-OP-JAN"])

    return L


def base_statements():
    return [
        {
            "stmt_id": "STMT-OP-2025-01", "account_code": "1000",
            "stmt_period_start": "2025-01-01", "stmt_period_end": "2025-01-31",
            "opening_balance": 100000, "closing_balance": 99500,
            "doc_ids": ["DOC-STMT-OP-JAN"],
            "lines": [
                {"date": "2025-01-10", "description": "Deposit - Acme Diner", "amount": 50000,
                 "direction": "in", "entry_id": "J-0002"},
                {"date": "2025-01-15", "description": "Check - Rossi Meats", "amount": 30000,
                 "direction": "out", "entry_id": "J-0003"},
                {"date": "2025-01-18", "description": "Transfer to payroll", "amount": 20000,
                 "direction": "out", "entry_id": "J-0004"},
                {"date": "2025-01-25", "description": "Account fee", "amount": 500,
                 "direction": "out", "entry_id": "J-0006"},
            ],
        },
        {
            "stmt_id": "STMT-OP-2025-02", "account_code": "1000",
            "stmt_period_start": "2025-02-01", "stmt_period_end": "2025-02-28",
            "opening_balance": 99500, "closing_balance": 99500,
            "doc_ids": ["DOC-STMT-OP-JAN"], "lines": [],
        },
        {
            "stmt_id": "STMT-PR-2025-01", "account_code": "1010",
            "stmt_period_start": "2025-01-01", "stmt_period_end": "2025-01-31",
            "opening_balance": 20000, "closing_balance": 25000,
            "doc_ids": ["DOC-STMT-PR-JAN"],
            "lines": [
                {"date": "2025-01-18", "description": "Transfer from operating", "amount": 20000,
                 "direction": "in", "entry_id": "J-0004"},
                {"date": "2025-01-20", "description": "Payroll run", "amount": 15000,
                 "direction": "out", "entry_id": "J-0005"},
            ],
        },
    ]


def base_opening_position():
    return {
        "period_start": "2025-01-01",
        "period_end": "2025-01-31",
        "as_of": "2024-12-31",
        "cash_by_account": {
            "1000": {"amount_cents": 100000, "doc_ids": ["DOC-OPEN"]},
            "1010": {"amount_cents": 20000, "doc_ids": ["DOC-OPEN"]},
        },
        "accounts_receivable": [
            {"debtor": "Acme Diner", "amount_cents": 50000, "doc_ids": ["DOC-OPEN"]},
        ],
        "accounts_payable": [
            {"creditor": "Rossi Meats", "amount_cents": 30000, "doc_ids": ["DOC-OPEN"]},
        ],
        "equity_components": {
            "member_capital": {"account_code": "3000", "amount_cents": 140000, "doc_ids": ["DOC-OPEN"]},
        },
    }


def write_reporoot(root_dir):
    materials_dir = os.path.join(root_dir, MATERIALS_REL)
    os.makedirs(materials_dir, exist_ok=True)
    contents = {
        "opening_letter.txt": "Fixture Prior CPA Firm -- opening position letter as at 2024-12-31.\n",
        "invoice_1001.txt": "Fixture invoice 1001 to Acme Diner, dated 2025-01-05, total $200.00.\n",
        "bank_statement_operating_jan.txt": "Fixture Bank -- Cash Operating -- January 2025 statement.\n",
        "bank_statement_payroll_jan.txt": "Fixture Bank -- Cash Payroll -- January 2025 statement.\n",
        "payroll_summary_jan.txt": "Fixture Payroll Co -- January 2025 payroll summary.\n",
    }
    for fn, text in contents.items():
        with open(os.path.join(materials_dir, fn), "w", encoding="utf-8") as f:
            f.write(text)

    # Baseline manifest matching this reporoot exactly (so a naive check-8
    # run against the *good* fixture reports no extra files).
    manifest_lines = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = "./" + os.path.relpath(full, root_dir)
            manifest_lines.append(f"{rel}\t{os.path.getsize(full)}")
    with open(os.path.join(GOOD_DIR, "baseline.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(manifest_lines)) + "\n")


def write_fixture(dir_path, ledger, documents, statements, opening_position):
    w(os.path.join(dir_path, "ledger.jsonl"), ledger, jsonl=True)
    w(os.path.join(dir_path, "documents.jsonl"), documents, jsonl=True)
    w(os.path.join(dir_path, "statements.jsonl"), statements, jsonl=True)
    w(os.path.join(dir_path, "opening_position.json"), opening_position)


def find(lines, entry_id, account_code):
    for l in lines:
        if l["entry_id"] == entry_id and l["account_code"] == account_code:
            return l
    raise KeyError((entry_id, account_code))


def build_good():
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    write_fixture(GOOD_DIR, ledger, documents, statements, opening_position)
    write_reporoot(os.path.join(GOOD_DIR, "reporoot"))


def build_check1():
    """Bank statement <-> ledger trace: retarget one statement line's
    entry_id so it no longer matches any ledger entry (and the ledger
    entry it used to describe now has no statement line)."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    op_jan = next(s for s in statements if s["stmt_id"] == "STMT-OP-2025-01")
    line = next(l for l in op_jan["lines"] if l["entry_id"] == "J-0003")
    line["entry_id"] = "J-0003X"
    write_fixture(os.path.join(BROKEN_DIR, "check1"), ledger, documents, statements, opening_position)


def build_check2():
    """Statement arithmetic: corrupt a closing balance. Drop the February
    continuation statement from this variant so the mutation doesn't also
    trip check 3 as collateral."""
    ledger = base_ledger()
    documents = base_documents()
    statements = [s for s in base_statements() if s["stmt_id"] != "STMT-OP-2025-02"]
    opening_position = base_opening_position()
    op_jan = next(s for s in statements if s["stmt_id"] == "STMT-OP-2025-01")
    op_jan["closing_balance"] += 100  # now inconsistent with opening + in - out
    write_fixture(os.path.join(BROKEN_DIR, "check2"), ledger, documents, statements, opening_position)


def build_check3():
    """Month-to-month continuity: break Feb's opening vs Jan's closing,
    while keeping Feb's own arithmetic internally consistent (so check 2
    stays green and the failure is isolated to check 3)."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    op_feb = next(s for s in statements if s["stmt_id"] == "STMT-OP-2025-02")
    op_feb["opening_balance"] = 99400
    op_feb["closing_balance"] = 99400  # keep it arithmetically self-consistent
    write_fixture(os.path.join(BROKEN_DIR, "check3"), ledger, documents, statements, opening_position)


def build_check4():
    """Inter-account transfer wrongly carries an income leg."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    ledger.append({
        "entry_id": "J-0004", "date": "2025-01-18", "account_code": "4900", "account_name": "",
        "debit": 0, "credit": 500, "memo": "Transfer rounding (should not be income)",
        "counterparty": "", "doc_ids": ["DOC-STMT-OP-JAN"],
    })
    write_fixture(os.path.join(BROKEN_DIR, "check4"), ledger, documents, statements, opening_position)


def build_check5():
    """Non-cash entry (invoice/revenue) loses its evidencing document."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    line = find(ledger, "J-0001", "4000")
    line["doc_ids"] = []
    write_fixture(os.path.join(BROKEN_DIR, "check5"), ledger, documents, statements, opening_position)


def build_check6():
    """A cash-touching entry loses its evidencing document. check 5 cannot
    see this (it only examines non-cash entries) -- only check 6's
    all-lines sweep catches it, demonstrating the two checks are not
    redundant."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    line = find(ledger, "J-0006", "1000")
    line["doc_ids"] = ["DOC-DOES-NOT-EXIST"]
    write_fixture(os.path.join(BROKEN_DIR, "check6"), ledger, documents, statements, opening_position)


def build_check7():
    """Unbalance a journal entry (debit != credit), which breaks both the
    per-entry balance sub-check and the period-end accounting equation."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    line = find(ledger, "J-0001", "4000")
    line["credit"] = 25000  # was 20000; now debit 20000 != credit 25000
    write_fixture(os.path.join(BROKEN_DIR, "check7"), ledger, documents, statements, opening_position)


def build_check8():
    """Forbidden document under materials/, plus an extra file outside the
    two permitted trees. Uses its own repo root so nothing under the real
    repo is touched."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    check8_dir = os.path.join(BROKEN_DIR, "check8")
    write_fixture(check8_dir, ledger, documents, statements, opening_position)

    reporoot = os.path.join(check8_dir, "reporoot")
    materials_dir = os.path.join(reporoot, MATERIALS_REL)
    os.makedirs(materials_dir, exist_ok=True)
    for fn, text in {
        "opening_letter.txt": "Fixture Prior CPA Firm -- opening position letter.\n",
        "invoice_1001.txt": "Fixture invoice 1001.\n",
        "bank_statement_operating_jan.txt": "Fixture Bank -- January 2025 statement.\n",
        "bank_statement_payroll_jan.txt": "Fixture Bank -- January 2025 statement.\n",
        "payroll_summary_jan.txt": "Fixture Payroll Co -- January 2025 payroll summary.\n",
    }.items():
        with open(os.path.join(materials_dir, fn), "w", encoding="utf-8") as f:
            f.write(text)
    # Forbidden document #1: filename pattern match.
    with open(os.path.join(materials_dir, "balance-sheet-2025.pdf"), "w", encoding="utf-8") as f:
        f.write("(pretend PDF bytes) FY2025 Balance Sheet -- Total Assets $500,000\n")

    # Forbidden document #2: an innocuous, Bright-Harbor-shoebox-style
    # filename whose *content* is forbidden -- proves the content-scan
    # branch (not just the filename-pattern branch) actually fires. This is
    # the realistic failure mode: a human filename like "scan0031.txt"
    # hiding a Trial Balance.
    with open(os.path.join(materials_dir, "scan0031.txt"), "w", encoding="utf-8") as f:
        f.write("Trial Balance as at 31 December 2025\nTotal Assets: $500,000.00\n")

    # Baseline manifest capturing everything EXCEPT the two files we are
    # about to add outside/inside the tree, so both violations are visible.
    manifest_lines = []
    for dirpath, _, filenames in os.walk(reporoot):
        for fn in filenames:
            if fn in ("balance-sheet-2025.pdf", "scan0031.txt"):
                continue
            full = os.path.join(dirpath, fn)
            rel = "./" + os.path.relpath(full, reporoot)
            manifest_lines.append(f"{rel}\t{os.path.getsize(full)}")
    with open(os.path.join(check8_dir, "baseline.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(manifest_lines)) + "\n")

    # Extra file outside both permitted trees, not in the baseline.
    with open(os.path.join(reporoot, "leftover-notes.txt"), "w", encoding="utf-8") as f:
        f.write("scratch notes that should never have been committed here\n")


def build_check9():
    """Opening letter cash for one account no longer ties to that account's
    first in-period statement opening balance."""
    ledger = base_ledger()
    documents = base_documents()
    statements = base_statements()
    opening_position = base_opening_position()
    opening_position["cash_by_account"]["1000"]["amount_cents"] = 90000  # stmt says 100000
    write_fixture(os.path.join(BROKEN_DIR, "check9"), ledger, documents, statements, opening_position)


if __name__ == "__main__":
    build_good()
    build_check1()
    build_check2()
    build_check3()
    build_check4()
    build_check5()
    build_check6()
    build_check7()
    build_check8()
    build_check9()
    print("fixtures built.")

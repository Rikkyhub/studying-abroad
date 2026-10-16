"""Validate public CSV trackers without dependencies. Run: python3 scripts/validate_data.py"""
import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPENSES = {"id", "period_start", "period_end", "phase", "category", "item", "currency", "quoted_amount", "paid_amount", "actual_amount", "fx_jpy_per_unit", "fx_asof", "quote_status", "payment_status", "paid_on", "source_url", "verified_at", "notes"}
TASKS = {"id", "phase", "task", "status", "priority", "due_date", "estimated_jpy", "source_url", "issue_url", "notes"}
ERRORS = []


def load(path, required):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not required.issubset(set(reader.fieldnames or ())):
            ERRORS.append(f"{path.name}: required columns are missing: {required - set(reader.fieldnames or ())}")
            return []
        rows = list(reader)
    seen = set()
    for n, row in enumerate(rows, 2):
        if None in row or None in row.values():
            ERRORS.append(f"{path.name}:{n}: CSV column count mismatch")
        key = (row.get("id") or "").strip()
        if not key or key in seen:
            ERRORS.append(f"{path.name}:{n}: missing/duplicate ID {key!r}")
        seen.add(key)
    return rows


def amount(value, label):
    if not value:
        return None
    try:
        n = Decimal(value)
        if not n.is_finite() or n < 0:
            raise ValueError("amount must be nonnegative and finite")
        return n
    except (InvalidOperation, ValueError):
        ERRORS.append(f"{label}: invalid nonnegative amount {value!r}")
        return None


def main():
    expense_rows = load(ROOT / "data/expenses.csv", EXPENSES)
    for n, row in enumerate(expense_rows, 2):
        label = f"expenses.csv:{n}"
        for column in ("quoted_amount", "paid_amount", "actual_amount", "fx_jpy_per_unit"):
            amount(row[column], label + ":" + column)
        if row["currency"] and len(row["currency"]) != 3:
            ERRORS.append(f"{label}: currency must be ISO 4217 3-letter code")
        if row["quote_status"] not in ("", "estimate", "confirmed", "actual"):
            ERRORS.append(f"{label}: unknown quote_status")
        if row["payment_status"] not in ("", "unpaid", "partial", "paid"):
            ERRORS.append(f"{label}: unknown payment_status")
    task_rows = load(ROOT / "data/tasks.csv", TASKS)
    for n, row in enumerate(task_rows, 2):
        label = f"tasks.csv:{n}"
        if row["status"] not in ("not_started", "in_progress", "blocked", "done"):
            ERRORS.append(f"{label}: unknown status")
        if row["priority"] not in ("P0", "P1", "P2", "P3"):
            ERRORS.append(f"{label}: unknown priority")
        amount(row["estimated_jpy"], label + ":estimated_jpy")
    if ERRORS:
        for err in ERRORS:
            print("ERROR:", err, file=sys.stderr)
        return 1
    print(f"PASS: {len(expense_rows)} expense rows; {len(task_rows)} task rows; schemas and values valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate public CSV trackers without dependencies. Run: python3 scripts/validate_data.py"""
import csv
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPENSES = {"id", "period_start", "period_end", "phase", "category", "item", "currency", "quoted_amount", "paid_amount", "actual_amount", "fx_jpy_per_unit", "fx_asof", "quote_status", "payment_status", "paid_on", "source_url", "verified_at", "notes"}
TASKS = {"id", "phase", "task", "status", "priority", "due_date", "estimated_jpy", "source_url", "issue_url", "notes"}
PAGES = {"id", "group", "area", "title", "summary", "path", "issue", "status", "sort", "verified_at", "refs"}
PLACES = {"id", "area", "name", "kind", "maps_query", "note", "source"}
FX = {"currency", "name_ja", "unit", "region", "jpy_per_unit", "rate_date", "rate_kind", "source"}
HTTP_URL = re.compile(r"^https?://[^\s;]+$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIMELINE = {"id", "period", "title", "status", "summary", "page_ids", "sort"}
ISSUE_URL = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/issues/\d+$")
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


def load_fx(path):
    """fx.csv は currency が主キー"""
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not FX.issubset(set(reader.fieldnames or ())):
            ERRORS.append(f"{path.name}: required columns are missing")
            return []
        rows = list(reader)
    codes = [r["currency"] for r in rows]
    if len(codes) != len(set(codes)):
        ERRORS.append(f"{path.name}: duplicate currency")
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
    page_rows = load(ROOT / "data/pages.csv", PAGES)
    page_ids = {(r.get("id") or "").strip() for r in page_rows}
    for n, row in enumerate(page_rows, 2):
        label = f"pages.csv:{n}"
        if not (ROOT / row["path"]).is_file():
            ERRORS.append(f"{label}: path does not exist: {row['path']!r}")
        if row["issue"] and not ISSUE_URL.match(row["issue"]):
            ERRORS.append(f"{label}: issue must be a github issues URL or empty")
        if row["group"] not in ("research", "plan"):
            ERRORS.append(f"{label}: unknown group")
        if not row["title"].strip() or not row["sort"].isdigit():
            ERRORS.append(f"{label}: title required and sort must be an integer")
        refs = [x.strip() for x in row["refs"].split(";") if x.strip()]
        if len(refs) > 3:
            ERRORS.append(f"{label}: refs must have at most 3 URLs")
        for u in refs:
            if not HTTP_URL.match(u):
                ERRORS.append(f"{label}: refs must be http(s) URLs separated by ';'")
    timeline_rows = load(ROOT / "data/timeline.csv", TIMELINE)
    for n, row in enumerate(timeline_rows, 2):
        for pid in filter(None, row["page_ids"].split(";")):
            if pid not in page_ids:
                ERRORS.append(f"timeline.csv:{n}: unknown page id {pid!r}")
        if not row["sort"].isdigit():
            ERRORS.append(f"timeline.csv:{n}: sort must be an integer")
    place_rows = load(ROOT / "data/places.csv", PLACES)
    for n, row in enumerate(place_rows, 2):
        label = f"places.csv:{n}"
        if row["area"] not in ("baguio", "capetown", "africa", "other"):
            ERRORS.append(f"{label}: unknown area")
        if not row["name"].strip() or not row["maps_query"].strip():
            ERRORS.append(f"{label}: name and maps_query are required")
        src = row["source"].strip()
        if src and not HTTP_URL.match(src) and not (ROOT / src).is_file():
            ERRORS.append(f"{label}: source must be an http(s) URL or an existing repo path")
    fx_rows = load_fx(ROOT / "data/fx.csv")
    for n, row in enumerate(fx_rows, 2):
        label = f"fx.csv:{n}"
        if not re.fullmatch(r"[A-Z]{3}", row["currency"]):
            ERRORS.append(f"{label}: currency must be a 3-letter uppercase code")
        rate = row["jpy_per_unit"].strip()
        if rate:
            n_rate = amount(rate, label + ":jpy_per_unit")
            if n_rate is not None and n_rate == 0:
                ERRORS.append(f"{label}: jpy_per_unit must be > 0 or empty")
            if not ISO_DATE.match(row["rate_date"]) or not row["rate_kind"].strip() or not HTTP_URL.match(row["source"]):
                ERRORS.append(f"{label}: a rate needs ISO rate_date, rate_kind and an http(s) source")
    if ERRORS:
        for err in ERRORS:
            print("ERROR:", err, file=sys.stderr)
        return 1
    print(f"PASS: {len(expense_rows)} expense rows; {len(task_rows)} task rows; schemas and values valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

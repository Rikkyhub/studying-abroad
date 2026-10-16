"""Check that public CSV files contain market estimates, not personal transactions.

This catches a narrow set of mistakes. Review all source, HTML, Markdown,
issues, screenshots and Git history separately before publishing.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISALLOWED_EXPENSE_FIELDS = {
    "paid_jpy", "paid_date", "actual_jpy", "actual_local", "actual_fx",
    "evidence", "receipt", "invoice_number", "bank_account",
}
LEGACY_PERSONAL_FIELDS = {"paid_amount", "actual_amount", "payment_status", "paid_on"}
PRIVATE_FUND_MARKERS = {"fund_savings", "fund_other", "資金", "預貯金", "預金残高"}


def check(root: Path) -> list[str]:
    """Report column locations, never values, to avoid CI log disclosure."""
    problems = []
    for path in sorted((root / "data").glob("*.csv")):
        with path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            header = set(reader.fieldnames or ())
            if path.name == "expenses.csv":
                for field in sorted(header & DISALLOWED_EXPENSE_FIELDS):
                    problems.append(f"{path.name}: prohibited private-data field: {field}")
            for line, record in enumerate(reader, 2):
                if path.name == "expenses.csv":
                    for field in sorted(LEGACY_PERSONAL_FIELDS & header):
                        if (record.get(field) or "").strip():
                            problems.append(f"{path.name}:{line}: nonempty private-data field: {field}")
                elif path.name == "funds.csv":
                    if any(any(marker in (record.get(field) or "")
                               for marker in PRIVATE_FUND_MARKERS)
                           for field in ("id", "type", "name")):
                        problems.append(f"{path.name}:{line}: personal funding row is not public")
    return problems


def main() -> int:
    problems = check(ROOT)
    if problems:
        for problem in problems:
            print("ERROR:", problem, file=sys.stderr)
        return 1
    print("PASS: public CSV personal-payment and personal-funding guard")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Check that public CSV files contain market estimates, not personal transactions.

This catches a narrow set of mistakes. Review all source, HTML, Markdown,
issues, screenshots and Git history separately before publishing.
"""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISALLOWED_EXPENSE_FIELDS = {
    "paid_jpy", "paid_date", "actual_jpy", "actual_local", "actual_fx",
    "evidence", "receipt", "invoice_number", "bank_account",
}
LEGACY_PERSONAL_FIELDS = {"paid_amount", "actual_amount", "payment_status", "paid_on"}
PRIVATE_FUND_MARKERS = {"fund_savings", "fund_other", "資金", "預貯金", "預金残高"}
# Detect direct links to identifiable Notion pages, without embedding private page IDs.
NOTION_PAGE_LINK = re.compile(
    r"https?://(?:[a-z0-9-]+\.)?(?:notion\.so|notion\.site|notion\.com)/[^\s<>\x27\"\)]*(?:[0-9a-f]{32}|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})",
    re.IGNORECASE,
)


# Official catalog/article identifiers are not personal phone or account numbers.
# Only these narrowly defined public URL paths are exempt; other numbers are checked.
OFFICIAL_CATALOG_URL = re.compile(
    r"https://www\.muji\.com/jp/ja/store/cmdty/(?:detail/\d{13}(?!\d)|section/S\d{7}(?!\d))"
    r"|https://support\.cambridgeenglish\.org/hc/en-gb/articles/\d{9}-[A-Za-z-]+"
)


def without_official_catalog_ids(value: str) -> str:
    return OFFICIAL_CATALOG_URL.sub("[official-catalog-reference]", value)


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
    # Scan published text and generated HTML too; CSV-only checks miss page links.
    # Emit only file paths and line numbers, never the potentially private URL.
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html", ".csv"}:
            continue
        if any(part in {"tests", "scripts", ".git"} for part in path.relative_to(root).parts):
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if NOTION_PAGE_LINK.search(line):
                problems.append(
                    f"{path.relative_to(root)}:{line_no}: Notion page link requires privacy review"
                )
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

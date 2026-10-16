"""Validate public CSV trackers without dependencies. Run: python3 scripts/validate_data.py

スキーマ（必須列・列数・ID重複・数値・日付・コード値）のみを検証する。
集計ルールの検証と生成物の整合性は scripts/build.py --check が担当する。
"""
import csv
import datetime as dt
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "expenses.csv": ["id", "category", "country", "phase", "item", "payee", "period_start", "period_end", "due_date", "status",
                     "currency", "low_local", "std_local", "high_local", "paid_jpy", "paid_date", "actual_local", "actual_fx",
                     "actual_jpy", "source", "evidence", "collected_on", "recheck_by", "issue", "note"],
    "tasks.csv": ["id", "phase", "task", "deadline", "status", "priority", "owner", "cost_note", "next_action", "source", "issue", "note"],
    "timeline.csv": ["id", "start", "end", "phase", "title", "place", "status", "note"],
    "articles.csv": ["id", "series", "title", "status", "materials", "needs", "draft"],
    "funds.csv": ["id", "type", "name", "amount_jpy", "as_of", "note"],
    "fx.csv": ["currency", "jpy_per_unit", "rate_date", "source", "note"],
    "meta.csv": ["key", "value", "note"],
}
NUMERIC = {
    "expenses.csv": ["low_local", "std_local", "high_local", "paid_jpy", "actual_local", "actual_fx", "actual_jpy"],
    "funds.csv": ["amount_jpy"],
    "fx.csv": ["jpy_per_unit"],
}
DATES = {
    "expenses.csv": ["period_start", "period_end", "due_date", "paid_date", "collected_on", "recheck_by"],
    "tasks.csv": ["deadline"],
    "timeline.csv": ["start", "end"],
    "funds.csv": ["as_of"],
    "fx.csv": ["rate_date"],
}
ENUMS = {
    ("expenses.csv", "status"): {"確定", "見積", "未確認", "実績"},
    ("tasks.csv", "status"): {"未着手", "進行中", "要確認", "完了", "保留", "不要"},
    ("tasks.csv", "priority"): {"1", "2", "3", "4"},
    ("articles.csv", "status"): {"未着手", "資料収集中", "下書き", "公開可能", "公開済み"},
    ("funds.csv", "type"): {"予算", "資金"},
}
# 公開リポジトリに載せてはいけない値のパターン（旅券番号・メール・電話・長い番号）
PRIVATE = [re.compile(p) for p in (r"[A-Z]{1,2}\d{7}\b", r"[\w.+-]+@[\w-]+\.[\w.]+", r"\b0\d{1,4}-\d{1,4}-\d{3,4}\b", r"\b\d{9,}\b")]
ERRORS = []


def load(name):
    path = ROOT / "data" / name
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, [])
        rows = list(reader)
    missing = [c for c in SCHEMAS[name] if c not in header]
    if missing:
        ERRORS.append(f"{name}: required columns are missing: {missing}")
        return []
    out, seen = [], set()
    key = "currency" if name == "fx.csv" else "key" if name == "meta.csv" else "id"
    for n, values in enumerate(rows, 2):
        if not any(v.strip() for v in values):
            continue
        if len(values) != len(header):
            ERRORS.append(f"{name}:{n}: CSV column count mismatch ({len(values)} != {len(header)}). セル内の半角カンマを確認")
            continue
        row = {h: v.strip() for h, v in zip(header, values)}
        k = row.get(key, "")
        if not k or k in seen:
            ERRORS.append(f"{name}:{n}: missing/duplicate {key} {k!r}")
        seen.add(k)
        out.append((n, row))
    return out


def check(name, rows):
    for n, row in rows:
        label = f"{name}:{n}"
        for col in NUMERIC.get(name, []):
            v = row[col]
            if v:
                try:
                    d = Decimal(v)
                    if not d.is_finite() or d < 0:
                        raise ValueError
                except (InvalidOperation, ValueError):
                    ERRORS.append(f"{label}:{col}: invalid nonnegative number {v!r}（桁区切りのカンマは不可）")
        for col in DATES.get(name, []):
            v = row[col]
            if v:
                try:
                    dt.date.fromisoformat(v)
                except ValueError:
                    ERRORS.append(f"{label}:{col}: date must be YYYY-MM-DD, got {v!r}")
        for (fname, col), allowed in ENUMS.items():
            if fname == name and row[col] not in allowed:
                ERRORS.append(f"{label}:{col}: unknown value {row[col]!r}（{'/'.join(sorted(allowed))}）")
        if name == "expenses.csv":
            if row["currency"] and not re.fullmatch(r"[A-Z]{3}", row["currency"]):
                ERRORS.append(f"{label}: currency must be ISO 4217 3-letter code")
            if row["period_start"] and row["period_end"] and row["period_end"] < row["period_start"]:
                ERRORS.append(f"{label}: period_end is before period_start")
        for col, v in row.items():
            if col in ("source", "issue") or v.startswith("http"):
                continue
            for pat in PRIVATE:
                if pat.search(v):
                    ERRORS.append(f"{label}:{col}: 個人情報らしき値（番号・メール・電話）。公開リポジトリには書かない")


def main():
    counts = {}
    loaded = {}
    for name in SCHEMAS:
        rows = load(name)
        check(name, rows)
        counts[name] = len(rows)
        loaded[name] = rows
    fx = {row["currency"] for _, row in loaded["fx.csv"]} | {"JPY"}
    for n, row in loaded["expenses.csv"]:
        if row["currency"] and row["currency"] not in fx:
            ERRORS.append(f"expenses.csv:{n}: currency {row['currency']} has no rate in fx.csv")
    if ERRORS:
        for err in ERRORS:
            print("ERROR:", err, file=sys.stderr)
        return 1
    print("PASS: " + "; ".join(f"{k} {v} rows" for k, v in counts.items()) + "; schemas and values valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Validate public CSV trackers without dependencies. Run: python3 scripts/validate_data.py

スキーマ（必須列・列数・ID重複・数値・日付・コード値）のみを検証する。
集計ルールと生成物の整合性は scripts/build.py --check、個人データ列の混入は
scripts/check_public_data.py が担当する。公開CSVは匿名の見積モデルだけを置く。
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
                     "currency", "low_local", "std_local", "high_local", "source", "collected_on", "recheck_by", "issue", "note"],
    "tasks.csv": ["id", "phase", "task", "deadline_kind", "deadline_note", "lead_days", "status", "priority", "owner", "cost_note", "next_action", "source", "issue", "note"],
    "timeline.csv": ["id", "period", "title", "status", "summary", "page_ids", "sort"],
    "pages.csv": ["id", "group", "area", "title", "summary", "path", "issue", "status", "sort", "verified_at", "refs"],
    "places.csv": ["id", "area", "name", "kind", "maps_query", "note", "source"],
    "articles.csv": ["id", "series", "title", "status", "materials", "needs", "draft"],
    "funds.csv": ["id", "type", "name", "amount_jpy", "as_of", "note"],
    "fx.csv": ["currency", "name_ja", "unit", "region", "jpy_per_unit", "rate_date", "rate_kind", "source"],
    "meta.csv": ["key", "value", "note"],
}
NUMERIC = {
    "expenses.csv": ["low_local", "std_local", "high_local"],
    "funds.csv": ["amount_jpy"],
    "fx.csv": ["jpy_per_unit"],
}
DATES = {
    "expenses.csv": ["period_start", "period_end", "due_date", "collected_on", "recheck_by"],
    "pages.csv": ["verified_at"],
    "funds.csv": ["as_of"],
    "fx.csv": ["rate_date"],
}
ENUMS = {
    # 公開CSVでは「確定」「実績」（個人の支払い・実費）を使わない
    ("expenses.csv", "status"): {"見積", "未確認"},
    ("tasks.csv", "status"): {"未着手", "進行中", "要確認", "完了", "保留", "不要"},
    ("tasks.csv", "priority"): {"1", "2", "3", "4"},
    ("tasks.csv", "deadline_kind"): {"公式期限", "学校・機関の個別期限", "推奨目安", "要確認"},
    ("articles.csv", "status"): {"未着手", "資料収集中", "下書き", "公開可能", "公開済み"},
    ("funds.csv", "type"): {"予算"},
    ("pages.csv", "group"): {"research", "plan"},
    ("pages.csv", "status"): {"researching", "ready", "draft"},
    ("places.csv", "area"): {"baguio", "capetown", "africa", "other"},
}
HTTP_URL = re.compile(r"^https?://[^\s;]+$")
ISSUE_URL = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/issues/\d+$")
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
                    ERRORS.append(f"{label}:{col}: invalid nonnegative number（桁区切りのカンマは不可）")
        for col in DATES.get(name, []):
            v = row[col]
            if v:
                try:
                    dt.date.fromisoformat(v)
                except ValueError:
                    ERRORS.append(f"{label}:{col}: date must be YYYY-MM-DD")
        for (fname, col), allowed in ENUMS.items():
            if fname == name and row[col] not in allowed:
                ERRORS.append(f"{label}:{col}: unknown value {row[col]!r}（{'/'.join(sorted(allowed))}）")
        if name == "tasks.csv":
            if not row["deadline_note"]:
                ERRORS.append(f"{label}: deadline_note is required（相対期限・要確認の文言）")
            elif re.search(r"\d{4}-\d{2}-\d{2}|\d{4}年\d{1,2}月\d{1,2}日", row["deadline_note"]):
                ERRORS.append(f"{label}: deadline_note に暦日を書かない（相対表記の目安にする）")
            if not re.fullmatch(r"-?\d+", row["lead_days"]):
                ERRORS.append(f"{label}: lead_days must be an integer")
        if name == "expenses.csv":
            for s in ("std", "high"):
                raw = row[f"{s}_local"]
                if row["low_local"] and raw and re.fullmatch(r"[\d.]+", row["low_local"]) and re.fullmatch(r"[\d.]+", raw):
                    if Decimal(row["low_local"]) > 0 and Decimal(raw) == 0:
                        ERRORS.append(f"{label}:{s}_local: 0 は未計上ではありません。low が非ゼロで {s} が未計上なら空欄にする")
            if row["currency"] and not re.fullmatch(r"[A-Z]{3}", row["currency"]):
                ERRORS.append(f"{label}: currency must be ISO 4217 3-letter code")
            if row["period_start"] and row["period_end"] and row["period_end"] < row["period_start"]:
                ERRORS.append(f"{label}: period_end is before period_start")
        for col, v in row.items():
            if col in ("source", "issue") or v.startswith("http"):
                continue
            if any(p.search(v) for p in PRIVATE):
                # 値そのものは出力しない（CIログへの露出防止）
                ERRORS.append(f"{label}:{col}: 個人情報らしき値（番号・メール・電話）。公開リポジトリには書かない")


def main():
    counts, loaded = {}, {}
    for name in SCHEMAS:
        rows = load(name)
        check(name, rows)
        counts[name] = len(rows)
        loaded[name] = rows
    fx = {row["currency"] for _, row in loaded["fx.csv"]} | {"JPY"}
    for n, row in loaded["expenses.csv"]:
        if row["currency"] and row["currency"] not in fx:
            ERRORS.append(f"expenses.csv:{n}: currency {row['currency']} has no rate in fx.csv")
    page_ids = {row["id"] for _, row in loaded["pages.csv"]}
    for n, row in loaded["pages.csv"]:
        label = f"pages.csv:{n}"
        if not (ROOT / row["path"]).is_file():
            ERRORS.append(f"{label}: path does not exist: {row['path']!r}")
        if row["issue"] and not ISSUE_URL.match(row["issue"]):
            ERRORS.append(f"{label}: issue must be a github issues URL or empty")
        if not row["title"] or not row["sort"].isdigit():
            ERRORS.append(f"{label}: title required and sort must be an integer")
        refs = [x.strip() for x in row["refs"].split(";") if x.strip()]
        if len(refs) > 3:
            ERRORS.append(f"{label}: refs must have at most 3 URLs")
        for u in refs:
            if not HTTP_URL.match(u):
                ERRORS.append(f"{label}: refs must be http(s) URLs separated by ';'")
    for n, row in loaded["timeline.csv"]:
        for pid in filter(None, row["page_ids"].split(";")):
            if pid not in page_ids:
                ERRORS.append(f"timeline.csv:{n}: unknown page id {pid!r}")
        if not row["sort"].isdigit():
            ERRORS.append(f"timeline.csv:{n}: sort must be an integer")
        if re.search(r"\d{1,2}/\d{1,2}|\d+日", row["period"] + row["summary"]):
            ERRORS.append(f"timeline.csv:{n}: 日単位の日付は書かない（月単位で書く）")
    for n, row in loaded["places.csv"]:
        label = f"places.csv:{n}"
        if not row["name"] or not row["maps_query"]:
            ERRORS.append(f"{label}: name and maps_query are required")
        src = row["source"]
        if src and not HTTP_URL.match(src) and not (ROOT / src).is_file():
            ERRORS.append(f"{label}: source must be an http(s) URL or an existing repo path")
    for n, row in loaded["fx.csv"]:
        label = f"fx.csv:{n}"
        if not re.fullmatch(r"[A-Z]{3}", row["currency"]):
            ERRORS.append(f"{label}: currency must be a 3-letter uppercase code")
        if row["jpy_per_unit"]:
            if Decimal(row["jpy_per_unit"] or "0") == 0 if re.fullmatch(r"[\d.]+", row["jpy_per_unit"]) else False:
                ERRORS.append(f"{label}: jpy_per_unit must be > 0 or empty")
            if not row["rate_date"] or not row["rate_kind"] or not HTTP_URL.match(row["source"]):
                ERRORS.append(f"{label}: a rate needs rate_date, rate_kind and an http(s) source")
    if ERRORS:
        for err in ERRORS:
            print("ERROR:", err, file=sys.stderr)
        return 1
    print("PASS: " + "; ".join(f"{k} {v} rows" for k, v in counts.items()) + "; schemas and values valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())

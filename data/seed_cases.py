"""Import CSV cases into SQLite."""
import csv
from pathlib import Path
from database.db import upsert_case

def seed(path: Path | None = None) -> int:
    """Load all CSV rows into the application database."""
    path = path or Path(__file__).with_name("cases.csv")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["title"] = row.get("title") or row["symptom"][:80]; row["topology"] = row.get("topology") or row.get("topology_note", ""); row["show_output"] = row.get("show_output") or row.get("show_outputs", ""); row["category"] = row.get("category") or row.get("concept_tag", "Interface/Connectivity")
        upsert_case(row)
    return len(rows)
if __name__ == "__main__": print(f"Seeded {seed()} cases")

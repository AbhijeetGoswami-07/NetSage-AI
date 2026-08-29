"""SQLite persistence with parameterized queries."""
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "netsage.db"
SCHEMA = Path(__file__).with_name("schema.sql")
def now() -> str: return datetime.now(timezone.utc).isoformat()
def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    """Open a row-producing SQLite connection and initialize its schema."""
    path.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    return connection
def upsert_case(case: dict[str, Any], connection: sqlite3.Connection | None = None) -> None:
    """Insert or update one case using bound parameters."""
    own = connection is None; connection = connection or connect()
    connection.execute("""INSERT INTO cases(case_id,title,symptom,topology,show_output,expected_fault,osi_layer,concept,severity,category,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(case_id) DO UPDATE SET title=excluded.title,symptom=excluded.symptom,topology=excluded.topology,show_output=excluded.show_output,expected_fault=excluded.expected_fault,osi_layer=excluded.osi_layer,concept=excluded.concept,severity=excluded.severity,category=excluded.category""", tuple(case.get(k, "") for k in ["case_id","title","symptom","topology","show_output","expected_fault","osi_layer","concept","severity","category"]) + (case.get("created_at", now()),))
    if own: connection.commit(); connection.close()
def list_cases(search: str = "", category: str = "All", severity: str = "All") -> list[dict]:
    """Return cases filtered by safe bound parameters."""
    clauses = ["(title LIKE ? OR symptom LIKE ? OR case_id LIKE ?)"]; params = [f"%{search}%"] * 3
    if category != "All": clauses.append("category = ?"); params.append(category)
    if severity != "All": clauses.append("severity = ?"); params.append(severity)
    with connect() as db: return [dict(row) for row in db.execute("SELECT * FROM cases WHERE " + " AND ".join(clauses) + " ORDER BY created_at DESC", params)]
def get_case(case_id: str) -> dict | None:
    """Fetch one case."""
    with connect() as db:
        row = db.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone(); return dict(row) if row else None
def save_diagnosis(case_id: str, diagnosis: dict, ai_mode: str) -> int:
    """Persist an original diagnosis and return its ID."""
    with connect() as db:
        cur = db.execute("INSERT INTO diagnoses(case_id,root_cause,osi_layer,confidence,evidence,next_command,fix_steps,category,severity,ai_mode,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (case_id, diagnosis["root_cause"], diagnosis["osi_layer"], diagnosis["confidence"], json.dumps(diagnosis["evidence"]), diagnosis["next_command"], json.dumps(diagnosis["fix_steps"]), diagnosis["category"], diagnosis["severity"], ai_mode, now())); db.commit(); return int(cur.lastrowid)
def save_review(review: dict) -> None:
    """Persist a review without overwriting the original diagnosis."""
    with connect() as db:
        db.execute("INSERT INTO reviews(diagnosis_id,decision,edited_diagnosis,reviewer_comment,reviewed_at) VALUES(?,?,?,?,?)", (review["diagnosis_id"], review["decision"], json.dumps(review.get("edited_diagnosis")), review["reviewer_comment"], now())); db.commit()
def save_verification(item: dict) -> None:
    """Persist user-provided verification evidence."""
    with connect() as db:
        db.execute("INSERT INTO verifications(case_id,status,before_result,after_result,verification_notes,verified_at) VALUES(?,?,?,?,?,?)", (item["case_id"],item["status"],item["before_result"],item["after_result"],item["verification_notes"],now())); db.commit()
def add_rule_results(case_id: str, results: list[dict]) -> None:
    """Persist deterministic findings for a case."""
    with connect() as db:
        db.execute("DELETE FROM rule_results WHERE case_id = ?", (case_id,))
        db.executemany("INSERT INTO rule_results(case_id,rule_name,status,severity,finding,evidence,recommendation,created_at) VALUES(?,?,?,?,?,?,?,?)", [(case_id,r["rule_name"],r["status"],r["severity"],r["finding"],r["evidence"],r["recommendation"],now()) for r in results]); db.commit()

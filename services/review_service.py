"""Human review persistence."""
import json
from database.db import connect

def save(review: dict) -> None:
    """Save a review and preserve correction details for edits/rejections."""
    from database.db import save_review
    save_review(review)
    if review["decision"] != "ACCEPT":
        with connect() as db:
            row=db.execute("SELECT case_id,root_cause FROM diagnoses WHERE diagnosis_id=?",(review["diagnosis_id"],)).fetchone()
            db.execute("INSERT INTO responsible_ai_logs(case_id,diagnosis_id,ai_diagnosis,human_decision,corrected_diagnosis,reason_for_correction,lesson,created_at) VALUES(?,?,?,?,?,?,?,datetime('now'))",(row["case_id"],review["diagnosis_id"],row["root_cause"],review["decision"],json.dumps(review.get("edited_diagnosis") or {}),review["reviewer_comment"],"Compare model claims with quoted network evidence.")); db.commit()

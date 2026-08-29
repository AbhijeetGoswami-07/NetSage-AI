"""Database-backed analytics."""
from database.db import connect

def metrics() -> dict[str, int | float]:
    """Return dashboard KPIs computed from SQLite."""
    with connect() as db:
        total = db.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
        diagnoses = db.execute("SELECT COUNT(*) FROM diagnoses").fetchone()[0]
        accepted = db.execute("SELECT COUNT(*) FROM reviews WHERE decision='ACCEPT'").fetchone()[0]
        edited = db.execute("SELECT COUNT(*) FROM reviews WHERE decision='EDIT'").fetchone()[0]
        rejected = db.execute("SELECT COUNT(*) FROM reviews WHERE decision='REJECT'").fetchone()[0]
        verified = db.execute("SELECT COUNT(*) FROM verifications WHERE status='VERIFIED'").fetchone()[0]
        failed = db.execute("SELECT COUNT(*) FROM verifications WHERE status='FAILED'").fetchone()[0]
        inconclusive = db.execute("SELECT COUNT(*) FROM verifications WHERE status='INCONCLUSIVE'").fetchone()[0]
        high = db.execute("SELECT COUNT(*) FROM cases WHERE severity IN ('high', 'critical')").fetchone()[0]
    
    reviewed = accepted + edited + rejected
    
    return {
        "total_cases": total,
        "total_diagnoses": diagnoses,
        "accepted": accepted,
        "edited": edited,
        "rejected": rejected,
        "agreement_pct": round(accepted / reviewed * 100, 1) if reviewed else 0.0,
        "verified": verified,
        "failed_verification": failed,
        "inconclusive_verification": inconclusive,
        "high_issues": high,
    }

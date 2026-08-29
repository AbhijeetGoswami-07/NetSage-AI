"""Combined rule and diagnosis orchestration."""
from ai.ai_client import diagnose
from database import db
from rules.rule_engine import run_rules

def analyze(case: dict) -> tuple[int, list[dict], dict, str]:
    """Run rules, persist findings, generate and persist a diagnosis."""
    try:
        # Step 1: Run deterministic rules
        rules = run_rules(
            case["show_output"],
            case.get("category", "Interface/Connectivity")
        )
        
        # Step 2: Persist rule results
        db.add_rule_results(case["case_id"], rules)
        
        # Step 3: Generate diagnosis (live AI or fallback demo)
        result, mode = diagnose(case, rules)
        
        # Step 4: Convert diagnosis model to dictionary
        diagnosis = result.model_dump()
        
        # Step 5: Persist diagnosis
        diagnosis_id = db.save_diagnosis(case["case_id"], diagnosis, mode)
        
        return diagnosis_id, rules, diagnosis, mode
    except Exception as e:
        # Re-raise the exception so the caller can handle it
        raise Exception(f"Analysis workflow failed: {type(e).__name__}: {str(e)}") from e

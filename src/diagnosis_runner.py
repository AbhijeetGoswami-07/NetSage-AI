"""Run diagnoses for all CSV cases and save a reviewable JSON artifact."""
import csv
import json
import logging
from .config import DATA_DIR, RESULTS_DIR
from .llm_client import run_diagnosis_prompt
from .models import CaseRecord
from .rule_checker import run_all_rule_checks

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def load_cases() -> list[CaseRecord]:
    """Load and validate all cases from data/cases.csv."""
    path = DATA_DIR / "cases.csv"
    if not path.exists():
        raise FileNotFoundError(f"Case file not found: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return [CaseRecord.model_validate(row) for row in csv.DictReader(handle)]


def run() -> list[dict]:
    """Run per-case AI diagnoses, continuing after individual failures."""
    results = []
    for case in load_cases():
        try:
            diagnosis = run_diagnosis_prompt(case.symptom, case.topology_note, case.show_outputs)
            diagnosis_data = diagnosis.model_dump()
        except Exception as exc:  # Keep the batch useful when one provider call fails.
            logging.error("%s failed: %s", case.case_id, exc)
            diagnosis_data = None
        results.append({"case_id": case.case_id, "symptom": case.symptom, "expected_fault": case.expected_fault,
                        "diagnosis": diagnosis_data, "rule_checks": run_all_rule_checks(case)})
    RESULTS_DIR.mkdir(exist_ok=True)
    output = RESULTS_DIR / "ai_diagnoses.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results

if __name__ == "__main__":
    print(f"Wrote {len(run())} cases to {RESULTS_DIR / 'ai_diagnoses.json'}")

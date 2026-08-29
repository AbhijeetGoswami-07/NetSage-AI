"""Generate CSV summaries and an optional issue-type chart."""
import json
from collections import Counter
from .config import DATA_DIR, OUTPUT_DIR, RESULTS_DIR
from .diagnosis_runner import load_cases


def generate_dashboard() -> list[dict[str, str | int]]:
    """Create aggregate dashboard_summary.csv and issue_types.png when possible."""
    cases = load_cases()
    diagnosis_path = RESULTS_DIR / "ai_diagnoses.json"
    diagnoses = []
    if diagnosis_path.exists():
        try:
            diagnoses = json.loads(diagnosis_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Could not read {diagnosis_path}: {exc}") from exc
    concept = Counter(case.concept_tag for case in cases)
    layers = Counter(case.osi_layer for case in cases)
    severity = Counter(case.severity for case in cases)
    rows = ([{"metric": "concept_tag", "value": key, "count": count} for key, count in sorted(concept.items())] +
            [{"metric": "osi_layer", "value": key, "count": count} for key, count in sorted(layers.items())] +
            [{"metric": "severity", "value": key, "count": count} for key, count in sorted(severity.items())])
    rows.append({"metric": "ai_diagnoses_available", "value": "yes" if diagnoses else "no", "count": len(diagnoses)})
    review_path = RESULTS_DIR / "review_log.csv"
    if review_path.exists():
        import csv
        with review_path.open(newline="", encoding="utf-8") as handle:
            decisions = Counter(row.get("human_decision", "Unknown") for row in csv.DictReader(handle))
        rows.extend({"metric": "human_decision", "value": key, "count": count} for key, count in sorted(decisions.items()))
    RESULTS_DIR.mkdir(exist_ok=True)
    import csv
    with (RESULTS_DIR / "dashboard_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value", "count"]); writer.writeheader(); writer.writerows(rows)
    try:
        import matplotlib.pyplot as plt
        OUTPUT_DIR.mkdir(exist_ok=True)
        plt.figure(figsize=(8, 4)); plt.bar(concept.keys(), concept.values()); plt.title("Issue types"); plt.ylabel("Cases"); plt.xticks(rotation=30, ha="right"); plt.tight_layout(); plt.savefig(OUTPUT_DIR / "issue_types.png"); plt.close()
    except ImportError:
        pass
    return rows

if __name__ == "__main__":
    print(f"Wrote {len(generate_dashboard())} summary rows to {RESULTS_DIR / 'dashboard_summary.csv'}")

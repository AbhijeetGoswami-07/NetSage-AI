"""Build safe, evidence-bounded prompts."""
from pathlib import Path

def build_prompt(case: dict, rule_results: list[dict], template_path: Path | None = None) -> str:
    """Fill only named prompt tokens; JSON examples remain literal."""
    template = (template_path or Path(__file__).with_name("diagnosis_prompt.md")).read_text(encoding="utf-8")
    findings = "\n".join(f"- {r['status']} {r['rule_name']}: {r['finding']} Evidence: {r['evidence']}" for r in rule_results)
    return template.replace("{symptom}", case["symptom"]).replace("{topology}", case["topology"]).replace("{show_output}", case["show_output"]).replace("{rule_results}", findings)

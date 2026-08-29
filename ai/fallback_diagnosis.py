"""Transparent local demonstration diagnosis."""
from models.diagnosis import Diagnosis

def fallback_diagnosis(case: dict, rules: list[dict]) -> Diagnosis:
    """Derive a labelled diagnosis from the strongest deterministic finding."""
    failed = next((item for item in rules if item["status"] == "FAIL"), None)
    if failed:
        category = case.get("category", "Interface/Connectivity"); cause = failed["finding"]; evidence = [failed["evidence"] or "Rule output"]
        confidence = 88; severity = failed["severity"]
    else:
        category = case.get("category", "Interface/Connectivity"); cause = "The supplied evidence is insufficient to establish one root cause."; evidence = ["No deterministic FAIL finding was established."]; confidence = 25; severity = case.get("severity", "medium")
    return Diagnosis(root_cause=cause, osi_layer=case.get("osi_layer", "Unknown"), confidence=confidence, evidence=evidence, next_command="Collect the command output most relevant to the reported flow, then review again.", fix_steps=["Review the cited evidence with a network instructor.","Apply any change manually in Packet Tracer only after approval.","Run a before/after connectivity test."], category=category, severity=severity)

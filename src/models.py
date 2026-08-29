"""Validated models for cases and diagnoses."""
from typing import Literal
from pydantic import BaseModel, Field

Confidence = Literal["low", "medium", "high"]
OsiLayer = Literal["L1", "L2", "L3", "L4", "L5", "L6", "L7"]

class DiagnosisOutput(BaseModel):
    """Structured, human-reviewable diagnosis returned by the LLM."""
    root_cause: str = Field(description="Likely root cause")
    osi_layer: OsiLayer
    confidence: Confidence
    evidence: list[str] = Field(default_factory=list)
    next_command: str
    fix_steps: list[str] = Field(default_factory=list)

class CaseRecord(BaseModel):
    """One troubleshooting case loaded from cases.csv."""
    case_id: str
    symptom: str
    topology_note: str
    show_outputs: str
    expected_fault: str
    osi_layer: str
    concept_tag: str
    severity: str

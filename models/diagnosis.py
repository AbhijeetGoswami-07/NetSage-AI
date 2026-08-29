"""Diagnosis validation contract."""
from pydantic import BaseModel, Field, field_validator
from .case import SUPPORTED_CATEGORIES
class Diagnosis(BaseModel):
    """A diagnosis that is advisory until human review."""
    root_cause: str = Field(min_length=1)
    osi_layer: str = Field(min_length=1)
    confidence: int = Field(ge=0, le=100)
    evidence: list[str] = Field(default_factory=list)
    next_command: str = "Gather more show output."
    fix_steps: list[str] = Field(default_factory=list)
    category: str = "Interface/Connectivity"
    severity: str = "medium"
    @field_validator("category")
    @classmethod
    def valid_category(cls, value: str) -> str:
        if value not in SUPPORTED_CATEGORIES: raise ValueError(f"Unsupported category: {value}")
        return value

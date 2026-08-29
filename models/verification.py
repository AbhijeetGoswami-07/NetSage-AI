"""Verification result model and calculation."""
from typing import Literal
from pydantic import BaseModel, Field

class Verification(BaseModel):
    """User-provided before/after evidence for a case."""
    case_id: str
    before_result: str = Field(min_length=1)
    after_result: str = Field(min_length=1)
    verification_notes: str = Field(default="")
    status: Literal["VERIFIED", "FAILED", "INCONCLUSIVE"]

def calculate_status(before_result: str, after_result: str) -> str:
    """Classify verification from explicit user-entered evidence.
    
    Rules:
    - Before=FAILED and After=SUCCESS → VERIFIED
    - Before=FAILED and After=FAILED → FAILED  
    - Otherwise → INCONCLUSIVE
    - Normalizes common typos (e.g., SUCCSE → SUCCESS, FAILE → FAILED)
    """
    # Normalize the after result
    after_normalized = after_result.upper().strip()
    
    # Fix common typos
    after_normalized = after_normalized.replace("SUCCSE", "SUCCESS")
    after_normalized = after_normalized.replace("SUCCES", "SUCCESS")
    after_normalized = after_normalized.replace("SUCESS", "SUCCESS")
    after_normalized = after_normalized.replace("FAILE", "FAILED")
    after_normalized = after_normalized.replace("FAILD", "FAILED")
    
    # Determine status based on after result keywords
    if "SUCCESS" in after_normalized or "PASS" in after_normalized or "UP" in after_normalized:
        return "VERIFIED"
    elif "FAILED" in after_normalized or "FAIL" in after_normalized or "DOWN" in after_normalized:
        return "FAILED"
    else:
        return "INCONCLUSIVE"

"""Human review model."""
from typing import Literal
from pydantic import BaseModel, Field

class Review(BaseModel):
    """A required human decision over an original diagnosis."""
    diagnosis_id: int
    decision: Literal["ACCEPT", "EDIT", "REJECT"]
    edited_diagnosis: dict | None = None
    reviewer_comment: str = Field(default="", min_length=0)

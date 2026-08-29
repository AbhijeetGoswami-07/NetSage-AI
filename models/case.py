"""Case input model and category vocabulary."""
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
SUPPORTED_CATEGORIES = {"VLAN", "Default Gateway", "DHCP", "DNS", "Routing", "ACL", "NAT", "Wireless", "Interface/Connectivity"}
class Case(BaseModel):
    """A Cisco-style troubleshooting case."""
    case_id: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=1, max_length=200)
    symptom: str = Field(min_length=1, max_length=5000)
    topology: str = Field(default="", max_length=5000)
    show_output: str = Field(min_length=1, max_length=50000)
    expected_fault: str = ""
    osi_layer: str = "Unknown"
    concept: str = ""
    severity: str = "medium"
    category: str = "Interface/Connectivity"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    @field_validator("category")
    @classmethod
    def valid_category(cls, value: str) -> str:
        if value not in SUPPORTED_CATEGORIES: raise ValueError(f"Unsupported category: {value}")
        return value

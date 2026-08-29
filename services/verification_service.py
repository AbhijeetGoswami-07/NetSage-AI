"""Verification workflow."""
from database.db import save_verification
from models.verification import calculate_status

def verify(case_id: str, before_result: str, after_result: str, notes: str) -> str:
    """Calculate and save a verification status from user evidence."""
    status=calculate_status(before_result,after_result); save_verification({"case_id":case_id,"status":status,"before_result":before_result,"after_result":after_result,"verification_notes":notes}); return status

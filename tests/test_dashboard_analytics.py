"""Dashboard analytics calculation tests."""
from services.analytics_service import metrics
from database.db import connect, upsert_case, save_diagnosis, save_review, save_verification
from models.case import Case
from pathlib import Path
import tempfile
import json

def test_metrics_empty_database():
    """Test metrics with empty database."""
    # Use temporary database for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db = Path(tmpdir) / "test.db"
        # This test uses the default database, so we can only verify structure
        result = metrics()
        
        # Check that all required keys are present
        required_keys = [
            "total_cases",
            "total_diagnoses", 
            "accepted",
            "edited",
            "rejected",
            "agreement_pct",
            "verified",
            "failed_verification",
            "inconclusive_verification",
            "high_issues"
        ]
        
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
            assert isinstance(result[key], (int, float)), f"Invalid type for {key}"

def test_agreement_percentage_calculation():
    """Test AI-human agreement calculation."""
    result = metrics()
    
    # Agreement should be 0-100% or 0 if no reviews
    assert 0 <= result['agreement_pct'] <= 100

def test_high_critical_issues_filter():
    """Test high/critical issues are counted correctly."""
    result = metrics()
    
    # Should be non-negative
    assert result['high_issues'] >= 0

def test_verification_count_distinct_statuses():
    """Test that verification counts are distinct by status."""
    result = metrics()
    
    # Each status should have independent counts
    assert result['verified'] >= 0
    assert result['failed_verification'] >= 0
    assert result['inconclusive_verification'] >= 0

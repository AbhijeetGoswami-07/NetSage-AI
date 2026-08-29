"""Form validation tests for case creation."""
from models.case import Case
from services.case_service import create_case
import pytest

def test_case_requires_symptom():
    """Test that symptom is required."""
    with pytest.raises(ValueError):
        Case(
            case_id="TEST-001",
            title="Test case",
            symptom="",  # Empty symptom
            topology="Test topology",
            show_output="show command output",
            category="Interface/Connectivity"
        )

def test_case_requires_show_output():
    """Test that show_output is required."""
    with pytest.raises(ValueError):
        Case(
            case_id="TEST-002",
            title="Test case",
            symptom="Test symptom",
            topology="Test topology",
            show_output="",  # Empty show_output
            category="Interface/Connectivity"
        )

def test_case_requires_valid_category():
    """Test that category must be valid."""
    with pytest.raises(ValueError):
        Case(
            case_id="TEST-003",
            title="Test case",
            symptom="Test symptom",
            topology="Test topology",
            show_output="show command output",
            category="InvalidCategory"  # Invalid category
        )

def test_case_with_all_required_fields():
    """Test that case is valid with all required fields."""
    case = Case(
        case_id="TEST-004",
        title="Test case",
        symptom="Test symptom",
        topology="Test topology",
        show_output="show command output",
        category="Interface/Connectivity"
    )
    assert case.case_id == "TEST-004"
    assert case.symptom == "Test symptom"
    assert case.show_output == "show command output"
    assert case.category == "Interface/Connectivity"

def test_case_supported_categories():
    """Test all supported categories."""
    from models.case import SUPPORTED_CATEGORIES
    
    for category in SUPPORTED_CATEGORIES:
        case = Case(
            case_id="TEST-005",
            title="Test case",
            symptom="Test symptom",
            topology="Test topology",
            show_output="show command output",
            category=category
        )
        assert case.category == category

def test_case_optional_topology():
    """Test that topology is optional."""
    case = Case(
        case_id="TEST-006",
        title="Test case",
        symptom="Test symptom",
        topology="",  # Empty topology is allowed
        show_output="show command output",
        category="Interface/Connectivity"
    )
    assert case.topology == ""

def test_case_severity_defaults():
    """Test that severity has default value."""
    case = Case(
        case_id="TEST-007",
        title="Test case",
        symptom="Test symptom",
        topology="Test topology",
        show_output="show command output",
        category="Interface/Connectivity"
        # severity not provided
    )
    assert case.severity == "medium"

def test_case_all_severity_levels():
    """Test all severity levels."""
    for severity in ["low", "medium", "high", "critical"]:
        case = Case(
            case_id="TEST-008",
            title="Test case",
            symptom="Test symptom",
            topology="Test topology",
            show_output="show command output",
            category="Interface/Connectivity",
            severity=severity
        )
        assert case.severity == severity

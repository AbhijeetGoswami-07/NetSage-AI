"""Database schema and operations tests."""
from database.db import connect, upsert_case, get_case, list_cases, save_diagnosis, save_review, save_verification
from models.case import Case
import json

def test_database_schema():
    """Test that all required tables exist."""
    with connect() as connection:
        names = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    
    required_tables = {
        'cases',
        'diagnoses', 
        'reviews',
        'verifications',
        'responsible_ai_logs',
        'rule_results'
    }
    assert required_tables <= names, f"Missing tables: {required_tables - names}"

def test_case_persistence():
    """Test that cases are properly persisted."""
    case_data = {
        'case_id': 'TEST-CASE-001',
        'title': 'Test case',
        'symptom': 'Test symptom',
        'topology': 'Test topology',
        'show_output': 'show interfaces',
        'category': 'Interface/Connectivity',
        'severity': 'high'
    }
    
    # Save case
    upsert_case(case_data)
    
    # Retrieve case
    retrieved = get_case('TEST-CASE-001')
    assert retrieved is not None
    assert retrieved['symptom'] == 'Test symptom'
    assert retrieved['case_id'] == 'TEST-CASE-001'

def test_case_upsert():
    """Test that upsert updates existing cases."""
    case_data = {
        'case_id': 'TEST-CASE-002',
        'title': 'Original title',
        'symptom': 'Original symptom',
        'topology': 'Original topology',
        'show_output': 'show interfaces',
        'category': 'VLAN',
        'severity': 'medium'
    }
    
    # First insert
    upsert_case(case_data)
    original = get_case('TEST-CASE-002')
    assert original['title'] == 'Original title'
    
    # Update with upsert
    case_data['title'] = 'Updated title'
    upsert_case(case_data)
    updated = get_case('TEST-CASE-002')
    assert updated['title'] == 'Updated title'

def test_diagnosis_persistence():
    """Test that diagnoses are properly persisted."""
    # First create a case
    case_data = {
        'case_id': 'TEST-CASE-003',
        'title': 'Test',
        'symptom': 'Test',
        'topology': '',
        'show_output': 'Test',
        'category': 'Interface/Connectivity',
        'severity': 'medium'
    }
    upsert_case(case_data)
    
    # Save diagnosis
    diagnosis_data = {
        'root_cause': 'Test root cause',
        'osi_layer': 'L2',
        'confidence': 85,
        'evidence': ['Evidence 1', 'Evidence 2'],
        'next_command': 'show version',
        'fix_steps': ['Step 1', 'Step 2'],
        'category': 'Interface/Connectivity',
        'severity': 'medium'
    }
    
    diagnosis_id = save_diagnosis('TEST-CASE-003', diagnosis_data, 'DEMO')
    assert diagnosis_id > 0

def test_review_persistence():
    """Test that reviews are properly persisted."""
    # Create case and diagnosis first
    case_data = {
        'case_id': 'TEST-CASE-004',
        'title': 'Test',
        'symptom': 'Test',
        'topology': '',
        'show_output': 'Test',
        'category': 'Interface/Connectivity',
        'severity': 'medium'
    }
    upsert_case(case_data)
    
    diagnosis_data = {
        'root_cause': 'Test root cause',
        'osi_layer': 'L2',
        'confidence': 85,
        'evidence': ['Evidence'],
        'next_command': 'show version',
        'fix_steps': ['Step 1'],
        'category': 'Interface/Connectivity',
        'severity': 'medium'
    }
    diagnosis_id = save_diagnosis('TEST-CASE-004', diagnosis_data, 'DEMO')
    
    # Save review
    review_data = {
        'diagnosis_id': diagnosis_id,
        'decision': 'ACCEPT',
        'edited_diagnosis': None,
        'reviewer_comment': 'Looks good'
    }
    save_review(review_data)
    
    # Verify review was saved
    with connect() as db:
        review = db.execute("SELECT * FROM reviews WHERE diagnosis_id = ?", (diagnosis_id,)).fetchone()
        assert review is not None
        assert review['decision'] == 'ACCEPT'

def test_verification_persistence():
    """Test that verifications are properly persisted."""
    # Create case
    case_data = {
        'case_id': 'TEST-CASE-005',
        'title': 'Test',
        'symptom': 'Test',
        'topology': '',
        'show_output': 'Test',
        'category': 'Interface/Connectivity',
        'severity': 'medium'
    }
    upsert_case(case_data)
    
    # Save verification
    verification_data = {
        'case_id': 'TEST-CASE-005',
        'status': 'VERIFIED',
        'before_result': 'PING FAILED',
        'after_result': 'PING SUCCESS',
        'verification_notes': 'Test notes'
    }
    save_verification(verification_data)
    
    # Verify verification was saved
    with connect() as db:
        verification = db.execute("SELECT * FROM verifications WHERE case_id = ?", ('TEST-CASE-005',)).fetchone()
        assert verification is not None
        assert verification['status'] == 'VERIFIED'

def test_list_cases_filtering():
    """Test case filtering in list_cases."""
    # Create test cases
    cases = [
        {
            'case_id': 'FILTER-001',
            'title': 'Interface issue',
            'symptom': 'No connectivity',
            'topology': '',
            'show_output': 'show interfaces',
            'category': 'Interface/Connectivity',
            'severity': 'high'
        },
        {
            'case_id': 'FILTER-002',
            'title': 'VLAN issue',
            'symptom': 'VLAN not working',
            'topology': '',
            'show_output': 'show vlan',
            'category': 'VLAN',
            'severity': 'medium'
        }
    ]
    
    for case in cases:
        upsert_case(case)
    
    # Test search
    results = list_cases(search='Interface')
    assert any(r['case_id'] == 'FILTER-001' for r in results)
    
    # Test category filter
    results = list_cases(category='VLAN')
    assert any(r['case_id'] == 'FILTER-002' for r in results)
    
    # Test severity filter
    results = list_cases(severity='high')
    assert any(r['case_id'] == 'FILTER-001' for r in results)

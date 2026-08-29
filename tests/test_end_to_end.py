"""End-to-end workflow tests."""
from models.verification import calculate_status
from models.review import Review
from services.classification_service import classify
from rules.rule_engine import run_rules

def test_end_to_end_core_workflow():
    """Test core workflow: rules → classification → verification."""
    output = 'Gi0/1 192.168.1.10 YES manual up up\nGi0/2 192.168.1.10 YES manual up up'
    rules = run_rules(output)
    assert rules and rules[0]['status'] == 'FAIL'
    assert classify('duplicate address', output) == 'Interface/Connectivity'
    assert calculate_status('PING FAILED', 'PING SUCCESS') == 'VERIFIED'

def test_review_accept_workflow():
    """Test ACCEPT review decision."""
    review = Review(
        diagnosis_id=1,
        decision='ACCEPT',
        reviewer_comment='Diagnosis accepted'
    )
    assert review.decision == 'ACCEPT'

def test_review_edit_workflow():
    """Test EDIT review decision with corrected information."""
    edited = {
        'root_cause': 'Corrected root cause',
        'confidence': 90
    }
    review = Review(
        diagnosis_id=1,
        decision='EDIT',
        edited_diagnosis=edited,
        reviewer_comment='Corrected after manual review'
    )
    assert review.decision == 'EDIT'
    assert review.edited_diagnosis == edited

def test_review_reject_workflow():
    """Test REJECT review decision."""
    review = Review(
        diagnosis_id=1,
        decision='REJECT',
        reviewer_comment='Insufficient evidence for conclusion'
    )
    assert review.decision == 'REJECT'

def test_verification_passed_workflow():
    """Test complete verification workflow for passed fix."""
    before = 'PING FAILED'
    after = 'PING SUCCESS'
    status = calculate_status(before, after)
    assert status == 'VERIFIED'

def test_verification_failed_workflow():
    """Test complete verification workflow for failed fix."""
    before = 'INTERFACE DOWN'
    after = 'INTERFACE DOWN'
    status = calculate_status(before, after)
    assert status == 'FAILED'

def test_verification_inconclusive_workflow():
    """Test complete verification workflow for inconclusive result."""
    before = 'unknown'
    after = 'unknown'
    status = calculate_status(before, after)
    assert status == 'INCONCLUSIVE'

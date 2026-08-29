from models.review import Review
import pytest

def test_edit_requires_comment_at_model_boundary():
    """Test that EDIT decisions can have comments at model level."""
    review = Review(diagnosis_id=1, decision='EDIT', reviewer_comment='Evidence corrected the root cause')
    assert review.decision == 'EDIT'
    assert review.reviewer_comment == 'Evidence corrected the root cause'

def test_accept_with_optional_comment():
    """Test that ACCEPT decisions allow empty comments at model level."""
    review = Review(diagnosis_id=1, decision='ACCEPT', reviewer_comment='')
    assert review.decision == 'ACCEPT'
    assert review.reviewer_comment == ''

def test_reject_with_required_comment():
    """Test that REJECT decisions can have comments at model level."""
    review = Review(diagnosis_id=1, decision='REJECT', reviewer_comment='Evidence is insufficient.')
    assert review.decision == 'REJECT'
    assert review.reviewer_comment == 'Evidence is insufficient.'

def test_all_decision_types():
    """Test all three decision types."""
    for decision in ['ACCEPT', 'EDIT', 'REJECT']:
        review = Review(diagnosis_id=1, decision=decision, reviewer_comment='Test comment')
        assert review.decision == decision

def test_edited_diagnosis_preserved():
    """Test that edited diagnosis is preserved."""
    edited = {'root_cause': 'New root cause', 'confidence': 85}
    review = Review(diagnosis_id=1, decision='EDIT', edited_diagnosis=edited, reviewer_comment='Changed')
    assert review.edited_diagnosis == edited

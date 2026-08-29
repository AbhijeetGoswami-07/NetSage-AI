import json
from models.diagnosis import Diagnosis
from ai.fallback_diagnosis import fallback_diagnosis

def test_diagnosis_validation():
    diagnosis=Diagnosis(root_cause='wrong VLAN',osi_layer='L2',confidence=90,evidence=['line'],next_command='show vlan brief',fix_steps=['review'],category='VLAN',severity='high')
    assert diagnosis.confidence == 90

def test_local_demo_is_labelled():
    result=fallback_diagnosis({'category':'Routing','osi_layer':'L3','severity':'medium'},[])
    assert result.confidence < 50

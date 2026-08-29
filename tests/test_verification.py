from models.verification import calculate_status

def test_verification_states():
    """Test basic verification status calculations."""
    assert calculate_status('PING FAILED', 'PING SUCCESS') == 'VERIFIED'
    assert calculate_status('PING FAILED', 'PING FAILED') == 'FAILED'
    assert calculate_status('unknown', 'unknown') == 'INCONCLUSIVE'

def test_verification_typo_normalization():
    """Test that common typos are normalized correctly."""
    # SUCCSE → SUCCESS → VERIFIED
    assert calculate_status('PING FAILED', 'PING SUCCSE') == 'VERIFIED'
    # SUCCES → SUCCESS → VERIFIED
    assert calculate_status('TEST FAILED', 'TEST SUCCES') == 'VERIFIED'
    # SUCESS → SUCCESS → VERIFIED
    assert calculate_status('CHECK FAILED', 'CHECK SUCESS') == 'VERIFIED'
    # FAILE → FAILED → FAILED
    assert calculate_status('PING SUCCESS', 'PING FAILE') == 'FAILED'
    # FAILD → FAILED → FAILED
    assert calculate_status('TEST SUCCESS', 'TEST FAILD') == 'FAILED'

def test_verification_case_insensitivity():
    """Test that verification is case-insensitive."""
    assert calculate_status('PING FAILED', 'ping success') == 'VERIFIED'
    assert calculate_status('PING FAILED', 'PING Success') == 'VERIFIED'
    assert calculate_status('PING FAILED', 'ping failed') == 'FAILED'

def test_verification_keyword_detection():
    """Test that verification detects keywords correctly."""
    # SUCCESS keyword
    assert calculate_status('FAILED', 'HTTP SUCCESS') == 'VERIFIED'
    # PASS keyword
    assert calculate_status('FAILED', 'TEST PASS') == 'VERIFIED'
    # UP keyword
    assert calculate_status('DOWN', 'Interface UP') == 'VERIFIED'
    # FAILED keyword
    assert calculate_status('PASSED', 'Connection FAILED') == 'FAILED'
    # FAIL keyword
    assert calculate_status('PASSED', 'Test FAIL') == 'FAILED'
    # DOWN keyword
    assert calculate_status('UP', 'Interface DOWN') == 'FAILED'

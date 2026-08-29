from services.classification_service import classify

def test_classification():
    assert classify('clients cannot obtain addresses','show ip dhcp binding') == 'DHCP'

def test_bad_category():
    try: classify('x','y','Unsupported')
    except ValueError: pass
    else: assert False

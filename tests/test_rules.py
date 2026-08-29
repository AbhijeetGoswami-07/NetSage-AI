from rules.rule_engine import run_rules

def test_duplicate_ip():
    text='Gi0/1 192.168.1.10 YES manual up up\nGi0/2 192.168.1.10 YES manual up up'
    results=run_rules(text)
    assert results[0]['rule_name']=='duplicate_ip' and results[0]['status']=='FAIL'

def test_missing_vlan():
    results=run_rules('show vlan brief\n10 USERS active\nAccess Mode VLAN: 20')
    assert any(item['rule_name']=='missing_vlan' for item in results)

def test_acl_and_interface():
    results=run_rules('Gi0/1 administratively down\n10 deny tcp any host 10.0.0.1 eq 443')
    assert {item['rule_name'] for item in results} >= {'interface_status','acl_deny'}

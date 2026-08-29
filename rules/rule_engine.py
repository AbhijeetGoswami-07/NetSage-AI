"""Structured deterministic checks for untrusted Cisco text."""
import ipaddress, re

def finding(rule_name: str, status: str, severity: str, text: str, evidence: str = "", recommendation: str = "") -> dict:
    """Build a stable rule result."""
    return {"rule_name":rule_name,"status":status,"severity":severity,"finding":text,"evidence":evidence,"recommendation":recommendation}
def run_rules(show_output: str, category: str = "Interface/Connectivity", required_networks: list[str] | None = None) -> list[dict]:
    """Run checks only when their evidence is present."""
    lines = show_output.splitlines(); results=[]
    ip_lines=[]
    for line in lines:
        match=re.search(r"^(\S+)\s+(\d+(?:\.\d+){3})\s+", line.strip())
        if match: ip_lines.append((match.group(1),match.group(2)))
    addresses={ip:[name for name,address in ip_lines if address==ip] for _,ip in ip_lines}
    for ip,names in addresses.items():
        if len(names)>1: results.append(finding("duplicate_ip","FAIL","high",f"IP {ip} appears on {', '.join(names)}",ip,"Assign unique host addresses."))
        try: ipaddress.ip_address(ip)
        except ValueError: results.append(finding("invalid_ip","FAIL","high",f"IP {ip} is not valid IPv4",ip,"Correct the interface address after human review."))
    gateway_match=re.search(r"(?:gateway|default-router)\s*[:=]?\s*(\d+(?:\.\d+){3})",show_output,re.I)
    host_match=re.search(r"(?:IP|address)\s*[:=]?\s*(\d+(?:\.\d+){3})\s+(?:mask\s+)?(\d+(?:\.\d+){3})",show_output,re.I)
    if gateway_match and host_match:
        try:
            network=ipaddress.ip_network(f"{host_match.group(1)}/{host_match.group(2)}",strict=False)
            if ipaddress.ip_address(gateway_match.group(1)) not in network: results.append(finding("gateway_mismatch","FAIL","high",f"Gateway {gateway_match.group(1)} is outside host subnet {network}",gateway_match.group(0),"Use a gateway in the host subnet."))
        except ValueError: results.append(finding("invalid_subnet","FAIL","high","Host address or subnet mask is invalid",host_match.group(0),"Correct the IPv4 address and mask."))
    if re.search(r"\b(?:up|down)\s+down\b|administratively down", show_output, re.I): results.append(finding("interface_status","FAIL","high","An interface is administratively or operationally down", next(line.strip() for line in lines if re.search(r"down",line,re.I)),"Check cabling, shutdown state, and the remote endpoint."))
    vlan_ids=set(re.findall(r"^\s*(\d+)\s+\S+\s+(?:active|act/lshut)",show_output,re.I|re.M)); assigned=set(re.findall(r"(?:Access Mode VLAN|access vlan)\s*:?\s*(\d+)",show_output,re.I))
    for vlan in assigned-vlan_ids: results.append(finding("missing_vlan","FAIL","high",f"Access VLAN {vlan} is assigned but not listed as active",vlan,"Create/activate the intended VLAN after human review."))
    if "show ip route" in show_output.lower() or re.search(r"(?:^|\n)[CSRBO*]+\s+\d+\.\d+\.\d+\.\d+",show_output):
        if not re.search(r"(?:S\*|O\*|B\*)\s+0\.0\.0\.0/0|Gateway of last resort",show_output): results.append(finding("missing_default_route","WARNING","medium","No default route is visible","show ip route","Verify the routing design and next hop."))
        for network in required_networks or []:
            if network not in show_output: results.append(finding("missing_route","FAIL","medium",f"Required network {network} is absent","show ip route","Add or learn the required route after review."))
    if re.search(r"deny\s+tcp.*eq\s+443|deny\s+ip",show_output,re.I): results.append(finding("acl_deny","FAIL","high","An ACL deny may block the reported flow",next(line.strip() for line in lines if re.search(r"deny\s+",line,re.I)),"Confirm direction and scope before editing the ACL."))
    if re.search(r"show .*dhcp|ip dhcp|dhcp",show_output,re.I) and re.search(r"Bindings from all pools: none|pool.*exhaust|no ip helper",show_output,re.I): results.append(finding("dhcp_configuration","WARNING","medium","DHCP evidence indicates no lease, exhaustion, or missing relay",next(line.strip() for line in lines if re.search(r"none|exhaust|helper",line,re.I)),"Verify pool scope, exclusions, and relay configuration."))
    if re.search(r"dns|name-server",show_output,re.I) and re.search(r"timeout|unreachable|temporary failure",show_output,re.I): results.append(finding("dns_configuration","FAIL","medium","Configured DNS service is unreachable",next(line.strip() for line in lines if re.search(r"timeout|unreachable|failure",line,re.I)),"Verify DNS reachability and resolver configuration."))
    if re.search(r"nat",show_output,re.I) and re.search(r"translations.*none|hits\s+0|no ip nat outside",show_output,re.I): results.append(finding("nat_translation","WARNING","medium","NAT evidence shows no matching translations",next(line.strip() for line in lines if re.search(r"none|hits|outside",line,re.I)),"Verify inside/outside roles and translation policy."))
    if not results: results.append(finding("evidence_coverage","NOT_CHECKED","low","No applicable deterministic fault was established","","Collect the next command requested by the diagnosis."))
    return results

# Responsible AI Log

This log records where NetSage AI was corrected by a human. It keeps the system auditable and makes recurring model errors visible. Replace these examples with real cases after running the system, and keep at least five reviewed corrections.

| case_id | AI diagnosis summary | Human correction | Why AI was wrong |
|---|---|---|---|
| CASE-001 | Host is down at Layer 1 | Port was in the wrong VLAN, Layer 2 | Model over-weighted the symptom and ignored switchport evidence. |
| CASE-002 | DHCP server is unreachable | DHCP pool used the wrong subnet, Layer 3 | Model failed to compare the interface and pool networks. |
| CASE-003 | Cable failure between routers | Missing route to the remote LAN, Layer 3 | Model treated lack of a route as a physical failure. |
| CASE-004 | Server application is down | ACL denied TCP/443, Layer 4 | Model ignored the explicit deny line in the ACL. |
| CASE-005 | NAT translation collision | Duplicate host IPs caused ARP instability, Layer 3 | Model classified the concept tag instead of reading duplicate addresses. |

For each real review, record the original AI output, the accepted/edit/rejected decision, the corrected fault, and the evidence that settled the decision. A human must review every diagnosis before a configuration change is applied.

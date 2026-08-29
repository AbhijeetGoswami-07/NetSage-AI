"""Deterministic checks for common Cisco lab configuration mistakes."""
import csv
import ipaddress
import re
from pathlib import Path
from .config import DATA_DIR, RESULTS_DIR
from .models import CaseRecord


def check_duplicate_ips(show_outputs: str) -> list[str]:
    """Find repeated IPv4 addresses on interface-looking lines."""
    found: dict[str, list[str]] = {}
    for line in show_outputs.splitlines():
        match = re.search(r"^(\S+)\s+(\d{1,3}(?:\.\d{1,3}){3})\s+", line.strip())
        if match:
            found.setdefault(match.group(2), []).append(match.group(1))
    return [f"IP {address} appears on interfaces: {', '.join(interfaces)}" for address, interfaces in found.items() if len(interfaces) > 1]


def check_gateway_mismatch(show_outputs: str, expected_gateway: str | None = None) -> list[str]:
    """Check a stated gateway against a stated host IP and mask."""
    ips = re.findall(r"(?:host IP|IP address|IPv4 address)\s*[:=]?\s*(\d+(?:\.\d+){3})\s*(?:/|mask\s+)?(\d+(?:\.\d+){3})?", show_outputs, re.I)
    gateway_match = re.search(r"(?:default gateway|gateway)\s*[:=]?\s*(\d+(?:\.\d+){3})", show_outputs, re.I)
    gateway = expected_gateway or (gateway_match.group(1) if gateway_match else None)
    if not gateway or not ips:
        return []
    host, mask = ips[0]
    try:
        network = ipaddress.ip_network(f"{host}/{mask or 24}", strict=False)
        if ipaddress.ip_address(gateway) not in network:
            return [f"Gateway {gateway} is outside host subnet {network}." ]
    except ValueError:
        return ["Host IP, mask, or gateway is not valid IPv4 data."]
    return []


def check_interface_down(show_outputs: str) -> list[str]:
    """Find interfaces marked administratively down or down/down."""
    issues = []
    for line in show_outputs.splitlines():
        if re.search(r"administratively down|\bdown\s+down\b", line, re.I):
            issues.append(f"Interface may be unavailable: {line.strip()}")
    return issues


def check_missing_vlan(show_outputs: str) -> list[str]:
    """Compare access VLAN IDs with VLAN IDs listed in show vlan output."""
    present = set(re.findall(r"^\s*(\d+)\s+\S+\s+(?:active|act/lshut)", show_outputs, re.I | re.M))
    assigned = set(re.findall(r"(?:Access Mode VLAN|access vlan)\s*:?\s*(\d+)", show_outputs, re.I))
    return [f"Access VLAN {vlan} is assigned but is absent from show vlan output." for vlan in sorted(assigned - present, key=int)]


def check_missing_routes(show_outputs: str, required_networks: list[str] | None = None) -> list[str]:
    """Detect a missing default route and optionally missing required networks."""
    issues = []
    if required_networks is None:
        required_networks = []
    has_default = bool(re.search(r"(?:S\*|O\*|B\*)\s+0\.0\.0\.0/0|Gateway of last resort", show_outputs))
    if "0.0.0.0/0" not in required_networks and not has_default:
        issues.append("No default route was found in show ip route output.")
    for network in required_networks:
        if network != "0.0.0.0/0" and network not in show_outputs:
            issues.append(f"Required network {network} is missing from the routing table.")
    return issues


def run_all_rule_checks(case: CaseRecord) -> dict[str, list[str]]:
    """Run every deterministic check for one case."""
    return {"duplicate_ips": check_duplicate_ips(case.show_outputs), "gateway_mismatch": check_gateway_mismatch(case.show_outputs),
            "interface_down": check_interface_down(case.show_outputs), "missing_vlan": check_missing_vlan(case.show_outputs),
            "missing_routes": check_missing_routes(case.show_outputs)}


def _load_cases(path: Path = DATA_DIR / "cases.csv") -> list[CaseRecord]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [CaseRecord.model_validate(row) for row in csv.DictReader(handle)]

if __name__ == "__main__":
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = []
    for case in _load_cases():
        checks = run_all_rule_checks(case)
        rows.append({"case_id": case.case_id, "check": name, "issues": " | ".join(items)} for name, items in checks.items())
    flattened = [row for group in rows for row in group]
    with (RESULTS_DIR / "rule_check_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id", "check", "issues"]); writer.writeheader(); writer.writerows(flattened)
    print(f"Wrote {len(flattened)} rule-check rows to {RESULTS_DIR / 'rule_check_report.csv'}")

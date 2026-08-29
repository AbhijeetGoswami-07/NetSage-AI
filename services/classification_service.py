"""Network category classification."""
from models.case import SUPPORTED_CATEGORIES

def classify(symptom: str, show_output: str, requested: str | None = None) -> str:
    """Return a supported category based on explicit category or evidence keywords."""
    if requested:
        if requested not in SUPPORTED_CATEGORIES: raise ValueError(f"Unsupported category: {requested}")
        return requested
    text=(symptom+" "+show_output).lower(); terms=[("VLAN",["vlan"]),("DHCP",["dhcp"]),("DNS",["dns"]),("Routing",["route","routing"]),("ACL",["acl","access-list"]),("NAT",["nat"]),("Wireless",["wireless","ssid"]),("Default Gateway",["gateway"])]
    return next((category for category, words in terms if any(word in text for word in words)), "Interface/Connectivity")

"""Case lifecycle service."""
import csv
from database import db
from models.case import Case

def initialize() -> int:
    """Initialize schema and seed CSV cases idempotently."""
    with db.connect(): pass
    path=db.ROOT/"data"/"cases.csv"
    if not path.exists(): return 0
    with path.open(newline="",encoding="utf-8") as handle:
        rows=list(csv.DictReader(handle))
    for row in rows:
        raw_category=row.get("category") or row.get("concept_tag","Interface/Connectivity")
        category_alias={"routing":"Routing","dns":"DNS","dhcp":"DHCP","acl":"ACL","nat":"NAT","vlan":"VLAN","wireless":"Wireless"}
        row={"case_id":row.get("case_id",""),"title":row.get("title") or row.get("symptom","Untitled")[:80],"symptom":row.get("symptom",""),"topology":row.get("topology") or row.get("topology_note",""),"show_output":row.get("show_output") or row.get("show_outputs",""),"expected_fault":row.get("expected_fault",""),"osi_layer":row.get("osi_layer","Unknown"),"concept":row.get("concept") or row.get("concept_tag",""),"severity":row.get("severity","medium"),"category":category_alias.get(raw_category.lower(),raw_category)}
        try: db.upsert_case(Case.model_validate(row).model_dump())
        except ValueError: continue
    return len(rows)

def create_case(data: dict) -> str:
    """Validate and save a new case."""
    case=Case.model_validate(data); db.upsert_case(case.model_dump()); return case.case_id

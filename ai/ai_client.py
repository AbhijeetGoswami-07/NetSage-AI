"""Live AI client with safe fallback."""
import json, os, requests
from dotenv import load_dotenv
from models.diagnosis import Diagnosis
from .fallback_diagnosis import fallback_diagnosis
from .prompt_builder import build_prompt
load_dotenv()
class AIClientError(RuntimeError): pass

def diagnose(case: dict, rules: list[dict]) -> tuple[Diagnosis, str]:
    """Return a validated live diagnosis or an explicitly labelled local one."""
    key=os.getenv("AI_API_KEY") or os.getenv("LLM_API_KEY", "")
    if not key or key == "your_key_here": return fallback_diagnosis(case, rules), "LOCAL DEMO"
    base=(os.getenv("AI_API_BASE_URL") or os.getenv("LLM_API_BASE_URL", "https://api.openai.com/v1")).rstrip("/")
    model=os.getenv("AI_MODEL") or os.getenv("LLM_MODEL", "gpt-4o-mini")
    payload={"model":model,"temperature":0.2,"response_format":{"type":"json_object"},"messages":[{"role":"user","content":build_prompt(case,rules)}]}
    try:
        response=requests.post(base+"/chat/completions",headers={"Authorization":f"Bearer {key}"},json=payload,timeout=30); response.raise_for_status()
        raw=response.json()["choices"][0]["message"]["content"]; return Diagnosis.model_validate(json.loads(raw)), "LIVE AI"
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as exc:
        return fallback_diagnosis(case, rules), f"LOCAL DEMO (AI error: {type(exc).__name__})"

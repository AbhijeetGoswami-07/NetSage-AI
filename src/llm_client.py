"""OpenAI-compatible LLM client with structured response validation."""
import json
import logging
from typing import Any
import requests
from pydantic import ValidationError
from .config import PROMPTS_DIR, get_llm_config
from .models import DiagnosisOutput

LOGGER = logging.getLogger(__name__)

class LLMResponseError(RuntimeError):
    """Raised when the provider response cannot be used as a diagnosis."""


def _extract_content(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMResponseError("LLM response did not contain message content") from exc


def run_diagnosis_prompt(symptom: str, topology_note: str, show_outputs: str, prompt_template: str | None = None) -> DiagnosisOutput:
    """Call the configured LLM and validate its JSON diagnosis with Pydantic."""
    config = get_llm_config()
    template = prompt_template or (PROMPTS_DIR / "diagnose_prompt.md").read_text(encoding="utf-8")
    user_message = (template.replace("{symptom}", symptom)
                    .replace("{topology_note}", topology_note)
                    .replace("{show_outputs}", show_outputs))
    body = {"model": config["model"], "temperature": 0.2, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": user_message}]}
    headers = {"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"}
    response = None
    raw = ""
    for attempt in range(2):
        try:
            response = requests.post(f"{config['base_url']}/chat/completions", headers=headers, json=body, timeout=45)
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            if attempt == 1:
                raise LLMResponseError(f"LLM request failed after retry: {exc}") from exc
            LOGGER.warning("LLM request failed; retrying once: %s", exc)
    try:
        raw = _extract_content(response.json())
        return DiagnosisOutput.model_validate(json.loads(raw))
    except (ValueError, json.JSONDecodeError) as exc:
        raise LLMResponseError(f"LLM returned invalid JSON: {raw[:500]}") from exc
    except ValidationError as exc:
        raise LLMResponseError(f"LLM JSON failed schema validation: {exc}") from exc

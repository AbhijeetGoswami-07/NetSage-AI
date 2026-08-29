"""Project paths and environment configuration."""
from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_DIR = PROJECT_ROOT / "output"
load_dotenv(PROJECT_ROOT / ".env")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def get_llm_config() -> dict[str, str]:
    """Return LLM settings, raising a clear error when the API key is absent."""
    if not LLM_API_KEY or LLM_API_KEY == "your_key_here":
        raise RuntimeError("LLM_API_KEY is missing; copy .env.example to .env and set it.")
    return {"api_key": LLM_API_KEY, "base_url": LLM_API_BASE_URL.rstrip("/"), "model": LLM_MODEL}

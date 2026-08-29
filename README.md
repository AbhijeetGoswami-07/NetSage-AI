# NetSage AI

An evidence-backed Cisco lab troubleshooting assistant with a Streamlit UI, SQLite history, deterministic checks, optional live AI, human review, and user-entered verification.

## Prerequisites

- Python 3.11+
- VS Code with the Python and Jupyter extensions
- An API key for an OpenAI-compatible chat-completions provider

## Setup

1. Open `netsage_ai` in VS Code.
2. Create a virtual environment: `python -m venv .venv`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and optionally fill in `AI_API_KEY`, `AI_API_BASE_URL`, and `AI_MODEL`.
5. Select the `.venv` interpreter in VS Code.

The supplied `data/cases.csv` contains 40 cases. Keep the required columns and quote multiline show output values when extending it.

## Run

```powershell
python -m streamlit run app.py
pytest -q
```

The database initializes from the CSV on first launch. The rule checker is deterministic, and missing AI credentials select clearly labelled local demo mode. The dashboard uses SQLite data; Streamlit pages cover new troubleshooting, case search/filter/export, review, verification, and responsible AI.

## Human review

Every diagnosis must be reviewed in the app. Reviews are stored in SQLite; the legacy CSV format is:

`case_id,ai_root_cause,human_decision,human_corrected_fault,notes`

Use `ACCEPT`, `EDIT`, or `REJECT` in the app. EDIT and REJECT require a comment. Never apply a suggested fix without reviewing its evidence and verifying the result in Packet Tracer.

## Responsible AI

Five seed correction examples are provided in `logs/responsible_ai.csv`; real corrections are persisted in SQLite and displayed on the Responsible AI page. See [docs/responsible_ai_log.md](docs/responsible_ai_log.md).

## Demo video

For a 5–10 minute demo, show a broken Packet Tracer lab, copy its symptom and `show` outputs, run the diagnosis for the case, inspect the JSON evidence, record the human review decision, apply the approved fix, and verify connectivity.

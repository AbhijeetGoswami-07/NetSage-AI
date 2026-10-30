# 🛰️ NetSage AI — Evidence-Backed Network Troubleshooting Assistant

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework Streamlit](https://img.shields.io/badge/Framework-Streamlit%201.36%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Database SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests Pytest](https://img.shields.io/badge/Tests-42%20Passed-10b981.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **NetSage AI** is an intelligent, evidence-grounded Cisco network troubleshooting platform. It eliminates AI hallucinations by combining a **deterministic algorithmic rule engine**, **quoted Cisco CLI evidence citations**, a **mandatory human-in-the-loop review gate**, and **automated field verification tracking**.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [How It Works (5-Stage Architecture)](#-how-it-works-5-stage-architecture)
- [Real-World Use Cases](#-real-world-use-cases)
- [Quick Start & How to Run](#-quick-start--how-to-run)
  - [Method 1: One-Click Launchers (Windows)](#method-1-one-click-launchers-windows)
  - [Method 2: Manual Terminal Setup](#method-2-manual-terminal-setup)
- [Configuration & Environment Variables](#-configuration--environment-variables)
- [Project Directory Structure](#-project-directory-structure)
- [Automated Testing](#-automated-testing)
- [Responsible AI & Audit Trail](#-responsible-ai--audit-trail)
- [License & Contributing](#-license--contributing)

---

## 🔍 Overview

When network outages strike, engineers and students often spend hours digging through complex Cisco command logs. While generic AI chatbots can answer theory questions, they frequently **hallucinate commands**, **miss protocol-specific nuances**, and **lack accountability**.

**NetSage AI** bridges this gap:
- Diagnoses are strictly tied to line-by-line evidence from Cisco `show` command outputs.
- 10 specialized deterministic rule checkers validate standard Cisco best practices before AI inference runs.
- Every diagnosis requires human engineering approval (`ACCEPT`, `EDIT`, or `REJECT`) before any fix is deployed.
- Operates in **100% offline Local Demo Mode** (zero cost) or connects to OpenAI-compatible LLMs for **Live AI Mode**.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **📑 Evidence-Backed Root Cause** | Identifies exact misconfigurations with cited lines from Cisco CLI output. |
| **⚙️ 10 Deterministic Rule Engines** | Validates native VLAN trunk mismatches, OSPF MTU conflicts, IP/ARP flapping, ACL ordering, and interface speed/duplex states. |
| **⚡ 1-Click Diagnostic Presets** | Pre-loaded real-world scenarios (VLAN Mismatch, OSPF EXSTART, Duplicate IP, ACL Denials) to test the app in one click. |
| **👤 Human-in-the-Loop Review Gate** | Mandatory audit step ensuring every diagnosis is validated or corrected by a human engineer. |
| **🧪 Automated Verification Tracker** | Evaluates pre-fix failure states against post-fix test states and calculates outcomes: `PASSED`, `FAILED`, or `INCONCLUSIVE`. |
| **⚖️ Responsible AI Ledger** | Records human feedback, reasons for corrections, and engineering lessons learned in SQLite to track model accuracy over time. |
| **📊 Executive Telemetry Dashboard** | High-tech visual analytics displaying incident distribution across network layers, agreement rates, and recent cases. |
| **💻 Cisco CLI Command Runbooks** | Displays next diagnostic steps and configuration fix commands inside terminal window interfaces. |

---

## 🔄 How It Works (5-Stage Architecture)

```
┌───────────────────────┐
│ 1. Capture Evidence   │  Paste symptoms & Cisco show command outputs
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 2. AI & Rule Engine   │  Deterministic rule evaluation + AI diagnostic reasoning
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 3. Human Review Gate  │  Engineer approves [ACCEPT], modifies [EDIT], or rejects [REJECT]
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 4. Field Verification │  Execute fix in Packet Tracer / hardware & record before/after tests
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 5. Responsible Audit  │  Outcome & lessons learned persisted to SQLite knowledge base
└───────────────────────┘
```

---

## 🎯 Real-World Use Cases

- **Cisco CCNA / CCNP / CCIE Students**: Troubleshoot Packet Tracer, GNS3, or EVE-NG lab topologies with step-by-step guidance.
- **Network Operations Centers (NOC)**: Rapidly parse device logs and `show` command dumps during critical outages.
- **Enterprise Network Engineers**: Maintain an auditable incident repository and cross-verify complex multi-vendor routing/VLAN configurations.
- **Networking Instructors**: Teach students systematic troubleshooting methodology and responsible AI auditing.

---

## 🚀 Quick Start & How to Run

### Prerequisites
- **Python 3.11+** installed on your system.
- Web browser (Chrome, Edge, Firefox).

---

### Method 1: One-Click Launchers (Windows)

The repository includes ready-to-run launchers in the root folder:

1. **Direct Launch**:
   - Double-click **`run.bat`** or **`start.bat`**.
   - The launcher activates the virtual environment, starts Streamlit, and automatically opens your browser to:
     👉 **`http://localhost:8501`**

2. **PowerShell Launch**:
   - Right-click **`run.ps1`** and choose **Run with PowerShell**, or execute:
     ```powershell
     .\run.ps1
     ```

3. **Run All Tests**:
   - Double-click **`run_tests.bat`** to execute the complete 42-case test suite.

---

### Method 2: Manual Terminal Setup

```powershell
# 1. Clone the repository
git clone https://github.com/AbhijeetGoswami-07/NetSage-AI.git
cd NetSage-AI

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows Command Prompt:
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Initialize & seed SQLite database (40 cases)
python -m database.seed_database

# 6. Launch the Streamlit application
streamlit run app.py
```

The web dashboard will start at: **`http://localhost:8501`**

---

## ⚙️ Configuration & Environment Variables

Copy `.env.example` to `.env` (or use the pre-generated `.env`):

```env
# NetSage AI Environment Configuration
# Leave AI_API_KEY blank to operate in 100% offline DETERMINISTIC LOCAL DEMO MODE.
AI_API_KEY=
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o
```

- **Local Demo Mode**: If `AI_API_KEY` is omitted or empty, NetSage AI operates completely offline using deterministic rules and local fallback diagnosis. Zero cost, no internet required.
- **Live AI Mode**: Set your API key from OpenAI or any OpenAI-compatible provider (e.g., DeepSeek, Together, Groq, Ollama) for live generative inference.

---

## 📁 Project Directory Structure

```
NetSage-AI/
│
├── app.py                      # Main Streamlit web application & modern SaaS UI
├── requirements.txt            # Python dependencies (pinned to stable versions)
├── run.bat / start.bat         # 1-Click Windows Command Prompt launchers
├── run.ps1                     # PowerShell launcher script
├── run_tests.bat               # 1-Click Pytest runner
├── PROJECT_DETAILS.txt         # Comprehensive project manual & reference
├── README.md                   # Project documentation & guide
├── .env                        # Environment configuration
├── .env.example                # Configuration template
│
├── ai/                         # Diagnostic reasoning & AI pipeline
│   ├── ai_client.py            # Live LLM client with safe fallback
│   ├── fallback_diagnosis.py   # Deterministic local diagnosis generator
│   ├── prompt_builder.py       # Evidence-grounded JSON prompt builder
│   └── diagnosis_prompt.md     # System prompt definition
│
├── rules/                      # Deterministic Cisco rule engine
│   ├── rule_engine.py          # Core rule dispatch & evaluation engine
│   ├── acl_rules.py            # Access control list checks
│   ├── vlan_rules.py           # Native VLAN trunk & pruning checks
│   ├── routing_rules.py        # OSPF, EIGRP, and static routing checks
│   ├── ip_rules.py             # IP conflict & ARP flap checks
│   ├── interface_rules.py      # Admin down / duplex / speed mismatch checks
│   ├── gateway_rules.py        # Default gateway reachability rules
│   └── nat_rules.py            # NAT overload & pool exhaustion rules
│
├── database/                   # SQLite persistence layer
│   ├── db.py                   # Thread-safe database connections & queries
│   ├── schema.sql              # Database schema (cases, reviews, verifications)
│   └── seed_database.py        # Database seeder
│
├── data/                       # Datasets & storage
│   ├── cases.csv               # 40 pre-configured Cisco incident benchmarks
│   ├── netsage.db              # SQLite database file
│   └── seed_cases.py           # Case ingestion parser
│
├── models/                     # Pydantic data schemas
│   ├── case.py                 # Case model & category validators
│   ├── diagnosis.py            # Diagnosis response schema
│   ├── review.py               # Human review schema (ACCEPT/EDIT/REJECT)
│   └── verification.py         # Verification status calculation logic
│
├── services/                   # Core business logic services
│   ├── case_service.py         # Case creation and filtering
│   ├── diagnosis_service.py    # Rule + AI diagnostic orchestration
│   ├── review_service.py       # Human decision persistence
│   ├── verification_service.py # Pre/post fix test verification
│   └── analytics_service.py    # Metric aggregation & reporting
│
└── tests/                      # Automated Pytest suite
    ├── test_rules.py           # Rule checker unit tests
    ├── test_database.py        # SQLite schema & persistence tests
    ├── test_end_to_end.py      # Full lifecycle workflow tests
    ├── test_form_validation.py # Input validation & edge cases
    ├── test_review.py          # Human gate logic tests
    ├── test_verification.py    # Status normalization tests
    └── test_ai_output.py       # Diagnosis schema validation
```

---

## 🧪 Automated Testing

NetSage AI includes a comprehensive test suite covering all services, database interactions, rules, and edge cases:

```powershell
# Run the complete test suite
pytest -v
```

**Results**: All **42 unit and integration tests** pass with 100% success rate:
- ✅ Deterministic rule checks (MTU, VLAN, duplicate IP, ACLs)
- ✅ Database schema creation, persistence, and querying
- ✅ Form validation and required field boundary tests
- ✅ Human review workflows (`ACCEPT`, `EDIT`, `REJECT`)
- ✅ Before-and-after verification status calculation
- ✅ Analytics metrics and AI agreement percentage

---

## ⚖️ Responsible AI & Audit Trail

NetSage AI is engineered around the principle that **AI should assist, not dictate**:
1. **Auditability**: Every diagnosis is timestamped and stored in SQLite alongside the exact show-command outputs used to reach it.
2. **Accountability**: Suggested remediation steps require human approval before application.
3. **Continuous Improvement**: When an engineer edits or rejects a diagnosis, the reason and corrective lesson are saved to the **Responsible AI Audit Log** (`logs/responsible_ai.csv` & SQLite), ensuring full visibility into system behavior.

---

## 📄 License & Credits

- **Author**: [Abhijeet Goswami](https://github.com/AbhijeetGoswami-07)
- **Repository**: [AbhijeetGoswami-07/NetSage-AI](https://github.com/AbhijeetGoswami-07/NetSage-AI)
- **License**: MIT License

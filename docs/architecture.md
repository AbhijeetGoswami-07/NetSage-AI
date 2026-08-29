# Architecture

```mermaid
flowchart LR
  UI[Streamlit app] --> Services[Service layer]
  Services --> Rules[Deterministic rule engine]
  Services --> AI[Live AI or local demo]
  Services --> DB[(SQLite)]
  DB --> Analytics[Dashboard analytics]
  Services --> Review[Human review]
  Review --> Verify[User-entered verification]
```

Packet Tracer is outside the application boundary. The user copies observed symptoms and `show` output into NetSage, reviews the evidence-backed recommendation, applies any approved change manually, and enters the before/after test result. No Cisco command is executed by the app.

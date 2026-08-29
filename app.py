"""Streamlit entry point for NetSage AI - Modern SaaS Dashboard."""
import pandas as pd
import streamlit as st
from database import db
from models.case import SUPPORTED_CATEGORIES
from services.case_service import initialize, create_case
from services.diagnosis_service import analyze
from services.review_service import save as save_review
from services.verification_service import verify
from services.analytics_service import metrics

st.set_page_config(page_title="NetSage AI", page_icon="🛰️", layout="wide")


def inject_custom_css() -> None:
    """Apply subtle professional styling improvements while preserving existing design."""
    st.markdown(
        """
        <style>
        /* ============ EXISTING DARK THEME (PRESERVED) ============ */
        html, body, .stApp {
            background-color: #0f1419 !important;
            color: #e8ecf1 !important;
        }

        /* ============ SIDEBAR ============ */
        section[data-testid="stSidebar"] {
            background-color: #1a1f2e !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 1rem 0 !important;
        }

        [data-testid="stSidebarNav"] {
            padding: 0.5rem 0.75rem !important;
        }

        [data-testid="stSidebarNavLink"] {
            border-radius: 8px !important;
            margin: 0.35rem 0 !important;
            padding: 0.65rem 1rem !important;
            transition: all 0.15s ease !important;
            font-size: 0.95rem !important;
        }

        [data-testid="stSidebarNavLink"]:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-left: 3px solid #4fa3ff !important;
        }

        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: rgba(79, 163, 255, 0.15) !important;
            border: 1px solid rgba(79, 163, 255, 0.3) !important;
            border-left: 3px solid #4fa3ff !important;
        }


        /* ============ PAGE HEADERS (SUBTLE IMPROVEMENT) ============ */
        .page-header {
            background: #2a3347 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 1.5rem 1.75rem !important;
            margin-bottom: 1.5rem !important;
        }

        .page-header h1 {
            margin: 0 !important;
            color: #e8ecf1 !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
        }

        .page-header p {
            margin: 0.5rem 0 0 0 !important;
            color: #a0aec0 !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }

        /* ============ CARDS & METRICS ============ */
        .stMetric {
            background: #1e2638 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 1rem 1.25rem !important;
            transition: all 0.2s ease !important;
        }

        .stMetric:hover {
            border-color: rgba(79, 163, 255, 0.2) !important;
            background: #252f42 !important;
        }

        .stMetric label {
            color: #a0aec0 !important;
            font-size: 0.85rem !important;
        }

        .stMetric [data-testid="stMetricValue"] {
            color: #4fa3ff !important;
            font-size: 1.8rem !important;
        }

        /* ============ SECTION LABELS ============ */
        .section-label {
            color: #4fa3ff !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            margin: 1rem 0 0.5rem 0 !important;
        }

        /* ============ BUTTONS ============ */
        .stButton > button {
            background: #4fa3ff !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            transition: all 0.15s ease !important;
            min-height: 40px !important;
        }

        .stButton > button:hover {
            background: #3d8ae5 !important;
            box-shadow: 0 2px 8px rgba(79, 163, 255, 0.25) !important;
        }

        .stButton > button:active {
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }

        .stButton > button:disabled {
            opacity: 0.5 !important;
            cursor: not-allowed !important;
        }

        /* ============ FORMS & INPUTS ============ */
        .stForm {
            background: #1e2638 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > textarea {
            background: #252f42 !important;
            color: #e8ecf1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.65rem 0.85rem !important;
            font-size: 0.95rem !important;
            transition: all 0.15s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > textarea:focus {
            border-color: #4fa3ff !important;
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(79, 163, 255, 0.1) !important;
        }

        .stSelectbox select {
            background: #252f42 !important;
            color: #e8ecf1 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 0.65rem 0.85rem !important;
        }

        .stSelectbox select:focus {
            border-color: #4fa3ff !important;
        }

        /* ============ TABLES & DATAFRAMES ============ */
        .stDataFrame {
            border-radius: 8px !important;
            overflow: hidden !important;
        }

        .stDataFrame table, .stDataFrame [role="grid"] {
            background: #1e2638 !important;
            color: #e8ecf1 !important;
        }

        .stDataFrame th {
            background: #252f42 !important;
            color: #e8ecf1 !important;
            font-weight: 600 !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        .stDataFrame td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
            padding: 0.8rem !important;
        }

        .stDataFrame tr:hover {
            background: #252f42 !important;
        }

        /* ============ ALERTS & MESSAGES ============ */
        .stAlert, .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
            border-left: 4px solid !important;
        }

        .stSuccess {
            background: rgba(74, 222, 128, 0.1) !important;
            border-left-color: #4ade80 !important;
            color: #4ade80 !important;
        }

        .stError {
            background: rgba(248, 113, 113, 0.1) !important;
            border-left-color: #f87171 !important;
            color: #f87171 !important;
        }

        .stWarning {
            background: rgba(251, 191, 36, 0.1) !important;
            border-left-color: #fbbf24 !important;
            color: #fbbf24 !important;
        }

        .stInfo {
            background: rgba(96, 165, 250, 0.1) !important;
            border-left-color: #60a5fa !important;
            color: #60a5fa !important;
        }

        /* ============ RESPONSIVE ============ */
        @media (max-width: 768px) {
            .page-header {
                padding: 1.25rem !important;
            }

            .page-header h1 {
                font-size: 1.5rem !important;
            }

            .stForm {
                padding: 1.25rem !important;
            }

            .stButton > button {
                width: 100% !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_custom_css()
initialize()


def show_diagnosis(diagnosis: dict, rules: list[dict], mode: str) -> None:
    """Render diagnosis in a clean format."""
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Confidence", f"{diagnosis['confidence']}%")
    with col2:
        st.metric("OSI Layer", diagnosis['osi_layer'])
    with col3:
        st.metric("Severity", diagnosis['severity'].upper())
    with col4:
        st.metric("Mode", mode)
    
    st.markdown("---")
    
    # Root cause
    st.markdown("<div class='section-label'>📌 Root Cause</div>", unsafe_allow_html=True)
    st.markdown(f"**{diagnosis['root_cause']}")
    
    st.markdown("---")
    
    # Category and severity
    st.markdown("<div class='section-label'>🏷️ Classification</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Category:** {diagnosis['category']}")
    with col2:
        st.markdown(f"**Severity:** {diagnosis['severity'].upper()}")
    
    st.markdown("---")
    
    # Evidence
    st.markdown("<div class='section-label'>📋 Evidence</div>", unsafe_allow_html=True)
    if diagnosis.get("evidence"):
        for item in diagnosis["evidence"]:
            st.markdown(f"- {item}")
    else:
        st.info("No evidence provided.")
    
    st.markdown("---")
    
    # Next command
    st.markdown("<div class='section-label'>🔧 Next Command</div>", unsafe_allow_html=True)
    next_cmd = diagnosis.get("next_command", "").strip()
    if not next_cmd:
        next_cmd = "Collect additional relevant show-command output and review the diagnosis again."
    
    st.text_area("Command Output", value=next_cmd, disabled=True, height=120)
    
    # Fix steps
    if diagnosis.get("fix_steps"):
        st.markdown("---")
        st.markdown("<div class='section-label'>⚙️ Recommended Fix Steps</div>", unsafe_allow_html=True)
        for i, step in enumerate(diagnosis["fix_steps"], 1):
            st.markdown(f"**{i}.** {step}")
    
    # Rule findings
    st.markdown("---")
    with st.expander("🔍 Rule Checker Findings"):
        if rules:
            st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
        else:
            st.info("✓ All deterministic rules passed successfully.")


def home_page():
    """Render the home page with introduction and quick navigation."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Welcome to NetSage AI</h1>
            <p>Evidence-backed AI assistance for structured network troubleshooting.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        **NetSage AI** combines deterministic rule checking with optional AI models and mandatory human review 
        to provide transparent, evidence-backed network diagnostics. 
        
        ### How It Works
        
        1. **Report Issue** - Capture symptoms, device context, and show-command evidence
        2. **AI Analysis** - System runs deterministic checks and optional AI analysis
        3. **Human Review** - Review AI findings and approve, edit, or reject the diagnosis
        4. **Apply Fix** - Execute recommended configuration changes
        5. **Verification** - Record before-and-after test results to confirm resolution
        """
    )
    
    st.markdown("---")
    
    # Quick action cards
    st.markdown("<div class='section-label'>Quick Start</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**🧪 New Case**\n\nReport network problems and get evidence-backed analysis.")
        if st.button("Start Troubleshooting", use_container_width=True, key="home_btn1"):
            st.session_state["nav"] = "New Troubleshooting"
            st.rerun()
    
    with col2:
        st.info("**📚 Browse Cases**\n\nSearch and explore all documented troubleshooting cases.")
        if st.button("View Case Library", use_container_width=True, key="home_btn2"):
            st.session_state["nav"] = "Cases"
            st.rerun()
    
    with col3:
        st.info("**📊 View Dashboard**\n\nMonitor case trends, decisions, and verification outcomes.")
        if st.button("Open Dashboard", use_container_width=True, key="home_btn3"):
            st.session_state["nav"] = "Dashboard"
            st.rerun()
    
    st.markdown("---")
    
    # Key features
    st.markdown("### Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **✓ Deterministic Rules**
        
        Transparent rule engine checks against best practices.
        """)
    
    with col2:
        st.markdown("""
        **👤 Human Review Gate**
        
        Every diagnosis requires human approval before action.
        """)
    
    with col3:
        st.markdown("""
        **📝 Responsible AI**
        
        Track how humans improved AI predictions over time.
        """)


def dashboard_page():
    """Render the dashboard with operational metrics."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Dashboard</h1>
            <p>Operational overview of diagnoses, reviews, and verification outcomes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    values = metrics()
    
    # Display key metrics
    st.markdown("<div class='section-label'>📊 Key Metrics</div>", unsafe_allow_html=True)
    
    metric_cols = st.columns(6)
    metrics_data = [
        ("Cases", values["total_cases"]),
        ("Diagnoses", values["total_diagnoses"]),
        ("Accepted", values["accepted"]),
        ("Edited", values["edited"]),
        ("Rejected", values["rejected"]),
        ("Verified", values["verified"]),
    ]
    
    for col, (label, value) in zip(metric_cols, metrics_data):
        with col:
            st.metric(label, value)
    
    st.markdown("---")
    
    # Summary statistics
    st.markdown("<div class='section-label'>📈 Summary</div>", unsafe_allow_html=True)
    
    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.metric("AI-Human Agreement", f"{values['agreement_pct']}%")
    with summary_cols[1]:
        st.metric("High/Critical Issues", values["high_issues"])
    with summary_cols[2]:
        inconclusive = values.get("inconclusive_verification", 0)
        failed = values.get("failed_verification", 0)
        st.metric("Verification", f"✓ {values['verified']} | ⚠ {inconclusive} | ✕ {failed}")
    
    with db.connect() as connection:
        category = connection.execute("SELECT category, COUNT(*) count FROM cases GROUP BY category").fetchall()
        decisions = connection.execute("SELECT decision, COUNT(*) count FROM reviews GROUP BY decision").fetchall()
        verification = connection.execute("SELECT status, COUNT(*) count FROM verifications GROUP BY status").fetchall()
        recent = connection.execute("SELECT case_id, title, category, severity, created_at FROM cases ORDER BY created_at DESC LIMIT 10").fetchall()
    
    st.markdown("---")
    st.markdown("<div class='section-label'>📊 Analytics</div>", unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Cases by Category**")
        if category:
            chart_data = {row["category"]: row["count"] for row in category}
            st.bar_chart(chart_data)
        else:
            st.info("No cases recorded yet.")
    
    with chart_col2:
        st.markdown("**Decision Distribution**")
        if decisions:
            chart_data = {row["decision"]: row["count"] for row in decisions}
            st.bar_chart(chart_data)
        else:
            st.info("No review decisions recorded yet.")
    
    # Verification results
    st.markdown("**Verification Outcomes**")
    if verification:
        ver_data = []
        for row in verification:
            ver_data.append({
                "Status": row["status"],
                "Count": row["count"]
            })
        st.dataframe(pd.DataFrame(ver_data), use_container_width=True, hide_index=True)
    else:
        st.info("No verification results recorded yet.")
    
    st.markdown("---")
    
    # Recent cases
    st.markdown("<div class='section-label'>📋 Recent Cases</div>", unsafe_allow_html=True)
    if recent:
        recent_data = []
        for row in recent:
            recent_data.append({
                "Case ID": row["case_id"],
                "Title": row["title"][:50] + "..." if len(row["title"]) > 50 else row["title"],
                "Category": row["category"],
                "Severity": row["severity"],
                "Created": row["created_at"][:10]
            })
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True, hide_index=True)
    else:
        st.info("No cases recorded yet. Create a new case to get started.")


def troubleshoot_page():
    """Render the troubleshooting form."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>New Troubleshooting Case</h1>
            <p>Capture network issue details with evidence for AI-backed diagnosis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Initialize session state
    if "form_analysis_in_progress" not in st.session_state:
        st.session_state.form_analysis_in_progress = False
    
    st.info(
        "**💡 Tip:** Provide clear symptom descriptions, relevant network topology context, "
        "and complete show-command output from your network devices for the most accurate diagnosis."
    )
    
    with st.form("case_form"):
        # Issue Information
        st.markdown("<div class='section-label'>Issue Information</div>", unsafe_allow_html=True)
        
        title = st.text_input(
            "Case Title",
            placeholder="Example: VLAN trunk not passing traffic"
        )
        
        symptom = st.text_area(
            "Symptom Description (Required)",
            placeholder="Describe what's happening...",
            height=100
        )
        
        st.markdown("---")
        
        # Network Context
        st.markdown("<div class='section-label'>Network Context</div>", unsafe_allow_html=True)
        
        topology = st.text_area(
            "Topology & Device Information (Optional)",
            placeholder="Describe your network setup...",
            height=80
        )
        
        st.markdown("---")
        
        # Technical Evidence
        st.markdown("<div class='section-label'>Technical Evidence</div>", unsafe_allow_html=True)
        
        output = st.text_area(
            "Show-Command Output (Required)",
            placeholder="Paste relevant show command output...",
            height=150
        )
        
        st.markdown("---")
        
        # Classification
        st.markdown("<div class='section-label'>Classification</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category (Required)", sorted(SUPPORTED_CATEGORIES))
        with col2:
            severity = st.selectbox("Severity (Required)", ["Low", "Medium", "High", "Critical"], format_func=lambda x: x.lower())
        
        st.markdown("---")
        
        # Submit button
        submit_button = st.form_submit_button(
            "🚀 Analyze Problem",
            disabled=st.session_state.form_analysis_in_progress,
            use_container_width=True
        )
    
    if submit_button:
        # Prevent duplicate submissions
        if st.session_state.form_analysis_in_progress:
            st.warning("⚠️ Analysis is already in progress. Please wait...")
            return
        
        # Validate required fields
        errors = {}
        if not symptom or not symptom.strip():
            errors["Symptom"] = "Symptom description is required."
        if not output or not output.strip():
            errors["Show-command output"] = "Show-command output is required."
        if not category or not category.strip():
            errors["Category"] = "Category is required."
        if not severity or not severity.strip():
            errors["Severity"] = "Severity is required."
        
        # Display validation errors
        if errors:
            for field, message in errors.items():
                st.error(f"❌ {field}: {message}")
            return
        
        # Set flag to prevent duplicate submissions
        st.session_state.form_analysis_in_progress = True
        
        try:
            with st.spinner("🔄 Analyzing network evidence..."):
                # Generate unique case ID
                case_id = f"LIVE-{len(db.list_cases()) + 1:04d}"
                
                # Create case
                create_case(
                    {
                        "case_id": case_id,
                        "title": title or symptom[:80],
                        "symptom": symptom,
                        "topology": topology,
                        "show_output": output,
                        "category": category,
                        "severity": severity.lower(),
                    }
                )
                
                # Analyze with AI
                diagnosis_id, rules, diagnosis, mode = analyze(db.get_case(case_id))
                
                if not diagnosis:
                    st.error("❌ Diagnosis could not be generated. Please try again.")
                    st.session_state.form_analysis_in_progress = False
                    return
                
                # Store results in session
                st.session_state["latest"] = {
                    "case_id": case_id,
                    "diagnosis_id": diagnosis_id,
                    "rules": rules,
                    "diagnosis": diagnosis,
                    "mode": mode,
                }
                
                st.success("✅ Analysis complete! Review the diagnosis below or go to Human Review.")
                st.session_state.form_analysis_in_progress = False
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {type(e).__name__}: {str(e)}")
            st.session_state.form_analysis_in_progress = False



def cases_page():
    """Render case library with search and filter."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Case Library</h1>
            <p>Search, filter, and export troubleshooting cases.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<div class='section-label'>🔍 Search & Filter</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search", placeholder="Case ID, title, or symptom")
    with col2:
        category = st.selectbox("Category", ["All"] + sorted(SUPPORTED_CATEGORIES))
    with col3:
        severity = st.selectbox("Severity", ["All", "Low", "Medium", "High", "Critical"], format_func=lambda x: x if x == "All" else x.lower())
    
    category_filter = None if category == "All" else category
    severity_filter = None if severity == "All" else severity.lower()
    
    rows = db.list_cases(search, category_filter, severity_filter)
    
    st.markdown("---")
    st.markdown("<div class='section-label'>📋 Cases</div>", unsafe_allow_html=True)
    
    if rows:
        display_data = []
        for row in rows:
            display_data.append({
                "Case ID": row["case_id"],
                "Title": row["title"][:50] + "..." if len(row["title"]) > 50 else row["title"],
                "Category": row["category"],
                "Severity": row["severity"].upper(),
                "Created": row["created_at"][:10]
            })
        
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.download_button(
            "📥 Export to CSV",
            pd.DataFrame(rows).to_csv(index=False),
            "netsage_cases.csv",
            "text/csv",
            use_container_width=True
        )
    else:
        st.info("No cases match your search criteria.")


def review_page():
    """Render human review workflow."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Human Review</h1>
            <p>Validate the AI diagnosis and approve, edit, or reject.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    item = st.session_state.get("latest")
    if not item:
        st.info("📋 No diagnosis to review. Analyze a case first in New Troubleshooting.")
        if st.button("Go to Troubleshooting", use_container_width=True):
            st.session_state["nav"] = "New Troubleshooting"
            st.rerun()
        return
    
    st.markdown("<div class='section-label'>📋 AI Diagnosis</div>", unsafe_allow_html=True)
    show_diagnosis(item["diagnosis"], item["rules"], item["mode"])
    
    st.markdown("---")
    st.markdown("<div class='section-label'>👤 Your Decision</div>", unsafe_allow_html=True)
    
    if "review_decision" not in st.session_state:
        st.session_state.review_decision = "ACCEPT"
    
    decision_col1, decision_col2, decision_col3 = st.columns(3)
    
    with decision_col1:
        if st.button("✅ ACCEPT", use_container_width=True, key="btn_accept"):
            st.session_state.review_decision = "ACCEPT"
            st.rerun()
    
    with decision_col2:
        if st.button("✏️ EDIT", use_container_width=True, key="btn_edit"):
            st.session_state.review_decision = "EDIT"
            st.rerun()
    
    with decision_col3:
        if st.button("❌ REJECT", use_container_width=True, key="btn_reject"):
            st.session_state.review_decision = "REJECT"
            st.rerun()
    
    decision = st.session_state.review_decision
    st.markdown("---")
    
    if decision == "ACCEPT":
        st.info("✅ Comment is optional for ACCEPT decisions.")
    elif decision == "EDIT":
        st.warning("✏️ Comment REQUIRED - explain the correction.")
    elif decision == "REJECT":
        st.warning("❌ Comment REQUIRED - explain rejection.")
    
    comment = st.text_area(
        "Reviewer Comment",
        placeholder="Enter your notes..." if decision in ("EDIT", "REJECT") else "Optional comment...",
        height=100
    )
    
    edited = None
    if decision == "EDIT":
        st.markdown("---")
        st.markdown("<div class='section-label'>📝 Corrected Root Cause</div>", unsafe_allow_html=True)
        root = st.text_area(
            "Edit root cause:",
            value=item["diagnosis"]["root_cause"],
            height=100,
            key="edited_root_cause"
        )
        edited = {**item["diagnosis"], "root_cause": root}
    
    st.markdown("---")
    if st.button("💾 Save Review", use_container_width=True, key="save_review_btn"):
        if decision in ("EDIT", "REJECT") and (not comment or not comment.strip()):
            st.error(f"Comment required for {decision} decision.")
            return
        
        final_comment = comment.strip() if comment and comment.strip() else "Accepted."
        
        try:
            save_review({
                "diagnosis_id": item["diagnosis_id"],
                "decision": decision,
                "edited_diagnosis": edited,
                "reviewer_comment": final_comment,
            })
            st.success("✅ Review saved!")
            if "latest" in st.session_state:
                del st.session_state["latest"]
            if "review_decision" in st.session_state:
                del st.session_state["review_decision"]
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save: {type(e).__name__}")


def verification_page():
    """Render verification workflow."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Verification</h1>
            <p>Record before-and-after test results to confirm the fix.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    cases = db.list_cases()
    
    if not cases:
        st.info("No cases available. Create a case first in New Troubleshooting.")
        return
    
    case_id = st.selectbox("Select Case", [row["case_id"] for row in cases])
    
    st.markdown("---")
    st.markdown("<div class='section-label'>🧪 Test Results</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown("**BEFORE FIX**")
        before = st.text_input("Before Result", placeholder="PING FAILED")
    with col2:
        st.markdown("**→**")
    with col3:
        st.markdown("**AFTER FIX**")
        after = st.text_input("After Result", placeholder="PING SUCCESS")
    
    st.markdown("---")
    st.markdown("<div class='section-label'>📝 Verification Notes</div>", unsafe_allow_html=True)
    notes = st.text_area(
        "Notes",
        placeholder="How did you verify? What commands did you run?",
        height=100
    )
    
    if before.strip() and after.strip():
        st.markdown("---")
        from models.verification import calculate_status
        preview_status = calculate_status(before, after)
        st.info(f"**Expected Status:** {preview_status}")
    
    st.markdown("---")
    if st.button("💾 Save Verification", use_container_width=True):
        if not before or not before.strip():
            st.error("Before result required.")
            return
        if not after or not after.strip():
            st.error("After result required.")
            return
        
        try:
            status = verify(case_id, before, after, notes)
            st.success(f"✅ Saved! Status: {status}")
            st.balloons()
        except Exception as e:
            st.error(f"Failed: {type(e).__name__}")


def responsible_page():
    """Render Responsible AI corrections and lessons learned."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Responsible AI</h1>
            <p>Track how human review improved AI predictions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    with db.connect() as connection:
        rows = connection.execute(
            "SELECT case_id, ai_diagnosis, human_decision, corrected_diagnosis, reason_for_correction, lesson FROM responsible_ai_logs ORDER BY created_at DESC"
        ).fetchall()
    
    if not rows:
        st.info("No corrections yet. Corrections will appear here when you EDIT or REJECT diagnoses.")
        return
    
    st.markdown("<div class='section-label'>📈 Summary</div>", unsafe_allow_html=True)
    
    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.metric("Total", len(rows))
    with summary_cols[1]:
        st.metric("Accepted", len([r for r in rows if r["human_decision"] == "ACCEPT"]))
    with summary_cols[2]:
        st.metric("Edited", len([r for r in rows if r["human_decision"] == "EDIT"]))
    with summary_cols[3]:
        st.metric("Rejected", len([r for r in rows if r["human_decision"] == "REJECT"]))
    
    st.markdown("---")
    st.markdown("<div class='section-label'>📋 Correction Log</div>", unsafe_allow_html=True)
    
    for i, row in enumerate(rows, 1):
        icon = "✅" if row["human_decision"] == "ACCEPT" else "✏️" if row["human_decision"] == "EDIT" else "❌"
        
        with st.expander(f"{icon} {row['case_id']} - {row['human_decision']}"):
            st.markdown(f"**AI Diagnosis:** {row['ai_diagnosis'][:150]}...")
            st.markdown(f"**Reason:** {row['reason_for_correction']}")
            st.markdown(f"**Lesson:** {row['lesson']}")


def main():
    """Dispatch the selected Streamlit page."""
    st.sidebar.title("🛰️ NetSage AI")
    st.sidebar.markdown("Evidence-backed troubleshooting")
    st.sidebar.markdown("---")
    
    default_nav = st.session_state.get("nav", "Home")
    nav_items = [
        "Home",
        "Dashboard",
        "New Troubleshooting",
        "Cases",
        "Human Review",
        "Verification",
        "Responsible AI",
        "About",
    ]
    
    page = st.sidebar.radio("Navigate", nav_items, index=nav_items.index(default_nav) if default_nav in nav_items else 0)
    
    pages = {
        "Home": home_page,
        "Dashboard": dashboard_page,
        "New Troubleshooting": troubleshoot_page,
        "Cases": cases_page,
        "Human Review": review_page,
        "Verification": verification_page,
        "Responsible AI": responsible_page,
    }
    
    if page == "About":
        st.markdown(
            """
            <div class='page-header'>
                <h1>About NetSage AI</h1>
                <p>Evidence-backed network troubleshooting with human review gate.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            NetSage AI combines deterministic rule checking with optional AI models and mandatory human review
            to provide transparent, evidence-backed network diagnostics.
            
            **Workflow:**
            1. Report Issue - Capture symptoms and show-command evidence
            2. AI Analysis - Run deterministic checks and optional AI
            3. Human Review - Approve, edit, or reject diagnosis
            4. Apply Fix - Execute configuration changes
            5. Verification - Record before-and-after results
            
            **Features:**
            - Deterministic rule engine for transparency
            - Mandatory human review gate
            - Complete audit trail
            - Responsible AI logging
            - SQLite database persistence
            """
        )
        return
    
    pages[page]()


if __name__ == "__main__":
    main()

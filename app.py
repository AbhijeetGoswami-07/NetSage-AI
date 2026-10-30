"""Streamlit entry point for NetSage AI - Modern Enterprise AI Network Operations Dashboard."""
import os
import pandas as pd
import streamlit as st
from database import db
from models.case import SUPPORTED_CATEGORIES
from services.case_service import initialize, create_case
from services.diagnosis_service import analyze
from services.review_service import save as save_review
from services.verification_service import verify
from services.analytics_service import metrics

st.set_page_config(
    page_title="NetSage AI - Network Troubleshooting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_custom_css() -> None:
    """Inject modern, sleek dark SaaS cyber-infrastructure styling."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ============ BASE & CANVAS ============ */
        html, body, .stApp {
            background: radial-gradient(circle at 15% 15%, #0f172a 0%, #070b14 100%) !important;
            color: #e2e8f0 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Top header bar in streamlit */
        header[data-testid="stHeader"] {
            background: rgba(7, 11, 20, 0.8) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* ============ SIDEBAR MODERNIZATION ============ */
        section[data-testid="stSidebar"] {
            background: #090d16 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 1.25rem 0.75rem !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 1.25rem 0 !important;
        }

        /* Brand Card in Sidebar */
        .sidebar-brand-card {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            text-align: center;
        }

        .sidebar-brand-title {
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .sidebar-brand-tag {
            font-size: 0.72rem;
            color: #94a3b8;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-weight: 600;
            margin-top: 0.25rem;
        }

        .system-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #34d399;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.25rem 0.65rem;
            border-radius: 9999px;
            margin-top: 0.6rem;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            display: inline-block;
        }

        /* Nav radio options styling in sidebar */
        [data-testid="stSidebar"] [role="radiogroup"] > label {
            background: transparent !important;
            border-radius: 8px !important;
            padding: 0.55rem 0.85rem !important;
            margin: 0.15rem 0 !important;
            border: 1px solid transparent !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #f1f5f9 !important;
            border-left: 3px solid #6366f1 !important;
            padding-left: 1rem !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.2) 0%, rgba(99, 102, 241, 0.05) 100%) !important;
            border: 1px solid rgba(99, 102, 241, 0.35) !important;
            border-left: 3px solid #6366f1 !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }

        /* Sidebar stats box */
        .sidebar-telemetry {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 0.85rem;
            margin-top: 1rem;
            font-size: 0.8rem;
        }

        .telemetry-item {
            display: flex;
            justify-content: space-between;
            color: #94a3b8;
            margin: 0.35rem 0;
        }

        .telemetry-val {
            color: #38bdf8;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
        }

        /* ============ HERO & PAGE HEADERS ============ */
        .page-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 1.75rem 2rem !important;
            margin-bottom: 1.75rem !important;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6366f1 0%, #06b6d4 50%, #3b82f6 100%);
        }

        .page-header h1 {
            margin: 0 !important;
            color: #f8fafc !important;
            font-size: 2.1rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            line-height: 1.2 !important;
        }

        .page-header p {
            margin: 0.45rem 0 0 0 !important;
            color: #94a3b8 !important;
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }

        /* ============ WORKFLOW STEPPER ============ */
        .stepper-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 0.85rem 1.25rem;
            margin-bottom: 1.75rem;
            gap: 8px;
        }

        .step-node {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #64748b;
        }

        .step-node.active {
            color: #38bdf8;
        }

        .step-node.completed {
            color: #10b981;
        }

        .step-badge {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.72rem;
            background: rgba(255, 255, 255, 0.08);
            color: #94a3b8;
        }

        .step-node.active .step-badge {
            background: #0284c7;
            color: white;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }

        .step-node.completed .step-badge {
            background: #10b981;
            color: white;
        }

        .step-divider {
            flex: 1;
            height: 2px;
            background: rgba(255, 255, 255, 0.08);
        }

        /* ============ METRIC CARDS ============ */
        .stMetric {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.6) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            padding: 1.15rem 1.35rem !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1) !important;
        }

        .stMetric:hover {
            border-color: rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 0 15px rgba(99, 102, 241, 0.2) !important;
        }

        .stMetric label {
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }

        .stMetric [data-testid="stMetricValue"] {
            background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2rem !important;
            font-weight: 800 !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ============ SECTION LABELS ============ */
        .section-label {
            color: #38bdf8 !important;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            margin: 1.25rem 0 0.6rem 0 !important;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* ============ BUTTONS ============ */
        .stButton > button {
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.4rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            transition: all 0.2s ease !important;
            min-height: 44px !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        }

        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.45) !important;
            transform: translateY(-1px) !important;
            filter: brightness(1.1) !important;
        }

        .stButton > button:active {
            transform: translateY(1px) !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
        }

        .stButton > button:disabled {
            background: #334155 !important;
            opacity: 0.6 !important;
            cursor: not-allowed !important;
            box-shadow: none !important;
            transform: none !important;
        }

        /* Secondary action button */
        .secondary-btn button {
            background: rgba(30, 41, 59, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: none !important;
            color: #cbd5e1 !important;
        }

        .secondary-btn button:hover {
            background: rgba(51, 65, 85, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
        }

        /* ============ FORMS & INPUTS ============ */
        .stForm {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 1.75rem !important;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.4) !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > textarea {
            background: #0b101b !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            padding: 0.75rem 1rem !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15) !important;
            outline: none !important;
        }

        .stTextArea textarea {
            font-family: 'JetBrains Mono', Consolas, monospace !important;
            font-size: 0.9rem !important;
            line-height: 1.5 !important;
        }

        /* Select box styling */
        [data-testid="stSelectbox"] > div > div {
            background: #0b101b !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
        }

        /* ============ CODE & TERMINAL CARDS ============ */
        .terminal-card {
            background: #070b14;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            margin: 1rem 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }

        .terminal-header {
            background: #111827;
            padding: 0.55rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .terminal-dots {
            display: flex;
            gap: 6px;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .dot-red { background-color: #ef4444; }
        .dot-yellow { background-color: #f59e0b; }
        .dot-green { background-color: #10b981; }

        .terminal-title {
            color: #94a3b8;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 500;
        }

        .terminal-body {
            padding: 1rem;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            line-height: 1.6;
            white-space: pre-wrap;
            max-height: 280px;
            overflow-y: auto;
        }

        /* ============ STATUS BADGES ============ */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 0.25rem 0.7rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-critical {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.35);
            color: #f87171;
        }

        .badge-high {
            background: rgba(249, 115, 22, 0.15);
            border: 1px solid rgba(249, 115, 22, 0.35);
            color: #fb923c;
        }

        .badge-medium {
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.35);
            color: #fbbf24;
        }

        .badge-low {
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #34d399;
        }

        .badge-info {
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.35);
            color: #38bdf8;
        }

        /* Diagnosis summary box */
        .diagnosis-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1.25rem 0;
            position: relative;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(99, 102, 241, 0.15);
        }

        .diagnosis-highlight {
            background: rgba(99, 102, 241, 0.12);
            border-left: 4px solid #6366f1;
            padding: 1rem 1.25rem;
            border-radius: 0 10px 10px 0;
            margin: 1rem 0;
            font-size: 1.15rem;
            font-weight: 600;
            color: #f1f5f9;
        }

        /* ============ TABLES & DATAFRAMES ============ */
        .stDataFrame {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        /* ============ ALERTS & NOTICES ============ */
        .stAlert {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 1rem 1.25rem !important;
        }

        /* Responsive overrides */
        @media (max-width: 768px) {
            .page-header {
                padding: 1.25rem !important;
            }
            .page-header h1 {
                font-size: 1.6rem !important;
            }
            .stepper-container {
                flex-direction: column;
                align-items: flex-start;
            }
            .step-divider {
                display: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_custom_css()
initialize()


# =========================================================================
# QUICK-START SAMPLE TEMPLATES
# =========================================================================
PRESET_TEMPLATES = {
    "OSI Layer 2: VLAN Trunk Mismatch": {
        "title": "Switchport Trunk Native VLAN Inconsistency on Gi0/1",
        "symptom": "Host-1 in VLAN 20 cannot reach Gateway. Native VLAN mismatch alarms observed in syslog on SW-1 and SW-2.",
        "topology": "Host-1 (VLAN 20) -> SW-1 [Gi0/1] <==Trunk==> [Gi0/1] SW-2 -> Core Router",
        "show_output": """SW-1# show interfaces trunk
Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       on               802.1q         trunking      10

SW-2# show interfaces trunk
Port        Mode             Encapsulation  Status        Native vlan
Gi0/1       on               802.1q         trunking      20

%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet0/1 (10), with SW-2 GigabitEthernet0/1 (20).""",
        "category": "VLAN",
        "severity": "High",
    },
    "OSI Layer 3: OSPF Neighbor Stuck in EXSTART": {
        "title": "OSPF Adjacency Failure - MTU Discrepancy",
        "symptom": "Branch router R2 is unable to form full OSPF neighbor adjacency with HQ Router R1. Neighbor state oscillates between EXSTART and DOWN.",
        "topology": "R1 [Gi0/0/0, MTU 1500] <-------> [Gi0/0/0, MTU 1400] R2",
        "show_output": """R1# show ip ospf neighbor
Neighbor ID     Pri   State           Dead Time   Address         Interface
192.168.12.2      1   EXSTART/DR      00:00:34    192.168.12.2    GigabitEthernet0/0/0

R1# show ip interface GigabitEthernet0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet Address 192.168.12.1/24, Area 0
  MTU 1500 bytes, BW 1000000 Kbit/sec

R2# show ip interface GigabitEthernet0/0/0
GigabitEthernet0/0/0 is up, line protocol is up
  Internet Address 192.168.12.2/24, Area 0
  MTU 1400 bytes, BW 1000000 Kbit/sec""",
        "category": "Routing",
        "severity": "Critical",
    },
    "OSI Layer 3: Duplicate IP Address Conflict": {
        "title": "ARP Flapping & IP Address Conflict on Default Gateway",
        "symptom": "Intermittent connectivity drops across subnet 10.10.10.0/24. Ping packet loss fluctuates between 40% and 80%.",
        "topology": "Core Switch (VLAN 10 SVI 10.10.10.1) <---> Rogue Wireless AP (Statically set to 10.10.10.1)",
        "show_output": """Switch# show ip arp 10.10.10.1
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.10.10.1              -   001b.d4fa.2100  ARPA   Vlan10

%IP-4-DUPADDR: Duplicate address 10.10.10.1 on Vlan10, sourced by 54e0.321b.aa94
%SYS-4-ARPFLAP: IP address 10.10.10.1 flapped from 001b.d4fa.2100 to 54e0.321b.aa94 on GigabitEthernet1/0/22""",
        "category": "IP",
        "severity": "Critical",
    },
    "OSI Layer 4: Standard ACL Blocking DNS Traffic": {
        "title": "Outbound Internet Fails - DNS UDP 53 Denied by Inbound ACL",
        "symptom": "Workstations can ping public IP 8.8.8.8 directly, but domain name resolution (nslookup) times out.",
        "topology": "LAN Subnet (172.16.1.0/24) -> Gateway Router [Gi0/1 in, ACL 101] -> ISP",
        "show_output": """Router# show access-lists 101
Extended IP access list 101
    10 permit tcp 172.16.1.0 0.0.0.255 any eq www (1482 matches)
    20 permit tcp 172.16.1.0 0.0.0.255 any eq 443 (8920 matches)
    30 permit icmp 172.16.1.0 0.0.0.255 any (210 matches)
    40 deny ip any any log (584 matches)

Router# show ip interface GigabitEthernet0/1
GigabitEthernet0/1 is up, line protocol is up
  Inbound access list is 101""",
        "category": "ACL",
        "severity": "High",
    },
}


def render_workflow_stepper(current_step: int = 1) -> None:
    """Render a modern visual troubleshooting stepper."""
    steps = [
        (1, "Capture Evidence"),
        (2, "AI & Rule Engine"),
        (3, "Human Review Gate"),
        (4, "Field Verification"),
        (5, "Resolution Audit"),
    ]
    html = "<div class='stepper-container'>"
    for idx, (num, name) in enumerate(steps):
        state = "completed" if num < current_step else "active" if num == current_step else "upcoming"
        icon = "✓" if num < current_step else str(num)
        html += f"""
        <div class='step-node {state}'>
            <div class='step-badge'>{icon}</div>
            <span>{name}</span>
        </div>
        """
        if idx < len(steps) - 1:
            html += "<div class='step-divider'></div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def show_diagnosis(diagnosis: dict, rules: list[dict], mode: str) -> None:
    """Render diagnosis in a high-tech modern SaaS layout."""
    confidence = diagnosis.get("confidence", 85)
    osi_layer = diagnosis.get("osi_layer", "Layer 3")
    severity = diagnosis.get("severity", "Medium").upper()
    category = diagnosis.get("category", "General")
    root_cause = diagnosis.get("root_cause", "Unspecified root cause")

    # Top KPI Metrics with Glassmorphism
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Confidence Score", f"{confidence}%")
    with col2:
        st.metric("OSI Layer", osi_layer)
    with col3:
        st.metric("Severity", severity)
    with col4:
        st.metric("Engine Mode", mode)

    # Diagnosis Highlight Banner
    st.markdown(
        f"""
        <div class='diagnosis-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span class='section-label' style='margin:0;'>🎯 ROOT CAUSE DIAGNOSIS</span>
                <span class='badge badge-{"critical" if severity in ("CRITICAL", "HIGH") else "medium"}'>{severity} PRIORITY</span>
            </div>
            <div class='diagnosis-highlight'>
                {root_cause}
            </div>
            <div style='display:flex; gap:12px; margin-top:0.75rem;'>
                <span class='badge badge-info'>📂 Category: {category}</span>
                <span class='badge badge-info'>🛰️ Target: {osi_layer}</span>
                <span class='badge badge-low'>🤖 Engine: {mode}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Evidence & Rule Engine Findings Grid
    col_evidence, col_rules = st.columns([1, 1])

    with col_evidence:
        st.markdown("<div class='section-label'>📋 Audited Evidence Citations</div>", unsafe_allow_html=True)
        evidence_list = diagnosis.get("evidence", [])
        if evidence_list:
            for item in evidence_list:
                st.markdown(
                    f"""
                    <div style='background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:0.65rem 0.9rem; margin-bottom:0.5rem; display:flex; align-items:flex-start; gap:8px;'>
                        <span style='color:#10b981;'>✓</span>
                        <span style='color:#cbd5e1; font-size:0.9rem;'>{item}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No specific evidence cited.")

    with col_rules:
        st.markdown("<div class='section-label'>⚙️ Deterministic Rule Validation</div>", unsafe_allow_html=True)
        if rules:
            st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
        else:
            st.markdown(
                """
                <div style='background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3); border-radius:10px; padding:1.25rem; text-align:center;'>
                    <span style='font-size:1.5rem;'>🛡️</span>
                    <div style='color:#34d399; font-weight:700; margin-top:0.35rem;'>All Deterministic Checks Passed</div>
                    <div style='color:#94a3b8; font-size:0.85rem; margin-top:0.25rem;'>No standard Cisco syntax violations or known misconfigurations detected.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Next Recommended Command in Terminal Window
    next_cmd = diagnosis.get("next_command", "").strip()
    if not next_cmd:
        next_cmd = "show ip interface brief\nshow running-config"

    st.markdown("<div class='section-label'>💻 Next Diagnostic / Fix Command</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='terminal-card'>
            <div class='terminal-header'>
                <div class='terminal-dots'>
                    <div class='dot dot-red'></div>
                    <div class='dot dot-yellow'></div>
                    <div class='dot dot-green'></div>
                </div>
                <div class='terminal-title'>cisco-ios-cli ~ recommended action</div>
                <div></div>
            </div>
            <div class='terminal-body'>{next_cmd}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Remediation Steps
    fix_steps = diagnosis.get("fix_steps", [])
    if fix_steps:
        st.markdown("<div class='section-label'>🛠️ Recommended Resolution Runbook</div>", unsafe_allow_html=True)
        for i, step in enumerate(fix_steps, 1):
            st.markdown(
                f"""
                <div style='background:rgba(30, 41, 59, 0.5); border-left:3px solid #38bdf8; border-radius:0 8px 8px 0; padding:0.65rem 1rem; margin-bottom:0.5rem;'>
                    <strong style='color:#38bdf8;'>Step {i}:</strong> <span style='color:#e2e8f0;'>{step}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================================
# PAGES
# =========================================================================

def home_page():
    """Render high-tech landing page with system telemetry and quick-start."""
    st.markdown(
        """
        <div class='page-header'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h1>NetSage AI Operations Center</h1>
                    <p>Evidence-backed Cisco diagnostic engine with deterministic rule checking and human review gates.</p>
                </div>
                <div class='system-status-pill'>
                    <span class='pulse-dot'></span>
                    <span>ONLINE & OPERATIONAL</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_workflow_stepper(1)

    # Quick Action Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border:1px solid rgba(56, 189, 248, 0.25); border-radius:14px; padding:1.25rem; height:100%; box-shadow:0 4px 20px rgba(0,0,0,0.25);'>
                <div style='font-size:1.75rem; margin-bottom:0.5rem;'>⚡</div>
                <h3 style='margin:0 0 0.5rem 0; color:#f8fafc; font-size:1.2rem;'>New Case Diagnosis</h3>
                <p style='color:#94a3b8; font-size:0.9rem; margin-bottom:1.25rem;'>Submit real or simulated Cisco CLI command outputs to diagnose network faults with citations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚀 Start Troubleshooting", use_container_width=True, key="home_btn1"):
            st.session_state["nav"] = "New Troubleshooting"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border:1px solid rgba(99, 102, 241, 0.25); border-radius:14px; padding:1.25rem; height:100%; box-shadow:0 4px 20px rgba(0,0,0,0.25);'>
                <div style='font-size:1.75rem; margin-bottom:0.5rem;'>📊</div>
                <h3 style='margin:0 0 0.5rem 0; color:#f8fafc; font-size:1.2rem;'>Telemetry Dashboard</h3>
                <p style='color:#94a3b8; font-size:0.9rem; margin-bottom:1.25rem;'>Analyze fault distributions, human review agreement, and resolution verification success rates.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📈 Open Dashboard", use_container_width=True, key="home_btn2"):
            st.session_state["nav"] = "Dashboard"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div style='background:linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border:1px solid rgba(16, 185, 129, 0.25); border-radius:14px; padding:1.25rem; height:100%; box-shadow:0 4px 20px rgba(0,0,0,0.25);'>
                <div style='font-size:1.75rem; margin-bottom:0.5rem;'>📚</div>
                <h3 style='margin:0 0 0.5rem 0; color:#f8fafc; font-size:1.2rem;'>Case Knowledge Base</h3>
                <p style='color:#94a3b8; font-size:0.9rem; margin-bottom:1.25rem;'>Explore 40+ pre-seeded Cisco network case studies with full configs, symptoms, and fixes.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🔍 Explore Cases", use_container_width=True, key="home_btn3"):
            st.session_state["nav"] = "Cases"
            st.rerun()

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    # Architecture Highlights
    st.markdown("<div class='section-label'>🛡️ System Architecture Pillars</div>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)

    pillars = [
        ("Deterministic Rules", "10 Specialized modules verify ACLs, VLANs, IPs, and routing before AI runs.", "⚙️"),
        ("Evidence-Backed", "Diagnoses are grounded strictly in quoted `show` command line outputs.", "📑"),
        ("Human-In-The-Loop", "Mandatory ACCEPT / EDIT / REJECT audit gate before any fix is deployed.", "👤"),
        ("Responsible AI", "Model drift and human correction tracking persisted permanently in SQLite.", "⚖️"),
    ]

    for col, (title, desc, icon) in zip([p1, p2, p3, p4], pillars):
        with col:
            st.markdown(
                f"""
                <div style='background:rgba(15, 23, 42, 0.5); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:1rem;'>
                    <div style='font-size:1.4rem; margin-bottom:0.35rem;'>{icon}</div>
                    <div style='color:#f8fafc; font-weight:700; font-size:0.95rem; margin-bottom:0.25rem;'>{title}</div>
                    <div style='color:#94a3b8; font-size:0.8rem; line-height:1.4;'>{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def dashboard_page():
    """Render modern operations analytics dashboard."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Executive Telemetry & Analytics</h1>
            <p>Operational health, diagnostic accuracy, and human-in-the-loop review metrics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    values = metrics()

    # Top Row Metrics Grid
    st.markdown("<div class='section-label'>📊 Global Telemetry</div>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    metrics_list = [
        ("Total Cases", values["total_cases"]),
        ("Diagnoses", values["total_diagnoses"]),
        ("Human Accepted", values["accepted"]),
        ("Human Corrected", values["edited"]),
        ("Rejected", values["rejected"]),
        ("Verified Fixes", values["verified"]),
    ]

    for col, (label, val) in zip([m1, m2, m3, m4, m5, m6], metrics_list):
        with col:
            st.metric(label, val)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Key Performance Indicators Row
    st.markdown("<div class='section-label'>📈 Key Quality Indicators</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric("AI-Human Alignment Rate", f"{values['agreement_pct']}%")
    with s2:
        st.metric("High & Critical Incidents", values["high_issues"])
    with s3:
        inconclusive = values.get("inconclusive_verification", 0)
        failed = values.get("failed_verification", 0)
        st.metric("Resolution Verification", f"✓ {values['verified']} | ⚠ {inconclusive} | ✕ {failed}")

    with db.connect() as connection:
        category = connection.execute("SELECT category, COUNT(*) count FROM cases GROUP BY category").fetchall()
        decisions = connection.execute("SELECT decision, COUNT(*) count FROM reviews GROUP BY decision").fetchall()
        verification = connection.execute("SELECT status, COUNT(*) count FROM verifications GROUP BY status").fetchall()
        recent = connection.execute("SELECT case_id, title, category, severity, created_at FROM cases ORDER BY created_at DESC LIMIT 10").fetchall()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Charts Grid
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-label'>📂 Incidents by Network Layer & Protocol</div>", unsafe_allow_html=True)
        if category:
            cat_data = {row["category"]: row["count"] for row in category}
            st.bar_chart(cat_data, color="#6366f1")
        else:
            st.info("No cases logged.")

    with c2:
        st.markdown("<div class='section-label'>🛡️ Human Review Decision Distribution</div>", unsafe_allow_html=True)
        if decisions:
            dec_data = {row["decision"]: row["count"] for row in decisions}
            st.bar_chart(dec_data, color="#06b6d4")
        else:
            st.info("No human decisions logged yet.")

    # Recent Incidents Table
    st.markdown("<div class='section-label'>📋 Recent Incident Pipeline</div>", unsafe_allow_html=True)
    if recent:
        df_recent = pd.DataFrame([
            {
                "Case ID": r["case_id"],
                "Title": r["title"][:60] + "..." if len(r["title"]) > 60 else r["title"],
                "Category": r["category"],
                "Severity": r["severity"].upper(),
                "Timestamp": r["created_at"][:19]
            }
            for r in recent
        ])
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("No incidents in pipeline.")


def troubleshoot_page():
    """Render enhanced troubleshooting interface with 1-click test templates."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>New Diagnostic Case</h1>
            <p>Provide Cisco symptoms and command outputs for evidence-backed deterministic and AI analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_workflow_stepper(1)

    if "form_analysis_in_progress" not in st.session_state:
        st.session_state.form_analysis_in_progress = False

    # Quick Preset Selector
    st.markdown("<div class='section-label'>⚡ 1-Click Diagnostic Presets (Quick-Test)</div>", unsafe_allow_html=True)
    cols = st.columns(len(PRESET_TEMPLATES))
    for col, (preset_name, preset_data) in zip(cols, PRESET_TEMPLATES.items()):
        with col:
            if st.button(preset_name.split(":")[1].strip(), use_container_width=True, key=f"preset_{preset_name}"):
                st.session_state["form_title"] = preset_data["title"]
                st.session_state["form_symptom"] = preset_data["symptom"]
                st.session_state["form_topology"] = preset_data["topology"]
                st.session_state["form_output"] = preset_data["show_output"]
                st.session_state["form_category"] = preset_data["category"]
                st.session_state["form_severity"] = preset_data["severity"]
                st.rerun()

    st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    with st.form("case_form"):
        st.markdown("<div class='section-label'>1. Incident Metadata</div>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
            title = st.text_input(
                "Incident Title",
                value=st.session_state.get("form_title", ""),
                placeholder="Example: OSPF Adjacency stuck in ExStart state on Gi0/0/0",
            )
        with col_t2:
            severity = st.selectbox(
                "Severity",
                ["Low", "Medium", "High", "Critical"],
                index=["Low", "Medium", "High", "Critical"].index(st.session_state.get("form_severity", "High")),
            )

        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            cat_list = sorted(SUPPORTED_CATEGORIES)
            cat_idx = cat_list.index(st.session_state.get("form_category", cat_list[0])) if st.session_state.get("form_category") in cat_list else 0
            category = st.selectbox("Protocol Category", cat_list, index=cat_idx)
        with col_c2:
            topology = st.text_input(
                "Network Topology Context (Optional)",
                value=st.session_state.get("form_topology", ""),
                placeholder="Example: R1 [Gi0/0] <---> [Gi0/0] R2 Area 0",
            )

        st.markdown("<div class='section-label'>2. Observable Symptom</div>", unsafe_allow_html=True)
        symptom = st.text_area(
            "Symptom Description (Required)",
            value=st.session_state.get("form_symptom", ""),
            placeholder="Describe ping failures, traceroute drops, flapping states, or syslog alarms...",
            height=90,
        )

        st.markdown("<div class='section-label'>3. Cisco CLI Evidence (show commands)</div>", unsafe_allow_html=True)
        output = st.text_area(
            "Show-Command Output (Required)",
            value=st.session_state.get("form_output", ""),
            placeholder="Paste 'show ip interface brief', 'show running-config', 'show ip ospf neighbor', etc...",
            height=160,
        )

        submit_button = st.form_submit_button(
            "⚡ Execute Evidence-Backed Diagnosis",
            disabled=st.session_state.form_analysis_in_progress,
            use_container_width=True,
        )

    if submit_button:
        if st.session_state.form_analysis_in_progress:
            st.warning("Analysis in progress. Please wait...")
            return

        errors = {}
        if not symptom or not symptom.strip():
            errors["Symptom"] = "Symptom description is required."
        if not output or not output.strip():
            errors["Show Output"] = "Show-command output is required."
        if not category or not category.strip():
            errors["Category"] = "Category is required."

        if errors:
            for field, message in errors.items():
                st.error(f"❌ {field}: {message}")
            return

        st.session_state.form_analysis_in_progress = True

        try:
            with st.spinner("🔍 Running deterministic rules and AI diagnostic inference..."):
                case_id = f"LIVE-{len(db.list_cases()) + 1:04d}"
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

                diagnosis_id, rules, diagnosis, mode = analyze(db.get_case(case_id))

                if not diagnosis:
                    st.error("❌ Diagnosis generation failed.")
                    st.session_state.form_analysis_in_progress = False
                    return

                st.session_state["latest"] = {
                    "case_id": case_id,
                    "diagnosis_id": diagnosis_id,
                    "rules": rules,
                    "diagnosis": diagnosis,
                    "mode": mode,
                }

                st.success("✅ Diagnosis generated! Proceed to Human Review Gate to approve or modify.")
                st.session_state.form_analysis_in_progress = False
                st.rerun()

        except Exception as e:
            st.error(f"❌ Diagnostic Error: {type(e).__name__}: {str(e)}")
            st.session_state.form_analysis_in_progress = False

    # If there is a freshly diagnosed case, display it right below
    if "latest" in st.session_state:
        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>🔍 Latest Generated Diagnostic Report</div>", unsafe_allow_html=True)
        item = st.session_state["latest"]
        show_diagnosis(item["diagnosis"], item["rules"], item["mode"])

        col_act1, col_act2 = st.columns([1, 1])
        with col_act1:
            if st.button("👉 Proceed to Human Review Gate", use_container_width=True):
                st.session_state["nav"] = "Human Review"
                st.rerun()
        with col_act2:
            if st.button("🧪 Go to Verification Test", use_container_width=True):
                st.session_state["nav"] = "Verification"
                st.rerun()


def cases_page():
    """Render modern case browser with search, filters, and export."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Incident & Case Knowledge Base</h1>
            <p>Search, filter, and audit all recorded network troubleshooting cases.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-label'>🔍 Search & Filter Matrix</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        search = st.text_input("Search Text", placeholder="Filter by ID, keywords, symptoms...")
    with c2:
        category = st.selectbox("Filter Category", ["All"] + sorted(SUPPORTED_CATEGORIES))
    with c3:
        severity = st.selectbox("Filter Severity", ["All", "Low", "Medium", "High", "Critical"])

    category_filter = None if category == "All" else category
    severity_filter = None if severity == "All" else severity.lower()

    rows = db.list_cases(search, category_filter, severity_filter)

    st.markdown("<div class='section-label'>📚 Filtered Case Repository ({})</div>".format(len(rows)), unsafe_allow_html=True)

    if rows:
        display_data = []
        for row in rows:
            display_data.append({
                "Case ID": row["case_id"],
                "Title": row["title"],
                "Category": row["category"],
                "Severity": row["severity"].upper(),
                "Created At": row["created_at"][:19]
            })

        st.dataframe(pd.DataFrame(display_data), use_container_width=True, hide_index=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        st.download_button(
            "📥 Export Filtered Cases as CSV",
            pd.DataFrame(rows).to_csv(index=False),
            "netsage_cases_export.csv",
            "text/csv",
            use_container_width=True
        )
    else:
        st.info("No cases matched your filter criteria.")


def review_page():
    """Render human-in-the-loop review approval gate."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Human-In-The-Loop Review Gate</h1>
            <p>Mandatory engineer validation before any diagnostic recommendation is applied.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_workflow_stepper(3)

    item = st.session_state.get("latest")
    if not item:
        st.markdown(
            """
            <div style='background:rgba(30, 41, 59, 0.5); border:1px dashed rgba(255,255,255,0.15); border-radius:14px; padding:2.5rem; text-align:center;'>
                <div style='font-size:2.5rem; margin-bottom:0.5rem;'>🛰️</div>
                <h3 style='color:#f8fafc; margin-bottom:0.25rem;'>No Pending Diagnosis for Review</h3>
                <p style='color:#94a3b8; max-width:500px; margin:0 auto 1.5rem auto;'>Submit an incident in New Troubleshooting to generate a diagnostic report requiring approval.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🚀 Start New Troubleshooting", use_container_width=True):
            st.session_state["nav"] = "New Troubleshooting"
            st.rerun()
        return

    st.markdown("<div class='section-label'>📋 AI & Rule Engine Finding Under Review</div>", unsafe_allow_html=True)
    show_diagnosis(item["diagnosis"], item["rules"], item["mode"])

    st.markdown("<div class='section-label'>👤 Human Decision Protocol</div>", unsafe_allow_html=True)

    if "review_decision" not in st.session_state:
        st.session_state.review_decision = "ACCEPT"

    d1, d2, d3 = st.columns(3)
    with d1:
        if st.button("✅ ACCEPT DIAGNOSIS", use_container_width=True, key="btn_accept"):
            st.session_state.review_decision = "ACCEPT"
            st.rerun()
    with d2:
        if st.button("✏️ EDIT ROOT CAUSE", use_container_width=True, key="btn_edit"):
            st.session_state.review_decision = "EDIT"
            st.rerun()
    with d3:
        if st.button("❌ REJECT DIAGNOSIS", use_container_width=True, key="btn_reject"):
            st.session_state.review_decision = "REJECT"
            st.rerun()

    decision = st.session_state.review_decision

    if decision == "ACCEPT":
        st.markdown(
            """
            <div style='background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3); border-radius:10px; padding:0.85rem 1.25rem; color:#34d399; font-weight:600;'>
                ✅ Selected: ACCEPT — Confirms AI & Rule diagnosis is accurate. Comment is optional.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif decision == "EDIT":
        st.markdown(
            """
            <div style='background:rgba(245, 158, 11, 0.1); border:1px solid rgba(245, 158, 11, 0.3); border-radius:10px; padding:0.85rem 1.25rem; color:#fbbf24; font-weight:600;'>
                ✏️ Selected: EDIT — Modify the root cause and provide corrective feedback (Required).
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif decision == "REJECT":
        st.markdown(
            """
            <div style='background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.3); border-radius:10px; padding:0.85rem 1.25rem; color:#f87171; font-weight:600;'>
                ❌ Selected: REJECT — Diagnosis is incorrect. Detailed rationale is required.
            </div>
            """,
            unsafe_allow_html=True,
        )

    edited = None
    if decision == "EDIT":
        st.markdown("<div class='section-label'>📝 Engineer Corrected Root Cause</div>", unsafe_allow_html=True)
        root = st.text_area(
            "Corrected Root Cause Definition",
            value=item["diagnosis"]["root_cause"],
            height=90,
            key="edited_root_cause"
        )
        edited = {**item["diagnosis"], "root_cause": root}

    comment = st.text_area(
        "Engineer Reviewer Notes",
        placeholder="Provide rationale or observations..." if decision in ("EDIT", "REJECT") else "Optional engineer notes...",
        height=90
    )

    if st.button("💾 Commit Human Review Decision", use_container_width=True, key="save_review_btn"):
        if decision in ("EDIT", "REJECT") and (not comment or not comment.strip()):
            st.error(f"❌ Reviewer notes are required when choosing {decision}.")
            return

        final_comment = comment.strip() if comment and comment.strip() else "Accepted by engineer."

        try:
            save_review({
                "diagnosis_id": item["diagnosis_id"],
                "decision": decision,
                "edited_diagnosis": edited,
                "reviewer_comment": final_comment,
            })
            st.success("✅ Review logged to audit trail! The case is ready for field verification.")
            if "latest" in st.session_state:
                del st.session_state["latest"]
            if "review_decision" in st.session_state:
                del st.session_state["review_decision"]
            st.rerun()
        except Exception as e:
            st.error(f"❌ Save Failed: {type(e).__name__}: {str(e)}")


def verification_page():
    """Render verification workflow."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Field Verification & Test Tracking</h1>
            <p>Confirm the resolution with verifiable before-and-after connectivity tests in Packet Tracer.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_workflow_stepper(4)

    cases = db.list_cases()
    if not cases:
        st.info("No cases available. Please create a case first.")
        return

    case_options = [row["case_id"] for row in cases]
    selected_case = st.selectbox("Target Case ID", case_options)

    st.markdown("<div class='section-label'>🧪 Verification Test Execution</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        st.markdown("**BEFORE FIX STATE** (e.g. Failure)")
        before = st.text_input("Before Test Result", placeholder="PING 10.1.1.1 FAILED (0/5 packets)")
    with c2:
        st.markdown("<div style='text-align:center; padding-top:1.5rem; font-size:1.5rem;'>➔</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("**AFTER FIX STATE** (e.g. Success)")
        after = st.text_input("After Test Result", placeholder="PING 10.1.1.1 SUCCESS (5/5 packets)")

    notes = st.text_area(
        "Verification Method & Commands Executed",
        placeholder="Commands run (e.g., ping, traceroute, show ip ospf neighbor), test outcomes, and timestamps...",
        height=90,
    )

    if before.strip() and after.strip():
        from models.verification import calculate_status
        preview_status = calculate_status(before, after)
        color = "#10b981" if preview_status == "PASSED" else "#ef4444" if preview_status == "FAILED" else "#f59e0b"
        st.markdown(
            f"""
            <div style='background:rgba(15, 23, 42, 0.7); border:1px solid {color}; border-radius:8px; padding:0.75rem 1rem; color:{color}; font-weight:700;'>
                ⚡ Auto-Calculated Verification Status: {preview_status}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("💾 Record Verification Status", use_container_width=True):
        if not before or not before.strip():
            st.error("❌ Before test result is required.")
            return
        if not after or not after.strip():
            st.error("❌ After test result is required.")
            return

        try:
            status = verify(selected_case, before, after, notes)
            st.success(f"✅ Verification Saved! Status recorded as: {status}")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Verification Save Failed: {type(e).__name__}: {str(e)}")


def responsible_page():
    """Render Responsible AI audits and learning logs."""
    st.markdown(
        """
        <div class='page-header'>
            <h1>Responsible AI Audit & Drift Log</h1>
            <p>Transparency audit log documenting how human engineering feedback refines diagnostic outcomes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_workflow_stepper(5)

    with db.connect() as connection:
        rows = connection.execute(
            "SELECT case_id, ai_diagnosis, human_decision, corrected_diagnosis, reason_for_correction, lesson FROM responsible_ai_logs ORDER BY created_at DESC"
        ).fetchall()

    if not rows:
        st.info("No Responsible AI entries logged yet.")
        return

    st.markdown("<div class='section-label'>📈 Human Feedback Telemetry</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Audited Cases", len(rows))
    with m2:
        st.metric("Accepted As-Is", len([r for r in rows if r["human_decision"] == "ACCEPT"]))
    with m3:
        st.metric("Human Corrections", len([r for r in rows if r["human_decision"] == "EDIT"]))
    with m4:
        st.metric("Rejections", len([r for r in rows if r["human_decision"] == "REJECT"]))

    st.markdown("<div class='section-label'>📜 Continuous Learning Feed</div>", unsafe_allow_html=True)
    for r in rows:
        icon = "✅" if r["human_decision"] == "ACCEPT" else "✏️" if r["human_decision"] == "EDIT" else "❌"
        with st.expander(f"{icon} {r['case_id']} — Decision: {r['human_decision']}"):
            st.markdown(f"**Original AI Diagnosis:** {r['ai_diagnosis']}")
            if r["corrected_diagnosis"]:
                st.markdown(f"**Corrected Diagnosis:** {r['corrected_diagnosis']}")
            st.markdown(f"**Reason for Correction:** {r['reason_for_correction']}")
            st.markdown(f"**Key Engineering Lesson:** {r['lesson']}")


def main():
    """Main routing and modern sidebar."""
    # Custom Brand Box in Sidebar
    st.sidebar.markdown(
        """
        <div class='sidebar-brand-card'>
            <div class='sidebar-brand-title'>🛰️ NetSage AI</div>
            <div class='sidebar-brand-tag'>Network Diagnostic Engine</div>
            <div class='system-status-pill'>
                <span class='pulse-dot'></span>
                <span>SYSTEM ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    page = st.sidebar.radio(
        "Navigation",
        nav_items,
        index=nav_items.index(default_nav) if default_nav in nav_items else 0,
        label_visibility="collapsed",
    )

    # Sidebar Telemetry Widget
    try:
        val = metrics()
        st.sidebar.markdown(
            f"""
            <div class='sidebar-telemetry'>
                <div style='font-weight:700; color:#cbd5e1; margin-bottom:0.4rem;'>📡 LIVE TELEMETRY</div>
                <div class='telemetry-item'><span>Total Cases:</span> <span class='telemetry-val'>{val['total_cases']}</span></div>
                <div class='telemetry-item'><span>Agreement Rate:</span> <span class='telemetry-val'>{val['agreement_pct']}%</span></div>
                <div class='telemetry-item'><span>Engine Mode:</span> <span class='telemetry-val'>{'LIVE AI' if os.getenv('AI_API_KEY') else 'LOCAL DEMO'}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        pass

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
                <p>Evidence-backed network troubleshooting platform designed for Cisco laboratories and enterprise networks.</p>
            </div>
            <div style='background:rgba(30, 41, 59, 0.5); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:1.75rem; line-height:1.6;'>
                <h3>Core Principles</h3>
                <p><strong>1. Strict Grounding:</strong> Diagnoses are tied directly to cited lines in <code>show</code> command output.</p>
                <p><strong>2. Deterministic Verification:</strong> Common misconfigurations (like MTU mismatches, duplicate IPs, or trunk native VLAN discrepancies) are validated by algorithmic rule checkers.</p>
                <p><strong>3. Human-In-The-Loop:</strong> No automated fix is executed without an engineer evaluating and approving the diagnosis.</p>
                <p><strong>4. Responsible Learning:</strong> Audits capture every human override to continuously measure and improve accuracy.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    pages[page]()


if __name__ == "__main__":
    main()

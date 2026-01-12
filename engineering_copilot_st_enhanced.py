import streamlit as st
from openai import OpenAI
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# ============================
# Configuration & Constants
# ============================

st.set_page_config(
    page_title="Storage Engineering AI Assistant",
    layout="wide"
)

# GLOBAL WARNING – ALWAYS VISIBLE
st.markdown("### ⚠️ Important Notice ")
st.warning(
    "Advisory tool only. "
    "**Do not paste user data, credentials, personally identifiable information (PII)**. "
    "Do not any confidential and strictly confidential information. "
    "All outputs must be independently reviewed and validated. "
)

# Constants
MAX_INPUT_LENGTH = 5000
MAX_OUTPUT_TOKENS = 1500         # Reduced default for output tokens (practical balance)
MODEL_VERSION = "gpt-4o-mini"  

# ============================
# Session State Initialization (minimal - only for token tracking)
# ============================
if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"total_tokens": 0, "requests": 0}

# ============================
# Secrets and API Client Initialization
# ============================

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Please add it to your Streamlit secrets.")
    st.info("Create a secrets.toml in UI or locally with in .streamlit/secrets.toml with: OPENAI_API_KEY = 'YOUR_API_KEY'")
    st.stop()

# Initialize the OpenAI client with the API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
VENDORS = ["NetApp ONTAP", "Pure FlashArray", "Dell EMC PowerMax"]
TAB_NAMES = ["📊 Management Dashboard", "💾 Storage Engineering"]

# ============================
# 12 Use cases : (English display, German display). 
# English key for prompt lookup, same applies for other langauages es, fr, ja or zh
# ============================
USE_CASES = [
    ("Explain Issue and Error", "Explain Issue and Error", "Problem/Fehler erklären"),
    ("Generate Runbook", "Generate Runbook", "Runbook generieren"),
    ("Generate Incident RCA", "Generate Incident RCA", "Incident RCA generieren"),
    ("Capacity Planning", "Capacity Planning", "Kapazitätsplanung"),
    ("Performance Analysis", "Performance Analysis", "Performance-Analyse"),
    ("DR Test Planning", "DR Test Planning", "DR-Testplanung"),
    ("Storage Migration", "Storage Migration", "Storage-Migration"),
    ("Generate Ansible Playbook", "Generate Ansible Playbook", "Ansible Playbook generieren"),
    ("Generate Change Request Documentation", "Generate Change Request Documentation", "Change Request Dokumentation generieren"),
    ("Storage Compliance & Audit Evidence", "Storage Compliance & Audit Evidence", "Storage Compliance & Audit-Nachweise"),
    ("Cross-Vendor Migration", "Cross-Vendor Migration Plan", "Herstellerübergreifende Migration"),
    ("Decommissioning & Data Retirement Procedure", "Decommissioning Procedure", "Decommissioning & Datenrückgabe Prozedur"),
]

# ============================
# Translations
# ============================
TRANSLATIONS = {
    "English": {
        "page_title": "🧠 Storage Engineering AI Assistant",
        "page_caption": "Engineering copilot for Storage teams in Banking",
        "sidebar_header": "ℹ️ Demo Info",
        "sidebar_audience": "**Audience**\n- Storage Engineering\n- Management\n- Audit & Compliance Teams",
        "sidebar_vendors": "**Vendors Covered**\n- NetApp ONTAP\n- Pure FlashArray\n- Dell EMC PowerMax",
        "language_label": "🌍 Select Language / Sprache wählen",
        "metrics": ["Supported Vendors", "Use Cases", "Engineers Impacted", "Time Saved (Est.)"],
        "dashboard_title": "📊 Engineering AI Usage Overview",
        "storage_title": "💾 Storage Engineering Assistant",
        "vendor_label": "Select Storage Vendor",
        "task_label": "Select Use Case",
        "input_label": "Input (error message, requirement, incident notes, CR details, audit question, etc.)",
        "button_label": "Run AI Assistant",
        "output_title": "✅ AI Output",
        "spinner_text": "Generating response...",
        "warning_empty_input": "Please provide input before running the assistant.",
        "warning_input_too_long": f"Input too long. Maximum {MAX_INPUT_LENGTH} characters allowed.",
        "demo_note": "⚠️ Demo note: Advisory only — No automation or direct system changes.",
        "solves_title": "🎯 What This Solves",
        "solves_list": [
            "Faster troubleshooting of storage issues",
            "Standardized, audit-ready runbooks & procedures",
            "High-quality incident Root Cause Analyses",
            "Better structured Change Requests (CRs)",
            "Compliance & audit evidence preparation",
            "Vendor-aware automation with Ansible",
            "Proactive capacity & performance planning",
            "Ransomware & DR readiness guidance"
        ],
        "workflow_title": "📌 Typical Workflow",
        "workflow_steps": [
            "Paste error message, requirement, audit question or CR details",
            "Select vendor and use-case",
            "AI generates professional, banking-compliant output",
            "Engineer reviews, validates and applies"
        ],
        "footer": "Demo generated on {date} | Always validate AI outputs in regulated banking environment",
        "export_label": "Export Output",
        "copy_label": "Copy to Clipboard",
        "char_count": "Characters: {count}/{max}",
        "token_info": "Tokens: {tokens} | Requests: {requests}"
    },

    "German / Deutsch": {
        "page_title": "🧠 Storage Engineering KI-Assistent",
        "page_caption": "Engineering Copilot für Storage-Teams im Banking-Umfeld",
        "sidebar_header": "ℹ️ Demo-Informationen",
        "sidebar_audience": "**Zielgruppe**\n- Storage Engineering\n- Management\n- Audit & Compliance Teams",
        "sidebar_vendors": "**Unterstützte Speicherhersteller**\n- NetApp ONTAP\n- Pure FlashArray\n- Dell EMC PowerMax",
        "language_label": "🌍 Sprache wählen / Select Language",
        "metrics": ["Unterstützte Hersteller", "Anwendungsfälle", "Betroffene Engineers", "Zeitersparnis (geschätzt)"],
        "dashboard_title": "📊 Übersicht zur Nutzung der Engineering KI",
        "storage_title": "💾 Storage Engineering Assistent",
        "vendor_label": "Speicherhersteller auswählen",
        "task_label": "Anwendungsfall auswählen",
        "input_label": "Eingabe (Fehlermeldung, Anforderung, Incident-Notizen, CR-Details, Audit-Frage usw.)",
        "button_label": "KI-Assistent starten",
        "output_title": "✅ KI-Ergebnis",
        "spinner_text": "Antwort wird generiert...",
        "warning_empty_input": "Bitte geben Sie eine Eingabe ein, bevor Sie den Assistenten starten.",
        "warning_input_too_long": f"Eingabe zu lang. Maximum {MAX_INPUT_LENGTH} Zeichen erlaubt.",
        "demo_note": "⚠️ Demo-Hinweis: Nur beratend — Keine Automatisierung oder direkte Systemänderungen.",
        "solves_title": "🎯 Was diese Anwendung löst",
        "solves_list": [
            "Schnellere Fehleranalyse bei Storage-Problemen",
            "Standardisierte, prüffähige Runbooks & Verfahren",
            "Hochwertige Incident Root Cause Analysen",
            "Besser strukturierte Change Requests (CRs)",
            "Vorbereitung von Compliance- & Audit-Nachweisen",
            "Herstellerspezifische Automatisierung mit Ansible",
            "Proaktive Kapazitäts- & Performance-Planung",
            "Ransomware-Schutz & DR-Vorbereitung"
        ],
        "workflow_title": "📌 Typischer Arbeitsablauf",
        "workflow_steps": [
            "Fehlermeldung, Anforderung, Audit-Frage oder CR-Details einfügen",
            "Hersteller und Anwendungsfall auswählen",
            "KI erstellt professionelle, bankenkonforme Ausgabe",
            "Engineer prüft, validiert und setzt um"
        ],
        "footer": "Demo erstellt am {date} | KI-Ausgaben in reguliertem Bankenumfeld immer prüfen",
        "export_label": "Ausgabe exportieren",
        "copy_label": "In Zwischenablage kopieren",
        "char_count": "Zeichen: {count}/{max}",
        "token_info": "Tokens: {tokens} | Anfragen: {requests}"
    }
}
# ============================
# Global System Prompt 
# ============================

SYSTEM_PROMPT = """
You are a Senior Storage Engineer & Architect with 20+ years of experience in large-scale, highly regulated banking environments (European global systemically important bank - G-SIB).
You have deep expertise in NetApp ONTAP, Pure Storage FlashArray//X, Dell EMC PowerMax and storage-related automation (Ansible).

Your responses must be:
- Precise, professional and audit-ready
- Always consider banking regulatory requirements (DORA, BaFin, ECB, MaRisk, GDPR, 4-eyes principle, strict change management, traceability)
- Use formal technical language suitable for L3 engineers, architects and auditors
- Provide step-by-step clarity when giving procedures
- Include risk considerations, rollback options and validation steps where appropriate
- Always respond in {response_language}
"""

# ============================
# Prompt Templates (keys = English internal name in use_cases)
# ============================
PROMPT_TEMPLATES = {
    "Explain Issue and Error": """
Explain the following issue clearly for {vendor}.

Include:
- What happened (symptoms and timeline)
- Likely root cause(s)
- Immediate remediation steps
- Preventive best practices
- Validation checks after remediation

Issue details:
{user_input}
""",

    "Generate Runbook": """
Create a detailed engineering runbook for the following task on {vendor}.

Include:
- Purpose and scope
- Preconditions and assumptions
- Step-by-step execution procedure
- Validation and success checks
- Rollback and recovery steps
- Risks and mitigation measures
Task:
{user_input}
""",

    "Generate Incident RCA": """
Generate a professional incident Root Cause Analysis for {vendor}.
Include:
- Incident summary
- Timeline of events
- Technical root cause
- Business and technical impact
- Corrective actions taken
- Preventive actions and long-term improvements
- Lessons learned
Incident details:
{user_input}
""",

    "Capacity Planning": """
Perform capacity planning analysis for {vendor}.
Include: 
- Current capacity usage and utilization trends
- Growth assumptions and projections
- Performance and tiering considerations
- Capacity thresholds and risk points
- Procurement and expansion timeline
- High-level cost estimation
Requirements:
{user_input}
""",

    "Performance Analysis": """
Analyze performance issues on {vendor}.
Include: 
- Observed symptoms and affected workloads
- Key performance metrics to review
- Likely bottlenecks and constraints
- Recommended tuning and configuration changes
- Monitoring and alerting improvements
- Validation steps after optimization
Performance data:
{user_input}
""",

    "DR Test Planning": """
Create a Disaster Recovery test plan for {vendor}.
Include: 
- Test objectives and success criteria
- Scope and systems included
- Detailed test procedures
- Roles and responsibilities
- Rollback and failback steps
- Evidence and documentation requirements
DR environment:
{user_input}
""",

    "Storage Migration": """
Create a storage migration plan for {vendor} within the same vendor or platform family.
Include: 
- Migration scope and objectives
- Pre-migration checks and prerequisites
- Migration strategy and approach
- Step-by-step migration procedure
- Data validation and consistency checks
- Post-migration activities
- Risks, mitigations, and rollback strategy
Migration details:
{user_input}
""",

    "Generate Ansible Playbook": """
Generate a production-ready Ansible playbook for {vendor}.
Include:
- Variables and inputs required
- Clearly named and structured tasks
- Idempotent logic and error handling
- Use of appropriate vendor modules
- Comments explaining critical steps

Constraints:
- Follow Ansible best practices
- Do not include explanatory text outside YAML

User requirement:
{user_input}

Output:
- YAML playbook only
""",

    "Generate Change Request Documentation": """
Create a professional, audit-ready Change Request (CR) document section for {vendor}.
Include:
- Change title and CR reference placeholder
- Business and technical justification
- Risk assessment and mitigation
- Detailed implementation steps
- Backout and recovery plan
- Impacted systems and outage window
- Required approvals (CAB, 4-eyes principle)
- Post-implementation validation steps
Change description:
{user_input}
""",

    "Storage Compliance & Audit Evidence": """
Act as a storage compliance specialist in a European global bank.
Generate audit-compliant documentation/explanation for the following storage-related audit topic on {vendor}.
Include:
- Relevant regulatory references (DORA, BaFin, ECB, GDPR)
- Current configuration/status explanation
- Evidence collection steps (commands/reports)
- Gap analysis (if any)
- Remediation recommendations
Audit question or topic:
{user_input}
""",

    "Cross-Vendor Migration": """
Create a detailed cross-vendor storage migration plan from current {vendor} to a different platform (NetApp ONTAP / Pure FlashArray / PowerMax).
- Current-state assessment and constraints
- Target platform recommendation and justification
- Compatibility and interoperability considerations
- Chosen migration strategy (host-based, replication, tools, etc.)
- High-level step-by-step migration workflow
- Data validation and cutover approach
- Rollback and fallback strategy
- Timeline, effort estimation, and risks

Migration context:
{user_input}
""",

    "Decommissioning & Data Retirement Procedure": """
Create a secure, compliant decommissioning and data retirement procedure for {vendor} in a banking environment.

Include:
- Scope and assets involved
- Pre-decommissioning checks
- Data sanitization method and standards
- Validation and evidence for auditors
- Documentation and sign-off requirements
- Stakeholder notification steps

Decommissioning scope:
{user_input}
"""
}

# ============================
# Helper Functions
# ============================

def get_displayed_use_cases(language: str) -> list:
    idx = 1 if language == "English" else 2
    return [case[idx] for case in USE_CASES]

def get_task_key_from_display(display_name: str, language: str) -> Optional[str]:
    for key, en, de in USE_CASES:
        if (language == "English" and display_name == en) or (language == "German / Deutsch" and display_name == de):
            return key
    return None

def validate_input(user_input: str) -> Tuple[bool, Optional[str]]:
    if not user_input.strip():
        return False, "empty"
    if len(user_input) > MAX_INPUT_LENGTH:
        return False, "too_long"
    return True, None

def ask_llm(prompt: str, language: str, temperature: float = 0.25, top_p: float = 0.90, max_tokens: Optional[int] = None) -> Tuple[Optional[str], Optional[Dict]]:
    """Call OpenAI API with defensive parsing and robust token accounting.

    This function tolerates multiple response shapes (dict-like or SDK objects),
    safely extracts content, usage and model name, and updates Streamlit token accounting
    without raising on unexpected/missing fields.
    """
    response_language = "German" if language == "German / Deutsch" else "English"
    full_system = SYSTEM_PROMPT.format(response_language=response_language)

    # Use provided max_tokens or fallback to global constant
    requested_max_tokens = max_tokens or MAX_OUTPUT_TOKENS

    try:
        response = client.chat.completions.create(
            model=MODEL_VERSION,
            messages=[
                {"role": "system", "content": full_system},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=requested_max_tokens,
            top_p=top_p,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # --- Defensive extractors ---
        def _get_attr_or_key(obj, key, default=None):
            try:
                if obj is None:
                    return default
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            except Exception:
                return default

        # Model name
        model_name = _get_attr_or_key(response, "model", None)

        # Usage extraction - result as a dict if possible
        usage_raw = _get_attr_or_key(response, "usage", {}) or {}
        usage = {}
        try:
            # If it's an SDK object with model_dump / dict method
            if hasattr(usage_raw, "model_dump"):
                usage = usage_raw.model_dump() or {}
            elif hasattr(usage_raw, "to_dict"):
                usage = usage_raw.to_dict() or {}
            elif isinstance(usage_raw, dict):
                usage = usage_raw
            else:
                # Last resort: try to convert
                usage = dict(usage_raw) if usage_raw else {}
        except Exception:
            usage = usage_raw if isinstance(usage_raw, dict) else {}

        # Extract total tokens robustly
        total_tokens = 0
        for k in ("total_tokens", "total", "completion_tokens"):
            try:
                v = usage.get(k) if isinstance(usage, dict) else None
                if v is not None:
                    total_tokens = int(v)
                    break
            except Exception:
                continue

        # Content extraction - support multiple shapes:
        content = None
        choices = _get_attr_or_key(response, "choices", None)
        if choices:
            try:
                first = choices[0]
                # If first is dict-like
                if isinstance(first, dict):
                    # new-format: message -> content
                    content = first.get("message", {}).get("content") or first.get("text") or first.get("content")
                else:
                    # SDK object - try message.content then text
                    msg = _get_attr_or_key(first, "message", None)
                    content = _get_attr_or_key(msg, "content", None) or _get_attr_or_key(first, "text", None)
            except Exception:
                content = None

        # Fallback content locations
        if content is None:
            content = _get_attr_or_key(response, "text", None) or _get_attr_or_key(response, "content", None)

        # Build metadata (safe)
        metadata = {
            "model": model_name or "unknown",
            "usage": usage if isinstance(usage, dict) else {},
            "requested_max_tokens": requested_max_tokens,
            "timestamp": datetime.now().isoformat()
        }

        # --- Safe session token accounting ---
        try:
            # ensure session_state keys exist
            if "token_usage" not in st.session_state:
                st.session_state.token_usage = {"total_tokens": 0, "requests": 0}

            st.session_state.token_usage["total_tokens"] = st.session_state.token_usage.get("total_tokens", 0) + int(total_tokens or 0)
            st.session_state.token_usage["requests"] = st.session_state.token_usage.get("requests", 0) + 1
        except Exception:
            # Never let accounting errors crash the app; log server-side if available
            try:
                st.warning("Token accounting failed to update; check server logs.")
            except Exception:
                pass

        # Return the best effort content + metadata
        return content, metadata

    except Exception as e:
        # Classify and show user-friendly messages, without exposing internals
        error_type = type(e).__name__
        error_message = str(e).lower()

        if "rate" in error_message or "ratelimit" in error_type.lower() or "rate_limit" in error_message:
            st.error("⚠️ API rate limit exceeded. Please wait a moment and try again.")
        elif "auth" in error_message or "authentication" in error_type.lower():
            st.error("⚠️ Authentication error. Please check your API key configuration.")
        elif "connection" in error_message or "apiconnectionerror" in error_type.lower():
            st.error("⚠️ Network connection error. Please check your internet connection.")
        elif "invalid" in error_message or "invalidrequesterror" in error_type.lower():
            st.error(f"⚠️ Invalid request: {str(e)}")
        else:
            # Generic fallback
            st.error(f"⚠️ Error contacting OpenAI API: {str(e)}")

        return None, None

# ============================
# UI Sidebar & Language Setup
# ============================
language = st.sidebar.radio(
    "🌍 Select Language / Sprache wählen",
    ["English", "German / Deutsch"],
    horizontal=True,
    key="language_selector"
)

lang = TRANSLATIONS.get(language, TRANSLATIONS["English"])

st.sidebar.header(lang.get("sidebar_header", "ℹ️ Demo Info"))
st.sidebar.markdown(lang.get("sidebar_audience"))
st.sidebar.markdown(lang.get("sidebar_vendors"))

st.sidebar.markdown("---")
st.sidebar.caption(lang["token_info"].format(
    tokens=st.session_state.token_usage["total_tokens"],
    requests=st.session_state.token_usage["requests"]
))

st.title(lang.get("page_title"))
st.caption(lang.get("page_caption"))

# ============================
# Tabs
# ============================
tab_dashboard, tab_storage = st.tabs(TAB_NAMES)

# ============================
# Management Dashboard Tab - No LLM 
# ============================
with tab_dashboard:
    st.subheader("Management Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Supported Vendors", len(VENDORS))
    col2.metric("Use Cases", len(USE_CASES))
    col3.metric("Engineers Impacted", "Storage Team")
    col4.metric("Time Saved (Est.)", "30–60%")
    st.info("Advisory tool only — always validate outputs.")

# ============================
# Engineering Dashboard Tab 
# ============================
with tab_storage:
    st.subheader(lang.get("storage_title"))
    
    vendor = st.selectbox(lang.get("vendor_label", "Storage Vendor"), VENDORS)
    
    displayed_tasks = get_displayed_use_cases(language)
    selected_task = st.selectbox(lang.get("task_label", "Use Case"), displayed_tasks)
    
    task_key = get_task_key_from_display(selected_task, language)
    
    st.markdown("### Generation Settings")
    col1, col2 = st.columns([5, 4])
    
    with col1:
        temperature = st.slider(
            "Temperature (determinism vs creativity)",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.05,
            help="0.0–0.3 → very precise & repeatable\n0.4–0.6 → balanced\n0.7+ → more creative"
        )
        top_p = st.slider(
            "Top-p (nucleus sampling)",
            min_value=0.70,
            max_value=0.98,
            value=0.90,
            step=0.02,
            help="Lower = more focused\n0.85–0.92 recommended for most banking tasks"
        )
    
    with col2:
        st.info("""
        **Recommended settings for banking use-cases:**
        • Procedures, CRs, Compliance, Runbooks → **0.15–0.30** temp / **0.82–0.90** top_p
        • RCA, Troubleshooting → **0.25–0.40** temp / **0.88–0.93** top_p
        • Brainstorming / alternatives → **0.50–0.75** temp / **0.92–0.96** top_p
        """)
    
    # Input & Generation
    user_input = st.text_area(
        lang.get("input_label", "Your input..."),
        height=180,
        help=f"Max {MAX_INPUT_LENGTH} characters",
        key="storage_input"
    )
    
    # Character counter
    char_count = len(user_input) if user_input else 0
    char_color = "green" if char_count <= MAX_INPUT_LENGTH else "red"
    st.caption(f'<span style="color:{char_color}">{lang["char_count"].format(count=char_count, max=MAX_INPUT_LENGTH)}</span>', unsafe_allow_html=True)
    
    if st.button(lang.get("button_label", "Generate →"), type="primary"):
        is_valid, error_type = validate_input(user_input)
        
        if not is_valid:
            if error_type == "empty":
                st.warning(lang.get("warning_empty_input"))
            else:
                st.warning(lang.get("warning_input_too_long"))
        elif not task_key or task_key not in PROMPT_TEMPLATES:
            st.error("Selected task not implemented.")
        else:
            prompt = PROMPT_TEMPLATES[task_key].format(vendor=vendor, user_input=user_input)
            
            with st.spinner(lang.get("spinner_text", "Generating...")):
                # Pass the new default explicitly
                result, metadata = ask_llm(prompt, language, temperature, top_p, max_tokens=MAX_OUTPUT_TOKENS)
            
            if result:
                if metadata:
                    total_tokens_display = metadata.get('usage', {}).get('total_tokens', 'N/A')
                    st.caption(f"Model: {metadata.get('model', 'unknown')} • Tokens: {total_tokens_display}")
                
                with st.expander(lang.get("output_title", "Result"), expanded=True):
                    if task_key == "Generate Ansible Playbook":
                        st.code(result, language="yaml")
                    else:
                        st.markdown(result)
                    
                    # Action buttons
                    col_export, col_copy = st.columns(2)
                    
                    with col_export:
                        st.download_button(
                            label=lang.get("export_label", "Export"),
                            data=result,
                            file_name=f"storage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                    with col_copy:
                        # Simple copy instruction - Streamlit doesn't support direct clipboard access
                        st.info("💡 Select the text above and use Ctrl+C (Cmd+C on Mac) to copy")

# Footer
st.markdown("---")
date_str = datetime.now().strftime("%d %b %Y %H:%M") if language == "English" else datetime.now().strftime("%d.%m.%Y %H:%M")
st.caption(f"Demo — {date_str} | Advisory only — Always validate outputs")

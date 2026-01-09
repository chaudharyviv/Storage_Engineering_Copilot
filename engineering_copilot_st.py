import streamlit as st
from openai import OpenAI
from datetime import datetime

# ============================
# Configuration & Constants
# ============================

st.set_page_config(
    page_title="Storage Engineering AI Assistant",
    layout="wide"
)
# ============================
# Secrets and API Client Initialization
# ============================

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OpenAI API key not found. Please add it to your Streamlit secrets.")
    st.info("Create a file .streamlit/secrets.toml with: OPENAI_API_KEY = 'YOUR_API_KEY'")
    st.stop()

# Initialize the OpenAI client with the API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

VENDORS = ["NetApp ONTAP", "Pure FlashArray", "Dell EMC PowerMax"]

TAB_NAMES = ["📊 Management Dashboard", "💾 Storage Engineering"]

# Use cases: (English key, English display, German display). English key is used internally for prompt lookup


USE_CASES = [
    ("Explain Issue and Error", "Explain Issue and Error", "Problem/Fehler erklären"),
    ("Generate Runbook", "Generate Runbook", "Runbook generieren"),
    ("Generate Incident RCA", "Generate Incident RCA", "Incident RCA generieren"),
    ("Capacity Planning", "Capacity Planning", "Kapazitätsplanung"),
    ("Performance Analysis", "Performance Analysis", "Performance-Analyse"),
    ("DR Test Planning", "DR Test Planning", "DR-Testplanung"),
    ("Storage Migration", "Storage Migration", "Storage-Migration"),
    ("Generate Ansible Playbook", "Generate Ansible Playbook", "Ansible Playbook generieren"),
]

# ============================
# Translations
# ============================
TRANSLATIONS = {
    "English": {
        "page_title": "🧠 Storage Engineering AI Assistant",
        "page_caption": "Engineering copilot for Storage teams",
        "sidebar_header": "ℹ️ Demo Info",
        "sidebar_audience": "**Audience**\n- Storage Engineering\n- Management",
        "sidebar_vendors": "**Vendors Covered**\n- NetApp\n- Pure FlashArray\n- Dell EMC PowerMax",
        "language_label": "🌍 Select Language / Sprache wählen",
        "metrics": ["Supported Vendors", "Use Cases", "Engineers Impacted", "Time Saved (Est.)"],
        "dashboard_title": "📊 Engineering AI Usage Overview",
        "storage_title": "💾 Storage Engineering Assistant",
        "vendor_label": "Select Storage Vendor",
        "task_label": "Select Use Case",
        "input_label": "Input (error, requirement, incident notes, or playbook goal)",
        "button_label": "Run AI Assistant",
        "output_title": "✅ AI Output",
        "spinner_text": "Generating response...",
        "warning_empty_input": "Please provide input before running the assistant.",
        "demo_note": "⚠️ Demo note: No automation or API execution — advisory only.",
        "solves_title": "🎯 What This Solves",
        "solves_list": [
            "Faster troubleshooting",
            "Standardized runbooks",
            "Cleaner incident RCAs",
            "Better automation with Ansible",
            "Vendor-aware responses",
            "Automated documentation",
            "Proactive capacity planning"
        ],
        "workflow_title": "📌 Typical Workflow",
        "workflow_steps": [
            "Engineer pastes error / requirement",
            "Selects vendor & task",
            "AI generates engineering-grade output",
            "Engineer validates & executes"
        ],
        "footer": "Demo generated on {date}",
    },
    "German / Deutsch": {
        "page_title": "🧠 Storage Engineering KI-Assistent",
        "page_caption": "Engineering Copilot für Storage-Teams",
        "sidebar_header": "ℹ️ Demo Info",
        "sidebar_audience": "**Zielgruppe**\n- Storage Engineering\n- Management",
        "sidebar_vendors": "**Unterstützte Hersteller**\n- NetApp ONTAP\n- Pure FlashArray\n- Dell EMC PowerMax",
        "language_label": "🌍 Select Language / Sprache wählen",
        "metrics": ["Unterstützte Hersteller", "Anwendungsfälle", "Betroffene Engineers", "Zeitersparnis (geschätzt)"],
        "dashboard_title": "📊 Engineering KI-Nutzungsübersicht",
        "storage_title": "💾 Storage Engineering Assistant",
        "vendor_label": "Storage-Hersteller wählen",
        "task_label": "Anwendungsfall wählen",
        "input_label": "Eingabe (Fehler, Anforderung, Incident-Notizen oder Playbook-Ziel)",
        "button_label": "KI-Assistent ausführen",
        "output_title": "✅ KI-Ausgabe",
        "spinner_text": "Antwort wird generiert...",
        "warning_empty_input": "Bitte geben Sie eine Eingabe ein, bevor Sie den Assistenten ausführen.",
        "demo_note": "⚠️ Demo-Hinweis: Keine Automatisierung oder API-Ausführung — nur beratend.",
        "solves_title": "🎯 Was dies löst",
        "solves_list": [
            "Schnellere Fehlerbehebung",
            "Standardisierte Runbooks",
            "Bessere Incident RCAs",
            "Bessere Automatisierung mit Ansible",
            "Herstellerspezifische Antworten",
            "Automatisierte Dokumentation",
            "Proaktive Kapazitätsplanung"
        ],
        "workflow_title": "📌 Typischer Arbeitsablauf",
        "workflow_steps": [
            "Engineer fügt Fehler/Anforderung ein",
            "Wählt Hersteller & Aufgabe",
            "KI generiert engineering-taugliche Ausgabe",
            "Engineer validiert & führt aus"
        ],
        "footer": "Demo erstellt am {date}",
    }
}

# ============================
# Prompt Templates (keys = English internal name)
# ============================
PROMPT_TEMPLATES = {
    "Explain Issue and Error": """
You are a senior storage engineer specializing in {vendor}.
Explain the following issue clearly.

Include:
- What happened
- Likely root cause
- Immediate remediation
- Preventive best practices

Issue:
{user_input}
""",
    "Generate Runbook": """
Create a detailed engineering runbook for the following task on {vendor}.

Include:
- Preconditions
- Step-by-step procedure
- Validation checks
- Rollback steps

Task:
{user_input}
""",
    "Generate Incident RCA": """
You are a storage SME.
Generate a professional incident RCA for {vendor}.

Include:
- Summary
- Root cause
- Impact
- Corrective actions
- Preventive actions

Incident details:
{user_input}
""",
    "Capacity Planning": """
Perform capacity planning analysis for {vendor} based on the following requirements.

Include:
- Current usage analysis
- Growth projection
- Storage tier recommendations
- Procurement timeline
- Cost estimation

Requirements:
{user_input}
""",
    "Performance Analysis": """
Analyze performance issues for {vendor} storage system.

Include:
- Performance metrics analysis
- Bottleneck identification
- Tuning recommendations
- Monitoring setup
- Alert thresholds

Performance data:
{user_input}
""",
    "DR Test Planning": """
Create a Disaster Recovery test plan for {vendor} environment.

Include:
- Test objectives
- Scope and limitations
- Test procedures
- Success criteria
- Rollback procedures
- Documentation requirements

DR environment:
{user_input}
""",
    "Storage Migration": """
Create a storage migration plan for {vendor} to new platform/version.

Include:
- Pre-migration checks
- Migration strategy
- Step-by-step migration procedure
- Validation steps
- Post-migration tasks
- Risk mitigation

Migration details:
{user_input}
""",
    "Generate Ansible Playbook": """
You are a senior storage automation engineer expert in Ansible and {vendor}.

Generate a complete, production-ready Ansible playbook based on the following requirement.

Requirements:
- Use best practices (idempotency, error handling, registers, conditionals)
- Include meaningful task names
- Use appropriate modules for {vendor} (e.g., na_ontap_*, purefa_*, dellemc_powermax_* if applicable)
- Add comments where helpful
- Structure with roles if it makes sense, otherwise a single playbook
- Include variables section at the top or suggest a separate vars file

User requirement:
{user_input}

Output only the YAML playbook (no explanations outside the code).
""",
}

# ============================
# Helper Functions
# ============================
def get_displayed_use_cases(language: str):
    """Return list of use case names in the selected language"""
    idx = 1 if language == "English" else 2
    return [case[idx] for case in USE_CASES]

def get_task_key_from_display(display_name: str, language: str):
    """Map displayed name back to internal English key"""
    idx = 1 if language == "English" else 2
    for key, en, de in USE_CASES:
        if (language == "English" and display_name == en) or (language == "German / Deutsch" and display_name == de):
            return key
    return None

def ask_llm(prompt: str, language: str, temperature: float = 0.2) -> str | None:
    response_language = "German" if language == "German / Deutsch" else "English"
    system_message = (
        f"You are a senior storage engineer expert. "
        f"Always respond professionally, concisely, and entirely in {response_language}. "
        f"Use technical storage terminology appropriate for experienced engineers."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=3000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error contacting OpenAI API: {str(e)}")
        return None

# ============================
# Sidebar & Language Setup
# ============================
language = st.sidebar.radio(
    TRANSLATIONS["English"]["language_label"],
    ["English", "German / Deutsch"],
    horizontal=True
)

lang = TRANSLATIONS[language]

st.sidebar.header(lang["sidebar_header"])
st.sidebar.markdown(lang["sidebar_audience"])
st.sidebar.markdown(lang["sidebar_vendors"])

st.title(lang["page_title"])
st.caption(lang["page_caption"])

# ============================
# Tabs
# ============================
tab_dashboard, tab_storage = st.tabs(TAB_NAMES)

# ============================
# Management Dashboard Tab
# ============================
with tab_dashboard:
    st.subheader(lang["dashboard_title"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(lang["metrics"][0], len(VENDORS))
    col2.metric(lang["metrics"][1], len(USE_CASES))
    col3.metric(lang["metrics"][2], "Storage Engineers")
    col4.metric(lang["metrics"][3], "30–50%")

    st.markdown("---")
    st.subheader(lang["solves_title"])
    st.markdown("\n".join(f"- {item}" for item in lang["solves_list"]))

    st.subheader(lang["workflow_title"])
    st.markdown("\n".join(f"{i+1}. {step}" for i, step in enumerate(lang["workflow_steps"])))

    st.info(lang["demo_note"])

# ============================
# Storage Engineering Tab
# ============================
with tab_storage:
    st.subheader(lang["storage_title"])

    vendor = st.selectbox(lang["vendor_label"], VENDORS)

    displayed_use_cases = get_displayed_use_cases(language)
    displayed_task = st.selectbox(lang["task_label"], displayed_use_cases)

    task_key = get_task_key_from_display(displayed_task, language)

    user_input = st.text_area(lang["input_label"], height=200, key="user_input")

    if st.button(lang["button_label"], key="run_ai"):
        if not user_input.strip():
            st.warning(lang["warning_empty_input"])
        else:
            if not task_key or task_key not in PROMPT_TEMPLATES:
                st.error("Selected task not supported.")
            else:
                prompt = PROMPT_TEMPLATES[task_key].format(vendor=vendor, user_input=user_input)
                with st.spinner(lang["spinner_text"]):
                    output = ask_llm(prompt, language)
                if output:
                    with st.expander(lang["output_title"], expanded=True):
                        if task_key == "Generate Ansible Playbook":
                            st.code(output, language="yaml")
                        else:
                            st.markdown(output)

# ============================
# Footer
# ============================
st.markdown("---")
date_format = '%d %b %Y %H:%M' if language == "English" else '%d.%m.%Y %H:%M'
st.caption(lang["footer"].format(date=datetime.now().strftime(date_format)))
st.caption("This application is based on AI outputs, please use carefully.")

# Storage Engineering AI Assistant

A Streamlit-based AI assistant for storage engineers and management teams in banking environments.  
Uses OpenAI's GPT models to generate vendor-aware, banking-compliant guidance and automation content for common storage engineering tasks.

## 🎯 Overview

This application provides an engineering copilot for storage teams working in highly regulated banking environments. It generates professional, audit-ready documentation including runbooks, incident RCAs, change requests, compliance evidence, and Ansible playbooks.

---

## ✨ Features

### Core Capabilities
- **🌍 Multi-language Support**: Full UI and output in **English** and **German / Deutsch**
- **📊 Management Dashboard**: High-level overview of supported vendors, use cases, and metrics
- **💾 Storage Engineering Assistant**: Vendor-aware AI assistance for 12 different use cases
- **🔧 Advanced Configuration**: Adjustable temperature and top-p parameters for different use case types
- **✅ Input Validation**: Character counter and length validation (max 5,000 characters)
- **📥 Export Functionality**: Download generated outputs as text files
- **📈 Token Usage Tracking**: Real-time tracking of API token consumption
- **🛡️ Enhanced Error Handling**: Specific error messages for rate limits, network issues, authentication errors

### Supported Vendors
- **NetApp ONTAP**
- **Pure FlashArray**
- **Dell EMC PowerMax**

### Supported Use Cases (12 Total)
1. **Explain Issue and Error** - Troubleshooting and error analysis
2. **Generate Runbook** - Step-by-step operational procedures
3. **Generate Incident RCA** - Root Cause Analysis documentation
4. **Capacity Planning** - Capacity analysis and projections
5. **Performance Analysis** - Performance troubleshooting and optimization
6. **DR Test Planning** - Disaster Recovery test procedures
7. **Storage Migration** - Migration planning and procedures
8. **Generate Ansible Playbook** - Production-ready automation code
9. **Generate Change Request Documentation** - Audit-ready CR documentation
10. **Storage Compliance & Audit Evidence** - Regulatory compliance documentation
11. **Cross-Vendor Migration** - Cross-platform migration planning
12. **Decommissioning & Data Retirement Procedure** - Secure decommissioning procedures

---

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **OpenAI API Key**: Required for GPT model access
- **Streamlit**: Web framework for the application

### Python Libraries
- `streamlit` - Web application framework
- `openai` - OpenAI API client

---

## 🚀 Installation

### 1. Clone or Download the Repository

```bash
cd Storage_Engineering_Copilot
```

### 2. Install Dependencies

```bash
pip install streamlit openai
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configure OpenAI API Key

The application uses **Streamlit secrets** for secure API key management.

#### Option A: Streamlit Cloud / Streamlit Community Cloud
1. Go to your app settings
2. Navigate to "Secrets"
3. Add:
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

#### Option B: Local Development
1. Create a `.streamlit` folder in your project root (if it doesn't exist)
2. Create a `secrets.toml` file inside `.streamlit/`
3. Add your API key:
```toml
OPENAI_API_KEY = "sk-your-api-key-here"
```

**Important**: Never commit `secrets.toml` to version control. Add it to `.gitignore`.

---

## 🏃 Running the Application

From the project root directory:

```bash
streamlit run engineering_copilot_st_enhanced.py
```

The application will start and automatically open in your browser at `http://localhost:8501`.

---

## 📖 Usage Guide

### Management Dashboard Tab

View high-level metrics:
- Number of supported vendors
- Total use cases available
- Target audience information
- Estimated time savings

### Storage Engineering Tab

1. **Select Language**: Choose English or German from the sidebar
2. **Choose Vendor**: Select from NetApp ONTAP, Pure FlashArray, or Dell EMC PowerMax
3. **Select Use Case**: Pick from 12 available use cases
4. **Configure Generation Settings** (optional):
   - **Temperature**: Controls determinism vs creativity
     - `0.15-0.30`: Recommended for procedures, CRs, compliance, runbooks
     - `0.25-0.40`: Recommended for RCA and troubleshooting
     - `0.50-0.75`: Recommended for brainstorming and alternatives
   - **Top-p**: Controls nucleus sampling
     - `0.82-0.90`: Recommended for most banking tasks
5. **Enter Input**: Paste your error message, requirement, incident notes, CR details, or audit question
   - Maximum 5,000 characters
   - Character counter shows current usage
6. **Generate**: Click "Run AI Assistant" button
7. **Review Output**: 
   - For Ansible playbooks: YAML code block
   - For other use cases: Formatted markdown documentation
8. **Export** (optional): Download the output as a text file

### Token Usage Tracking

The sidebar displays:
- Total tokens consumed in the current session
- Number of API requests made

---

## ⚙️ Configuration

### Model Settings
Default model: `gpt-4o-mini` (configurable in code)

To change the model, edit the `MODEL_VERSION` constant:
```python
MODEL_VERSION = "gpt-4o"  # or "gpt-4-turbo", etc.
```

### Input Limits
- Maximum input length: 5,000 characters (configurable via `MAX_INPUT_LENGTH`)
- Maximum output tokens: 3,000 (configurable via `MAX_OUTPUT_TOKENS`)

### Customization Options

#### Adding New Use Cases
1. Add entry to `USE_CASES` list: `(internal_key, "English Display", "German Display")`
2. Add corresponding template to `PROMPT_TEMPLATES` dictionary

#### Adding New Vendors
1. Update the `VENDORS` list
2. Update vendor references in prompt templates as needed

#### Modifying System Prompt
Edit the `SYSTEM_PROMPT` constant to change the AI's behavior and expertise level.

#### Adding Languages
1. Add new language entry to `TRANSLATIONS` dictionary
2. Update `get_displayed_use_cases()` function if needed

---

## 🔒 Security & Privacy

### Important Security Notes
- ⚠️ **Advisory Only**: This application does NOT execute any storage operations, scripts, or direct API calls to storage systems
- ⚠️ **No Sensitive Data**: Do NOT paste sensitive production data, credentials, customer PII, or proprietary information
- ⚠️ **API Key Security**: Keep your OpenAI API key secure and never commit it to version control
- ⚠️ **Validation Required**: Always review and validate AI-generated outputs before use in production
- ⚠️ **Banking Compliance**: While outputs are designed for banking environments, they must be reviewed by qualified engineers

### Best Practices
- Use network isolation for production deployments
- Implement input sanitization for sensitive environments
- Consider additional audit logging for compliance requirements
- Review API usage regularly to monitor costs

---

## 🎨 Architecture

### File Structure
```
Storage_Engineering_Copilot/
├── engineering_copilot_st_enhanced.py  # Main application file
├── engineering_copilot_st.py            # Original version (backup)
├── README.MD                            # This file
├── LICENSE                              # License file
└── .streamlit/
    └── secrets.toml                     # API keys (not in repo)
```

### Key Components
- **Constants**: Configuration values (model, limits, vendors)
- **Translations**: Multi-language UI text
- **Prompt Templates**: Use case-specific prompts
- **Helper Functions**: Input validation, API calls, UI utilities
- **Session State**: Token usage tracking (minimal state)

---

## ⚠️ Limitations & Notes

1. **No History**: The application does not save request history or session outputs (by design)
2. **No Follow-up**: Each request is independent; no conversation context is maintained
3. **Advisory Only**: Generated content must be validated by qualified storage engineers
4. **Vendor Modules**: Ansible playbooks reference vendor-specific modules but require validation for your environment
5. **Model Limitations**: Output quality depends on the selected OpenAI model and parameters
6. **Token Limits**: Very long inputs may be truncated or exceed model context windows

---

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure `secrets.toml` exists in `.streamlit/` folder
- Verify the key is correctly formatted: `OPENAI_API_KEY = "sk-..."`
- For Streamlit Cloud, check app settings → Secrets

**"API rate limit exceeded"**
- Wait a few moments and try again
- Check your OpenAI account usage limits
- Consider upgrading your OpenAI plan

**"Network connection error"**
- Check your internet connection
- Verify firewall settings allow OpenAI API access
- Check if you're behind a corporate proxy

**Application not starting**
- Verify all dependencies are installed: `pip install streamlit openai`
- Check Python version: `python --version` (should be 3.9+)
- Review error messages in the terminal

---

## 📝 License

See `LICENSE` file for details.

---

## 🤝 Contributing

This is a demo application for storage engineering teams. For enhancements:
1. Review the code structure
2. Test changes thoroughly
3. Ensure banking compliance considerations are maintained
4. Update documentation as needed

---

## 📧 Support

For issues or questions:
- Review the troubleshooting section above
- Check OpenAI API status
- Validate your configuration setup

---

**Last Updated**: 2024  
**Version**: Enhanced (no history/session features)  
**Model**: GPT-4o-mini (default)

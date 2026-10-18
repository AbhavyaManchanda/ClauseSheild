"""
app.py - Main Streamlit interface for ClauseShield.
A local, privacy-first contract reviewer and clause auditor for freelancers.
"""

import time
import streamlit as st
from analyzer import (
    extract_text_from_pdf,
    check_ollama_status,
    analyze_contract_text,
    DEFAULT_OLLAMA_HOST,
    DEFAULT_MODEL
)

# Page Configuration
st.set_page_config(
    page_title="ClauseShield — Privacy-First Contract Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished desktop feel
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .privacy-badge {
        display: inline-block;
        background-color: #ecfdf5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        border: 1px solid #a7f3d0;
    }
    .risk-card {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


def reset_analysis():
    st.session_state.analysis_result = None
    st.session_state.extracted_data = None
    st.session_state.uploaded_file_name = None


# --- SIDEBAR: Configuration & Health Check ---
with st.sidebar:
    st.image("https://api.iconify.design/lucide:shield-alert.svg?color=%232563eb", width=48)
    st.title("ClauseShield")
    st.caption("v1.0.0 • Freelancer Defense System")

    st.markdown("---")
    st.subheader("⚡ Local LLM Engine")

    ollama_host = st.text_input("Ollama Host URL", value=DEFAULT_OLLAMA_HOST, help="Default is http://localhost:11434")

    # Check Ollama connection
    is_online, available_models, err = check_ollama_status(ollama_host)

    if is_online:
        st.success("🟢 Ollama Service Active", icon="✅")
        if not available_models:
            st.warning("No models found in Ollama. Run: `ollama pull llama3.1`")
            model_options = [DEFAULT_MODEL]
        else:
            # Prefer llama3.1 if present
            default_index = 0
            for idx, m in enumerate(available_models):
                if "llama3.1" in m.lower():
                    default_index = idx
                    break
            model_options = available_models

        selected_model = st.selectbox(
            "Selected Model",
            options=model_options,
            index=default_index,
            help="Llama 3.1 8B or 70B recommended for legal clause parsing"
        )
    else:
        st.error("🔴 Ollama Not Detected", icon="⚠️")
        st.info(
            "**How to start Ollama locally:**\n"
            "1. Download from [ollama.com](https://ollama.com)\n"
            "2. In your terminal, run:\n"
            "   ```bash\n"
            "   ollama serve\n"
            "   ollama pull llama3.1\n"
            "   ```\n"
            "3. Click 'Refresh Connection' below."
        )
        selected_model = DEFAULT_MODEL
        if st.button("🔄 Refresh Connection"):
            st.rerun()

    st.markdown("---")
    st.subheader("🎯 Review Priorities")
    focus_ip = st.checkbox("Intellectual Property & Rights", value=True)
    focus_payment = st.checkbox("Payment Schedules & Net Terms", value=True)
    focus_noncompete = st.checkbox("Non-Competes & Exclusivity", value=True)
    focus_scope = st.checkbox("Scope Creep & Revisions", value=True)
    focus_liability = st.checkbox("Liability & Indemnification", value=True)

    chosen_focus = []
    if focus_ip: chosen_focus.append("IP Ownership & Portfolio Rights")
    if focus_payment: chosen_focus.append("Payment Terms & Late Fees")
    if focus_noncompete: chosen_focus.append("Non-Compete & Exclusivity Restrictions")
    if focus_scope: chosen_focus.append("Scope Creep & Revision Limits")
    if focus_liability: chosen_focus.append("Liability Caps & Mutual Indemnity")

    st.markdown("---")
    st.markdown("### 🔒 Privacy Guarantee")
    st.caption(
        "• **100% Offline Processing**: All text extraction and LLM inference occur strictly on your machine.\n"
        "• **Zero Telemetry**: No contract details, names, or financial terms ever touch an external cloud server.\n"
        "• **No API Keys**: Fully open-weight stack."
    )


# --- MAIN AREA ---
st.markdown('<div class="main-header">🛡️ ClauseShield</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    'Private, local contract reviewer & negotiation copilot for freelancers and independent contractors.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div>'
    '<span class="privacy-badge">🔒 100% Local Inference</span>'
    '<span class="privacy-badge">🚫 Zero Cloud APIs</span>'
    '<span class="privacy-badge">⚖️ Freelancer Protective</span>'
    '<span class="privacy-badge">🦙 Powered by Llama 3.1</span>'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

# File Upload Section
uploaded_file = st.file_uploader(
    "Upload Freelance Contract, SOW, MSA, or NDA (PDF format)",
    type=["pdf"],
    help="Contract text is parsed locally in-memory and never saved to disk or transmitted."
)

if uploaded_file is not None:
    # If a new file is uploaded, reset previous analysis
    if st.session_state.uploaded_file_name != uploaded_file.name:
        reset_analysis()
        st.session_state.uploaded_file_name = uploaded_file.name

        with st.spinner("Extracting text from PDF locally..."):
            try:
                extracted = extract_text_from_pdf(uploaded_file)
                st.session_state.extracted_data = extracted
                st.toast("PDF successfully extracted!", icon="📄")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                st.session_state.extracted_data = None

if st.session_state.extracted_data is not None:
    extracted = st.session_state.extracted_data

    # Document stats metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pages", extracted["pages"])
    with col2:
        st.metric("Word Count", f"{extracted['word_count']:,}")
    with col3:
        st.metric("Characters", f"{extracted['char_count']:,}")
    with col4:
        st.metric("Active Model", selected_model)

    with st.expander("🔍 Preview Extracted Contract Text (Local In-Memory)", expanded=False):
        st.text_area(
            "Extracted Raw Content",
            value=extracted["text"][:4000] + ("\n... [Truncated preview]" if len(extracted["text"]) > 4000 else ""),
            height=250,
            disabled=True
        )

    st.write("")

    # Audit Button
    audit_disabled = not is_online
    btn_label = "🛡️ Audit Contract Locally" if is_online else "⚠️ Ollama Offline - Start Ollama to Audit"

    col_btn, col_reset = st.columns([3, 1])
    with col_btn:
        start_audit = st.button(btn_label, type="primary", use_container_width=True, disabled=audit_disabled)
    with col_reset:
        if st.session_state.analysis_result:
            if st.button("Clear Results", use_container_width=True):
                reset_analysis()
                st.rerun()

    if start_audit:
        st.session_state.analysis_result = ""
        st.markdown("---")
        st.subheader("📊 Audit Progress & Real-Time Analysis")

        report_container = st.empty()
        full_response = ""

        with st.spinner(f"Auditing with {selected_model}... Identifying predatory clauses..."):
            try:
                stream_gen = analyze_contract_text(
                    contract_text=extracted["text"],
                    model=selected_model,
                    host=ollama_host,
                    custom_focus=chosen_focus,
                    stream=True
                )

                for chunk in stream_gen:
                    full_response += chunk
                    report_container.markdown(full_response + " ▌")

                report_container.markdown(full_response)
                st.session_state.analysis_result = full_response
                st.toast("Contract Audit Complete!", icon="🎉")

            except Exception as e:
                st.error(f"Inference error: {str(e)}")
                st.info(
                    "Tip: Make sure you have pulled the model using `ollama pull "
                    f"{selected_model}` and that your local Ollama instance has enough RAM/VRAM."
                )

# Display completed analysis if available in session state
if st.session_state.analysis_result:
    result_text = st.session_state.analysis_result

    st.markdown("---")
    
    # Download & Export Bar
    col_rep_head, col_dl = st.columns([3, 1])
    with col_rep_head:
        st.subheader("📑 Audit Results & Negotiation Kit")
    with col_dl:
        report_filename = f"ClauseShield_Report_{st.session_state.uploaded_file_name.replace('.pdf', '')}.md"
        st.download_button(
            label="💾 Download Markdown Report",
            data=result_text,
            file_name=report_filename,
            mime="text/markdown",
            use_container_width=True
        )

    tab1, tab2 = st.tabs(["📋 Complete Risk Report", "✉️ Negotiation Email Draft"])

    with tab1:
        st.markdown(result_text)

    with tab2:
        # Extract the negotiation email section if present
        email_content = ""
        if "## 4. Client Negotiation Email Draft" in result_text:
            email_section = result_text.split("## 4. Client Negotiation Email Draft")[-1]
            # Strip disclaimer if at end
            if "---" in email_section:
                email_content = email_section.split("---")[0].strip()
            else:
                email_content = email_section.strip()
        else:
            email_content = "Review the complete report in the first tab to locate the email template."

        st.markdown("### Ready-to-Send Client Negotiation Email")
        st.caption("Copy this template into your email client. Tweak bracketed placeholders before sending.")
        st.text_area("Client Email Draft", value=email_content, height=350)

elif uploaded_file is None:
    # Helpful placeholder instructions when no file is uploaded
    st.info(
        "👋 **Welcome to ClauseShield!**\n\n"
        "To get started:\n"
        "1. Ensure Ollama is running (`ollama serve`).\n"
        "2. Ensure you have the Llama 3.1 model (`ollama pull llama3.1`).\n"
        "3. Drag and drop any freelance contract or SOW above.\n"
        "4. Click **Audit Contract Locally** to get an instant risk scorecard, clause redlines, and client email!"
    )


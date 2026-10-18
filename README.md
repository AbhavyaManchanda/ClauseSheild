# 🛡️ ClauseShield — Privacy-First Local Contract Reviewer

**ClauseShield** is a 100% local, privacy-first desktop application engineered specifically for freelancers, independent contractors, and creative consultants.

It parses commercial agreements (SOWs, MSAs, Freelance Agreements, NDAs), runs local inference using open-weight models (such as **Llama 3.1** via **Ollama**), flags predatory clauses, and generates an actionable risk assessment alongside counter-negotiation language and client email drafts.

---

## 🔒 The Privacy-First Mandate

- **100% Local Inference**: Zero contract text, trade secrets, names, rates, or NDA terms ever leave your machine.
- **Zero API Keys**: No OpenAI, Anthropic, or external cloud accounts needed.
- **No Cloud Telemetry**: Everything executes in-memory on your local network (`localhost:11434`).

---

## 🚀 Key Features

1. **Freelancer-Protective Legal Audit**:
   - **IP Grab Detection**: Catches broad work-for-hire clauses, missing pre-existing IP reservations, and IP assignments occurring prior to 100% full payment.
   - **Cash Flow Safeguards**: Identifies Net 60/90 terms, missing late payment interest, and unfair dispute windows.
   - **Non-Competes & Exclusivity**: Flags illegal or overly broad restraints on trade and future client engagements.
   - **Scope Creep Controls**: Detects subjective "client satisfaction" acceptance criteria and missing change order processes.
   - **Uncapped Liability**: Flags one-sided indemnification clauses and missing liability caps (should be limited to fees paid).

2. **Actionable Output**:
   - **Risk Scorecard**: Color-coded badges (`🟢 Low`, `🟡 Medium`, `🔴 High`, `🚨 Dangerous`).
   - **Itemized Redlines**: Verbatim clause quotes with battle-tested counter-language ready to paste.
   - **Polite Negotiation Email Draft**: Professional email template ready to send directly to your client.
   - **Markdown Export**: One-click download of the comprehensive audit report.

---

## 📁 Project Structure

```text
clauseshield/
├── app.py              # Main Streamlit desktop interface & UI logic
├── analyzer.py         # Local PDF extraction & Ollama execution logic
├── prompts.py          # Freelancer-focused system prompts & review templates
├── requirements.txt    # Python dependencies
└── README.md           # Setup, installation, and usage instructions
```

---

## 🛠️ Quickstart Guide

### 1. Install & Launch Ollama
If you haven't installed Ollama yet:
- **Download**: Visit [ollama.com](https://ollama.com) and install it for your operating system (macOS, Windows, Linux).
- **Start Ollama**:
  ```bash
  ollama serve
  ```

### 2. Pull the Llama 3.1 Model
Open your terminal or PowerShell and run:
```bash
ollama pull llama3.1
```
*(Tip: `llama3.1` defaults to the 8B parameter model, which runs smoothly on most laptops with 8GB+ RAM. If you have a high-end GPU or M-series Mac, you can also pull `llama3.1:70b` for legal-counsel grade depth.)*

### 3. Install Python Dependencies
Clone or navigate to the `clauseshield` directory, create a virtual environment, and install dependencies:

```bash
# Navigate to the project directory
cd clauseshield

# Create and activate a virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# macOS / Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 4. Launch ClauseShield
Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🖥️ How to Use ClauseShield

1. **Verify Ollama Status**: Check the sidebar indicator. It will display a green `🟢 Ollama Service Active` badge once Ollama is detected.
2. **Select Model**: Choose `llama3.1` (or any other locally installed model) from the sidebar dropdown.
3. **Set Review Priorities**: Toggle specific focus areas (IP, Payment, Non-Compete, Scope, Liability).
4. **Upload Contract**: Drag and drop your contract PDF.
5. **Inspect Raw Extraction**: Review the extracted page count and character stats in the preview expander.
6. **Click "Audit Contract Locally"**: Watch the real-time token stream as Llama 3.1 audits every clause.
7. **Export & Negotiate**:
   - Review the **Risk Scorecard** and **Clause Breakdown**.
   - Copy the customized **Client Negotiation Email**.
   - Click **Download Markdown Report** to save a copy for your records.

---

## 🧩 Hardware & Performance Recommendations

| Model | Recommended RAM / VRAM | Inference Speed |
| :--- | :--- | :--- |
| `llama3.1:8b` (Default) | 8 GB - 16 GB | ~25 - 60 tokens/sec |
| `llama3.2:3b` (Ultra-fast) | 4 GB - 8 GB | ~50 - 90 tokens/sec |
| `llama3.1:70b` (Deep Analysis) | 40 GB+ / Dual GPU | ~10 - 25 tokens/sec |

*ClauseShield supports any text generation model hosted on your Ollama instance (including `mistral`, `qwen2.5`, `phi3`, etc.).*

---

## ⚖️ Legal Disclaimer

*ClauseShield is an AI-assisted analysis and negotiation preparation tool designed for informational purposes. It does not provide legal advice, nor does it create an attorney-client relationship. Always consult a qualified attorney for high-stakes or complex contractual disputes.*


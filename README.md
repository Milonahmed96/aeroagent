# ✈️ AeroAgent — Autonomous AOG Quoting Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude%20Sonnet-blueviolet)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> An AI-powered aviation parts quoting pipeline that automates AOG (Aircraft on Ground) email triage, inventory lookup, and professional quote generation using Claude AI.

---

## 🚀 Live Demo

▶️ **[Try the Live Pipeline →](https://huggingface.co/spaces/Milon96/aeroagent.py)**  

---

## 📸 Preview

```
Email Input  →  Claude Extracts JSON  →  SQLite Inventory Check  →  AI Quote Generated
```

| Step | What Happens |
|------|-------------|
| 📧 Email In | Paste any AOG request email |
| 🤖 AI Extraction | Claude parses part number, airline, urgency |
| 🗄️ DB Lookup | Checks inventory + alternate parts |
| 📝 Quote Out | Professional quote email generated instantly |

---

## 🧠 Features

- **LLM Email Extraction** — Claude parses unstructured AOG emails into structured JSON
- **Intelligent Routing** — Auto-suggests alternate parts when primary is out of stock
- **AI Quote Generation** — Professional sales quotes tailored to urgency and customer
- **SQLite Inventory DB** — 6 real aviation parts with alternates and certifications
- **Gradio UI** — Clean web interface with sample emails for instant demo

---

## 🗂️ Project Structure

```
aeroagent/
├── aeroagent.ipynb          # Main Colab notebook
├── aeroagent.py             # Standalone Python script
├── requirements.txt         # Dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Ignores secrets and cache
├── README.md                # This file
└── .github/
    ├── workflows/
    │   └── ci.yml           # GitHub Actions CI
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/Milonahmed96/aeroagent.git
cd aeroagent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 4. Run locally
```bash
python aeroagent.py
```

### 5. Or open in Colab
[![Open In Colab](https://colab.research.google.com/drive/1nFNW_0M2DKx5h-91qmeM3okbdruywu3E#scrollTo=gmw_-0KwN6T-)

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com) |

**Never commit your API key.** Use `.env` locally or Colab Secrets in Google Colab.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Anthropic Claude Sonnet (`claude-sonnet-4-5`) |
| Database | SQLite (via Python `sqlite3`) |
| UI | Gradio |
| Language | Python 3.10+ |
| Hosting | Google Colab / Hugging Face Spaces |

---

## 📦 Sample Parts Database

| Part Number | Description | Aircraft | Stock |
|-------------|-------------|----------|-------|
| AV-29341-A | Hydraulic Actuator Flap | Boeing 737-800 | 3 |
| GE-CF56-7B | CFM56-7B Fan Blade | Boeing 737 NG | 0 (alt available) |
| AIR-A320-BLV | Bleed Air Valve | Airbus A320 | 5 |
| NGS-777-STR | Nose Gear Steering Actuator | Boeing 777 | 1 |

---

## 🌐 Deployment

### Hugging Face Spaces
'https://huggingface.co/spaces/Milon96/aeroagent.py'

### Gradio Share Link
```python
demo.launch(share=True)  # Already in the notebook
```
Copy the 'https://e7bc60d718f33cedcb.gradio.live' URL and share it directly.

---

## 🗺️ Roadmap

- [ ] Add more aircraft types and parts
- [ ] Email sending integration (SendGrid)
- [ ] PDF quote generation
- [ ] Multi-turn conversation memory
- [ ] Authentication for multi-user access

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 👤 Author
Milon Ahmed

Built as part of the **AI Engineer Roadmap** portfolio.  
Connect on [LinkedIn](www.linkedin.com/in/ahmed-intelligence) | [GitHub](https://github.com/Milonahmed96)

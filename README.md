# GutCheck 🩸

**Your blood test, finally explained.**

Built for **Mistral AI Worldwide Hackathon 2026** | Track: Anything Goes

---

## What is GutCheck?

GutCheck is an AI-powered web app that accepts a blood test PDF, extracts all biomarkers, flags abnormalities, explains everything in plain English, and generates a personalized diet + lifestyle action plan.

### Why?
Millions of people receive blood test reports every year but cannot understand them. Medical jargon, confusing reference ranges, and lack of doctor time leave patients confused and anxious. GutCheck solves this instantly.

---

## Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Upload blood test PDFs (up to 10MB) |
| 🔬 **Biomarker Analysis** | AI-powered analysis using Mistral Large 3 |
| 🎯 **Status Flags** | Clear 🟢 Normal / 🟡 Borderline / 🔴 Concern indicators |
| 💡 **Plain English** | Explanations without medical jargon |
| 📋 **Action Plan** | 3 specific recommendations per flagged biomarker |
| 🔊 **Voice Readout** | Results read aloud using Voxtral TTS |
| 🔍 **Deep Dive** | Research agent searches latest studies via web |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| AI Models | Mistral Large 3 (`mistral-large-latest`) |
| Voice | Voxtral (`voxtral-v0-2507`) |
| PDF Parsing | PyMuPDF + pdfplumber fallback |
| Agent/Search | Mistral Agents API + web_search tool |
| Experiment Tracking | Weights & Biases (wandb) |
| Deployment | Hugging Face Spaces |

---

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd gutcheck
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
MISTRAL_API_KEY=your_mistral_api_key_here
WANDB_API_KEY=your_wandb_api_key_here  # Optional
```

Get your Mistral API key: https://console.mistral.ai/api-keys/

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Project Structure

```
gutcheck/
│
├── app.py                  # Main Streamlit app entry point
├── core/
│   ├── __init__.py
│   ├── pdf_extractor.py    # Extract text from blood test PDF
│   ├── analyzer.py         # Mistral Large 3 analysis engine
│   ├── voice.py            # Voxtral voice output
│   └── agent.py            # Mistral Agent for research
│
├── prompts/
│   ├── __init__.py
│   ├── system_prompt.py    # Main analysis system prompt
│   └── agent_prompt.py     # Agent instructions
│
├── utils/
│   ├── __init__.py
│   ├── tracker.py          # W&B experiment tracking
│   └── helpers.py          # Utility functions
│
├── sample_reports/         # Sample PDFs for demo
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Usage

1. **Upload** your blood test PDF via the file uploader
2. Click **"Analyze Report"**
3. View results:
   - 🟢🟡🔴 Overall health status
   - Plain English summary
   - Top priorities
   - Detailed biomarker breakdown
4. Optional:
   - Click **"Read Results Aloud"** for voice output
   - Click **"Deep Dive Research"** for latest studies on flagged biomarkers

---

## Sample Reports

The `sample_reports/` folder includes 3 test PDFs:

| File | Description |
|------|-------------|
| `healthy_25f.pdf` | All normal biomarkers (GREEN status) |
| `deficient_40m.pdf` | 3 concerns - Vitamin D, Iron, Hemoglobin (YELLOW) |
| `risk_55m.pdf` | Multiple urgent issues (RED status) |

---

## Deployment to Hugging Face Spaces

1. Create a new Space at https://huggingface.co/spaces
2. Select **Streamlit** as the SDK
3. Connect your GitHub repository
4. Add your `MISTRAL_API_KEY` in Space secrets
5. Deploy!

Your app will be live at: `https://[username]-gutcheck.hf.space`

---

## API Costs (Estimated)

| Operation | Tokens | Cost |
|-----------|--------|------|
| PDF Analysis | ~2000 input + ~800 output | ~$0.009 |
| Voice Generation | ~500 characters | ~$0.002 |
| Deep Dive Research | ~1000 tokens | ~$0.003 |

**Total per full analysis:** ~$0.01-0.02

---

## W&B Dashboard

If you provide a `WANDB_API_KEY`, GutCheck tracks:
- Every PDF upload (file size, extraction method)
- Analysis metrics (response time, token count, status)
- Voice requests
- Research queries
- Error events

View your live dashboard at the URL provided after initialization.

---

## Troubleshooting

### "MISTRAL_API_KEY not found"
Make sure your `.env` file exists and contains your API key.

### "Failed to extract text from PDF"
- Try a different PDF (some scanned PDFs may not have extractable text)
- Ensure the PDF is a valid blood test report

### App runs slowly
- Check your internet connection (API calls require connectivity)
- W&B tracking can be disabled by removing `WANDB_API_KEY`

---

## Built For

**Mistral AI Worldwide Hackathon 2026**
- Track: Anything Goes
- Category: Health & Wellness

---

## Disclaimer

⚕️ **This analysis is for educational purposes only. Please consult your doctor for medical advice.**

GutCheck does not provide medical diagnosis or treatment recommendations. Always consult with a qualified healthcare provider for medical concerns.

---

## License

MIT License - Built for hackathon demonstration

---

*Made with ❤️ using Mistral AI*

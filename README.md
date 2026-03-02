# 🩸 GutCheck - Blood Test Analyzer

**Your blood test, finally explained in plain English.**

> Built for **Mistral AI Worldwide Hackathon 2026** | Track: Anything Goes

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face%20Spaces-blue)](https://huggingface.co/spaces/Harshiiiii118/gutcheck)
[![GitHub](https://img.shields.io/badge/GitHub-Code-black)](https://github.com/harshith1118/bloddshot)
[![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral%20AI-orange)](https://mistral.ai)

---

## 🎯 The Problem

- **80% of patients** can't understand their blood test results
- **Doctors have <10 minutes** per patient - no time to explain each number
- **Medical jargon** is confusing - what does "Hemoglobin 11.2 g/dL" even mean?

**GutCheck fixes that.**

---

## 💡 The Solution

**Upload your blood test PDF → Get instant AI-powered analysis**

GutCheck reads your blood test report and explains:
- ✅ Which biomarkers are **Normal**
- ⚠️ Which are **Borderline** (need monitoring)
- 🔴 Which are **Concerning** (need attention)
- 📋 **Plain English explanations** - no medical jargon
- 🎯 **Actionable recommendations** for each flagged biomarker

Results in **15-30 seconds**.

---

## ✨ Features

### What Works Now
- **PDF Upload** - Upload any blood test PDF (max 10MB)
- **Smart Text Extraction** - PyMuPDF + pdfplumber fallback
- **AI Analysis** - Mistral AI extracts and analyzes all biomarkers
- **Visual Status Indicators** - Color-coded results (Green/Yellow/Red)
- **Plain English Explanations** - Each biomarker explained simply
- **Actionable Recommendations** - Diet, lifestyle, supplement suggestions
- **React UI** - Clean, modern interface with Tailwind CSS
- **FastAPI Backend** - Python server with JSON API

### Tech Stack
| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + Vite + Tailwind CSS + Framer Motion |
| **Backend** | FastAPI (Python) |
| **AI Model** | Mistral AI (`Mistral-Large-3`) |
| **PDF Parsing** | PyMuPDF + pdfplumber |
| **Deployment** | Hugging Face Spaces (Docker) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Mistral AI API key (get free at [console.mistral.ai](https://console.mistral.ai))

### 1. Clone the Repository
```bash
git clone https://github.com/harshith1118/bloddshot.git
cd bloddshot
```

### 2. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install frontend packages
cd gutcheck-web
npm install
cd ..
```

### 3. Set Up Environment
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_api_key_here" > .env
```

### 4. Build & Run
```bash
# Build the React frontend
cd gutcheck-web
npm run build
cd ..

# Start the FastAPI server
python gutcheck-web/main.py
```

Open **http://localhost:7860** in your browser.

---

## 📁 Project Structure

```
gutcheck/
├── gutcheck-web/           # React Frontend + FastAPI Backend
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── components/     # UI components
│   │   │   ├── Header.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── UploadSection.jsx
│   │   │   ├── AnalysisResults.jsx
│   │   │   └── Footer.jsx
│   │   └── lib/
│   │       └── api.js      # API client
│   ├── dist/               # Built React app (production)
│   └── main.py             # FastAPI server
│
├── core/                   # Backend Analysis Engine
│   ├── analyzer.py         # Mistral AI integration
│   ├── pdf_extractor.py    # PDF text extraction
│   ├── voice.py            # Voice output (Voxtral)
│   └── agent.py            # Research agent
│
├── prompts/                # AI Prompts
│   ├── system_prompt.py    # Main analysis instructions
│   └── agent_prompt.py     # Research agent prompts
│
├── utils/                  # Utilities
│   ├── tracker.py          # W&B experiment tracking
│   └── helpers.py          # Helper functions
│
├── sample_reports/         # Test PDFs for demo
│   ├── healthy_25f.pdf     # All normal results
│   ├── deficient_40m.pdf   # Multiple deficiencies
│   └── risk_55m.pdf        # High-risk results
│
├── Dockerfile              # Production deployment
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧪 Sample Test Reports

We've included **3 sample blood test reports** for testing:

| File | Description |
|------|-------------|
| `healthy_25f.pdf` | 25-year-old female, all normal results |
| `deficient_40m.pdf` | 40-year-old male, vitamin deficiencies |
| `risk_55m.pdf` | 55-year-old male, multiple risk factors |

### How to Test
1. Run the app locally or visit the live demo
2. Upload any sample PDF from `sample_reports/`
3. Wait 15-30 seconds for analysis
4. Review the biomarker breakdown and recommendations

---

## 🎯 Hackathon Criteria

| Requirement | Status |
|-------------|--------|
| ✅ App is live | Deployed on Hugging Face Spaces |
| ✅ Unique idea | Blood test analyzer with AI explanations |
| ✅ Mistral AI | Using Mistral AI models for analysis |
| ✅ Quality UI | React 18 + Tailwind CSS + Framer Motion |
| ✅ Sample data | 3 test PDFs included |

---

## 📊 How It Works

### Architecture

```
User Upload → React UI → FastAPI Backend → Mistral AI → JSON Response → React Display
                │              │
                │              └→ PDF Extraction (PyMuPDF)
                │
                └→ Display Results (Color-coded cards)
```

### Analysis Pipeline

1. **PDF Upload** → User uploads blood test PDF via React UI
2. **Text Extraction** → PyMuPDF extracts text (pdfplumber fallback)
3. **AI Analysis** → Mistral AI processes with structured prompt
4. **JSON Response** → Returns biomarkers, status, recommendations
5. **UI Display** → React renders color-coded results

---

## 🔬 AI Analysis Output

The AI returns structured JSON like this:

```json
{
  "overall_status": "YELLOW",
  "summary": "Your blood test shows 3 areas that need attention...",
  "biomarkers": [
    {
      "name": "Vitamin D",
      "value": "18",
      "unit": "ng/mL",
      "normal_range": "30-100",
      "status": "CONCERN",
      "explanation": "Your vitamin D level is low...",
      "recommendations": [
        "Get 20 minutes of direct sunlight daily",
        "Eat fatty fish 3 times per week",
        "Consider vitamin D3 supplement: 2000 IU daily"
      ]
    }
  ],
  "top_priorities": ["Increase vitamin D through sunlight and diet"],
  "disclaimer": "This analysis is for educational purposes only."
}
```

---

## 🌐 Live Demo

**Try GutCheck:** https://huggingface.co/spaces/Harshiiiii118/gutcheck

### Demo Instructions
1. Open the live demo on Hugging Face Spaces
2. Upload a sample PDF (or your own blood test report)
3. Wait 15-30 seconds for AI analysis
4. Review results:
   - Check overall status (🟢/🟡/🔴)
   - Expand biomarkers to see explanations
   - Read actionable recommendations

---

## 📄 License

MIT License

---

## ⚠️ Medical Disclaimer

**GutCheck is for educational purposes only.**

- ❌ NOT a medical diagnosis
- ❌ NOT a substitute for professional medical advice
- ❌ NOT intended to replace doctor consultations
- ✅ ALWAYS consult your healthcare provider for medical concerns

---

## 🙏 Acknowledgments

- **Mistral AI** - For the AI models
- **Hugging Face** - For Spaces hosting
- **Hackathon Organizers** - Mistral AI Worldwide Hackathon 2026

---

## 📞 Contact

- **GitHub:** [@harshith1118](https://github.com/harshith1118)
- **Hugging Face:** [@Harshiiiii118](https://huggingface.co/Harshiiiii118)

---

**Built with Mistral AI**

*Hackathon Submission: Mistral AI Worldwide Hackathon 2026*  
*Track: Anything Goes | Category: Health & Wellness*

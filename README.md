# 🩸 GutCheck - Blood Test Analyzer

**Your blood test, finally explained in plain English.**

> Built for **Mistral AI Worldwide Hackathon 2026** | Track: Anything Goes

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Hugging%20Face%20Spaces-blue)](https://huggingface.co/spaces/Harshiiiii118/gutcheck)
[![GitHub](https://img.shields.io/badge/GitHub-Code-black)](https://github.com/harshith1118/bloddshot)
[![Mistral AI](https://img.shields.io/badge/Powered%20by-Mistral%20Large%203-orange)](https://mistral.ai)

---

## 🎯 The Problem

- 80% of patients don't understand their results
- Doctors have <10 minutes per patient
- Medical jargon is confusing

## 💡 The Solution

**Upload your blood test PDF → Get instant AI-powered analysis**

GutCheck uses Mistral Large 3 to:
- Extract all biomarkers from your PDF
- Flag abnormalities with clear visual indicators
- Explain each result in **plain English** (no jargon)
- Provide **actionable diet & lifestyle recommendations**
- Deliver results in **15-30 seconds**

### Before vs After

| Before GutCheck | After GutCheck |
|----------------|----------------|
| "Vitamin D: 18 ng/mL (Ref: 30-100)" ❓ | "🔴 **Vitamin D is LOW** - You're not getting enough sunlight or dietary vitamin D" |
| Google symptoms for hours | Get 3 specific actions: sunlight, food, supplements |
| Wait days for doctor callback | Instant analysis in 15-30 seconds |

---

## ✨ Key Features

### 1. **AI-Powered Analysis** 
- Powered by **Mistral Large 3** (`mistral-large-latest`)
- JSON-structured output for consistent, reliable results
- Smart biomarker extraction from any PDF format

### 2. **Clear Visual Indicators**
- ✅ **Normal** - Within healthy range
- ⚠️ **Borderline** - Slightly outside range, monitor closely
- 🔴 **Concern** - Significantly abnormal, needs attention

### 3. **Plain English Explanations**
Every flagged biomarker includes:
- What it means for your health
- Why it might be abnormal
- What you can do about it

### 4. **Actionable Recommendations**
For each abnormal biomarker, you get **3 specific actions**:
- 🥗 **Diet changes** (specific foods to eat/avoid)
- 🏃 **Lifestyle adjustments** (sleep, exercise, sunlight)
- 💊 **Supplement guidance** (dosage and timing)

### 5. **Privacy-First Design**
- Files processed in real-time
- No data stored on servers
- Secure API communication

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite + Tailwind CSS | Modern, responsive UI |
| **Backend** | FastAPI (Python) | High-performance API server |
| **AI Model** | Mistral Large 3 | Biomarker analysis & explanations |
| **PDF Parsing** | PyMuPDF + pdfplumber | Extract text from any PDF format |
| **Deployment** | Hugging Face Spaces (Docker) | Free, reliable hosting |

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
# Create .env file from example
cp .env.example .env

# Add your Mistral API key
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

We've included **3 sample blood test reports** so you can test GutCheck immediately:

| File | Description | Expected Result |
|------|-------------|-----------------|
| `healthy_25f.pdf` | 25-year-old female, all normal | 🟢 GREEN - No concerns |
| `deficient_40m.pdf` | 40-year-old male, vitamin deficiencies | 🟡 YELLOW - 3 concerns |
| `risk_55m.pdf` | 55-year-old male, multiple risk factors | 🔴 RED - Urgent attention |

### Try It Yourself
1. Open the app
2. Upload any sample PDF from `sample_reports/`
3. Watch GutCheck analyze in real-time
4. See different results for each report!

---

## 🎯 Hackathon Criteria Checklist

| Requirement | Status | Details |
|-------------|--------|---------|
| ✅ App is live | **Done** | Deployed on Hugging Face Spaces |
| ✅ Unique idea | **Done** | Blood test analyzer with AI explanations |
| ✅ Mistral Large 3 | **Done** | Using `mistral-large-latest` with JSON mode |
| ✅ Quality UI | **Done** | React 18 + Tailwind CSS |
| ✅ Sample data | **Done** | 3 test PDFs included |

---

## 📊 How It Works

### Architecture Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   User      │────▶│  React UI    │────▶│  FastAPI Server │────▶│ Mistral AI   │
│  Uploads    │     │  (Vite)      │     │  (Python)       │     │ (Large 3)    │
│  PDF        │     │              │     │                 │     │              │
└─────────────┘     └──────────────┘     └─────────────────┘     └──────────────┘
                           │                    │
                           │                    ▼
                           │           ┌─────────────────┐
                           │           │ PDF Extractor   │
                           │           │ (PyMuPDF)       │
                           │           └─────────────────┘
                           │                    │
                           ▼                    ▼
                    ┌──────────────────────────────┐
                    │  JSON Response with Analysis │
                    │  - Overall status            │
                    │  - Biomarker breakdown       │
                    │  - Recommendations           │
                    └──────────────────────────────┘
```

### Analysis Pipeline

1. **PDF Upload** → User uploads blood test PDF (max 10MB)
2. **Text Extraction** → PyMuPDF extracts raw text from PDF
3. **Validation** → Verify it's actually a blood test report
4. **AI Analysis** → Mistral Large 3 processes the text with structured prompts
5. **JSON Response** → Returns structured analysis with biomarkers, status, recommendations
6. **UI Display** → React renders results with color-coded indicators

---

## 🔬 The AI Prompt

GutCheck uses a carefully engineered system prompt that instructs Mistral Large 3 to:

1. **Extract** all biomarkers with values and units
2. **Flag** each as Normal/Borderline/Concern based on reference ranges
3. **Explain** in simple English (like explaining to a 15-year-old)
4. **Recommend** 3 specific actions per flagged biomarker
5. **Output** pure JSON (no markdown, no extra text)

### Example Output

```json
{
  "overall_status": "YELLOW",
  "summary": "Your blood test shows 3 areas that need attention. Your vitamin D and iron levels are low, which may cause fatigue. Your cholesterol is slightly elevated.",
  "biomarkers": [
    {
      "name": "Vitamin D",
      "value": "18",
      "unit": "ng/mL",
      "normal_range": "30-100",
      "status": "CONCERN",
      "explanation": "Your vitamin D level is low. This vitamin helps your body absorb calcium for strong bones. Low levels can cause tiredness, muscle weakness, and frequent infections.",
      "recommendations": [
        "Get 20 minutes of direct sunlight daily (arms and face exposed)",
        "Eat fatty fish (salmon, mackerel) 3 times per week",
        "Consider vitamin D3 supplement: 2000 IU daily with breakfast"
      ]
    }
  ],
  "top_priorities": [
    "Increase vitamin D through sunlight and diet",
    "Add iron-rich foods to combat deficiency"
  ],
  "disclaimer": "⚕️ This analysis is for educational purposes only. Please consult your doctor for medical advice."
}
```

---

## 🌐 Live Demo

**Try GutCheck now:** https://huggingface.co/spaces/Harshiiiii118/gutcheck

### Demo Instructions for Judges

1. **Open the live demo** on Hugging Face Spaces
2. **Upload a sample PDF** (or your own blood test report)
3. **Wait 15-30 seconds** for AI analysis
4. **Review the results:**
   - Check the overall status (🟢/🟡/🔴)
   - Expand individual biomarkers to see explanations
   - Read the actionable recommendations
5. **Try different PDFs** to see how results change

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

## ⚠️ Medical Disclaimer

**GutCheck is for educational purposes only.**

- ❌ **NOT** a medical diagnosis
- ❌ **NOT** a substitute for professional medical advice
- ❌ **NOT** intended to replace doctor consultations
- ✅ **ALWAYS** consult your healthcare provider for medical concerns

---

## 🙏 Acknowledgments

- **Mistral AI** - For the incredible Mistral Large 3 model
- **Hugging Face** - For free Spaces hosting
- **Hackathon Organizers** - For making this event possible

---

## 📞 Contact

- **GitHub:** [@harshith1118](https://github.com/harshith1118)
- **Hugging Face:** [@Harshiiiii118](https://huggingface.co/Harshiiiii118)

---

**Built with ❤️ using Mistral AI**

*Hackathon Submission: Mistral AI Worldwide Hackathon 2026*  
*Track: Anything Goes | Category: Health & Wellness*

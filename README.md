---
title: GutCheck - Blood Test Analyzer
emoji: 🩸
colorFrom: blue
colorTo: purple
sdk: docker
app_file: gutcheck-web/main.py
pinned: false
license: MIT
---

# 🩸 GutCheck

**Your blood test, finally explained.**

Built for **Mistral AI Worldwide Hackathon 2026**

🔗 **Live Demo:** https://huggingface.co/spaces/Harshiiiii118/gutcheck

---

## 🚀 The Problem

- 500M+ blood tests performed yearly worldwide
- 80% of patients don't understand their results
- Doctors have <10 minutes per patient
- Medical jargon is confusing

## 💡 The Solution

**Upload PDF → Get instant AI analysis**

- Plain English explanations (no jargon)
- Clear status indicators (✅ Normal / ⚠️ Borderline / 🔴 Concern)
- Actionable diet & lifestyle recommendations
- Results in 15-30 seconds

---

## ✨ Features

- **AI-powered analysis** using Mistral Large 3
- **Clear visual indicators** for each biomarker
- **Plain English explanations** - imagine explaining to a 15-year-old
- **3 actionable recommendations** per flagged biomarker
- **Fast results** - 15-30 second response time
- **Privacy-first** - files processed in real-time, not stored

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18 + Vite + Tailwind CSS |
| **Backend** | FastAPI (Python) |
| **AI Model** | Mistral Large 3 (`mistral-large-latest`) |
| **PDF Parsing** | PyMuPDF + pdfplumber |
| **Deployment** | Hugging Face Spaces (Docker) |
| **Tracking** | Weights & Biases (optional) |

---

## 🎯 Hackathon Criteria

| Criterion | Status |
|-----------|--------|
| App is live | ✅ Deployed on HF Spaces |
| Unique idea | ✅ Blood test analyzer |
| Mistral Large 3 | ✅ Using `mistral-large-latest` with JSON mode |
| UI Quality | ✅ React + Tailwind CSS |
| Sample PDFs | ✅ 3 test reports included |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Mistral AI API key

### 1. Clone & Install
```bash
git clone https://huggingface.co/spaces/Harshiiiii118/gutcheck
cd gutcheck

# Install backend
pip install -r requirements.txt

# Install frontend
cd gutcheck-web
npm install
```

### 2. Set API Key
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_key_here" > .env
```

### 3. Build & Run
```bash
# Build frontend
cd gutcheck-web
npm run build

# Run backend
cd ..
python gutcheck-web/main.py
```

Open http://localhost:7860

---

## 📁 Project Structure

```
gutcheck/
├── core/               # Analysis engine
│   ├── analyzer.py     # Mistral AI integration
│   └── pdf_extractor.py
├── gutcheck-web/       # React frontend
│   ├── src/
│   ├── dist/           # Built assets
│   └── main.py         # FastAPI server
├── prompts/            # AI prompts
├── sample_reports/     # Test PDFs
├── Dockerfile
└── requirements.txt
```

---

## 🧪 Sample Test Reports

Included in `sample_reports/`:

1. **healthy_25f.pdf** - All normal results
2. **risk_55m.pdf** - Multiple concerns (diabetes risk, high cholesterol)
3. **anemia_40f.pdf** - Iron deficiency anemia

---

## ⚠️ Disclaimer

**This is for educational purposes only.**

- ❌ Not a medical diagnosis
- ❌ Not a substitute for professional medical advice
- ✅ Always consult your doctor for medical concerns

---

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ using Mistral AI**

*Hackathon Submission: Mistral AI Worldwide Hackathon 2026*

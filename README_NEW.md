# GutCheck 🩸

**Your blood test, finally explained.**

Built for **Mistral AI Worldwide Hackathon 2026** | Track: Anything Goes

---

## What is GutCheck?

GutCheck is a modern AI-powered web app that accepts a blood test PDF, extracts all biomarkers, flags abnormalities, explains everything in plain English, and generates a personalized diet + lifestyle action plan.

### Why?
Millions of people receive blood test reports every year but cannot understand them. Medical jargon, confusing reference ranges, and lack of doctor time leave patients confused and anxious. GutCheck solves this instantly.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Drag & drop or click to upload blood test PDFs (up to 10MB) |
| 🔬 **Biomarker Analysis** | AI-powered analysis using Mistral Large 3 |
| 🎯 **Status Flags** | Clear 🟢 Normal / 🟡 Borderline / 🔴 Concern indicators |
| 💡 **Plain English** | Explanations without medical jargon |
| 📋 **Action Plan** | 3 specific recommendations per flagged biomarker |
| 🔍 **Deep Dive** | Research agent searches latest studies via web |
| 🎨 **Modern UI** | Beautiful, responsive React interface with animations |

---

## 🚀 Quick Start

### Option 1: Run Locally (Development)

```bash
# Clone the repository
git clone <your-repo-url>
cd gutcheck

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd gutcheck-web
npm install

# Build frontend
npm run build

# Go back and run backend
cd ..
python gutcheck-web/main.py
```

Open http://localhost:7860

### Option 2: Use the Streamlit App (Legacy)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

Open http://localhost:8501

---

## 🛠️ Tech Stack

### Frontend (New)
| Layer | Technology |
|-------|------------|
| Framework | React 18 + Vite |
| Styling | Tailwind CSS |
| Animations | Framer Motion |
| HTTP Client | Axios |
| File Upload | react-dropzone |

### Backend
| Layer | Technology |
|-------|------------|
| Framework | FastAPI |
| AI Models | Mistral Large 3 (`mistral-large-latest`) |
| Voice | Voxtral (`voxtral-v0-2507`) - *optional* |
| PDF Parsing | PyMuPDF + pdfplumber fallback |
| Agent/Search | Mistral Agents API + web_search tool |

### Legacy (Still Works)
| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Experiment Tracking | Weights & Biases (wandb) |

---

## 📁 Project Structure

```
gutcheck/
│
├── gutcheck-web/           # New React frontend + FastAPI backend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── lib/            # API client
│   │   ├── App.jsx         # Main app
│   │   └── main.jsx        # Entry point
│   ├── main.py             # FastAPI backend server
│   ├── Dockerfile          # For Hugging Face deployment
│   └── package.json        # Node dependencies
│
├── app.py                  # Legacy Streamlit app
├── core/                   # Shared Python modules
│   ├── pdf_extractor.py    # PDF text extraction
│   ├── analyzer.py         # Mistral Large 3 analysis
│   ├── voice.py            # Voxtral TTS (optional)
│   └── agent.py            # Research agent
├── prompts/                # AI prompts
├── utils/                  # Utilities
├── sample_reports/         # Test PDFs
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🚀 Deploy to Hugging Face Spaces

### Using Docker Space (Recommended)

1. **Create a new Space** at https://huggingface.co/spaces/create
   - Select **Docker** as the SDK
   - Choose "Blank" template

2. **Push your code** to the Space repository:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/gutcheck
   git push -u hf main
   ```

3. **Add Environment Secret**:
   - Go to Space Settings → Repository secrets
   - Add `MISTRAL_API_KEY` with your Mistral AI API key
   - Get your key at: https://console.mistral.ai/api-keys/

4. **Wait for build** (~5-10 minutes for first build)

5. **Your app is live!** at `https://huggingface.co/spaces/YOUR_USERNAME/gutcheck`

---

## 🧪 Testing

### Sample Reports

The `sample_reports/` folder includes 3 test PDFs:

| File | Description |
|------|-------------|
| `healthy_25f.pdf` | All normal biomarkers (GREEN status) |
| `deficient_40m.pdf` | 3 concerns - Vitamin D, Iron, Hemoglobin (YELLOW) |
| `risk_55m.pdf` | Multiple urgent issues (RED status) |

### Test Locally

```bash
# Run the backend server
python gutcheck-web/main.py

# Open browser to http://localhost:7860
# Upload a sample PDF and test
```

---

## 💰 API Costs (Estimated)

| Operation | Tokens | Cost |
|-----------|--------|------|
| PDF Analysis | ~3000 input + ~1500 output | ~$0.015 |
| Voice Generation | ~500 characters | ~$0.002 |
| Deep Dive Research | ~1000 tokens | ~$0.003 |

**Total per full analysis:** ~$0.02

---

## 🏆 Hackathon Submission

**Mistral AI Worldwide Hackathon 2026**
- Track: Anything Goes
- Category: Health & Wellness

### Submission Checklist
- [ ] GitHub repo with clean README
- [ ] Live demo on Hugging Face Spaces
- [ ] 3 sample PDFs for testing
- [ ] 2-minute demo video
- [ ] Submit on Hackiterate before deadline

---

## 📊 Pitch Deck Structure

| Slide | Content |
|-------|---------|
| **1 — Hook** | "You got your blood test back. Can you understand it?" |
| **2 — Problem** | 500M blood tests yearly. 80% don't understand results. |
| **3 — Demo** | LIVE: Upload report → watch GutCheck analyze in real time |
| **4 — Tech** | Mistral Large 3 + React + FastAPI diagram |
| **5 — Vision** | Connect to wearables, track over time, predict issues |

---

## ⚠️ Disclaimer

**This analysis is for educational purposes only. Please consult your doctor for medical advice.**

GutCheck does not provide medical diagnosis or treatment recommendations. Always consult with a qualified healthcare provider for medical concerns.

---

## 📄 License

MIT License - Built for hackathon demonstration

---

*Made with ❤️ using Mistral AI + React + FastAPI*

---
title: GutCheck - Blood Test Analyzer
emoji: 🩸
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: ""
app_file: gutcheck-web/main.py
pinned: false
---

# 🩸 GutCheck

**Your blood test, finally explained.**

Built for Mistral AI Worldwide Hackathon 2026

## Features

- 🔬 AI-powered blood test analysis using Mistral Large 3
- 🎯 Clear status indicators (Normal / Borderline / Attention)
- 💡 Plain English explanations - no medical jargon
- 📋 Actionable diet and lifestyle recommendations
- ⚡ Results in ~15-30 seconds

## How to Use

1. Upload your blood test report PDF
2. Wait for AI analysis
3. Review results with clear explanations
4. Follow personalized recommendations

## Tech Stack

- **Frontend:** React 18 + Vite + Tailwind CSS
- **Backend:** FastAPI (Python)
- **AI:** Mistral Large 3 for analysis
- **PDF:** PyMuPDF for text extraction

## Environment Variables

Set the following in your Space secrets:

- `MISTRAL_API_KEY` - Your Mistral AI API key

Get your API key at: https://console.mistral.ai/api-keys/

## Local Development

```bash
# Install dependencies
pip install -r gutcheck-web/requirements.txt
cd gutcheck-web && npm install

# Build frontend
cd gutcheck-web && npm run build

# Run backend
python gutcheck-web/main.py
```

## Deployment

This Space uses Docker deployment. The Dockerfile builds both the React frontend and Python backend.

---

*For educational purposes only. Consult your doctor for medical advice.*

Built with ❤️ using Mistral AI

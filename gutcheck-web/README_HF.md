---
title: GutCheck - Blood Test Analyzer
emoji: 🩸
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
tags:
  - mistral-ai
  - healthcare
  - hackathon
  - medical-analysis
---

# GutCheck 🩸

**Your blood test, finally explained.**

Built for Mistral AI Worldwide Hackathon 2026

## Features

- 🔬 AI-powered blood test analysis using Mistral Large 3
- 🎯 Clear status indicators (🟢 Normal / 🟡 Borderline / 🔴 Concern)
- 💡 Plain English explanations - no medical jargon
- 📋 Actionable diet and lifestyle recommendations
- 🔍 Deep dive research with Mistral Agents API

## How to Use

1. Upload your blood test report PDF
2. Wait for AI analysis (~10-30 seconds)
3. Review results with clear explanations
4. Follow personalized recommendations

## Environment Variables

Set the following in your Hugging Face Space secrets:

- `MISTRAL_API_KEY` - Your Mistral AI API key (get at https://console.mistral.ai/api-keys/)

## Tech Stack

- **Frontend:** React 18 + Vite + Tailwind CSS + Framer Motion
- **Backend:** FastAPI (Python)
- **AI:** Mistral Large 3 for analysis
- **PDF:** PyMuPDF for text extraction

## Local Development

```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd gutcheck-web
npm install

# Build frontend
npm run build

# Run backend server
python main.py
```

## Deployment

Deploy to Hugging Face Spaces:

1. Create a new Space with Docker SDK
2. Push this repository
3. Add `MISTRAL_API_KEY` secret
4. App will be live at `https://huggingface.co/spaces/your-username/gutcheck`

---

*For educational purposes only. Consult your doctor for medical advice.*

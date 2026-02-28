# GutCheck — Product Requirements Document (PRD)
## Mistral AI Worldwide Hackathon 2026

---

## 1. PRODUCT OVERVIEW

**Product Name:** GutCheck  
**Tagline:** "Your blood test, finally explained."  
**Track:** Anything Goes (Online)  
**Hackathon:** Mistral AI Worldwide Hackathon 2026  

### Problem Statement
Millions of people receive blood test reports every year but cannot 
understand them. Medical jargon, confusing reference ranges, and 
lack of doctor time leave patients confused and anxious. 
GutCheck solves this instantly.

### Solution
An AI-powered web app that accepts a blood test PDF, extracts all 
biomarkers, flags abnormalities, explains everything in plain 
English, and generates a personalized diet + lifestyle action plan.

---

## 2. CORE REQUIREMENTS

### Must Use (Hackathon Rules)
- **Primary Model:** `mistral-large-latest` (Mistral Large 3)
  - Used for: PDF understanding, biomarker analysis, 
    explanation generation, wellness plan
- **Voice Model:** `voxtral-v0-2507` (Voxtral)
  - Used for: Reading analysis results aloud to user
- **Agents API:** Mistral Agents with web_search tool
  - Used for: Searching latest research on flagged biomarkers
- **API Base URL:** `https://api.mistral.ai/v1`
- **SDK:** `mistralai` Python package

### Sponsor Tools (Bonus Points)
- **Weights & Biases:** Track every API call, response time, 
  token usage for demo dashboard
- **Hugging Face Spaces:** Final deployment

---

## 3. TECH STACK

| Layer | Technology | Version |
|---|---|---|
| Frontend | Streamlit | latest |
| AI Models | Mistral Large 3 | mistral-large-latest |
| Voice | Voxtral | voxtral-v0-2507 |
| PDF Parsing | PyMuPDF (fitz) | latest |
| PDF Fallback | pdfplumber | latest |
| Agent/Search | Mistral Agents API | built-in |
| Experiment Tracking | Weights & Biases (wandb) | latest |
| Deployment | Hugging Face Spaces | - |
| Env Management | python-dotenv | latest |
| HTTP Client | httpx | latest |

---

## 4. PROJECT STRUCTURE
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
│   ├── system_prompt.py    # Main analysis system prompt
│   └── agent_prompt.py     # Agent instructions
│
├── utils/
│   ├── tracker.py          # W&B experiment tracking
│   └── helpers.py          # Utility functions
│
├── sample_reports/         # 3 sample PDFs for demo
│   ├── healthy_25f.pdf
│   ├── deficient_40m.pdf
│   └── risk_55m.pdf
│
├── requirements.txt
├── .env                    # API keys (never commit)
├── .gitignore
└── README.md
```

---

## 5. FEATURE SPECIFICATIONS

### Feature 1: PDF Upload & Extraction
**Priority:** P0 (must have)

**Behavior:**
- User uploads blood test PDF via Streamlit file uploader
- System extracts raw text using PyMuPDF
- If PyMuPDF fails → fallback to pdfplumber
- If both fail → show clear error message
- Extracted text passed to analyzer

**Acceptance Criteria:**
- [ ] Accepts PDF files up to 10MB
- [ ] Extracts text from both digital and scanned PDFs
- [ ] Shows extraction success/failure to user
- [ ] Passes clean text to Mistral Large 3

---

### Feature 2: Biomarker Analysis Engine
**Priority:** P0 (must have)  
**Model:** `mistral-large-latest`

**System Prompt:**
```
You are GutCheck, a friendly medical report analyzer.

When given a blood test report, you MUST:

1. EXTRACT all biomarkers mentioned with their values and units
2. FLAG each biomarker as:
   - ✅ NORMAL - within reference range
   - ⚠️ BORDERLINE - slightly outside range  
   - 🔴 CONCERN - significantly outside range
3. EXPLAIN each flagged biomarker in simple English
   (imagine explaining to a smart 15-year-old)
4. GIVE overall health score: GREEN / YELLOW / RED
5. PROVIDE 3 specific, actionable recommendations 
   per flagged biomarker (food, lifestyle, supplements)
6. ALWAYS end with: 
   "⚕️ This analysis is for educational purposes only. 
   Please consult your doctor for medical advice."

Response format: JSON only. No extra text.
No markdown. Pure JSON.

JSON Schema:
{
  "overall_status": "GREEN|YELLOW|RED",
  "summary": "2-3 sentence plain English summary",
  "biomarkers": [
    {
      "name": "Hemoglobin",
      "value": "11.2",
      "unit": "g/dL",
      "normal_range": "13.5-17.5",
      "status": "CONCERN",
      "explanation": "plain English explanation",
      "recommendations": ["rec1", "rec2", "rec3"]
    }
  ],
  "top_priorities": ["most important thing to address"],
  "disclaimer": "standard disclaimer"
}
```

**Acceptance Criteria:**
- [ ] Returns valid JSON every time
- [ ] Correctly flags out-of-range values
- [ ] Explanations use zero medical jargon
- [ ] Recommendations are specific and actionable
- [ ] Handles missing/incomplete reports gracefully

---

### Feature 3: UI Results Display
**Priority:** P0 (must have)

**Layout:**
```
┌─────────────────────────────────────────┐
│  🩸 GutCheck                    [Upload]│
├─────────────────────────────────────────┤
│  Overall Status: 🟡 YELLOW              │
│  "You have 2 areas that need attention" │
├─────────────────────────────────────────┤
│  BIOMARKERS                             │
│  ✅ Blood Sugar    95 mg/dL   Normal    │
│  ⚠️  Cholesterol  215 mg/dL  Borderline│
│  🔴 Vitamin D      18 ng/mL  Low       │
├─────────────────────────────────────────┤
│  📋 ACTION PLAN                         │
│  For Low Vitamin D:                     │
│  1. Get 20min sunlight daily            │
│  2. Eat fatty fish 3x/week              │
│  3. Consider D3 supplement 2000IU       │
├─────────────────────────────────────────┤
│  🔊 [Read Results Aloud]  [Deep Dive]   │
└─────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Color coded status indicators
- [ ] Expandable sections per biomarker
- [ ] Clean, calming color palette (not clinical white)
- [ ] Mobile responsive
- [ ] Loads results progressively (streaming)

---

### Feature 4: Voice Readout
**Priority:** P1 (should have)  
**Model:** `voxtral-v0-2507`

**Behavior:**
- User clicks "Read Results Aloud" button
- Voxtral reads the summary + flagged items + top recommendations
- Calm, warm voice tone
- Especially useful for elderly users

**Acceptance Criteria:**
- [ ] Reads full analysis in natural voice
- [ ] Skips technical jargon in voice mode
- [ ] Has stop/pause button
- [ ] Works in browser without installation

---

### Feature 5: Deep Dive Research Agent
**Priority:** P1 (should have)  
**Model:** Mistral Agents API + web_search tool

**Behavior:**
- User clicks "Deep Dive" on any flagged biomarker
- Mistral Agent searches for latest research on that biomarker
- Returns: latest studies, new treatment approaches, 
  clinical trials if relevant
- Cites sources with links

**Agent Instructions:**
```
You are a medical research assistant.
When given a biomarker concern, search the web for:
1. Latest research (last 2 years) on this condition
2. Most effective evidence-based interventions
3. When to urgently see a doctor
Always cite your sources.
Keep response under 200 words.
```

**Acceptance Criteria:**
- [ ] Agent performs minimum 2 web searches per query
- [ ] Returns cited sources
- [ ] Completes in under 30 seconds
- [ ] Handles "no recent research found" gracefully

---

### Feature 6: W&B Tracking Dashboard
**Priority:** P2 (nice to have — bonus judge points)

**Track:**
- Every PDF upload (timestamp, file size)
- Every analysis (tokens used, response time, model)
- Every voice request
- Every agent deep dive
- Overall usage metrics

**Acceptance Criteria:**
- [ ] Live W&B dashboard accessible via public link
- [ ] Show judges real usage during demo
- [ ] Track cost per analysis

---

## 6. SAMPLE TEST DATA

### Report 1: healthy_25f.pdf
```
Patient: Jane Smith, 25F
Hemoglobin: 13.8 g/dL (Normal: 12.0-16.0)
Cholesterol: 175 mg/dL (Normal: <200)
Blood Sugar: 88 mg/dL (Normal: 70-100)
Vitamin D: 42 ng/mL (Normal: 30-100)
Iron: 95 mcg/dL (Normal: 60-170)
Expected Output: GREEN - All normal
```

### Report 2: deficient_40m.pdf
```
Patient: John Doe, 40M
Hemoglobin: 11.2 g/dL (Normal: 13.5-17.5) ← LOW
Cholesterol: 215 mg/dL (Normal: <200) ← HIGH
Blood Sugar: 95 mg/dL (Normal: 70-100)
Vitamin D: 18 ng/mL (Normal: 30-100) ← LOW
Iron: 45 mcg/dL (Normal: 60-170) ← LOW
Expected Output: YELLOW - 3 concerns
```

### Report 3: risk_55m.pdf
```
Patient: Robert Chen, 55M
Hemoglobin: 10.1 g/dL ← VERY LOW
Cholesterol: 268 mg/dL ← HIGH
Blood Sugar: 126 mg/dL ← PRE-DIABETIC
Vitamin D: 12 ng/mL ← CRITICALLY LOW
Triglycerides: 210 mg/dL ← HIGH
Expected Output: RED - Urgent attention needed
```

---

## 7. API CONFIGURATION
```python
# .env file
MISTRAL_API_KEY=your_key_here
WANDB_API_KEY=your_key_here
HF_TOKEN=your_key_here

# config.py
MISTRAL_MODELS = {
    "analyzer": "mistral-large-latest",
    "voice": "voxtral-v0-2507",
    "agent": "mistral-large-latest"
}

MISTRAL_PARAMS = {
    "temperature": 0.3,   # Low = more consistent medical output
    "max_tokens": 2000,
    "response_format": {"type": "json_object"}
}
```

---

## 8. PITCH DECK STRUCTURE (5 Slides)

| Slide | Content |
|---|---|
| **1 — Hook** | "You got your blood test back. Can you understand it?" Show confusing lab report image |
| **2 — Problem** | 500M blood tests done yearly. 80% of patients don't understand results. Doctors have 7 min per patient |
| **3 — Demo** | LIVE: Upload report → watch GutCheck analyze in real time |
| **4 — Tech** | Mistral Large 3 + Voxtral + Agents diagram |
| **5 — Vision** | Next: Connect to wearables, track over time, predict issues before they happen |

**Pitch Hook (First 10 seconds):**
> *"I got my blood test back last year. 
> My doctor had 4 minutes. 
> I had 23 confusing numbers. 
> I had no idea if I was dying or fine. 
> GutCheck fixes that."*

---

## 9. SUBMISSION CHECKLIST

- [ ] GitHub repo with clean README
- [ ] Live demo on Hugging Face Spaces
- [ ] W&B dashboard public link
- [ ] 3 sample PDFs in repo for judges to test
- [ ] 2-minute demo video
- [ ] Submit on Hackiterate before deadline

---

## 10. SUCCESS METRICS

| Metric | Target |
|---|---|
| Analysis accuracy | Correctly flags 90%+ of abnormal values |
| Response time | Under 10 seconds per analysis |
| Demo uptime | 100% during judging window |
| Pitch time | Under 2 minutes |

---

*Built for Mistral AI Worldwide Hackathon 2026*
*Track: Anything Goes | Category: Health & Wellness*
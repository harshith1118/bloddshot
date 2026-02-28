# ✅ GutCheck - Final Verification Checklist

## Pre-Deployment Tests

Run these tests before deploying:

### 1. Core Functionality Test
```bash
cd C:\Users\Lenovo\Desktop\mistral
python -c "
from core.pdf_extractor import extract_text_from_pdf
from core.analyzer import BiomarkerAnalyzer

# Test PDF extraction
for pdf in ['healthy_25f.pdf', 'deficient_40m.pdf', 'risk_55m.pdf']:
    with open(f'sample_reports/{pdf}', 'rb') as f:
        text, method = extract_text_from_pdf(f.read())
    print(f'{pdf}: {len(text)} chars extracted via {method}')

# Test analyzer
analyzer = BiomarkerAnalyzer()
print(f'Analyzer ready: {analyzer.model}')
"
```

Expected output:
- All 3 PDFs extract successfully
- Different character counts for each PDF
- Analyzer initializes without error

### 2. Frontend Build Test
```bash
cd gutcheck-web
npm run build
```

Expected output:
- `✓ built in X.XXs`
- No errors
- `dist/` folder updated

### 3. Local Server Test
```bash
cd C:\Users\Lenovo\Desktop\mistral
python gutcheck-web/main.py
```

Then open http://localhost:7860 and:
- Upload each sample PDF
- Verify different results for each
- Check response time < 30 seconds

---

## Deployment Steps

### 1. Create Hugging Face Space
- URL: https://huggingface.co/spaces/create
- Name: `gutcheck`
- SDK: **Docker**
- Visibility: Public

### 2. Add API Secret
- Settings → Repository secrets
- Name: `MISTRAL_API_KEY`
- Value: Your API key

### 3. Push Code
```bash
cd C:\Users\Lenovo\Desktop\mistral
git init
git add .
git commit -m "GutCheck v1.0 - Hackathon submission"

# Replace YOUR_USERNAME
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/gutcheck
git push -u hf main
```

### 4. Monitor Build
- Go to Space → App tab
- Watch build logs
- Wait for "Running" status (~10-15 min)

### 5. Test Live
- Upload `healthy_25f.pdf` → Should show GREEN
- Upload `risk_55m.pdf` → Should show RED
- Verify different results

---

## Hackathon Submission

### Required Links
1. **Live Demo:** https://huggingface.co/spaces/YOUR_USERNAME/gutcheck
2. **GitHub:** https://github.com/YOUR_USERNAME/gutcheck

### Submission Checklist
- [ ] Space is Public
- [ ] MISTRAL_API_KEY secret added
- [ ] All 3 sample PDFs tested
- [ ] Different PDFs = Different results
- [ ] Response time < 30 seconds
- [ ] UI looks professional
- [ ] GitHub README is complete
- [ ] Hackiterate submission complete

---

## Common Issues & Fixes

### Build Fails
**Issue:** Docker build timeout
**Fix:** Wait 5 minutes, HF auto-retries

### 500 Error
**Issue:** Missing API key
**Fix:** Add MISTRAL_API_KEY in Space secrets

### Same Results for All PDFs
**Issue:** Should show different results
**Fix:** Already fixed - reduced max_tokens, simplified prompt

### Slow Response (>60s)
**Issue:** API taking too long
**Fix:** Already fixed - max_tokens reduced to 2000

---

## Success Criteria

| Criteria | Status |
|----------|--------|
| PDF upload works | ✅ |
| Different PDFs = Different results | ✅ |
| Response time < 30s | ✅ |
| Professional UI | ✅ |
| No emoji overload | ✅ |
| Deployed on HF Spaces | ⏳ |
| Public accessibility | ⏳ |

---

**Ready for deployment!** 🚀

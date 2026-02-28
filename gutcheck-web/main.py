"""
GutCheck Web Backend
FastAPI server that serves React frontend and handles PDF analysis
"""

import os
import sys
import json

# Add parent directory to path so we can import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from core.pdf_extractor import extract_text_from_pdf, validate_pdf
from core.analyzer import BiomarkerAnalyzer

load_dotenv()

app = FastAPI(title="GutCheck API")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (React build)
try:
    app.mount("/assets", StaticFiles(directory="gutcheck-web/dist/assets"), name="assets")
except:
    pass  # Directory might not exist in dev mode


class AnalysisResponse(BaseModel):
    overall_status: str
    summary: str
    biomarkers: list
    top_priorities: list
    disclaimer: str


@app.get("/")
async def serve_frontend():
    """Serve the React app"""
    try:
        return FileResponse("gutcheck-web/dist/index.html")
    except FileNotFoundError:
        return JSONResponse({
            "message": "Frontend not built. Run 'npm run build' in gutcheck-web directory."
        })


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_blood_test(pdf: UploadFile = File(...)):
    """
    Analyze a blood test PDF and return results
    """
    try:
        # Read PDF
        pdf_bytes = await pdf.read()
        
        # Validate PDF
        is_valid, error_msg = validate_pdf(pdf_bytes)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Extract text
        extracted_text, extraction_method = extract_text_from_pdf(pdf_bytes)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        # Analyze with Mistral
        analyzer = BiomarkerAnalyzer()
        
        # Validate it's a blood test report
        validation = analyzer.validate_report(extracted_text)
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail="This doesn't appear to be a blood test report"
            )
        
        # Run analysis
        result = analyzer.analyze(extracted_text)
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gutcheck-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

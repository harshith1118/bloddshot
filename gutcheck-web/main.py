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
        print(f"Received PDF: {pdf.filename}, size: {pdf.size if hasattr(pdf, 'size') else 'unknown'}")
        
        # Read PDF
        pdf_bytes = await pdf.read()
        print(f"Read {len(pdf_bytes)} bytes")

        # Validate PDF
        is_valid, error_msg = validate_pdf(pdf_bytes)
        if not is_valid:
            print(f"PDF validation failed: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)

        # Extract text
        print("Extracting text from PDF...")
        extracted_text, extraction_method = extract_text_from_pdf(pdf_bytes)
        print(f"Text extraction complete: method={extraction_method}, chars={len(extracted_text) if extracted_text else 0}")

        if not extracted_text:
            print("Failed to extract text from PDF")
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

        # Analyze with Mistral
        print("Initializing BiomarkerAnalyzer...")
        analyzer = BiomarkerAnalyzer()

        # Validate it's a blood test report
        validation = analyzer.validate_report(extracted_text)
        print(f"Report validation: {validation}")
        if not validation["is_valid"]:
            raise HTTPException(
                status_code=400,
                detail="This doesn't appear to be a blood test report"
            )

        # Run analysis
        print("Running biomarker analysis...")
        result = analyzer.analyze(extracted_text)
        print(f"Analysis complete: {len(result.get('biomarkers', []))} biomarkers")

        return JSONResponse(content=result)

    except HTTPException as he:
        print(f"HTTP Exception: {he.detail}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "gutcheck-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

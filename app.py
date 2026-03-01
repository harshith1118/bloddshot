"""
GutCheck - Blood Test Analyzer
Main Streamlit Application Entry Point

Built for Mistral AI Worldwide Hackathon 2026
"""

import streamlit as st
import time
from typing import Optional, Dict, Any

from core.pdf_extractor import extract_text_from_pdf, validate_pdf
from core.analyzer import BiomarkerAnalyzer
from core.voice import VoiceGenerator
from core.agent import ResearchAgent
from utils.helpers import (
    format_status_emoji,
    format_biomarker_status,
    get_status_color_hex,
    create_analysis_summary,
    format_recommendations
)
from utils.tracker import get_tracker

# Page configuration
st.set_page_config(
    page_title="GutCheck - Blood Test Analyzer",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    /* Tagline */
    .tagline {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Status Cards */
    .status-card {
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-left: 5px solid;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .status-card h2 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Biomarker Cards */
    .biomarker-card {
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .biomarker-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Recommendation Box */
    .recommendation-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #0ea5e9;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border-left: 5px solid #f59e0b;
        margin-top: 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #3B82F6;
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "extracted_text" not in st.session_state:
        st.session_state.extracted_text = None
    if "extraction_method" not in st.session_state:
        st.session_state.extraction_method = None
    if "audio_data" not in st.session_state:
        st.session_state.audio_data = None


def render_header():
    """Render the app header."""
    st.markdown('<p class="main-header">🩸 GutCheck</p>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">Your blood test, finally explained.</p>', unsafe_allow_html=True)


def render_upload_section() -> Optional[bytes]:
    """Render the PDF upload section."""
    st.markdown("""
    <div class="upload-section">
        <h3 style="margin-top: 0; color: #1e293b;">📄 Upload Your Blood Test Report</h3>
        <p style="color: #64748b; margin-bottom: 1rem;">
            Upload your blood test report PDF (max 10MB). We'll analyze all biomarkers 
            and give you clear, actionable insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload your blood test report PDF (max 10MB)",
        key="pdf_uploader"
    )
    
    if uploaded_file is not None:
        return uploaded_file.read()
    
    return None


def render_analysis_results(analysis_result: Dict[str, Any]):
    """Render the analysis results."""
    overall_status = analysis_result.get("overall_status", "UNKNOWN")
    summary = analysis_result.get("summary", "No summary available.")
    biomarkers = analysis_result.get("biomarkers", [])
    top_priorities = analysis_result.get("top_priorities", [])
    disclaimer = analysis_result.get(
        "disclaimer",
        "⚕️ This analysis is for educational purposes only. Please consult your doctor for medical advice."
    )
    
    # Overall Status Card
    status_color = get_status_color_hex(overall_status)
    status_emoji = format_status_emoji(overall_status)
    
    flagged_count = sum(
        1 for b in biomarkers 
        if b.get("status", "").upper() in ["BORDERLINE", "CONCERN"]
    )
    
    st.markdown(
        f"""
        <div class="status-card" style="border-color: {status_color};">
            <h2 style="margin: 0; color: {status_color};">
                {status_emoji} Overall Status: {overall_status}
            </h2>
            <p style="margin: 0.5rem 0 0 0; color: #64748b;">
                {flagged_count} biomarker(s) need attention
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Summary
    st.markdown("### 📋 Summary")
    st.info(summary)
    
    # Top Priorities
    if top_priorities:
        st.markdown("### 🎯 Top Priorities")
        for i, priority in enumerate(top_priorities, 1):
            st.markdown(f"{i}. {priority}")
    
    # Biomarkers Section
    st.markdown("### 🔬 Biomarker Analysis")
    
    for biomarker in biomarkers:
        name = biomarker.get("name", "Unknown")
        value = biomarker.get("value", "N/A")
        unit = biomarker.get("unit", "")
        normal_range = biomarker.get("normal_range", "N/A")
        status = biomarker.get("status", "UNKNOWN")
        explanation = biomarker.get("explanation", "No explanation available.")
        recommendations = biomarker.get("recommendations", [])
        
        status_icon, status_text, status_color_name = format_biomarker_status(status)
        status_hex = get_status_color_hex(status)
        
        with st.expander(
            f"{status_icon} **{name}** — {value} {unit} ({status_text})",
            expanded=(status.upper() in ["BORDERLINE", "CONCERN"])
        ):
            st.markdown(f"""
            **Value:** {value} {unit}  
            **Reference Range:** {normal_range}  
            **Status:** {status_text}
            """)
            
            st.markdown("**Explanation:**")
            st.write(explanation)
            
            if recommendations:
                st.markdown("**Recommendations:**")
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. {rec}")
    
    # Disclaimer
    st.markdown(f'<div class="disclaimer">{disclaimer}</div>', unsafe_allow_html=True)


def render_voice_button(analysis_result: Dict[str, Any]):
    """Render the voice readout button."""
    st.markdown("### 🔊 Voice Output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔊 Read Results Aloud", use_container_width=True, disabled=True):
            with st.spinner("Generating voice..."):
                try:
                    voice_gen = VoiceGenerator()
                    audio_bytes = voice_gen.generate_summary_speech(analysis_result)
                    
                    if audio_bytes:
                        st.session_state.audio_data = audio_bytes
                        st.success("Voice generated!")
                        st.audio(audio_bytes, format="audio/mp3")
                    else:
                        st.error("Failed to generate voice.")
                        
                except Exception as e:
                    st.error(f"Voice generation error: {str(e)}")
    
    # Show info about voice availability
    st.info("""
    **🔊 Voice Output (Coming Soon)**
    
    Voice generation using Voxtral requires API access. 
    For now, you can read the analysis results above.
    
    *Voice feature will be enabled when Voxtral API access is available.*
    """)
    
    with col2:
        if st.button("🔍 Deep Dive Research", use_container_width=True):
            st.session_state.show_research = True


def render_research_section(analysis_result: Dict[str, Any]):
    """Render the deep dive research section."""
    st.markdown("### 🔬 Deep Dive Research")
    
    biomarkers = analysis_result.get("biomarkers", [])
    flagged = [b for b in biomarkers if b.get("status", "").upper() in ["BORDERLINE", "CONCERN"]]
    
    if not flagged:
        st.info("All biomarkers are normal. No deep dive needed!")
        return
    
    selected = st.selectbox(
        "Select a biomarker to research:",
        options=[b.get("name") for b in flagged],
        key="research_biomarker"
    )
    
    if selected and st.button("Search Research"):
        with st.spinner("Searching latest research..."):
            try:
                agent = ResearchAgent()
                biomarker_data = next(b for b in flagged if b.get("name") == selected)
                
                result = agent.research_biomarker(
                    biomarker_name=selected,
                    status=biomarker_data.get("status", ""),
                    explanation=biomarker_data.get("explanation", "")
                )
                
                st.markdown(result.get("findings", "No findings available."))
                
                if result.get("sources"):
                    st.markdown("**Sources:**")
                    for source in result["sources"]:
                        st.markdown(f"- {source}")
                        
            except Exception as e:
                st.error(f"Research error: {str(e)}")


def main():
    """Main application function."""
    initialize_session_state()
    render_header()
    
    # Initialize tracker
    tracker = get_tracker()
    tracker.initialize()
    
    # Upload section
    pdf_bytes = render_upload_section()
    
    if pdf_bytes:
        # Validate PDF
        is_valid, error_msg = validate_pdf(pdf_bytes)
        if not is_valid:
            st.error(error_msg)
            return
        
        # Analyze button
        if st.button("🔬 Analyze Report", type="primary", use_container_width=True):
            start_time = time.time()
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("⏳ Extracting text from PDF...")
            progress_bar.progress(25)
            
            extracted_text, extraction_method = extract_text_from_pdf(pdf_bytes)
            
            if not extracted_text:
                st.error("Failed to extract text from PDF. Please try a different file.")
                tracker.log_error("PDF_EXTRACTION_FAILED", "Could not extract text")
                progress_bar.empty()
                status_text.empty()
                return
            
            st.session_state.extracted_text = extracted_text
            st.session_state.extraction_method = extraction_method
            progress_bar.progress(50)
            status_text.text(f"✅ Text extracted ({extraction_method})")
            
            status_text.text("🤖 Analyzing biomarkers with AI...")
            progress_bar.progress(60)

            try:
                analyzer = BiomarkerAnalyzer()

                # Validate it's a blood test report
                validation = analyzer.validate_report(extracted_text)
                if not validation["is_valid"]:
                    st.warning(validation["message"])

                # Run analysis with retry
                max_retries = 2
                analysis_result = None
                
                for attempt in range(max_retries):
                    try:
                        status_text.text(f"🤖 Analyzing... (attempt {attempt + 1}/{max_retries})")
                        analysis_result = analyzer.analyze(extracted_text)
                        if analysis_result and analysis_result.get("biomarkers"):
                            break
                    except Exception as retry_error:
                        if attempt == max_retries - 1:
                            raise
                        time.sleep(1)
                
                if not analysis_result or not analysis_result.get("biomarkers"):
                    raise Exception("No biomarkers detected in analysis result")

                response_time = time.time() - start_time

                st.session_state.analysis_result = analysis_result

                progress_bar.progress(100)
                status_text.text(f"✅ Analysis complete in {response_time:.1f}s!")

                # Log to W&B
                tracker.log_analysis(
                    pdf_size_kb=len(pdf_bytes) / 1024,
                    extraction_method=extraction_method,
                    response_time_sec=response_time,
                    overall_status=analysis_result.get("overall_status"),
                    biomarker_count=len(analysis_result.get("biomarkers", []))
                )

                # Auto-hide progress after success
                time.sleep(0.3)
                progress_bar.empty()
                status_text.empty()

                st.success(f"Analysis complete in {response_time:.1f} seconds!")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Analysis error: {str(e)}")
                tracker.log_error("ANALYSIS_FAILED", str(e))
    
    # Display results if available
    if st.session_state.analysis_result:
        st.divider()
        render_analysis_results(st.session_state.analysis_result)
        
        st.divider()
        render_voice_button(st.session_state.analysis_result)
        
        if st.session_state.get("show_research", False):
            st.divider()
            render_research_section(st.session_state.analysis_result)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>
            <strong>Built with Mistral Large 3 + Voxtral + Agents API</strong><br>
            Mistral AI Worldwide Hackathon 2026 | Track: Anything Goes
        </p>
        <p style="margin-top: 0.5rem; font-size: 0.75rem; color: #cbd5e1;">
            ⚕️ This analysis is for educational purposes only. Please consult your doctor for medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

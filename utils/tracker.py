"""
Weights & Biases Experiment Tracking
Tracks API calls, token usage, response times for dashboard.
"""

import os
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class WandBTracker:
    """Tracks GutCheck usage metrics with Weights & Biases."""
    
    def __init__(self, project_name: str = "gutcheck"):
        self.api_key = os.getenv("WANDB_API_KEY")
        self.enabled = self.api_key is not None
        self.project_name = project_name
        self.run = None
        self._initialized = False
    
    def initialize(self):
        """Initialize W&B run."""
        if not self.enabled:
            print("W&B tracking disabled (no WANDB_API_KEY)")
            return
        
        if self._initialized:
            return
        
        try:
            import wandb
            
            self.run = wandb.init(
                project=self.project_name,
                name="gutcheck-demo",
                config={
                    "model": "mistral-large-latest",
                    "voice_model": "voxtral-v0-2507",
                    "hackathon": "Mistral AI Worldwide Hackathon 2026"
                }
            )
            self._initialized = True
            print("W&B tracking initialized")
            
        except Exception as e:
            print(f"W&B initialization failed: {e}")
            self.enabled = False
    
    def log_analysis(self, 
                     pdf_size_kb: float,
                     extraction_method: str,
                     response_time_sec: float,
                     token_count: Optional[int] = None,
                     overall_status: Optional[str] = None,
                     biomarker_count: Optional[int] = None):
        """Log a complete analysis event."""
        if not self.enabled or not self._initialized:
            return
        
        try:
            import wandb
            
            metrics = {
                "analysis/pdf_size_kb": pdf_size_kb,
                "analysis/extraction_method": extraction_method,
                "analysis/response_time_sec": response_time_sec,
                "analysis/timestamp": time.time()
            }
            
            if token_count:
                metrics["analysis/token_count"] = token_count
            
            if overall_status:
                metrics["analysis/overall_status"] = overall_status
            
            if biomarker_count:
                metrics["analysis/biomarker_count"] = biomarker_count
            
            wandb.log(metrics)
            
        except Exception as e:
            print(f"W&B log failed: {e}")
    
    def log_voice_request(self, generation_time_sec: float, success: bool):
        """Log a voice generation request."""
        if not self.enabled or not self._initialized:
            return
        
        try:
            import wandb
            
            wandb.log({
                "voice/generation_time_sec": generation_time_sec,
                "voice/success": 1 if success else 0,
                "voice/timestamp": time.time()
            })
            
        except Exception as e:
            print(f"W&B log failed: {e}")
    
    def log_research_request(self, biomarker: str, search_time_sec: float, success: bool):
        """Log a deep dive research request."""
        if not self.enabled or not self._initialized:
            return
        
        try:
            import wandb
            
            wandb.log({
                "research/search_time_sec": search_time_sec,
                "research/success": 1 if success else 0,
                "research/biomarker": biomarker,
                "research/timestamp": time.time()
            })
            
        except Exception as e:
            print(f"W&B log failed: {e}")
    
    def log_error(self, error_type: str, error_message: str, context: Optional[Dict] = None):
        """Log an error event."""
        if not self.enabled or not self._initialized:
            return
        
        try:
            import wandb
            
            metrics = {
                "error/type": error_type,
                "error/message": error_message,
                "error/timestamp": time.time()
            }
            
            if context:
                for key, value in context.items():
                    metrics[f"error/context_{key}"] = value
            
            wandb.log(metrics)
            
        except Exception as e:
            print(f"W&B log failed: {e}")
    
    def get_public_url(self) -> Optional[str]:
        """Get the public URL for the W&B dashboard."""
        if not self._initialized or not self.run:
            return None
        
        return self.run.get_url()
    
    def finish(self):
        """Finish the W&B run."""
        if self.run:
            try:
                import wandb
                wandb.finish()
                self._initialized = False
            except Exception as e:
                print(f"W&B finish failed: {e}")


# Global tracker instance
tracker = WandBTracker()


def get_tracker() -> WandBTracker:
    """Get the global tracker instance."""
    return tracker

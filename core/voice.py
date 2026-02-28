"""
Voice Output Module
Uses Mistral Speech API for text-to-speech output.
"""

import os
import base64
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class VoiceGenerator:
    """Generates speech from text using Mistral TTS."""
    
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment")
        
        # Voxtral model as per PRD
        self.model = "voxtral-v0-2507"
        
        # Initialize Mistral client
        from mistralai import Mistral
        self.client = Mistral(api_key=self.api_key)
    
    def generate_speech(self, text: str) -> Optional[bytes]:
        """
        Generate speech audio from text using Voxtral.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio file bytes or None if failed
        """
        try:
            # Prepare the text for voice output
            # Remove markdown, emojis, and technical formatting
            clean_text = self._clean_text_for_voice(text)
            
            response = self.client.audio.generate(
                model=self.model,
                input=clean_text,
                response_format="mp3"
            )
            
            return response.audio_data
            
        except Exception as e:
            print(f"Voice generation failed: {e}")
            return None
    
    def _clean_text_for_voice(self, text: str) -> str:
        """
        Clean text for better voice output.
        Removes emojis, markdown, and technical formatting.
        """
        import re
        
        # Remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub("", text)
        
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def generate_summary_speech(self, analysis_result: Dict[str, Any]) -> Optional[bytes]:
        """
        Generate speech for just the summary and key points.
        Optimized for quicker playback.
        
        Args:
            analysis_result: The full analysis JSON
            
        Returns:
            Audio file bytes or None if failed
        """
        # Create a concise script for voice output
        summary = analysis_result.get("summary", "")
        status = analysis_result.get("overall_status", "")
        
        # Build voice script
        script_parts = [f"Your blood test analysis is complete. Overall status: {status}."]
        script_parts.append(summary)
        
        # Add top priorities
        priorities = analysis_result.get("top_priorities", [])
        if priorities:
            script_parts.append("Here are your top priorities:")
            for i, priority in enumerate(priorities[:3], 1):
                script_parts.append(f"{i}. {priority}")
        
        # Add disclaimer
        script_parts.append("Remember, this analysis is for educational purposes only. Please consult your doctor for medical advice.")
        
        full_script = " ".join(script_parts)
        
        return self.generate_speech(full_script)

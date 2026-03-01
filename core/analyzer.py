"""
Biomarker Analysis Engine
Uses Mistral Large 3 to analyze blood test reports and generate JSON responses.
"""

import json
import os
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from prompts.system_prompt import get_system_prompt

load_dotenv()


def extract_json_from_response(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract valid JSON from model response text.
    Handles markdown code blocks and fixes common JSON issues.
    """
    if not text:
        print("ERROR: Empty response from model")
        return None

    # Clean up the text - remove markdown code blocks
    text = text.strip()
    
    # Remove markdown code block wrappers if present
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Direct JSON parse failed: {e}")
        pass

    # Try to extract JSON from markdown code block
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            print(f"Markdown block JSON parse failed: {e}")
            pass

    # Look for any JSON object (first { to last })
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            json_str = text[start:end]
            # Fix common issues
            json_str = fix_json_string(json_str)
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Extracted JSON parse failed: {e}")
        print(f"JSON string was: {text[start:end][:200]}...")
        pass
    except Exception as e:
        print(f"Unexpected error during JSON extraction: {e}")
        pass

    return None


def fix_json_string(json_str: str) -> str:
    """
    Fix common JSON string issues.
    """
    # Fix unescaped newlines in strings (but not outside strings)
    # This is a simplified fix - replace literal newlines in strings with \n
    lines = json_str.split('\n')
    fixed_lines = []
    in_string = False
    
    for line in lines:
        if in_string:
            # We're continuing a string from previous line
            fixed_lines.append('\\n' + line.rstrip())
        else:
            fixed_lines.append(line.rstrip())
        
        # Count quotes to see if we're in a string
        # Simple heuristic: odd number of unescaped quotes means we're in a string
        quote_count = 0
        i = 0
        while i < len(line):
            if line[i] == '"' and (i == 0 or line[i-1] != '\\'):
                quote_count += 1
            i += 1
        
        if quote_count % 2 == 1:
            in_string = not in_string
    
    return '\n'.join(fixed_lines)


class BiomarkerAnalyzer:
    """Analyzes blood test reports using Mistral."""

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment. Please set it in your .env file or Space secrets.")

        # Use mistral-medium for faster response (good balance of speed/accuracy)
        self.model = "mistral-medium-latest"
        self.system_prompt = get_system_prompt()

        # Initialize Mistral client with timeout
        from mistralai import Mistral
        self.client = Mistral(api_key=self.api_key, timeout=30)
        print(f"Mistral client initialized with model: {self.model}")

    def analyze(self, extracted_text: str) -> Dict[str, Any]:
        """
        Analyze extracted PDF text and return structured results.
        Optimized for speed.
        """
        # Pre-process: truncate text to essential content (reduce tokens)
        processed_text = self._preprocess_text(extracted_text)
        print(f"Analyzing text ({len(processed_text)} chars)...")

        user_message = f"""{processed_text}

Return JSON only."""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,  # Lower temp for faster, more deterministic output
                max_tokens=2500,  # Reduced from 4000 - blood tests don't need more
                response_format={"type": "json_object"},
            )

            result_text = response.choices[0].message.content
            print(f"Raw API response length: {len(result_text)} chars")

            # Check if response was truncated
            if not result_text or result_text.strip() == "":
                print("ERROR: Empty response from API")
                return self._get_fallback_response("Empty response from AI model")

            # Check if JSON is complete (ends with })
            result_text = result_text.strip()
            if not result_text.endswith('}'):
                print("WARNING: Response appears truncated, attempting to fix...")
                last_brace = result_text.rfind('}')
                if last_brace > 0:
                    result_text = result_text[:last_brace+1]
                    print(f"Truncated to last complete JSON object: {len(result_text)} chars")

            result = extract_json_from_response(result_text)

            if result is None:
                print(f"Failed to parse JSON. Full response: {result_text[:1000]}...")
                return self._get_fallback_response("Could not parse AI response")

            print(f"Successfully parsed result with {len(result.get('biomarkers', []))} biomarkers")
            return result

        except Exception as e:
            print(f"API call failed: {str(e)}")
            return self._get_fallback_response(f"API error: {str(e)}")

    def _preprocess_text(self, text: str) -> str:
        """
        Pre-process PDF text to reduce token count and remove noise.
        """
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and len(line) > 1:  # Skip empty or single-char lines
                cleaned_lines.append(line)
        
        # Rejoin with single newlines
        cleaned = '\n'.join(cleaned_lines)
        
        # Remove duplicate consecutive lines
        lines = cleaned.split('\n')
        unique_lines = []
        prev = None
        for line in lines:
            if line != prev:
                unique_lines.append(line)
                prev = line
        
        return '\n'.join(unique_lines)
    
    def _get_fallback_response(self, error_msg: str) -> Dict[str, Any]:
        """Return a structured fallback response on error."""
        return {
            "overall_status": "UNKNOWN",
            "summary": f"Analysis failed: {error_msg}. Please try again or check the logs.",
            "biomarkers": [],
            "top_priorities": ["Check Space logs for detailed error messages"],
            "disclaimer": "This analysis is for educational purposes only."
        }
    
    def analyze_with_streaming(self, extracted_text: str):
        """
        Analyze with streaming response for better UX.
        
        Args:
            extracted_text: Raw text extracted from blood test PDF
            
        Yields:
            Chunks of the response as they arrive
        """
        user_message = f"""Please analyze this blood test report:

{extracted_text}

Remember to return ONLY valid JSON matching the required schema."""

        stream = self.client.chat.stream(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        for chunk in stream:
            if chunk.data.choices[0].delta.content:
                yield chunk.data.choices[0].delta.content
    
    def validate_report(self, extracted_text: str) -> Dict[str, Any]:
        """
        Quick validation to check if the text appears to be a blood test report.
        
        Args:
            extracted_text: Raw text to validate
            
        Returns:
            Dictionary with validation results
        """
        # Check for common blood test keywords
        keywords = [
            "hemoglobin", "cholesterol", "glucose", "blood sugar",
            "vitamin", "iron", "platelet", "white blood", "red blood",
            "hdl", "ldl", "triglyceride", "creatinine", "albumin",
            "mg/dl", "g/dl", "mmol/l", "reference range", "lab results"
        ]
        
        text_lower = extracted_text.lower()
        found_keywords = [kw for kw in keywords if kw in text_lower]
        
        if len(found_keywords) < 2:
            return {
                "is_valid": False,
                "message": "This doesn't appear to be a blood test report. "
                          f"Found only {len(found_keywords)} relevant terms.",
                "found_terms": found_keywords
            }
        
        return {
            "is_valid": True,
            "message": f"Valid blood test report detected. Found {len(found_keywords)} relevant terms.",
            "found_terms": found_keywords
        }

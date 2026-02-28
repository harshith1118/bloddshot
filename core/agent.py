"""
Research Agent Module
Uses Mistral Agents API with web_search tool for deep dive research.
"""

import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from prompts.agent_prompt import get_agent_prompt

load_dotenv()


class ResearchAgent:
    """Research agent that searches the web for biomarker information."""
    
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment")
        
        self.model = "mistral-large-latest"
        self.instructions = get_agent_prompt()
        
        # Initialize Mistral client
        from mistralai import Mistral
        self.client = Mistral(api_key=self.api_key)
    
    def research_biomarker(self, biomarker_name: str, status: str, explanation: str) -> Dict[str, Any]:
        """
        Research a specific biomarker using web search.
        
        Args:
            biomarker_name: Name of the biomarker (e.g., "Vitamin D")
            status: Status (NORMAL, BORDERLINE, CONCERN)
            explanation: Brief explanation of the issue
            
        Returns:
            Dictionary with research findings and sources
        """
        # Build the research query
        query = self._build_research_query(biomarker_name, status, explanation)
        
        # Use Mistral's built-in web search tool via agent pattern
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,
                max_tokens=1000,
                tools=[{"type": "web_search"}]
            )
            
            # Extract response and tool calls
            message = response.choices[0].message
            
            result = {
                "biomarker": biomarker_name,
                "findings": message.content,
                "sources": [],
                "search_performed": True
            }
            
            # Extract sources from tool calls if available
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "web_search":
                        # Parse search results if available
                        pass
            
            return result
            
        except Exception as e:
            return {
                "biomarker": biomarker_name,
                "findings": f"Research unavailable: {str(e)}",
                "sources": [],
                "search_performed": False
            }
    
    def _build_research_query(self, biomarker: str, status: str, explanation: str) -> str:
        """Build an optimized search query for the biomarker."""
        return f"""Research this biomarker concern:

Biomarker: {biomarker}
Status: {status}
Issue: {explanation}

Please search for:
1. Latest research (2024-2026) on {biomarker.lower()} abnormalities
2. Evidence-based interventions and treatments
3. When someone should urgently see a doctor for this condition

Provide cited sources with links."""
    
    def quick_research(self, biomarker_name: str) -> str:
        """
        Quick research without full agent pattern.
        Falls back to model knowledge if web search unavailable.
        
        Args:
            biomarker_name: Name of the biomarker
            
        Returns:
            Research summary text
        """
        query = f"""Provide a brief research summary for {biomarker_name}:

1. What recent studies (2024-2026) say about this condition
2. Most effective evidence-based interventions
3. When to urgently see a doctor

Keep it under 150 words. Cite any sources you reference."""

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful medical research assistant. Provide accurate, cited information."},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Research temporarily unavailable. Please consult your healthcare provider for information about {biomarker_name}."

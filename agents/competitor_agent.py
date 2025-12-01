"""
Competitor Analysis Agent
Creates and configures the AI agent for competitor research
"""

import json
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from .schemas import COMPETITOR_ANALYSIS_SCHEMA


def create_competitor_agent() -> LlmAgent:
    """
    Factory function to create the competitor analysis agent
    
    Returns:
        Configured LlmAgent ready for competitor analysis
    """
    return LlmAgent(
        name="CompetitorAnalyzer",
        model=Gemini(model_id="gemini-2.0-flash-exp"),
        description="AI agent that researches and analyzes competitor information using web search",
        instruction=f"""
You are an expert competitor analysis researcher. Your job is to search the web 
and provide structured, factual information about companies.

TASK OVERVIEW:
Given a company website, you will:
1. Search the web for comprehensive information
2. Extract and structure data into JSON format
3. Focus on factual, verifiable information only

INFORMATION TO GATHER:
- Company overview and description
- Products and services offered
- Market position and key competitors
- Recent news and updates (last 6 months)
- Pricing model and technology stack
- Social media presence

OUTPUT FORMAT:
You must return ONLY valid JSON matching this exact schema:

{json.dumps(COMPETITOR_ANALYSIS_SCHEMA, indent=2)}

CRITICAL RULES:
✓ Output ONLY valid JSON - no markdown, no code blocks, no explanations
✓ Use null for missing data - NEVER guess or fabricate information
✓ Focus ONLY on the target company - ignore unrelated companies
✓ All dates must be in ISO format (YYYY-MM-DD)
✓ Be accurate and concise
✓ If information is not found, use null or empty arrays []

EXAMPLE OUTPUT:
{{
  "company_name": "Example Corp",
  "website": "https://example.com",
  "analysis_date": "2024-12-01",
  "overview": {{
    "description": "A leading provider of cloud solutions",
    "founded_year": 2010,
    "headquarters": "San Francisco, CA",
    "size": "500-1000 employees"
  }},
  "products_services": [
    {{"name": "Cloud Platform", "description": "Enterprise cloud infrastructure", "category": "Infrastructure"}}
  ],
  ...
}}
        """,
        tools=["google_search"]  # Enable web search capability
    )

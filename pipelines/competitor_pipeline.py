"""
Competitor Analysis Pipelines
Orchestrates the agent, data processing, and report generation
"""

import json
from typing import Dict, Any, List, Tuple
from datetime import datetime

from google.adk.runners import Runner
from agents import create_competitor_agent
from services import format_html_from_json


class OptimizedCompetitorAnalysisPipeline:
    """
    Optimized single-company analysis pipeline
    
    Cost Optimization: Uses ONLY 1 LLM call instead of 3
    - Traditional approach: DataCollector → Summarizer → ReportWriter (3 calls)
    - Optimized approach: Unified agent does all at once (1 call)
    - Savings: 67% reduction in API costs
    """
    
    def __init__(self):
        """Initialize the pipeline with agent and runner"""
        self.agent = create_competitor_agent()
        self.runner = Runner()
    
    def analyze_competitor(
        self, 
        company_website: str, 
        company_name: str = None
    ) -> str:
        """
        Analyze a single competitor and generate HTML report
        
        Args:
            company_website: Target company's website URL
            company_name: Optional company name for better results
            
        Returns:
            Complete HTML report as string
            
        Raises:
            ValueError: If analysis fails or response cannot be parsed
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting Analysis: {company_name or company_website}")
        print(f"💰 Cost Optimization: 1 LLM call (saves 67% vs traditional)")
        print(f"{'='*60}\n")
        
        # Step 1: Create analysis prompt
        prompt = self._create_prompt(company_website, company_name)
        
        # Step 2: Run AI agent (SINGLE LLM CALL)
        print("🔍 Running AI analysis with web search...")
        response = self.runner.run(agent=self.agent, input_text=prompt)
        
        # Step 3: Parse JSON response
        structured_data = self._parse_response(response)
        print("✅ Data collected and structured\n")
        
        # Step 4: Generate HTML (NO LLM - Pure Python)
        print("📄 Generating HTML report (no LLM call)...")
        html_report = format_html_from_json(structured_data)
        print("✅ HTML report generated\n")
        
        print(f"{'='*60}")
        print("✨ Analysis Complete!")
        print(f"💰 Total LLM Calls: 1")
        print(f"{'='*60}\n")
        
        return html_report
    
    def _create_prompt(self, website: str, name: str = None) -> str:
        """Create analysis prompt for the agent"""
        return f"""
Analyze the competitor at: {website}
{f'Company Name: {name}' if name else ''}

Search for comprehensive information and return structured JSON data.
Current date: {datetime.now().strftime("%Y-%m-%d")}

Focus on gathering accurate, verifiable information from reliable sources.
        """.strip()
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """
        Parse agent response into structured JSON
        
        Handles multiple response formats:
        - Direct JSON objects
        - JSON wrapped in markdown code blocks
        - Plain text JSON
        """
        try:
            # Extract text from response
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            # Try direct JSON parsing
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Extract from markdown code blocks
                if "```json" in response_text:
                    json_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    json_text = response_text.split("```")[1].split("```")[0]
                else:
                    json_text = response_text
                
                return json.loads(json_text.strip())
        
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            print(f"Raw response preview: {response_text[:500]}...")
            raise ValueError(f"Failed to parse agent response: {e}")
    
    def save_report(self, html_content: str, filename: str = None) -> str:
        """
        Save HTML report to file
        
        Args:
            html_content: HTML report content
            filename: Optional filename (auto-generated if not provided)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"competitor_analysis_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Report saved to: {filename}")
        return filename


class BatchOptimizedPipeline(OptimizedCompetitorAnalysisPipeline):
    """
    Batch processing pipeline for multiple competitors
    
    Super Cost Optimization: Analyzes ALL companies in SINGLE LLM call
    - Traditional: 3 calls per company × N companies = 3N calls
    - Optimized single: 1 call per company × N companies = N calls
    - Batch optimized: 1 call total for all companies = 1 call
    - Savings: 90%+ for 10+ companies
    """
    
    def analyze_multiple_competitors(
        self, 
        companies: List[Tuple[str, str]]
    ) -> Dict[str, str]:
        """
        Analyze multiple competitors in a single batch
        
        Args:
            companies: List of (website, name) tuples
            Example: [("https://stripe.com", "Stripe"), ...]
            
        Returns:
            Dictionary mapping company_name → html_report
        """
        print(f"\n{'='*60}")
        print(f"🚀 BATCH Analysis for {len(companies)} competitors")
        print(f"💰 Cost Savings: ~{self._calculate_savings(len(companies))}% vs sequential")
        print(f"{'='*60}\n")
        
        # Create batch prompt
        batch_prompt = self._create_batch_prompt(companies)
        
        # Run batch analysis (SINGLE LLM CALL for ALL companies!)
        print(f"🔍 Running batch AI analysis for all {len(companies)} companies...")
        response = self.runner.run(agent=self.agent, input_text=batch_prompt)
        
        # Parse batch results
        try:
            batch_data = self._parse_batch_response(response)
        except Exception as e:
            print(f"❌ Batch parsing failed: {e}")
            print("🔄 Falling back to individual analysis...")
            return self._fallback_individual_analysis(companies)
        
        # Generate HTML reports for each company
        results = {}
        for data in batch_data:
            company_name = data.get("company_name", "Unknown")
            html = format_html_from_json(data)
            results[company_name] = html
            print(f"✅ Generated report for {company_name}")
        
        print(f"\n{'='*60}")
        print(f"✨ Batch Analysis Complete!")
        print(f"💰 Total LLM Calls: 1 (for {len(companies)} companies!)")
        print(f"💵 Savings: ~{self._calculate_savings(len(companies))}% vs individual")
        print(f"{'='*60}\n")
        
        return results
    
    def _create_batch_prompt(self, companies: List[Tuple[str, str]]) -> str:
        """Create batch analysis prompt for multiple companies"""
        companies_list = "\n".join([
            f"{i+1}. {name} - {url}" 
            for i, (url, name) in enumerate(companies)
        ])
        
        return f"""
Analyze these {len(companies)} competitors and return a JSON array with complete analysis for each.

Companies to analyze:
{companies_list}

Return a JSON ARRAY (not an object) where each element is a complete competitor analysis.
Each element must follow the exact schema provided in your instructions.

Output format:
[
  {{...complete data for company 1...}},
  {{...complete data for company 2...}},
  {{...complete data for company 3...}}
]

CRITICAL: 
- Output ONLY the JSON array, no markdown, no explanations
- Each company must have complete data
- Maintain consistent structure across all entries

Current date: {datetime.now().strftime("%Y-%m-%d")}
        """.strip()
    
    def _parse_batch_response(self, response) -> List[Dict[str, Any]]:
        """Parse batch response into list of company data"""
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        # Extract JSON array
        if "```json" in response_text:
            json_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            json_text = response_text.split("```")[1].split("```")[0]
        else:
            json_text = response_text
        
        batch_data = json.loads(json_text.strip())
        
        # Validate it's a list
        if not isinstance(batch_data, list):
            raise ValueError("Response is not a JSON array")
        
        return batch_data
    
    def _fallback_individual_analysis(
        self, 
        companies: List[Tuple[str, str]]
    ) -> Dict[str, str]:
        """Fallback: Analyze companies individually if batch fails"""
        print("⚠️ Using fallback: Individual analysis mode")
        results = {}
        
        for i, (url, name) in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] Analyzing {name}...")
            try:
                html = self.analyze_competitor(url, name)
                results[name] = html
            except Exception as e:
                print(f"❌ Failed: {e}")
                results[name] = self._create_error_report(name, str(e))
        
        return results
    
    def _create_error_report(self, company_name: str, error: str) -> str:
        """Create simple error report HTML"""
        return f"""
        <html>
        <head><title>Analysis Failed - {company_name}</title></head>
        <body>
            <h1>Analysis Failed</h1>
            <p><strong>Company:</strong> {company_name}</p>
            <p><strong>Error:</strong> {error}</p>
        </body>
        </html>
        """
    
    def _calculate_savings(self, num_companies: int) -> int:
        """Calculate percentage savings vs individual analysis"""
        individual_calls = num_companies  # 1 call per company
        batch_calls = 1  # 1 call total
        savings = ((individual_calls - batch_calls) / individual_calls) * 100
        return int(savings)
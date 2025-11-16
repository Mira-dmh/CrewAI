#!/usr/bin/env python3
"""
Single-agent runner that reads multi-agent search params
and generates comparable market trends analysis
"""

import argparse
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path for importing single.py
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))

from crewai import LLM
from dotenv import load_dotenv

# Import SingleAgentCrew from single.py in same directory
from single import SingleAgentCrew

# Load environment variables from project root
project_root = current_dir.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

class SingleAgentRunner:
    """Runner for single-agent market trends analysis"""
    
    def __init__(self):
        self.llm = LLM(model="gpt-4o-mini")
        
    def run_from_multi_agent_session(self, session_dir: str) -> dict:
        """
        Read multi-agent search params and run single-agent analysis
        
        Args:
            session_dir: Path to multi-agent session folder (e.g., src/outputs/linkedin/2d274566)
            
        Returns:
            Dictionary with single-agent results and execution metrics
        """
        session_path = Path(session_dir)
        params_file = session_path / "user_search_params.json"
        
        if not params_file.exists():
            raise FileNotFoundError(f"Cannot find {params_file}")
        
        # Read multi-agent search parameters
        with open(params_file, 'r') as f:
            params_data = json.load(f)
        
        search_params = params_data.get('search_parameters', {})
        job_title = search_params.get('job_title', '')
        location = search_params.get('location', 'United States')
        
        print("\n" + "="*70)
        print("SINGLE-AGENT MARKET TRENDS ANALYSIS")
        print("="*70)
        print(f"📂 Reading from session: {session_path.name}")
        print(f"💼 Job Title: {job_title}")
        print(f"📍 Location: {location}")
        print("="*70 + "\n")
        
        # Initialize crew
        crew = SingleAgentCrew(self.llm)
        
        # Track execution time
        start_time = time.time()
        
        try:
            # Execute single-agent search
            print("🤖 Starting single-agent analysis...")
            result = crew.kickoff(job_title=job_title, location=location)
            
            execution_time = time.time() - start_time
            
            # Parse output as market trends
            output_text = str(result)
            market_trends = self._parse_to_market_trends(output_text, job_title)
            
            # Prepare result object
            result_data = {
                'session_id': session_path.name,
                'job_title': job_title,
                'location': location,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat(),
                'market_trends': market_trends,
                'raw_output': output_text,
                'success': True
            }
            
            # Save single-agent market trends
            output_file = session_path / "market_trends_single_agent.json"
            with open(output_file, 'w') as f:
                json.dump(market_trends, f, indent=2)
            
            print(f"\n✅ Single-agent analysis complete!")
            print(f"⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"💾 Saved to: {output_file}")
            
            return result_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"\n❌ Error occurred: {e}")
            return {
                'session_id': session_path.name,
                'job_title': job_title,
                'location': location,
                'execution_time': execution_time,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'success': False
            }
    
    def _parse_to_market_trends(self, output: str, job_title: str) -> dict:
        """
        Parse single-agent output into market_trends.json compatible format
        """
        import re
        
        # Extract salary information
        salary_matches = re.findall(r'\$[\d,]+(?:k)?(?:\s*-\s*\$[\d,]+(?:k)?)?', output)
        avg_salary = salary_matches[0] if salary_matches else "$0"
        
        # Extract skills
        common_skills = [
            'Python', 'Java', 'JavaScript', 'SQL', 'Machine Learning',
            'Data Analysis', 'Communication', 'Leadership', 'Excel', 'Tableau'
        ]
        found_skills = [skill for skill in common_skills if skill.lower() in output.lower()]
        
        # Extract companies
        common_companies = [
            'Google', 'Amazon', 'Microsoft', 'Apple', 'Facebook', 'Meta',
            'Netflix', 'Tesla', 'IBM', 'Oracle'
        ]
        found_companies = [comp for comp in common_companies if comp.lower() in output.lower()]
        
        # Build market trends structure matching multi-agent format
        market_trends = {
            "market_overview": {
                "job_title": job_title,
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                "market_health": "moderate",
                "job_posting_trends": {
                    "growth_rate": "N/A",
                    "recent_postings": "Analysis based on available data",
                    "seasonal_patterns": "N/A"
                },
                "salary_data": {
                    "average_salary": avg_salary,
                    "salary_ranges": {
                        "entry_level": "N/A",
                        "mid_level": "N/A",
                        "senior_level": "N/A"
                    },
                    "factors_influencing_salary": [
                        "Experience level",
                        "Location",
                        "Industry sector"
                    ]
                },
                "skill_demand_analysis": {
                    "most_in_demand_skills": found_skills[:5] if found_skills else ["N/A"],
                    "skill_frequencies": {skill: "N/A" for skill in found_skills[:5]}
                },
                "hiring_patterns": {
                    "top_hiring_companies": found_companies[:5] if found_companies else ["N/A"],
                    "hiring_velocity": {
                        "average_time_to_hire": "N/A",
                        "common_hiring_channels": ["LinkedIn", "Company Websites"]
                    }
                },
                "geographic_distribution": {
                    "top_cities_for_jobs": ["N/A"],
                    "emerging_markets": ["Remote opportunities"]
                }
            }
        }
        
        return market_trends


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Run single-agent analysis from multi-agent session',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze from a specific multi-agent session
  python single-agent/cli_runner.py src/outputs/linkedin/2d274566
  
  # Or use session ID only (will look in src/outputs/linkedin/)
  python single-agent/cli_runner.py 2d274566
        """
    )
    
    parser.add_argument(
        'session',
        help='Multi-agent session directory or session ID (e.g., 2d274566 or src/outputs/linkedin/2d274566)'
    )
    
    args = parser.parse_args()
    
    # Normalize session path
    session_input = args.session
    if not session_input.startswith('src/outputs/linkedin'):
        # Assume it's just the session ID
        session_dir = f"src/outputs/linkedin/{session_input}"
    else:
        session_dir = session_input
    
    # Run single-agent analysis
    runner = SingleAgentRunner()
    result = runner.run_from_multi_agent_session(session_dir)
    
    if result['success']:
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nNext step: Run comparison analysis")
        print(f"Command: python single-agent/compare_results.py {session_dir}")
        print("="*70)
    else:
        print("\n❌ Analysis failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

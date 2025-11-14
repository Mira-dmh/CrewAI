#!/usr/bin/env python3
"""
Comparison analyzer for single-agent vs multi-agent market trends
Compares market_trends_single_agent.json with market_trends.json
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class MarketTrendsComparator:
    """Compare single-agent and multi-agent market trends outputs"""
    
    def __init__(self, session_dir: str):
        self.session_path = Path(session_dir)
        self.multi_agent_file = self.session_path / "market_trends.json"
        self.single_agent_file = self.session_path / "market_trends_single_agent.json"
        # Additional multi-agent files
        self.job_postings = {}
        self.verification = {}
        
    def load_data(self) -> tuple:
        """Load both market trends files and additional multi-agent outputs"""
        print(f"\n📂 Loading data from session: {self.session_path.name}\n")
        
        # Load job postings (multi-agent)
        job_postings_file = self.session_path / "job_postings.json"
        if job_postings_file.exists():
            with open(job_postings_file, 'r') as f:
                job_postings = json.load(f)
                print(f"✅ Loaded job_postings.json - Found {len(job_postings.get('jobs', []))} jobs")
        else:
            print(f"⚠️  job_postings.json not found")
            job_postings = {}
        
        # Load verification report (multi-agent)
        verification_file = self.session_path / "verification_report.json"
        if verification_file.exists():
            with open(verification_file, 'r') as f:
                verification = json.load(f)
                print(f"✅ Loaded verification_report.json - Confidence: {verification.get('overall_confidence', 'N/A')}")
        else:
            print(f"⚠️  verification_report.json not found")
            verification = {}
        
        # Load market trends (multi-agent)
        if not self.multi_agent_file.exists():
            raise FileNotFoundError(f"Multi-agent market trends not found: {self.multi_agent_file}")
        
        with open(self.multi_agent_file, 'r') as f:
            multi_data = json.load(f)
            print(f"✅ Loaded market_trends.json (multi-agent)")
        
        # Load market trends (single-agent)
        if not self.single_agent_file.exists():
            raise FileNotFoundError(f"Single-agent market trends not found: {self.single_agent_file}")
        
        with open(self.single_agent_file, 'r') as f:
            single_data = json.load(f)
            print(f"✅ Loaded market_trends_single_agent.json\n")
        
        # Store additional data for later use
        self.job_postings = job_postings
        self.verification = verification
        
        return single_data, multi_data
    
    def extract_comparable_metrics(self, data: Dict, agent_type: str) -> Dict:
        """Extract metrics from market trends data"""
        overview = data.get('market_overview', {})
        
        # Extract salary data
        salary_data = overview.get('salary_data', {})
        avg_salary = salary_data.get('average_salary', 'N/A')
        salary_ranges = salary_data.get('salary_ranges', {})
        
        # Extract skills
        skill_analysis = overview.get('skill_demand_analysis', {})
        skills = skill_analysis.get('most_in_demand_skills', [])
        skill_count = len([s for s in skills if s != 'N/A'])
        
        # Extract companies
        hiring_patterns = overview.get('hiring_patterns', {})
        companies = hiring_patterns.get('top_hiring_companies', [])
        company_count = len([c for c in companies if c != 'N/A'])
        
        # Extract growth rate
        job_trends = overview.get('job_posting_trends', {})
        growth_rate = job_trends.get('growth_rate', 'N/A')
        
        # Extract geographic data
        geo_dist = overview.get('geographic_distribution', {})
        cities = geo_dist.get('top_cities_for_data_science_jobs', geo_dist.get('top_cities_for_jobs', []))
        city_count = len([c for c in cities if c != 'N/A'])
        
        metrics = {
            'agent_type': agent_type,
            'avg_salary': avg_salary,
            'salary_range_entry': salary_ranges.get('entry_level', 'N/A'),
            'salary_range_mid': salary_ranges.get('mid_level', 'N/A'),
            'salary_range_senior': salary_ranges.get('senior_level', 'N/A'),
            'skills_identified': skill_count,
            'top_skills': skills[:5],
            'companies_identified': company_count,
            'top_companies': companies[:5],
            'growth_rate': growth_rate,
            'cities_identified': city_count,
            'top_cities': cities[:5],
            'market_health': overview.get('market_health', 'N/A')
        }
        
        return metrics
    
    def generate_comparison_table(self) -> str:
        """Generate formatted comparison table"""
        single_data, multi_data = self.load_data()
        
        single_metrics = self.extract_comparable_metrics(single_data, 'Single Agent')
        multi_metrics = self.extract_comparable_metrics(multi_data, 'Multi Agent')
        
        # Build comparison table
        table_lines = []
        table_lines.append("\n" + "="*100)
        table_lines.append("MARKET TRENDS COMPARISON: SINGLE-AGENT VS MULTI-AGENT")
        table_lines.append("="*100)
        
        # Header
        table_lines.append(f"\n{'Metric':<35} {'Single Agent':<30} {'Multi Agent':<30}")
        table_lines.append("-"*100)
        
        # Salary comparison
        table_lines.append(f"{'Average Salary':<35} {single_metrics['avg_salary']:<30} {multi_metrics['avg_salary']:<30}")
        table_lines.append(f"{'Entry Level Salary':<35} {single_metrics['salary_range_entry']:<30} {multi_metrics['salary_range_entry']:<30}")
        table_lines.append(f"{'Mid Level Salary':<35} {single_metrics['salary_range_mid']:<30} {multi_metrics['salary_range_mid']:<30}")
        table_lines.append(f"{'Senior Level Salary':<35} {single_metrics['salary_range_senior']:<30} {multi_metrics['salary_range_senior']:<30}")
        
        table_lines.append("-"*100)
        
        # Skills comparison
        table_lines.append(f"{'Skills Identified':<35} {single_metrics['skills_identified']:<30} {multi_metrics['skills_identified']:<30}")
        
        single_skills_str = ', '.join(single_metrics['top_skills'][:3]) if single_metrics['top_skills'] else 'None'
        multi_skills_str = ', '.join(multi_metrics['top_skills'][:3]) if multi_metrics['top_skills'] else 'None'
        table_lines.append(f"{'Top Skills (sample)':<35} {single_skills_str:<30} {multi_skills_str:<30}")
        
        table_lines.append("-"*100)
        
        # Companies comparison
        table_lines.append(f"{'Companies Identified':<35} {single_metrics['companies_identified']:<30} {multi_metrics['companies_identified']:<30}")
        
        single_comp_str = ', '.join(single_metrics['top_companies'][:3]) if single_metrics['top_companies'] else 'None'
        multi_comp_str = ', '.join(multi_metrics['top_companies'][:3]) if multi_metrics['top_companies'] else 'None'
        table_lines.append(f"{'Top Companies (sample)':<35} {single_comp_str:<30} {multi_comp_str:<30}")
        
        table_lines.append("-"*100)
        
        # Market insights
        table_lines.append(f"{'Growth Rate':<35} {single_metrics['growth_rate']:<30} {multi_metrics['growth_rate']:<30}")
        table_lines.append(f"{'Market Health':<35} {single_metrics['market_health']:<30} {multi_metrics['market_health']:<30}")
        table_lines.append(f"{'Cities Identified':<35} {single_metrics['cities_identified']:<30} {multi_metrics['cities_identified']:<30}")
        
        single_city_str = ', '.join(single_metrics['top_cities'][:2]) if single_metrics['top_cities'] else 'None'
        multi_city_str = ', '.join(multi_metrics['top_cities'][:2]) if multi_metrics['top_cities'] else 'None'
        table_lines.append(f"{'Top Cities (sample)':<35} {single_city_str:<30} {multi_city_str:<30}")
        
        table_lines.append("="*100)
        
        # Add multi-agent specific data
        table_lines.append("\n📋 MULTI-AGENT EXCLUSIVE DATA")
        table_lines.append("-"*100)
        
        # Job postings count
        job_count = len(self.job_postings.get('jobs', []))
        table_lines.append(f"{'Jobs Scraped from LinkedIn':<35} {'N/A (not applicable)':<30} {job_count:<30}")
        
        # Verification confidence
        if self.verification:
            confidence = self.verification.get('overall_confidence', 'N/A')
            table_lines.append(f"{'Verification Confidence Score':<35} {'N/A (not applicable)':<30} {confidence:<30}")
            
            flagged = len(self.verification.get('flagged_issues', []))
            table_lines.append(f"{'Flagged Issues':<35} {'N/A (not applicable)':<30} {flagged:<30}")
        
        table_lines.append("="*100)
        
        # Summary analysis
        table_lines.append("\n📊 ANALYSIS SUMMARY")
        table_lines.append("-"*100)
        
        # Calculate completeness scores
        single_completeness = self._calculate_completeness(single_metrics)
        multi_completeness = self._calculate_completeness(multi_metrics)
        
        table_lines.append(f"Data Completeness:     Single: {single_completeness:.1f}%  |  Multi: {multi_completeness:.1f}%")
        
        if multi_completeness > single_completeness:
            improvement = multi_completeness - single_completeness
            table_lines.append(f"✅ Multi-agent provides {improvement:.1f}% more complete data")
        elif single_completeness > multi_completeness:
            improvement = single_completeness - multi_completeness
            table_lines.append(f"⚠️  Single-agent provides {improvement:.1f}% more complete data")
        else:
            table_lines.append(f"➖ Both agents provide equal data completeness")
        
        # Skill comparison
        if multi_metrics['skills_identified'] > single_metrics['skills_identified']:
            diff = multi_metrics['skills_identified'] - single_metrics['skills_identified']
            table_lines.append(f"✅ Multi-agent identified {diff} more skills")
        elif single_metrics['skills_identified'] > multi_metrics['skills_identified']:
            diff = single_metrics['skills_identified'] - multi_metrics['skills_identified']
            table_lines.append(f"⚠️  Single-agent identified {diff} more skills")
        
        # Company comparison
        if multi_metrics['companies_identified'] > single_metrics['companies_identified']:
            diff = multi_metrics['companies_identified'] - single_metrics['companies_identified']
            table_lines.append(f"✅ Multi-agent identified {diff} more companies")
        elif single_metrics['companies_identified'] > multi_metrics['companies_identified']:
            diff = single_metrics['companies_identified'] - multi_metrics['companies_identified']
            table_lines.append(f"⚠️  Single-agent identified {diff} more companies")
        
        table_lines.append("="*100 + "\n")
        
        return '\n'.join(table_lines)
    
    def _calculate_completeness(self, metrics: Dict) -> float:
        """Calculate data completeness score (0-100%)"""
        total_fields = 0
        filled_fields = 0
        
        # Check each field
        fields_to_check = [
            'avg_salary', 'salary_range_entry', 'salary_range_mid', 'salary_range_senior',
            'growth_rate', 'market_health'
        ]
        
        for field in fields_to_check:
            total_fields += 1
            if metrics.get(field) and metrics[field] != 'N/A':
                filled_fields += 1
        
        # Count skills, companies, cities
        total_fields += 3
        if metrics['skills_identified'] > 0:
            filled_fields += 1
        if metrics['companies_identified'] > 0:
            filled_fields += 1
        if metrics['cities_identified'] > 0:
            filled_fields += 1
        
        return (filled_fields / total_fields) * 100 if total_fields > 0 else 0
    
    def save_comparison_report(self):
        """Save comparison to JSON file"""
        single_data, multi_data = self.load_data()
        
        single_metrics = self.extract_comparable_metrics(single_data, 'Single Agent')
        multi_metrics = self.extract_comparable_metrics(multi_data, 'Multi Agent')
        
        report = {
            'session_id': self.session_path.name,
            'comparison_date': datetime.now().isoformat(),
            'single_agent': single_metrics,
            'multi_agent': multi_metrics,
            'completeness_scores': {
                'single_agent': self._calculate_completeness(single_metrics),
                'multi_agent': self._calculate_completeness(multi_metrics)
            }
        }
        
        output_file = self.session_path / "comparison_report.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Comparison report saved to: {output_file}\n")
        return output_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Compare single-agent and multi-agent market trends analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare results from a session
  python single-agent/compare_results.py src/outputs/linkedin/2d274566
  
  # Or use session ID only
  python single-agent/compare_results.py 2d274566
        """
    )
    
    parser.add_argument(
        'session',
        help='Session directory or session ID (e.g., 2d274566 or src/outputs/linkedin/2d274566)'
    )
    
    args = parser.parse_args()
    
    # Normalize session path
    session_input = args.session
    if not session_input.startswith('src/outputs/linkedin'):
        session_dir = f"src/outputs/linkedin/{session_input}"
    else:
        session_dir = session_input
    
    # Run comparison
    try:
        comparator = MarketTrendsComparator(session_dir)
        
        # Generate and print comparison table
        table = comparator.generate_comparison_table()
        print(table)
        
        # Save report
        comparator.save_comparison_report()
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have run the single-agent analysis first:")
        print(f"  python single-agent/cli_runner.py {session_dir}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

"""
Job Fit Ranking - Example Usage Script
Demonstrates the ranking algorithm with real job search data
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from job_ranker import JobFitRanker, ResumeJobMatcher
import json
from datetime import datetime


def example_1_basic_ranking():
    """Example 1: Basic job ranking with default settings"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Job Ranking")
    print("=" * 80)
    
    # Initialize matcher with resume
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6  # Balanced approach
    )
    
    # Rank jobs from LinkedIn search results
    ranked_jobs = matcher.rank_jobs_from_json(
        json_path="src/outputs/linkedin/job_postings.json",
        top_k=5
    )
    
    # Display results
    print(f"\n📊 Top 5 Job Matches (out of {len(ranked_jobs)} total):\n")
    
    for i, job in enumerate(ranked_jobs, 1):
        print(f"{i}. {job['job_title']}")
        print(f"   Company: {job.get('company_name', 'Not specified')}")
        print(f"   Location: {job.get('location', 'Not specified')}")
        print(f"   🎯 Fit Score: {job['fit_percentage']} ({job['fit_score']:.4f})")
        print(f"   Level: {job.get('experience_level', 'Not specified')}")
        print()


def example_2_detailed_analysis():
    """Example 2: Detailed fit analysis for a specific job"""
    print("=" * 80)
    print("EXAMPLE 2: Detailed Job Fit Analysis")
    print("=" * 80)
    
    # Initialize matcher with critical keywords
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.65,
        critical_keywords=["Python", "Machine Learning", "Data Analysis", "SQL", "AWS"]
    )
    
    # Load a specific job
    with open("src/outputs/linkedin/job_postings.json", 'r') as f:
        data = json.load(f)
        jobs = data.get('job_postings', [])
    
    if jobs:
        target_job = jobs[0]  # Analyze first job
        
        print(f"\n🎯 Analyzing: {target_job['job_title']}\n")
        
        # Get detailed analysis
        analysis = matcher.analyze_specific_job(target_job)
        
        # Display score breakdown
        print("📊 Score Breakdown:")
        breakdown = analysis['score_breakdown']
        print(f"   • Final Score: {breakdown['final_score']:.4f} ({breakdown['final_score']*100:.1f}%)")
        print(f"   • Embedding Similarity: {breakdown['embedding_similarity']:.4f}")
        print(f"   • Keyword Relevance: {breakdown['keyword_relevance']:.4f}")
        print(f"   • Keyword Boost: {breakdown['keyword_boost']:.4f}")
        print(f"   • Alpha (weight): {breakdown['alpha']:.2f}")
        
        # Display assessment
        print(f"\n✅ Assessment: {analysis['overall_assessment']}")
        
        # Display matched skills
        if analysis['matched_critical_skills']:
            print(f"\n💪 Matched Critical Skills:")
            for skill in analysis['matched_critical_skills']:
                print(f"   ✓ {skill}")
        
        # Display missing skills
        if analysis['missing_critical_skills']:
            print(f"\n⚠️  Missing Critical Skills:")
            for skill in analysis['missing_critical_skills']:
                print(f"   ✗ {skill}")
        
        # Display recommendations
        print(f"\n💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"   • {rec}")
        
        # Display keyword matches
        if analysis['matching_keywords']:
            print(f"\n🔑 Top Matching Keywords:")
            print(f"   {', '.join(analysis['matching_keywords'][:5])}")


def example_3_compare_configurations():
    """Example 3: Compare different alpha configurations"""
    print("=" * 80)
    print("EXAMPLE 3: Comparing Different Alpha Configurations")
    print("=" * 80)
    
    # Load resume
    with open("data/user_resume.txt", 'r') as f:
        resume_text = f.read()
    
    # Load jobs
    with open("src/outputs/linkedin/job_postings.json", 'r') as f:
        data = json.load(f)
        jobs = data.get('job_postings', [])
    
    if not jobs:
        print("No jobs available for comparison")
        return
    
    target_job = jobs[0]
    
    # Test different alpha values
    alphas = [0.3, 0.5, 0.7, 0.9]
    
    print(f"\n🎯 Job: {target_job['job_title']}\n")
    print(f"{'Alpha':<10} {'Emphasis':<20} {'Score':<10} {'Fit %':<10}")
    print("-" * 50)
    
    for alpha in alphas:
        ranker = JobFitRanker(alpha=alpha)
        
        job_desc = ranker._build_job_description(target_job)
        score = ranker.compute_job_fit_score(resume_text, job_desc)
        
        if alpha < 0.4:
            emphasis = "Keyword-Heavy"
        elif alpha < 0.6:
            emphasis = "Balanced"
        elif alpha < 0.8:
            emphasis = "Semantic-Heavy"
        else:
            emphasis = "Very Semantic"
        
        print(f"{alpha:<10} {emphasis:<20} {score:.4f}   {score*100:.1f}%")
    
    print("\n💡 Interpretation:")
    print("   • Lower alpha (0.3-0.4): Prioritizes exact keyword matches")
    print("   • Medium alpha (0.5-0.6): Balanced approach (recommended)")
    print("   • Higher alpha (0.7-0.9): Focuses on semantic/conceptual similarity")


def example_4_batch_processing():
    """Example 4: Process multiple job postings efficiently"""
    print("=" * 80)
    print("EXAMPLE 4: Batch Processing with Custom Keywords")
    print("=" * 80)
    
    # Define user profile
    critical_skills = [
        "Python", "R", "SQL",
        "Machine Learning", "Data Analysis", "Data Visualization",
        "Git", "AWS", "Streamlit"
    ]
    
    print(f"\n👤 User Profile - Critical Skills:")
    print(f"   {', '.join(critical_skills)}")
    
    # Initialize matcher
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6,
        critical_keywords=critical_skills
    )
    
    # Rank all jobs
    all_ranked = matcher.rank_jobs_from_json(
        json_path="src/outputs/linkedin/job_postings.json",
        top_k=None  # Get all jobs
    )
    
    # Categorize by fit level
    excellent = [j for j in all_ranked if j['fit_score'] >= 0.8]
    good = [j for j in all_ranked if 0.65 <= j['fit_score'] < 0.8]
    moderate = [j for j in all_ranked if 0.5 <= j['fit_score'] < 0.65]
    weak = [j for j in all_ranked if j['fit_score'] < 0.5]
    
    print(f"\n📊 Job Distribution by Fit Level:")
    print(f"   🟢 Excellent (≥80%):  {len(excellent)} jobs")
    print(f"   🟡 Good (65-79%):     {len(good)} jobs")
    print(f"   🟠 Moderate (50-64%): {len(moderate)} jobs")
    print(f"   🔴 Weak (<50%):       {len(weak)} jobs")
    
    # Show top matches in each category
    if excellent:
        print(f"\n🟢 Excellent Matches:")
        for job in excellent[:3]:
            print(f"   • {job['job_title']} - {job['fit_percentage']}")
    
    if good:
        print(f"\n🟡 Good Matches:")
        for job in good[:3]:
            print(f"   • {job['job_title']} - {job['fit_percentage']}")


def example_5_save_results():
    """Example 5: Save ranked results to JSON file"""
    print("=" * 80)
    print("EXAMPLE 5: Saving Ranked Results")
    print("=" * 80)
    
    # Initialize matcher
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6,
        critical_keywords=["Python", "Data Science", "Machine Learning"]
    )
    
    # Rank jobs
    ranked_jobs = matcher.rank_jobs_from_json(
        json_path="src/outputs/linkedin/job_postings.json",
        top_k=10
    )
    
    # Prepare output
    output = {
        "ranking_metadata": {
            "timestamp": datetime.now().isoformat(),
            "algorithm": "Hybrid Semantic + Keyword Ranking",
            "alpha": 0.6,
            "critical_keywords": ["Python", "Data Science", "Machine Learning"],
            "total_jobs_ranked": len(ranked_jobs)
        },
        "ranked_jobs": ranked_jobs
    }
    
    # Save to file
    output_path = "src/outputs/linkedin/ranked_job_results.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_path}")
    print(f"   Total jobs ranked: {len(ranked_jobs)}")
    print(f"\n📋 Top 3 Matches:")
    for i, job in enumerate(ranked_jobs[:3], 1):
        print(f"   {i}. {job['job_title']} - {job['fit_percentage']}")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("🎯 JOB FIT RANKING ALGORITHM - DEMONSTRATION")
    print("=" * 80)
    print("\nThis script demonstrates various features of the job fit ranking system.")
    print("It combines embedding-based semantic similarity with keyword relevance.")
    print()
    
    # Check if required files exist
    if not os.path.exists("data/user_resume.txt"):
        print("❌ Error: data/user_resume.txt not found")
        return
    
    if not os.path.exists("src/outputs/linkedin/job_postings.json"):
        print("❌ Error: src/outputs/linkedin/job_postings.json not found")
        print("   Please run a LinkedIn job search first")
        return
    
    try:
        # Run examples
        example_1_basic_ranking()
        input("\nPress Enter to continue to next example...")
        
        example_2_detailed_analysis()
        input("\nPress Enter to continue to next example...")
        
        example_3_compare_configurations()
        input("\nPress Enter to continue to next example...")
        
        example_4_batch_processing()
        input("\nPress Enter to continue to next example...")
        
        example_5_save_results()
        
        print("\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

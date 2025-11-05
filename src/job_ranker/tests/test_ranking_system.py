"""
Quick test script for job fit ranking system
Run this to verify the installation and basic functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required = {
        'openai': 'OpenAI API client',
        'sklearn': 'Scikit-learn for TF-IDF',
        'numpy': 'Numerical computations'
    }
    
    missing = []
    for package, description in required.items():
        try:
            __import__(package)
            print(f"  ✅ {package}: {description}")
        except ImportError:
            print(f"  ❌ {package}: {description} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"   Install with: pip install {' '.join(missing)}")
        return False
    
    print("✅ All dependencies installed!\n")
    return True


def check_environment():
    """Check if environment variables are set"""
    print("🔍 Checking environment...")
    
    if os.getenv('OPENAI_API_KEY'):
        print("  ✅ OPENAI_API_KEY is set")
        return True
    else:
        print("  ❌ OPENAI_API_KEY not found")
        print("     Set it in your .env file or environment")
        return False


def check_files():
    """Check if required files exist"""
    print("\n🔍 Checking required files...")
    
    required_files = {
        'data/user_resume.txt': 'Resume file',
        'src/job_ranker/job_fit_ranker.py': 'Ranking module',
        'src/job_ranker/ranking_integration.py': 'Integration utilities'
    }
    
    missing = []
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"  ✅ {file}: {description}")
        else:
            print(f"  ❌ {file}: {description} - NOT FOUND")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {len(missing)}")
        return False
    
    print("✅ All required files present!\n")
    return True


def test_basic_functionality():
    """Test basic ranking functionality"""
    print("🔍 Testing basic functionality...")
    
    try:
        from job_ranker import JobFitRanker, ResumeJobMatcher
        print("  ✅ Successfully imported JobFitRanker")
        print("  ✅ Successfully imported ResumeJobMatcher")
        
        # Test initialization
        ranker = JobFitRanker(alpha=0.6)
        print("  ✅ JobFitRanker initialized")
        
        # Test with sample data
        sample_resume = "Python developer with experience in machine learning and data analysis"
        sample_job = "Looking for Python developer skilled in ML and data science"
        
        score = ranker.compute_job_fit_score(sample_resume, sample_job)
        print(f"  ✅ Computed sample fit score: {score:.4f}")
        
        if 0 <= score <= 1:
            print("  ✅ Score is in valid range [0, 1]")
        else:
            print(f"  ⚠️  Score {score} is outside expected range")
        
        print("\n✅ Basic functionality working!\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing functionality: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_actual_data():
    """Test with actual resume and job data if available"""
    print("🔍 Testing with actual data...")
    
    if not os.path.exists("data/user_resume.txt"):
        print("  ⚠️  Resume file not found, skipping")
        return True
    
    if not os.path.exists("src/outputs/linkedin/job_postings.json"):
        print("  ⚠️  Job postings not found, skipping")
        print("     Run a LinkedIn search first to generate job data")
        return True
    
    try:
        from job_ranker import ResumeJobMatcher
        
        # Initialize matcher
        matcher = ResumeJobMatcher(
            resume_path="data/user_resume.txt",
            alpha=0.6,
            critical_keywords=["Python", "Machine Learning"]
        )
        print("  ✅ Matcher initialized with resume")
        
        # Rank jobs
        ranked_jobs = matcher.rank_jobs_from_json(
            json_path="src/outputs/linkedin/job_postings.json",
            top_k=3
        )
        print(f"  ✅ Ranked {len(ranked_jobs)} jobs")
        
        # Validate results
        if ranked_jobs:
            top_job = ranked_jobs[0]
            print(f"\n  📊 Top Match:")
            print(f"     Job: {top_job['job_title']}")
            print(f"     Fit: {top_job['fit_percentage']}")
            print(f"     Score: {top_job['fit_score']:.4f}")
            
            # Check sorting
            scores = [j['fit_score'] for j in ranked_jobs]
            if scores == sorted(scores, reverse=True):
                print("  ✅ Jobs correctly sorted by score")
            else:
                print("  ⚠️  Job sorting may be incorrect")
            
            print("\n✅ Actual data test passed!\n")
            return True
        else:
            print("  ⚠️  No jobs returned")
            return False
        
    except Exception as e:
        print(f"\n❌ Error testing with actual data: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 JOB FIT RANKING SYSTEM - VERIFICATION TEST")
    print("=" * 70)
    print()
    
    results = {
        "Dependencies": check_dependencies(),
        "Environment": check_environment(),
        "Files": check_files(),
        "Basic Functionality": test_basic_functionality(),
        "Actual Data": test_with_actual_data()
    }
    
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {test_name}")
    
    print()
    
    if all(results.values()):
        print("🎉 All tests passed! The ranking system is ready to use.")
        print()
        print("Next steps:")
        print("  1. Run: python examples/job_ranking_demo.py")
        print("  2. Check: docs/JOB_RANKING_README.md")
        print("  3. Integrate: docs/INTEGRATION_GUIDE.md")
    else:
        failed = [name for name, passed in results.items() if not passed]
        print(f"⚠️  Some tests failed: {', '.join(failed)}")
        print()
        print("Please fix the issues above before using the ranking system.")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

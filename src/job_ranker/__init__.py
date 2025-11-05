"""
Job Fit Ranking System

A sophisticated hybrid ranking algorithm that assesses job-resume fit by combining
embedding-based semantic similarity with keyword relevance weighting.

Main Components:
- JobFitRanker: Core ranking algorithm
- ResumeJobMatcher: High-level wrapper for easy use
- Streamlit integration utilities

Usage:
    from job_ranker import JobFitRanker, ResumeJobMatcher
    
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6
    )
    
    ranked_jobs = matcher.rank_jobs_from_json("jobs.json", top_k=10)
"""

from .job_fit_ranker import JobFitRanker, ResumeJobMatcher

__all__ = ['JobFitRanker', 'ResumeJobMatcher']
__version__ = '1.0.0'

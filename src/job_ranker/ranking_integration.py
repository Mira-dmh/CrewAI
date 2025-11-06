"""
Integration utilities for job fit ranking system
Helper functions for Streamlit integration and data processing
"""

import streamlit as st
from typing import List, Dict, Optional
import pandas as pd
from .job_fit_ranker import JobFitRanker, ResumeJobMatcher


def display_ranked_jobs_streamlit(
    ranked_jobs: List[Dict],
    show_scores: bool = True,
    show_details: bool = True
):
    """
    Display ranked jobs in Streamlit with nice formatting.
    
    Args:
        ranked_jobs: List of ranked job dicts
        show_scores: Whether to show fit scores
        show_details: Whether to show expandable details
    """
    st.markdown(f"### 🎯 Found {len(ranked_jobs)} Job Matches")
    
    for i, job in enumerate(ranked_jobs, 1):
        # Color code by fit score
        score = job.get('fit_score', 0)
        if score >= 0.8:
            emoji = "🟢"
            color = "green"
        elif score >= 0.65:
            emoji = "🟡"
            color = "orange"
        elif score >= 0.5:
            emoji = "🟠"
            color = "orange"
        else:
            emoji = "🔴"
            color = "red"
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"#### {i}. {emoji} {job['job_title']}")
                st.markdown(f"**Company:** {job.get('company_name', 'Not specified')}")
                st.markdown(f"**Location:** {job.get('location', 'Not specified')}")
            
            with col2:
                if show_scores:
                    st.metric("Fit Score", job['fit_percentage'])
                
                if job.get('job_url'):
                    st.link_button("🔗 View Job", job['job_url'], use_container_width=True)
            
            if show_details:
                with st.expander("View Details"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Type:** {job.get('employment_type', 'Not specified')}")
                        st.markdown(f"**Experience:** {job.get('experience_level', 'Not specified')}")
                    with col_b:
                        st.markdown(f"**Posted:** {job.get('date_posted', 'Not specified')}")
                        if show_scores:
                            st.markdown(f"**Raw Score:** {job.get('fit_score', 0):.4f}")
            
            st.divider()


def display_fit_analysis_streamlit(analysis: Dict):
    """
    Display detailed fit analysis in Streamlit.
    
    Args:
        analysis: Analysis dict from analyze_fit_breakdown
    """
    # Score breakdown
    st.markdown("### 📊 Fit Score Breakdown")
    
    breakdown = analysis['score_breakdown']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Final Score", f"{breakdown['final_score']*100:.1f}%")
    with col2:
        st.metric("Semantic", f"{breakdown['embedding_similarity']:.3f}")
    with col3:
        st.metric("Keywords", f"{breakdown['keyword_relevance']:.3f}")
    with col4:
        st.metric("Boost", f"{breakdown['keyword_boost']:.3f}")
    
    # Overall assessment
    st.markdown(f"### ✅ {analysis['overall_assessment']}")
    
    # Skills comparison
    col_skills1, col_skills2 = st.columns(2)
    
    with col_skills1:
        st.markdown("#### 💪 Matched Critical Skills")
        if analysis['matched_critical_skills']:
            for skill in analysis['matched_critical_skills']:
                st.markdown(f"✓ {skill}")
        else:
            st.info("No critical skills matched")
    
    with col_skills2:
        st.markdown("#### ⚠️ Missing Critical Skills")
        if analysis['missing_critical_skills']:
            for skill in analysis['missing_critical_skills']:
                st.markdown(f"✗ {skill}")
        else:
            st.success("All critical skills matched!")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    for rec in analysis['recommendations']:
        st.info(rec)
    
    # Keyword details
    with st.expander("🔑 Keyword Analysis Details"):
        col_kw1, col_kw2 = st.columns(2)
        
        with col_kw1:
            st.markdown("**Matching Keywords:**")
            if analysis['matching_keywords']:
                st.markdown(", ".join(analysis['matching_keywords'][:10]))
            else:
                st.info("No common keywords found")
        
        with col_kw2:
            st.markdown("**Missing Keywords:**")
            if analysis['missing_keywords']:
                st.markdown(", ".join(analysis['missing_keywords'][:10]))
            else:
                st.success("All keywords covered!")


def create_ranking_dataframe(ranked_jobs: List[Dict]) -> pd.DataFrame:
    """
    Convert ranked jobs to pandas DataFrame for analysis.
    
    Args:
        ranked_jobs: List of ranked job dicts
        
    Returns:
        DataFrame with job data
    """
    df_data = []
    
    for job in ranked_jobs:
        df_data.append({
            'Job Title': job.get('job_title', 'N/A'),
            'Company': job.get('company_name', 'N/A'),
            'Location': job.get('location', 'N/A'),
            'Fit Score': job.get('fit_score', 0),
            'Fit %': job.get('fit_percentage', 'N/A'),
            'Experience Level': job.get('experience_level', 'N/A'),
            'Employment Type': job.get('employment_type', 'N/A'),
            'Job URL': job.get('job_url', 'N/A')
        })
    
    return pd.DataFrame(df_data)


def add_ranking_to_streamlit_page():
    """
    Add job ranking feature to existing Streamlit page.
    
    Usage:
        # In your Streamlit page:
        from utils.ranking_integration import add_ranking_to_streamlit_page
        add_ranking_to_streamlit_page()
    """
    st.markdown("---")
    st.markdown("## 🎯 Job Fit Ranking")
    st.markdown("*Rank jobs by fit using AI-powered semantic + keyword analysis*")
    
    # Configuration
    with st.expander("⚙️ Ranking Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            alpha = st.slider(
                "Semantic vs Keyword Weight (α)",
                min_value=0.0,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Higher = more semantic, Lower = more keyword-focused"
            )
        
        with col2:
            top_k = st.number_input(
                "Number of Top Jobs",
                min_value=1,
                max_value=50,
                value=10,
                step=1
            )
        
        critical_keywords = st.text_input(
            "Critical Keywords (comma-separated)",
            placeholder="Python, Machine Learning, AWS",
            help="Skills that must be present for bonus scoring"
        )
        
        keywords_list = [kw.strip() for kw in critical_keywords.split(",")] if critical_keywords else []
    
    # Rank button
    if st.button("🚀 Rank Jobs by Fit", type="primary", use_container_width=True):
        try:
            with st.spinner("Analyzing job fit scores..."):
                # Initialize matcher
                matcher = ResumeJobMatcher(
                    resume_path="data/user_resume.txt",
                    alpha=alpha,
                    critical_keywords=keywords_list
                )
                
                # Rank jobs
                ranked_jobs = matcher.rank_jobs_from_json(
                    json_path="src/outputs/linkedin/job_postings.json",
                    top_k=top_k
                )
                
                # Display results
                st.success(f"✅ Ranked {len(ranked_jobs)} jobs by fit score!")
                
                # Show distribution
                scores = [j['fit_score'] for j in ranked_jobs]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    st.metric("Average Fit", f"{avg_score*100:.1f}%")
                with col_stats2:
                    st.metric("Best Match", f"{max(scores)*100:.1f}%" if scores else "N/A")
                with col_stats3:
                    st.metric("Matches >70%", sum(1 for s in scores if s >= 0.7))
                
                # Display jobs
                st.markdown("---")
                display_ranked_jobs_streamlit(ranked_jobs)
                
                # Download option
                df = create_ranking_dataframe(ranked_jobs)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Results (CSV)",
                    csv,
                    "ranked_jobs.csv",
                    "text/csv",
                    use_container_width=True
                )
                
        except FileNotFoundError as e:
            st.error(f"❌ File not found: {e}")
            st.info("Please make sure you have run a job search first")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            import traceback
            with st.expander("View Error Details"):
                st.code(traceback.format_exc())


def get_ranking_widget(
    resume_path: str,
    jobs_json_path: str,
    alpha: float = 0.6,
    critical_keywords: Optional[List[str]] = None
) -> List[Dict]:
    """
    Simple function to get ranked jobs programmatically.
    
    Args:
        resume_path: Path to resume file
        jobs_json_path: Path to job postings JSON
        alpha: Semantic vs keyword weight
        critical_keywords: List of critical skills
        
    Returns:
        List of ranked jobs
    """
    matcher = ResumeJobMatcher(
        resume_path=resume_path,
        alpha=alpha,
        critical_keywords=critical_keywords
    )
    
    return matcher.rank_jobs_from_json(jobs_json_path, top_k=None)

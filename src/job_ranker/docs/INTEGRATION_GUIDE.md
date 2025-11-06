# Job Fit Ranking System - Quick Integration Guide

## 🎯 Adding Ranking to Specific Jobs Page

### Option 1: Quick Integration (Recommended)

Add this to your `src/streamlit_pages/specific_jobs.py`:

```python
# At the top of the file
from job_ranker.ranking_integration import add_ranking_to_streamlit_page

# After job search results are displayed
if search_success and os.path.exists("src/outputs/linkedin/job_postings.json"):
    add_ranking_to_streamlit_page()
```

This adds a complete ranking section with:
- Configurable alpha parameter
- Critical keywords input
- Top K selection
- Score visualization
- CSV download

### Option 2: Custom Integration

For more control over the UI:

```python
from job_ranker import ResumeJobMatcher
from job_ranker.ranking_integration import display_ranked_jobs_streamlit

# In your job search tab, after results are loaded
if st.button("🎯 Rank Jobs by Fit"):
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6,
        critical_keywords=["Python", "Machine Learning", "Data Science"]
    )
    
    ranked_jobs = matcher.rank_jobs_from_json(
        json_path="src/outputs/linkedin/job_postings.json",
        top_k=10
    )
    
    display_ranked_jobs_streamlit(ranked_jobs)
```

### Option 3: Replace Existing Display

Instead of showing jobs in order scraped, show by fit score:

```python
# Instead of:
# for job in job_postings:
#     display_job(job)

# Do this:
matcher = ResumeJobMatcher(resume_path="data/user_resume.txt", alpha=0.6)
ranked_jobs = matcher.rank_jobs_from_json("src/outputs/linkedin/job_postings.json")

for job in ranked_jobs:
    # Show fit score badge
    st.metric("Fit Score", job['fit_percentage'])
    display_job(job)
```

## 🔧 Configuration Examples

### For Recent Graduates

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.65,  # Slightly more semantic to capture potential
    critical_keywords=["Python", "SQL", "Data Analysis", "Git"]
)
```

### For Experienced Professionals

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.55,  # More keyword focus for specific expertise
    critical_keywords=["Leadership", "Architecture", "Kubernetes", "AWS"]
)
```

### For Career Changers

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.75,  # High semantic weight for transferable skills
    critical_keywords=[]  # Don't penalize for missing specific tools
)
```

## 📊 Adding Analytics

Show ranking statistics:

```python
ranked_jobs = matcher.rank_jobs_from_json("jobs.json")

# Calculate stats
scores = [j['fit_score'] for j in ranked_jobs]
avg_score = sum(scores) / len(scores)
top_score = max(scores)
num_excellent = sum(1 for s in scores if s >= 0.8)
num_good = sum(1 for s in scores if 0.65 <= s < 0.8)

# Display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Fit", f"{avg_score*100:.1f}%")
col2.metric("Best Match", f"{top_score*100:.1f}%")
col3.metric("Excellent", num_excellent)
col4.metric("Good", num_good)
```

## 🎨 UI Enhancements

### Color-coded Badges

```python
def get_fit_badge(score):
    if score >= 0.8:
        return "🟢 Excellent Match"
    elif score >= 0.65:
        return "🟡 Good Match"
    elif score >= 0.5:
        return "🟠 Moderate Match"
    else:
        return "🔴 Weak Match"

for job in ranked_jobs:
    st.markdown(f"### {job['job_title']} - {get_fit_badge(job['fit_score'])}")
```

### Interactive Filtering

```python
min_score = st.slider("Minimum Fit Score", 0.0, 1.0, 0.5, 0.05)
filtered_jobs = [j for j in ranked_jobs if j['fit_score'] >= min_score]

st.write(f"Showing {len(filtered_jobs)} jobs with fit ≥ {min_score*100:.0f}%")
display_ranked_jobs_streamlit(filtered_jobs)
```

### Comparison View

```python
if len(ranked_jobs) >= 2:
    st.markdown("### 🔍 Compare Top Matches")
    
    job1 = ranked_jobs[0]
    job2 = ranked_jobs[1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**#{1}: {job1['job_title']}**")
        st.metric("Fit Score", job1['fit_percentage'])
        analysis1 = matcher.analyze_specific_job(job1)
        st.write(f"Matched Skills: {len(analysis1['matched_critical_skills'])}")
    
    with col2:
        st.markdown(f"**#{2}: {job2['job_title']}**")
        st.metric("Fit Score", job2['fit_percentage'])
        analysis2 = matcher.analyze_specific_job(job2)
        st.write(f"Matched Skills: {len(analysis2['matched_critical_skills'])}")
```

## 🚀 Performance Tips

### Cache the Matcher

```python
@st.cache_resource
def get_matcher(alpha, keywords):
    return ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=alpha,
        critical_keywords=keywords
    )

# Use cached matcher
matcher = get_matcher(alpha=0.6, keywords=tuple(["Python", "SQL"]))
```

### Progressive Loading

```python
# Show quick preview first
with st.spinner("Analyzing top 5 jobs..."):
    top_5 = matcher.rank_jobs_from_json("jobs.json", top_k=5)
    display_ranked_jobs_streamlit(top_5)

# Then load the rest
if st.button("Load All Matches"):
    with st.spinner("Analyzing all jobs..."):
        all_jobs = matcher.rank_jobs_from_json("jobs.json", top_k=None)
        display_ranked_jobs_streamlit(all_jobs[5:])
```

## 📝 Complete Integration Example

Here's a full section you can add to `specific_jobs.py`:

```python
from job_ranker import ResumeJobMatcher
from job_ranker.ranking_integration import display_ranked_jobs_streamlit, create_ranking_dataframe

def display_ranked_results_section():
    """Display ranked job results with full analysis"""
    st.markdown("---")
    st.markdown("## 🎯 AI-Powered Job Fit Ranking")
    st.info("Ranks jobs using hybrid semantic + keyword matching")
    
    # Configuration
    with st.expander("⚙️ Configure Ranking Algorithm", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            alpha = st.slider(
                "Semantic Weight (α)",
                0.0, 1.0, 0.6, 0.05,
                help="Higher = more semantic, Lower = more keyword-focused"
            )
            
            top_k = st.number_input("Show Top", 1, 50, 10, 1)
        
        with col2:
            keywords_input = st.text_area(
                "Critical Skills (one per line)",
                "Python\nMachine Learning\nSQL\nAWS",
                height=100
            )
            
            keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
    
    # Rank button
    if st.button("🚀 Rank Jobs", type="primary", use_container_width=True):
        try:
            with st.spinner("Computing fit scores..."):
                matcher = ResumeJobMatcher(
                    resume_path="data/user_resume.txt",
                    alpha=alpha,
                    critical_keywords=keywords
                )
                
                ranked_jobs = matcher.rank_jobs_from_json(
                    json_path="src/outputs/linkedin/job_postings.json",
                    top_k=top_k
                )
                
                # Stats
                scores = [j['fit_score'] for j in ranked_jobs]
                avg_score = sum(scores) / len(scores)
                
                col_stats = st.columns(4)
                col_stats[0].metric("Total Jobs", len(ranked_jobs))
                col_stats[1].metric("Avg Fit", f"{avg_score*100:.1f}%")
                col_stats[2].metric("Best", f"{max(scores)*100:.1f}%")
                col_stats[3].metric("≥70%", sum(1 for s in scores if s >= 0.7))
                
                # Display jobs
                st.markdown("---")
                display_ranked_jobs_streamlit(ranked_jobs, show_scores=True, show_details=True)
                
                # Export
                df = create_ranking_dataframe(ranked_jobs)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Rankings (CSV)",
                    csv,
                    "ranked_jobs.csv",
                    "text/csv",
                    use_container_width=True
                )
                
        except FileNotFoundError:
            st.error("❌ No job search results found. Please run a search first.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Add to your page after search results
if os.path.exists("src/outputs/linkedin/job_postings.json"):
    display_ranked_results_section()
```

## 🧪 Testing

Test the integration:

```python
# Test with sample data
def test_ranking():
    from job_ranker import ResumeJobMatcher
    
    matcher = ResumeJobMatcher(
        resume_path="data/user_resume.txt",
        alpha=0.6,
        critical_keywords=["Python"]
    )
    
    ranked = matcher.rank_jobs_from_json(
        "src/outputs/linkedin/job_postings.json",
        top_k=3
    )
    
    assert len(ranked) <= 3
    assert all('fit_score' in job for job in ranked)
    assert ranked[0]['fit_score'] >= ranked[-1]['fit_score']
    
    print("✅ Ranking working correctly!")

test_ranking()
```

---

**Ready to integrate?** Start with Option 1 for the quickest setup, or customize with the examples above!

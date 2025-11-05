# Job Fit Ranking System

A sophisticated hybrid ranking algorithm that assesses job-resume fit by combining **embedding-based semantic similarity** with **keyword relevance weighting**.

## 🎯 Overview

This system ranks job postings based on how well they match a candidate's resume using two complementary approaches:

1. **Semantic Similarity (Embeddings)**: Uses OpenAI's `text-embedding-3-small` to capture deep conceptual matches
2. **Keyword Relevance (TF-IDF)**: Employs scikit-learn's TF-IDF vectorization to identify exact skill/term matches
3. **Critical Keyword Boosting**: Provides bonus scoring for must-have skills

### Algorithm Formula

```
final_score = α × embedding_similarity + (1-α) × keyword_relevance + keyword_boost
```

Where:
- **α** (alpha): Weight parameter balancing semantic vs keyword matching (0.0 to 1.0)
- **embedding_similarity**: Cosine similarity between resume and job description embeddings (0-1)
- **keyword_relevance**: TF-IDF-based keyword overlap score (0-1)
- **keyword_boost**: Bonus for critical skill matches (0-0.2)

## 📦 Installation

### Prerequisites

```bash
# Required packages
pip install openai scikit-learn numpy
```

### Environment Setup

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Quick Start

### Basic Usage

```python
from job_ranker import ResumeJobMatcher

# Initialize matcher
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.6  # Balanced approach
)

# Rank jobs from JSON file
ranked_jobs = matcher.rank_jobs_from_json(
    json_path="src/outputs/linkedin/job_postings.json",
    top_k=10
)

# Display results
for job in ranked_jobs:
    print(f"{job['job_title']} - Fit: {job['fit_percentage']}")
```

### Detailed Analysis

```python
# Analyze a specific job in detail
analysis = matcher.analyze_specific_job(job_dict)

print(f"Score: {analysis['score_breakdown']['final_score']:.2f}")
print(f"Assessment: {analysis['overall_assessment']}")
print(f"Matched Skills: {analysis['matched_critical_skills']}")
print(f"Recommendations: {analysis['recommendations']}")
```

## 🎨 Features

### 1. Hybrid Scoring System

Combines two complementary approaches:

- **Embeddings**: Captures semantic meaning and conceptual relationships
  - Example: "Python developer" matches "software engineer proficient in Python"
  - Handles synonyms, related concepts, and context

- **Keywords**: Ensures exact skill matches aren't missed
  - Example: Resume mentions "React" → job requires "React" → strong match
  - Critical for technical skills and specific tools

### 2. Configurable Alpha Parameter

Tune the balance between semantic and keyword matching:

| Alpha Value | Emphasis | Use Case |
|------------|----------|----------|
| 0.2-0.4 | Keyword-heavy | When exact skill matches are critical |
| 0.5-0.6 | **Balanced** (recommended) | General purpose, most robust |
| 0.7-0.8 | Semantic-heavy | Career transitions, transferable skills |
| 0.9 | Very semantic | Exploring adjacent fields |

### 3. Critical Keyword Boosting

Specify must-have skills for bonus scoring:

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.6,
    critical_keywords=["Python", "Machine Learning", "AWS"]
)
```

Each matched critical keyword adds **0.05 points** (up to 0.2 total boost).

### 4. TF-IDF Keyword Analysis

- Extracts up to 500 most important keywords
- Uses unigrams and bigrams for richer matching
- Identifies both matching and missing keywords

### 5. Comprehensive Analytics

Get detailed breakdowns including:
- Component scores (embedding, keyword, boost)
- Matched vs missing critical skills
- Top matching keywords
- Actionable recommendations

## 📊 Example Use Cases

### Use Case 1: Standard Job Search

**Scenario**: Recent graduate looking for entry-level data science positions

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.6,  # Balanced
    critical_keywords=["Python", "SQL", "Data Analysis", "Machine Learning"]
)

ranked_jobs = matcher.rank_jobs_from_json("jobs.json", top_k=10)
```

**Why α=0.6?**
- Balance between technical skill requirements and broader fit
- Ensures critical tools are recognized while allowing for conceptual matches

### Use Case 2: Career Transition

**Scenario**: Software engineer transitioning to machine learning

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.75,  # More semantic
    critical_keywords=["Python", "TensorFlow", "PyTorch"]
)
```

**Why α=0.75?**
- Higher semantic weight captures transferable programming skills
- Still requires critical ML frameworks via keyword boost

### Use Case 3: Specialized Technical Role

**Scenario**: Senior engineer with specific tech stack requirements

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.4,  # More keyword-focused
    critical_keywords=["Kubernetes", "Terraform", "Go", "gRPC"]
)
```

**Why α=0.4?**
- Exact technology matches are paramount
- Less emphasis on conceptual similarity

### Use Case 4: Broad Exploration

**Scenario**: Exploring various roles to find best fit

```python
matcher = ResumeJobMatcher(
    resume_path="data/user_resume.txt",
    alpha=0.6,
    critical_keywords=[]  # No hard requirements
)

# Rank all jobs, then categorize
all_jobs = matcher.rank_jobs_from_json("jobs.json", top_k=None)

excellent = [j for j in all_jobs if j['fit_score'] >= 0.8]
good = [j for j in all_jobs if 0.65 <= j['fit_score'] < 0.8]
moderate = [j for j in all_jobs if 0.5 <= j['fit_score'] < 0.65]
```

## 🎛️ Advanced Configuration

### Custom JobFitRanker

For more control, use `JobFitRanker` directly:

```python
from job_ranker import JobFitRanker

ranker = JobFitRanker(
    alpha=0.6,
    embedding_model="text-embedding-3-small",  # or "text-embedding-3-large"
    max_tfidf_features=500,  # Number of keywords to extract
    critical_keywords=["Python", "AWS"]
)

# Load your data
with open("resume.txt") as f:
    resume_text = f.read()

with open("jobs.json") as f:
    jobs = json.load(f)['job_postings']

# Rank jobs
ranked = ranker.rank_jobs(resume_text, jobs, top_k=10)
```

### Batch Processing

Process large datasets efficiently:

```python
import json

# Load all job postings
all_jobs = []
for file in ["jobs_1.json", "jobs_2.json", "jobs_3.json"]:
    with open(file) as f:
        all_jobs.extend(json.load(f)['job_postings'])

# Rank in one batch
matcher = ResumeJobMatcher("resume.txt", alpha=0.6)
with open("resume.txt") as f:
    resume = f.read()

ranked = matcher.ranker.rank_jobs(resume, all_jobs, top_k=50)
```

## 📈 Performance Tuning

### Optimizing Alpha

Test different values to find what works for your use case:

```python
from utils.job_fit_ranker import JobFitRanker

alphas = [0.3, 0.5, 0.7, 0.9]
results = {}

for alpha in alphas:
    ranker = JobFitRanker(alpha=alpha)
    ranked = ranker.rank_jobs(resume_text, jobs, top_k=5)
    results[alpha] = ranked

# Compare results and choose best alpha
```

### Caching Strategy

Embeddings are automatically cached to reduce API calls:

```python
# First call: Computes embeddings
ranked_1 = matcher.rank_jobs_from_json("jobs.json")

# Subsequent calls: Uses cached embeddings
ranked_2 = matcher.rank_jobs_from_json("jobs.json")  # Faster!
```

### Cost Optimization

OpenAI embeddings cost approximately:

- **text-embedding-3-small**: $0.02 per 1M tokens
- **text-embedding-3-large**: $0.13 per 1M tokens

For most use cases, `-small` provides excellent results at lower cost.

## 🔌 Streamlit Integration

### Add to Existing Page

```python
# In your Streamlit page (e.g., specific_jobs.py)
from job_ranker.ranking_integration import add_ranking_to_streamlit_page

# Add ranking section
add_ranking_to_streamlit_page()
```

### Custom Streamlit Widget

```python
from job_ranker.ranking_integration import (
    display_ranked_jobs_streamlit,
    display_fit_analysis_streamlit,
    create_ranking_dataframe
)

# Rank jobs
ranked_jobs = matcher.rank_jobs_from_json("jobs.json")

# Display with Streamlit components
display_ranked_jobs_streamlit(ranked_jobs, show_scores=True)

# Show detailed analysis for selected job
if st.button("Analyze"):
    analysis = matcher.analyze_specific_job(selected_job)
    display_fit_analysis_streamlit(analysis)

# Export to DataFrame
df = create_ranking_dataframe(ranked_jobs)
st.dataframe(df)
```

## 📝 Example Scripts

### Run Demo

```bash
# Run all examples
python src/job_ranker/examples/job_ranking_demo.py
```

Includes:
1. Basic job ranking
2. Detailed fit analysis
3. Alpha configuration comparison
4. Batch processing with categorization
5. Saving results to JSON

### Integration Test

```python
# Test with your actual data
from job_ranker.ranking_integration import get_ranking_widget

ranked = get_ranking_widget(
    resume_path="data/user_resume.txt",
    jobs_json_path="src/outputs/linkedin/job_postings.json",
    alpha=0.6,
    critical_keywords=["Python", "Machine Learning"]
)

print(f"Top match: {ranked[0]['job_title']} ({ranked[0]['fit_percentage']})")
```

## 🎓 Understanding the Algorithm

### Why Hybrid Approach?

Pure semantic similarity can miss critical technical requirements:
- Job requires "React" but only mentions "frontend framework" → semantic match, skill mismatch

Pure keyword matching lacks context:
- Resume says "data analysis" but job says "analytics" → should match, but keywords differ

**Solution**: Combine both approaches with configurable weighting.

### What Makes a Good Match?

The algorithm considers:

1. **Skills Overlap**: Direct mention of same technologies/tools
2. **Conceptual Alignment**: Similar responsibilities and problem domains
3. **Experience Level**: Implied seniority from job description
4. **Domain Knowledge**: Industry-specific terminology

### Score Interpretation

| Score Range | Interpretation | Action |
|------------|----------------|--------|
| 0.80-1.00 | Excellent fit | Apply immediately |
| 0.65-0.79 | Good fit | Strong candidate |
| 0.50-0.64 | Moderate fit | Consider if interested |
| 0.00-0.49 | Weak fit | Probably not a match |

## 🛠️ Troubleshooting

### Issue: All scores are very high (>0.9)

**Solution**: Increase keyword weight (lower alpha)

```python
matcher = ResumeJobMatcher(resume_path="resume.txt", alpha=0.4)
```

### Issue: All scores are very low (<0.3)

**Solution**: Increase semantic weight (higher alpha) or check resume quality

```python
matcher = ResumeJobMatcher(resume_path="resume.txt", alpha=0.75)
```

### Issue: OpenAI API errors

**Solution**: Check your API key and rate limits

```python
import os
print(os.getenv("OPENAI_API_KEY"))  # Should not be None
```

### Issue: Slow performance

**Solution**: 
1. Reduce `max_tfidf_features` for faster keyword processing
2. Use `top_k` to limit results
3. Cache embeddings are already implemented

## 📚 API Reference

### JobFitRanker

Main ranking engine class.

```python
JobFitRanker(
    alpha: float = 0.6,
    embedding_model: str = "text-embedding-3-small",
    max_tfidf_features: int = 500,
    critical_keywords: List[str] = None
)
```

**Methods:**

- `compute_job_fit_score(resume_text, job_description) -> float`: Score single job
- `rank_jobs(resume_text, jobs, top_k) -> List[Dict]`: Rank multiple jobs
- `analyze_fit_breakdown(resume_text, job) -> Dict`: Detailed analysis

### ResumeJobMatcher

High-level wrapper for common workflows.

```python
ResumeJobMatcher(
    resume_path: str,
    alpha: float = 0.6,
    critical_keywords: List[str] = None
)
```

**Methods:**

- `rank_jobs_from_json(json_path, top_k) -> List[Dict]`: Rank from JSON file
- `analyze_specific_job(job_dict) -> Dict`: Analyze single job

## 🤝 Contributing

Suggestions for improvement:

1. **Custom Embeddings**: Train domain-specific embeddings
2. **Learning to Rank**: Use ML model to optimize alpha per user
3. **Temporal Decay**: Adjust scores based on posting age
4. **Company Fit**: Incorporate company culture matching

## 📄 License

Part of the CrewAI Career Assistant project.

## 📞 Support

For questions or issues:
1. Check example scripts in `src/job_ranker/examples/job_ranking_demo.py`
2. Review integration guide in `src/job_ranker/docs/INTEGRATION_GUIDE.md`
3. Run with verbose mode for debugging

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Maintained by**: CrewAI Career Assistant Team

"""
Job Fit Ranking Algorithm - Hybrid Semantic + Keyword Approach
================================================================

This module implements a sophisticated job fit scoring system that combines:
1. Embedding-based semantic similarity (deep understanding)
2. Keyword/TF-IDF relevance weighting (explicit matching)
3. Configurable weight balancing between the two approaches

Author: CrewAI Job Search Assistant
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re


class JobFitRanker:
    """
    Hybrid job fit ranking system combining semantic embeddings with keyword relevance.
    
    Architecture:
    - Uses OpenAI embeddings for deep semantic understanding
    - Applies TF-IDF for keyword importance weighting
    - Combines scores using configurable alpha parameter
    - Supports custom keyword boosting for critical skills
    
    Scoring Formula:
        final_score = α × embedding_similarity + (1-α) × keyword_relevance + keyword_boost
        
    Where:
        α (alpha): Weight for semantic vs keyword (0-1)
        embedding_similarity: Cosine similarity of embeddings (0-1)
        keyword_relevance: TF-IDF based matching score (0-1)
        keyword_boost: Bonus for critical keywords (0-0.2)
    """
    
    def __init__(
        self,
        alpha: float = 0.6,
        use_openai_embeddings: bool = True,
        embedding_model: str = "text-embedding-3-small",
        critical_keywords: Optional[List[str]] = None,
        keyword_boost_weight: float = 0.1
    ):
        """
        Initialize the job fit ranker.
        
        Args:
            alpha: Weight for embedding similarity (0-1). Higher = more semantic, lower = more keyword.
                   Recommended: 0.6 for balanced, 0.7-0.8 for semantic-heavy, 0.3-0.4 for keyword-heavy
            use_openai_embeddings: Whether to use OpenAI embeddings (True) or fallback to TF-IDF only
            embedding_model: OpenAI embedding model to use
            critical_keywords: List of must-have keywords to boost (e.g., ["Python", "AWS", "React"])
            keyword_boost_weight: Bonus multiplier for critical keywords (0-0.2 recommended)
        """
        self.alpha = alpha
        self.use_openai_embeddings = use_openai_embeddings
        self.embedding_model = embedding_model
        self.critical_keywords = [kw.lower() for kw in (critical_keywords or [])]
        self.keyword_boost_weight = keyword_boost_weight
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),  # Unigrams and bigrams
            stop_words='english',
            lowercase=True,
            min_df=1
        )
        
        # Cache for embeddings to avoid redundant API calls
        self._embedding_cache = {}
        
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text using OpenAI API (with caching).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        
        try:
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            
            embedding = np.array(response.data[0].embedding)
            self._embedding_cache[text] = embedding
            return embedding
            
        except Exception as e:
            print(f"Warning: Failed to get embedding: {e}")
            print("Falling back to TF-IDF only mode")
            return None
    
    def _compute_embedding_similarity(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Compute cosine similarity between resume and job description embeddings.
        
        Args:
            resume_text: Resume content
            job_description: Job description content
            
        Returns:
            Similarity score (0-1)
        """
        if not self.use_openai_embeddings:
            return 0.0
        
        resume_embedding = self._get_embedding(resume_text)
        job_embedding = self._get_embedding(job_description)
        
        if resume_embedding is None or job_embedding is None:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(resume_embedding, job_embedding) / (
            np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
        )
        
        # Normalize to 0-1 range (cosine similarity is -1 to 1)
        return (similarity + 1) / 2
    
    def _compute_keyword_relevance(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Compute TF-IDF based keyword relevance score.
        
        Args:
            resume_text: Resume content
            job_description: Job description content
            
        Returns:
            Relevance score (0-1)
        """
        try:
            # Fit TF-IDF on both documents
            corpus = [resume_text, job_description]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(corpus)
            
            # Compute cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return max(0.0, min(1.0, similarity))  # Clamp to 0-1
            
        except Exception as e:
            print(f"Warning: TF-IDF computation failed: {e}")
            return 0.0
    
    def _compute_keyword_boost(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Compute bonus score for critical keywords match.
        
        Args:
            resume_text: Resume content
            job_description: Job description content
            
        Returns:
            Boost score (0-keyword_boost_weight)
        """
        if not self.critical_keywords:
            return 0.0
        
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Count how many critical keywords appear in BOTH resume and job description
        matched_keywords = 0
        total_keywords = len(self.critical_keywords)
        
        for keyword in self.critical_keywords:
            if keyword in resume_lower and keyword in job_lower:
                matched_keywords += 1
        
        # Return proportional boost
        if total_keywords > 0:
            match_ratio = matched_keywords / total_keywords
            return match_ratio * self.keyword_boost_weight
        
        return 0.0
    
    def compute_job_fit_score(
        self,
        resume_text: str,
        job_description: str,
        return_components: bool = False
    ) -> Union[float, Dict[str, float]]:
        """
        Compute overall job fit score combining all components.
        
        Args:
            resume_text: Full resume text
            job_description: Full job description text
            return_components: If True, return dict with component scores
            
        Returns:
            Overall fit score (0-1) or dict with breakdown if return_components=True
        """
        # Compute individual components
        embedding_sim = self._compute_embedding_similarity(resume_text, job_description)
        keyword_rel = self._compute_keyword_relevance(resume_text, job_description)
        keyword_boost = self._compute_keyword_boost(resume_text, job_description)
        
        # Combined score
        base_score = self.alpha * embedding_sim + (1 - self.alpha) * keyword_rel
        final_score = min(1.0, base_score + keyword_boost)  # Cap at 1.0
        
        if return_components:
            return {
                "final_score": final_score,
                "embedding_similarity": embedding_sim,
                "keyword_relevance": keyword_rel,
                "keyword_boost": keyword_boost,
                "base_score": base_score,
                "alpha": self.alpha
            }
        
        return final_score
    
    def rank_jobs(
        self,
        resume_text: str,
        job_postings: List[Dict],
        top_k: Optional[int] = None,
        return_scores: bool = True
    ) -> List[Dict]:
        """
        Rank a list of job postings by fit score.
        
        Args:
            resume_text: User's resume text
            job_postings: List of job posting dicts with 'job_title' and optionally 'description'
            top_k: Return only top K jobs (None for all)
            return_scores: Include fit scores in results
            
        Returns:
            Sorted list of job postings with scores
        """
        scored_jobs = []
        
        for job in job_postings:
            # Build job description from available fields
            job_description = self._build_job_description(job)
            
            # Compute fit score
            score = self.compute_job_fit_score(resume_text, job_description)
            
            # Add score to job data
            job_with_score = job.copy()
            if return_scores:
                job_with_score['fit_score'] = round(score, 4)
                job_with_score['fit_percentage'] = f"{round(score * 100, 1)}%"
            
            scored_jobs.append(job_with_score)
        
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x.get('fit_score', 0), reverse=True)
        
        # Return top K if specified
        if top_k is not None:
            return scored_jobs[:top_k]
        
        return scored_jobs
    
    def _build_job_description(self, job: Dict) -> str:
        """
        Build a comprehensive job description from job posting fields.
        
        Args:
            job: Job posting dictionary
            
        Returns:
            Combined job description text
        """
        parts = []
        
        # Add available fields
        if job.get('job_title'):
            parts.append(f"Position: {job['job_title']}")
        
        if job.get('company_name'):
            parts.append(f"Company: {job['company_name']}")
        
        if job.get('location'):
            parts.append(f"Location: {job['location']}")
        
        if job.get('employment_type'):
            parts.append(f"Type: {job['employment_type']}")
        
        if job.get('experience_level'):
            parts.append(f"Level: {job['experience_level']}")
        
        if job.get('description'):
            parts.append(f"Description: {job['description']}")
        
        if job.get('skills'):
            if isinstance(job['skills'], list):
                parts.append(f"Skills: {', '.join(job['skills'])}")
            else:
                parts.append(f"Skills: {job['skills']}")
        
        if job.get('requirements'):
            parts.append(f"Requirements: {job['requirements']}")
        
        return " ".join(parts)
    
    def analyze_fit_breakdown(
        self,
        resume_text: str,
        job_description: str
    ) -> Dict:
        """
        Provide detailed analysis of job fit with explanations.
        
        Args:
            resume_text: User's resume
            job_description: Job description
            
        Returns:
            Dict with detailed breakdown and recommendations
        """
        components = self.compute_job_fit_score(
            resume_text,
            job_description,
            return_components=True
        )
        
        # Extract keywords from both
        resume_keywords = self._extract_top_keywords(resume_text)
        job_keywords = self._extract_top_keywords(job_description)
        
        # Find matching keywords
        matching_keywords = set(resume_keywords) & set(job_keywords)
        missing_keywords = set(job_keywords) - set(resume_keywords)
        
        # Find matched critical keywords
        matched_critical = [
            kw for kw in self.critical_keywords
            if kw in resume_text.lower() and kw in job_description.lower()
        ]
        missing_critical = [
            kw for kw in self.critical_keywords
            if kw in job_description.lower() and kw not in resume_text.lower()
        ]
        
        return {
            "score_breakdown": components,
            "overall_assessment": self._get_fit_assessment(components['final_score']),
            "matching_keywords": list(matching_keywords)[:10],
            "missing_keywords": list(missing_keywords)[:10],
            "matched_critical_skills": matched_critical,
            "missing_critical_skills": missing_critical,
            "recommendations": self._generate_recommendations(
                components['final_score'],
                missing_keywords,
                missing_critical
            )
        }
    
    def _extract_top_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract top keywords using TF-IDF."""
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text])
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            # Get top N keywords
            top_indices = scores.argsort()[-top_n:][::-1]
            return [feature_names[i] for i in top_indices if scores[i] > 0]
        except:
            return []
    
    def _get_fit_assessment(self, score: float) -> str:
        """Get qualitative assessment of fit score."""
        if score >= 0.8:
            return "Excellent Match - Highly Recommended"
        elif score >= 0.65:
            return "Good Match - Strong Candidate"
        elif score >= 0.5:
            return "Moderate Match - Potential Fit"
        elif score >= 0.35:
            return "Weak Match - Significant Gaps"
        else:
            return "Poor Match - Not Recommended"
    
    def _generate_recommendations(
        self,
        score: float,
        missing_keywords: set,
        missing_critical: List[str]
    ) -> List[str]:
        """Generate actionable recommendations based on fit analysis."""
        recommendations = []
        
        if score < 0.5:
            recommendations.append("Consider upskilling in the missing areas before applying")
        
        if missing_critical:
            recommendations.append(
                f"Critical missing skills: {', '.join(missing_critical[:5])} - "
                "Consider gaining experience in these areas"
            )
        
        if len(missing_keywords) > 10:
            recommendations.append(
                "Significant keyword gaps detected - Review job requirements carefully"
            )
        
        if score >= 0.65:
            recommendations.append("Strong match - Tailor your resume to highlight relevant experience")
        
        if score >= 0.8:
            recommendations.append("Excellent fit - Apply with confidence!")
        
        return recommendations or ["Review job requirements and assess your qualifications"]


class ResumeJobMatcher:
    """
    High-level interface for matching resumes to job postings.
    Simplifies the ranking workflow for common use cases.
    """
    
    def __init__(
        self,
        resume_path: Optional[str] = None,
        resume_text: Optional[str] = None,
        alpha: float = 0.6,
        critical_keywords: Optional[List[str]] = None
    ):
        """
        Initialize matcher with resume and configuration.
        
        Args:
            resume_path: Path to resume file
            resume_text: Resume text (if not providing path)
            alpha: Embedding vs keyword weight (0-1)
            critical_keywords: List of must-have skills
        """
        # Load resume
        if resume_path:
            with open(resume_path, 'r') as f:
                self.resume_text = f.read()
        elif resume_text:
            self.resume_text = resume_text
        else:
            raise ValueError("Must provide either resume_path or resume_text")
        
        # Initialize ranker
        self.ranker = JobFitRanker(
            alpha=alpha,
            critical_keywords=critical_keywords
        )
    
    def rank_jobs_from_json(
        self,
        json_path: str,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Rank jobs from a LinkedIn search results JSON file.
        
        Args:
            json_path: Path to job postings JSON
            top_k: Number of top jobs to return
            
        Returns:
            Ranked list of jobs with scores
        """
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        job_postings = data.get('job_postings', [])
        
        return self.ranker.rank_jobs(
            self.resume_text,
            job_postings,
            top_k=top_k
        )
    
    def analyze_specific_job(self, job: Dict) -> Dict:
        """
        Get detailed fit analysis for a specific job.
        
        Args:
            job: Job posting dictionary
            
        Returns:
            Detailed analysis with recommendations
        """
        job_description = self.ranker._build_job_description(job)
        
        return self.ranker.analyze_fit_breakdown(
            self.resume_text,
            job_description
        )

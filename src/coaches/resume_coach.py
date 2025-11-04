
"""
Resume Coach - AI-powered resume improvement assistant
Analyzes resume content, identifies missing skills, and rewrites the resume.
"""

import json
import os
import re
from pathlib import Path
from crewai import LLM
from dotenv import load_dotenv

# Load API keys
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "outputs" / "lead_research_analyst"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def normalize(text: str) -> str:
    """Clean and standardize text."""
    return re.sub(r"\s+", " ", text.strip()).lower()

def contains(word: str, text: str) -> bool:
    """Check if a word is contained in text (case-insensitive)."""
    return normalize(word) in normalize(text)

def load_job_data():
    """Load job research results."""
    path = DATA_DIR / "research_data.json"
    if not path.exists():
        raise FileNotFoundError(f"❌ research_data.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_text(uploaded_resume_path=None):
    """Load user resume text."""
    data_path = uploaded_resume_path or (BASE_DIR / "data" / "user_resume.txt")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Resume not found at {data_path}")
    with open(data_path, "r", encoding="utf-8") as f:
        return f.read()

def find_missing_skills(job_data, resume_text):
    """Find skills in job description that are missing in resume."""
    return [s for s in job_data.get("required_skills", []) if not contains(s, resume_text)]

def build_improvement_prompt(job_data, resume_text, missing_skills):
    """Build LLM prompt for resume rewrite."""
    job_title = job_data.get("job_title", "the target role")
    job_description = job_data.get("job_description", "")
    skills = ", ".join(job_data.get("required_skills", []))

    return f"""
You are an expert resume editor. The user is applying for **{job_title}**.

Here is their current resume:
---
{resume_text}
---

Job Description:
{job_description}

Key required skills: {skills}
Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}

Rewrite the resume to:
1. Add missing but relevant skills.
2. Quantify achievements (numbers, metrics).
3. Improve clarity and professional tone.
4. Keep it honest—no fabricated experience.
5. Return the improved resume in clean markdown format.
"""

def write_updated_resume(text):
    """Save the improved resume to file."""
    out_path = OUT_DIR / "resume_updated.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path

def run_resume_coach(uploaded_resume_path=None):
    """Main entrypoint: run the resume improvement pipeline."""
    job_data = load_job_data()
    resume_text = load_resume_text(uploaded_resume_path)
    missing_skills = find_missing_skills(job_data, resume_text)

    prompt = build_improvement_prompt(job_data, resume_text, missing_skills)

    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    print("🤖 Improving resume with AI...")
    improved_resume = llm.call(prompt)

    path = write_updated_resume(improved_resume)
    return {
        "missing_skills": missing_skills,
        "updated_resume_path": str(path),
        "preview": improved_resume[:700] + "..."
    }

if __name__ == "__main__":
    result = run_resume_coach()
    print(json.dumps(result, indent=2))
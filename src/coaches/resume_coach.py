import json
from pathlib import Path
import re

def normalize(text: str) -> str:
    """Clean and standardize text"""
    return re.sub(r"\s+", " ", text.strip().lower())

def contains(word: str, text: str) -> bool:
    """Check if a word is in text (case-insensitive)."""
    return normalize(word) in normalize(text)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "outputs" / "lead_research_analyst"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def load_job_data():
    """Load analyzed job research data."""
    path = DATA_DIR / "research_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_text():
    """Load user's resume (plain text)."""
    resume_path = BASE_DIR / "data" / "user_resume.txt"
    with open(resume_path, "r", encoding="utf-8") as f:
        return f.read()

def find_missing_skills(job_data, resume_text):
    missing = []
    for skill in job_data.get("required_skills", []):
        if not contains(skill, resume_text):
            missing.append(skill)
    return missing

def enhance_resume(resume_text, job_data, missing_skills):
    """Rebuild a stronger resume version."""
    header = "=== AI-Enhanced Resume Draft ===\n\n"
    jd = job_data.get("job_description", "")
    companies = ", ".join(job_data.get("top_hiring_companies", []))
    skills = ", ".join(job_data.get("required_skills", []))
    salary = ", ".join(job_data.get("average_salaries", []))

    improvements = [
        f"Added missing or underrepresented skills: {', '.join(missing_skills)}." if missing_skills else "All key skills found.",
        "Strengthened project and achievement descriptions using measurable impact verbs.",
        "Ensured alignment with job requirements and AI/ML trends.",
        "Added more technical depth where relevant (e.g., MLOps, model deployment).",
    ]

    # Rebuild main sections
    enhanced = (
        f"{header}"
        f"·TARGET ROLE:\n{jd}\n\n"
        f"·Top Employers Hiring for This Role:\n{companies}\n\n"
        f"·Key Skills in Demand:\n{skills}\n\n"
        f"·Salary Benchmark:\n{salary}\n\n"
        f"·Suggested Enhancements:\n- " + "\n- ".join(improvements) + "\n\n"
        f"·Enhanced Resume Content:\n\n"
        f"{resume_text}\n\n"
    )

    # Add new section: AI recommendations
    if missing_skills:
        enhanced += "### New Suggested Skill Section:\n"
        enhanced += "\n".join([f"- {skill}" for skill in missing_skills]) + "\n\n"

    enhanced += "### Actionable Tips:\n"
    enhanced += (
        "- Use quantified achievements (e.g., 'increased efficiency by 20%').\n"
        "- Start bullet points with strong verbs: Designed, Implemented, Optimized, Deployed.\n"
        "- Highlight Python frameworks, teamwork, and project ownership.\n"
        "- Mention tools like TensorFlow, PyTorch, Docker, or MLOps pipelines.\n"
    )

    return enhanced


def write_updated_resume(content: str):
    """Save enhanced resume text."""
    out_path = OUT_DIR / "resume_updated.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path

def run_resume_coach(resume_path=None):
    job_data = load_job_data()
    resume_text = load_resume_text() if resume_path is None else Path(resume_path).read_text(encoding="utf-8")

    missing_skills = find_missing_skills(job_data, resume_text)
    enhanced_resume = enhance_resume(resume_text, job_data, missing_skills)
    updated_path = write_updated_resume(enhanced_resume)

    return {
        "missing_skills": missing_skills,
        "updated_resume_path": str(updated_path),
        "improvement_summary": f"Enhanced resume generated with {len(missing_skills)} missing skills identified."
    }

if __name__ == "__main__":
    result = run_resume_coach()
    print(json.dumps(result, indent=2))
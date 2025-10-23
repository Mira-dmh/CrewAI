import json
from pathlib import Path
import re

def normalize(text: str) -> str:
    """Clean and standardize text (remove extra spaces, lowercase, etc.)"""
    return re.sub(r"\s+", " ", text.strip()).lower()

def contains(word: str, text: str) -> bool:
    """Check if a word is contained in a text (case-insensitive)."""
    return normalize(word) in normalize(text)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "outputs" / "lead_research_analyst"   
OUT_DIR  = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def load_job_data():
    """Load job research results (from lead_research_analyst output)."""
    file_path = DATA_DIR / "research_data.json"
    if not file_path.exists():
        raise FileNotFoundError(f"❌ Could not find research_data.json at {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_text():
    """Load user resume text from /data/user_resume.txt"""
    data_path = BASE_DIR / "data" / "user_resume.txt"
    if not data_path.exists():
        raise FileNotFoundError(f"❌ Could not find user_resume.txt at {data_path}")
    
    with open(data_path, "r", encoding="utf-8") as f:
        return f.read()

def find_missing_skills(job_data, resume_text):
    missing = []
    for skill in job_data.get("required_skills", []):
        if not contains(skill, resume_text):
            missing.append(skill)
    return missing

def build_improvement_bullets(job_data, missing_skills):
    bullets = []
    if missing_skills:
        bullets.append(f"Add or emphasize missing skills: {', '.join(missing_skills)}.")
    bullets.append("Rewrite achievements with metrics (e.g., 'improved model accuracy by 7%').")
    bullets.append("Mirror keywords from the job description in Skills / Experience sections.")
    bullets.append("Bring relevant responsibilities to the top for quick ATS matching.")
    return bullets

def write_updated_resume(resume_text, missing_skills):
    header = "=== Updated Resume Suggestions ===\n"
    if missing_skills:
        skill_line = "Added keywords: " + ", ".join(missing_skills) + "\n"
    else:
        skill_line = "No missing skill keywords detected.\n"
    updated_resume = (
        header + skill_line + "\n" + resume_text +
        ("\n\n[Injected keywords for ATS optimization]: " + ", ".join(missing_skills) if missing_skills else "")
    )
    
    out_path = OUT_DIR / "resume_updated.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(updated_resume)
    return out_path


def run_resume_coach():
    job_data = load_job_data()
    resume_text = load_resume_text()

    missing_skills = find_missing_skills(job_data, resume_text)
    bullets = build_improvement_bullets(job_data, missing_skills)
    write_updated_resume(resume_text, missing_skills)

    return {
        "missing_skills": missing_skills,
        "improvements": bullets,
        "updated_resume_path": str(OUT_DIR / "resume_updated.txt")
    }

if __name__ == "__main__":
    result = run_resume_coach()
    print(json.dumps(result, indent=2))
import json
from pathlib import Path
import re

def normalize(text: str) -> str:
    """Clean and standardize text (remove extra spaces, lowercase, etc.)"""
    return re.sub(r"\s+", " ", text.strip()).lower()

def contains(word: str, text: str) -> bool:
    """Check if a word is contained in a text (case-insensitive)."""
    return normalize(word) in normalize(text)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUT_DIR.mkdir(exist_ok=True)

def load_job_data():
    with open(DATA_DIR / "sample_job_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_resume_text():
    with open(DATA_DIR / "user_resume.txt", "r", encoding="utf-8") as f:
        return f.read()

def find_missing_skills(job_data, resume_text):
    missing = []
    for skill in job_data.get("skills_required", []):
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
    body = resume_text + "\n\n[Keywords injected for ATS]: " + ", ".join(missing_skills) if missing_skills else ""
    with open(OUT_DIR / "resume_updated.txt", "w", encoding="utf-8") as f:
        f.write(header + skill_line + "\n" + body)

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
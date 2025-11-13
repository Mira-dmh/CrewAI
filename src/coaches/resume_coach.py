"""
Resume Coach - AI-powered resume improvement assistant
Supports .pdf and .txt resume files
"""

import json
import os
import re
from pathlib import Path
from crewai import LLM
from dotenv import load_dotenv
import PyPDF2  # PDF support

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "outputs" / "lead_research_analyst"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)


# --------------------------
# PDF Text Extraction
# --------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file safely."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise RuntimeError(f"❌ Failed to read PDF file: {e}")
    return text


# --------------------------
# Utility Functions
# --------------------------
def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def contains(word: str, text: str) -> bool:
    return normalize(word) in normalize(text)


# --------------------------
# Load Job Research Data
# --------------------------
def load_job_data():
    path = DATA_DIR / "research_data.json"
    if not path.exists():
        raise FileNotFoundError(f"❌ research_data.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --------------------------
# Load Resume (PDF / TXT)
# --------------------------
def load_resume_text(uploaded_resume_path=None):
    """
    Load resume from:
    - user-uploaded text file
    - user-uploaded pdf file
    - locally stored user_resume.txt
    """
    data_path = uploaded_resume_path or (BASE_DIR / "data" / "user_resume.txt")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Resume not found at {data_path}")

    # PDF
    if str(data_path).lower().endswith(".pdf"):
        return extract_text_from_pdf(str(data_path))

    # TXT
    with open(data_path, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------
# Missing Skills Detection
# --------------------------
def find_missing_skills(job_data, resume_text):
    return [
        s for s in job_data.get("required_skills", [])
        if not contains(s, resume_text)
    ]


# --------------------------
# LLM Prompt Construction
# --------------------------
def build_improvement_prompt(job_data, resume_text, missing_skills):
    job_title = job_data.get("job_title", "the target role")
    job_description = job_data.get("job_description", "")
    skills = ", ".join(job_data.get("required_skills", []))

    prompt = f"""
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
1. Add missing but relevant skills naturally.
2. Quantify achievements (numbers, metrics).
3. Improve clarity, structure, and professional tone.
4. Keep the resume honest — do not invent fake experience.
5. Return the improved resume in clean markdown format.

Only output the rewritten resume — no explanation.
"""
    return prompt


# --------------------------
# Save Updated Resume
# --------------------------
def write_updated_resume(text):
    out_path = OUT_DIR / "resume_updated.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    return out_path


# --------------------------
# Main Entry Point
# --------------------------
def run_resume_coach(uploaded_resume_path=None):
    """Full pipeline for resume improvement"""

    job_data = load_job_data()
    resume_text = load_resume_text(uploaded_resume_path)
    missing_skills = find_missing_skills(job_data, resume_text)

    prompt = build_improvement_prompt(job_data, resume_text, missing_skills)

    # Use CrewAI's LLM
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    print("🤖 Improving resume with AI...")
    improved_resume = llm.call(prompt)

    path = write_updated_resume(improved_resume)

    return {
        "missing_skills": missing_skills,
        "updated_resume_path": str(path),
        "preview": improved_resume[:800] + "..."
    }


# --------------------------
# Standalone Test Run
# --------------------------
if __name__ == "__main__":
    result = run_resume_coach()
    print(json.dumps(result, indent=2))
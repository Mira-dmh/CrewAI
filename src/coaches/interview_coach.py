"""
Interview Coach (Resume-Aware Version)
Generates interview questions and answers based on both job research data and updated resume.
"""

import json
from pathlib import Path
from crewai import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
JOB_DATA_PATH = BASE_DIR / "outputs" / "lead_research_analyst" / "research_data.json"
RESUME_PATH = BASE_DIR / "outputs" / "resume_updated.txt"
OUT_PATH = BASE_DIR / "outputs" / "interview_prep_guide.md"

def load_job_data():
    """Load job research JSON."""
    if not JOB_DATA_PATH.exists():
        raise FileNotFoundError(f"❌ Missing job data at {JOB_DATA_PATH}")
    with open(JOB_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_updated_resume():
    """Load the updated resume text."""
    if not RESUME_PATH.exists():
        raise FileNotFoundError(f"❌ Missing resume file at {RESUME_PATH}")
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(job_data, resume_text):
    """Build prompt combining job research + updated resume."""
    job_title = job_data.get("job_title", "Data Scientist")
    job_description = job_data.get("job_description", "")
    skills = ", ".join(job_data.get("required_skills", []))

    prompt = f"""
You are an expert Interview Coach preparing a candidate for a **{job_title}** role.

Below is the **Job Description**:
{job_description}

Required Skills: {skills}

And here is the candidate's **Updated Resume**:
---
{resume_text}
---

Your task:
Generate a detailed **Interview Preparation Guide** that:
1. Uses the resume details to personalize all example answers.
2. Includes **three sections**:
   - Technical Questions (**at least 10**, mix conceptual + applied)
   - Behavioral (STAR) Questions (**at least 5**, covering teamwork, leadership, conflict, learning)
   - Scenario Questions (**at least 5**, realistic job-related scenarios)
3. For each question:
   - Provide a 1-sentence **Answering Framework**
   - Provide a **Sample Answer**, personalized based on the resume (use first-person “I”)
4. End with a section “Questions to Ask the Interviewer”.
5. Make it realistic, professional, and aligned with the resume’s tone.

Output in clean Markdown format:

# Interview Prep Guide – {job_title}

## Technical Questions
**Question:**  
**Framework:**  
**Sample Answer:**  

## Behavioral Questions
**Question:**  
**Framework:**  
**Sample Answer:**  

## Scenario Questions
**Question:**  
**Framework:**  
**Sample Answer:**  

## Questions to Ask the Interviewer
- ...
- ...
- ...
"""
    return prompt

def run_llm(prompt):
    """Run the CrewAI LLM."""
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    print("🤖 Generating resume-aware interview guide...")
    return llm.call(prompt)

def write_output(content):
    """Write generated content to markdown."""
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return str(OUT_PATH)

def run_interview_coach():
    """Main function to generate personalized interview prep."""
    job_data = load_job_data()
    resume_text = load_updated_resume()
    prompt = build_prompt(job_data, resume_text)
    result = run_llm(prompt)
    path = write_output(result)

    return {
        "guide_path": str(path),
        "message": "✅ Interview guide generated based on updated resume!",
        "preview": result[:700] + "..."
    }

if __name__ == "__main__":
    output = run_interview_coach()
    print(json.dumps(output, indent=2))
"""
Interview Coach - Multi-Category Resume-Aware Interview Guide
Generates questions across multiple categories (General / Industry / Competency / Admissions / Government / Veterans)
and outputs personalized sample answers based on the candidate's resume + job description.
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
    """Load updated resume text."""
    if not RESUME_PATH.exists():
        raise FileNotFoundError(f"❌ Missing resume file at {RESUME_PATH}")
    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(job_data, resume_text):
    """Generate prompt to produce multi-category interview prep."""
    job_title = job_data.get("job_title", "Data Scientist")
    job_description = job_data.get("job_description", "")
    skills = ", ".join(job_data.get("required_skills", []))

    return f"""
You are a highly experienced Interview Coach. Prepare a full interview prep guide for a candidate applying for **{job_title}**.

=============================
📌 JOB DESCRIPTION
{job_description}

📌 REQUIRED SKILLS
{skills}

📌 UPDATED RESUME
{resume_text}
=============================

Generate a **comprehensive interview guide**, with all answers personalized to this resume.

The guide must include **six categories**:

---

# 1. GENERAL INTERVIEW QUESTIONS  
(These cover 80% of standard interview questions.)  
Provide:  
- **10 questions**  
- 1-sentence **Answering Framework**  
- **Personalized Sample Answer**  

---

# 2. INDUSTRY-SPECIFIC QUESTIONS  
(Tailored to the exact job title + industry.)  
Provide:  
- **8 questions**  
- Framework + Personalized Sample Answer  

---

# 3. COMPETENCY / SKILLSET QUESTIONS  
(Assess soft skills + technical competencies.)  
Provide:  
- **8 questions**  
- Use STAR where appropriate  
- Framework + Personalized Sample Answer  

---

# 4. ADMISSIONS-STYLE QUESTIONS  
(If the candidate might apply for grad programs, fellowships, or research roles.)  
Provide:  
- **6 questions**  
- Framework + Personalized Sample Answer  

---

# 5. GOVERNMENT / POLICY QUESTIONS  
(If the job touches public data, compliance, ethics, policy, privacy, or regulation.)  
Provide:  
- **5 questions**  
- Framework + Personalized Sample Answer  

---

# 6. VETERANS / CAREER TRANSITION QUESTIONS  
(General career transition questions that apply to ANYONE switching fields.)  
Provide:  
- **5 questions**  
- Framework + Personalized Sample Answer  

---

# Final Section: QUESTIONS TO ASK THE INTERVIEWER  
Provide **8 thoughtful, high-quality questions** tailored to the job and resume.

---

📌 FORMAT REQUIREMENTS  
Return the final output in clean Markdown:

## Category Name
### Question 1
**Framework:**  
**Answer:** (personalized using resume)

Do NOT shorten. Make answers realistic, polished, and job-aligned.
"""

def run_llm(prompt):
    """Run LLM through CrewAI."""
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    print("🤖 Generating categorized interview guide...")
    return llm.call(prompt)


def write_output(content):
    """Save markdown output."""
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return str(OUT_PATH)


def run_interview_coach():
    """Main workflow."""
    job_data = load_job_data()
    resume_text = load_updated_resume()
    prompt = build_prompt(job_data, resume_text)

    result = run_llm(prompt)
    path = write_output(result)

    return {
        "guide_path": str(path),
        "message": "✅ Multi-category interview guide created!",
        "preview": result[:700] + "..."
    }


if __name__ == "__main__":
    output = run_interview_coach()
    print(json.dumps(output, indent=2))
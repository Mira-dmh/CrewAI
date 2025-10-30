"""
Interview Coach - AI-driven Interview Preparation Assistant
Generates technical, behavioral, and scenario questions based on job research data.
"""

import json
from pathlib import Path
import random

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "outputs" / "lead_research_analyst"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

STAR_TIP = (
    "Use the STAR method (Situation, Task, Action, Result). "
    "Keep answers concise and highlight measurable impact."
)

def load_job_data():
    """Load job research JSON (from lead_research_analyst outputs)."""
    path = DATA_DIR / "research_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_questions_with_answers(job_data):
    """Generate questions with outlines & sample answers."""
    skills = job_data.get("required_skills", [])
    job_title = job_data.get("job_title", "Machine Learning Engineer")

    # --- Technical Questions ---
    tech = []
    for s in skills[:8]:
        tech.append({
            "q": f"What is your experience with {s}?",
            "outline": "Describe projects or tasks using this tool. Mention scale, team, and results.",
            "answer": f"In my projects, I applied {s} to solve real problems — for example, in my CrewAI assistant project, I used it to improve model performance and deployment efficiency."
        })

    # --- Behavioral Questions ---
    behavioral = [
        {
            "q": "Tell me about a time you solved a difficult technical problem.",
            "outline": STAR_TIP,
            "answer": "During my data analytics project, I faced inconsistent datasets. I automated the cleaning process using Python scripts, reducing prep time by 30%."
        },
        {
            "q": "Describe a situation where you had to learn a new skill quickly.",
            "outline": STAR_TIP,
            "answer": "When asked to use Docker for deployment, I self-learned it in 3 days and containerized the ML pipeline for stable production use."
        },
        {
            "q": "How do you handle tight deadlines and competing priorities?",
            "outline": "Explain how you prioritize tasks, communicate proactively, and maintain quality under pressure.",
            "answer": "I break tasks into milestones, use a task tracker, and communicate early when blockers appear. It keeps the team on track without burnout."
        },
    ]

    # --- Scenario Questions ---
    scenario = [
        {
            "q": "Your deployed model underperforms after release — how do you fix it?",
            "outline": "Discuss debugging, monitoring, retraining, and stakeholder communication.",
            "answer": "I'd check data drift, logs, and retrain using updated datasets. I’d also add monitoring metrics for early issue detection."
        },
        {
            "q": "You’re leading a project where two engineers disagree — what’s your approach?",
            "outline": "Explain conflict resolution, active listening, and focusing on data-driven decisions.",
            "answer": "I'd hold a short sync to understand both sides, then guide the decision with objective benchmarks like accuracy or efficiency."
        },
    ]

    return tech, behavioral, scenario

def write_prep_guide(job_data, tech, behavioral, scenario):
    """Write enhanced interview prep guide."""
    path = OUT_DIR / "interview_prep_guide.md"
    job_title = job_data.get("job_title", "Machine Learning Engineer")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f" Interview Prep Guide – {job_title}\n\n")
        f.write(f"Target Role Description: {job_data.get('job_description','')}\n\n")

        f.write(" ## Technical Questions & Sample Answers\n")
        for t in tech:
            f.write(f"Question: {t['q']}\n")
            f.write(f"Framework: {t['outline']}\n")
            f.write(f"Sample Answer: {t['answer']}\n\n")

        f.write("## Behavioral Questions & Sample Answers\n")
        for b in behavioral:
            f.write(f"Question: {b['q']}\n")
            f.write(f"Framework: {b['outline']}\n")
            f.write(f"Sample Answer: {b['answer']}\n\n")

        f.write("## Scenario-Based Questions & Sample Answers\n")
        for s in scenario:
            f.write(f"Question: {s['q']}\n")
            f.write(f"Framework: {s['outline']}\n")
            f.write(f"Sample Answer: {s['answer']}\n\n")

        f.write("##  General Tips\n")
        f.write("- Keep answers within 1–2 minutes.\n")
        f.write("- Use action verbs: Designed, Led, Deployed, Improved.\n")
        f.write("- Tie each example to a measurable impact.\n")
        f.write(f"- {STAR_TIP}\n")

    return str(path)

def run_interview_coach():
    job_data = load_job_data()
    tech, behavioral, scenario = generate_questions_with_answers(job_data)
    guide_path = write_prep_guide(job_data, tech, behavioral, scenario)
    return {
        "guide_path": guide_path,
        "counts": {
            "technical": len(tech),
            "behavioral": len(behavioral),
            "scenario": len(scenario)
        }
    }

if __name__ == "__main__":
    result = run_interview_coach()
    print(json.dumps(result, indent=2))
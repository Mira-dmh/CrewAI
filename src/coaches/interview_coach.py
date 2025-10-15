import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_DIR  = Path(__file__).resolve().parents[1] / "outputs"
OUT_DIR.mkdir(exist_ok=True)

STAR_TIP = (
    "Use the STAR method (Situation, Task, Action, Result). "
    "Keep answers concise and quantify impact."
)

def load_job_data():
    with open(DATA_DIR / "sample_job_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def generate_questions(job_data):
    skills = job_data.get("skills_required", [])
    technical = [f"What is your experience with {s}?" for s in skills[:6]]
    behavioral = [
        "Tell me about a time you solved a difficult technical problem.",
        "Describe how you handled conflicting deadlines.",
        "Give an example of cross-functional collaboration that improved outcomes."
    ]
    scenario = [
        "Your model underperforms after deployment. How do you diagnose and fix it?",
        "The data pipeline is flaky; outline your stabilization plan."
    ]
    return technical, behavioral, scenario

def write_prep_guide(job_data, technical, behavioral, scenario, tips):
    path = OUT_DIR / "interview_prep_guide.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Interview Prep Guide – {job_data.get('job_title','')}\n\n")
        f.write(f"**Company/Location:** {job_data.get('company','')} / {job_data.get('location','')}\n\n")
        f.write("## Technical Questions\n")
        for q in technical: f.write(f"- {q}\n")
        f.write("\n## Behavioral Questions\n")
        for q in behavioral: f.write(f"- {q}\n")
        f.write("\n## Scenario Questions\n")
        for q in scenario: f.write(f"- {q}\n")
        f.write("\n## Tips\n")
        for t in tips: f.write(f"- {t}\n")
    return str(path)

def run_interview_coach():
    job_data = load_job_data()
    technical, behavioral, scenario = generate_questions(job_data)
    tips = [
        STAR_TIP,
        "Reference quantified achievements from your résumé.",
        "Tie answers back to the role’s responsibilities and required tools."
    ]
    guide_path = write_prep_guide(job_data, technical, behavioral, scenario, tips)
    return {"guide_path": guide_path, "counts": {
        "technical": len(technical), "behavioral": len(behavioral), "scenario": len(scenario)
    }}

if __name__ == "__main__":
    print(json.dumps(run_interview_coach(), indent=2))
from coaches.resume_coach import run_resume_coach
from coaches.interview_coach import run_interview_coach

if __name__ == "__main__":
    print("== Running Resume Coach ==")
    rc = run_resume_coach()
    print(rc)

    print("\n== Running Interview Coach ==")
    ic = run_interview_coach()
    print(ic)

    print("\nOutputs:")
    print(" -", rc["updated_resume_path"])
    print(" -", ic["guide_path"])
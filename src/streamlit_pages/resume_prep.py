"""
Resume Preparation Page - AI-Powered Resume & Interview Coach
"""

import streamlit as st
import sys
from pathlib import Path

# === Add project root to import path ===
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "src" / "coaches"))

# === Import your two coach modules ===
from resume_coach import run_resume_coach
from interview_coach import run_interview_coach


def resume_prep_page():
    """AI-powered resume and interview preparation functionality"""
    st.title("🧠 Resume & Interview Preparation")
    st.markdown("Use AI-powered tools to optimize your resume and prepare for interviews intelligently.")

    # === Tabs for Resume / Interview ===
    tab1, tab2 = st.tabs(["📄 Resume Optimization", "🎤 Interview Preparation"])

    # === TAB 1: Resume Coach ===
    with tab1:
        st.subheader("📄 Resume Optimization Assistant")
        st.markdown("Upload your resume and get AI-powered feedback based on current job market requirements.")

        uploaded_file = st.file_uploader("Upload your resume (.txt)", type=["txt"])

        if uploaded_file:
            # Step 1️⃣ Save resume to /data folder
            data_dir = BASE_DIR / "data"
            data_dir.mkdir(exist_ok=True)
            resume_path = data_dir / "user_resume.txt"

            content = uploaded_file.read().decode("utf-8", errors="ignore")
            with open(resume_path, "w", encoding="utf-8") as f:
                f.write(content)

            st.success(f"✅ Resume uploaded: {uploaded_file.name}")

            # Step 2️⃣ Run Resume Coach
            with st.spinner("🤖 Analyzing your resume..."):
                try:
                    result = run_resume_coach(resume_path)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    result = None

            if result:
                st.markdown("### 🧠 Resume Improvement Suggestions")
                st.json(result)

                updated_path = Path(result["updated_resume_path"])
                if updated_path.exists():
                    with open(updated_path, "r", encoding="utf-8") as f:
                        updated_text = f.read()

                    st.text_area("📄 Updated Resume Draft", updated_text, height=400)

                    with open(updated_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Updated Resume",
                            data=f,
                            file_name="resume_updated.txt",
                            mime="text/plain"
                        )
                else:
                    st.warning("⚠️ Could not find generated resume file.")
        else:
            st.info("💡 Upload a `.txt` resume to start AI analysis.")

    # === TAB 2: Interview Coach ===
    with tab2:
        st.subheader("🎤 Interview Preparation Assistant")
        st.markdown("Generate personalized interview questions and tips based on your target job role.")

        if st.button("✨ Generate Interview Guide", use_container_width=True):
            with st.spinner("🧩 Generating interview questions..."):
                try:
                    result = run_interview_coach()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    result = None

            if result:
                st.success("✅ Interview Guide Created Successfully!")

                guide_path = Path(result["guide_path"])
        
                if "counts" in result:
                   st.markdown(f"**Total Questions:** {result['counts']}")
                else:
                   st.markdown("✅ Interview guide generated successfully!")

                if guide_path.exists():
                    with open(guide_path, "r", encoding="utf-8") as f:
                        guide_text = f.read()
                    st.text_area("📘 Interview Prep Guide", guide_text, height=400)

                    with open(guide_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Interview Guide",
                            data=f,
                            file_name="interview_prep_guide.md",
                            mime="text/markdown"
                        )
                else:
                    st.warning("⚠️ Could not find generated interview guide file.")
        else:
            st.info("💡 Click **Generate Interview Guide** to create a custom Q&A set.")

    st.markdown("---")
    st.caption("CrewAI Career Toolkit | Resume Coach + Interview Coach © 2025")


# === Run standalone ===
if __name__ == "__main__":
    st.set_page_config(page_title="Resume & Interview Coach", page_icon="🧠", layout="wide")
    resume_prep_page()
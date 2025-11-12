"""
Resume Preparation Page - AI-Powered Resume & Interview Coach (PDF + TXT Supported)
"""

import streamlit as st
import sys
from pathlib import Path

# === Add project root to import path ===
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "src" / "coaches"))

from resume_coach import run_resume_coach
from interview_coach import run_interview_coach

import PyPDF2


def extract_pdf_text(pdf_file):
    """Extract text from uploaded PDF using PyPDF2."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def resume_prep_page():
    st.title("🧠 Resume & Interview Preparation")
    st.markdown("Use AI to optimize your resume and prepare for interviews.")

    # === Tabs for Resume / Interview ===
    tab1, tab2 = st.tabs(["📄 Resume Optimization", "🎤 Interview Preparation"])

    # ============================================================
    # TAB 1: RESUME OPTIMIZATION
    # ============================================================
    with tab1:
        st.subheader("📄 Resume Optimization Assistant")
        st.markdown("Upload your resume (PDF or TXT) and let AI rewrite it.")

        uploaded_file = st.file_uploader("Upload your resume", type=["txt", "pdf"])

        if uploaded_file:
            data_dir = BASE_DIR / "data"
            data_dir.mkdir(exist_ok=True)
            resume_path = data_dir / "user_resume.txt"

            # TXT
            if uploaded_file.type == "text/plain":
                content = uploaded_file.read().decode("utf-8", errors="ignore")

            # PDF
            elif uploaded_file.type == "application/pdf":
                content = extract_pdf_text(uploaded_file)

            else:
                st.error("❌ Unsupported file type.")
                return

            # Save to TXT
            resume_path.write_text(content, encoding="utf-8")

            st.success(f"✅ Resume uploaded: {uploaded_file.name}")

            # Run Resume Coach
            with st.spinner("🤖 Improving your resume..."):
                try:
                    result = run_resume_coach(resume_path)
                except Exception as e:
                    st.error(f"❌ {e}")
                    return

            st.markdown("### 🧠 Resume Improvement Suggestions")
            st.json(result)

            updated_path = Path(result["updated_resume_path"])
            if updated_path.exists():
                updated_text = updated_path.read_text(encoding="utf-8")

                st.text_area("📄 Updated Resume", updated_text, height=400)

                st.download_button(
                    label="⬇️ Download Updated Resume",
                    data=updated_text,
                    file_name="resume_updated.txt",
                    mime="text/plain"
                )
        else:
            st.info("💡 Upload a `.txt` or `.pdf` resume to begin.")

    # ============================================================
    # TAB 2: INTERVIEW PREPARATION — ONE BUTTON VERSION
    # ============================================================
    with tab2:
        st.subheader("🎤 Interview Preparation Assistant")
        st.markdown("Generate a **complete** interview guide (General + Technical + Skillset + Specialized).")

        if st.button("✨ Generate Full Interview Guide", use_container_width=True):
            with st.spinner("🤖 Generating full interview guide..."):
                try:
                    # unified version → default category = "full"
                    result = run_interview_coach("full")
                except Exception as e:
                    st.error(f"❌ {e}")
                    return

            st.success("✅ Interview Guide Created Successfully!")

            guide_path = Path(result["guide_path"])
            if guide_path.exists():
                guide_text = guide_path.read_text(encoding="utf-8")

                st.text_area("📘 Interview Prep Guide", guide_text, height=420)

                st.download_button(
                    label="⬇️ Download Interview Guide",
                    data=guide_text,
                    file_name="interview_prep_guide.md",
                    mime="text/markdown"
                )
            else:
                st.warning("⚠️ Could not find generated guide file.")
        else:
            st.info("💡 Click the button above to generate the full interview prep guide.")

    st.markdown("---")
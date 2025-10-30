import streamlit as st
import json
from Crew.research_crew import JobResearchCrew
from crewai import LLM

llm = LLM(model="gpt-4.1-mini")

def run(job_title):
    """Run the CrewAI pipeline with the given job title"""
    crew = JobResearchCrew(llm=llm).crew()
    result = crew.kickoff(inputs={"job_title": job_title})
    return result


def info_page():
    """Job Market Research Dashboard with AI-Powered Research"""
    
    st.title("Job Market Research Dashboard")
    
    job_title = st.text_input("Enter a job title or description:", "")
    run_completed = False
    
    if st.button("Run Research Crew"):
        st.write("⏳ Running the crew, please wait...")
        try:
            result = run(job_title)
            st.success("✅ Crew finished running!")
            run_completed = True
        except Exception as e:
            st.error(f"Error running crew: {e}")

    if run_completed:
        json_path = "src/outputs/content/job_market_summary.json"
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            st.warning("No research results found yet.")
            return

        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            st.header("Job Description")
            st.write(data.get("job_overview", "No data available."))

        with col2:
            st.header("Market Trends")
            for trend in data.get("market_insights", []):
                st.markdown(f"- {trend}")

        with col3:
            st.header("Top Hiring Companies")
            for company in data.get("top_hiring_companies", []):
                st.markdown(f"- {company}")

        with col4:
            st.header("Required Skills")
            for skill in data.get("skills_in_demand", []):
                st.markdown(f"- {skill}")

        with col5:
            st.header("Expected Salary")
            for salary in data.get("salary_expectations", []):
                st.markdown(f"- {salary}")

        with col6:
            st.header("Next Steps")
            for step in data.get("next_steps", []):
                st.markdown(f"- {step}")
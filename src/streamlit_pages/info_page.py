import streamlit as st
import json
from Crew.research_crew import JobResearchCrew
from crewai import LLM
from onet_get import search_top_job

llm = LLM(
    model="gpt-4o-mini",   # limit output length
    max_completion_tokens = 1000,
    )

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
            search_top_job(job_title)
            run(job_title)
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





        st.markdown("""
            <style>
                /* Add horizontal padding between Streamlit columns */
                div[data-testid="column"] {
                    padding: 0 0.7rem; /* spacing between columns */
                }

                /* Add vertical spacing between column rows */
                div[data-testid="stHorizontalBlock"] {
                    margin-bottom: 1.8rem !important;
                }

                /* Equal-height info boxes */
                .info-box {
                    background-color: #262731; /* dark background */
                    border: 1px solid #3a3b46;
                    border-radius: 18px;
                    height: 280px;
                    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.4);
                    overflow-y: auto;
                    transition: all 0.2s ease-in-out;
                }

                .info-box:hover {
                    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.6);
                    transform: translateY(-2px);
                }

                /* Sticky header for scrolling */
                .info-header {
                    position: sticky;
                    top: 0;
                    background-color: #2f3040; /* slightly lighter for contrast */
                    border-bottom: 1px solid #3a3b46;
                    padding: 14px 18px;
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #ffffff; /* white text */
                    border-top-left-radius: 18px;
                    border-top-right-radius: 18px;
                    z-index: 2;
                }

                .info-content {
                    padding: 14px 18px 18px 18px;
                    border-bottom-left-radius: 18px;
                    border-bottom-right-radius: 18px;
                    color: #ffffff; /* main content text */
                }

                .info-content p,
                .info-content li {
                    font-size: 0.95rem;
                    color: #e0e0e0; /* soft white text for readability */
                }

                ul {
                    margin-top: 0;
                    padding-left: 1.2rem;
                }
            </style>
        """, unsafe_allow_html=True)


        # --- Helper to render sticky-header boxes ---
        def render_box(title, content_items):
            if isinstance(content_items, list):
                content_html = "".join([f"<li>{item}</li>" for item in content_items]) or "<p>No data available</p>"
                content_html = f"<ul>{content_html}</ul>"
            else:
                content_html = f"<p>{content_items}</p>"
            
            st.markdown(f"""
                <div class="info-box">
                    <div class="info-header">{title}</div>
                    <div class="info-content">{content_html}</div>
                </div>
            """, unsafe_allow_html=True)


        # --- Layout ---
        col1, col2, col3 = st.columns(3, gap="large")
        col4, col5, col6 = st.columns(3, gap="large")

        with col1:
            render_box("Job Description", data.get("job_overview", "No data available."))

        with col2:
            render_box("Market Trends", data.get("market_insights", "No data available"))

        with col3:
            render_box("Top Hiring Companies", data.get("top_hiring_companies", []))

        with col4:
            render_box("Required Skills", data.get("skills_in_demand", []))

        with col5:
            render_box("Expected Salary", data.get("salary_expectations", []))

        with col6:
            render_box("Next Steps", data.get("next_steps", []))
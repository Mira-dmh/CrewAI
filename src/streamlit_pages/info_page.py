import streamlit as st
import json
import os
from src.research import JobResearchCrew, llm
from crewai import LLM

def info_page():
    """Job Market Research Dashboard with AI-Powered Research"""
    
    st.title("💡 Job Market Research Dashboard")
    st.markdown("*Explore job markets and generate new research with AI agents*")
    
    # Add AI research section at the top
    st.markdown("## 🤖 Generate New Research")
    
    with st.form("research_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            research_job_title = st.text_input(
                "Job Title to Research:",
                placeholder="e.g., Data Scientist, Software Engineer, Product Manager",
                help="Enter any job title to generate comprehensive market research"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            research_button = st.form_submit_button("🔍 Research Job Market", use_container_width=True)
        
        if research_button and research_job_title:
            generate_new_research(research_job_title)
        elif research_button and not research_job_title:
            st.error("❌ Please enter a job title to research!")
    
    st.markdown("---")
    
    # Load data from JSON
    json_path = "src/outputs/lead_research_analyst/research_data.json"
    with open(json_path, "r") as f:
        data = json.load(f)

    st.title("Job Market Research Dashboard")

    # Create 2x3 grid
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

# 1. Job Market Overview
with col1:
    st.header("Job Description")
    st.write(data.get("job_description", "No data available."))

# 2. Top Hiring Companies
with col2:
    st.header("Market Trends")
    if data["hiring_trends"]:
        for trend in data["hiring_trends"]:
            st.markdown(f"- {trend}")
    else:
        st.write("No data available.")

# 3. In-Demand Skills & Tools
with col3:
    st.header("Top Hiring Companies")
    if data["top_hiring_companies"]:
        for company in data["top_hiring_companies"]:
            st.markdown(f"- {company}")
    else:
        st.write("No data available.")

# 4. Salary Range & Locations
with col4:
    st.header("Required Skills")
    if data["required_skills"]:
        for skill in data["required_skills"]:
            st.markdown(f"- {skill}")
    else:
        st.write("No data available.")

# 5. Interview Topics / Skill Focus
with col5:
    st.header("Placeholder")
    

# 6. Citations or Source URLs
with col6:
    st.header("Placeholder")
import streamlit as st
import json
import os

def info_page():
    """Job Market Research Dashboard"""
    
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
        st.header("1. Job Market Overview")
        st.write(data.get("job_description", "No data available."))

    # 2. Top Hiring Companies
    with col2:
        st.header("2. Top Hiring Companies")
        companies = data.get("top_hiring_companies", [])
        if companies:
            for company in companies:
                st.markdown(f"- {company}")
        else:
            st.write("No data available.")

    # 3. In-Demand Skills & Tools
    with col3:
        st.header("3. In-Demand Skills & Tools")
        skills = data.get("required_skills", [])
        if skills:
            for skill in skills:
                st.markdown(f"- {skill}")
        else:
            st.write("No data available.")

    # 4. Salary Range & Locations
    with col4:
        st.header("4. Salary Range & Locations")
        salary_info = data.get("salary_insights", "Competitive salaries across major tech hubs")
        st.write(salary_info)

    # 5. Interview Topics / Skill Focus
    with col5:
        st.header("5. Interview Topics / Skill Focus")
        interview_focus = data.get("interview_focus", "System design, algorithms, and behavioral questions")
        st.write(interview_focus)

    # 6. Data Source
    with col6:
        st.header("6. Data Source")
        st.write("**File**: research_data.json")
        st.write("**Format**: JSON")
        st.write("**Source**: Lead Research Analyst")
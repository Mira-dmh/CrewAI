import streamlit as st
import json

# Load data from JSON
DASHBOARD_FILE = "dashboard_data.json"

def load_dashboard(file_path="src/outputs/lead_research_analyst/research_data.json"):
    with open(file_path, "r") as f:
        return json.load(f)

data = load_dashboard()

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
    st.write("hiring_trends", "No data available.")

# 3. In-Demand Skills & Tools
with col3:
    st.header("3. In-Demand Skills & Tools")
    if data["top_hiring_companies"]:
        for company in data["top_hiring_companies"]:
            st.markdown(f"- {company}")
    else:
        st.write("No data available.")

# 4. Salary Range & Locations
with col4:
    st.header("4. Salary Range & Locations")
    if data["required_skills"]:
        for skill in data["required_skills"]:
            st.markdown(f"- {skill}")
    else:
        st.write("No data available.")

# 5. Interview Topics / Skill Focus
with col5:
    st.header("5. Interview Topics / Skill Focus")
    

# 6. Citations or Source URLs
with col6:
    st.header("6. Citations / Source URLs")
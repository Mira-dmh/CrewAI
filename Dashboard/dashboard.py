import streamlit as st
import pandas as pd

# page config
st.set_page_config(page_title="Career Explorer Dashboard", page_icon="💼", layout="wide")

st.title("💼 Career Explorer Dashboard")
st.markdown("Welcome! This dashboard helps you explore job insights and prepare for your next opportunity.")

# Sidebar for navigation
page = st.sidebar.radio(
    "Select Dashboard",
    ["🔍 General Job Info", "🧭 Job Search & Preparation"]
)

# =============================
# 🔍 General Job Info Dashboard
# =============================
if page == "🔍 General Job Info":
    st.header("🔍 General Job Information")

    job_title = st.text_input("Enter a Job Title (e.g., Data Scientist, Product Manager, Software Engineer):")

    if job_title:
        st.write(f"### General Overview for **{job_title}**")

      
        st.write("#### 🌟 Job Summary")
        st.info(f"{job_title}s analyze data, build models, and communicate insights to drive business decisions.")

        st.write("#### 💼 Common Responsibilities")
        st.markdown("""
        - Collect, clean, and analyze large datasets  
        - Develop machine learning models  
        - Visualize results and communicate findings  
        - Collaborate with cross-functional teams  
        """)

        st.write("#### 📊 Typical Skills")
        st.bar_chart(pd.DataFrame({
            "Skill Importance": [90, 80, 75, 65],
        }, index=["Python", "SQL", "Machine Learning", "Communication"]))

        st.write("#### 💰 Average Salary (Estimates)")
        col1, col2, col3 = st.columns(3)
        col1.metric("US", "$120,000 / yr")
        col2.metric("UK", "£65,000 / yr")
        col3.metric("Singapore", "S$90,000 / yr")

# ===================================
# 🧭 Job Search & Preparation Dashboard
# ===================================
elif page == "🧭 Job Search & Preparation":
    st.header("🧭 Job Search & Preparation")

    st.write("You can either explore a **new job role** or find jobs in a **specific location** below:")

    option = st.radio(
        "Choose what you want to explore:",
        ["Find a new job", "Find jobs in a specific location"]
    )

    # ----------------
    # Find a new job
    # ----------------
    if option == "Find a new job":
        new_job = st.text_input("Enter a new job title:")
        if new_job:
            st.success(f"Finding more detailed insights about **{new_job}**...")
            st.markdown(f"""
            ### Insights for {new_job}
            - 🔍 Market demand: High
            - 💡 Required skills: Python, Data Analysis, Communication
            - 🎯 Growth rate: 22% (next 5 years)
            """)

            st.write("#### 🧑‍💼 Resume Tips")
            st.markdown("""
            - Emphasize measurable achievements (e.g., *Improved model accuracy by 15%*)  
            - Tailor each resume to the job description  
            - Use keywords from job postings  
            """)

            st.write("#### 💬 Interview Prep")
            st.markdown("""
            **Sample Questions:**
            1. Tell me about a time you used data to solve a problem.  
            2. What tools or libraries do you prefer for model evaluation?  
            3. How do you handle missing or inconsistent data?  
            """)

    # ----------------
    # Find jobs by location
    # ----------------
    elif option == "Find jobs in a specific location":
        city = st.text_input("Enter City / State / Country:")
        if city:
            st.success(f"Fetching job listings for **{city}**...")

            # Simulate some job results
            job_data = pd.DataFrame({
                "Job Title": ["Data Analyst", "Software Engineer", "AI Researcher"],
                "Company": ["TechCorp", "InnoSoft", "DeepAI"],
                "Location": [city]*3,
                "Salary Range": ["$90k-$110k", "$100k-$130k", "$120k-$160k"]
            })
            st.dataframe(job_data)

            st.write("#### 💬 Interview Preparation")
            st.markdown("""
            - Research local job market trends  
            - Prepare examples using STAR method  
            - Focus on communication and problem-solving skills  
            """)

# =============================
# Footer Information
# =============================
st.sidebar.markdown("---")
st.sidebar.info("Created with ❤️ using Streamlit | Expandable with LangChain & CrewAI for intelligent search.")

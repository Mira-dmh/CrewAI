import streamlit as st
import json
import os

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
    
    # Load existing data from JSON
    st.markdown("## 📊 Current Market Data")
    
    try:
        json_path = "src/outputs/lead_research_analyst/research_data.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
            
            display_market_dashboard(data)
        else:
            st.info("🔍 No market data available yet. Use the research form above to generate your first market analysis!")
            display_sample_dashboard()
            
    except Exception as e:
        st.error(f"❌ Error loading market data: {str(e)}")
        st.info("📝 Displaying sample data instead...")
        display_sample_dashboard()


def generate_new_research(job_title):
    """Generate new market research using CrewAI"""
    
    try:
        # Import CrewAI components
        from crewai import LLM
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from crew import JobResearchCrew
        from dotenv import load_dotenv
        
        load_dotenv()
        
        if not os.getenv("OPENAI_API_KEY"):
            st.warning("⚠️ OpenAI API key not found in environment variables.")
            st.info("💡 Set your OPENAI_API_KEY in the .env file to enable AI research.")
            return
        
        # Initialize LLM and CrewAI
        llm = LLM(model="gpt-4o-mini", temperature=0.7)
        crew_instance = JobResearchCrew(llm=llm)
        crew = crew_instance.crew()
        
        # Execute research
        with st.spinner(f"🤖 AI agents are researching the {job_title} job market..."):
            inputs = {"job_title": job_title}
            result = crew.kickoff(inputs=inputs)
            
            st.success(f"✅ Research complete for {job_title}!")
            st.info("🔄 The dashboard below will update with the new data. You may need to refresh the page.")
            
            # Display the new research results
            with st.expander("📋 View Generated Research", expanded=True):
                st.markdown(f"### 🎯 Research Results for {job_title}")
                st.markdown(str(result))
    
    except ImportError:
        st.error("❌ CrewAI is not available. Please check your installation.")
    except Exception as e:
        st.error(f"❌ Error generating research: {str(e)}")


def display_market_dashboard(data):
    """Display the market research dashboard with real data"""
    
    # Create 2x3 grid
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # 1. Job Description
    with col1:
        st.markdown("### 📝 Job Description")
        job_desc = data.get("job_description", "No data available.")
        st.write(job_desc)

    # 2. Market Trends
    with col2:
        st.markdown("### 📈 Market Trends")
        trends = data.get("hiring_trends", [])
        if trends:
            for trend in trends:
                st.markdown(f"• {trend}")
        else:
            st.write("No trend data available.")

    # 3. Top Hiring Companies
    with col3:
        st.markdown("### 🏢 Top Hiring Companies")
        companies = data.get("top_hiring_companies", [])
        if companies:
            for company in companies:
                st.markdown(f"• {company}")
        else:
            st.write("No company data available.")

    # 4. Required Skills
    with col4:
        st.markdown("### 💡 Required Skills")
        skills = data.get("required_skills", [])
        if skills:
            for skill in skills:
                st.markdown(f"• {skill}")
        else:
            st.write("No skills data available.")

    # 5. Salary Information
    with col5:
        st.markdown("### 💰 Salary Ranges")
        salaries = data.get("average_salaries", [])
        if salaries:
            for salary in salaries:
                st.markdown(f"• {salary}")
        else:
            st.write("No salary data available.")

    # 6. Job Title
    with col6:
        st.markdown("### 🎯 Job Title")
        job_title = data.get("job_title", "Not specified")
        st.write(f"**{job_title}**")
        
        # Add last updated info if available
        st.markdown("---")
        st.markdown("**Data Source**: AI Research Analyst")
        st.markdown("**Format**: JSON")


def display_sample_dashboard():
    """Display sample dashboard when no data is available"""
    
    # Create 2x3 grid with sample data
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.markdown("### 📝 Job Description")
        st.info("Generate research above to see real job descriptions and market analysis.")

    with col2:
        st.markdown("### 📈 Market Trends")
        st.info("Market trends will appear here after generating research.")

    with col3:
        st.markdown("### 🏢 Top Hiring Companies")
        st.info("Top hiring companies will be listed here after research.")

    with col4:
        st.markdown("### 💡 Required Skills")
        st.info("Key skills and requirements will be shown here.")

    with col5:
        st.markdown("### 💰 Salary Ranges")
        st.info("Salary information will be displayed here after research.")

    with col6:
        st.markdown("### 🎯 Research Status")
        st.warning("No data available")
        st.markdown("Use the research form above to generate your first market analysis!")
"""
Specific Jobs Page - Targeted Job Search Functionality with CrewAI Integration
"""

import streamlit as st
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import CrewAI components
try:
    from crewai import LLM
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from crew import JobResearchCrew
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

def specific_jobs_page():
    """Targeted job search functionality"""
    st.markdown("## 🎯 Specific Jobs Search")
    
    st.markdown("### Find Targeted Job Listings")
    st.markdown("This page will help you search for specific job positions based on your criteria.")
    
    # Job search form
    with st.form("job_search_form"):
        st.markdown("**Search Parameters:**")
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title/Position", placeholder="e.g., Software Engineer, Data Scientist")
            location = st.text_input("Location", placeholder="e.g., San Francisco, Remote")
        
        with col2:
            company = st.text_input("Company (optional)", placeholder="e.g., Google, Microsoft")
            experience = st.selectbox("Experience Level", ["Any", "Entry Level", "Mid Level", "Senior Level", "Executive"])
        
        # Additional filters
        st.markdown("**Additional Filters:**")
        col3, col4 = st.columns(2)
        
        with col3:
            job_type = st.selectbox("Job Type", ["Any", "Full-time", "Part-time", "Contract", "Freelance"])
            salary_range = st.selectbox("Salary Range", ["Any", "$50k-$75k", "$75k-$100k", "$100k-$150k", "$150k+"])
        
        with col4:
            remote_option = st.selectbox("Remote Work", ["Any", "Remote", "Hybrid", "On-site"])
            industry = st.selectbox("Industry", ["Any", "Technology", "Finance", "Healthcare", "Marketing", "Education"])
        
        submit = st.form_submit_button("🔍 Search Jobs", use_container_width=True)
        
        if submit:
            if not job_title:
                st.error("❌ Please enter a job title to search!")
                return
            
            # Show search summary
            search_summary = []
            if job_title:
                search_summary.append(f"**Position**: {job_title}")
            if location:
                search_summary.append(f"**Location**: {location}")
            if company:
                search_summary.append(f"**Company**: {company}")
            if experience != "Any":
                search_summary.append(f"**Experience**: {experience}")
            if job_type != "Any":
                search_summary.append(f"**Type**: {job_type}")
            if remote_option != "Any":
                search_summary.append(f"**Remote**: {remote_option}")
            
            if search_summary:
                st.markdown("**Your search criteria:**")
                for item in search_summary:
                    st.markdown(f"- {item}")
                st.markdown("---")
            
            # Process search with CrewAI
            if CREWAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                process_search_with_crewai(job_title, location, company, experience, job_type, remote_option, industry, salary_range)
            else:
                st.warning("⚠️ CrewAI is not available or OpenAI API key is not set.")
                st.info("💡 To enable AI-powered search: Set your OpenAI API key in the .env file")
                display_mock_search_results(job_title, location)
    
    # Additional features section
    st.markdown("---")
    st.markdown("### 🛠️ Advanced Features (Coming Soon)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Smart Matching")
        st.markdown("- AI-powered job recommendations")
        st.markdown("- Skills-based matching")
        st.markdown("- Company culture fit")
    
    with col2:
        st.markdown("#### 📊 Market Insights")
        st.markdown("- Salary benchmarking")
        st.markdown("- Industry trends")
        st.markdown("- Competition analysis")
    
    with col3:
        st.markdown("#### 🚀 Application Tracking")
        st.markdown("- Application status")
        st.markdown("- Interview scheduling")
        st.markdown("- Follow-up reminders")
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: Enter detailed search criteria above for AI-powered job discovery!")


def process_search_with_crewai(job_title, location, company, experience, job_type, remote_option, industry, salary_range):
    """Process job search using CrewAI agents and tasks"""
    
    try:
        # Initialize LLM
        llm = LLM(model="gpt-4o-mini", temperature=0.7)
        
        # Create CrewAI instance
        crew_instance = JobResearchCrew(llm=llm)
        crew = crew_instance.crew()
        
        # Prepare search query
        search_query = build_search_query(job_title, location, company, experience, job_type, remote_option, industry, salary_range)
        
        with st.spinner("🤖 AI agents are analyzing your search criteria and finding job opportunities..."):
            # Process inputs for location-based search
            if location:
                inputs = {
                    "job_title": job_title,
                    "location": location
                }
                
                st.info(f"🎯 Searching for {job_title} positions in {location}")
                
                # Execute CrewAI workflow for job scraping
                result = crew.kickoff(inputs=inputs)
                
                # Display results
                display_crewai_results(result, "location_search", job_title, location)
                
            else:
                # If no location specified, do general market research
                inputs = {"job_title": job_title}
                
                st.info(f"🔍 Researching {job_title} market opportunities")
                
                # Execute CrewAI workflow for market research
                result = crew.kickoff(inputs=inputs)
                
                # Display results
                display_crewai_results(result, "job_research", job_title, None)
        
    except Exception as e:
        st.error(f"❌ Error processing search: {str(e)}")
        st.info("💡 Falling back to mock results...")
        display_mock_search_results(job_title, location)


def build_search_query(job_title, location, company, experience, job_type, remote_option, industry, salary_range):
    """Build a comprehensive search query from form inputs"""
    
    query_parts = [job_title]
    
    if location:
        query_parts.append(f"in {location}")
    if company:
        query_parts.append(f"at {company}")
    if experience != "Any":
        query_parts.append(f"{experience.lower()} level")
    if job_type != "Any":
        query_parts.append(f"{job_type.lower()}")
    if remote_option != "Any":
        query_parts.append(f"{remote_option.lower()}")
    if industry != "Any":
        query_parts.append(f"in {industry}")
    if salary_range != "Any":
        query_parts.append(f"salary {salary_range}")
    
    return " ".join(query_parts)


def display_crewai_results(result, search_type, job_title, location):
    """Display results from CrewAI processing"""
    
    st.success("✅ Search Complete!")
    
    if search_type == "location_search":
        st.markdown(f"## 🎯 Job Opportunities for {job_title}")
        if location:
            st.markdown(f"**Location**: {location}")
    else:
        st.markdown(f"## 📊 Market Research for {job_title}")
    
    # Display the AI-generated content
    st.markdown("### 🤖 AI Analysis Results:")
    
    # Convert result to string if it's not already
    result_text = str(result)
    
    # Display in expandable sections
    with st.expander("📋 Detailed Analysis", expanded=True):
        st.markdown(result_text)
    
    # Try to parse and structure the output if it's JSON
    try:
        if result_text.startswith('{') and result_text.endswith('}'):
            result_json = json.loads(result_text)
            
            if search_type == "location_search" and "job_postings" in result_json:
                display_job_postings(result_json["job_postings"])
            elif search_type == "job_research":
                display_market_research(result_json)
                
    except json.JSONDecodeError:
        # If not JSON, display as text
        pass
    
    # Add timestamp
    st.markdown("---")
    st.markdown(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("**Powered by**: CrewAI + OpenAI GPT-4")


def display_job_postings(job_postings):
    """Display formatted job postings"""
    
    st.markdown("### 💼 Found Job Postings:")
    
    if isinstance(job_postings, list) and job_postings:
        for i, job in enumerate(job_postings, 1):
            with st.container():
                st.markdown(f"#### 📋 Job #{i}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Position**: {job.get('job_title', 'N/A')}")
                    st.markdown(f"**Company**: {job.get('company_name', 'N/A')}")
                    st.markdown(f"**Location**: {job.get('location', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Posted**: {job.get('date_posted', 'N/A')}")
                    st.markdown(f"**Type**: {job.get('employment_type', 'N/A')}")
                    
                    if job.get('job_url'):
                        st.link_button("🔗 View Job", job['job_url'])
                
                st.divider()
    else:
        st.info("No specific job postings found, but market analysis is available above.")


def display_market_research(research_data):
    """Display formatted market research data"""
    
    if not isinstance(research_data, dict):
        return
    
    # Display key market insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏢 Top Companies")
        companies = research_data.get("top_hiring_companies", [])
        if companies:
            for company in companies[:5]:  # Show top 5
                st.markdown(f"• {company}")
        else:
            st.info("No company data available")
    
    with col2:
        st.markdown("### 💡 Key Skills")
        skills = research_data.get("required_skills", [])
        if skills:
            for skill in skills[:5]:  # Show top 5
                st.markdown(f"• {skill}")
        else:
            st.info("No skills data available")
    
    with col3:
        st.markdown("### 💰 Salary Info")
        salaries = research_data.get("average_salaries", [])
        if salaries:
            for salary in salaries:
                st.markdown(f"• {salary}")
        else:
            st.info("No salary data available")
    
    # Display trends
    if "hiring_trends" in research_data:
        st.markdown("### 📈 Market Trends")
        trends = research_data["hiring_trends"]
        if trends:
            for trend in trends:
                st.markdown(f"• {trend}")


def display_mock_search_results(job_title, location):
    """Display mock search results when CrewAI is not available"""
    
    st.info("🔧 **Demo Mode**: Showing sample results")
    
    location_text = f" in {location}" if location else ""
    st.markdown(f"## 🎯 Sample Results for {job_title}{location_text}")
    
    # Mock job postings
    mock_jobs = [
        {
            "job_title": f"Senior {job_title}",
            "company_name": "TechCorp Inc.",
            "location": location or "San Francisco, CA",
            "date_posted": "2 days ago",
            "employment_type": "Full-time",
            "salary": "$120,000 - $150,000"
        },
        {
            "job_title": f"{job_title}",
            "company_name": "Innovation Labs",
            "location": location or "New York, NY",
            "date_posted": "1 week ago", 
            "employment_type": "Full-time",
            "salary": "$100,000 - $130,000"
        },
        {
            "job_title": f"Lead {job_title}",
            "company_name": "Future Systems",
            "location": location or "Remote",
            "date_posted": "3 days ago",
            "employment_type": "Full-time",
            "salary": "$140,000 - $170,000"
        }
    ]
    
    st.markdown("### 💼 Sample Job Postings:")
    
    for i, job in enumerate(mock_jobs, 1):
        with st.container():
            st.markdown(f"#### 📋 Sample Job #{i}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Position**: {job['job_title']}")
                st.markdown(f"**Company**: {job['company_name']}")
                st.markdown(f"**Location**: {job['location']}")
            
            with col2:
                st.markdown(f"**Posted**: {job['date_posted']}")
                st.markdown(f"**Type**: {job['employment_type']}")
                st.markdown(f"**Salary**: {job['salary']}")
            
            st.divider()
    
    # Mock LinkedIn search URL
    if location:
        search_url = f"https://linkedin.com/jobs/search?keywords={job_title.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
        st.markdown(f"### 🔍 LinkedIn Search")
        st.link_button("🔗 Search on LinkedIn", search_url)
    
    st.warning("💡 **Note**: These are sample results. Set up your OpenAI API key to get real AI-powered job search results!")
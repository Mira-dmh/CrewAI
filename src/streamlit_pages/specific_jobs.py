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
    from crew import MainCrew
    from Crew.linkedin_search_crew import LinkedInSearchCrew
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
    
    # JSON Results Management Section
    st.markdown("---")
    st.markdown("### 💾 Search Results Management")
    
    if CREWAI_AVAILABLE:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📁 Latest Search Results")
            if st.button("🔄 Load Latest JSON Results", use_container_width=True):
                load_and_display_json_results()
                
            latest_results = LinkedInSearchCrew.load_latest_search_results()
            if latest_results:
                metadata = latest_results.get("search_metadata", {})
                st.success(f"✅ Last search: {metadata.get('job_title', 'N/A')}")
                st.markdown(f"📅 {metadata.get('search_timestamp', 'N/A')}")
            else:
                st.info("No saved results yet")
        
        with col2:
            st.markdown("#### � Search History")
            if st.button("📋 View All Searches", use_container_width=True):
                display_all_search_history()
                
            all_results = LinkedInSearchCrew.get_all_search_results()
            st.info(f"📊 Total searches: {len(all_results)}")
            
            if all_results:
                # Show quick preview of recent searches
                st.markdown("**Recent searches:**")
                for file_path in all_results[:3]:  # Show last 3
                    try:
                        results = LinkedInSearchCrew.load_search_results_by_file(file_path)
                        if results:
                            metadata = results.get("search_metadata", {})
                            job_title = metadata.get("job_title", "Unknown")
                            st.markdown(f"• {job_title}")
                    except:
                        continue
    else:
        st.warning("⚠️ CrewAI not available - Enable to use JSON results management")
    
    # Additional features section  
    st.markdown("---")
    st.markdown("### 🛠️ Advanced Features")
    
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
        st.markdown("#### 🚀 JSON Integration")
        st.markdown("- Auto-save search results")
        st.markdown("- Load previous searches")
        st.markdown("- Export/Import capability")
    
    # Quick Test Section
    st.markdown("---")
    st.markdown("### 🧪 Quick Test: LinkedIn Search Workflow")
    
    if CREWAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        col1, col2 = st.columns(2)
        
        with col1:
            test_job = st.text_input("Test Job Title", value="Software Engineer", key="test_job")
            test_location = st.text_input("Test Location", value="San Francisco", key="test_location")
        
        with col2:
            if st.button("🚀 Run Quick Test", use_container_width=True):
                st.markdown("### 🔄 Testing Complete Workflow:")
                
                # Step 1: Capture input
                st.markdown("**Step 1**: ✅ Captured user input")
                st.json({"job_title": test_job, "location": test_location})
                
                # Step 2: Execute search 
                with st.spinner("**Step 2**: 🤖 Executing LinkedIn search..."):
                    try:
                        llm = LLM(model="gpt-4o-mini", temperature=0.7)
                        linkedin_crew = LinkedInSearchCrew(llm=llm)
                        result = linkedin_crew.search_jobs(test_job, test_location)
                        st.success("**Step 2**: ✅ LinkedIn search completed")
                    except Exception as e:
                        st.error(f"**Step 2**: ❌ Search failed: {e}")
                        result = None
                
                # Step 3: Check JSON save
                if result:
                    st.markdown("**Step 3**: 💾 Checking JSON file save...")
                    latest = LinkedInSearchCrew.load_latest_search_results()
                    if latest:
                        st.success("**Step 3**: ✅ JSON file saved successfully")
                        
                        # Step 4: Display results
                        st.markdown("**Step 4**: 📊 Displaying results from JSON:")
                        metadata = latest.get("search_metadata", {})
                        st.json({
                            "job_title": metadata.get("job_title"),
                            "location": metadata.get("location"), 
                            "timestamp": metadata.get("search_timestamp"),
                            "output_preview": str(latest.get("crew_output", ""))[:200] + "..."
                        })
                        st.success("**Workflow Complete**: ✅ All steps successful!")
                    else:
                        st.error("**Step 3**: ❌ JSON file save failed")
                        
            st.info("💡 This tests the complete capture → search → save → load workflow")
    else:
        st.warning("⚠️ Set up OpenAI API key to test the LinkedIn search workflow")
    
    st.markdown("---")
    st.info("💡 **Pro Tip**: All search results are automatically saved as JSON files for easy access and processing!")


def process_search_with_crewai(job_title, location, company, experience, job_type, remote_option, industry, salary_range):
    """Process job search using specialized LinkedIn CrewAI agents and tasks"""
    
    try:
        # Initialize LLM
        llm = LLM(model="gpt-4o-mini", temperature=0.7)
        
        # Always use specialized LinkedIn search crew for comprehensive search
        linkedin_crew = LinkedInSearchCrew(llm=llm)
        
        # Prepare search parameters
        search_params = {
            "company": company or "",
            "experience_level": experience,
            "job_type": job_type,
            "remote_option": remote_option,
            "industry": industry,
            "salary_range": salary_range
        }
        
        with st.spinner("🤖 LinkedIn AI agents are navigating to LinkedIn and performing your search..."):
            
            # Show search progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Capturing search input...")
            progress_bar.progress(25)
            
            status_text.text(f"🌐 Navigating to LinkedIn for {job_title} search...")
            progress_bar.progress(50)
            
            st.info(f"🎯 Searching LinkedIn for {job_title}" + (f" in {location}" if location else ""))
            
            status_text.text("📊 Analyzing search results...")
            progress_bar.progress(75)
            
            # Execute LinkedIn-specific search with all parameters
            result = linkedin_crew.search_jobs(
                job_title=job_title,
                location=location,
                **search_params
            )
            
            status_text.text("💾 Saving results to JSON file...")
            progress_bar.progress(100)
            
            # Display results with JSON file info
            display_crewai_results_with_json(result, job_title, location, search_params)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
        
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


def display_crewai_results_with_json(result, job_title, location, search_params):
    """Display results from CrewAI processing with JSON file management"""
    
    st.success("✅ LinkedIn Search Complete!")
    
    # Header with search info
    st.markdown(f"## 🎯 LinkedIn Job Search Results for {job_title}")
    if location:
        st.markdown(f"**Location**: {location}")
    st.markdown("**Source**: LinkedIn + AI Analysis")
    
    # JSON File Management Section
    st.markdown("### 💾 Search Results Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**� Latest Results**")
        if st.button("🔄 Load Latest JSON"):
            load_and_display_json_results()
    
    with col2:
        st.markdown("**📂 All Results**")
        if st.button("📋 View All Searches"):
            display_all_search_history()
            
    with col3:
        st.markdown("**💾 JSON Status**")
        # Check if JSON was saved successfully
        latest_results = LinkedInSearchCrew.load_latest_search_results()
        if latest_results:
            st.success("JSON Saved ✅")
        else:
            st.warning("JSON Save Error ⚠️")
    
    # Display the current AI-generated content
    st.markdown("### 🤖 Current Search Results:")
    
    # Convert result to string if it's not already
    result_text = str(result)
    
    # Display in expandable sections
    with st.expander("📋 Detailed Analysis", expanded=True):
        st.markdown(result_text)
    
    # Try to parse and structure the output if it's JSON
    try:
        if result_text.startswith('{') and result_text.endswith('}'):
            result_json = json.loads(result_text)
            
            if "job_postings" in result_json:
                display_job_postings(result_json["job_postings"])
                
    except json.JSONDecodeError:
        # If not JSON, display as text
        pass
    
    # LinkedIn-specific insights
    st.markdown("### 📊 LinkedIn Search Insights")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Search Engine", "LinkedIn")
    with col2:
        st.metric("AI Agent", "LinkedIn Scraper")
    with col3:
        st.metric("Data Source", "Real-time")
    with col4:
        st.metric("JSON Output", "✅ Saved")
    
    # Search parameters summary
    with st.expander("🔍 Search Parameters Used"):
        st.json({
            "job_title": job_title,
            "location": location or "Any",
            **search_params
        })
    
    # Add timestamp and JSON file info
    st.markdown("---")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.markdown(f"**Generated**: {timestamp}")
    st.markdown(f"**JSON File**: `src/outputs/linkedin/latest_search_results.json`")
    st.markdown("**Powered by**: LinkedIn CrewAI + OpenAI GPT-4")


def load_and_display_json_results():
    """Load and display the latest JSON search results"""
    
    latest_results = LinkedInSearchCrew.load_latest_search_results()
    
    if latest_results:
        st.markdown("### � Loaded from JSON File")
        
        # Display metadata
        metadata = latest_results.get("search_metadata", {})
        st.markdown(f"**Job Title**: {metadata.get('job_title', 'N/A')}")
        st.markdown(f"**Location**: {metadata.get('location', 'Any')}")
        st.markdown(f"**Search Time**: {metadata.get('search_timestamp', 'N/A')}")
        
        # Display crew output
        crew_output = latest_results.get("crew_output", "")
        with st.expander("🤖 AI Analysis from JSON", expanded=True):
            st.markdown(str(crew_output))
        
        # Display search parameters
        search_params = metadata.get("search_parameters", {})
        if search_params:
            with st.expander("🔍 Search Parameters from JSON"):
                st.json(search_params)
    else:
        st.error("❌ No JSON results found. Please run a search first.")


def display_all_search_history():
    """Display all available search result files"""
    
    all_results = LinkedInSearchCrew.get_all_search_results()
    
    if all_results:
        st.markdown("### 📚 Search History")
        
        for i, file_path in enumerate(all_results[:10]):  # Show last 10 searches
            # Extract timestamp from filename
            filename = os.path.basename(file_path)
            timestamp = filename.replace("search_results_", "").replace(".json", "")
            
            # Format timestamp for display
            try:
                from datetime import datetime
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                display_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                display_time = timestamp
            
            # Load and display basic info
            results = LinkedInSearchCrew.load_search_results_by_file(file_path)
            if results:
                metadata = results.get("search_metadata", {})
                job_title = metadata.get("job_title", "Unknown")
                location = metadata.get("location", "Any")
                
                with st.expander(f"🔍 Search #{i+1}: {job_title} - {display_time}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Job**: {job_title}")
                        st.markdown(f"**Location**: {location}")
                    with col2:
                        st.markdown(f"**File**: {filename}")
                        if st.button(f"Load This Search", key=f"load_{i}"):
                            # Display this specific search
                            crew_output = results.get("crew_output", "")
                            st.markdown("### 🤖 Loaded Search Results:")
                            st.markdown(str(crew_output))
    else:
        st.info("📝 No search history found. Run some searches to build your history!")


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
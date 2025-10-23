"""
Dashboard  Helper
Provides easy integration functions for Streamlit dashboard
"""

import streamlit as st
import json
import sys
import os
from typing import Dict, Any, Optional

class MockLLM:
    """Mock LLM for demonstration purposes"""
    def __init__(self, model="mock-gpt-4"):
        self.model = model
    
    def __call__(self, prompt):
        return f"Mock response for: {prompt[:50]}..."

# Simplified Dashboard Integration without external LLM dependencies
class DashboardIntegration:
    """
    Helper class for integrating job search workflow with Streamlit dashboard
    """
    
    def __init__(self, llm=None):
        # Use mock LLM if none provided
        self.llm = llm or MockLLM()
        self.mock_mode = isinstance(self.llm, MockLLM)
        
    def create_input_section(self) -> Dict[str, Any]:
        """
        Create Streamlit input section for job search
        Returns user inputs as dictionary
        """
        st.title("🔍 Job Search Assistant")
        if self.mock_mode:
            st.info("🔧 Running in demonstration mode with mock data")
        
        st.markdown("### Tell us what you're looking for!")
        
        # Create tabs for different search types
        tab1, tab2 = st.tabs(["📊 Job Market Research", "📍 Find Specific Jobs"])
        
        user_inputs = {}
        
        with tab1:
            st.markdown("**Get comprehensive market analysis for any job position**")
            job_title = st.text_input(
                "Enter job position to research:",
                placeholder="e.g., Machine Learning Engineer, Product Manager, Data Scientist",
                key="job_research_input"
            )
            
            if st.button("🔍 Research Job Market", key="research_button"):
                if job_title:
                    user_inputs = {
                        "type": "job_research",
                        "job_title": job_title,
                        "location": None
                    }
                else:
                    st.error("Please enter a job title to research!")
        
        with tab2:
            st.markdown("**Find specific job postings in your preferred location**")
            col1, col2 = st.columns(2)
            
            with col1:
                job_title_loc = st.text_input(
                    "Job Title:",
                    placeholder="e.g., Software Engineer",
                    key="job_title_location"
                )
            
            with col2:
                location = st.text_input(
                    "Location:",
                    placeholder="e.g., San Francisco, CA",
                    key="location_input"
                )
            
            if st.button("🎯 Find Jobs", key="location_search_button"):
                if job_title_loc and location:
                    user_inputs = {
                        "type": "location_search", 
                        "job_title": job_title_loc,
                        "location": location
                    }
                elif not job_title_loc:
                    st.error("Please enter a job title!")
                elif not location:
                    st.error("Please enter a location!")
        
        return user_inputs
    
    def process_user_request(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user request and return mock results
        """
        if not user_inputs:
            return {}
            
        try:
            with st.spinner("🤖 Processing your request..."):
                if user_inputs["type"] == "job_research":
                    result = self._generate_mock_job_research(user_inputs["job_title"])
                elif user_inputs["type"] == "location_search":
                    result = self._generate_mock_location_search(
                        user_inputs["job_title"],
                        user_inputs["location"]
                    )
                else:
                    result = {"error": "Unknown request type"}
                    
            return result
            
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
    
    def _generate_mock_job_research(self, job_title: str) -> Dict[str, Any]:
        """Generate mock job research data"""
        return {
            "workflow_type": "job_research",
            "input_analysis": {
                "request_type": "job_research",
                "job_title": job_title,
                "location": "",
                "keywords": job_title.split(),
                "routing_recommendation": "lead_research_analyst",
                "processed_query": job_title
            },
            "research_data": json.dumps({
                "job_description": f"A {job_title} is responsible for analyzing data, implementing solutions, and collaborating with cross-functional teams.",
                "hiring_trends": [
                    "High demand in tech sector",
                    "Remote work opportunities increasing",
                    "Focus on AI/ML skills growing"
                ],
                "top_hiring_companies": ["Google", "Microsoft", "Apple", "Amazon", "Meta"],
                "required_skills": ["Python", "SQL", "Communication", "Problem-solving"],
                "average_salaries": ["Entry: $85k-110k", "Mid: $110k-140k", "Senior: $140k-180k+"]
            }),
            "formatted_content": f"""
## 📊 Market Analysis for {job_title}

### 🌟 Job Overview
A {job_title} plays a crucial role in modern organizations by leveraging technical skills to drive business outcomes.

### 📈 Market Trends
- **High Demand**: Strong growth expected in the coming years
- **Remote Opportunities**: 70% of positions offer remote/hybrid options
- **Skill Evolution**: Emphasis on AI/ML and data-driven decision making

### 🏢 Top Hiring Companies
- Google
- Microsoft  
- Apple
- Amazon
- Meta

### 💡 Key Skills in Demand
- Python programming
- SQL and database management
- Strong communication skills
- Problem-solving abilities

### 💰 Salary Expectations
- **Entry Level**: $85,000 - $110,000
- **Mid Level**: $110,000 - $140,000  
- **Senior Level**: $140,000 - $180,000+
            """,
            "verification": "✅ All information has been verified through multiple sources.",
            "output_files": {
                "research": "mock_research_data.json",
                "content": "mock_job_market_summary.md",
                "verification": "mock_verification_report.md"
            }
        }
    
    def _generate_mock_location_search(self, job_title: str, location: str) -> Dict[str, Any]:
        """Generate mock location search data"""
        return {
            "workflow_type": "location_search",
            "input_analysis": {
                "request_type": "location_search",
                "job_title": job_title,
                "location": location,
                "keywords": [job_title, location],
                "routing_recommendation": "linkedin_scraper",
                "processed_query": f"{job_title} in {location}"
            },
            "job_postings": f"""
## 🎯 Found Job Opportunities for {job_title} in {location}

### 📋 Job Listing 1
- **Job Title**: Senior {job_title}
- **Company**: TechCorp Inc.
- **Location**: {location}
- **Date Posted**: 2 days ago
- **Salary**: $120,000 - $150,000
- **Direct Link**: [View Job](https://example.com/job1)

### 📋 Job Listing 2  
- **Job Title**: {job_title}
- **Company**: Innovation Labs
- **Location**: {location}
- **Date Posted**: 1 week ago
- **Salary**: $100,000 - $130,000
- **Direct Link**: [View Job](https://example.com/job2)

### 📋 Job Listing 3
- **Job Title**: Lead {job_title}
- **Company**: Future Systems
- **Location**: {location}
- **Date Posted**: 3 days ago
- **Salary**: $140,000 - $170,000
- **Direct Link**: [View Job](https://example.com/job3)

### 🔍 LinkedIn Search URL
[LinkedIn Jobs Search for {job_title} in {location}](https://linkedin.com/jobs/search?keywords={job_title.replace(' ', '%20')}&location={location.replace(' ', '%20')})
            """,
            "verification": f"✅ Found 3 active job postings for {job_title} in {location}. All links verified as of today.",
            "output_files": {
                "job_postings": "mock_job_postings.md",
                "verification": "mock_verification_report.md"
            }
        }
        
    def create_input_section(self) -> Dict[str, Any]:
        """
        Create Streamlit input section for job search
        Returns user inputs as dictionary
        """
        st.title("🔍 CrewAI Job Search Assistant")
        st.markdown("### Tell us what you're looking for!")
        
        # Create tabs for different search types
        tab1, tab2 = st.tabs(["📊 Job Market Research", "📍 Find Specific Jobs"])
        
        user_inputs = {}
        
        with tab1:
            st.markdown("**Get comprehensive market analysis for any job position**")
            job_title = st.text_input(
                "Enter job position to research:",
                placeholder="e.g., Machine Learning Engineer, Product Manager, Data Scientist",
                key="job_research_input"
            )
            
            if st.button("🔍 Research Job Market", key="research_button"):
                if job_title:
                    user_inputs = {
                        "type": "job_research",
                        "job_title": job_title,
                        "location": None
                    }
                else:
                    st.error("Please enter a job title to research!")
        
        with tab2:
            st.markdown("**Find specific job postings in your preferred location**")
            col1, col2 = st.columns(2)
            
            with col1:
                job_title_loc = st.text_input(
                    "Job Title:",
                    placeholder="e.g., Software Engineer",
                    key="job_title_location"
                )
            
            with col2:
                location = st.text_input(
                    "Location:",
                    placeholder="e.g., San Francisco, CA",
                    key="location_input"
                )
            
            if st.button("🎯 Find Jobs", key="location_search_button"):
                if job_title_loc and location:
                    user_inputs = {
                        "type": "location_search", 
                        "job_title": job_title_loc,
                        "location": location
                    }
                elif not job_title_loc:
                    st.error("Please enter a job title!")
                elif not location:
                    st.error("Please enter a location!")
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """
        Display results in Streamlit dashboard
        """
        if not results:
            return
            
        if "error" in results:
            st.error(f"❌ Error: {results['error']}")
            return
        
        workflow_type = results.get("workflow_type", "unknown")
        
        if workflow_type == "job_research":
            self._display_job_research_results(results)
        elif workflow_type == "location_search":
            self._display_location_search_results(results)
        else:
            st.warning("Unknown workflow type in results")
    
    def _display_job_research_results(self, results: Dict[str, Any]) -> None:
        """
        Display job research workflow results
        """
        st.success("✅ Job Market Research Complete!")
        
        # Display input analysis
        input_analysis = results.get("input_analysis", {})
        if input_analysis:
            with st.expander("📝 Input Analysis"):
                st.json(input_analysis)
        
        # Display formatted content
        formatted_content = results.get("formatted_content", "")
        if formatted_content:
            st.markdown(formatted_content)
        
        # Display raw research data
        research_data = results.get("research_data", "")
        if research_data:
            with st.expander("🔍 Detailed Research Data"):
                try:
                    research_json = json.loads(research_data)
                    st.json(research_json)
                except json.JSONDecodeError:
                    st.text(research_data)
        
        # Display verification results
        verification = results.get("verification", "")
        if verification:
            with st.expander("✅ Verification Report"):
                st.markdown(verification)
        
        # Display output file info
        output_files = results.get("output_files", {})
        if output_files:
            with st.expander("📁 Generated Files"):
                for file_type, file_path in output_files.items():
                    st.text(f"{file_type}: {file_path}")
    
    def _display_location_search_results(self, results: Dict[str, Any]) -> None:
        """
        Display location search workflow results
        """
        st.success("✅ Job Search Complete!")
        
        # Display input analysis
        input_analysis = results.get("input_analysis", {})
        if input_analysis:
            with st.expander("📝 Search Parameters"):
                st.json(input_analysis)
        
        # Display job postings
        job_postings = results.get("job_postings", "")
        if job_postings:
            st.markdown(job_postings)
        
        # Display verification results
        verification = results.get("verification", "")
        if verification:
            with st.expander("✅ Verification Report"):
                st.markdown(verification)
        
        # Display output file info
        output_files = results.get("output_files", {})
        if output_files:
            with st.expander("📁 Generated Files"):
                for file_type, file_path in output_files.items():
                    st.text(f"{file_type}: {file_path}")
    
    def display_workflow_status(self) -> None:
        """
        Display current workflow status in sidebar
        """
        with st.sidebar:
            st.markdown("## 🤖 System Status")
            
            if self.mock_mode:
                st.warning("🔧 Demo Mode")
                st.markdown("### Mock Agents")
                mock_agents = [
                    "dashboard_input_catcher",
                    "lead_research_analyst", 
                    "agent_content_editor",
                    "linkedin_scraper",
                    "resume_coach",
                    "interview_coach",
                    "verification_specialist"
                ]
                for agent_name in mock_agents:
                    st.text(f"🟡 {agent_name}")
                
                st.markdown("### Mock Workflows")
                st.text("🟡 job_research")
                st.text("🟡 location_search")
            else:
                st.success("✅ Production Mode")
                st.text("🟢 All systems operational")
    
    def create_complete_dashboard(self) -> None:
        """
        Create complete dashboard with all components
        """
        # Display status in sidebar
        self.display_workflow_status()
        
        # Create input section
        user_inputs = self.create_input_section()
        
        # Process request if inputs provided
        if user_inputs:
            results = self.process_user_request(user_inputs)
            self.display_results(results)
        
        # Add instructions
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            **Job Market Research**: Enter any job title to get comprehensive market analysis including:
            - Job description and requirements
            - Current hiring trends  
            - Top hiring companies
            - Required skills and qualifications
            - Salary expectations
            
            **Find Specific Jobs**: Enter a job title and location to get:
            - Direct links to current job postings
            - Company information
            - Job posting details
            - LinkedIn search URLs
            
            *Note: Currently running in demonstration mode with mock data.*
            """)

# Simplified main function without external dependencies
def main():
    """
    Main function for Streamlit app - no external LLM required
    """
    st.set_page_config(
        page_title="Job Search Assistant", 
        page_icon="🔍", 
        layout="wide"
    )
    
    # Create dashboard integration with mock LLM
    dashboard = DashboardIntegration()
    
    # Create complete dashboard
    dashboard.create_complete_dashboard()

if __name__ == "__main__":
    main()
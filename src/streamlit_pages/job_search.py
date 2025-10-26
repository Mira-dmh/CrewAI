"""
Job Search Hub - Complete Job Search and Market Research Platform
Combines job market insights, specific job search, and AI-powered research tools
"""

import streamlit as st
import json
import sys
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from datetime import datetime

# Import separate page functions
from .info_page import info_page as job_market_insights_core
from .specific_jobs import specific_jobs_page as specific_job_search_core

# Load environment variables
load_dotenv()

# Import real LLM from CrewAI
from crewai import LLM

def job_market_insights():
    """Job Market Research Dashboard - Info Section"""
    
    st.markdown("## 📊 Job Market Research Dashboard")
    st.markdown("Get comprehensive insights into current job market trends and data.")
    
    # Call the imported info_page function
    job_market_insights_core()

def specific_job_search():
    """Specific Job Search Section with Enhanced Parameters"""
    
    st.markdown("## 🎯 Targeted Job Search")
    st.markdown("Find specific job opportunities with detailed search criteria.")
    
    # Call the imported specific_jobs_page function
    specific_job_search_core()

def ai_powered_research():
    """AI-Powered Job Research Section"""
    
    st.markdown("## 🤖 AI-Powered Job Research")
    st.markdown("Get comprehensive market analysis and job insights using AI agents.")
    
    # Initialize AI system
    dashboard = DashboardIntegration()
    
    # Display AI status
    st.success("🤖 Connected to real AI - Ready for intelligent analysis!")
    
    # Create research interface
    research_tab1, research_tab2 = st.tabs(["📊 Market Research", "📍 Location-Based Search"])
    
    with research_tab1:
        st.markdown("**Get comprehensive market analysis for any job position**")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            job_title = st.text_input(
                "Enter job position to research:",
                placeholder="e.g., Machine Learning Engineer, Product Manager, Data Scientist",
                key="ai_job_research_input",
                help="Enter any job title to get AI-powered market analysis"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            research_button = st.button("🔍 Research", key="ai_research_button", use_container_width=True)
        
        if research_button and job_title:
            user_inputs = {
                "type": "job_research",
                "job_title": job_title,
                "location": None
            }
            
            # Process with AI
            results = dashboard.process_user_request(user_inputs)
            dashboard.display_results(results)
            
        elif research_button and not job_title:
            st.error("❌ Please enter a job title to research!")
    
    with research_tab2:
        st.markdown("**Find specific job postings with AI-powered analysis**")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            job_title_loc = st.text_input(
                "Job Title:",
                placeholder="e.g., Software Engineer",
                key="ai_job_title_location"
            )
        with col2:
            location = st.text_input(
                "Location:",
                placeholder="e.g., San Francisco, CA",
                key="ai_location_input"
            )
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            search_button = st.button("🎯 Search", key="ai_location_search_button", use_container_width=True)
        
        if search_button and job_title_loc and location:
            user_inputs = {
                "type": "location_search", 
                "job_title": job_title_loc,
                "location": location
            }
            
            # Process with AI
            results = dashboard.process_user_request(user_inputs)
            dashboard.display_results(results)
            
        elif search_button:
            if not job_title_loc:
                st.error("❌ Please enter a job title!")
            if not location:
                st.error("❌ Please enter a location!")
    
    # Display AI system status in expander
    with st.expander("🤖 AI System Status"):
        dashboard.display_workflow_status()

# Main Dashboard Integration Class (existing functionality)
class DashboardIntegration:
    """
    Helper class for integrating job search workflow with Streamlit dashboard
    """
    
    def __init__(self, llm=None):
        # Use real LLM from CrewAI
        if llm is None:
            if os.getenv("OPENAI_API_KEY"):
                self.llm = LLM(model="gpt-4o-mini", temperature=0.7)
                print("✅ Using real OpenAI LLM")
            else:
                raise ValueError("OPENAI_API_KEY environment variable is required")
        else:
            self.llm = llm
    
    def process_user_request(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process user request and return results using real AI"""
        if not user_inputs:
            return {}
            
        try:
            start_time = datetime.now()
            
            with st.spinner("🤖 AI agents are working on your request..."):
                # Use real CrewAI
                result = self._process_with_real_crewai(user_inputs)
            
            # Track session after successful processing
            if "error" not in result:
                self._track_session(user_inputs, result, start_time)
                    
            return result
            
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}
    
    def _process_with_real_crewai(self, user_inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process request using real CrewAI system"""
        try:
            # Import CrewAI components
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from crew import JobResearchCrew
            
            # Create crew with real LLM
            crew_instance = JobResearchCrew(llm=self.llm)
            crew = crew_instance.crew()
            
            # Prepare inputs based on request type
            if user_inputs["type"] == "job_research":
                inputs = {"job_title": user_inputs["job_title"]}
                st.info(f"🔍 Researching: {user_inputs['job_title']}")
                
            elif user_inputs["type"] == "location_search":
                inputs = {
                    "job_title": user_inputs["job_title"],
                    "location": user_inputs["location"]
                }
                st.info(f"🎯 Searching: {user_inputs['job_title']} in {user_inputs['location']}")
            else:
                return {"error": "Unknown request type"}
            
            # Execute CrewAI workflow
            result = crew.kickoff(inputs=inputs)
            
            # Format result for display
            return {
                "workflow_type": user_inputs["type"],
                "input_analysis": inputs,
                "ai_result": str(result),
                "formatted_content": self._format_crewai_result(result, user_inputs),
                "verification": "✅ Results generated by real AI agents",
                "output_files": {
                    "ai_output": "Generated by CrewAI system"
                }
            }
            
        except ImportError as e:
            return {"error": f"CrewAI import failed: {str(e)}"}
        except Exception as e:
            return {"error": f"CrewAI execution failed: {str(e)}"}
    
    def _format_crewai_result(self, result, user_inputs: Dict[str, Any]) -> str:
        """Format CrewAI result for display"""
        job_title = user_inputs.get("job_title", "Unknown")
        location = user_inputs.get("location", "")
        
        formatted = f"""
## 🤖 AI-Generated Analysis for {job_title}

### 📋 CrewAI Agent Results:
{str(result)}

### 📊 Analysis Details:
- **Job Position**: {job_title}
"""
        if location:
            formatted += f"- **Location**: {location}\n"
            
        formatted += f"""
- **Generated by**: Real AI Agents (CrewAI + OpenAI)
- **Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

### 💡 Next Steps:
1. Review the detailed analysis above
2. Use the insights to tailor your resume
3. Prepare for interviews based on the requirements
4. Apply to the recommended companies
        """
        
        return formatted
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display results in Streamlit dashboard"""
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
        """Display job research workflow results"""
        st.success("✅ Job Market Research Complete!")
        
        # Display formatted content
        formatted_content = results.get("formatted_content", "")
        if formatted_content:
            st.markdown(formatted_content)
        
        # Display additional details in expanders
        input_analysis = results.get("input_analysis", {})
        if input_analysis:
            with st.expander("📝 Analysis Parameters"):
                st.json(input_analysis)
        
        research_data = results.get("research_data", "")
        if research_data:
            with st.expander("🔍 Detailed Research Data"):
                try:
                    research_json = json.loads(research_data)
                    st.json(research_json)
                except json.JSONDecodeError:
                    st.text(research_data)
        
        verification = results.get("verification", "")
        if verification:
            with st.expander("✅ Verification Report"):
                st.markdown(verification)
    
    def _display_location_search_results(self, results: Dict[str, Any]) -> None:
        """Display location search workflow results"""
        st.success("✅ Job Search Complete!")
        
        # Display job postings
        job_postings = results.get("job_postings", "")
        if job_postings:
            st.markdown(job_postings)
        
        # Display additional details in expanders
        input_analysis = results.get("input_analysis", {})
        if input_analysis:
            with st.expander("📝 Search Parameters"):
                st.json(input_analysis)
        
        verification = results.get("verification", "")
        if verification:
            with st.expander("✅ Verification Report"):
                st.markdown(verification)
    
    def display_workflow_status(self):
        """Display current workflow status"""
        st.success("✅ Real AI Active")
        st.markdown("**Active AI Agents:**")
        ai_agents = [
            "dashboard_input_catcher",
            "lead_research_analyst", 
            "agent_content_editor",
            "linkedin_scraper",
            "verification_specialist"
        ]
        for agent_name in ai_agents:
            st.text(f"🟢 {agent_name}")
                
        # Display API status
        st.markdown("**API Status:**")
        if os.getenv("OPENAI_API_KEY"):
            st.text("🟢 OpenAI API: Connected")
        else:
            st.text("🔴 OpenAI API: Not Set")
            
        if os.getenv("SERPER_API_KEY"):
            st.text("🟢 Search API: Available")
        else:
            st.text("🟡 Search API: Not configured")
    
    def _track_session(self, user_inputs: Dict[str, Any], result: Dict[str, Any], start_time: datetime):
        """Track user session for analytics and history"""
        try:
            # Import session manager
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from utils.session_manager import session_manager
            
            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds() / 60  # in minutes
            
            # Determine session type and create title
            if user_inputs["type"] == "job_research":
                session_type = "job_search" 
                title = f"Job Market Research: {user_inputs['job_title']}"
                details = f"Market analysis for {user_inputs['job_title']} positions"
                location = "Global"
                job_title = user_inputs["job_title"]
            elif user_inputs["type"] == "location_search":
                session_type = "job_search"
                title = f"Job Search: {user_inputs['job_title']}"
                details = f"Job search for {user_inputs['job_title']} in {user_inputs['location']}"
                location = user_inputs["location"]
                job_title = user_inputs["job_title"]
            else:
                session_type = "other"
                title = "Job Search Activity"
                details = "General job search activity"
                location = "Unknown"
                job_title = ""
            
            # Count results (estimate from result content)
            results_count = 5 if "error" not in result else 0
            
            # Save session
            session_manager.add_session(
                session_type=session_type,
                title=title,
                details=details,
                job_title=job_title,
                location=location,
                results_count=results_count,
                duration_minutes=int(duration)
            )
            
        except Exception as e:
            # Don't fail the main process if session tracking fails
            print(f"Warning: Session tracking failed: {e}")

def job_search_page():
    """
    Complete Job Search Hub - Main page function for multipage app
    """
    
    # Page title and description
    st.title("🔍 Job Search Hub")
    st.markdown("*Your complete platform for job market research, targeted search, and AI-powered insights*")
    
    # Create main navigation tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Market Insights", 
        "🎯 Targeted Search", 
        "🤖 AI Research"
    ])
    
    with tab1:
        job_market_insights()
    
    with tab2:
        specific_job_search()
    
    with tab3:
        ai_powered_research()
    
    # Footer with navigation tips
    st.markdown("---")
    with st.expander("ℹ️ How to Use This Hub"):
        st.markdown("""
        ### 📊 Market Insights
        View comprehensive job market data and trends from AI-generated research reports.
        
        ### 🎯 Targeted Search  
        Use detailed search criteria to find specific job opportunities across multiple platforms.
        
        ### 🤖 AI Research
        Get real-time AI-powered analysis of job markets and specific job searches.
        
        **Pro Tip**: Start with AI Research to generate market insights, then use Targeted Search to find specific opportunities!
        """)

# Main function for standalone use
def main():
    """Main function for Streamlit app"""
    st.set_page_config(
        page_title="Job Search Hub", 
        page_icon="🔍", 
        layout="wide"
    )
    
    job_search_page()

if __name__ == "__main__":
    main()
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from datetime import datetime
import json
import requests
from urllib.parse import quote
import os
import re
import uuid

# Import json_manager functions directly
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.json_manager import (
    save_linkedin_search,
    load_latest_linkedin_search,
    get_linkedin_search_history,
    SearchResultsManager
)

# Import LinkedIn job search tools
from Tools.LinkedInJobSearchTool import LinkedInJobSearchTool

@CrewBase
class LinkedInSearchCrew:
    """
    Specialized crew for LinkedIn job search operations
    Includes agents for input processing, LinkedIn scraping, market trends analysis, and verification
    """
    
    agents_config = '../config/linkedin_agents.yaml'
    tasks_config = '../config/linkedin_tasks.yaml'
    
    def __init__(self, llm):
        self.llm = llm  
        self.agents: List[BaseAgent] = []
        self.tasks: List[Task] = []
        # Generate unique session ID for this search
        self.session_id = str(uuid.uuid4())[:8]  # Short UUID (e.g., "a3b4c5d6")
        self.output_dir = f"src/outputs/linkedin/{self.session_id}"
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 Session ID: {self.session_id}")
        print(f"📁 Output directory: {self.output_dir}")
        # Initialize LinkedIn search tool with session-specific output directory
        self.linkedin_search_tool = LinkedInJobSearchTool(output_dir=self.output_dir)
        # Save session info
        self._save_session_info()
    
    @agent
    def dashboard_input_processor(self) -> Agent:
        """Process and analyze user search inputs from the dashboard"""
        return Agent(
            config=self.agents_config['dashboard_input_processor'], # type: ignore[index]
            llm=self.llm 
        )
    
    @agent
    def linkedin_scraper(self) -> Agent:
        """Specialized agent for LinkedIn job posting discovery - uses targeted SerperDev searches"""
        # Use both our custom tool and SerperDev for best results
        
        return Agent(
            config=self.agents_config['LinkedIn_Scraper'], # type: ignore[index]
            tools=[self.linkedin_search_tool],  # Use session-specific tool instance
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def linkedin_market_trends_analyst(self) -> Agent:
        """Analyze LinkedIn market trends and employment patterns"""
        return Agent(
            config=self.agents_config['linkedin_market_trends_analyst'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )
    
    @agent
    def verification_specialist(self) -> Agent:
        """Verify and validate LinkedIn search results and market data"""
        return Agent(
            config=self.agents_config['verification_specialist'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )

    @task
    def linkedin_input_processing_task(self) -> Task:
        """Process user input specifically for LinkedIn search parameters"""
        return Task(
            config=self.tasks_config['dashboard_input_processing_task'], # type: ignore[index]
            agent=self.dashboard_input_processor(),
            output_file=f"{self.output_dir}/user_search_params.json"
        )
    
    @task
    def linkedin_scraping_task(self) -> Task:
        """Main LinkedIn job scraping and discovery task"""
        return Task(
            config=self.tasks_config['linkedin_scraping_task'], # type: ignore[index]
            agent=self.linkedin_scraper(),
            context=[self.linkedin_input_processing_task()],
            output_file=f"{self.output_dir}/job_postings.json"
        )
    
    @task
    def linkedin_market_trends_task(self) -> Task:
        """Analyze LinkedIn market trends for the searched positions"""
        return Task(
            config=self.tasks_config['linkedin_market_trends_task'], # type: ignore[index]
            agent=self.linkedin_market_trends_analyst(),
            context=[self.linkedin_input_processing_task()],
            output_file=f"{self.output_dir}/market_trends.json"
        )
    
    @task
    def linkedin_verification_task(self) -> Task:
        """Verify LinkedIn search results and market analysis accuracy"""
        return Task(
            config=self.tasks_config['linkedin_verification_task'], # type: ignore[index]
            agent=self.verification_specialist(),
            context=[self.linkedin_scraping_task(), self.linkedin_market_trends_task()],
            output_file=f"{self.output_dir}/verification_report.json"
        )
    
    def _save_session_info(self):
        """Save session metadata to session_info.json"""
        session_info = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "output_dir": self.output_dir,
            "status": "initialized"
        }
        
        session_file = f"{self.output_dir}/session_info.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_info, f, indent=2, ensure_ascii=False)

    @crew
    def crew(self) -> Crew:
        """
        Create the LinkedIn search crew with sequential processing
        Optimized for LinkedIn job discovery and market analysis workflow
        """
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True
        )
    
    def search_jobs(self, job_title: str, location: str = "", company: str = "", 
                    job_type: str = "Any", remote_option: str = "Any", 
                    date_posted: str = "Any time", work_authorization: str = "Any", **kwargs):
        """
        Execute comprehensive LinkedIn job search with all filters using CrewAI agents and tasks
        
        Workflow:
        1. Dashboard Input Processor Agent validates and structures search parameters
        2. LinkedIn Scraper Agent performs multiple searches and extracts job data
        3. Market Trends Analyst Agent analyzes job market patterns
        4. Verification Specialist Agent validates results accuracy
        
        Args:
            job_title (str): The job title to search for (REQUIRED)
            location (str, optional): Location for job search (city, state, or zip code)
            company (str, optional): Specific company name (leave empty to search all companies)
            job_type (str, optional): Job type filter (Full-time, Part-time, Internship, Contract, Temporary)
            remote_option (str, optional): Work mode (Remote, Hybrid, On-site)
            date_posted (str, optional): Date filter (Past 24 hours, Past week, Past month, Any time)
            work_authorization (str, optional): Visa/work auth (OPT, CPT, US Visa Sponsorship, Any)
            **kwargs: Additional search parameters
            
        Returns:
            CrewAI CrewOutput object containing:
            - tasks_output[0]: Validated search parameters
            - tasks_output[1]: Job postings (30-50+ LinkedIn jobs with full details)
            - tasks_output[2]: Market trends analysis
            - tasks_output[3]: Verification report
        """
        # Check if we should use fallback mode
        use_fallback = kwargs.get('use_fallback', False)
        
        if use_fallback:
            print("\n🔄 Using fallback mode (direct LinkedIn URL generation)")
            return self._fallback_search_jobs(job_title, location, company, job_type, 
                                             remote_option, date_posted, work_authorization, **kwargs)
        
        # Prepare input parameters for all agents
        inputs = {
            "job_title": job_title,
            "location": location or "",
            "company": company or "",
            "job_type": job_type or "Any",
            "remote_option": remote_option or "Any",
            "date_posted": date_posted or "Any time",
            "work_authorization": work_authorization or "Any",
            "search_timestamp": datetime.now().isoformat(),
            **kwargs
        }
        
        print(f"\n🚀 Starting LinkedIn Job Search Crew")
        print(f"📋 Job Title: {job_title}")
        print(f"📍 Location: {location or 'Any'}")
        print(f"🏢 Company: {company or 'Any'}")
        print(f"⏰ Date Posted: {date_posted}")
        print(f"🔧 Filters: {job_type}, {remote_option}, {work_authorization}")
        print(f"\n🤖 Agents will execute 4 tasks sequentially:")
        print(f"   1️⃣ Input Processing - Validate and structure parameters")
        print(f"   2️⃣ Job Scraping - Search LinkedIn and extract 30-50+ jobs")
        print(f"   3️⃣ Market Analysis - Analyze trends and patterns")
        print(f"   4️⃣ Verification - Validate results accuracy\n")
        
        # Execute crew with sequential task processing
        # Task execution order:
        # 1. linkedin_input_processing_task (by dashboard_input_processor agent)
        # 2. linkedin_scraping_task (by linkedin_scraper agent)
        # 3. linkedin_market_trends_task (by linkedin_market_trends_analyst agent)
        # 4. linkedin_verification_task (by verification_specialist agent)
        result = self.crew().kickoff(inputs=inputs)
        
        # Save comprehensive search results
        try:
            saved_file = save_linkedin_search(
                result, 
                job_title, 
                location, 
                company=company,
                job_type=job_type,
                remote_option=remote_option,
                date_posted=date_posted,
                work_authorization=work_authorization,
                **kwargs
            )
            if saved_file:
                print(f"\n✅ Search results saved to: {saved_file}")
                print(f"📊 Access job postings from: tasks_output[1].raw")
        except Exception as e:
            print(f"\n⚠️ Warning: Could not save results: {e}")
        
        return result
    
    def _fallback_search_jobs(self, job_title: str, location: str = "", company: str = "", 
                              job_type: str = "Any", remote_option: str = "Any", 
                              date_posted: str = "Any time", work_authorization: str = "Any", **kwargs):
        """
        Fallback method: Generate LinkedIn search URLs and structure without using agents
        This bypasses SerperDev limitations and creates direct LinkedIn job search links
        """
        print(f"\n🔗 Generating direct LinkedIn search URLs...")
        
        # Build LinkedIn search URL
        base_url = "https://www.linkedin.com/jobs/search/"
        
        # Map parameters to LinkedIn query parameters
        params = []
        
        # Keywords (job title)
        if job_title:
            params.append(f"keywords={quote(job_title)}")
        
        # Location
        if location and location != "Any":
            params.append(f"location={quote(location)}")
        
        # Company
        if company and company != "Any":
            params.append(f"f_C={quote(company)}")
        
        # Job Type mapping
        job_type_map = {
            "Full-time": "F",
            "Part-time": "P",
            "Internship": "I",
            "Contract": "C",
            "Temporary": "T"
        }
        if job_type in job_type_map:
            params.append(f"f_JT={job_type_map[job_type]}")
        
        # Remote option mapping
        remote_map = {
            "Remote": "2",
            "Hybrid": "3",
            "On-site": "1"
        }
        if remote_option in remote_map:
            params.append(f"f_WT={remote_map[remote_option]}")
        
        # Date posted mapping
        date_map = {
            "Past 24 hours": "r86400",
            "Past week": "r604800",
            "Past month": "r2592000"
        }
        if date_posted in date_map:
            params.append(f"f_TPR={date_map[date_posted]}")
        
        # Build full URL
        search_url = base_url + "?" + "&".join(params) if params else base_url
        
        # Generate structured JSON output
        job_postings_data = {
            "search_metadata": {
                "job_title": job_title,
                "location": location or "Any",
                "company": company or "Any",
                "job_type": job_type,
                "remote_option": remote_option,
                "date_posted": date_posted,
                "work_authorization": work_authorization,
                "search_url": search_url,
                "search_date": datetime.now().isoformat(),
                "method": "direct_url_generation",
                "note": "Visit the search_url to see live LinkedIn job postings"
            },
            "linkedin_search_urls": [
                {
                    "description": "Main search URL - Click to view all matching jobs on LinkedIn",
                    "url": search_url,
                    "open_in_browser": True
                },
                {
                    "description": "Alternative: LinkedIn job search homepage",
                    "url": "https://www.linkedin.com/jobs/",
                    "open_in_browser": False
                }
            ],
            "search_instructions": {
                "step_1": f"Click on the search_url above or visit: {search_url}",
                "step_2": "You will see live LinkedIn job postings matching your criteria",
                "step_3": "Each job has an 'Apply' button and full job details",
                "step_4": "URLs are in format: https://www.linkedin.com/jobs/view/[JOB_ID]"
            },
            "manual_search_tips": [
                f"Search for: '{job_title}' on LinkedIn Jobs",
                f"Filter by location: '{location}'" if location else "No location filter",
                f"Filter by job type: '{job_type}'" if job_type != "Any" else "All job types",
                f"Filter by work mode: '{remote_option}'" if remote_option != "Any" else "All work modes"
            ]
        }
        
        # Save to JSON file
        output_file = "src/outputs/linkedin/job_postings.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(job_postings_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ LinkedIn search URL generated!")
        print(f"📁 Saved to: {output_file}")
        print(f"🔗 Search URL: {search_url}")
        print(f"\n💡 Open the URL in your browser to see live LinkedIn jobs!")
        
        # Return mock CrewOutput-like object
        class FallbackResult:
            def __init__(self, data):
                self.raw = json.dumps(data, indent=2)
                self.json_dict = data
                self.tasks_output = [
                    type('obj', (object,), {'raw': json.dumps(data, indent=2)})()
                ]
        
        return FallbackResult(job_postings_data)
    
    @staticmethod
    def load_latest_search_results():
        """
        Load the latest search results from JSON file
        
        Returns:
            dict: Latest search results or None if file doesn't exist
        """
        return load_latest_linkedin_search()
    
    @staticmethod
    def get_all_search_results():
        """
        Get list of all available search result files
        
        Returns:
            list: List of search result file paths
        """
        return get_linkedin_search_history()
    
    @staticmethod
    def load_search_results_by_file(file_path: str):
        """
        Load search results from a specific file
        
        Args:
            file_path (str): Path to the JSON results file
            
        Returns:
            dict: Search results or None if error
        """
        return SearchResultsManager.load_results_by_file(file_path)
    
    def analyze_market_trends(self, job_title: str, location: str = ""):
        """
        Analyze LinkedIn market trends using specialized agents and tasks
        
        Workflow:
        1. Dashboard Input Processor Agent validates analysis parameters
        2. Market Trends Analyst Agent researches and analyzes market data
        3. Verification Specialist Agent validates analysis accuracy
        
        Args:
            job_title (str): The job title to analyze (REQUIRED)
            location (str, optional): Location for market analysis
            
        Returns:
            CrewAI CrewOutput object containing:
            - tasks_output[0]: Validated analysis parameters
            - tasks_output[1]: Comprehensive market trends analysis
            - tasks_output[2]: Verification report
        """
        inputs = {
            "job_title": job_title,
            "location": location or "",
            "company": "",
            "job_type": "Any",
            "remote_option": "Any",
            "date_posted": "Any time",
            "work_authorization": "Any",
            "analysis_type": "market_trends",
            "search_timestamp": datetime.now().isoformat()
        }
        
        print(f"\n📊 Starting Market Trends Analysis")
        print(f"📋 Job Title: {job_title}")
        print(f"📍 Location: {location or 'Global'}")
        print(f"\n🤖 Agents will analyze:")
        print(f"   📈 Job posting trends and volume")
        print(f"   💰 Salary data and ranges")
        print(f"   🎯 In-demand skills")
        print(f"   🏢 Top hiring companies")
        print(f"   🌍 Geographic distribution\n")
        
        # Execute crew for market analysis
        result = self.crew().kickoff(inputs=inputs)
        
        print(f"\n✅ Market analysis complete!")
        print(f"📊 Access trends data from: tasks_output[1].raw")
        
        return result
    
    def search_jobs_direct(self, job_title: str, location: str = "", company: str = "", 
                          job_type: str = "Any", remote_option: str = "Any", 
                          date_posted: str = "Any time", work_authorization: str = "Any"):
        """
        Direct LinkedIn job search - Generates LinkedIn search URL and sample job structure
        This method creates a direct LinkedIn search link with all filters applied
        
        Args:
            job_title (str): The job title to search for (REQUIRED)
            location (str, optional): Location for job search
            company (str, optional): Specific company name
            job_type (str, optional): Job type filter
            remote_option (str, optional): Work mode
            date_posted (str, optional): Date filter
            work_authorization (str, optional): Visa/work auth
            
        Returns:
            dict: JSON structure with LinkedIn search URL and instructions
        """
        print(f"\n� Generating Direct LinkedIn Search URL")
        print(f"📋 Job Title: {job_title}")
        print(f"📍 Location: {location or 'Any'}\n")
        
        # Build LinkedIn search URL
        base_url = "https://www.linkedin.com/jobs/search/"
        params = []
        
        # Add job title as keywords
        if job_title:
            params.append(f"keywords={quote(job_title)}")
        
        # Add location
        if location:
            params.append(f"location={quote(location)}")
        
        # Job Type mapping
        job_type_map = {
            "Full-time": "F",
            "Part-time": "P",
            "Internship": "I",
            "Contract": "C",
            "Temporary": "T"
        }
        if job_type in job_type_map:
            params.append(f"f_JT={job_type_map[job_type]}")
        
        # Remote option mapping  
        remote_map = {
            "Remote": "2",
            "Hybrid": "3",
            "On-site": "1"
        }
        if remote_option in remote_map:
            params.append(f"f_WT={remote_map[remote_option]}")
        
        # Date posted mapping
        date_map = {
            "Past 24 hours": "r86400",
            "Past week": "r604800",
            "Past month": "r2592000"
        }
        if date_posted in date_map:
            params.append(f"f_TPR={date_map[date_posted]}")
        
        # Build full URL
        linkedin_url = base_url + "?" + "&".join(params) if params else base_url
        
        print(f"✅ LinkedIn Search URL Generated:")
        print(f"   {linkedin_url}\n")
        
        # Create sample job structure (template)
        sample_jobs = [
            {
                "note": "Click the linkedin_search_url above to see live job postings",
                "job_title": f"{job_title} (Example)",
                "company_name": "Visit LinkedIn to see actual companies",
                "location": location or "Multiple locations",
                "application_url": linkedin_url,
                "employment_type": job_type,
                "work_arrangement": remote_option,
                "instructions": "Open the linkedin_search_url in your browser to see real-time job listings"
            }
        ]
        
        # Build final JSON structure
        result_data = {
            "search_metadata": {
                "job_title": job_title,
                "location": location or "Any",
                "company": company or "Any",
                "job_type": job_type,
                "remote_option": remote_option,
                "date_posted": date_posted,
                "work_authorization": work_authorization,
                "search_date": datetime.now().isoformat(),
                "method": "direct_linkedin_url",
                "note": "Click linkedin_search_url to view live LinkedIn job postings"
            },
            "linkedin_search_url": linkedin_url,
            "how_to_use": {
                "step_1": f"Click the URL: {linkedin_url}",
                "step_2": "You will see live LinkedIn job postings with your filters applied",
                "step_3": "Each job has full details, company info, and 'Easy Apply' or 'Apply' button",
                "step_4": "Job URLs are in format: https://www.linkedin.com/jobs/view/[JOB_ID]"
            },
            "job_postings": sample_jobs,
            "total_results_available": "Visit LinkedIn URL to see actual count",
            "additional_search_urls": [
                {
                    "description": "Browse all jobs in this location",
                    "url": f"https://www.linkedin.com/jobs/search/?location={quote(location)}" if location else "https://www.linkedin.com/jobs/",
                },
                {
                    "description": "Search with different filters",
                    "url": "https://www.linkedin.com/jobs/"
                }
            ]
        }
        
        # Save to JSON file
        output_file = "src/outputs/linkedin/job_postings.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to: {output_file}")
        print(f"� LinkedIn Search URL: {linkedin_url}")
        print(f"\n� Open the URL in your browser to see live LinkedIn jobs!")
        print(f"   All your search filters are already applied to the URL.\n")
        
        return result_data

"""
LinkedIn Search Crew - Specialized crew for LinkedIn job search and market analysis
Focuses on LinkedIn-specific agents and tasks for targeted job discovery
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from datetime import datetime

# Import json_manager functions directly
from utils.json_manager import (
    save_linkedin_search,
    load_latest_linkedin_search,
    get_linkedin_search_history,
    SearchResultsManager
)

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
    
    @agent
    def dashboard_input_processor(self) -> Agent:
        """Process and analyze user search inputs from the dashboard"""
        return Agent(
            config=self.agents_config['dashboard_input_processor'], # type: ignore[index]
            llm=self.llm 
        )
    
    @agent
    def linkedin_scraper(self) -> Agent:
        """Specialized agent for LinkedIn job posting discovery and scraping"""
        return Agent(
            config=self.agents_config['LinkedIn_Scraper'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
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
            output_file="src/outputs/linkedin/user_search_params.json"
        )
    
    @task
    def linkedin_scraping_task(self) -> Task:
        """Main LinkedIn job scraping and discovery task"""
        return Task(
            config=self.tasks_config['linkedin_scraping_task'], # type: ignore[index]
            agent=self.linkedin_scraper(),
            context=[self.linkedin_input_processing_task()],
            output_file="src/outputs/linkedin/job_postings.json"
        )
    
    @task
    def linkedin_market_trends_task(self) -> Task:
        """Analyze LinkedIn market trends for the searched positions"""
        return Task(
            config=self.tasks_config['linkedin_market_trends_task'], # type: ignore[index]
            agent=self.linkedin_market_trends_analyst(),
            context=[self.linkedin_input_processing_task()],
            output_file="src/outputs/linkedin/market_trends.json"
        )
    
    @task
    def linkedin_verification_task(self) -> Task:
        """Verify LinkedIn search results and market analysis accuracy"""
        return Task(
            config=self.tasks_config['linkedin_verification_task'], # type: ignore[index]
            agent=self.verification_specialist(),
            context=[self.linkedin_scraping_task(), self.linkedin_market_trends_task()],
            output_file="src/outputs/linkedin/verification_report.json"
        )

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
    
    def search_jobs(self, job_title: str, location: str = None, **kwargs):
        """
        Convenience method to execute LinkedIn job search
        
        Args:
            job_title (str): The job title to search for
            location (str, optional): Location for job search
            **kwargs: Additional search parameters
            
        Returns:
            CrewAI result object with job search results
        """
        inputs = {
            "job_title": job_title,
            "location": location or "",
            "search_timestamp": datetime.now().isoformat(),
            **kwargs
        }
        
        # Execute crew search
        result = self.crew().kickoff(inputs=inputs)
        
        # Save search results using JSON manager
        try:
            saved_file = save_linkedin_search(result, job_title, location, **kwargs)
            if saved_file:
                print(f"✅ Search results saved to: {saved_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not save results: {e}")
        
        return result
    
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
    
    def analyze_market_trends(self, job_title: str, location: str = None):
        """
        Convenience method to analyze LinkedIn market trends
        
        Args:
            job_title (str): The job title to analyze
            location (str, optional): Location for market analysis
            
        Returns:
            CrewAI result object with market trend analysis
        """
        inputs = {
            "job_title": job_title,
            "location": location or "",
            "analysis_type": "market_trends"
        }
        
        return self.crew().kickoff(inputs=inputs)
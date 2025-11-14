from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

class SingleAgentCrew:
    """Single agent that handles all tasks sequentially"""
    
    def __init__(self, llm):
        self.llm = llm
        
    def generalist_agent(self) -> Agent:
        return Agent(
            role='Job Search Generalist',
            goal='Handle all aspects of job search including scraping, analysis, and verification',
            backstory='''You are a versatile job search assistant capable of:
                - Scraping LinkedIn job postings
                - Analyzing market trends
                - Verifying data quality
                - Generating insights''',
            tools=[SerperDevTool()],
            llm=self.llm,
            verbose=True
        )
    
    def comprehensive_search_task(self, job_title: str, location: str) -> Task:
        return Task(
            description=f'''Search for {job_title} jobs in {location}. Complete all steps:
                1. Scrape LinkedIn job postings
                2. Analyze salary trends and skills demand
                3. Verify data quality
                4. Generate comprehensive report''',
            expected_output='Complete job market analysis with postings, trends, and verification',
            agent=self.generalist_agent()
        )
    
    def kickoff(self, job_title: str, location: str):
        crew = Crew(
            agents=[self.generalist_agent()],
            tasks=[self.comprehensive_search_task(job_title, location)],
            verbose=True
        )
        return crew.kickoff()

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class JobResearchCrew:
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    
    def __init__(self, llm):
        self.llm = llm  
        self.agents: List[BaseAgent] = []
        self.tasks: List[Task] = []
    
    @agent
    def dashboard_input_catcher(self) -> Agent:
        return Agent(
            config=self.agents_config['dashboard_input_catcher'], # type: ignore[index]
            llm=self.llm 
        )
    
    @agent
    def lead_research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_research_analyst'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )
    
    @agent
    def agent_content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_content_editor'], # type: ignore[index]
            llm=self.llm 
        )
    
    @agent
    def linkedin_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['LinkedIn_Scraper'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )
    
    @agent
    def verification_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['verification_specialist'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )

    @task
    def dashboard_input_processing_task(self) -> Task:
        return Task(
            config=self.tasks_config['dashboard_input_processing_task'], # type: ignore[index]
            agent=self.dashboard_input_catcher(),
            output_file="src/outputs/dashboard/user_input_analysis.json"
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            agent=self.lead_research_analyst(),
            output_file="src/outputs/lead_research_analyst/research_data.json"
        )
    
    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_generation_task'], # type: ignore[index]
            agent=self.agent_content_editor(),
            context=[self.research_task()],
            output_file="src/outputs/content/job_market_summary.md"
        )
    
    @task
    def linkedin_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_scraping_task'], # type: ignore[index]
            agent=self.linkedin_scraper(),
            output_file="src/outputs/linkedin/job_postings.md"
        )
    
    @task
    def research_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_verification_task'], # type: ignore[index]
            agent=self.verification_specialist(),
            context=[self.research_task(), self.content_generation_task()],
            output_file="src/outputs/verification/verification_report.md"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
        )
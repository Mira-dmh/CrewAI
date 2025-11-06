from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import yaml

import os
import yaml

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),  
    '..', 'config', 'research_agents.yaml'
)

with open(os.path.abspath(CONFIG_PATH), 'r') as f:
    agents_config = yaml.safe_load(f)

manager = Agent(
    config=agents_config['manager'], # type: ignore[index]
    allow_delegation=True,
)

@CrewBase
class JobResearchCrew:
    agents_config = '../config/research_agents.yaml'
    tasks_config = '../config/research_tasks.yaml'
    
    
    def __init__(self, llm):
        self.llm = llm  
        self.agents: List[BaseAgent] = []
        self.tasks: List[Task] = []
    
    

    @agent
    def lead_research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_research_analyst'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm
        )
        
    @agent
    def verification_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['verification_analyst'], # type: ignore[index]
            tools=[SerperDevTool(),FileReadTool(file_path="data/onet/onet_snapshot.json")],
            llm=self.llm
        )
    
    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['content_editor'], # type: ignore[index]
            llm=self.llm
        )
        
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            agent=self.lead_research_analyst(),
            output_file="src/outputs/lead_research_analyst/research_data.json"
        )
    
    @task
    def verify_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['verify_research_task'], # type: ignore[index]
            agent=self.verification_analyst(),
            context=[self.research_task()],
            output_file="src/outputs/verification_analyst/verification_score.json"
        )
        
    @task
    def content_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_generation_task'], # type: ignore[index]
            agent=self.content_editor(),
            tools=[FileReadTool(file_path="outputs/lead_research_analyst/research_data.json")],
            output_file="src/outputs/content/job_market_summary.json"
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            manager_agent=manager,
            process=Process.hierarchical,
            verbose=True
        )
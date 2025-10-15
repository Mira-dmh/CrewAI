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
    def lead_research_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_research_analyst'], # type: ignore[index]
            tools=[SerperDevTool()],
            llm=self.llm 
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            agent=self.lead_research_analyst()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
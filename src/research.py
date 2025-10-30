from Crew.research_crew import JobResearchCrew
from crewai import LLM


llm = LLM(
    model="gpt-4.1-mini"
)

job_title = "Data Analyst"
def run():
    crew = JobResearchCrew(llm=llm).crew()
    result = crew.kickoff(inputs={"job_title": job_title})
    #real input come from dashboard
    print(result)

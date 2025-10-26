from crew import JobResearchCrew
from crewai import LLM


llm = LLM(
    model="gpt-4.1-mini"
)


def run():
    print("running")
    crew = JobResearchCrew(llm=llm).crew()
    result = crew.kickoff(inputs={"job_title": "machine learning engineer"}) #fake input
    #real input come from dashboard
    print(result)

if __name__ == "__main__":
    run()
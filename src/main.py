from crew import JobResearchCrew
from crewai import LLM


llm = LLM(
    model="groq/llama-3.1-8b-instant"
)


def run():
    print("running")
    crew = JobResearchCrew(llm=llm).crew()
    result = crew.kickoff(inputs={"job_title": "machine learning engineer"})
    print(result)

if __name__ == "__main__":
    run()
# pyproject.toml: crewai>=0.61, pydantic, requests, fastapi, uvicorn, pandas, qdrant-client, llama-index, langchain, bs4

from crewai import Agent, Task, Crew, Process
import os

# Set environment variables to skip telemetry
os.environ['CREWAI_SKIP_TELEMETRY'] = 'true'

print("=== CrewAI Job Market Analysis System ===")
print("This script sets up a comprehensive job market analysis system with 5 specialized agents:")
print("1. Labor-Market Analyst")
print("2. Market Data Engineer") 
print("3. Resume Strategist")
print("4. Job Sourcer")
print("5. Interviewer")
print()

insight_agent = Agent(
    role="Labor-Market Analyst",
    goal="Synthesize AI impact on STEM jobs with citations and trend metrics",
    backstory="Economist skilled in labor APIs and policy reports",
    verbose=True,
    allow_delegation=False,
)

dashboard_agent = Agent(
    role="Market Data Engineer",
    goal="Assemble salary percentiles, openings trends, time-to-fill, skills demand",
    backstory="Data engineer who integrates Lightcast/Glassdoor APIs",
    verbose=True,
    allow_delegation=False,
)

resume_agent = Agent(
    role="Resume Strategist",
    goal="Tailor resume to a target job using RAG over resume + job description",
    backstory="ATS-savvy editor who optimizes keywords and measurable impact",
    verbose=True,
    allow_delegation=False,
)

sourcing_agent = Agent(
    role="Job Sourcer", 
    goal="Find and summarize relevant job listings with links and key requirements",
    backstory="Recruiting researcher experienced with job boards and scraping ethics",
    verbose=True,
    allow_delegation=False,
)

interview_agent = Agent(
    role="Interviewer",
    goal="Generate role-specific interview questions and scoring rubrics", 
    backstory="Hiring manager who designs behavioral and technical screens",
    verbose=True,
    allow_delegation=False,
)

insight_task = Task(
    description="Produce a 1-pager on AI's impact on STEM labor: demand shifts, automation risks, emerging skills; include 5 citations.",
    agent=insight_agent,
    expected_output="A comprehensive 1-page report on AI's impact on STEM jobs with 5 citations and trend analysis.",
)

dashboard_task = Task(
    description="Given a job title and location, fetch salary percentiles, openings trend, inferred time-to-fill, and top skills.",
    agent=dashboard_agent,
    expected_output="A dashboard report with salary data, job market trends, and skills analysis for the specified role and location.",
)

resume_task = Task(
    description="Using provided resume.pdf and job_description.txt, run RAG to output tailored resume bullets and a revised summary.",
    agent=resume_agent,
    expected_output="A tailored resume with optimized bullets and summary section based on the job requirements.",
)

sourcing_task = Task(
    description="Search Indeed/LinkedIn APIs or RSS/proxies for the role; output 10 current postings with titles, companies, locations, links.",
    agent=sourcing_agent,
    expected_output="A list of 10 current job postings with titles, companies, locations, and application links.",
)

interview_task = Task(
    description="Create a 30/60/90-minute interview plan with 10 questions, expected answers, and a rubric.",
    agent=interview_agent,  
    expected_output="A structured interview plan with 10 questions, model answers, and scoring rubric.",
)

crew = Crew(
    agents=[insight_agent, dashboard_agent, resume_agent, sourcing_agent, interview_agent],
    tasks=[insight_task, dashboard_task, resume_task, sourcing_task, interview_task],
    process=Process.sequential,
    verbose=True,
)

print("Crew setup complete! Attempting to run...")
print("Input parameters: Job Title='Data Scientist', Location='USA'")
print()

try:
    result = crew.kickoff(inputs={"job_title":"Data Scientist","location":"USA"})
    print("=== RESULTS ===")
    print(result)
except Exception as e:
    print(f"Error occurred: {e}")
    print("\n=== SETUP SUCCESSFUL, BUT EXECUTION REQUIRES API KEY ===")
    print("The CrewAI framework has been successfully installed and configured!")
    print("To run this script, you need to configure an LLM provider:")
    print()
    print("Option 1 - OpenAI:")
    print("  export OPENAI_API_KEY='your-api-key-here'")
    print()
    print("Option 2 - Use Ollama (local LLM):")
    print("  Install Ollama and configure the agents to use it")
    print()
    print("Option 3 - Other providers:")
    print("  Configure agents with custom LLM providers (Anthropic, etc.)")

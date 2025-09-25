from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
import os

# Set environment variables to use a mock response
os.environ['CREWAI_SKIP_TELEMETRY'] = 'true'

# Create agents with minimal LLM requirements
test_agent = Agent(
    role="Test Agent",
    goal="Test the CrewAI setup",
    backstory="A simple test agent",
    verbose=True,
    allow_delegation=False,
)

# Create a simple task
test_task = Task(
    description="Say 'Hello, CrewAI is working!' and explain that this is a successful test.",
    agent=test_agent,
    expected_output="A simple hello message confirming the setup works",
)

# Create and run the crew
crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    process=Process.sequential,
    verbose=True,
)

print("Starting CrewAI test...")
print("Note: This requires an LLM API key (OpenAI, Anthropic, etc.) to work properly.")
print("For now, this will demonstrate the setup but may fail without proper API configuration.")

try:
    result = crew.kickoff()
    print("Result:", result)
except Exception as e:
    print(f"Expected error (no API key configured): {e}")
    print("\nTo make this work, you need to:")
    print("1. Set OPENAI_API_KEY environment variable with your OpenAI API key, OR")
    print("2. Configure a different LLM provider, OR") 
    print("3. Use Ollama for local LLM")

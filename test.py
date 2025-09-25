from crewai import Agent, Task, Crew, Process

# Create a simple agent
test_agent = Agent(
    role="Test Agent",
    goal="Test the CrewAI setup",
    backstory="A simple test agent",
)

# Create a simple task
test_task = Task(
    description="Say hello and confirm CrewAI is working",
    agent=test_agent,
    expected_output="A simple hello message confirming the setup works",
)

# Create and run the crew
crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    process=Process.sequential,
)

print("Starting CrewAI test...")
result = crew.kickoff()
print("Result:", result)

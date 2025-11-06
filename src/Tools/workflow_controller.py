"""
Workflow Controller for Dashboard Input Processing
Handles routing user input to appropriate agent workflows
"""

import json
from typing import Dict, Any, List
import sys
import os

# Add the parent directory to the Python path to import crew
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crew import JobResearchCrew

class WorkflowController:
    """
    Controls the workflow routing based on dashboard input analysis
    """
    
    def __init__(self, llm):
        self.crew = JobResearchCrew(llm)
        self.llm = llm
    
    def process_dashboard_input(self, user_input: str, location: str = None) -> Dict[str, Any]:
        """
        Process user input from dashboard and route to appropriate workflow
        
        Args:
            user_input: Raw user input from dashboard
            location: Optional location parameter
            
        Returns:
            Dictionary containing workflow results
        """
        
        # Step 1: Analyze user input
        input_analysis = self._analyze_user_input(user_input, location)
        
        # Step 2: Route to appropriate workflow
        if input_analysis.get("request_type") == "job_research":
            return self._execute_job_research_workflow(input_analysis)
        elif input_analysis.get("request_type") == "location_search":
            return self._execute_location_search_workflow(input_analysis)
        else:
            return {"error": "Unable to determine request type", "analysis": input_analysis}
    
    def _analyze_user_input(self, user_input: str, location: str = None) -> Dict[str, Any]:
        """
        Use dashboard_input_catcher agent to analyze user input
        """
        # Create input analysis task
        analysis_task = self.crew.dashboard_input_processing_task()
        
        # Execute with user input
        input_data = {
            "user_input": user_input,
            "location": location or ""
        }
        
        # Run the analysis
        result = analysis_task.execute_sync(input_data)
        
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # Fallback parsing if JSON is malformed
            return {
                "request_type": "job_research" if location is None else "location_search",
                "job_title": user_input,
                "location": location or "",
                "keywords": user_input.split(),
                "routing_recommendation": "lead_research_analyst" if location is None else "linkedin_scraper",
                "processed_query": user_input
            }
    
    def _execute_job_research_workflow(self, input_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute job research workflow for general market analysis
        """
        job_title = input_analysis.get("job_title", "")
        
        # Execute research task
        research_task = self.crew.research_task()
        research_result = research_task.execute_sync({"job_title": job_title})
        
        # Execute content generation task
        content_task = self.crew.content_generation_task()
        content_result = content_task.execute_sync({"research_data": research_result})
        
        # Execute verification task
        verification_task = self.crew.research_verification_task()
        verification_result = verification_task.execute_sync({
            "research_data": research_result,
            "content": content_result
        })
        
        return {
            "workflow_type": "job_research",
            "input_analysis": input_analysis,
            "research_data": research_result,
            "formatted_content": content_result,
            "verification": verification_result,
            "output_files": {
                "research": "src/outputs/lead_research_analyst/research_data.json",
                "content": "src/outputs/content/job_market_summary.md",
                "verification": "src/outputs/verification/verification_report.md"
            }
        }
    
    def _execute_location_search_workflow(self, input_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute location-based job search workflow
        """
        job_title = input_analysis.get("job_title", "")
        location = input_analysis.get("location", "")
        
        # Execute LinkedIn scraping task
        linkedin_task = self.crew.linkedin_scraping_task()
        linkedin_result = linkedin_task.execute_sync({
            "job_title": job_title,
            "location": location
        })
        
        # Execute verification task for LinkedIn results
        verification_task = self.crew.research_verification_task()
        verification_result = verification_task.execute_sync({
            "linkedin_data": linkedin_result
        })
        
        return {
            "workflow_type": "location_search",
            "input_analysis": input_analysis,
            "job_postings": linkedin_result,
            "verification": verification_result,
            "output_files": {
                "job_postings": "src/outputs/linkedin/job_postings.md",
                "verification": "src/outputs/verification/verification_report.md"
            }
        }
    
    def get_available_workflows(self) -> List[str]:
        """
        Return list of available workflow types
        """
        return ["job_research", "location_search"]
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get current status of all agents and tasks
        """
        return {
            "agents": {
                "dashboard_input_catcher": "active",
                "lead_research_analyst": "active", 
                "agent_content_editor": "active",
                "linkedin_scraper": "active",
                "verification_specialist": "active"
            },
            "workflows": {
                "job_research": "available",
                "location_search": "available"
            },
            "output_directories": [
                "src/outputs/dashboard",
                "src/outputs/lead_research_analyst",
                "src/outputs/content",
                "src/outputs/linkedin", 
                "src/outputs/verification"
            ]
        }

# Example usage function
def example_usage():
    """
    Example of how to use the WorkflowController
    """
    from crewai import LLM
    
    # Initialize LLM using CrewAI (replace with your preferred configuration)
    llm = LLM(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    
    # Create workflow controller
    controller = WorkflowController(llm)
    
    # Example 1: Job research workflow
    print("=== Job Research Workflow ===")
    result1 = controller.process_dashboard_input("Machine Learning Engineer")
    print(f"Result: {result1}")
    
    # Example 2: Location search workflow  
    print("\n=== Location Search Workflow ===")
    result2 = controller.process_dashboard_input("Data Scientist", "San Francisco, CA")
    print(f"Result: {result2}")
    
    # Check workflow status
    print("\n=== Workflow Status ===")
    status = controller.get_workflow_status()
    print(f"Status: {status}")

if __name__ == "__main__":
    example_usage()
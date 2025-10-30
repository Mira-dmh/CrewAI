"""
Crew Factory - Utility for creating and managing different CrewAI instances
"""

from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

class CrewFactory:
    """Factory class for creating different types of CrewAI instances"""
    
    @staticmethod
    def create_llm(model: str = "gpt-4o-mini", temperature: float = 0.7):
        """Create and return an LLM instance"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return LLM(model=model, temperature=temperature)
    
    @staticmethod
    def create_main_crew(llm=None):
        """Create and return a MainCrew instance for general job research"""
        if llm is None:
            llm = CrewFactory.create_llm()
        # Lazy import to avoid import-time path issues
        from crew import MainCrew
        return MainCrew(llm=llm)
    
    @staticmethod
    def create_linkedin_crew(llm=None):
        """Create and return a LinkedInSearchCrew instance for LinkedIn-specific searches"""
        if llm is None:
            llm = CrewFactory.create_llm()
        # Lazy import to avoid circular imports
        from .linkedin_search_crew import LinkedInSearchCrew
        return LinkedInSearchCrew(llm=llm)
    
    @staticmethod
    def get_crew_for_search_type(search_type: str, llm=None):
        """
        Get the appropriate crew based on search type
        
        Args:
            search_type (str): 'linkedin', 'general', or 'market_research'
            llm: Optional LLM instance
            
        Returns:
            Appropriate CrewAI instance
        """
        if search_type.lower() in ['linkedin', 'linkedin_search', 'job_search']:
            return CrewFactory.create_linkedin_crew(llm)
        else:
            return CrewFactory.create_main_crew(llm)
    
    @staticmethod
    def is_crewai_available():
        """Check if CrewAI and required dependencies are available"""
        try:
            from crewai import LLM
            return os.getenv("OPENAI_API_KEY") is not None
        except ImportError:
            return False
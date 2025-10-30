"""
Crew Module - Specialized CrewAI Teams
Contains different crew configurations for various job search functionalities
"""

from .linkedin_search_crew import LinkedInSearchCrew
from .crew_factory import CrewFactory

__all__ = ['LinkedInSearchCrew', 'CrewFactory']
"""
Location Verification Tool - Validates if job location matches user's search location
"""

from typing import Type, Dict, List, ClassVar
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import json


class LocationVerificationInput(BaseModel):
    """Input schema for location verification"""
    search_location: str = Field(..., description="User's search location (e.g., 'CA', 'San Francisco')")
    actual_location: str = Field(..., description="Actual job location from LinkedIn (e.g., 'Toronto, Ontario')")


class LocationVerificationTool(BaseTool):
    name: str = "Verify Job Location Match"
    description: str = """Verify if the actual job location matches the user's search location.
    
    This tool helps identify location mismatches, such as:
    - CA (California) vs CA (Canada)
    - Toronto (Canada) when searching for California jobs
    - New York when searching for California
    
    Input should be a dict with:
    - search_location: User's original search (e.g., 'CA')
    - actual_location: Real location from LinkedIn (e.g., 'Toronto, Ontario')
    
    Returns JSON with match status and confidence score.
    """
    args_schema: Type[BaseModel] = LocationVerificationInput
    
    # US states mapping (ClassVar to avoid Pydantic validation)
    US_STATES: ClassVar[Dict[str, str]] = {
        "CA": "California", "NY": "New York", "TX": "Texas", "FL": "Florida",
        "IL": "Illinois", "PA": "Pennsylvania", "OH": "Ohio", "GA": "Georgia",
        "NC": "North Carolina", "MI": "Michigan", "NJ": "New Jersey", "VA": "Virginia",
        "WA": "Washington", "AZ": "Arizona", "MA": "Massachusetts", "TN": "Tennessee",
        "IN": "Indiana", "MO": "Missouri", "MD": "Maryland", "WI": "Wisconsin",
        "CO": "Colorado", "MN": "Minnesota", "SC": "South Carolina", "AL": "Alabama",
        "LA": "Louisiana", "KY": "Kentucky", "OR": "Oregon", "OK": "Oklahoma",
        "CT": "Connecticut", "UT": "Utah", "IA": "Iowa", "NV": "Nevada",
        "AR": "Arkansas", "MS": "Mississippi", "KS": "Kansas", "NM": "New Mexico",
        "NE": "Nebraska", "WV": "West Virginia", "ID": "Idaho", "HI": "Hawaii",
        "NH": "New Hampshire", "ME": "Maine", "MT": "Montana", "RI": "Rhode Island",
        "DE": "Delaware", "SD": "South Dakota", "ND": "North Dakota", "AK": "Alaska",
        "VT": "Vermont", "WY": "Wyoming"
    }
    
    # Canadian provinces (ClassVar)
    CANADIAN_PROVINCES: ClassVar[Dict[str, str]] = {
        "ON": "Ontario", "QC": "Quebec", "BC": "British Columbia", "AB": "Alberta",
        "MB": "Manitoba", "SK": "Saskatchewan", "NS": "Nova Scotia", "NB": "New Brunswick",
        "NL": "Newfoundland and Labrador", "PE": "Prince Edward Island", "NT": "Northwest Territories",
        "YT": "Yukon", "NU": "Nunavut"
    }
    
    # Major Canadian cities (ClassVar)
    CANADIAN_CITIES: ClassVar[List[str]] = [
        "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa",
        "Winnipeg", "Quebec City", "Hamilton", "Kitchener", "London", "Victoria",
        "Halifax", "Oshawa", "Windsor", "Saskatoon", "Regina", "Sherbrooke"
    ]

    def _run(self, search_location: str, actual_location: str) -> str:
        """
        Verify if actual location matches search location.
        
        Args:
            search_location: User's search input (e.g., 'CA')
            actual_location: Real location from LinkedIn (e.g., 'Toronto, Ontario')
            
        Returns:
            JSON string with verification results
        """
        # Normalize inputs
        search_loc = search_location.strip()
        actual_loc = actual_location.strip()
        
        # If actual location is "Not specified", uncertain match
        if actual_loc in ["Not specified", "", "Any"]:
            return json.dumps({
                "match_status": "UNCERTAIN",
                "match_confidence": 0.5,
                "search_location": search_loc,
                "actual_location": actual_loc,
                "reason": "Job location not specified in posting"
            })
        
        # Convert search location to uppercase for state code comparison
        search_upper = search_loc.upper()
        
        # Check if actual location is in Canada
        is_canada = any(city in actual_loc for city in self.CANADIAN_CITIES) or \
                   any(prov in actual_loc for prov in self.CANADIAN_PROVINCES.values()) or \
                   "Canada" in actual_loc
        
        # If searching for CA (California) but job is in Canada
        if search_upper == "CA" and is_canada:
            return json.dumps({
                "match_status": "MISMATCH",
                "match_confidence": 0.0,
                "search_location": search_loc,
                "actual_location": actual_loc,
                "reason": "CA refers to California (US), but job is in Canada. Provinces like Ontario, Alberta are in Canada.",
                "recommendation": "REJECT this job - location does not match user's search intent"
            })
        
        # Check if search is a US state code
        if search_upper in self.US_STATES:
            state_name = self.US_STATES[search_upper]
            
            # Check if actual location contains the state code or full name
            if search_upper in actual_loc.upper() or state_name in actual_loc:
                return json.dumps({
                    "match_status": "MATCH",
                    "match_confidence": 1.0,
                    "search_location": search_loc,
                    "actual_location": actual_loc,
                    "reason": f"Job is in {state_name} ({search_upper}), matches user search"
                })
            else:
                return json.dumps({
                    "match_status": "MISMATCH",
                    "match_confidence": 0.0,
                    "search_location": search_loc,
                    "actual_location": actual_loc,
                    "reason": f"User searched for {state_name} ({search_upper}), but job is in {actual_loc}",
                    "recommendation": "REJECT this job - location does not match"
                })
        
        # Check if search is a city name
        if search_loc in actual_loc:
            return json.dumps({
                "match_status": "MATCH",
                "match_confidence": 0.9,
                "search_location": search_loc,
                "actual_location": actual_loc,
                "reason": f"City name '{search_loc}' found in job location"
            })
        
        # Partial match - uncertain
        return json.dumps({
            "match_status": "UNCERTAIN",
            "match_confidence": 0.5,
            "search_location": search_loc,
            "actual_location": actual_loc,
            "reason": "Unable to confidently determine if locations match",
            "recommendation": "Manually verify this job's location before applying"
        })


# Create instance for import
verify_job_location_match = LocationVerificationTool()

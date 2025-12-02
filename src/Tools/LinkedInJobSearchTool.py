"""
LinkedIn Job Search Tool - Uses SerperDev with improved search strategy
This tool searches for specific LinkedIn job postings using targeted company searches
"""

import os
import json
import re
from datetime import datetime
from typing import Type, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import requests

load_dotenv()


class LinkedInSearchInput(BaseModel):
    """Input schema for LinkedIn job search"""
    job_title: str = Field(..., description="Job title to search for (required)")
    location: Optional[str] = Field("", description="Location to search in")
    company: Optional[str] = Field("", description="Specific company to search")
    job_type: Optional[str] = Field("", description="Job type: Full-time/Part-time/Internship/Contract/Temporary")
    remote_option: Optional[str] = Field("", description="Remote option: Remote/Hybrid/On-site")
    date_posted: Optional[str] = Field("", description="Date posted: Past 24 hours/Past week/Past month")
    work_authorization: Optional[str] = Field("", description="Work authorization requirements")


class LinkedInJobSearchTool(BaseTool):
    name: str = "Search LinkedIn Jobs with Filters"
    description: str = """Search LinkedIn for specific job postings using SerperDev with improved strategy.
    
    This tool uses an advanced search strategy that targets specific companies to find
    actual job posting URLs (linkedin.com/jobs/view/[ID]) instead of collection pages.
    
    Input should be a dict with:
    - job_title (required): Job title to search for
    - location (optional): Location
    - company (optional): Specific company
    - job_type (optional): Full-time/Part-time/Internship/Contract/Temporary
    - remote_option (optional): Remote/Hybrid/On-site
    - date_posted (optional): Past 24 hours/Past week/Past month
    - work_authorization (optional): Work authorization requirements
    """
    args_schema: Type[BaseModel] = LinkedInSearchInput
    output_dir: str = "src/outputs/linkedin"  # Default output directory
    
    def __init__(self, output_dir: str = None, **kwargs):
        """Initialize the tool with optional custom output directory"""
        super().__init__(**kwargs)
        if output_dir:
            self.output_dir = output_dir

    def _extract_location_from_text(self, title: str, snippet: str) -> str:
        """
        Extract actual location from LinkedIn job title or snippet.
        Common patterns: "City, State", "City, Province", "City, Country"
        """
        text = f"{title} {snippet}"
        
        # Pattern 1: City, State/Province (e.g., "San Francisco, CA" or "Toronto, Ontario")
        location_pattern = r'([A-Z][a-zA-Z\s]+),\s*([A-Z]{2}|[A-Z][a-zA-Z\s]+)'
        matches = re.findall(location_pattern, text)
        
        if matches:
            # Return first match (most likely to be correct)
            city, region = matches[0]
            return f"{city.strip()}, {region.strip()}"
        
        # Pattern 2: Just state/country codes (CA, NY, etc.)
        state_pattern = r'\b([A-Z]{2})\b'
        state_matches = re.findall(state_pattern, text)
        if state_matches:
            return state_matches[0]
        
        return "Not specified"
    
    def _run(self, job_title: str, location: str = "", company: str = "", 
             job_type: str = "", remote_option: str = "", date_posted: str = "",
             work_authorization: str = "") -> str:
        """
        Execute the LinkedIn job search with the provided parameters.
        
        Args:
            job_title: Job title to search for (required)
            location: Location to search in
            company: Specific company to search
            job_type: Job type filter
            remote_option: Remote work filter
            date_posted: Date posted filter
            work_authorization: Work authorization filter
            
        Returns:
            JSON string with job postings including actual LinkedIn URLs
        """
        # Build params dict
        params = {
            "job_title": job_title,
            "location": location,
            "company": company,
            "job_type": job_type,
            "remote_option": remote_option,
            "date_posted": date_posted,
            "work_authorization": work_authorization
        }
        
        # Get API key
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return json.dumps({"error": "SERPER_API_KEY not found in environment"})
        
        all_jobs = []
        max_jobs_target = 40  # Target: 40 job postings
        
        # STRATEGY 1: If user specifies a company, search only that company
        if company and company not in ["", "Any"]:
            # Build search query for specific company
            query = f'site:linkedin.com/jobs/view "{job_title}" "{company}"'
            if location:
                # Remove commas from location for SerperDev compatibility
                clean_location = location.replace(',', '')
                query += f' {clean_location}'
            
            try:
                response = requests.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": api_key,
                        "Content-Type": "application/json"
                    },
                    json={"q": query, "num": max_jobs_target}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("organic", [])
                    
                    for result in results:
                        url = result.get("link", "")
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")
                        
                        # Extract job_id from URL
                        match = re.search(r'/jobs/view/[^/]+-(\d+)', url)
                        if match:
                            job_id = match.group(1)
                            actual_location = self._extract_location_from_text(title, snippet)
                            
                            if not any(j["job_id"] == job_id for j in all_jobs):
                                all_jobs.append({
                                    "job_id": job_id,
                                    "job_title": title,
                                    "company_name": company,
                                    "location": actual_location,
                                    "search_location": location or "Any",
                                    "application_url": url,
                                    "job_description": snippet,
                                    "employment_type": params.get("job_type", "Not specified"),
                                    "work_arrangement": params.get("remote_option", "Not specified"),
                                    "date_posted": "Recent",
                                    "source": "LinkedIn"
                                })
            except Exception as e:
                print(f"Error searching {company}: {e}")
        
        # STRATEGY 2: General search without company restriction (DEFAULT)
        else:
            # Build general search query
            # Use site: to restrict to LinkedIn job view pages
            query = f'site:linkedin.com/jobs/view "{job_title}"'
            if location:
                # Remove commas from location - SerperDev doesn't like them in queries
                # "Philadelphia, PA" -> "Philadelphia PA"
                clean_location = location.replace(',', '')
                query += f' {clean_location}'
            
            # Add filters to query if specified
            if job_type and job_type not in ["", "Any"]:
                query += f' {job_type}'
            if remote_option and remote_option not in ["", "Any"]:
                query += f' {remote_option}'
            
            try:
                response = requests.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": api_key,
                        "Content-Type": "application/json"
                    },
                    json={"q": query, "num": 10}  # Max 10 results per query for SerperDev free tier
                )
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("organic", [])
                    
                    for result in results:
                        url = result.get("link", "")
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")
                        
                        # Extract company name from title
                        # LinkedIn titles typically: "Company hiring Job Title" or "Job Title - Company" or "Job Title at Company"
                        company_name = "Not specified"
                        
                        # Method 1: Pattern "Company hiring Job Title in Location"
                        if "hiring" in title.lower():
                            hiring_match = re.search(r'^(.+?)\s+hiring\s+', title, re.IGNORECASE)
                            if hiring_match:
                                company_name = hiring_match.group(1).strip()
                        
                        # Method 2: Extract from URL path (fallback)
                        # URLs like: linkedin.com/jobs/view/title-at-company-name-123456
                        if company_name == "Not specified":
                            url_match = re.search(r'/jobs/view/.+-at-([a-z0-9-]+)-\d+', url, re.IGNORECASE)
                            if url_match:
                                # Convert "avesta-computer-services" to "Avesta Computer Services"
                                company_name = url_match.group(1).replace('-', ' ').title()
                        
                        # Method 3: Pattern "Job Title at Company in Location"
                        if company_name == "Not specified" and " at " in title:
                            at_match = re.search(r'\bat\s+(.+?)(?:\s+in\s+|\s*$)', title, re.IGNORECASE)
                            if at_match:
                                company_name = at_match.group(1).strip()
                        
                        # Method 4: Pattern "Job Title - Company"
                        if company_name == "Not specified" and " - " in title:
                            parts = title.split(" - ")
                            if len(parts) >= 2:
                                # Sometimes last part is location, check for that
                                potential_company = parts[1].strip() if len(parts) == 2 else parts[-1].strip()
                                # Filter out common location indicators
                                if not any(loc in potential_company for loc in [", CA", ", NY", ", TX", "United States"]):
                                    company_name = potential_company
                        
                        # Extract job_id from URL
                        match = re.search(r'/jobs/view/[^/]+-(\d+)', url)
                        if match:
                            job_id = match.group(1)
                            
                            # Extract actual location from snippet or title
                            actual_location = self._extract_location_from_text(title, snippet)
                            
                            # Don't add duplicates
                            if not any(j["job_id"] == job_id for j in all_jobs):
                                all_jobs.append({
                                    "job_id": job_id,
                                    "job_title": title,
                                    "company_name": company_name,  # Extracted from title/snippet
                                    "location": actual_location,  # Real location from LinkedIn
                                    "search_location": location or "Any",  # User's search input
                                    "application_url": url,
                                    "job_description": snippet,
                                    "employment_type": params.get("job_type", "Not specified"),
                                    "work_arrangement": params.get("remote_option", "Not specified"),
                                    "date_posted": "Recent",
                                    "source": "LinkedIn"
                                })
            
            except Exception as e:
                print(f"Error searching general jobs: {e}")
        
        # Build result JSON
        result_data = {
            "search_metadata": {
                "job_title": job_title,
                "location": location or "Any",
                "company": company or "All companies (general search)",
                "job_type": params.get("job_type", "Any"),
                "remote_option": params.get("remote_option", "Any"),
                "date_posted": params.get("date_posted", "Any time"),
                "work_authorization": params.get("work_authorization", "Any"),
                "search_date": datetime.now().isoformat(),
                "total_results_found": len(all_jobs),
                "method": "serperdev_general_search" if not company else "serperdev_targeted_company_search"
            },
            "job_postings": all_jobs
        }
        
        # Save to file (use dynamic output directory)
        output_file = f"{self.output_dir}/job_postings.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        return json.dumps(result_data, indent=2, ensure_ascii=False)


# Create instance for import
search_linkedin_jobs_with_filters = LinkedInJobSearchTool()



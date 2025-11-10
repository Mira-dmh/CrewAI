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
        
        # Target companies list (can be customized)
        target_companies = [
            "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber",
            "LinkedIn", "Salesforce", "Oracle", "IBM", "Intel", "Adobe", "Cisco",
            "Dell", "HP", "VMware", "ServiceNow", "Workday", "Zoom"
        ]
        
        # If specific company provided, search only that company
        if company and company not in ["", "Any"]:
            target_companies = [company]
        
        all_jobs = []
        max_jobs_target = 40  # Target: 40 job postings
        
        # Search each company until we reach 40 jobs
        for comp in target_companies[:15]:  # Search more companies if needed
            if len(all_jobs) >= max_jobs_target:
                break  # Stop when we have enough jobs
                
            # Build search query: target /jobs/view specifically
            query = f'site:linkedin.com/jobs/view "{job_title}" {comp}'
            if location:
                query += f' {location}'
            
            try:
                response = requests.post(
                    "https://google.serper.dev/search",
                    headers={
                        "X-API-KEY": api_key,
                        "Content-Type": "application/json"
                    },
                    json={"q": query, "num": 10}  # 10 results per company
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
                            
                            # Don't add duplicates
                            if not any(j["job_id"] == job_id for j in all_jobs):
                                all_jobs.append({
                                    "job_id": job_id,
                                    "job_title": title,
                                    "company_name": comp,  # Searched company
                                    "location": location or "Not specified",
                                    "application_url": url,
                                    "job_description": snippet,
                                    "employment_type": params.get("job_type", "Not specified"),
                                    "work_arrangement": params.get("remote_option", "Not specified"),
                                    "date_posted": "Recent",
                                    "source": "LinkedIn"
                                })
            
            except Exception as e:
                print(f"Error searching {comp}: {e}")
                continue
        
        # Build result JSON
        result_data = {
            "search_metadata": {
                "job_title": job_title,
                "location": location or "Any",
                "company": company or f"Top {len(target_companies)} companies",
                "job_type": params.get("job_type", "Any"),
                "remote_option": params.get("remote_option", "Any"),
                "date_posted": params.get("date_posted", "Any time"),
                "work_authorization": params.get("work_authorization", "Any"),
                "search_date": datetime.now().isoformat(),
                "total_results_found": len(all_jobs),
                "method": "serperdev_targeted_company_search"
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



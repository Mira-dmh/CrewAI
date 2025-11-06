import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

USERNAME = os.getenv("ONET_USERNAME")
PASSWORD = os.getenv("ONET_PASSWORD")

BASE_URL = "https://services.onetcenter.org/ws"
keyword = "Data Scientist"

def search_top_job (keyword: str, start: int = 1, limit: int = 1):
    url = f"{BASE_URL}/online/search"
    params = {
        "keyword": keyword,
        "start": start,
        "end": start + limit - 1   
    }
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=params, headers=headers, auth=(USERNAME, PASSWORD)) # type: ignore[arg-type]
    response.raise_for_status()
    data = response.json()
    
    occupations = data.get("occupation", [])
    if occupations:
        top_job = occupations[0]  
        relevance = top_job["relevance_score"]
        if relevance > 95:
            soc_code = top_job["code"]
            job_data = get_occupation_data(soc_code)
            with open("src/data/onet/onet_snapshot.json", "w") as f:
                json.dump(job_data, f, indent=2)
            
        else: 
            return "No Relevant Jobs"
    else:
        return "No relevant Jobs"
        

        

def get_occupation_data(code):
    url = f"{BASE_URL}/online/occupations/{code}"
    params = {"details": "all"}
    headers = {"Accept": "application/json"}
    response = requests.get(url, params=params, auth=(USERNAME, PASSWORD), headers=headers) # type: ignore[arg-type]
    response.raise_for_status()
    return response.json()
import json
import os
from dotenv import load_dotenv

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

# load environment variables from .env file
load_dotenv()


class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    # check if the API key is available
    api_key = os.environ.get('BROWSERLESS_API_KEY')
    if not api_key:
        return "Error: BROWSERLESS_API_KEY not found in environment variables. Please check your .env file."
    
    url = f"https://chrome.browserless.io/content?token={api_key}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            return f"Error: Failed to fetch content. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: Network request failed - {str(e)}"
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing researches and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do a research about a given topic.",
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)



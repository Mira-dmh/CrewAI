import json
from pathlib import Path

DASHBOARD_FILE = Path(__file__).parent / "dashboard_data.json"

def save_json_output(agent_output, file_path=DASHBOARD_FILE):
    """
    Write the agent's JSON-ready output directly to the dashboard file.
    
    Args:
        agent_output (dict or list): Must be JSON-serializable.
        file_path (Path or str): File path to write to.
    """
    with open(file_path, "w") as f:
        json.dump(agent_output, f, indent=4)
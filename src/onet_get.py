
"""
O*NET Disabled Version
This module is kept only so that imports do not break.
All functions return safe fallback values.

Because O*NET credentials are not provided, all API calls are disabled.
"""

def search_top_job(keyword: str, start: int = 1, limit: int = 1):
    """
    Disabled fallback version.
    Always returns a safe response and prevents app crashes.
    """
    return {
        "status": "disabled",
        "message": "O*NET API is disabled (no credentials provided).",
        "results": []
    }


def get_occupation_data(code: str):
    """
    Disabled fallback for occupation data.
    """
    return {
        "status": "disabled",
        "message": "O*NET API is disabled (no credentials provided).",
        "occupation_code": code,
        "details": {}
    }
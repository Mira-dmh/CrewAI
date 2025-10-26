"""
Session Manager - Handles user session tracking and storage
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

# Helper function for easy session tracking from any page
def track_page_visit(page_name: str, action: str = "visited"):
    """
    Quick function to track page visits and actions
    """
    try:
        session_manager.add_session(
            session_type="navigation",
            title=f"{page_name} {action.title()}",
            details=f"User {action} {page_name} page",
            job_title="",
            location="",
            results_count=0,
            duration_minutes=1
        )
    except Exception:
        pass  # Fail silently if session tracking is unavailable

class SessionManager:
    """Manages user sessions with JSON file storage"""
    
    def __init__(self, sessions_file_path: str = None):
        """Initialize session manager with file path"""
        if sessions_file_path is None:
            # Default path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.sessions_file = os.path.join(current_dir, "data", "user_sessions.json")
        else:
            self.sessions_file = sessions_file_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.sessions_file), exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not os.path.exists(self.sessions_file):
            self._create_initial_file()
    
    def _create_initial_file(self):
        """Create initial sessions file with empty structure"""
        initial_data = {
            "sessions": [],
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_sessions": 0,
                "version": "1.0"
            }
        }
        with open(self.sessions_file, 'w') as f:
            json.dump(initial_data, f, indent=2)
    
    def load_sessions(self) -> Dict:
        """Load sessions from JSON file"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._create_initial_file()
            return self.load_sessions()
    
    def save_sessions(self, data: Dict):
        """Save sessions to JSON file"""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        data["metadata"]["total_sessions"] = len(data["sessions"])
        
        with open(self.sessions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_session(self, session_type: str, title: str, details: str, 
                   job_title: str = "", location: str = "", 
                   results_count: int = 0, duration_minutes: int = 0) -> str:
        """Add a new session record"""
        
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        new_session = {
            "id": session_id,
            "timestamp": datetime.now().isoformat(),
            "type": session_type,
            "title": title,
            "details": details,
            "job_title": job_title,
            "location": location,
            "results_count": results_count,
            "duration_minutes": duration_minutes,
            "status": "completed"
        }
        
        data = self.load_sessions()
        data["sessions"].insert(0, new_session)  # Add to beginning (most recent first)
        
        # Keep only last 50 sessions to prevent file from getting too large
        if len(data["sessions"]) > 50:
            data["sessions"] = data["sessions"][:50]
        
        self.save_sessions(data)
        return session_id
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Get recent sessions, limited by count"""
        data = self.load_sessions()
        return data["sessions"][:limit]
    
    def get_sessions_by_type(self, session_type: str) -> List[Dict]:
        """Get sessions filtered by type"""
        data = self.load_sessions()
        return [s for s in data["sessions"] if s["type"] == session_type]
    
    def get_sessions_by_date(self, days_back: int = 7) -> List[Dict]:
        """Get sessions from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        data = self.load_sessions()
        
        recent_sessions = []
        for session in data["sessions"]:
            session_date = datetime.fromisoformat(session["timestamp"].replace('Z', '+00:00'))
            if session_date >= cutoff_date:
                recent_sessions.append(session)
        
        return recent_sessions
    
    def get_session_stats(self) -> Dict:
        """Get statistics about sessions"""
        data = self.load_sessions()
        sessions = data["sessions"]
        
        if not sessions:
            return {
                "total_sessions": 0,
                "sessions_today": 0,
                "sessions_this_week": 0,
                "most_common_type": "None",
                "average_duration": 0
            }
        
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        sessions_today = 0
        sessions_this_week = 0
        type_counts = {}
        total_duration = 0
        
        for session in sessions:
            session_date = datetime.fromisoformat(session["timestamp"].replace('Z', '+00:00')).date()
            
            if session_date == today:
                sessions_today += 1
            if session_date >= week_ago:
                sessions_this_week += 1
            
            session_type = session["type"]
            type_counts[session_type] = type_counts.get(session_type, 0) + 1
            total_duration += session.get("duration_minutes", 0)
        
        most_common_type = max(type_counts, key=type_counts.get) if type_counts else "None"
        average_duration = total_duration / len(sessions) if sessions else 0
        
        return {
            "total_sessions": len(sessions),
            "sessions_today": sessions_today,
            "sessions_this_week": sessions_this_week,
            "most_common_type": most_common_type,
            "average_duration": round(average_duration, 1)
        }
    
    def format_session_for_display(self, session: Dict) -> str:
        """Format a session for display in the UI"""
        timestamp = datetime.fromisoformat(session["timestamp"].replace('Z', '+00:00'))
        
        # Format time
        if timestamp.date() == datetime.now().date():
            time_str = timestamp.strftime("%I:%M %p")
        elif timestamp.date() == (datetime.now().date() - timedelta(days=1)):
            time_str = "Yesterday"
        else:
            time_str = timestamp.strftime("%b %d")
        
        # Session type icons
        type_icons = {
            "job_search": "🔍",
            "market_analysis": "📊",
            "resume_optimization": "📝",
            "profile_enhancement": "👤",
            "salary_research": "💰",
            "interview_prep": "🎯"
        }
        
        icon = type_icons.get(session["type"], "📋")
        
        return f"**{time_str}** {icon} {session['title']}"

# Global session manager instance
session_manager = SessionManager()
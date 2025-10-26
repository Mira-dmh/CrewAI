"""
CrewAI Job Search Assistant - Main Entry Point
This file imports and runs the main application from src/app.py
"""

import sys
import os

# Get the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add src to Python path so imports work correctly
sys.path.insert(0, os.path.join(script_dir, 'src'))

# Import and run the main application
exec(open(os.path.join(script_dir, 'src', 'app.py')).read())
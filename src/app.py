"""
CrewAI Job Search Assistant - AI-Powered Job Search Platform
Main entry point for the multipage app with integrated CrewAI agents and tasks
"""

import streamlit as st
from streamlit_pages.home import home_page
from streamlit_pages.job_search import job_search_page
from streamlit_pages.analytics import analytics_page
from streamlit_pages.settings import settings_page
from streamlit_pages.specific_jobs import specific_jobs_page
from streamlit_pages.resume_prep import resume_prep_page

# Configure the main app
st.set_page_config(
    page_title="CrewAI Job Search Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user preferences
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {
        "theme": "light",
        "show_tips": True,
        "last_visited": None
    }

# Track current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# URL-based page routing - no need for st.Page definitions

# Handle URL-based navigation
current_page = st.query_params.get("page", "home")

# Create sidebar navigation
with st.sidebar:
    st.markdown("## 📍 Navigation")
    
    # Main section
    st.markdown("### Main")
    home_button_type = "primary" if current_page == "home" else "secondary"
    if st.button("🏠 Home", key="nav_home", use_container_width=True, type=home_button_type):
        st.query_params.page = "home"
        st.rerun()
    
    # Services section
    st.markdown("### Services")   
    job_search_button_type = "primary" if current_page == "info_page" else "secondary"
    if st.button("🔍 Job Research Assistant", key="nav_info_page", use_container_width=True, type=job_search_button_type):
        st.query_params.page = "job_search"
        st.rerun()
    
    specific_button_type = "primary" if current_page == "Specific_Jobs" else "secondary"
    if st.button("🎯 Specific Jobs", key="nav_specific", use_container_width=True, type=specific_button_type):
        st.query_params.page = "Specific_Jobs"
        st.rerun()
    
    resume_button_type = "primary" if current_page == "Resume_Prep" else "secondary"
    if st.button("📝 Resume Prep", key="nav_resume", use_container_width=True, type=resume_button_type):
        st.query_params.page = "Resume_Prep"
        st.rerun()
    
    # Analytics & Settings section
    st.markdown("### Analytics & Settings")
    analytics_button_type = "primary" if current_page == "analytics" else "secondary"
    if st.button("📊 Job Market Analytics", key="nav_analytics", use_container_width=True, type=analytics_button_type):
        st.query_params.page = "analytics"
        st.rerun()
    
    settings_button_type = "primary" if current_page == "settings" else "secondary"
    if st.button("⚙️ Settings", key="nav_settings", use_container_width=True, type=settings_button_type):
        st.query_params.page = "settings"
        st.rerun()

# Page routing function
def route_to_page():
    """Route to the appropriate page based on URL parameter"""
    if current_page == "job_search":
        job_search_page()
    elif current_page == "Specific_Jobs":
        specific_jobs_page()
    elif current_page == "Resume_Prep":
        resume_prep_page()
    elif current_page == "analytics":
        analytics_page()
    elif current_page == "settings":
        settings_page()
    else:  # Default to home
        home_page()

# Add some shared styling and header
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 2rem;
    }
    .nav-section {
        padding: 0.5rem 0;
        border-bottom: 1px solid #e6e9ef;
        margin-bottom: 1rem;
    }
    /* Custom sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Custom button styling */
    .stButton button {
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Shared header for all pages
with st.container():
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🤖 CrewAI Job Search Assistant")
    st.markdown("*Your AI-powered career companion*")
    st.markdown('</div>', unsafe_allow_html=True)

# Add breadcrumb navigation
def show_breadcrumb():
    """Display breadcrumb navigation"""
    current_url = st.query_params.get("page", "home")
    
    breadcrumb_map = {
        "home": "🏠 Home",
        "job_search": "🏠 Home > 🔍 Job Search Assistant", 
        "Specific_Jobs": "🏠 Home > 🎯 Specific Jobs",
        "Resume_Prep": "🏠 Home > 📝 Resume Prep",
        "analytics": "🏠 Home > 📊 Analytics",
        "settings": "🏠 Home > ⚙️ Settings"
    }
    
    if current_url in breadcrumb_map:
        st.markdown(f"**{breadcrumb_map[current_url]}**")
        st.markdown("---")

show_breadcrumb()

# Run the selected page
route_to_page()